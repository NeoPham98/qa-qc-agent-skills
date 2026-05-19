#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

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
UAT_16_HEADERS = [
    "Test Case ID",
    "Test Case Name",
    "Precondition",
    "Test Steps",
    "Test Data",
    "Expected Result",
    "Priority",
    "Test Type",
    "Module",
    "Requirement ID",
    "Execution Result",
    "Actual Result",
    "Bug ID",
    "Tester",
    "Execution Date",
    "Notes",
]
API_ID_RE = re.compile(r"^TD_P[123]_\d{3}_TC_\d{3}$")
UI_ID_RE = re.compile(r"^TD_\d{3}_TC_\d{3}$")


def normalize_header(value: str) -> str:
    stripped = value.strip()
    return HEADER_ALIASES.get(value, HEADER_ALIASES.get(stripped, stripped))


def parse_tsv(path: Path) -> tuple[list[str], list[dict[str, str]], list[str]]:
    raw = path.read_text(encoding="utf-8-sig")
    lines = raw.splitlines()
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader), lines


def validate_legacy_19(path: Path) -> list[str]:
    headers, rows, lines = parse_tsv(path)
    normalized_headers = [normalize_header(header) for header in headers]
    errors: list[str] = []

    alias_headers = [header for header in headers if normalize_header(header) != header]
    if alias_headers:
        errors.append(f"{path}: header does not match legacy 19-column contract")
        errors.append(f"{path}: exported header still uses aliases: {', '.join(alias_headers)}")
    elif normalized_headers != LEGACY_19_HEADERS:
        errors.append(f"{path}: header does not match legacy 19-column contract")

    for line_no, line in enumerate(lines, start=1):
        if line.count("\t") != 18:
            errors.append(f"{path}:{line_no}: expected exactly 18 tabs")
        if line and not all(cell.startswith('"') and cell.endswith('"') for cell in line.split("\t")):
            errors.append(f"{path}:{line_no}: all cells must be quoted")

    if not rows:
        errors.append(f"{path}: no testcase rows")
        return errors

    id_column = normalized_headers.index("Test Case ID") if "Test Case ID" in normalized_headers else None
    notes_column = normalized_headers.index("Notes") if "Notes" in normalized_headers else None
    for row_no, row in enumerate(rows, start=2):
        normalized = {normalize_header(key): value for key, value in row.items() if key is not None}
        tc_id = (normalized.get("Test Case ID") or "").strip()
        if not (API_ID_RE.match(tc_id) or UI_ID_RE.match(tc_id)):
            errors.append(f"{path}:{row_no}: invalid Test Case ID '{tc_id}'")
        if "\n" in (normalized.get("Group Tests") or ""):
            pass
        if (normalized.get("Notes") or "").strip():
            errors.append(f"{path}:{row_no}: Notes must be empty in initial output")
        for column in ["Test Steps", "Expected result"]:
            if not (normalized.get(column) or "").strip():
                errors.append(f"{path}:{row_no}: empty required column '{column}'")
        if tc_id.startswith("TD_P") and re.search(r"negative|invalid|missing|không hợp lệ|thiếu|lỗi", " ".join(normalized.values()), re.I):
            blob = " ".join([normalized.get("Test Steps", ""), normalized.get("Expected result", "")])
            if re.search(r"\bdb\b|database", blob, re.I):
                errors.append(f"{path}:{row_no}: negative API case must not verify DB")
    return errors


def validate_uat_16(path: Path) -> list[str]:
    headers, rows, lines = parse_tsv(path)
    normalized_headers = [normalize_header(header) for header in headers]
    errors: list[str] = []

    if len(normalized_headers) != 16 or normalized_headers != [normalize_header(header) for header in UAT_16_HEADERS]:
        errors.append(f"{path}: header does not match UAT 16-column contract")
    for line_no, line in enumerate(lines, start=1):
        if line.count("\t") != 15:
            errors.append(f"{path}:{line_no}: expected exactly 15 tabs")
        if line and not all(cell.startswith('"') and cell.endswith('"') for cell in line.split("\t")):
            errors.append(f"{path}:{line_no}: all cells must be quoted")
    if not rows:
        errors.append(f"{path}: no testcase rows")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate BIDV testcase TSV contracts")
    parser.add_argument("path", type=Path)
    parser.add_argument("--profile", choices=["legacy_19_column_testcase", "uat_16_column_testcase"], required=True)
    args = parser.parse_args()

    errors = validate_legacy_19(args.path) if args.profile == "legacy_19_column_testcase" else validate_uat_16(args.path)
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, ensure_ascii=True, indent=2))
        return 1
    print(json.dumps({"status": "passed", "profile": args.profile, "path": str(args.path)}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
