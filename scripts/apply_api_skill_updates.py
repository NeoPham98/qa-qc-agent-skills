from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def insert_before(path: str, marker: str, block: str, guard: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if guard in text:
        return
    idx = text.index(marker)
    p.write_text(text[:idx] + block.rstrip() + "\n\n" + text[idx:], encoding="utf-8")


api_td_block = """## API Spec Extraction and Operation Cards

Before generating any `TD_P1/TD_P2/TD_P3` nodes for an API spec-driven request, build or consume an **API Requirement Inventory / Operation Cards** artifact. This artifact is the evidence source for TD generation and must include, per endpoint:

- source document/page/section reference
- HTTP method and endpoint path
- auth/header requirements
- path/query/request body fields
- required/optional fields
- type, format, length, enum, nullable, and range constraints when source provides them
- common response envelope and endpoint-specific `data` schema
- documented error codes/messages
- business rules, state rules, cross-field rules, and downstream dependencies
- DB/source-of-truth verification availability
- enrichment references used, for example `BIDV/api_automation/nms_sdk/endpoints.py` or `schemas.py`
- confidence/gap status and open questions

Do not generate TD nodes from endpoint names alone. If a source or approved enrichment artifact contains required fields, schema fields, business errors, or response validators, those facts must be reflected in TD nodes instead of being replaced by generic `[PENDING_DOC]` placeholders.

## API TD specificity rules

- `TD_P1` nodes must name the exact method/path/header/auth target under test.
- `TD_P2` nodes must name the exact request/response field, schema rule, type, format, enum, null/empty, or boundary target when known.
- `TD_P3` nodes must name the exact business rule, state transition, flow dependency, or error code/message when known.
- Generic nodes such as “kiểm tra dữ liệu không hợp lệ”, “verify API works”, “validate invalid input”, or “check response is correct” are not acceptable when source facts exist.
- Missing facts remain open questions; do not invent rules, but do not mark known facts as pending.
"""
insert_before("skills/api-td-generate/SKILL.md", "## API TD output contract", api_td_block, "## API Spec Extraction and Operation Cards")


tc_block = """## API testcase specificity contract

For API TD-derived output, every testcase row must preserve executable API detail from the TD node and operation card:

- test summary or steps include the HTTP method and endpoint path
- preconditions include environment, authentication/header setup, and seeded data when needed
- test data contains concrete JSON/body/query/path/header values, or a justified no-body/no-param explanation
- steps include the actual request operation and exact field/header/parameter variation under test
- expected result includes expected HTTP status and response envelope assertion
- negative expected result includes the exact error code/message when source provides it
- source traceability includes TD ID plus PDF page/section or enrichment symbol

Minimum expectations per endpoint, when source facts exist:

- one valid minimum request case
- one auth/header negative case
- missing required field cases, or a justified representative subset for very large schemas
- invalid type/format/null/empty/boundary/enum cases for constrained fields
- response schema assertion cases
- documented business error/state-rule cases

Do not collapse several required fields or several business errors into one vague testcase. Do not use placeholders such as “valid data”, “invalid data”, “correct response”, “appropriate error”, “như trên”, or “tương tự” when concrete values are available. For BIDV manual testcase output, write `Test Steps` and `Expected result` in Vietnamese unless the user explicitly requests another language.
"""
insert_before("skills/tc-generate-from-td/SKILL.md", "## Outputs", tc_block, "## API testcase specificity contract")


api_agent_block = """## API spec extraction responsibilities

Before producing TD nodes, parse API source docs into an endpoint inventory and operation cards. Cross-check approved enrichment inputs when supplied, especially SDK endpoint/schema references such as `BIDV/api_automation/nms_sdk/endpoints.py` and `schemas.py`.

Self-review before handoff:

- every TD node includes method/path and source reference
- every negative TD identifies the exact field, header, parameter, business rule, or error code
- every schema TD cites request/response fields when known
- every business TD cites rule/error/state evidence or records an open question
- known required fields/error codes/schema facts are not left as generic `[PENDING_DOC]`
"""
insert_before("agents/api-test-design-agent/AGENT.md", "## Inputs", api_agent_block, "## API spec extraction responsibilities")


tc_agent_block = """## API testcase specificity responsibilities

For API TD-derived testcase work:

- Preserve method, endpoint path, field/header/rule target, test data, and expected assertion from TD/operation cards.
- Convert each distinct field validation or documented business error into a concrete testcase row unless the source explicitly justifies grouping.
- Keep `Test Steps` and `Expected result` in Vietnamese for BIDV manual outputs unless requested otherwise.
- Keep TSV newline escaping compatible with the legacy one-line-per-testcase contract; formatted XLSX exports should render those escaped newlines as real line breaks.
- Run structural validation and API specificity validation before reporting a testcase artifact as ready.
"""
insert_before("agents/testcase-generator/AGENT.md", "## Inputs", tc_agent_block, "## API testcase specificity responsibilities")


orch_block = """## API spec-driven quality gate

For API spec -> TD/testcase flows, the orchestrator must require an API Requirement Inventory / Endpoint Catalog / Operation Cards checkpoint before TD generation. The checkpoint should be enriched with approved references when supplied, such as `BIDV/api_automation/nms_sdk/endpoints.py` and `BIDV/api_automation/nms_sdk/schemas.py`.

Required API flow:

1. Verify prompt mirrors.
2. Extract endpoint inventory and operation cards from source docs.
3. Enrich with approved SDK/source references without silently replacing PDF evidence.
4. Generate `TD_P1`, `TD_P2`, and `TD_P3` from extracted facts.
5. Run API TD specificity validation before testcase generation.
6. Generate testcase rows from detailed TD nodes only.
7. Run legacy TSV validation plus API testcase specificity validation.
8. Export formatted XLSX when requested or when producing final manual testcase handoff.

If source/enrichment contains required fields, schema fields, or business error codes, output must not keep generic placeholders for those facts. Missing facts become open questions; known facts become concrete TD/TC coverage.
"""
insert_before("agents/delivery-orchestrator/AGENT.md", "## Team-compatible orchestration", orch_block, "## API spec-driven quality gate")


verify_block = r"""## API specificity hard-fail conditions

For API TD/testcase deliverables, structural validation is not enough. Any item below must fail output review:

- API testcase rows pass the legacy 19-column contract but lack concrete method/path/request execution details.
- `Test Datas` remains generic or placeholder-only while source/enrichment provides fields.
- `Expected result` lacks HTTP status or response/error assertion.
- Negative tests do not identify the exact field, header, parameter, rule, or error code under test.
- Required fields from operation cards are not covered by missing-field tests or a documented representative-set rationale.
- Documented business error codes are not covered or explicitly marked out of scope.
- Known source facts are replaced by `[PENDING_DOC]` without an open-question reason.
- Formatted XLSX output shows escaped `\n` instead of real line breaks in manual-step cells.
"""
insert_before("skills/output-verify/SKILL.md", "## Review gates", verify_block, "## API specificity hard-fail conditions")


# Workflow map updates
p = ROOT / "data/source-inventory/workflow_map.md"
text = p.read_text(encoding="utf-8")
if "| API spec extraction / operation inventory |" not in text:
    row = "| API spec extraction / operation inventory | User requests API TD/testcase from API spec or source docs | API PDF/source docs, optional SDK enrichment references | Internal extraction contract before API TD prompts | `api-td-generate` / `delivery-orchestrator` | API Requirement Inventory / Operation Cards | Source fidelity and API specificity baseline |\n"
    text = text.replace("|---|---|---|---|---|---|---|\n", "|---|---|---|---|---|---|---|\n" + row, 1)
    text = text.replace("## Orchestrator rule\n", "## API enrichment sources\n\nFor NMS API work, approved enrichment references may include `BIDV/api_automation/nms_sdk/endpoints.py` and `BIDV/api_automation/nms_sdk/schemas.py`. These references can fill known required fields, business errors, and schema assertions when traceable, but they must not silently override contradictory PDF evidence.\n\n## Orchestrator rule\n")
    p.write_text(text, encoding="utf-8")


# Registry updates
p = ROOT / "data/source-inventory/prompt_fragment_registry.md"
text = p.read_text(encoding="utf-8")
replacements = {
    "Project/Squad/Epic, API spec, API scope, source references": "Project/Squad/Epic, API spec, API scope, source references, endpoint inventory, operation cards, open questions",
    "API TD context, method, endpoint, headers/auth details": "API TD context, operation cards, method, endpoint, headers/auth details, header error expectations",
    "Request schema, field constraints, validation rules": "Operation cards, request schema, response schema, field constraints, validation rules, concrete field targets",
    "Business rules, value ranges, state rules, dependencies": "Operation cards, business rules, error codes/messages, value ranges, state rules, dependencies",
    "API Test Design, API spec, data rules, endpoint/header/error details": "API Test Design, operation cards, API spec, data rules, endpoint/header/schema/error/business details",
    "Prompt mirror fidelity, 19-column contract, TD coverage, source fidelity": "Prompt mirror fidelity, 19-column contract, TD coverage, source fidelity, API specificity validation, anti-genericity checks",
}
for old, new in replacements.items():
    text = text.replace(old, new)
p.write_text(text, encoding="utf-8")

print("contract updates complete")
