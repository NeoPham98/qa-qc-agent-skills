from __future__ import annotations

from dataclasses import dataclass, field

from source_manifest import SourceManifest

INTENT_KEYWORDS = {
    "knowledge_setup": ["knowledge setup", "setup knowledge", "source inventory", "collect", "thu thập", "tri thức"],
    "input_understanding": ["understand", "input understanding", "skim", "skimming", "đọc hiểu", "hiểu input"],
    "document_analysis": ["document analysis", "analyze docs", "breakdown", "break down", "phân tích tài liệu", "bóc tách"],
    "knowledge_cooking": ["cook knowledge", "knowledge cooking", "cooking knowledge", "chuẩn hóa tri thức"],
    "business_rule_modeling": ["business rule", "rule model", "business model", "luật nghiệp vụ"],
    "coverage_modeling": ["coverage model", "mô hình coverage", "mô hình độ phủ"],
    "reasoning": ["reasoning", "reason", "suy luận", "risk reasoning"],
    "brainstorming": ["brainstorm", "brainstorming", "edge case", "defect hypothesis"],
    "planning": ["planning", "plan", "strategy", "test strategy", "lập kế hoạch"],
    "output_generation": ["generate output", "artifact", "sinh output", "ra output"],
    "review_learning": ["lesson", "learning", "memory update", "reflection", "học lại", "cập nhật memory"],
    "full_ai_tester_delivery": ["ai tester os", "qc senior", "senior qc", "full ai tester"],
    "test_design": ["test design", "td", "thiết kế test", "sinh td", "markmap"],
    "testcase": ["testcase", "test case", "test cases", "ca kiểm thử", "sinh tc"],
    "manual_testcase": ["manual", "tester execute", "execute manual", "kiểm thử thủ công"],
    "excel_19_col": ["19 cột", "19 column", "excel", "xlsx", "legacy file"],
    "uat": ["uat", "acceptance", "nghiệm thu"],
    "acceptance_test": ["acceptance test", "business test", "nghiệp vụ"],
    "automation_script": ["automation", "script", "sinh script", "auto test"],
    "gherkin": ["gherkin", "cucumber", "feature", ".feature"],
    "api_test": ["test api", "api test", "kiểm thử api"],
    "manual_execution": ["đọc kết quả", "execution result", "import result", "execute result"],
    "execution_result": ["round 1", "round 2", "actual result", "bugid", "status"],
    "dashboard": ["dashboard", "tổng hợp", "report", "báo cáo"],
    "status": ["trạng thái", "status", "pass", "fail", "untested"],
    "paygates_summary": ["paygates", "tổng hợp trạng thái test case"],
    "coverage_audit": ["coverage", "độ phủ", "audit"],
    "gap_analysis": ["gap", "thiếu", "đủ chưa"],
    "review": ["review", "đánh giá", "kiểm tra"],
    "full_delivery": ["full", "end-to-end", "từ đầu đến cuối"],
}


@dataclass
class IntentClassification:
    request_type: str
    confidence: float
    source_roles: list[str] = field(default_factory=list)
    prompt_intents: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    alternatives: list[str] = field(default_factory=list)
    missing_inputs: list[str] = field(default_factory=list)


def classify_intent(manifest: SourceManifest) -> IntentClassification:
    prompt = manifest.user_prompt.lower()
    intents = [intent for intent, keys in INTENT_KEYWORDS.items() if any(key in prompt for key in keys)]
    source_roles = sorted({role for source in manifest.sources for role in source.fingerprint.candidate_roles})
    evidence = [f"source_role:{role}" for role in source_roles] + [f"prompt_intent:{intent}" for intent in intents]
    workflow_pack = getattr(manifest, "workflow_pack", "default")
    request_type = infer_request_type(source_roles, intents, workflow_pack=workflow_pack)
    confidence = score_confidence(request_type, source_roles, intents)
    alternatives = infer_alternatives(request_type, source_roles, intents, workflow_pack=workflow_pack)
    missing_inputs = []
    if any(intent in intents for intent in ["dashboard", "paygates_summary"]) and not manifest.user_context.project:
        missing_inputs.append("project/squad/sprint/epic metadata for dashboard grouping")
    return IntentClassification(request_type, confidence, source_roles, intents, evidence, alternatives, missing_inputs)


