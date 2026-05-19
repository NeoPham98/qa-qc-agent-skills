#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

HEADER_ALIASES = {
    "Test Case / Summary": "Test Case Summary",
    "Expected / result": "Expected result",
    "Manual Test Results / Round 1": "Manual Test Results Round 1",
    "Notes ": "Notes",
    "Test Data": "Test Datas",
}

LEGACY_19_HEADERS = [
    "Test Case ID",
    "Function",
    "Group Tests",
    "Scenario Outline",
    "Test Case Summary",
    "Pre-conditions",
    "Test Datas",
    "Test Steps",
    "Expected result",
    "Environment",
    "Priority",
    "Regression",
    "Automation",
    "Manual Test Results Round 1",
    "Manual Test Results Round 2",
    "Automation Test Results",
    "Actual result",
    "BugID",
    "Notes",
]

UAT_16_HEADERS = [
    "Test Case ID",
    "Test Case Name",
    "Precondition",
    "Test Steps",
    "Test Data",
    "Expected Result",
    "Priority",
    "Test Type",
    "Module",
    "Requirement ID",
    "Execution Result",
    "Actual Result",
    "Bug ID",
    "Tester",
    "Execution Date",
    "Notes",
]

MARKER_RE = re.compile(r"\b(Primary Condition|Primary Target|Atomic Target)\s*:\s*([^\n\r;]+(?:;[^\n\r]+)?)", re.I)
ALLOW_COMBINED_RE = re.compile(
    r"cross-field|decision table|combined rule|business rule|form-level rule|combined ui rule|quy tắc kết hợp|luật nghiệp vụ kết hợp",
    re.I,
)
GENERIC_API_RE = re.compile(r"^(invalid data|data không hợp lệ|verify error|check validation|validate error|kiểm tra lỗi)$", re.I)
CONNECTOR_RE = re.compile(r"\s(?:and|và)\s|\s\+\s|/|;|,", re.I)
MARKER_BOUNDARY_RE = re.compile(r"\b(?:Source|Coverage)\s*:", re.I)
FIELD_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9_]*(?:Cif|Id|ID|Code|Type|Status|Amount|Date|Currency|Account|Header|Token)?\b")
INVALID_RE = re.compile(
    r"missing|invalid|wrong type|empty|inactive|required|omitted|length|enum|format|boundary|disabled|thiếu|sai|không hợp lệ|rỗng",
    re.I,
)
UAT_TRANSITION_RE = re.compile(r"\b(approve|reject|cancel|phê duyệt|từ chối|hủy)\b", re.I)
API_TARGET_RE = re.compile(
    r"method|content-type|header|body|query|path|param|field|request|response|business|rule|[A-Za-z][A-Za-z0-9_]*(?:Cif|Id|ID|Code|Type|Status|Amount|Date|Currency|Account)",
    re.I,
)
UI_MULTI_RE = re.compile(r"username|password|button|popup|message|role|table|filter|sort|pagination|screen|navigation|field|action|state", re.I)
UAT_TECH_RE = re.compile(r"\b(css|dom|xpath|selector|html|locator)\b", re.I)
UAT_BUSINESS_RE = re.compile(r"approve|reject|cancel|request|business|checker|maker|approval|transition|outcome|rule|actor|phê duyệt|từ chối|nghiệp vụ", re.I)
GENERIC_STEP_RE = re.compile(
    r"send request with atomic target|send request with primary condition|verify http status and response body|prepare [A-Z]+ /[^\n]+\s+2\. set required headers",
    re.I,
)
GENERIC_DATA_RE = re.compile(r"^(valid data|invalid data|data hợp lệ|data không hợp lệ|như trên|same as above)$", re.I)

PROFILES = {
    "api_legacy_19_column_testcase",
    "ui_legacy_19_column_testcase",
    "uat_16_column_testcase",
}


def normalize_header(value: str) -> str:
    stripped = value.strip()
    return HEADER_ALIASES.get(value, HEADER_ALIASES.get(stripped, stripped))


def parse_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def row_value(row: dict[str, str], key: str) -> str:
    for raw_key, value in row.items():
        if raw_key is None:
            continue
        if raw_key.strip() == key or normalize_header(raw_key) == key:
            return value or ""
    return ""


def find_primary_condition(row: dict[str, str], fields: list[str]) -> str | None:
    blob = "\n".join(row_value(row, field).replace("\\n", "\n") for field in fields)
    match = MARKER_RE.search(blob)
    if not match:
        return None
    condition = match.group(2).strip()
    condition = MARKER_BOUNDARY_RE.split(condition, maxsplit=1)[0].strip()
    condition = condition.rstrip(";| ").strip()
    return re.split(r"\s{2,}|\\n", condition, maxsplit=1)[0].strip()


def message(path: Path, row_no: int, tc_id: str, rule: str) -> str:
    return f"{path}:{row_no}: {tc_id or '[missing Test Case ID]'}: {rule}"


def likely_bundled(condition: str) -> bool:
    if ALLOW_COMBINED_RE.search(condition):
        return False
    lowered = condition.lower()
    if CONNECTOR_RE.search(condition):
        terms = [term.strip() for term in re.split(r"\s(?:and|và)\s|\s\+\s|/|;|,", lowered) if term.strip()]
        meaningful_terms = [term for term in terms if INVALID_RE.search(term) or UI_MULTI_RE.search(term) or API_TARGET_RE.search(term)]
        if len(meaningful_terms) >= 2:
            return True
    fields = {match.group(0).lower() for match in FIELD_RE.finditer(condition)}
    invalid_terms = INVALID_RE.findall(condition)
    return len(fields) >= 2 and len(invalid_terms) >= 2


