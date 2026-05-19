---
name: tc-generate-from-td
description: Generates BIDV API/UI testcase artifacts from Test Design using selected BIDV runtime verbatim prompts.
role_affinity: [qc_middle, tester]
domain: [testcase, api, ui, bidv]
lifecycle_stage: [testcase_authoring]
produces: [md, testcase, tsv]
consumes: [test_design, runtime_verbatim_prompt, source_docs]
maturity: draft
tier: 1
languages: [vi, en]
---

# BIDV Testcase Generate From Test Design

## Operating mode

This skill is invoked only inside **Prompt-Compatible Orchestration Mode**. Native/freeform testcase generation outside selected BIDV testcase prompt rules is unsupported.

## Selection criteria

Use this skill when generating API or UI manual testcase from a Test Design artifact.

## Prompt compatibility

Owned BIDV source/runtime prompt mapping:

- API testcase: `BIDV/Prompt/API/API_Gen_TC_From_TD_v2.txt` -> `prompts-verbatim/API/API_Gen_TC_From_TD_v2.txt`
- UI testcase: `BIDV/Prompt/UI/UI_Gen_TC_From_TD.txt` -> `prompts-verbatim/UI/UI_Gen_TC_From_TD.txt`

Runtime execution must load the `Runtime Verbatim Prompt` from `../../data/source-inventory/prompt_fragment_registry.md`. Files under `prompts/*.md` are non-runtime notes unless verified as content-equivalent to the source prompt.

## Required inputs

- Project/Squad/Epic.
- Source Test Design.
- API spec or UI/RSD/PTTK docs required by the selected prompt.
- Source BIDV prompt path.
- Runtime verbatim prompt path.
- Prompt mirror verification result.
- Target output contract, normally legacy BIDV 19-column TSV.

## Workflow

1. Receive selected API/UI runtime verbatim testcase prompt from orchestrator.
2. Verify prompt mirror fidelity before generation.
3. Verify all prompt-required inputs are present or explicitly missing.
4. Generate testcase rows according to selected BIDV prompt rules.
5. For API TD input, derive source-based testcase rows from a `TD_P1_*`, `TD_P2_*`, or `TD_P3_*` Markmap node and preserve `TD_Px_NNN_TC_NNN` IDs.
6. Expand coverage with tester-standard cases when required by the coverage matrix; mark inferred cases with the correct assumption marker and keep source trace.
7. Normalize testcase source to Markdown.
8. Export legacy BIDV 19-column TSV when required.
9. Send Markdown and TSV to review.

## Coverage matrix contract

Each testcase row must include these markers in `Test Case Summary`, `Test Datas`, or `Notes`:

- `Coverage: <CATEGORY>`
- `Primary Condition: <one atomic test condition>`
- `Source: <TD node / source section / assumption basis>`

Use `[ASSUMPTION: tester-standard gateway/API behavior]` for API cases, `[ASSUMPTION: tester-standard UI/business validation behavior]` for UI/business cases, and `[ASSUMPTION: tester-standard data/file processing behavior]` for data/file/report cases that are tester-standard rather than explicitly documented.

API coverage categories: `METHOD`, `CONTENT_TYPE`, `AUTH`, `MANDATORY_HEADERS`, `LANGUAGE`, `BODY_SCHEMA`, `BOUNDARY`, `BUSINESS_ERROR`, `RESPONSE_SCHEMA`, `ERROR_PRIORITY`.

UI/business coverage categories: `NAVIGATION`, `FIELD_VALIDATION`, `REQUIRED_FIELDS`, `FORMAT_VALIDATION`, `BOUNDARY`, `BUSINESS_RULE`, `ROLE_PERMISSION`, `STATE_TRANSITION`, `ERROR_MESSAGE`, `DATA_PERSISTENCE`, `CANCEL_BACK_REFRESH`.

UAT/E2E coverage categories: `HAPPY_PATH`, `ALTERNATE_PATH`, `NEGATIVE_BUSINESS_RULE`, `ROLE_OR_ACTOR`, `PRECONDITION`, `POSTCONDITION`, `APPROVAL_FLOW`, `INTEGRATION_POINT`, `DATA_CONSISTENCY`, `EXCEPTION_FLOW`.

Data/file/report cases must use the corresponding validator profile categories when those routes are enabled. Never use assumption markers to invent customer data, token/secret, thresholds, mappings, backend states, or undocumented business rules.


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

Do not collapse several required fields or several business errors into one vague testcase. Do not use placeholders such as “valid data”, “invalid data”, “correct response”, “appropriate error”, “như trên”, or “tương tự” when concrete values are available.

## Standard & Language Compliance:
- Default Language: Vietnamese (`Tiếng Việt`) is the default language for all manual testcase steps, preconditions, data, and expected results.
- Verification Verbs: Every testcase must use verification action verbs (e.g. `kiểm tra` or `verify` / `assert`) in either the `Test Steps` or `Expected result` column.
- Exact HTTP Status Format: Expected results must state the expected HTTP status matching the regex (e.g. `HTTP Status: 200` or `HTTP 200` or `Status: 400`). Avoid writing `HTTP Status Code: 200`.
- Primary Condition Marker: Every testcase row must explicitly contain a `Primary Condition: <condition>` marker in the `Test Case Summary` column.
- Negative Condition Specificity: For negative testcases, the `Primary Condition` must specify the exact target name (e.g. `requestCif`, `authToken`) and include keywords like `field`, `rule`, `method`, `header`, `body`, or `param`.
- Coverage Category Marker: Every row must include `Coverage: <CATEGORY>` in the `Notes` column matching the exact required categories (e.g. `METHOD`, `CONTENT_TYPE`, `AUTH`, `MANDATORY_HEADERS`, `LANGUAGE`, `BODY_SCHEMA`, `BOUNDARY`, `BUSINESS_ERROR`, `RESPONSE_SCHEMA`, `ERROR_PRIORITY`).
- Newline Word Boundary Rule: Since newline `\n` in markdown tables is escaped to `\n` literal in TSVs, always put spaces around `\n` when writing keywords (e.g. `\n response` instead of `\nresponse`) to prevent merging into `nresponse` and failing word boundary checks.
- Forbidden Phrases: Vague phrases such as `valid data`, `invalid data`, `data hợp lệ`, `data không hợp lệ`, `correct response`, `appropriate error`, `như trên`, `tương tự` are strictly banned.


## Outputs

- `TestCaseSource.md` or equivalent Markdown source.
- Legacy BIDV 19-column TSV when selected route requires it.

## Review gates

- Correct API/UI testcase runtime verbatim prompt selected.
- API testcase source is derived from BIDV Markmap TD nodes.
- API testcase IDs follow `TD_Px_NNN_TC_NNN`; `TC-API-*` is not valid for API TD-derived output.
- Test Design coverage preserved and expanded according to the applicable coverage matrix.
- Assumption-derived tester-standard cases are explicitly marked and do not invent business facts.
- 19-column contract satisfied.
- No invented API/UI/data/error/DB details outside source docs.

## Related references

- `../../data/output-contracts/legacy_19_column_testcase_contract.md`
- `../../data/output-contracts/markdown_normalization_rules.md`
- `prompts/api_gen_tc_from_td.md` (non-runtime note/wrapper)
- `prompts/ui_gen_tc_from_td.md` (non-runtime note/wrapper)
