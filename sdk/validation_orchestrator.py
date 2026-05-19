from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from pathlib import Path
import subprocess
import sys

from route_planner import RoutePlan

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class ValidationCheck:
    name: str
    target: str
    status: str
    details: str = ""


@dataclass
class ValidationReport:
    schema_version: str
    status: str
    checks: list[ValidationCheck] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")


def validate_matrix_artifact(output_dir: Path, plan: RoutePlan, report: ValidationReport) -> None:
    if "CoverageMatrix.md" not in [*plan.final_outputs, *plan.support_outputs]:
        return
    path = output_dir / "CoverageMatrix.md"
    if not path.exists():
        report.checks.append(ValidationCheck("coverage_matrix_exists", "CoverageMatrix.md", "pending", "Coverage matrix will be created during execution."))
        return
    ok, details = run_validator(["scripts/validate_test_generation_matrix.py", str(path)])
    report.checks.append(ValidationCheck("coverage_matrix_contract", "CoverageMatrix.md", "success" if ok else "error", details))


def validate_test_plan_artifact(output_dir: Path, plan: RoutePlan, report: ValidationReport) -> None:
    if "TestPlan.md" not in [*plan.final_outputs, *plan.support_outputs]:
        return
    path = output_dir / "TestPlan.md"
    if not path.exists():
        report.checks.append(ValidationCheck("test_plan_exists", "TestPlan.md", "pending", "Test plan will be created during execution."))
        return
    ok, details = run_validator(["scripts/validate_test_plan.py", str(path)])
    report.checks.append(ValidationCheck("test_plan_contract", "TestPlan.md", "success" if ok else "error", details))


def validate_api_automation_artifacts(output_dir: Path, plan: RoutePlan, report: ValidationReport) -> None:
    outputs = [*plan.final_outputs, *plan.support_outputs]
    analysis_path = output_dir / "API_TestCase_Analysis.md"
    source_path = output_dir / "TestCaseSource.md"
    if "API_TestCase_Analysis.md" in outputs:
        if not analysis_path.exists():
            report.checks.append(ValidationCheck("api_automation_analysis_exists", "API_TestCase_Analysis.md", "pending", "API automation analysis will be created during execution."))
        else:
            args = ["scripts/validate_api_automation_analysis.py", str(analysis_path)]
            if source_path.exists():
                args.extend(["--testcase-source", str(source_path)])
            ok, details = run_validator(args)
            report.checks.append(ValidationCheck("api_automation_analysis_contract", "API_TestCase_Analysis.md", "success" if ok else "error", details))

    feature_phases = {
        "api_method_header_validation.feature": "TD_P1",
        "api_validation.feature": "TD_P2",
        "api_logic_business.feature": "TD_P3",
    }
    for output in outputs:
        if not output.endswith(".feature"):
            continue
        path = output_dir / output
        if not path.exists():
            report.checks.append(ValidationCheck("api_automation_feature_exists", output, "pending", "API automation feature will be created during execution."))
            continue
        args = ["scripts/validate_api_automation_feature.py", str(path)]
        phase = feature_phases.get(output)
        if phase:
            args.extend(["--phase", phase])
        ok, details = run_validator(args)
        report.checks.append(ValidationCheck("api_automation_feature_contract", output, "success" if ok else "error", details))


def validate_no_bidv_runtime_refs(output_dir: Path, report: ValidationReport) -> None:
    if not output_dir.exists():
        return
    ok, details = run_validator(["scripts/validate_no_bidv_runtime_refs.py", str(output_dir)])
    report.checks.append(ValidationCheck("no_bidv_runtime_refs", str(output_dir), "success" if ok else "error", details))


def validate_planned_outputs(output_dir: Path, plan: RoutePlan) -> ValidationReport:
    report = ValidationReport(schema_version="1.0", status="success")
    for output in plan.final_outputs:
        path = output_dir / output
        if output == "OutputReview.md":
            if path.exists():
                report.checks.append(ValidationCheck("output_review_exists", output, "success"))
            else:
                report.checks.append(ValidationCheck("output_review_exists", output, "warning", "OutputReview is expected after generation."))
                report.warnings.append("OutputReview.md missing in plan/dry-run output")
            continue
        if path.exists():
            report.checks.append(ValidationCheck("final_output_exists", output, "success"))
        else:
            report.checks.append(ValidationCheck("final_output_exists", output, "pending", "Final output will be created during execution."))
    validate_matrix_artifact(output_dir, plan, report)
    validate_test_plan_artifact(output_dir, plan, report)
    validate_api_automation_artifacts(output_dir, plan, report)
    validate_no_bidv_runtime_refs(output_dir, report)
    if any(check.status == "error" for check in report.checks):
        report.status = "errors_found"
    elif report.warnings:
        report.status = "warnings"
    return report


def run_validator(args: list[str]) -> tuple[bool, str]:
    proc = subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=False)
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip()
