#!/usr/bin/env python3
"""Validate BIDV legacy API testcase TSV contains executable API detail."""

from __future__ import annotations

import argparse
import csv
import re
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

FORBIDDEN = [
    "valid data",
    "invalid data",
    "data hợp lệ",
    "data không hợp lệ",
    "correct response",
    "appropriate error",
    "như trên",
    "tương tự",
    "...",
    "etc",
]

METHOD_RE = re.compile(r"\b(GET|POST|PUT|PATCH|DELETE)\b", re.I)
PATH_RE = re.compile(r"/[-A-Za-z0-9_/{}/]+")
STATUS_RE = re.compile(r"\b(HTTP\s*)?Status\s*:?\s*\d{3}\b|\bHTTP\s*\d{3}\b", re.I)
ASSERTION_RE = re.compile(r"\b(code|message|success|data|errors|traceId|response|body|schema|field|lỗi|mã lỗi)\b", re.I)
ID_RE = re.compile(r"^TD_P[123]_\d+_TC_\d+$")
PLACEHOLDER_ONLY_RE = re.compile(r"^\s*(\[PENDING_DOC[^\]]*\]|N/A|NA|-)?\s*$", re.I)


def load_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def is_negative(row: dict[str, str]) -> bool:
    blob = " ".join(row.get(col, "") for col in ["Scenario Outline", "Test Case Summary", "Test Steps", "Expected result"]).lower()
    return any(token in blob for token in ["missing", "invalid", "thiếu", "sai", "không hợp lệ", "negative", "lỗi"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate API testcase specificity in BIDV legacy TSV")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    headers, rows = load_rows(args.path)
    errors: list[str] = []

    if headers != HEADERS:
        errors.append("header does not match legacy 19-column contract")
    if not rows:
        errors.append("no testcase rows")

    for idx, row in enumerate(rows, start=2):
        tc_id = row.get("Test Case ID", "")
        summary = row.get("Test Case Summary", "")
        data = row.get("Test Datas", "")
        steps = row.get("Test Steps", "")
        expected = row.get("Expected result", "")
        blob = " ".join(row.values())
        lower = blob.lower()

        if not ID_RE.match(tc_id):
            errors.append(f"{args.path}:{idx}: Test Case ID must derive from TD_Px_NNN")
        if not (METHOD_RE.search(summary) or METHOD_RE.search(steps)):
            errors.append(f"{args.path}:{idx}: missing HTTP method in summary/steps")
        if not (PATH_RE.search(summary) or PATH_RE.search(steps) or PATH_RE.search(row.get("Pre-conditions", ""))):
            errors.append(f"{args.path}:{idx}: missing endpoint path")
        if PLACEHOLDER_ONLY_RE.match(data):
            errors.append(f"{args.path}:{idx}: Test Datas is placeholder-only")
        if not STATUS_RE.search(expected):
            errors.append(f"{args.path}:{idx}: Expected result missing HTTP status")
        if not ASSERTION_RE.search(expected):
            errors.append(f"{args.path}:{idx}: Expected result missing response/error assertion")
        if is_negative(row) and not re.search(r"field|header|param|key|request|response|code|message|bỏ|thiếu|sai|lỗi|rule", blob, re.I):
            errors.append(f"{args.path}:{idx}: negative case does not identify exact target")
        for phrase in FORBIDDEN:
            if phrase in lower:
                errors.append(f"{args.path}:{idx}: forbidden generic phrase '{phrase}'")

    if errors:
        print("API testcase specificity validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"API testcase specificity validation passed ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
