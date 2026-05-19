#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from extract_xlsx_profiles import PAYGATES_SHEETS, STATUS_ALIASES, profile_workbook

CANONICAL_STATUSES = {
    "Ready to UAT",
    "Pending",
    "In-Test",
    "Update test cases",
    "Test case out of date",
    "Completed",
    "In-Progress",
    "AI gen",
    "Manual",
    "AI gen + Manual",
    "API",
    "Web UI",
}


def validate_tracker(path: Path) -> list[str]:
    profile = profile_workbook(path)
    errors: list[str] = []

    missing = profile.get("paygates_missing_sheets", [])
    if missing:
        errors.append(f"{path}: missing expected sheets: {', '.join(missing)}")

    for sheet in profile["sheets"]:
        for alias in sheet.get("status_aliases", []):
            errors.append(
                f"{path}: sheet {sheet['name']} uses alias '{alias['source']}' -> '{alias['normalized']}'"
            )
        for status in sheet.get("status_values", []):
            if status not in CANONICAL_STATUSES and status not in STATUS_ALIASES:
                errors.append(f"{path}: sheet {sheet['name']} has unknown status '{status}'")

    for warning in profile.get("formula_warnings", []):
        errors.append(f"{path}: sheet {warning['sheet']} formula warning: {warning['warning']}")

    if profile.get("workbook_type") != "paygates_tracker":
        errors.append(f"{path}: workbook is not classified as paygates_tracker")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Paygates tracker workbook")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    errors = validate_tracker(args.path)
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, ensure_ascii=True, indent=2))
        return 1
    print(json.dumps({"status": "passed", "path": str(args.path), "expected_sheets": PAYGATES_SHEETS}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
