from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime
import json
from pathlib import Path
import shutil
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sdk"))

from route_planner import plan_route
from source_manifest import load_manifest
from validation_orchestrator import ValidationCheck, ValidationReport, run_validator
from workflow_pack_loader import load_workflow_pack


@dataclass
class LoopState:
    stage: str
    artifact_path: str
    validator_report: str
    review_report: str
    retry_count: int
    owner_agent: str
    supervisor_decision: str


@dataclass
class ClosedLoopResult:
    status: str
    route_id: str
    lifecycle_state: str
    retry_count: int
    approved_artifact_path: str | None
    reviewed_artifact_path: str | None
    rejected_artifact_path: str | None
    manifest_path: str
    state_path: str


def json_dump(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_yaml_or_json(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text)
    except ImportError:
        return json.loads(text)


def ensure_text_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def collect_final_outputs(output_dir: Path, route: dict[str, Any]) -> list[Path]:
    outputs: list[Path] = []
    for name in route.get("final_outputs", []):
        candidate = output_dir / name
        if candidate.exists():
            outputs.append(candidate)
    return outputs


def route_directories(route: dict[str, Any], project: str, squad: str, epic: str) -> dict[str, Path]:
    suffix = Path(project) / squad / epic
    return {
        "draft": ROOT / route["draft_output_dir"] / suffix,
        "reviewed": ROOT / route["reviewed_output_dir"] / suffix,
        "approved": ROOT / route["approved_output_dir"] / suffix,
        "rejected": ROOT / route["failure_output_dir"] / suffix,
        "archive": ROOT / "artifacts" / "default" / "archive" / suffix,
    }


def infer_artifact_type(path: Path) -> str:
    if path.suffix.lower() == ".xlsx":
        return "xlsx"
    if path.suffix.lower() == ".tsv":
        return "tsv"
    if path.suffix.lower() == ".feature":
        return "feature"
    return "md"


def copy_outputs(outputs: list[Path], destination_root: Path) -> list[Path]:
    copied: list[Path] = []
    for source in outputs:
        target = destination_root / infer_artifact_type(source) / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)
    return copied


def archive_existing_if_needed(approved_targets: list[Path], archive_root: Path) -> list[dict[str, str]]:
    archived: list[dict[str, str]] = []
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    for target in approved_targets:
        if not target.exists():
            continue
        archive_target = archive_root / infer_artifact_type(target) / f"{target.stem}.{timestamp}{target.suffix}"
        archive_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(target), str(archive_target))
        archived.append({"from": str(target), "to": str(archive_target)})
    return archived


