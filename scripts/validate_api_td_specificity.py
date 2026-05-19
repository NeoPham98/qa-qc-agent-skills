#!/usr/bin/env python3
"""Validate API Test Design has concrete API specificity."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

FORBIDDEN = [
    "verify api works",
    "validate invalid input",
    "check response is correct",
    "valid data",
    "invalid data",
    "data hợp lệ",
    "data không hợp lệ",
    "kiểm tra dữ liệu không hợp lệ",
    "kiểm tra dữ liệu hợp lệ",
    "như trên",
    "tương tự",
    "with one changed condition",
    "send request with one changed condition",
    "assert http status and code/message/success/errors/response body schema",
]

PHASES = ["TD_P1_", "TD_P2_", "TD_P3_"]
ENDPOINT_RE = re.compile(r"\b(GET|POST|PUT|PATCH|DELETE)\s+(/[^\s]+)")
TD_RE = re.compile(r"^###\s+(TD_P[123]_\d+).*", re.MULTILINE)


def section_for(text: str, start: int) -> str:
    next_match = re.search(r"\n###\s+TD_P[123]_\d+", text[start + 1 :])
    if not next_match:
        return text[start:]
    return text[start : start + 1 + next_match.start()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate API TD specificity")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    text = args.path.read_text(encoding="utf-8-sig")
    lower = text.lower()
    errors: list[str] = []

    for phase in PHASES:
        if phase not in text:
            errors.append(f"missing phase IDs: {phase}")

    endpoints = ENDPOINT_RE.findall(text)
    if not endpoints:
        errors.append("missing HTTP method + endpoint headings")

    td_matches = list(TD_RE.finditer(text))
    if not td_matches:
        errors.append("no TD_Px nodes found")

    for phrase in FORBIDDEN:
        if phrase in lower:
            errors.append(f"forbidden generic phrase: {phrase}")

    for match in td_matches:
        td_id = match.group(1)
        block = section_for(text, match.start())
        if "**Steps**" not in block or "**Expected**" not in block:
            errors.append(f"{td_id}: missing Steps or Expected")
        if "Source" not in block and "source" not in block:
            errors.append(f"{td_id}: missing source reference")
        preceding = text[: match.start()]
        heading_match = list(ENDPOINT_RE.finditer(preceding[-3000:]))
        if not heading_match:
            errors.append(f"{td_id}: cannot associate with method/endpoint heading")
        if td_id.startswith("TD_P2") and not re.search(r"field|schema|request|response|body|param|kiểu|định dạng|enum|length|mandatory|required|bắt buộc", block, re.I):
            errors.append(f"{td_id}: schema node lacks field/schema target")
        if td_id.startswith("TD_P3") and not re.search(r"business|rule|error|code|state|flow|trạng thái|nghiệp vụ|lỗi", block, re.I):
            errors.append(f"{td_id}: business node lacks rule/error/state target")

    if errors:
        print("API TD specificity validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"API TD specificity validation passed ({len(td_matches)} TD nodes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
