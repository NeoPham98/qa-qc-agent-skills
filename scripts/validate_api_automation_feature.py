#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TC_ID_RE = re.compile(r"TD_P[123]_\d{3}_TC_\d{3}")
STEP_RE = re.compile(r"^\s*(Given|When|Then|And|But)\b")
BAD_STEP_RE = re.compile(r"^\s*([A-Z][A-Za-z]+)\b")
BIDV_PATH_RE = re.compile(r"(^|[\\/`\s])BIDV[\\/]", re.I)
PLACEHOLDER_RE = re.compile(r"\b(valid data|invalid data|TODO|TBD|như trên|tương tự)\b", re.I)
INVENTED_INTERNAL_RE = re.compile(r"\b(select\s+.+\s+from|insert\s+into|update\s+.+\s+set|delete\s+from|information_schema|pg_catalog|sys\.)\b", re.I)
PHASE_BY_FILE = {
    "api_method_header_validation.feature": "TD_P1",
    "api_validation.feature": "TD_P2",
    "api_logic_business.feature": "TD_P3",
}


def validate(path: Path, phase: str | None) -> list[str]:
    text = path.read_text(encoding="utf-8-sig")
    errors: list[str] = []
    expected_phase = phase or PHASE_BY_FILE.get(path.name)

    if BIDV_PATH_RE.search(text):
        errors.append(f"{path}: raw BIDV path reference is not allowed")
    if not re.search(r"^\s*Feature:\s+\S", text, re.MULTILINE):
        errors.append(f"{path}: missing Feature line")
    if not re.search(r"^\s*Scenario(?: Outline)?:\s+\S", text, re.MULTILINE):
        errors.append(f"{path}: missing Scenario or Scenario Outline")
    if PLACEHOLDER_RE.search(text):
        errors.append(f"{path}: placeholder-only value found")
    if INVENTED_INTERNAL_RE.search(text):
        errors.append(f"{path}: possible invented SQL/internal schema marker found")

    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("@"):
            continue
        if re.match(r"^(Feature|Background|Scenario|Scenario Outline|Examples):", stripped):
            continue
        if stripped.startswith("|"):
            continue
        if BAD_STEP_RE.match(stripped) and not STEP_RE.match(stripped):
            keyword = BAD_STEP_RE.match(stripped).group(1)  # type: ignore[union-attr]
            errors.append(f"{path}:{line_no}: invalid Gherkin step keyword '{keyword}'")

    ids = TC_ID_RE.findall(text)
    if not ids:
        errors.append(f"{path}: no testcase ids found")
    if expected_phase:
        for tc_id in sorted(set(ids)):
            if not tc_id.startswith(expected_phase):
                errors.append(f"{path}: testcase id {tc_id} is outside expected phase {expected_phase}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate API automation Gherkin feature output")
    parser.add_argument("path", type=Path)
    parser.add_argument("--phase", choices=["TD_P1", "TD_P2", "TD_P3"])
    args = parser.parse_args()

    errors = validate(args.path, args.phase)
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, ensure_ascii=True, indent=2))
        return 1
    print(json.dumps({"status": "passed", "path": str(args.path)}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
