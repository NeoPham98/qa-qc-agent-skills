#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

REQUIRED_COLUMNS = [
    "Matrix Row ID",
    "Source Ref",
    "Source Kind",
    "Field Or Rule",
    "Rule Type",
    "Technique",
    "Value Class",
    "Coverage Status",
    "Rationale",
]
VALID_SOURCE_KINDS = {
    "runtime_input",
    "normalized_knowledge",
    "workflow_pack_contract",
    "prompt_contract",
    "golden_example",
}
VALID_STATUSES = {"covered", "gap", "open_question", "pruned", "duplicate", "unmapped"}
BIDV_PATH_RE = re.compile(r"(^|[\\/`\s])BIDV[\\/]", re.I)
TD_ID_RE = re.compile(r"^TD(?:_P[123])?_\d{3}$")
TC_ID_RE = re.compile(r"^TD(?:_P[123])?_\d{3}_TC_\d{3}$")


def parse_markdown_tables(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    table: list[list[str]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        stripped = line.strip()
        if stripped.startswith("|"):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if all(set(cell) <= {"-", ":", " "} for cell in cells):
                continue
            table.append(cells)
            continue
        rows.extend(rows_from_table(table))
        table = []
    rows.extend(rows_from_table(table))
    return rows


def rows_from_table(table: list[list[str]]) -> list[dict[str, str]]:
    if len(table) < 2:
        return []
    header = table[0]
    return [dict(zip(header, row)) for row in table[1:] if len(row) == len(header)]


def parse_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_rows(path: Path) -> list[dict[str, str]]:
    if path.suffix.lower() in {".tsv", ".tab"}:
        return parse_tsv(path)
    return parse_markdown_tables(path)


def row_value(row: dict[str, str], column: str) -> str:
    return (row.get(column) or "").strip()


def validate(path: Path) -> list[str]:
    rows = load_rows(path)
    errors: list[str] = []
    if not rows:
        return [f"{path}: no matrix rows found"]

    matrix_rows = [row for row in rows if set(REQUIRED_COLUMNS).issubset(row)]
    if not matrix_rows:
        return [f"{path}: no generation matrix table found"]

    headers = set(matrix_rows[0])
    missing = [column for column in REQUIRED_COLUMNS if column not in headers]
    if missing:
        errors.append(f"{path}: missing columns: {', '.join(missing)}")
        return errors

    seen_ids: set[str] = set()
    seen_duplicate_keys: dict[tuple[str, ...], str] = {}
    for idx, row in enumerate(matrix_rows, start=2):
        matrix_id = row_value(row, "Matrix Row ID")
        if not matrix_id:
            errors.append(f"{path}:{idx}: empty Matrix Row ID")
        elif matrix_id in seen_ids:
            errors.append(f"{path}:{idx}: duplicate Matrix Row ID '{matrix_id}'")
        seen_ids.add(matrix_id)

        blob = " ".join(row.values())
        if BIDV_PATH_RE.search(blob):
            errors.append(f"{path}:{idx}: raw BIDV path reference is not allowed")

        status = row_value(row, "Coverage Status")
        if status not in VALID_STATUSES:
            errors.append(f"{path}:{idx}: invalid Coverage Status '{status}'")

        source_ref = row_value(row, "Source Ref")
        source_kind = row_value(row, "Source Kind")
        if status != "open_question" and not source_ref:
            errors.append(f"{path}:{idx}: Source Ref is required unless Coverage Status is open_question")
        if source_kind and source_kind not in VALID_SOURCE_KINDS:
            errors.append(f"{path}:{idx}: invalid Source Kind '{source_kind}'")

        for column in ["Field Or Rule", "Rule Type", "Technique", "Value Class", "Rationale"]:
            if not row_value(row, column):
                errors.append(f"{path}:{idx}: empty required column '{column}'")

        td_id = row_value(row, "TD ID")
        tc_id = row_value(row, "Test Case ID")
        if td_id and not TD_ID_RE.match(td_id):
            errors.append(f"{path}:{idx}: invalid TD ID '{td_id}'")
        if tc_id and not TC_ID_RE.match(tc_id):
            errors.append(f"{path}:{idx}: invalid Test Case ID '{tc_id}'")
        if status == "covered" and not (td_id or tc_id):
            errors.append(f"{path}:{idx}: covered row must reference TD ID or Test Case ID")

        duplicate_key = (
            row_value(row, "Business Variant"),
            row_value(row, "Flow Or Screen"),
            row_value(row, "API Endpoint"),
            row_value(row, "Field Or Rule"),
            row_value(row, "Rule Type"),
            row_value(row, "Technique"),
            row_value(row, "Value Class"),
        )
        if duplicate_key in seen_duplicate_keys and status != "duplicate":
            errors.append(f"{path}:{idx}: potential duplicate of {seen_duplicate_keys[duplicate_key]} without duplicate status")
        else:
            seen_duplicate_keys[duplicate_key] = matrix_id or f"row {idx}"
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate test generation coverage matrix")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    errors = validate(args.path)
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, ensure_ascii=True, indent=2))
        return 1
    print(json.dumps({"status": "passed", "path": str(args.path)}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