def validate_headers(path: Path, headers: list[str], profile: str) -> list[str]:
    normalized = [normalize_header(header) for header in headers]
    expected = UAT_16_HEADERS if profile == "uat_16_column_testcase" else LEGACY_19_HEADERS
    if profile == "uat_16_column_testcase":
        header_matches = normalized == expected or [header.strip() for header in headers] == expected
    else:
        header_matches = normalized == expected
    if not header_matches:
        return [f"{path}: header does not match expected profile {profile}"]
    return []


def validate_row(path: Path, row_no: int, row: dict[str, str], profile: str) -> list[str]:
    errors: list[str] = []
    tc_id = row_value(row, "Test Case ID")
    steps = row_value(row, "Test Steps")
    data = row_value(row, "Test Datas") or row_value(row, "Test Data")
    expected = row_value(row, "Expected result") or row_value(row, "Expected Result")
    if profile == "uat_16_column_testcase":
        condition = find_primary_condition(row, ["Test Case Name", "Test Data", "Expected Result"])
    else:
        condition = find_primary_condition(row, ["Test Case Summary", "Test Datas", "Expected result"])

    if GENERIC_STEP_RE.search(steps.replace("\\n", "\n")):
        errors.append(message(path, row_no, tc_id, "test steps use generic reusable API prose instead of exact mutation/verify detail"))
    if GENERIC_DATA_RE.match(data.strip()):
        errors.append(message(path, row_no, tc_id, "test data is generic instead of concrete field=value or value class"))
    if re.search(r"status and response body|correct result|expected result|kết quả đúng", expected, re.I):
        errors.append(message(path, row_no, tc_id, "expected result is generic instead of measurable status/message/field/state"))

    if not condition:
        return [message(path, row_no, tc_id, "missing Primary Condition, Primary Target, or Atomic Target marker")]

    if likely_bundled(condition):
        errors.append(message(path, row_no, tc_id, "bundles multiple independent conditions in one testcase"))

    if profile == "api_legacy_19_column_testcase":
        if GENERIC_API_RE.search(condition.strip()):
            errors.append(message(path, row_no, tc_id, "uses generic API primary condition"))
        if re.search(r"missing|invalid|wrong type|required|omitted|thiếu|sai|không hợp lệ", condition, re.I) and not API_TARGET_RE.search(condition):
            errors.append(message(path, row_no, tc_id, "API negative case does not name exact field/header/param/path/body/business target"))
        if re.search(r"\b(verify|assert|check)\b", condition, re.I) and not API_TARGET_RE.search(condition):
            errors.append(message(path, row_no, tc_id, "primary condition looks like generic verify/check prose"))

    if profile == "ui_legacy_19_column_testcase":
        if likely_bundled(condition) and not ALLOW_COMBINED_RE.search(condition):
            errors.append(message(path, row_no, tc_id, "UI testcase combines multiple fields/actions/states"))

    if profile == "uat_16_column_testcase":
        if UAT_TECH_RE.search(condition):
            errors.append(message(path, row_no, tc_id, "UAT primary condition is technical UI detail instead of business-facing"))
        if not UAT_BUSINESS_RE.search(condition):
            errors.append(message(path, row_no, tc_id, "UAT primary condition is not business-facing"))
        transitions = {match.group(0).lower() for match in UAT_TRANSITION_RE.finditer(condition)}
        if len(transitions) >= 2 and not ALLOW_COMBINED_RE.search(condition):
            errors.append(message(path, row_no, tc_id, "bundles multiple independent conditions in one testcase"))

    return errors


def validate(path: Path, profile: str) -> list[str]:
    headers, rows = parse_tsv(path)
    errors = validate_headers(path, headers, profile)
    if not rows:
        errors.append(f"{path}: no testcase rows")
    for row_no, row in enumerate(rows, start=2):
        errors.extend(validate_row(path, row_no, row, profile))
    return errors


def validate_testcase_source_md(source_md_path: Path) -> list[str]:
    text = source_md_path.read_text(encoding="utf-8-sig")
    errors: list[str] = []

    api_tc_re = re.compile(r"\bTD_P[123]_\d+_TC_\d+\b")
    ui_tc_re = re.compile(r"\bTD_\d+_TC_\d+\b")
    ids_found = set(api_tc_re.findall(text)) | set(ui_tc_re.findall(text))

    if not ids_found:
        errors.append(
            f"{source_md_path}: appears metadata-only; no testcase IDs found (expected TD_P[123]_..._TC_... or TD_..._TC_...)"
        )

    primary_marker_re = re.compile(r"\b(Primary Condition|Primary Target|Atomic Target)\s*:", re.I)
    if not primary_marker_re.search(text):
        errors.append(f"{source_md_path}: missing Primary Condition/Primary Target/Atomic Target markers")

    content_markers = ["Pre-conditions", "Test Datas", "Test Steps", "Expected result", "Test Case ID", "Open Questions"]
    if not any(marker.lower() in text.lower() for marker in content_markers):
        errors.append(
            f"{source_md_path}: missing testcase execution content markers (expected preconditions/test steps/test data/expected result/open questions)"
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate testcase granularity")
    parser.add_argument("path", type=Path)
    parser.add_argument("--profile", choices=sorted(PROFILES), required=True)
    parser.add_argument(
        "--source-md",
        type=Path,
        default=None,
        help="Optional TestCaseSource.md path to validate it contains real testcase execution content",
    )
    args = parser.parse_args()

    errors = validate(args.path, args.profile)
    if args.source_md is not None:
        errors.extend(validate_testcase_source_md(args.source_md))

    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, ensure_ascii=True, indent=2))
        return 1
    print(json.dumps({"status": "passed", "profile": args.profile, "path": str(args.path)}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
