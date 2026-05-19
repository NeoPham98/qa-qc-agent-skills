from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sdk"))

from workflow_pack_loader import load_workflow_pack


def load_yaml(path: Path) -> dict:
    try:
        import yaml  # type: ignore
    except ImportError:  # pragma: no cover
        from workflow_pack_loader import parse_simple_yaml
        return parse_simple_yaml(path.read_text(encoding="utf-8"))
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def prompt_sources(canonical: dict) -> list[str]:
    sources: list[str] = []
    for section in [
        "api_test_design",
        "api_testcase",
        "api_automation_gherkin",
        "ui_test_design",
        "ui_testcase",
        "uat_testcase",
    ]:
        prompts = canonical[section]["canonical_prompts"]
        sources.extend(item["source_path"] for item in prompts.values())
    return sources


def test_canonical_sources_use_breakdown_api_prompts() -> None:
    canonical = load_yaml(ROOT / "knowledge" / "default" / "manifests" / "canonical-sources.yml")
    sources = prompt_sources(canonical)

    assert "Prompt/API/API_TD_2_Method_Header_BreakDown.txt" in sources
    assert "Prompt/API/API_TD_3_Schema_Validation_BreakDown.txt" in sources
    assert "Prompt/API/API_TD_4_Value_Business_Cross_Logic_BreakDown.txt" in sources
    assert "Prompt/API/[Old]_API_Gen_TC_From_TD.txt" not in sources
    assert "Prompt/API/[Old]_API_Gen_TD_v1.2.txt" not in sources


def test_workflow_pack_routes_to_canonical_runtime_prompts() -> None:
    workflow = load_workflow_pack(ROOT, "default")

    assert workflow["stages"]["api_td_method_header"]["prompt"] == "prompts/API/API_TD_2_Method_Header_BreakDown.txt"
    assert workflow["stages"]["api_td_schema_validation"]["prompt"] == "prompts/API/API_TD_3_Schema_Validation_BreakDown.txt"
    assert workflow["stages"]["api_td_business_logic"]["prompt"] == "prompts/API/API_TD_4_Value_Business_Cross_Logic_BreakDown.txt"


def test_runtime_canonical_sources_match_knowledge_registry() -> None:
    knowledge = load_yaml(ROOT / "knowledge" / "default" / "manifests" / "canonical-sources.yml")
    runtime = load_yaml(ROOT / "workflow-packs" / "default" / "canonical-sources.yml")

    assert runtime == knowledge
    assert runtime["sensitive_sources"]["properties"]["runtime_policy"] == "redact_before_use"
    assert runtime["legacy_sources"]["old_api_prompts"]["runtime_policy"] == "never_default_route"
