#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from minimal_xlsx import write_xlsx
from paygates_dashboard import HEADERS


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Paygates dashboard XLSX from TSV")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    with args.input.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = [[row.get(header, "") for header in HEADERS] for row in reader]
    write_xlsx(HEADERS, rows, args.output, sheet_name="Paygates Dashboard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
