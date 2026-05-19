#!/usr/bin/env python3
"""Export TestExecution markdown tables to TSV-compatible status rows."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from markdown_tables import parse_markdown_table

HEADERS = [
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


def normalize_row(row: dict[str, str]) -> dict[str, str]:
    return {header: row.get(header, "") for header in HEADERS} | {
        "Status": row.get("Status", "Not Run"),
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
