---
name: api-td-generate
description: Generates API Test Design only through BIDV prompt-compatible API TD fragments.
role_affinity: [qc_middle, tester, qa_lead]
domain: [api, testing, bidv]
lifecycle_stage: [test_design]
produces: [md, api_test_design]
consumes: [api_spec, prompt_fragment, source_docs]
maturity: draft
tier: 1
languages: [vi, en]
---

# BIDV API Test Design Generate

## Operating mode

This skill is invoked only inside **Prompt-Compatible Orchestration Mode**. Native/freeform API TD generation outside selected BIDV runtime verbatim prompts is unsupported.

## Selection criteria

Use this skill when the requested artifact is API Test Design.

## Prompt compatibility

Owned BIDV source/runtime prompt mapping:

- `BIDV/Prompt/API/API_TD_1_Setup_Context.txt` -> `prompts-verbatim/API/API_TD_1_Setup_Context.txt`
- `BIDV/Prompt/API/API_TD_2_Method_Header.txt` -> `prompts-verbatim/API/API_TD_2_Method_Header.txt`
- `BIDV/Prompt/API/API_TD_3_Schema_Validation.txt` -> `prompts-verbatim/API/API_TD_3_Schema_Validation.txt`
- `BIDV/Prompt/API/API_TD_4_Value_Business_Cross_Logic.txt` -> `prompts-verbatim/API/API_TD_4_Value_Business_Cross_Logic.txt`

Runtime execution must load the `Runtime Verbatim Prompt` from `../../data/source-inventory/prompt_fragment_registry.md`. Files under `prompts/*.md` are non-runtime notes unless verified as content-equivalent to the source prompt.

## Required inputs

- Project/Squad/Epic.
- API spec/source docs.
- API scope, endpoint/method/header/auth/schema/business rules as required by the selected fragment.
- Source BIDV prompt path.
- Runtime verbatim prompt path.
- Prompt mirror verification result.
- Expected output path.

## Workflow

1. Receive exactly one selected API TD runtime verbatim prompt from orchestrator, or an ordered runtime prompt bundle for full API TD.
2. Verify prompt mirror fidelity before generation.
3. For setup/context, load source docs and identify API scope only; do not generate TD nodes.
3. For Method/Header, generate only `TD_P1_*` Markmap nodes under `## Method & Header`.
4. For Schema Validation, generate only `TD_P2_*` Markmap nodes under `## Schema Validation`.
5. For Value/Business/Cross Logic, generate only `TD_P3_*` Markmap nodes under `## Value, Business Logic, Cross Logic`.
6. Verify mandatory prompt inputs are present or explicitly missing.
7. Normalize to BIDV Markmap Markdown using `../../data/output-contracts/markdown_normalization_rules.md`.
8. Record open questions for missing endpoint/schema/error/business details.
9. Add `## Coverage Obligations` with API coverage categories, source/assumption/open-question classification, and meaningful placeholders for missing data.
10. Send output to review.

## API Spec Extraction and Operation Cards

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

## Coverage Obligations

Full API Test Design output must include a `## Coverage Obligations` section before the TD node sections. It must list these categories and classify each as `Source-derived`, `Assumption-derived tester-standard`, or `Open question / requires BIDV confirmation`:

- `METHOD`
- `CONTENT_TYPE`
- `AUTH`
- `MANDATORY_HEADERS`
- `LANGUAGE`
- `BODY_SCHEMA`
- `BOUNDARY`
- `BUSINESS_ERROR`
- `RESPONSE_SCHEMA`
- `ERROR_PRIORITY`

If source lacks concrete values, use meaningful placeholders such as `<VALID_CUSTOMER>`, `<CIF_INVALID_AGE>`, `<USER_WITHOUT_PERMISSION>`, or `<FILE_MISSING_REQUIRED_COLUMN>`. Do not invent real customer data, credentials, thresholds, allowed values, mappings, or undocumented business rules.


Full API TD output must use this shape, not a summary table:

```markdown
# <Method> <Endpoint> - <Tên API Tiếng Việt>

## Coverage Obligations
- METHOD: <Source-derived | Assumption-derived tester-standard | Open question / requires BIDV confirmation> - <basis>
- CONTENT_TYPE: <Source-derived | Assumption-derived tester-standard | Open question / requires BIDV confirmation> - <basis>
- AUTH: <Source-derived | Assumption-derived tester-standard | Open question / requires BIDV confirmation> - <basis>
- MANDATORY_HEADERS: <Source-derived | Assumption-derived tester-standard | Open question / requires BIDV confirmation> - <basis>
- LANGUAGE: <Source-derived | Assumption-derived tester-standard | Open question / requires BIDV confirmation> - <basis>
- BODY_SCHEMA: <Source-derived | Assumption-derived tester-standard | Open question / requires BIDV confirmation> - <basis>
- BOUNDARY: <Source-derived | Assumption-derived tester-standard | Open question / requires BIDV confirmation> - <basis>
- BUSINESS_ERROR: <Source-derived | Assumption-derived tester-standard | Open question / requires BIDV confirmation> - <basis>
- RESPONSE_SCHEMA: <Source-derived | Assumption-derived tester-standard | Open question / requires BIDV confirmation> - <basis>
- ERROR_PRIORITY: <Source-derived | Assumption-derived tester-standard | Open question / requires BIDV confirmation> - <basis>

## Method & Header
### TD_P1_001 - [ST] - <condition summary>
- **Steps**: <high-level action>
- **Expected**: <high-level expected result>

## Schema Validation
### TD_P2_001 - [ST] - <condition summary>
- **Steps**: <high-level action>
- **Expected**: <high-level expected result>

## Value, Business Logic, Cross Logic
### TD_P3_001 - [ST] - <condition summary>
- **Steps**: <high-level action>
- **Expected**: <high-level expected result>
```

Rules:

- `TD_P1` is reserved for Method/Header only.
- `TD_P2` is reserved for Schema Validation only.
- `TD_P3` is reserved for Value/Business/Cross Logic only.
- Do not create a separate `Error Handling` section; place errors in the owning prompt phase.
- Do not output `| Test Condition ID | ... |` tables for API TD prompt output.
- Missing source facts must be written as `[ASSUMPTION: ...]` only when allowed by the BIDV prompt and mirrored in Open Questions.

## Outputs

- API Test Design Markmap Markdown with `TD_P1`, `TD_P2`, and `TD_P3` nodes.
- Open questions when prompt-required data is missing.

## Review gates

- Correct API TD fragment selected.
- Output is BIDV Markmap, not a table.
- Full API TD contains `TD_P1`, `TD_P2`, and `TD_P3` phase IDs when all phases are requested.
- Full API TD contains `## Coverage Obligations` with the API coverage categories and source/assumption/open-question classification.
- Source references preserved.
- Missing values are open questions, not invented facts.
