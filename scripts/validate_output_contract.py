#!/usr/bin/env python3
"""Validate contract-compatible TSV output contracts."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

TESTCASE_REQUIRED = [
    "Test Suite Name",
    "Testcase LV1",
    "Testcase LV2",
    "External ID",
    "Name",
    "Summary",
    "PreConditions",
    "Status",
    "ExecutionType",
    "Importance",
    "Step",
    "Expected Result",
    "StepExec Type",
    "Spec Title",
    "Document ID",
    "Requirement ID",
    "Test Condition ID",
    "Evidence Required",
    "Execution Eligibility",
]

EXECUTION_REQUIRED = [
    "Test Execution ID",
    "Test Set ID",
    "Test Case ID",
    "Environment",
    "Build / Version",
    "Tester",
    "Status",
    "Requirement ID",
    "Test Condition ID",
]


def load_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def validate(path: Path, required: list[str]) -> list[str]:
    headers, rows = load_tsv(path)
    errors: list[str] = []
    missing = [column for column in required if column not in headers]
    if missing:
        errors.append(f"{path}: missing columns: {', '.join(missing)}")
    if not rows:
        errors.append(f"{path}: no data rows")
        return errors
    for idx, row in enumerate(rows, start=2):
        for column in required:
            if column in headers and not (row.get(column) or "").strip():
                errors.append(f"{path}:{idx}: empty required column '{column}'")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--testcase", type=Path)
    parser.add_argument("--execution", type=Path)
    parser.add_argument("--dashboard", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    if args.testcase:
        errors.extend(validate(args.testcase, TESTCASE_REQUIRED))
    if args.execution:
        errors.extend(validate(args.execution, EXECUTION_REQUIRED))
    if args.dashboard:
        from subprocess import run
        import sys
        proc = run([sys.executable, str(Path(__file__).with_name("validate_paygates_dashboard.py")), str(args.dashboard)], text=True, capture_output=True, check=False)
        if proc.returncode != 0:
            errors.append(proc.stdout.strip() or proc.stderr.strip())
    if errors:
        print("BIDV output contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("BIDV output contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
