#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "office_rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

HEADER_ALIASES = {
    "Test Case / Summary": "Test Case Summary",
    "Expected / result": "Expected result",
    "Manual Test Results / Round 1": "Manual Test Results Round 1",
    "Notes ": "Notes",
    "Test Data": "Test Datas",
}

LEGACY_19_HEADERS = [
    "Test Case ID",
    "Function",
    "Group Tests",
    "Scenario Outline",
    "Test Case Summary",
    "Pre-conditions",
    "Test Datas",
    "Test Steps",
    "Expected result",
    "Environment",
    "Priority",
    "Regression",
    "Automation",
    "Manual Test Results Round 1",
    "Manual Test Results Round 2",
    "Automation Test Results",
    "Actual result",
    "BugID",
    "Notes",
]

PAYGATES_SHEETS = [
    "Tổng hợp chung",
    "Squad_Tester",
    "Squad_Base",
    "Tổng Hợp Test Case Theo Sprint",
    "Tổng Hợp Test Case Automation T",
    "Squad_VA",
    "Squad_CnR",
    "Squad_DevPortal",
    "Squad_BO",
    "Sprint 8",
]

STATUS_ALIASES = {
    "Read to UAT": "Ready to UAT",
    "AI Gen": "AI gen",
    "In - Progress": "In-Progress",
    "UI": "Web UI",
}

API_ID_RE = re.compile(r"^TD_P[123]_\d{3}_TC_\d{3}$")
UI_ID_RE = re.compile(r"^TD_\d{3}_TC_\d{3}$")


def normalize_header(header: str) -> str:
    stripped = header.strip()
    return HEADER_ALIASES.get(header, HEADER_ALIASES.get(stripped, stripped))


def classify_workbook(path: Path, sheets: list[dict]) -> str:
    lower = path.as_posix().lower()
    if "tổng hợp trạng thái test case paygates" in lower:
        return "paygates_tracker"
    if lower.endswith("-tcs.xlsx") or "testcase" in lower or "test case" in lower:
        return "legacy_testcase"
    sheet_names = {sheet["name"] for sheet in sheets}
    if any(name in sheet_names for name in PAYGATES_SHEETS):
        return "paygates_tracker"
    return "xlsx_reference"


def profile_workbook(path: Path) -> dict:
    with zipfile.ZipFile(path) as z:
        shared = read_shared_strings(z)
        formulas_by_sheet = read_formulas(z)
        sheets = []
        for sheet_name, sheet_path in workbook_sheets(z):
            rows = read_sheet_rows(z, sheet_path, shared)
            non_empty = [row for row in rows if any(cell.strip() for cell in row)]
            header_row = find_header_row(non_empty)
            headers = header_row or []
            normalized_headers = [normalize_header(header) for header in headers]
            id_findings = collect_id_findings(non_empty, normalized_headers)
            status_values = collect_status_values(non_empty)
            formulas = formulas_by_sheet.get(sheet_path, [])
            overflow_columns = max((len(row) for row in rows), default=0) if normalized_headers[:19] == LEGACY_19_HEADERS else 0
            sheets.append({
                "name": sheet_name,
                "row_count": len(non_empty),
                "column_count": max((len(row) for row in rows), default=0),
                "headers": headers,
                "normalized_headers": normalized_headers,
                "header_aliases": alias_records(headers),
                "status_values": status_values,
                "status_aliases": status_alias_records(status_values),
                "formulas": formulas,
                "overflow_columns": max(0, overflow_columns - 19),
                "id_findings": id_findings,
            })
    workbook_type = classify_workbook(path, sheets)
    return {
        "path": path.as_posix(),
        "workbook_type": workbook_type,
        "sheet_count": len(sheets),
        "sheets": sheets,
        "paygates_missing_sheets": missing_paygates_sheets(sheets) if workbook_type == "paygates_tracker" else [],
        "formula_warnings": formula_warnings(sheets),
    }


def alias_records(headers: list[str]) -> list[dict[str, str]]:
    records = []
    for header in headers:
        normalized = normalize_header(header)
        if normalized != header:
            records.append({"source": header, "normalized": normalized})
    return records


def status_alias_records(status_values: list[str]) -> list[dict[str, str]]:
    return [{"source": value, "normalized": STATUS_ALIASES[value]} for value in status_values if value in STATUS_ALIASES]


def collect_status_values(rows: list[list[str]]) -> list[str]:
    known = set(STATUS_ALIASES) | set(STATUS_ALIASES.values()) | {"Pending", "In-Test", "Update test cases", "Test case out of date", "Completed", "Manual", "AI gen + Manual", "API", "Web UI"}
    return sorted({cell.strip() for row in rows for cell in row if cell.strip() in known})


