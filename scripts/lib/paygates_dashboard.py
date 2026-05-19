from __future__ import annotations

import csv
from pathlib import Path

try:
    from markdown_tables import parse_markdown_table
except ImportError:
    from .markdown_tables import parse_markdown_table

HEADERS = [
    "Project / Product Scope",
    "Squad",
    "Sprint",
    "Epic / Function",
    "Requirement ID",
    "Test Condition ID",
    "Test Set ID",
    "Detail Artifact Link",
    "Passed",
    "Failed",
    "Untested",
    "Accepted",
    "N/A",
    "Total Test cases",
    "Current test status",
    "Test case generate type",
    "Automation test status",
    "Open Questions",
]

COUNT_COLUMNS = ["Passed", "Failed", "Untested", "Accepted", "N/A", "Total Test cases"]
STATUS_MAP = {
    "pass": "Passed",
    "passed": "Passed",
    "fail": "Failed",
    "failed": "Failed",
    "not run": "Untested",
    "pending": "Untested",
    "untested": "Untested",
    "": "Untested",
    "accepted": "Accepted",
    "n/a": "N/A",
    "na": "N/A",
    "not applicable": "N/A",
}
ALLOWED_CURRENT_STATUS = {"Failed", "Untested", "Completed", "In-Test", "N/A"}


def load_rows(path: Path) -> list[dict[str, str]]:
    if path.suffix.lower() in {".tsv", ".csv"}:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f, delimiter="\t"))
    return parse_markdown_table(path.read_text(encoding="utf-8-sig"))


def normalize_status(value: str | None) -> str:
    key = (value or "").strip().lower()
    return STATUS_MAP.get(key, value.strip() if value else "Untested")


def pending(value: str | None, field: str, questions: list[str]) -> str:
    if value and value.strip():
        return value.strip()
    marker = f"[PENDING_DOC:{field}]"
    questions.append(marker)
    return marker


def current_status(counts: dict[str, int]) -> str:
    total = counts["Total Test cases"]
    if total and counts["N/A"] == total:
        return "N/A"
    if counts["Failed"] > 0:
        return "Failed"
    if total and counts["Untested"] == total:
        return "Untested"
    if total and counts["Untested"] == 0:
        return "Completed"
    return "In-Test"


def aggregate_dashboard(
    testcase_rows: list[dict[str, str]],
    execution_rows: list[dict[str, str]] | None = None,
    metadata: dict[str, str] | None = None,
) -> dict[str, str]:
    metadata = metadata or {}
    questions: list[str] = []
    case_ids = [row.get("Test Case ID", "").strip() for row in testcase_rows if row.get("Test Case ID", "").strip()]
    execution_by_case: dict[str, str] = {}
    test_set_ids: set[str] = set()
    if execution_rows:
        for row in execution_rows:
            case_id = row.get("Test Case ID", "").strip()
            if case_id:
                execution_by_case[case_id] = normalize_status(row.get("Status", ""))
            if row.get("Test Set ID", "").strip():
                test_set_ids.add(row["Test Set ID"].strip())

    counts = {"Passed": 0, "Failed": 0, "Untested": 0, "Accepted": 0, "N/A": 0, "Total Test cases": len(case_ids)}
    for case_id in case_ids:
        status = execution_by_case.get(case_id, "Untested")
        if status not in counts:
            questions.append(f"[PENDING_DOC:unsupported_status:{case_id}:{status}]")
            status = "Untested"
        counts[status] += 1

    requirement_ids = sorted({row.get("Requirement ID", "").strip() for row in testcase_rows if row.get("Requirement ID", "").strip()})
    condition_ids = sorted({row.get("Test Condition ID", "").strip() for row in testcase_rows if row.get("Test Condition ID", "").strip()})

    generate_type = metadata.get("generate_type") or metadata.get("test_case_generate_type")
    automation_status = metadata.get("automation_status") or metadata.get("automation_test_status")
    if not generate_type:
        generate_type = "[PENDING_DOC:test_case_generate_type]"
        questions.append(generate_type)
    if not automation_status:
        automation_status = "[PENDING_DOC:automation_status]"
        questions.append(automation_status)

    row = {
        "Project / Product Scope": pending(metadata.get("project"), "project", questions),
        "Squad": pending(metadata.get("squad"), "squad", questions),
        "Sprint": pending(metadata.get("sprint"), "sprint", questions),
        "Epic / Function": pending(metadata.get("epic") or metadata.get("function"), "epic", questions),
        "Requirement ID": ", ".join(requirement_ids),
        "Test Condition ID": ", ".join(condition_ids),
        "Test Set ID": metadata.get("test_set_id", ", ".join(sorted(test_set_ids))),
        "Detail Artifact Link": pending(metadata.get("detail_link"), "detail_artifact_link", questions),
        "Passed": str(counts["Passed"]),
        "Failed": str(counts["Failed"]),
        "Untested": str(counts["Untested"]),
        "Accepted": str(counts["Accepted"]),
        "N/A": str(counts["N/A"]),
        "Total Test cases": str(counts["Total Test cases"]),
        "Current test status": current_status(counts),
        "Test case generate type": generate_type,
        "Automation test status": automation_status,
        "Open Questions": "; ".join(dict.fromkeys(questions)),
    }
    return row


def validate_dashboard_rows(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    if not rows:
        return ["dashboard has no data rows"]
    for idx, row in enumerate(rows, start=2):
        missing = [header for header in HEADERS if header not in row]
        if missing:
            errors.append(f"row {idx}: missing columns: {', '.join(missing)}")
            continue
        counts: dict[str, int] = {}
        for column in COUNT_COLUMNS:
            value = (row.get(column) or "").strip()
            if not value.isdigit():
                errors.append(f"row {idx}: {column} must be a non-negative integer")
                value = "0"
            counts[column] = int(value)
        subtotal = counts["Passed"] + counts["Failed"] + counts["Untested"] + counts["Accepted"] + counts["N/A"]
        if subtotal != counts["Total Test cases"]:
            errors.append(f"row {idx}: counts do not reconcile with Total Test cases")
        if (row.get("Current test status") or "").strip() not in ALLOWED_CURRENT_STATUS:
            errors.append(f"row {idx}: unsupported Current test status '{row.get('Current test status', '')}'")
        for required in ["Project / Product Scope", "Squad", "Sprint", "Epic / Function", "Detail Artifact Link"]:
            if not (row.get(required) or "").strip():
                errors.append(f"row {idx}: empty required column '{required}'")
    return errors
