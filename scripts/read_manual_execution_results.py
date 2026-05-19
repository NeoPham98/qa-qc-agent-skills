#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from lib.xlsx_table import read_xlsx_table, rows_to_dicts

EXECUTION_HEADERS = [
    "Test Execution ID",
    "Test Set ID",
    "Test Case ID",
    "Environment",
    "Build / Version",
    "Tester",
    "Planned Run Date",
    "Status",
    "Actual Result",
    "Evidence",
    "Defect Link",
    "Requirement ID",
    "Test Condition ID",
    "Notes",
]

STATUS_MAP = {
    "": "Not Run",
    "pending": "Not Run",
    "not run": "Not Run",
    "untested": "Not Run",
    "pass": "Pass",
    "passed": "Pass",
    "đạt": "Pass",
    "fail": "Fail",
    "failed": "Fail",
    "không đạt": "Fail",
    "khong dat": "Fail",
    "blocked": "Blocked",
    "retest": "Retest",
    "n/a": "Not Run",
    "na": "Not Run",
    "accepted": "Accepted",
}


def load_rows(path: Path, sheet_name: str | None) -> list[dict[str, str]]:
    suffix = path.suffix.lower()
    if suffix == ".xlsx":
        return rows_to_dicts(read_xlsx_table(path, sheet_name=sheet_name))
    if suffix in {".tsv", ".csv"}:
        delimiter = "\t" if suffix == ".tsv" else ","
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f, delimiter=delimiter))
    raise ValueError("input must be .xlsx, .tsv, or .csv")


def normalize_status(value: str) -> str:
    key = (value or "").strip().lower()
    return STATUS_MAP.get(key, value.strip() or "Not Run")


def status_column(args: argparse.Namespace) -> str:
    if args.status_column:
        return args.status_column
    if args.automation:
        return "Automation Test Results"
    if args.round == "2":
        return "Manual Test Results Round 2"
    return "Manual Test Results Round 1"


def pending(value: str | None, field: str) -> str:
    return value.strip() if value and value.strip() else f"[PENDING_DOC:{field}]"


def build_execution_rows(rows: list[dict[str, str]], args: argparse.Namespace) -> list[dict[str, str]]:
    column = status_column(args)
    output: list[dict[str, str]] = []
    for row in rows:
        case_id = (row.get("Test Case ID") or "").strip()
        if not case_id:
            continue
        notes = row.get("Notes", "")
        raw_status = row.get(column, "")
        normalized = normalize_status(raw_status)
        if normalized not in {"Not Run", "Pass", "Fail", "Blocked", "Retest", "Accepted"}:
            notes = "; ".join(part for part in [notes, f"[PENDING_DOC:unsupported_status:{raw_status}]"] if part)
            normalized = "Not Run"
        output.append({
            "Test Execution ID": pending(args.test_execution_id, "test_execution_id"),
            "Test Set ID": pending(args.test_set_id, "test_set_id"),
            "Test Case ID": case_id,
            "Environment": row.get("Environment", "") or pending(args.environment, "environment"),
            "Build / Version": pending(args.build_version, "build_version"),
            "Tester": pending(args.tester, "tester"),
            "Planned Run Date": args.planned_run_date or "",
            "Status": normalized,
            "Actual Result": row.get("Actual result", row.get("Actual Result", "")),
            "Evidence": args.evidence or "",
            "Defect Link": row.get("BugID", row.get("Defect Link", "")),
            "Requirement ID": row.get("Requirement ID", "") or args.requirement_id or "[PENDING_DOC:requirement_id]",
            "Test Condition ID": row.get("Test Condition ID", "") or args.test_condition_id or "[PENDING_DOC:test_condition_id]",
            "Notes": notes,
        })
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Read BIDV manual execution results from VA-style workbook/TSV/CSV")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--sheet-name")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--round", choices=["1", "2"], default="1")
    group.add_argument("--automation", action="store_true")
    parser.add_argument("--status-column")
    parser.add_argument("--test-execution-id")
    parser.add_argument("--test-set-id")
    parser.add_argument("--tester")
    parser.add_argument("--build-version")
    parser.add_argument("--environment")
    parser.add_argument("--planned-run-date")
    parser.add_argument("--evidence")
    parser.add_argument("--requirement-id")
    parser.add_argument("--test-condition-id")
    args = parser.parse_args()

    rows = build_execution_rows(load_rows(args.input, args.sheet_name), args)
    if not rows:
        raise ValueError("input contains no rows with Test Case ID")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=EXECUTION_HEADERS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
