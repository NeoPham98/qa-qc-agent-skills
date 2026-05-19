#!/usr/bin/env python3
"""Validate API testcase coverage with the default legacy 19-column profile."""

from __future__ import annotations

from validate_testcase_coverage import main


if __name__ == "__main__":
    raise SystemExit(main(default_profile="api_legacy_19_column_testcase"))
