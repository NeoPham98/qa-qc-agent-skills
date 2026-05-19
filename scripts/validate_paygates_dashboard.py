#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from paygates_dashboard import HEADERS, validate_dashboard_rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Paygates dashboard TSV")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    with args.path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)
        headers = reader.fieldnames or []

    errors: list[str] = []
    if headers != HEADERS:
        missing = [header for header in HEADERS if header not in headers]
        extra = [header for header in headers if header not in HEADERS]
        if missing:
            errors.append(f"{args.path}: missing headers: {', '.join(missing)}")
        if extra:
            errors.append(f"{args.path}: extra headers: {', '.join(extra)}")
        if not missing and not extra:
            errors.append(f"{args.path}: header order does not match Paygates contract")
    errors.extend(f"{args.path}: {error}" for error in validate_dashboard_rows(rows))

    if errors:
        print("BIDV Paygates dashboard validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("BIDV Paygates dashboard validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