def infer_request_type(source_roles: list[str], intents: list[str], workflow_pack: str = "default") -> str:
    if workflow_pack == "ai-tester":
        return infer_ai_tester_request_type(source_roles, intents)
    return infer_default_request_type(source_roles, intents)


def infer_ai_tester_request_type(source_roles: list[str], intents: list[str]) -> str:
    wants = set(intents)
    if wants & {"review_learning", "review"}:
        return "review_to_memory_update"
    if wants & {"output_generation", "full_ai_tester_delivery", "test_design", "testcase", "manual_testcase", "excel_19_col", "uat", "acceptance_test", "automation_script", "gherkin", "api_test", "dashboard", "status", "paygates_summary", "manual_execution", "execution_result", "coverage_audit", "gap_analysis", "full_delivery"}:
        return "strategy_to_outputs"
    if wants & {"reasoning", "brainstorming", "planning"}:
        return "cooked_knowledge_to_strategy"
    if wants & {"knowledge_cooking", "business_rule_modeling", "coverage_modeling"}:
        return "understanding_to_cooked_knowledge"
    if wants & {"input_understanding", "document_analysis"}:
        return "source_to_understanding"
    if wants & {"knowledge_setup"}:
        return "source_to_knowledge"
    return "strategy_to_outputs"


def infer_default_request_type(source_roles: list[str], intents: list[str]) -> str:
    has = set(source_roles)
    wants = set(intents)
    if wants & {"coverage_audit", "gap_analysis", "review"}:
        return "coverage_audit"
    if has & {"executed_workbook", "manual_execution_result", "google_sheet_execution"}:
        if wants & {"dashboard", "status", "paygates_summary"}:
            return "executed_workbook_to_dashboard"
        return "executed_workbook_to_execution"
    if wants & {"dashboard", "status", "paygates_summary"}:
        return "testcase_to_dashboard"
    if wants & {"automation_script", "gherkin"}:
        if "api_spec" in has:
            return "api_spec_to_automation"
        return "testcase_to_api_automation"
    if wants & {"uat", "acceptance_test"}:
        return "urd_to_uat_testcase"
    if "api_test_design" in has or ("test_design" in has and wants & {"testcase", "manual_testcase", "excel_19_col"}):
        return "api_test_design_to_testcase"
    if "ui_test_design" in has:
        return "ui_test_design_to_testcase"
    if "api_spec" in has:
        if wants & {"test_design", "api_test"} and not wants & {"testcase", "manual_testcase", "excel_19_col"}:
            return "api_spec_to_test_design"
        return "api_spec_to_testcase"
    if has & {"ui_spec", "rsd", "pttk"}:
        if wants & {"test_design"} and not wants & {"testcase", "manual_testcase", "excel_19_col"}:
            return "ui_source_to_test_design"
        return "ui_source_to_testcase"
    if has & {"legacy_testcase", "api_testcase", "testcase"}:
        return "testcase_to_dashboard" if wants & {"dashboard", "status"} else "testcase_to_api_automation"
    return "unknown"


def score_confidence(request_type: str, source_roles: list[str], intents: list[str]) -> float:
    if request_type == "unknown":
        return 0.0
    score = 0.45
    if source_roles:
        score += 0.25
    if intents:
        score += 0.25
    if len(source_roles) > 3:
        score -= 0.1
    return min(max(score, 0.0), 0.95)


def infer_alternatives(request_type: str, source_roles: list[str], intents: list[str], workflow_pack: str = "default") -> list[str]:
    alternatives: list[str] = []
    if workflow_pack == "ai-tester":
        if request_type == "strategy_to_outputs":
            alternatives.extend(["cooked_knowledge_to_strategy", "source_to_understanding"])
        if request_type == "source_to_understanding":
            alternatives.append("source_to_knowledge")
        return alternatives
    if request_type == "api_spec_to_testcase":
        alternatives.extend(["api_spec_to_test_design", "api_spec_to_automation"])
    if request_type == "ui_source_to_testcase":
        alternatives.append("ui_source_to_test_design")
    if request_type == "unknown":
        alternatives.extend(["api_spec_to_testcase", "ui_source_to_testcase", "urd_to_uat_testcase"])
    return alternatives
