#!/usr/bin/env python3
"""Validate testcase coverage categories for generated TSV artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

LEGACY_19_HEADER = [
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

TEXT_COLUMNS = [
    "Group Tests",
    "Scenario Outline",
    "Test Case Summary",
    "Pre-conditions",
    "Test Datas",
    "Test Steps",
    "Expected result",
    "Notes",
]

PROFILE_REQUIREMENTS: dict[str, list[str]] = {
    "api_legacy_19_column_testcase": [
        "METHOD",
        "CONTENT_TYPE",
        "AUTH",
        "MANDATORY_HEADERS",
        "LANGUAGE",
        "BODY_SCHEMA",
        "BOUNDARY",
        "BUSINESS_ERROR",
        "RESPONSE_SCHEMA",
        "ERROR_PRIORITY",
    ],
    "ui_legacy_19_column_testcase": [
        "NAVIGATION",
        "FIELD_VALIDATION",
        "REQUIRED_FIELDS",
        "FORMAT_VALIDATION",
        "BOUNDARY",
        "BUSINESS_RULE",
        "ROLE_PERMISSION",
        "STATE_TRANSITION",
        "ERROR_MESSAGE",
        "DATA_PERSISTENCE",
        "CANCEL_BACK_REFRESH",
    ],
    "uat_legacy_19_column_testcase": [
        "HAPPY_PATH",
        "ALTERNATE_PATH",
        "NEGATIVE_BUSINESS_RULE",
        "ROLE_OR_ACTOR",
        "PRECONDITION",
        "POSTCONDITION",
        "APPROVAL_FLOW",
        "INTEGRATION_POINT",
        "DATA_CONSISTENCY",
        "EXCEPTION_FLOW",
    ],
    "data_legacy_19_column_testcase": [
        "SOURCE_TARGET_MAPPING",
        "MANDATORY_DATA",
        "TYPE_FORMAT",
        "TRANSFORMATION_RULE",
        "FILTER_CONDITION",
        "AGGREGATION",
        "DUPLICATE_HANDLING",
        "NULL_EMPTY_HANDLING",
        "RECONCILIATION",
        "AUDIT_LOG",
    ],
    "file_batch_legacy_19_column_testcase": [
        "FILE_FORMAT",
        "FILE_STRUCTURE",
        "MANDATORY_COLUMNS",
        "ROW_LEVEL_VALIDATION",
        "BOUNDARY_VOLUME",
        "DUPLICATE_FILE_OR_ROW",
        "PROCESSING_STATUS",
        "ERROR_FILE_OR_MESSAGE",
        "SCHEDULE_TRIGGER",
        "OUTPUT_REPORT",
    ],
}

COVERAGE_MARKER_RE = re.compile(r"\bCoverage\s*:\s*([A-Z][A-Z0-9_ /-]*)", re.I)

FALLBACK_KEYWORDS: dict[str, list[re.Pattern[str]]] = {
    "METHOD": [re.compile(r"\bmethod\b|\bGET\b|\bPOST\b|\bPUT\b|\bPATCH\b|\bDELETE\b", re.I)],
    "CONTENT_TYPE": [re.compile(r"content[- ]?type|application/json|application/xml|text/plain|malformed json", re.I)],
    "AUTH": [re.compile(r"authToken|authorization|token|xác thực|hết hạn", re.I)],
    "MANDATORY_HEADERS": [re.compile(r"header|requestID|X-App-Code|app code|channel", re.I)],
    "LANGUAGE": [re.compile(r"Accept-language|language|ngôn ngữ|\bvi\b|\ben\b", re.I)],
    "BODY_SCHEMA": [re.compile(r"schema|body|requestCif|missing field|wrong type|sai kiểu|thiếu field|rỗng", re.I)],
    "BOUNDARY": [re.compile(r"boundary|length|độ dài|max|min|vượt|quá dài", re.I)],
    "BUSINESS_ERROR": [re.compile(r"business|nghiệp vụ|mã lỗi|error code|code=\"?\d{3}\"?|code `?\d{3}`?", re.I)],
    "RESPONSE_SCHEMA": [re.compile(r"response schema|success response|failure response|response body|traceId|responseTime|errors|null", re.I)],
    "ERROR_PRIORITY": [re.compile(r"priority|ưu tiên|multiple|nhiều lỗi|thứ tự lỗi", re.I)],
    "NAVIGATION": [re.compile(r"navigation|điều hướng|mở màn hình|page|screen|button|link", re.I)],
    "FIELD_VALIDATION": [re.compile(r"field validation|validate field|nhập hợp lệ|không hợp lệ", re.I)],
    "REQUIRED_FIELDS": [re.compile(r"required|mandatory|bắt buộc|bỏ trống|thiếu", re.I)],
    "FORMAT_VALIDATION": [re.compile(r"format|định dạng|email|date|ngày|ký tự đặc biệt", re.I)],
    "BUSINESS_RULE": [re.compile(r"business rule|nghiệp vụ|rule", re.I)],
    "ROLE_PERMISSION": [re.compile(r"role|permission|quyền|phân quyền|user without", re.I)],
    "STATE_TRANSITION": [re.compile(r"state|status|trạng thái|transition|approve|reject|submit", re.I)],
    "ERROR_MESSAGE": [re.compile(r"error message|message lỗi|thông báo lỗi|toast|alert", re.I)],
    "DATA_PERSISTENCE": [re.compile(r"persist|lưu|hiển thị lại|database|db|record", re.I)],
    "CANCEL_BACK_REFRESH": [re.compile(r"cancel|back|refresh|hủy|quay lại|tải lại|session timeout", re.I)],
    "HAPPY_PATH": [re.compile(r"happy path|success|thành công|luồng chính", re.I)],
    "ALTERNATE_PATH": [re.compile(r"alternate|nhánh phụ|luồng phụ", re.I)],
    "NEGATIVE_BUSINESS_RULE": [re.compile(r"negative business|fail nghiệp vụ|business error", re.I)],
    "ROLE_OR_ACTOR": [re.compile(r"actor|role|vai trò|người dùng", re.I)],
    "PRECONDITION": [re.compile(r"precondition|tiền điều kiện|điều kiện đầu vào", re.I)],
    "POSTCONDITION": [re.compile(r"postcondition|hậu điều kiện|sau xử lý", re.I)],
    "APPROVAL_FLOW": [re.compile(r"approval|approve|reject|return|phê duyệt|từ chối|trả lại", re.I)],
    "INTEGRATION_POINT": [re.compile(r"integration|tích hợp|hệ thống ngoài|external system", re.I)],
    "DATA_CONSISTENCY": [re.compile(r"consistency|nhất quán|đối soát|reconcile", re.I)],
    "EXCEPTION_FLOW": [re.compile(r"exception|timeout|duplicate|expired|invalid state|ngoại lệ", re.I)],
    "SOURCE_TARGET_MAPPING": [re.compile(r"source.*target|mapping|ánh xạ", re.I)],
    "MANDATORY_DATA": [re.compile(r"mandatory data|dữ liệu bắt buộc|thiếu dữ liệu", re.I)],
    "TYPE_FORMAT": [re.compile(r"type|format|kiểu|định dạng", re.I)],
    "TRANSFORMATION_RULE": [re.compile(r"transform|transformation|biến đổi|chuyển đổi", re.I)],
    "FILTER_CONDITION": [re.compile(r"filter|include|exclude|điều kiện lọc", re.I)],
    "AGGREGATION": [re.compile(r"aggregation|sum|count|group|tổng hợp", re.I)],
    "DUPLICATE_HANDLING": [re.compile(r"duplicate|trùng|unique", re.I)],
    "NULL_EMPTY_HANDLING": [re.compile(r"null|empty|default|rỗng", re.I)],
    "RECONCILIATION": [re.compile(r"reconciliation|reconcile|đối soát", re.I)],
    "AUDIT_LOG": [re.compile(r"audit|log|tracking|nhật ký", re.I)],
    "FILE_FORMAT": [re.compile(r"file format|định dạng file|xlsx|csv|pdf|txt", re.I)],
    "FILE_STRUCTURE": [re.compile(r"file structure|header|sheet|layout|cấu trúc file", re.I)],
    "MANDATORY_COLUMNS": [re.compile(r"mandatory column|required column|thiếu cột|cột bắt buộc", re.I)],
    "ROW_LEVEL_VALIDATION": [re.compile(r"row level|dòng lỗi|từng dòng|row validation", re.I)],
    "BOUNDARY_VOLUME": [re.compile(r"volume|file rỗng|nhiều dòng|vượt giới hạn|boundary volume", re.I)],
    "DUPLICATE_FILE_OR_ROW": [re.compile(r"duplicate file|duplicate row|trùng file|trùng dòng|trùng key", re.I)],
    "PROCESSING_STATUS": [re.compile(r"processing status|success|failed|partial|trạng thái xử lý", re.I)],
    "ERROR_FILE_OR_MESSAGE": [re.compile(r"error file|file lỗi|message lỗi|thông báo lỗi", re.I)],
    "SCHEDULE_TRIGGER": [re.compile(r"schedule|trigger|batch|lịch|manual trigger", re.I)],
    "OUTPUT_REPORT": [re.compile(r"output report|report|báo cáo|export", re.I)],
}


def normalize_cell(value: str | None) -> str:
    return (value or "").strip().strip('"')


def read_legacy_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        try:
            raw_header = next(reader)
        except StopIteration:
            return [], []
        header = [normalize_cell(cell) for cell in raw_header]
        rows: list[dict[str, str]] = []
        for raw_row in reader:
            if not any(normalize_cell(cell) for cell in raw_row):
                continue
            padded = raw_row + [""] * max(0, len(header) - len(raw_row))
            rows.append({column: normalize_cell(padded[index]) for index, column in enumerate(header)})
        return header, rows


def row_text(row: dict[str, str]) -> str:
    return "\n".join(row.get(column, "") for column in TEXT_COLUMNS)


def normalize_category(value: str) -> str:
    value = value.strip().upper()
    value = re.split(r"[\]\[\)\(,.;:\n\r]", value, maxsplit=1)[0]
    value = re.sub(r"[^A-Z0-9_]+", "_", value).strip("_")
    return value


def detect_marker_category(text: str, requirements: list[str]) -> str | None:
    for match in COVERAGE_MARKER_RE.finditer(text):
        category = normalize_category(match.group(1))
        if category in requirements:
            return category
    return None


def detect_fallback_category(text: str, requirements: list[str]) -> str | None:
    for category in requirements:
        for pattern in FALLBACK_KEYWORDS.get(category, []):
            if pattern.search(text):
                return category
    return None


def detect_categories(rows: list[dict[str, str]], requirements: list[str]) -> tuple[dict[str, int], dict[str, list[str]]]:
    coverage = {category: 0 for category in requirements}
    category_texts = {category: [] for category in requirements}
    for row in rows:
        text = row_text(row)
        category = detect_marker_category(text, requirements) or detect_fallback_category(text, requirements)
        if category is None:
            continue
        coverage[category] += 1
        category_texts[category].append(text)
    return coverage, category_texts


def validate_response_schema(category_texts: dict[str, list[str]]) -> list[str]:
    texts = category_texts.get("RESPONSE_SCHEMA", [])
    if not texts:
        return []
    combined = "\n".join(texts)
    errors = []
    if not re.search(r"success|thành công|code\s*=\s*\"?0\"?", combined, re.I):
        errors.append("missing required coverage detail: RESPONSE_SCHEMA success schema")
    if not re.search(r"failure|fail|error|lỗi|success\s*=\s*false", combined, re.I):
        errors.append("missing required coverage detail: RESPONSE_SCHEMA failure schema")
    return errors


def validate(path: Path, profile: str) -> tuple[int, dict[str, object]]:
    requirements = PROFILE_REQUIREMENTS.get(profile)
    if requirements is None:
        return 2, {"status": "failed", "errors": [f"unknown profile: {profile}"]}

    header, rows = read_legacy_tsv(path)
    errors: list[str] = []
    if header != LEGACY_19_HEADER:
        errors.append("header does not match legacy 19-column canonical header")
    if not rows:
        errors.append("no testcase rows found")

    coverage, category_texts = detect_categories(rows, requirements)
    for category in requirements:
        if coverage.get(category, 0) == 0:
            errors.append(f"missing required coverage category: {category}")

    if profile == "api_legacy_19_column_testcase" and coverage.get("RESPONSE_SCHEMA", 0) > 0:
        errors.extend(validate_response_schema(category_texts))

    if errors:
        return 1, {"status": "failed", "errors": errors}

    return 0, {
        "status": "passed",
        "rows_checked": len(rows),
        "profile": profile,
        "coverage": {category: coverage[category] for category in requirements if coverage[category] > 0},
    }


def build_parser(default_profile: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate generated testcase coverage categories.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--profile", default=default_profile, choices=sorted(PROFILE_REQUIREMENTS))
    return parser


def main(default_profile: str | None = None) -> int:
    parser = build_parser(default_profile)
    args = parser.parse_args()
    if not args.profile:
        parser.error("--profile is required")
    exit_code, payload = validate(args.path, args.profile)
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
