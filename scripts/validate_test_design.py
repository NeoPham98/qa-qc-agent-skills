#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

API_PHASES = ["TD_P1", "TD_P2", "TD_P3"]
API_CONTROL_PARAMS = [
    "METHOD_CHECK",
    "CONTENT_TYPE_CHECK",
    "MANDATORY_CHECK",
    "TYPE_CHECK",
    "LENGTH_CHECK",
    "SCOPE_FIELDS",
    "EG_CHECK",
]
API_ID_RE = re.compile(r"^###\s+(TD_P[123]_\d{3})\b", re.MULTILINE)
UI_ID_RE = re.compile(r"^###\s+(TD_\d{3})\s+-\s+\[[^\]]+\]\s+-\s+.+$", re.MULTILINE)


def section_for(text: str, start: int, id_pattern: str) -> str:
    next_match = re.search(rf"\n###\s+{id_pattern}", text[start + 1 :], re.MULTILINE)
    if not next_match:
        return text[start:]
    return text[start : start + 1 + next_match.start()]


def validate_api(text: str, path: Path) -> list[str]:
    errors: list[str] = []
    lower = text.lower()
    for phase in API_PHASES:
        if phase not in text:
            errors.append(f"{path}: missing phase {phase}")
    for token in API_CONTROL_PARAMS:
        if token not in text:
            errors.append(f"{path}: missing control parameter {token}")

    ids = list(API_ID_RE.finditer(text))
    if not ids:
        errors.append(f"{path}: no TD_P[123]_NNN headings found")

    for match in ids:
        td_id = match.group(1)
        block = section_for(text, match.start(), r"TD_P[123]_\d{3}")
        if "**Steps**" not in block or "**Expected**" not in block:
            errors.append(f"{path}: {td_id} missing Steps or Expected section")
        if "Source" not in block and "source" not in block:
            errors.append(f"{path}: {td_id} missing source trace/reference")
        if td_id.startswith("TD_P2") and not re.search(r"field|schema|request|response|body|param|required|mandatory|type|length|enum|format|bắt buộc", block, re.I):
            errors.append(f"{path}: {td_id} missing schema/field target detail")
        if td_id.startswith("TD_P3") and not re.search(r"business|rule|error|code|state|flow|nghiệp vụ|trạng thái|lỗi", block, re.I):
            errors.append(f"{path}: {td_id} missing business/state/error detail")

    if "td_p1" in lower and not re.search(r"GET|POST|PUT|PATCH|DELETE", text):
        errors.append(f"{path}: API TD missing HTTP method coverage")
    return errors


def validate_ui(text: str, path: Path) -> list[str]:
    errors: list[str] = []
    ids = list(UI_ID_RE.finditer(text))
    if not ids:
        errors.append(f"{path}: no canonical UI TD headings found")
    for match in ids:
        td_id = match.group(1)
        block = section_for(text, match.start(), r"TD_\d{3}")
        if "**Steps**" not in block or "**Expected**" not in block:
            errors.append(f"{path}: {td_id} missing Steps or Expected section")
        if "Source" not in block and "source" not in block:
            errors.append(f"{path}: {td_id} missing source trace/reference")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate test design contracts")
    parser.add_argument("path", type=Path)
    parser.add_argument("--type", choices=["api", "ui"], required=True)
    args = parser.parse_args()

    text = args.path.read_text(encoding="utf-8-sig")
    errors = validate_api(text, args.path) if args.type == "api" else validate_ui(text, args.path)
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, ensure_ascii=True, indent=2))
        return 1
    print(json.dumps({"status": "passed", "type": args.type, "path": str(args.path)}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
