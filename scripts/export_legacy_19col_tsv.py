#!/usr/bin/env python3
"""Export legacy 19-column testcase TSV from a markdown source table."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

HEADERS = [
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


def parse_markdown_table(text: str) -> list[dict[str, str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        rows.append([cell.strip() for cell in stripped.strip("|").split("|")])
    if not rows:
        return []
    header = rows[0]
    return [dict(zip(header, row)) for row in rows[1:] if len(row) == len(header)]


def first_present(row: dict[str, str], *keys: str, default: str = "") -> str:
    for key in keys:
        value = row.get(key)
        if value not in (None, ""):
            return value
    return default


def normalize_row(row: dict[str, str]) -> dict[str, str]:
    case_id = row.get("Test Case ID", "")
    test_case_name = first_present(row, "Test Case Name", "Name", default=case_id)
    source_trace = first_present(row, "Requirement / Source Trace", "Source Trace")
    summary = first_present(row, "Test Case Summary", "Summary", default=source_trace or test_case_name)
    return {
        "Test Case ID": case_id,
        "Function": first_present(row, "Function", "Endpoint", "API Endpoint", "LV2"),
        "Group Tests": first_present(row, "Group Tests", "Test Group", "Group", "LV2"),
        "Scenario Outline": first_present(row, "Scenario Outline", "Test Case Name", "LV3", default=summary),
        "Test Case Summary": summary,
        "Pre-conditions": first_present(row, "Pre-conditions", "Preconditions", "PreConditions"),
        "Test Datas": first_present(row, "Test Datas", "Test Data"),
        "Test Steps": first_present(row, "Test Steps", "Step"),
        "Expected result": first_present(row, "Expected result", "Expected Result"),
        "Environment": first_present(row, "Environment", default="SIT"),
        "Priority": first_present(row, "Priority", "Importance", default="Medium"),
        "Regression": row.get("Regression", ""),
        "Automation": row.get("Automation", ""),
        "Manual Test Results Round 1": row.get("Manual Test Results Round 1", ""),
        "Manual Test Results Round 2": row.get("Manual Test Results Round 2", ""),
        "Automation Test Results": row.get("Automation Test Results", ""),
        "Actual result": first_present(row, "Actual result", "Actual Result"),
        "BugID": row.get("BugID", ""),
        "Notes": first_present(row, "Notes", "Note", default=""),
    }


def escape_tsv_cell(value: str) -> str:
    return (value or "").replace("\r\n", "\\n").replace("\n", "\\n").replace("\r", "\\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    rows = [normalize_row(row) for row in parse_markdown_table(args.input.read_text(encoding="utf-8"))]
    escaped_rows = [{key: escape_tsv_cell(value) for key, value in row.items()} for row in rows]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerows(escaped_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
