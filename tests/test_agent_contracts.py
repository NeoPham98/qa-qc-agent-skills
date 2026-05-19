from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"

REQUIRED_AGENT_FILES = [
    "delivery-orchestrator/AGENT.md",
    "knowledge-retriever/AGENT.md",
    "api-test-design-agent/AGENT.md",
    "ui-test-design-agent/AGENT.md",
    "testcase-generator/AGENT.md",
    "test-set-execution-manager/AGENT.md",
    "output-reviewer/AGENT.md",
    "contract-validator/AGENT.md",
    "supervisor/AGENT.md",
]


def read_agent(relative_path: str) -> str:
    return (AGENTS / relative_path).read_text(encoding="utf-8")


def test_all_agents_define_inputs_outputs_and_forbidden_behavior() -> None:
    for relative_path in REQUIRED_AGENT_FILES:
        text = read_agent(relative_path)
        assert "## Required inputs" in text or "## Inputs" in text, relative_path
        assert "## Required output" in text or "## Required outputs" in text or "## Outputs" in text, relative_path
        assert "Forbidden behavior" in text, relative_path
        assert "source trace" in text.lower() or "source reference" in text.lower() or "source references" in text.lower(), relative_path


def test_orchestrator_encodes_closed_loop_company_machine() -> None:
    text = read_agent("delivery-orchestrator/AGENT.md")

    assert "Project → Squad → Epic" in text
    assert "Test Design → Test Case" in text
    assert "manual execution import/status update" in text
    assert "output_review → supervisor_approval → artifact_publish" in text
    assert "artifacts/default/draft" in text
    assert "artifacts/default/approved" in text


def test_knowledge_retriever_refuses_raw_sensitive_sources() -> None:
    text = read_agent("knowledge-retriever/AGENT.md")

    assert "knowledge/default/redacted/" in text
    assert "properties.txt" in text
    assert "redaction_status: redacted" in text
    assert "Do not expose bearer tokens" in text


def test_api_td_agent_enforces_phases_and_control_params() -> None:
    text = read_agent("api-test-design-agent/AGENT.md")

    for token in ["TD_P1", "TD_P2", "TD_P3", "METHOD_CHECK", "CONTENT_TYPE_CHECK", "MANDATORY_CHECK", "TYPE_CHECK", "LENGTH_CHECK", "SCOPE_FIELDS", "EG_CHECK"]:
        assert token in text
    assert "validate_test_design.py --type api" in text


def test_ui_td_agent_enforces_canonical_id_format() -> None:
    text = read_agent("ui-test-design-agent/AGENT.md")

    assert "### TD_NNN [Technique] <condition>" in text
    assert "TD_NNN" in text
    assert "validate_test_design.py --type ui" in text


def test_testcase_generator_enforces_19col_and_uat_contracts() -> None:
    text = read_agent("testcase-generator/AGENT.md")

    assert "exactly 18 tabs" in text
    assert "Quote all cells" in text
    assert "logical `\\n`" in text
    assert "TD_P[123]_NNN_TC_NNN" in text
    assert "TD_NNN_TC_NNN" in text
    assert "UAT 16-column" in text
    assert "Negative API cases do not verify DB" in text
    assert "Primary Condition" in text
    assert "1 testcase = 1 primary condition" in text
    assert "validate_testcase_granularity.py" in text
    assert "Do not bundle multiple invalid inputs" in text


def test_execution_reviewer_validator_and_supervisor_have_separate_gates() -> None:
    execution = read_agent("test-set-execution-manager/AGENT.md")
    reviewer = read_agent("output-reviewer/AGENT.md")
    validator = read_agent("contract-validator/AGENT.md")
    supervisor = read_agent("supervisor/AGENT.md")

    assert "status-enums.yml" in execution
    assert "Read to UAT" in execution
    assert "Do not silently fix generator-owned artifacts" in reviewer
    assert "Paygates dashboard/tracker" in validator
    assert "SupervisorApproval.md" in supervisor
    assert "max_retries: 2" in supervisor
    assert "Do not publish rejected or retry-required artifacts" in supervisor


if __name__ == "__main__":
    test_all_agents_define_inputs_outputs_and_forbidden_behavior()
    test_orchestrator_encodes_closed_loop_company_machine()
    test_knowledge_retriever_refuses_raw_sensitive_sources()
    test_api_td_agent_enforces_phases_and_control_params()
    test_ui_td_agent_enforces_canonical_id_format()
    test_testcase_generator_enforces_19col_and_uat_contracts()
    test_execution_reviewer_validator_and_supervisor_have_separate_gates()
    print("test_agent_contracts: PASS")