def collect_id_findings(rows: list[list[str]], headers: list[str]) -> list[dict[str, str]]:
    if "Test Case ID" not in headers:
        return []
    idx = headers.index("Test Case ID")
    findings = []
    for row_no, row in enumerate(rows[1:], start=2):
        if idx >= len(row):
            continue
        raw = row[idx]
        trimmed = raw.strip()
        if not trimmed:
            continue
        if raw != trimmed:
            findings.append({"row": str(row_no), "type": "leading_or_trailing_space", "value": raw, "normalized": trimmed})
        if not (API_ID_RE.match(trimmed) or UI_ID_RE.match(trimmed)):
            findings.append({"row": str(row_no), "type": "id_pattern_mismatch", "value": raw, "normalized": trimmed})
    return findings


def missing_paygates_sheets(sheets: list[dict]) -> list[str]:
    present = {sheet["name"] for sheet in sheets}
    return [name for name in PAYGATES_SHEETS if name not in present]


def formula_warnings(sheets: list[dict]) -> list[dict[str, str]]:
    warnings = []
    for sheet in sheets:
        for formula in sheet["formulas"]:
            if "Squad_CnR" in formula and "Squad_VA" in formula:
                warnings.append({"sheet": sheet["name"], "formula": formula, "warning": "criteria range references Squad_CnR but sum range references Squad_VA"})
    return warnings


def find_header_row(rows: list[list[str]]) -> list[str] | None:
    for row in rows[:20]:
        normalized = [normalize_header(cell) for cell in row]
        if "Test Case ID" in normalized or len(set(normalized) & set(LEGACY_19_HEADERS)) >= 5:
            return row
    return rows[0] if rows else None


def read_shared_strings(z: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    return ["".join(text.text or "" for text in item.findall(".//main:t", NS)) for item in root.findall("main:si", NS)]


def workbook_sheets(z: zipfile.ZipFile) -> list[tuple[str, str]]:
    workbook = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rel_by_id = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels.findall("rel:Relationship", NS)}
    sheets = []
    for sheet in workbook.findall(".//main:sheets/main:sheet", NS):
        rel_id = sheet.attrib.get(f"{{{NS['office_rel']}}}id")
        target = rel_by_id.get(rel_id or "", "")
        clean_target = target.lstrip("/")
        sheet_path = clean_target if clean_target.startswith("xl/") else "xl/" + clean_target
        sheets.append((sheet.attrib.get("name", "Sheet"), sheet_path))
    return sheets


def read_sheet_rows(z: zipfile.ZipFile, sheet_path: str, shared: list[str]) -> list[list[str]]:
    root = ET.fromstring(z.read(sheet_path))
    rows = []
    for row_node in root.findall(".//main:sheetData/main:row", NS):
        row = []
        current_col = 1
        for cell_node in row_node.findall("main:c", NS):
            col_idx = column_index(cell_node.attrib.get("r", "")) or current_col
            while current_col < col_idx:
                row.append("")
                current_col += 1
            row.append(cell_value(cell_node, shared))
            current_col += 1
        rows.append(row)
    return rows


def column_index(ref: str) -> int | None:
    match = re.match(r"([A-Z]+)", ref.upper())
    if not match:
        return None
    index = 0
    for char in match.group(1):
        index = index * 26 + ord(char) - 64
    return index


def cell_value(cell_node: ET.Element, shared: list[str]) -> str:
    cell_type = cell_node.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(text.text or "" for text in cell_node.findall(".//main:t", NS))
    value_node = cell_node.find("main:v", NS)
    if value_node is None or value_node.text is None:
        return ""
    value = value_node.text
    if cell_type == "s":
        try:
            return shared[int(value)]
        except (ValueError, IndexError):
            return ""
    return value


def read_formulas(z: zipfile.ZipFile) -> dict[str, list[str]]:
    formulas = {}
    for name in z.namelist():
        if not name.startswith("xl/worksheets/") or not name.endswith(".xml"):
            continue
        root = ET.fromstring(z.read(name))
        sheet_formulas = []
        for cell_node in root.findall(".//main:c", NS):
            formula_node = cell_node.find("main:f", NS)
            if formula_node is not None and formula_node.text:
                sheet_formulas.append(f"{cell_node.attrib.get('r', '')}: ={formula_node.text}")
        formulas[name] = sheet_formulas
    return formulas


def extract_profiles(source: Path) -> dict:
    workbooks = []
    for path in sorted(source.rglob("*.xlsx")):
        workbooks.append(profile_workbook(path))
    return {
        "schema_version": "1.0",
        "source_root": str(source),
        "header_aliases": HEADER_ALIASES,
        "status_aliases": STATUS_ALIASES,
        "legacy_19_headers": LEGACY_19_HEADERS,
        "paygates_expected_sheets": PAYGATES_SHEETS,
        "workbooks": workbooks,
    }


def write_output(data: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        import yaml  # type: ignore
        output.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    except ImportError:
        output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract BIDV XLSX sheet/header/status/formula profiles")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if not args.source.exists() or not args.source.is_dir():
        raise SystemExit(f"source directory not found: {args.source}")
    data = extract_profiles(args.source)
    write_output(data, args.output)
    print(json.dumps({"status": "success", "workbooks": len(data["workbooks"]), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
