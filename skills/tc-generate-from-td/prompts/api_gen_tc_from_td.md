# API Test Case From Test Design

**Original source**: `BIDV/Prompt/API/API_Gen_TC_From_TD_v2.txt`

## Objective

Convert API Test Design Markdown/Markmap into detailed manual API test cases using BIDV legacy 19-column TSV contract. Output must be detailed enough to support future automation without rewriting.

## Inputs

- Test Design Markdown provides source-derived TD nodes and coverage obligations.
- RSD/PTTK enrich URL, endpoint, headers, JSON body, exact field names, error codes/messages.
- DB document enriches DB connection/table/column verification when available.
- Coverage matrix expansion is required when TD/source facts support it or when the case is tester-standard and explicitly marked as an assumption.

## Prohibitions

- Do not invent endpoint, field name, URL, DB info, error code or message.
- Do not invent business data, token/secret, threshold, allowed values, DB state, or mapping not present in source.
- Expand cases according to the API coverage matrix. If a case is tester-standard rather than source-stated, mark it `[ASSUMPTION: tester-standard gateway/API behavior]`.
- Do not use vague phrases: `như trên`, `tương tự`, `...`, `etc`, `valid data`.
- Max length/list size data must be concrete, not described abstractly.
- Every testcase must include verify step.
- Every testcase must include `Coverage: <CATEGORY>`, `Primary Condition: <atomic condition>`, and `Source: <TD/source/assumption>` in Test Case Summary or Test Datas.
- Negative case must not verify DB.
- Header/protocol group `TD_P1` never verifies DB.
- Write API happy path in `TD_P2`/`TD_P3` verifies DB only when DB/source docs support create/update/delete/persistence verification. POST validate/check/read-only APIs do not verify DB unless the source documents persistence.

## Coverage matrix

API testcase output must cover these categories when applicable to the source/API shape:

- `METHOD`: valid method and unsupported method when method is known or reasonably inferred.
- `CONTENT_TYPE`: valid JSON content type and invalid content type when request body is JSON.
- `AUTH`: missing token and invalid/expired token when auth header/token exists.
- `MANDATORY_HEADERS`: missing important headers such as requestID, app/channel code.
- `LANGUAGE`: vi/en or documented language values.
- `BODY_SCHEMA`: missing required field, empty, wrong type, malformed body when applicable.
- `BOUNDARY`: exact/max/over length or documented format boundary.
- `BUSINESS_ERROR`: one testcase per documented business error code/rule.
- `RESPONSE_SCHEMA`: success schema and failure schema.
- `ERROR_PRIORITY`: multiple simultaneous errors to verify deterministic error priority.

## ID mapping

- Input node: `### TD_P1_001 - [BVA] - Summary`.
- Output ID: `TD_P1_001_TC_001`.
- Counter increments within component group and resets when moving to another group (`TD_P1`, `TD_P2`, `TD_P3`).
- Do not generate `TC-API-*` IDs for testcase sourced from BIDV API TD.
- Do not create testcase rows that do not trace to a `TD_P1_*`, `TD_P2_*`, or `TD_P3_*` node.

## Output contract

Use `data/output-contracts/legacy_19_column_testcase_contract.md`.

Header is exactly:

```tsv
"Test Case ID"	"Function"	"Group Tests"	"Scenario Outline"	"Test Case Summary"	"Pre-conditions"	"Test Datas"	"Test Steps"	"Expected result"	"Environment"	"Priority"	"Regression"	"Automation"	"Manual Test Results Round 1"	"Manual Test Results Round 2"	"Automation Test Results"	"Actual result"	"BugID"	"Notes"
```

Quote all cells. Use `
` for logical newlines inside a cell.

## Required detail rules

- Pre-conditions must include Env, DB, URL, Endpoint, Header, Pre-Data; use `[PENDING_DOC]` if source lacks values.
- Test Datas must include concrete request body/file/body overrides; `[PENDING_DOC]` is allowed only when source lacks the required value.
- Test Steps must include setup URL/header/body, API call with explicit override field, response verification, and optional DB verification.
- Expected result must map 1-1 to verify steps and print expected API response fields/body as specifically as source allows.
