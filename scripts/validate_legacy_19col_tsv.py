#!/usr/bin/env python3
"""Validate legacy 19-column testcase TSV."""

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

REQUIRED_NON_EMPTY = [
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
]

BANNED_VAGUE = ["như trên", "tương tự", "valid data", "data hợp lệ", "data không hợp lệ", "...", "etc"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    raw = args.path.read_text(encoding="utf-8-sig")
    for line_no, line in enumerate(raw.splitlines(), start=1):
        if line.count("\t") != 18:
            errors.append(f"{args.path}:{line_no}: expected 18 tabs, found {line.count(chr(9))}")

    with args.path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if reader.fieldnames != HEADERS:
            legacy_headers = ["Test Data" if h == "Test Datas" else h for h in HEADERS]
            if reader.fieldnames == legacy_headers:
                errors.append(f"{args.path}: header uses legacy alias 'Test Data'; expected legacy 'Test Datas'")
            else:
                errors.append(f"{args.path}: header does not match legacy 19-column contract")
        rows = list(reader)

    if not rows:
        errors.append(f"{args.path}: no data rows")

    for idx, row in enumerate(rows, start=2):
        for column in REQUIRED_NON_EMPTY:
            if not (row.get(column) or "").strip():
                errors.append(f"{args.path}:{idx}: empty required column '{column}'")
        joined = " ".join(row.values()).lower()
        for phrase in BANNED_VAGUE:
            if phrase in joined:
                errors.append(f"{args.path}:{idx}: banned vague phrase '{phrase}'")
        if "verify" not in (row.get("Test Steps", "") + " " + row.get("Expected result", "")).lower() and "kiểm tra" not in (row.get("Test Steps", "") + " " + row.get("Expected result", "")).lower():
            errors.append(f"{args.path}:{idx}: missing explicit verify/check step")

    if errors:
        print("legacy 19-column validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("legacy 19-column validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
