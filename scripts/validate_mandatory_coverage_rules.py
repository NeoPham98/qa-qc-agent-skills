#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

REQUIRED_TOP_LEVEL = {
    "version",
    "name",
    "default_profile",
    "principles",
    "api_rules",
    "ui_rules",
    "manual_execution_rules",
    "review_blockers",
}

REQUIRED_API_GROUPS = {
    "operation",
    "method_header",
    "schema_validation",
    "business_logic",
}

REQUIRED_BLOCKERS = {
    "happy_case_only_output",
    "bundled_independent_conditions",
    "missing_exception_cases_for_documented_errors",
    "missing_negative_validation_for_documented_required_inputs",
    "missing_boundary_cases_for_documented_length_or_range",
    "missing_response_error_coverage",
    "repurposed_canonical_testcase_id",
}


def load_yaml(path: Path) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML is required to validate mandatory coverage rules")
    data = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    return data or {}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    data = load_yaml(path)

    missing_top = REQUIRED_TOP_LEVEL - set(data)
    if missing_top:
        errors.append(f"{path}: missing top-level keys: {sorted(missing_top)}")

    api_rules = data.get("api_rules") or {}
    missing_api = REQUIRED_API_GROUPS - set(api_rules)
    if missing_api:
        errors.append(f"{path}: missing api rule groups: {sorted(missing_api)}")

    principles = data.get("principles") or []
    joined_principles = "\n".join(str(item).lower() for item in principles)
    if "happy" not in joined_principles or "never sufficient" not in joined_principles:
        errors.append(f"{path}: principles must state that happy-path coverage alone is insufficient")
    if "one primary condition" not in joined_principles:
        errors.append(f"{path}: principles must require one primary condition per testcase")

    blockers = set(data.get("review_blockers") or [])
    missing_blockers = REQUIRED_BLOCKERS - blockers
    if missing_blockers:
        errors.append(f"{path}: missing review blockers: {sorted(missing_blockers)}")

    operation_required = set((api_rules.get("operation") or {}).get("required") or [])
    for required in {"valid_request_success", "documented_exception_or_business_failure", "success_response_envelope", "failure_response_envelope"}:
        if required not in operation_required:
            errors.append(f"{path}: api_rules.operation.required missing {required}")

    business_required = set((api_rules.get("business_logic") or {}).get("required") or [])
    for required in {"one_case_per_documented_business_rule", "one_case_per_documented_error_code"}:
        if required not in business_required:
            errors.append(f"{path}: api_rules.business_logic.required missing {required}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate mandatory testcase coverage rules")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    try:
        errors = validate(args.path)
    except Exception as exc:
        errors = [f"{args.path}: {exc}"]

    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, ensure_ascii=True, indent=2))
        return 1
    print(json.dumps({"status": "passed", "path": str(args.path)}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
