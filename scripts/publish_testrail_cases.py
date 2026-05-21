#!/usr/bin/env python3
"""Publish testcase definitions to TestRail.

MVP in this repo: generate an import-friendly CSV and gate publish behind explicit approval.
API integration can be enabled later once TestRail endpoint/template is confirmed.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sdk.output_publishers.testrail_publisher import (
    load_testrail_config_from_env,
    publish_testcases_from_import_csv,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish testcase definitions to TestRail")
    parser.add_argument("--input", required=True, type=Path, help="TestRailImport.generated.csv")
    parser.add_argument("--approved", action="store_true", help="Explicit approval gate")
    parser.add_argument("--mode", choices=["api", "csv-only"], default="api")
    args = parser.parse_args()

    if args.mode == "csv-only":
        if not args.input.exists():
            raise FileNotFoundError(args.input)
        return 0
    config = load_testrail_config_from_env()
    publish_testcases_from_import_csv(args.input, config=config, approved=args.approved, mode=args.mode)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
