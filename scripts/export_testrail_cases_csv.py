#!/usr/bin/env python3
"""Export BIDV legacy 19-column testcase TSV to a TestRail-friendly CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


REQUIRED_HEADERS = [
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

OUTPUT_HEADERS = [
    "Section",
    "Title",
    "External ID",
    "Preconditions",
    "Steps",
    "Expected Result",
    "Priority",
    "Type",
    "Automation Type",
    "References",
]


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        headers = reader.fieldnames or []
        if headers != REQUIRED_HEADERS:
            raise ValueError("input TSV does not match legacy 19-column contract")
        rows = list(reader)
    if not rows:
        raise ValueError("input TSV contains no testcase rows")
    return rows


def clean(value: str | None) -> str:
    return (value or "").replace("\\n", "\n").replace("\r\n", "\n").replace("\r", "\n").strip()


def build_steps(row: dict[str, str]) -> str:
    blocks: list[str] = []
    test_data = clean(row.get("Test Datas"))
    test_steps = clean(row.get("Test Steps"))
    expected = clean(row.get("Expected result"))
    if test_data:
        blocks.append(f"Test Data:\n{test_data}")
    if test_steps:
        blocks.append(f"Steps:\n{test_steps}")
    if expected:
        blocks.append(f"Expected Result:\n{expected}")
    return "\n\n".join(blocks).strip()


def pick_title(row: dict[str, str]) -> str:
    summary = clean(row.get("Test Case Summary"))
    outline = clean(row.get("Scenario Outline"))
    case_id = clean(row.get("Test Case ID"))
    if summary:
        return f"{case_id} - {summary}"
    if outline:
        return f"{case_id} - {outline}"
    return case_id


def map_priority(value: str) -> str:
    normalized = clean(value).lower()
    if normalized in {"high", "critical"}:
        return "High"
    if normalized in {"medium", "normal"}:
        return "Medium"
    if normalized in {"low", "minor"}:
        return "Low"
    return clean(value) or "Medium"


def map_automation(value: str) -> str:
    normalized = clean(value).lower()
    if normalized in {"yes", "y", "true", "automated"}:
        return "Automated Candidate"
    return "Manual"


def build_output_row(row: dict[str, str]) -> dict[str, str]:
    case_id = clean(row.get("Test Case ID"))
    preconditions = clean(row.get("Pre-conditions"))
    expected = clean(row.get("Expected result"))
    steps = build_steps(row)
    if not case_id:
        raise ValueError("missing Test Case ID")
    if not steps:
        raise ValueError(f"{case_id}: missing Steps/Test Datas/Expected result content")
    if not expected:
        raise ValueError(f"{case_id}: missing Expected result")
    references = " | ".join(part for part in [clean(row.get("Function")), clean(row.get("Notes"))] if part)
    return {
        "Section": clean(row.get("Group Tests")) or "Generated",
        "Title": pick_title(row),
        "External ID": case_id,
        "Preconditions": preconditions,
        "Steps": steps,
        "Expected Result": expected,
        "Priority": map_priority(row.get("Priority", "")),
        "Type": "Functional",
        "Automation Type": map_automation(row.get("Automation", "")),
        "References": references,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Export BIDV legacy testcase TSV to TestRail-friendly CSV")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    rows = [build_output_row(row) for row in load_rows(args.input)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_HEADERS)
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
