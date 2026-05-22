from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_METADATA = [
    "Artifact ID",
    "Project",
    "Squad",
    "Epic",
    "Source Refs",
    "Created By",
    "Created At",
    "Confidence",
    "Open Questions",
]

SOURCE_TRACE_RE = re.compile(r"(source[-_ ]?\d+|source ref|source refs|normalized knowledge|section|page|sheet|\[PENDING_DOC:[^\]]+\])", re.IGNORECASE)
SECRET_RE = re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[^\s'\"]{12,}")
TESTCASE_ROW_RE = re.compile(r"TD_P[123]_\d{3}_TC_\d{3}|\t.*\t.*\t")
HYPOTHESIS_AS_RULE_RE = re.compile(r"(?i)(hypothesis|giả thuyết).{0,80}(confirmed|requirement|business rule|must|shall|bắt buộc)")


def validate_artifact(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing artifact: {path}"]
    text = path.read_text(encoding="utf-8")
    for field in REQUIRED_METADATA:
        if not re.search(rf"(^|[#*\-\s]){re.escape(field)}\s*:", text, re.IGNORECASE | re.MULTILINE):
            errors.append(f"{path.name}: missing metadata field {field}")
    if "[PENDING_DOC:" not in text and not SOURCE_TRACE_RE.search(text):
        errors.append(f"{path.name}: missing source trace marker or [PENDING_DOC] marker")
    if SECRET_RE.search(text):
        errors.append(f"{path.name}: possible unredacted secret")
    if path.name not in {"TestCaseSource.md", "UAT_TestCaseSource.md"} and TESTCASE_ROW_RE.search(text):
        errors.append(f"{path.name}: cognition artifact appears to contain final testcase rows")
    if HYPOTHESIS_AS_RULE_RE.search(text):
        errors.append(f"{path.name}: hypothesis appears to be treated as confirmed rule")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AI Tester cognition artifact metadata and safety rules")
    parser.add_argument("artifacts", nargs="+")
    args = parser.parse_args()
    errors: list[str] = []
    for artifact in args.artifacts:
        errors.extend(validate_artifact(Path(artifact)))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("cognition artifact validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