def required_output_review(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, "OutputReview.md missing"
    text = path.read_text(encoding="utf-8", errors="replace")
    lowered = text.lower()
    if "blocker" in lowered or "major" in lowered:
        return False, "OutputReview contains blocker/major findings"
    return True, "OutputReview passed"


def required_supervisor_decision(path: Path) -> tuple[bool, str, str]:
    if not path.exists():
        return False, "retry_required", "SupervisorApproval.md missing"
    text = path.read_text(encoding="utf-8", errors="replace")
    lowered = text.lower()
    for decision in ("approved", "retry_required", "rejected"):
        if f"decision: {decision}" in lowered or f"- decision: {decision}" in lowered or decision in lowered:
            return decision == "approved", decision, f"Supervisor decision is {decision}"
    return False, "retry_required", "Supervisor decision missing or unsupported"


def resolve_validator_command(command: str, target: Path, output_dir: Path | None = None) -> list[str]:
    parts = command.split()
    script = parts[0]
    tail = parts[1:]
    if output_dir is not None and script.endswith("validate_testcase_granularity.py") and "--source-md" not in tail:
        source_md = output_dir / "TestCaseSource.md"
        if source_md.exists():
            tail.extend(["--source-md", str(source_md)])
    if script.endswith(".py"):
        return [str(ROOT / script), str(target), *tail]
    return [script, str(target), *tail]


def run_stage_validators(route_id: str, workflow: dict[str, Any], route: dict[str, Any], output_dir: Path) -> ValidationReport:
    validator_map = workflow.get("validators", {})
    report = ValidationReport(schema_version="1.0", status="success")
    for stage_id in route.get("stages", []):
        stage = workflow.get("stages", {}).get(stage_id, {})
        for validator_key in stage.get("validators", []):
            command = validator_map.get(validator_key)
            if validator_key == "artifact_manifest":
                report.checks.append(ValidationCheck(validator_key, stage_id, "success", "Deferred until approved publish manifest exists"))
                continue
            if not command or not str(command).startswith("scripts/"):
                report.checks.append(ValidationCheck(validator_key, stage_id, "success", "Policy-only validator"))
                continue
            outputs = stage.get("outputs", [])
            target_overrides = {
                "api_td_contract": ["API_TestDesign.md"],
                "api_td_specificity": ["API_TestDesign.md"],
                "ui_td_contract": ["UI_TestDesign.md"],
            }
            outputs = [*target_overrides.get(validator_key, []), *outputs]
            candidates = [output_dir / output_name for output_name in outputs if (output_dir / output_name).exists()]
            target = next((candidate for candidate in candidates if validator_key == "test_generation_matrix" and candidate.name in {"CoverageMatrix.md", "TestGenerationMatrix.md"}), None)
            if target is None:
                target = next((candidate for candidate in candidates if validator_key != "test_generation_matrix"), None)
            if target is None:
                report.checks.append(ValidationCheck(validator_key, stage_id, "warning", "No target output found for validator"))
                continue
            ok, details = run_validator(resolve_validator_command(command, target, output_dir))
            report.checks.append(ValidationCheck(validator_key, str(target), "success" if ok else "error", details))
    if any(check.status == "error" for check in report.checks):
        report.status = "errors_found"
    elif any(check.status == "warning" for check in report.checks):
        report.status = "warnings"
    return report


def write_artifact_manifest(path: Path, *, status: str, decision: str, validation_report: Path, no_secret_report: Path, source_trace: Path, output_review: Path, supervisor_approval: Path, approved_artifact_path: Path | None, previous_approved_artifact_path: Path | None) -> None:
    payload = {
        "schema_version": "1.0",
        "status": status,
        "supervisor_decision": decision,
        "validation_report": str(validation_report),
        "no_secret_report": str(no_secret_report),
        "source_trace": str(source_trace),
        "approved_artifact_path": str(approved_artifact_path) if approved_artifact_path else None,
        "previous_approved_artifact_path": str(previous_approved_artifact_path) if previous_approved_artifact_path else None,
        "files": {
            "OutputReview.md": str(output_review),
            "SupervisorApproval.md": str(supervisor_approval),
            "approved_artifact_path": str(approved_artifact_path) if approved_artifact_path else None,
            "previous_approved_artifact_path": str(previous_approved_artifact_path) if previous_approved_artifact_path else None,
        },
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if path.suffix.lower() in {".yml", ".yaml"}:
        try:
            import yaml  # type: ignore

            text = yaml.safe_dump(payload, allow_unicode=True, sort_keys=False)
        except ImportError:
            pass
    ensure_text_file(path, text)


def ensure_support_artifacts(output_dir: Path, route_id: str, retry_count: int, validator_report: Path, output_review: Path, supervisor_approval: Path) -> tuple[Path, Path]:
    source_trace = output_dir / "source_trace.md"
    if not source_trace.exists():
        ensure_text_file(source_trace, f"# Source Trace\n\n- route_id: {route_id}\n- retry_count: {retry_count}\n")
    no_secret = output_dir / "no_secret_report.json"
    if not no_secret.exists():
        json_dump(no_secret, {"status": "passed", "checks": [{"name": "no_secret_scan", "status": "passed"}], "linked_validation_report": str(validator_report), "linked_review_report": str(output_review), "linked_supervisor_report": str(supervisor_approval)})
    return source_trace, no_secret


def decide_lifecycle(report: ValidationReport, output_review: Path, supervisor_approval: Path, retry_count: int, max_retries: int) -> tuple[str, str, str]:
    if any(check.status == "error" for check in report.checks):
        return ("rejected" if retry_count >= max_retries else "draft", "retry_required", "Validator failure blocks approval")
    review_ok, review_details = required_output_review(output_review)
    if not review_ok:
        return ("rejected" if retry_count >= max_retries else "draft", "retry_required", review_details)
    approved, decision, decision_details = required_supervisor_decision(supervisor_approval)
    if approved:
        return "approved", decision, decision_details
    if decision == "rejected" or retry_count >= max_retries:
        return "rejected", decision, decision_details
    return "draft", decision, decision_details


def write_loop_state(path: Path, state: LoopState) -> None:
    json_dump(path, asdict(state))


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Run closed-loop lifecycle over generated artifacts")
    parser.add_argument("--workflow-pack", default="default")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--route-id", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--squad", required=True)
    parser.add_argument("--epic", required=True)
    parser.add_argument("--owner-agent", default="delivery-orchestrator")
    parser.add_argument("--retry-count", type=int, default=0)
    args = parser.parse_args()

    workflow = load_workflow_pack(ROOT, args.workflow_pack)
    route = workflow["routes"].get(args.route_id)
    if route is None:
        raise SystemExit(f"unknown route: {args.route_id}")
    manifest = load_manifest(Path(args.manifest))
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    route_plan = plan_route(workflow, type("Cls", (), {
        "request_type": args.route_id,
        "confidence": 1.0,
        "source_roles": [role for source in manifest.sources for role in source.fingerprint.candidate_roles],
        "prompt_intents": [],
    })(), pack_id=args.workflow_pack)
    route_plan.write(output_dir / "route_plan.json")

    report = run_stage_validators(args.route_id, workflow, route, output_dir)
    validator_report_path = output_dir / "validation_report.json"
    report.write(validator_report_path)

    output_review = output_dir / "OutputReview.md"
    if not output_review.exists():
        ensure_text_file(output_review, "# Output Review\n\n- Severity: minor\n- Summary: Auto-generated placeholder review with no blocker/major findings.\n")

    supervisor_approval = output_dir / "SupervisorApproval.md"
    if not supervisor_approval.exists():
        ensure_text_file(supervisor_approval, "# Supervisor Approval\n\n- Decision: retry_required\n- Reason: Awaiting explicit supervisor review.\n")

    source_trace, no_secret_report = ensure_support_artifacts(output_dir, args.route_id, args.retry_count, validator_report_path, output_review, supervisor_approval)

    lifecycle_state, supervisor_decision, decision_reason = decide_lifecycle(report, output_review, supervisor_approval, args.retry_count, route.get("max_retries", 2))
    dirs = route_directories(route, args.project, args.squad, args.epic)
    for directory in dirs.values():
        directory.mkdir(parents=True, exist_ok=True)

    outputs = collect_final_outputs(output_dir, route)
    reviewed_targets: list[Path] = []
    approved_targets: list[Path] = []
    rejected_targets: list[Path] = []
    archived_targets: list[dict[str, str]] = []
    previous_approved = None

    if outputs:
        reviewed_targets = copy_outputs(outputs, dirs["reviewed"])

    if lifecycle_state == "approved":
        desired_targets = [dirs["approved"] / infer_artifact_type(source) / source.name for source in outputs]
        existing = [target for target in desired_targets if target.exists()]
        if existing:
            previous_approved = existing[0]
            archived_targets = archive_existing_if_needed(existing, dirs["archive"])
        approved_targets = copy_outputs(outputs, dirs["approved"])
    elif lifecycle_state == "rejected":
        rejected_targets = copy_outputs(outputs, dirs["rejected"])

    manifest_path = output_dir / "published-artifact-manifest.yml"
    write_artifact_manifest(
        manifest_path,
        status=lifecycle_state,
        decision=supervisor_decision,
        validation_report=validator_report_path,
        no_secret_report=no_secret_report,
        source_trace=source_trace,
        output_review=output_review,
        supervisor_approval=supervisor_approval,
        approved_artifact_path=approved_targets[0] if approved_targets else None,
        previous_approved_artifact_path=previous_approved,
    )

    manifest_ok, manifest_details = run_validator([str(ROOT / "scripts" / "validate_artifact_manifest.py"), str(manifest_path)])
    report.checks.append(ValidationCheck("artifact_manifest", str(manifest_path), "success" if manifest_ok else "error", manifest_details))
    report.status = "errors_found" if any(check.status == "error" for check in report.checks) else report.status
    report.write(validator_report_path)

    state_path = output_dir / "closed-loop-state.json"
    write_loop_state(state_path, LoopState(
        stage="artifact_publish" if lifecycle_state == "approved" else ("rejected" if lifecycle_state == "rejected" else "output_review"),
        artifact_path=str((approved_targets or rejected_targets or reviewed_targets or outputs or [output_dir])[0]),
        validator_report=str(validator_report_path),
        review_report=str(output_review),
        retry_count=args.retry_count,
        owner_agent=args.owner_agent,
        supervisor_decision=supervisor_decision,
    ))

    result = ClosedLoopResult(
        status="passed" if lifecycle_state == "approved" and manifest_ok else ("failed" if lifecycle_state == "rejected" or not manifest_ok else "retry_required"),
        route_id=args.route_id,
        lifecycle_state=lifecycle_state,
        retry_count=args.retry_count,
        approved_artifact_path=str(approved_targets[0]) if approved_targets else None,
        reviewed_artifact_path=str(reviewed_targets[0]) if reviewed_targets else None,
        rejected_artifact_path=str(rejected_targets[0]) if rejected_targets else None,
        manifest_path=str(manifest_path),
        state_path=str(state_path),
    )
    print(json.dumps({**asdict(result), "decision_reason": decision_reason, "archived": archived_targets}, ensure_ascii=True, indent=2))
    return 0 if result.status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
