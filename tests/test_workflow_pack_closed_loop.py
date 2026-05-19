from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "workflow-packs" / "default"


def load_workflow() -> dict:
    return json.loads((PACK / "workflow.json").read_text(encoding="utf-8"))


def load_yaml(name: str) -> dict:
    return yaml.safe_load((PACK / name).read_text(encoding="utf-8"))


def test_every_route_has_review_supervisor_and_publish_gates() -> None:
    workflow = load_workflow()

    for route_id, route in workflow["routes"].items():
        stages = route["stages"]
        assert "output_review" in stages, route_id
        assert "supervisor_approval" in stages, route_id
        assert "artifact_publish" in stages, route_id
        assert stages.index("output_review") < stages.index("supervisor_approval") < stages.index("artifact_publish"), route_id
        assert route["max_retries"] == 2, route_id
        assert route["draft_output_dir"] == "artifacts/default/draft", route_id
        assert route["reviewed_output_dir"] == "artifacts/default/reviewed", route_id
        assert route["approved_output_dir"] == "artifacts/default/approved", route_id
        assert route["failure_output_dir"] == "artifacts/default/rejected", route_id


def test_source_bootstrap_routes_are_available() -> None:
    workflow = load_workflow()

    assert {"source_inventory", "source_normalization", "secret_redaction", "knowledge_validation"} <= set(workflow["routes"])
    assert {"source_inventory", "source_normalization", "secret_redaction", "knowledge_validation", "secret_validation"} <= set(workflow["stages"])


def test_validation_stages_exist_before_review_for_core_routes() -> None:
    workflow = load_workflow()
    expected_validation_stage = {
        "api_spec_to_test_design": "api_td_validation",
        "api_spec_to_testcase": "api_tc_validation",
        "api_test_design_to_testcase": "api_tc_validation",
        "api_spec_to_automation": "api_tc_validation",
        "ui_source_to_test_design": "ui_td_validation",
        "ui_source_to_testcase": "ui_tc_validation",
        "ui_test_design_to_testcase": "ui_tc_validation",
        "urd_to_uat_testcase": "uat_tc_validation",
        "executed_workbook_to_dashboard": "tracker_validation",
        "testcase_to_dashboard": "tracker_validation",
    }

    for route_id, validation_stage in expected_validation_stage.items():
        stages = workflow["routes"][route_id]["stages"]
        assert validation_stage in stages, route_id
        assert stages.index(validation_stage) < stages.index("output_review"), route_id


def test_workflow_registers_specificity_granularity_and_coverage_validators() -> None:
    workflow = load_workflow()

    assert {
        "api_td_specificity",
        "api_tc_specificity",
        "api_tc_granularity",
        "ui_tc_granularity",
        "uat_tc_granularity",
        "testcase_coverage_api",
        "testcase_coverage_ui",
        "testcase_coverage_uat",
        "testcase_coverage_data",
        "testcase_coverage_file_batch",
    } <= set(workflow["validators"])
    assert workflow["stages"]["api_td_validation"]["validators"] == ["api_td_contract", "api_td_specificity"]
    assert workflow["stages"]["api_tc_validation"]["outputs"] == ["Legacy19TestCase.generated.tsv"]
    assert workflow["stages"]["api_tc_validation"]["validators"] == [
        "api_tc_specificity",
        "api_tc_granularity",
        "testcase_coverage_api",
    ]
    assert workflow["stages"]["ui_tc_validation"]["validators"] == ["ui_tc_granularity", "testcase_coverage_ui"]
    assert workflow["stages"]["uat_tc_validation"]["validators"] == ["uat_tc_granularity"]


def test_artifact_policy_has_required_lifecycle_states() -> None:
    policy = load_yaml("artifact-policy.yml")

    assert set(policy["states"]) == {"draft", "reviewed", "approved", "rejected", "archive"}
    assert policy["publish_rules"]["generator_writes_only"] == "draft"
    assert policy["publish_rules"]["approved_overwrite_policy"] == "forbid_overwrite_use_archive_or_version_suffix"
    assert {"validation_report", "OutputReview.md", "SupervisorApproval.md", "no_secret_report"} <= set(policy["required_approved_evidence"])


def test_review_gates_require_supervisor_after_review() -> None:
    gates = load_yaml("review-gates.yml")

    assert gates["output_review"]["required"] is True
    assert gates["output_review"]["reviewer_must_not_be_generator"] is True
    assert gates["supervisor_approval"]["required"] is True
    assert gates["supervisor_approval"]["must_follow"] == "output_review"
    assert "all_validators_passed" in gates["supervisor_approval"]["approve_only_if"]
    assert "no_secrets_detected" in gates["supervisor_approval"]["approve_only_if"]


if __name__ == "__main__":
    test_every_route_has_review_supervisor_and_publish_gates()
    test_source_bootstrap_routes_are_available()
    test_validation_stages_exist_before_review_for_core_routes()
    test_workflow_registers_specificity_granularity_and_coverage_validators()
    test_artifact_policy_has_required_lifecycle_states()
    test_review_gates_require_supervisor_after_review()
    print("test_workflow_pack_closed_loop: PASS")
