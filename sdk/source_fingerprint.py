from __future__ import annotations

from pathlib import Path

from source_adapters.local_files import sample_text
from source_manifest import SourceItem

HEADER_ROLE_MAP = {
    "legacy_testcase": {"Test Case ID", "Function", "Group Tests", "Scenario Outline", "Test Case Summary", "Pre-conditions", "Test Datas", "Test Steps", "Expected result"},
    "executed_workbook": {"Manual Test Results Round 1", "Manual Test Results Round 2", "Automation Test Results", "Actual result", "BugID", "Notes"},
    "manual_execution_result": {"Status", "Actual Result", "Tester", "Execution Date", "BugID"},
}

FILENAME_KEYWORDS = {
    "api_spec": ["api", "swagger", "openapi", "endpoint", "service", "sdk"],
    "ui_spec": ["ui", "screen", "màn hình", "mh", "frontend", "giao diện"],
    "rsd": ["rsd", "requirement", "yêu cầu"],
    "pttk": ["pttk", "thiết kế", "technical"],
    "urd": ["urd", "business", "nghiệp vụ"],
    "test_design": ["testdesign", "test_design", "td"],
    "legacy_testcase": ["testcase", "test_case", "19col", "va_"],
}

CONTENT_KEYWORDS = {
    "api_spec": ["endpoint", "request", "response", "method", "header", "schema", "authorization", "content-type", "http"],
    "ui_spec": ["màn hình", "field", "button", "nút", "validation", "message", "thông báo", "tìm kiếm", "thêm mới", "chỉnh sửa"],
    "rsd": ["use case", "actor", "luồng", "nghiệp vụ", "điều kiện", "ngoại lệ"],
    "pttk": ["database", "sequence", "api", "request", "response", "service", "table"],
    "urd": ["mục tiêu", "phạm vi", "business", "người dùng", "quy trình"],
    "test_design": ["td_p1", "td_p2", "td_p3", "test condition", "markmap"],
    "api_test_design": ["td_p1", "td_p2", "td_p3", "method", "header", "schema", "business logic"],
    "api_testcase": ["endpoint", "request body", "response", "http status", "td_p"],
}


def fingerprint_sources(sources: list[SourceItem], base_dir: Path | None = None) -> list[SourceItem]:
    for source in sources:
        source.fingerprint.candidate_roles = infer_roles(source, base_dir=base_dir)
    return sources


def infer_roles(source: SourceItem, base_dir: Path | None = None) -> list[str]:
    roles: list[str] = []
    headers = set(source.fingerprint.detected_headers)
    for role, required in HEADER_ROLE_MAP.items():
        if len(required & headers) >= min(3, len(required)):
            roles.append(role)
    name = source.original_locator.lower()
    for role, keywords in FILENAME_KEYWORDS.items():
        if any(keyword.lower() in name for keyword in keywords):
            roles.append(role)
    text = ""
    if source.local_path:
        path = Path(source.local_path)
        if not path.is_absolute() and base_dir is not None:
            path = base_dir / path
        text = sample_text(path).lower() if path.exists() else ""
    for role, keywords in CONTENT_KEYWORDS.items():
        matches = [keyword for keyword in keywords if keyword.lower() in text]
        if len(matches) >= 2:
            roles.append(role)
            source.fingerprint.detected_keywords.extend(matches[:8])
    if source.kind == "google_sheet" and any(role in roles for role in ["executed_workbook", "manual_execution_result"]):
        roles.append("google_sheet_execution")
    if not roles and source.extension == ".xlsx":
        roles.append("legacy_testcase")
    if not roles and source.extension in {".pdf", ".doc", ".docx"}:
        roles.append("business_requirement")
    return sorted(set(roles))
