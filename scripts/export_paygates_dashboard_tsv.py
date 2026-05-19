#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from paygates_dashboard import HEADERS, aggregate_dashboard, load_rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Paygates dashboard TSV")
    parser.add_argument("--testcase", required=True, type=Path)
    parser.add_argument("--execution", type=Path)
    parser.add_argument("--metadata-json", type=Path)
    parser.add_argument("--project")
    parser.add_argument("--squad")
    parser.add_argument("--sprint")
    parser.add_argument("--epic")
    parser.add_argument("--function")
    parser.add_argument("--detail-link")
    parser.add_argument("--generate-type")
    parser.add_argument("--automation-status")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    metadata = {}
    if args.metadata_json:
        metadata.update(json.loads(args.metadata_json.read_text(encoding="utf-8")))
    for key in ["project", "squad", "sprint", "epic", "function", "detail_link", "generate_type", "automation_status"]:
        value = getattr(args, key)
        if value:
            metadata[key] = value

    testcase_rows = load_rows(args.testcase)
    execution_rows = load_rows(args.execution) if args.execution else []
    row = aggregate_dashboard(testcase_rows, execution_rows, metadata)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
