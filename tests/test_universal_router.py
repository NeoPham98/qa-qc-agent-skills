from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sdk"))

from intent_classifier import classify_intent
from route_planner import plan_route
from source_fingerprint import fingerprint_sources
from source_manifest import SourceManifest, SourceItem, SourceFingerprint
from workflow_pack_loader import load_workflow_pack


def manifest_with(role: str, prompt: str) -> SourceManifest:
    return SourceManifest(
        schema_version="1.0",
        run_id="test-run",
        user_prompt=prompt,
        output_directory="out",
        sources=[SourceItem(
            id="source-1",
            kind="local_file",
            original_locator="api.md",
            extension=".md",
            fingerprint=SourceFingerprint(candidate_roles=[role]),
        )],
    )


def test_api_spec_to_testcase_route():
    manifest = manifest_with("api_spec", "Sinh testcase BIDV 19 cột")
    cls = classify_intent(manifest)
    assert cls.request_type == "api_spec_to_testcase"
    workflow = load_workflow_pack(ROOT, "default")
    plan = plan_route(workflow, cls)
    assert "API_TestDesign.md" in plan.final_outputs
    assert "Legacy19TestCase.generated.xlsx" in plan.final_outputs


def test_api_spec_to_automation_route():
    manifest = manifest_with("api_spec", "Sinh test API automation gherkin feature")
    cls = classify_intent(manifest)
    assert cls.request_type == "api_spec_to_automation"
    workflow = load_workflow_pack(ROOT, "default")
    plan = plan_route(workflow, cls)
    assert "api_validation.feature" in plan.final_outputs


def test_executed_workbook_to_dashboard_route():
    manifest = manifest_with("executed_workbook", "Đọc kết quả execute và tạo dashboard trạng thái")
    cls = classify_intent(manifest)
    assert cls.request_type == "executed_workbook_to_dashboard"
    workflow = load_workflow_pack(ROOT, "default")
    plan = plan_route(workflow, cls)
    assert "TestExecution.from-manual.tsv" in plan.final_outputs
    assert "PaygatesDashboard.generated.xlsx" in plan.final_outputs
