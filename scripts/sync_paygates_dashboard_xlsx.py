#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from minimal_xlsx import write_xlsx
from paygates_dashboard import HEADERS


def validate_dashboard(path: Path) -> None:
    proc = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("validate_paygates_dashboard.py")), str(path)],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stdout.strip() or proc.stderr.strip())


def load_dashboard(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if list(reader.fieldnames or []) != HEADERS:
            raise ValueError("dashboard TSV headers do not match Paygates contract")
        return [[row.get(header, "") for header in HEADERS] for row in reader]


def main() -> int:
    parser = argparse.ArgumentParser(description="Safely sync/export Paygates dashboard XLSX from validated TSV")
    parser.add_argument("--dashboard-tsv", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-workbook", type=Path)
    args = parser.parse_args()

    if args.source_workbook:
        if not args.source_workbook.exists():
            raise FileNotFoundError(f"source workbook not found: {args.source_workbook}")
        if args.source_workbook.resolve() == args.output.resolve():
            raise ValueError("output must differ from source workbook; in-place overwrite is not allowed")

    validate_dashboard(args.dashboard_tsv)
    rows = load_dashboard(args.dashboard_tsv)
    write_xlsx(HEADERS, rows, args.output, sheet_name="Paygates Dashboard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
