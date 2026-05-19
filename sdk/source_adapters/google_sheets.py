from __future__ import annotations

import csv
import importlib
import os
import re
from pathlib import Path
from urllib.parse import urlparse

from source_manifest import GoogleSheetRef, SourceItem


SHEET_ID_RE = re.compile(r"/spreadsheets/d/([a-zA-Z0-9-_]+)")


def parse_spreadsheet_id(value: str) -> str:
    match = SHEET_ID_RE.search(value)
    if match:
        return match.group(1)
    if re.fullmatch(r"[a-zA-Z0-9-_]{20,}", value):
        return value
    parsed = urlparse(value)
    if parsed.netloc:
        raise ValueError(f"Cannot parse Google Sheet ID from URL: {value}")
    raise ValueError(f"Invalid Google Sheet ID or URL: {value}")


def build_google_sheet_source(source_id: str, url_or_id: str, tab: str | None = None, range_name: str | None = None) -> SourceItem:
    spreadsheet_id = parse_spreadsheet_id(url_or_id)
    return SourceItem(
        id=source_id,
        kind="google_sheet",
        original_locator=url_or_id,
        google_sheet=GoogleSheetRef(spreadsheet_id=spreadsheet_id, url=url_or_id, tab=tab, range=range_name),
        extension=".gsheet",
    )


def _credentials(scopes: list[str]):
    service_account_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    oauth_token_path = os.environ.get("GOOGLE_OAUTH_TOKEN_JSON")
    if service_account_path:
        module = importlib.import_module("google.oauth2.service_account")
        return module.Credentials.from_service_account_file(service_account_path, scopes=scopes)
    if oauth_token_path:
        module = importlib.import_module("google.oauth2.credentials")
        return module.Credentials.from_authorized_user_file(oauth_token_path, scopes=scopes)
    raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_OAUTH_TOKEN_JSON to use Google Sheets.")


def _service(scopes: list[str]):
    try:
        from googleapiclient.discovery import build
    except ImportError as exc:
        raise RuntimeError("Google Sheets support requires google-api-python-client.") from exc
    return build("sheets", "v4", credentials=_credentials(scopes))


def export_sheet_to_tsv(source: SourceItem, output_path: Path) -> Path:
    if source.google_sheet is None:
        raise ValueError("Source is not a Google Sheet source")
    service = _service(["https://www.googleapis.com/auth/spreadsheets.readonly"])
    sheet_range = source.google_sheet.range or source.google_sheet.tab or "A:Z"
    result = service.spreadsheets().values().get(spreadsheetId=source.google_sheet.spreadsheet_id, range=sheet_range).execute()
    values = result.get("values", [])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(values)
    source.google_sheet.exported_path = str(output_path)
    source.local_path = str(output_path)
    source.extension = ".tsv"
    if values:
        source.fingerprint.detected_headers = [str(v).strip() for v in values[0]]
    return output_path


def write_tsv_to_new_sheet(spreadsheet_id: str, tab_name: str, tsv_path: Path) -> dict:
    service = _service(["https://www.googleapis.com/auth/spreadsheets"])
    with tsv_path.open("r", encoding="utf-8-sig", newline="") as f:
        values = list(csv.reader(f, delimiter="\t"))
    add_body = {"requests": [{"addSheet": {"properties": {"title": tab_name}}}]}
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=add_body).execute()
    update_body = {"values": values}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{tab_name}'!A1",
        valueInputOption="RAW",
        body=update_body,
    ).execute()
    return {"spreadsheet_id": spreadsheet_id, "tab_name": tab_name, "updated_cells": result.get("updatedCells", 0)}
