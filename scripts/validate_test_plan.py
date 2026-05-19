#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED_METADATA = [
    "Test Plan ID",
    "Project",
    "Squad",
    "Epic",
    "Environment",
    "Build/Release",
]
REQUIRED_SECTIONS = [
    "Scope In",
    "Scope Out",
    "Source Baseline",
    "Requirement Baseline",
    "Test Levels / Phases",
    "Entry Criteria",
    "Exit Criteria",
    "Deliverables",
    "Roles and Responsibilities",
    "Environment / Test Data / Dependencies",
    "Risks and Mitigations",
    "Schedule / Milestones",
    "Coverage Strategy",
    "Open Questions",
]
VALID_SOURCE_KINDS = {
    "runtime_input",
    "normalized_knowledge",
    "workflow_pack_contract",
    "prompt_contract",
    "golden_example",
}
DELIVERABLE_TOKENS = [
    "test design",
    "testcase",
    "test case",
    "execution",
    "dashboard",
    "coverage matrix",
    "automation",
    ".feature",
]
BIDV_PATH_RE = re.compile(r"(^|[\\/`\s])BIDV[\\/]", re.I)
METADATA_RE = re.compile(r"^\*\*(?P<key>[^*]+)\*\*\s*:\s*(?P<value>.*)$")
HEADING_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$", re.MULTILINE)
PENDING_RE = re.compile(r"^\[PENDING_DOC:[^\]]+\]$")


def parse_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        match = METADATA_RE.match(line.strip())
        if match:
            metadata[match.group("key").strip()] = match.group("value").strip()
    return metadata


def parse_markdown_tables(section: str) -> list[dict[str, str]]:
    tables: list[dict[str, str]] = []
    table: list[list[str]] = []
    for line in [*section.splitlines(), ""]:
        stripped = line.strip()
        if stripped.startswith("|"):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if all(set(cell) <= {"-", ":", " "} for cell in cells):
                continue
            table.append(cells)
            continue
        if len(table) >= 2:
            header = table[0]
            tables.extend(dict(zip(header, row)) for row in table[1:] if len(row) == len(header))
        table = []
    return tables


def section_text(text: str, title: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(title)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    next_match = re.search(r"^##\s+", text[match.end() :], re.MULTILINE)
    if not next_match:
        return text[match.end() :]
    return text[match.end() : match.end() + next_match.start()]


def has_substantive_content(section: str) -> bool:
    for line in section.splitlines():
        stripped = line.strip()
        if stripped and not set(stripped) <= {"|", "-", ":", " "}:
            return True
    return False


def row_value(row: dict[str, str], *names: str) -> str:
    for name in names:
        value = (row.get(name) or "").strip()
        if value:
            return value
    return ""


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8-sig")
    errors: list[str] = []

    if BIDV_PATH_RE.search(text):
        errors.append(f"{path}: raw BIDV path reference is not allowed")

    metadata = parse_metadata(text)
    for key in REQUIRED_METADATA:
        value = metadata.get(key, "").strip()
        if not value:
            errors.append(f"{path}: missing metadata '{key}'")
        elif value.startswith("{{") or value.endswith("}}"):
            errors.append(f"{path}: unresolved template metadata '{key}'")
        elif value.startswith("[PENDING_DOC:") and not PENDING_RE.match(value):
            errors.append(f"{path}: invalid pending marker for '{key}'")

    headings = {match.group("title").strip() for match in HEADING_RE.finditer(text)}
    for title in REQUIRED_SECTIONS:
        if title not in headings:
            errors.append(f"{path}: missing section '## {title}'")
        elif not has_substantive_content(section_text(text, title)):
            errors.append(f"{path}: empty section '## {title}'")

    source_rows = parse_markdown_tables(section_text(text, "Source Baseline"))
    if not source_rows:
        errors.append(f"{path}: Source Baseline must include at least one source row")
    for idx, row in enumerate(source_rows, start=1):
        source_ref = row_value(row, "Source Ref", "Source ID", "Source")
        source_kind = row_value(row, "Source Kind", "Kind")
        if not source_ref:
            errors.append(f"{path}: Source Baseline row {idx} missing Source Ref")
        if source_kind and source_kind not in VALID_SOURCE_KINDS:
            errors.append(f"{path}: Source Baseline row {idx} invalid Source Kind '{source_kind}'")
        if not row_value(row, "Scope", "Purpose", "Note"):
            errors.append(f"{path}: Source Baseline row {idx} missing Scope/Purpose/Note")

    requirement_rows = parse_markdown_tables(section_text(text, "Requirement Baseline"))
    if not requirement_rows:
        errors.append(f"{path}: Requirement Baseline must include at least one requirement row")

    deliverables = section_text(text, "Deliverables").lower()
    if deliverables and not any(token in deliverables for token in DELIVERABLE_TOKENS):
        errors.append(f"{path}: Deliverables must include at least one downstream artifact")

    coverage = section_text(text, "Coverage Strategy").lower()
    if coverage and "coveragematrix" not in coverage and "coverage matrix" not in coverage and "testgenerationmatrix" not in coverage:
        errors.append(f"{path}: Coverage Strategy must reference CoverageMatrix or TestGenerationMatrix")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Test Plan Markdown contract")
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
