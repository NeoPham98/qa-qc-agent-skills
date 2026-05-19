#!/usr/bin/env python3
"""Export testcase markdown tables to TSV-compatible rows."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from markdown_tables import parse_markdown_table

HEADERS = [
    "Test Suite Name",
    "Details",
    "Testcase LV1",
    "Testcase LV2",
    "Testcase LV3",
    "External ID",
    "Name",
    "Summary",
    "PreConditions",
    "Status",
    "ExecutionType",
    "Importance",
    "Keywords",
    "Number of Attachments",
    "Step",
    "Expected Result",
    "Actual Result",
    "StepExec Type",
    "Spec Title",
    "Document ID",
    "Estimated exec. Duration",
    "Requirement ID",
    "Test Condition ID",
    "Evidence Required",
    "Open Question / Dependency",
    "Execution Eligibility",
]


def normalize_row(row: dict[str, str]) -> dict[str, str]:
    case_id = row.get("Test Case ID", row.get("External ID", ""))
    return {
        "Test Suite Name": row.get("Test Suite Name", "Generated"),
        "Details": row.get("Details", "Generated from markdown source"),
        "Testcase LV1": row.get("LV1", row.get("Testcase LV1", "QC")),
        "Testcase LV2": row.get("LV2", row.get("Testcase LV2", "")),
        "Testcase LV3": row.get("LV3", row.get("Testcase LV3", "")),
        "External ID": case_id,
        "Name": row.get("Name", case_id),
        "Summary": row.get("Summary", row.get("Name", "")),
        "PreConditions": row.get("Preconditions", row.get("PreConditions", "")),
        "Status": row.get("Status", "Ready"),
        "ExecutionType": row.get("ExecutionType", "Manual"),
        "Importance": row.get("Importance", "Medium"),
        "Keywords": row.get("Keywords", ""),
        "Number of Attachments": row.get("Number of Attachments", "0"),
        "Step": row.get("Step", ""),
        "Expected Result": row.get("Expected Result", ""),
        "Actual Result": row.get("Actual Result", ""),
        "StepExec Type": row.get("StepExec Type", "Manual"),
        "Spec Title": row.get("Spec Title", ""),
        "Document ID": row.get("Document ID", row.get("Requirement ID", "")),
        "Estimated exec. Duration": row.get("Estimated exec. Duration", ""),
        "Requirement ID": row.get("Requirement ID", ""),
        "Test Condition ID": row.get("Test Condition ID", ""),
        "Evidence Required": row.get("Evidence Required", ""),
        "Open Question / Dependency": row.get("Open Question / Dependency", ""),
        "Execution Eligibility": row.get("Execution Eligibility", "Ready"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    rows = [normalize_row(row) for row in parse_markdown_table(args.input.read_text(encoding="utf-8"))]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
