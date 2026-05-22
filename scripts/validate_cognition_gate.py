from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_ARTIFACTS = [
    "SourceInventory.md",
    "DocumentMap.md",
    "FactInventory.md",
    "RiskModel.md",
    "CoveragePlan.md",
    "TesterStrategyPlan.md",
    "QuestionBacklog.md",
]

COVERAGE_CLASSES = [
    "happy",
    "exception",
    "negative",
    "boundary",
    "response",
    "error",
    "business",
    "cross",
    "state",
    "permission",
    "regression",
]

SOURCE_TRACE_RE = re.compile(r"(source[-_ ]?\d+|source ref|source refs|section|page|sheet|\[PENDING_DOC:[^\]]+\])", re.IGNORECASE)
SECRET_RE = re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[^\s'\"]{12,}")
BLOCKER_RE = re.compile(r"(?i)(blocker|blocking|chặn|cản trở)")
PROCEED_RE = re.compile(r"(?i)(proceed rule|proceed-with-pending|continue|tiếp tục|rationale|lý do)")
HYPOTHESIS_CONFIRMED_RE = re.compile(r"(?i)(hypothesis|giả thuyết).{0,80}(confirmed|requirement|business rule|must|shall|bắt buộc)")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def validate_gate(output_dir: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_ARTIFACTS:
        if not (output_dir / name).exists():
            errors.append(f"missing required cognition gate artifact: {name}")
    if not (output_dir / "BusinessRuleModel.md").exists():
        open_questions = read_text(output_dir / "OpenQuestions.md")
        if not open_questions or not BLOCKER_RE.search(open_questions):
            errors.append("missing BusinessRuleModel.md and no blocker OpenQuestions.md")
    business_rules = read_text(output_dir / "BusinessRuleModel.md")
    if business_rules and not SOURCE_TRACE_RE.search(business_rules):
        errors.append("BusinessRuleModel.md lacks source refs or [PENDING_DOC] markers")
    question_backlog = read_text(output_dir / "QuestionBacklog.md")
    if BLOCKER_RE.search(question_backlog) and not PROCEED_RE.search(question_backlog):
        errors.append("QuestionBacklog.md has blocker questions without proceed rule")
    coverage_plan = read_text(output_dir / "CoveragePlan.md").lower()
    if coverage_plan:
        missing_coverage = [name for name in COVERAGE_CLASSES if name not in coverage_plan]
        if missing_coverage and "not applicable" not in coverage_plan and "n/a" not in coverage_plan:
            errors.append(f"CoveragePlan.md missing coverage classes or rationale: {', '.join(missing_coverage)}")
    for path in output_dir.glob("*.md"):
        text = read_text(path)
        if SECRET_RE.search(text):
            errors.append(f"{path.name}: possible unredacted secret")
        if HYPOTHESIS_CONFIRMED_RE.search(text):
            errors.append(f"{path.name}: hypothesis appears to be treated as confirmed requirement")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AI Tester cognition gate before output generation")
    parser.add_argument("output_dir")
    args = parser.parse_args()
    errors = validate_gate(Path(args.output_dir))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("cognition gate validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
