#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

REQUIRED_COLUMNS = ["Test Case ID", "Main Component", "Phase", "Rationale"]
TC_ID_RE = re.compile(r"TD_P[123]_\d{3}_TC_\d{3}")
BIDV_PATH_RE = re.compile(r"(^|[\\/`\s])BIDV[\\/]", re.I)
SECRET_RE = re.compile(r"(password|secret|token|api[_-]?key)\s*[:=]\s*\S+", re.I)
PHASE_COMPONENTS = {
    "TD_P1": "method/header",
    "TD_P2": "schema/validation",
    "TD_P3": "logic/business",
}


def parse_markdown_tables(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    table: list[list[str]] = []
    for line in [*text.splitlines(), ""]:
        stripped = line.strip()
        if stripped.startswith("|"):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if all(set(cell) <= {"-", ":", " "} for cell in cells):
                continue
            table.append(cells)
            continue
        if len(table) >= 2:
            header = table[0]
            rows.extend(dict(zip(header, row)) for row in table[1:] if len(row) == len(header))
        table = []
    return rows


def parse_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_analysis_rows(path: Path) -> list[dict[str, str]]:
    if path.suffix.lower() in {".tsv", ".tab"}:
        return parse_tsv(path)
    return parse_markdown_tables(path.read_text(encoding="utf-8-sig"))


def row_value(row: dict[str, str], *columns: str) -> str:
    for column in columns:
        value = (row.get(column) or "").strip()
        if value:
            return value
    return ""


def source_ids(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8-sig")
    return set(TC_ID_RE.findall(text))


def expected_phase(tc_id: str) -> str:
    return tc_id.split("_")[1].replace("P", "TD_P") if False else tc_id[:5]


def validate(path: Path, testcase_source: Path | None) -> list[str]:
    text = path.read_text(encoding="utf-8-sig")
    errors: list[str] = []
    if BIDV_PATH_RE.search(text):
        errors.append(f"{path}: raw BIDV path reference is not allowed")
    if SECRET_RE.search(text):
        errors.append(f"{path}: possible secret marker found")

    rows = load_analysis_rows(path)
    matrix_rows = [row for row in rows if set(REQUIRED_COLUMNS).issubset(row)]
    if not matrix_rows:
        return [*errors, f"{path}: no API automation analysis table found"]

    analysis_ids: list[str] = []
    for idx, row in enumerate(matrix_rows, start=2):
        tc_id = row_value(row, "Test Case ID")
        phase = row_value(row, "Phase")
        component = row_value(row, "Main Component").lower()
        rationale = row_value(row, "Rationale")
        if not tc_id or not TC_ID_RE.fullmatch(tc_id):
            errors.append(f"{path}:{idx}: invalid Test Case ID '{tc_id}'")
            continue
        analysis_ids.append(tc_id)
        expected = tc_id[:5]
        if phase != expected:
            errors.append(f"{path}:{idx}: {tc_id} must have Phase {expected}, got '{phase}'")
        if PHASE_COMPONENTS[expected].split("/")[0] not in component and PHASE_COMPONENTS[expected].split("/")[1] not in component:
            errors.append(f"{path}:{idx}: {tc_id} Main Component does not match {expected}")
        if not rationale:
            errors.append(f"{path}:{idx}: empty Rationale")

    seen: set[str] = set()
    for tc_id in analysis_ids:
        if tc_id in seen:
            errors.append(f"{path}: duplicate testcase classification '{tc_id}'")
        seen.add(tc_id)

    if testcase_source:
        expected_ids = source_ids(testcase_source)
        missing = sorted(expected_ids - set(analysis_ids))
        extra = sorted(set(analysis_ids) - expected_ids)
        if missing:
            errors.append(f"{path}: missing testcase ids from source: {', '.join(missing)}")
        if extra:
            errors.append(f"{path}: analysis contains ids not in source: {', '.join(extra)}")

    non_table_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("|") or set(stripped) <= {"-", ":", " "}:
            continue
        if stripped.startswith("#"):
            continue
        non_table_lines.append(stripped)
    if non_table_lines:
        errors.append(f"{path}: analysis output must be table-only apart from headings")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate API automation testcase analysis")
    parser.add_argument("path", type=Path)
    parser.add_argument("--testcase-source", type=Path)
    args = parser.parse_args()

    errors = validate(args.path, args.testcase_source)
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, ensure_ascii=True, indent=2))
        return 1
    print(json.dumps({"status": "passed", "path": str(args.path)}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
