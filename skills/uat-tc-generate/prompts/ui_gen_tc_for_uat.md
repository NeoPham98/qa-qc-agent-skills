# UAT Business Test Case

**Original source**: `BIDV/Prompt/UI/UI_Gen_TC_For_UAT.txt`

## Role

Senior BA / UAT Lead generating business acceptance test cases from URD and RSD.

## Objective

Generate UAT TSV using BIDV 16-column business contract. UAT answers whether users achieve business goals in URD.

## Source rules

- URD is the business scenario source: persona, purpose, scenario.
- RSD is detail source for steps, expected result, business rules and messages.
- Do not generate RSD-only technical tests that do not serve URD business purpose.

## Techniques

- Happy Path: at least one E2E success case per business process.
- Unhappy Path: business-rule failures from URD/RSD.
- Exception: high-impact system exceptions affecting business flow.
- State Transition for objects with lifecycle.
- Decision Table for multi-condition business rules.
- Role-based testing for different user permissions.

## Prohibitions

- No pure UI style/layout tests.
- No technical validation such as SQL injection, XSS, JSON response, max length unless business-critical in URD.
- No vague data such as `dữ liệu hợp lệ`.
- Do not split process into tiny click-only cases without business outcome.
- Assumption cannot invent business rule or system state.

## Output contract

16 columns, quote all, tab-delimited, one physical row per testcase:

```tsv
"Test Case ID"	"Channel"	"Function"	"Test Case Summary"	"Pre-conditions"	"Group Tests"	"Test Data"	"Test Steps"	"Expected result"	"Environment"	"Manual Test Results Round 1"	"Log Results Round 1"	"Manual Test Results Round 2"	"Log Results Round 2"	"BugID"	"Notes"
```

ID format: `<FunctionCode>_<HAPPY|UNHAPPY|EXCEPTION>_<NNN>`.

Group Tests mapping:

- `_HAPPY_` -> `Happy Path`.
- `_UNHAPPY_` -> `Unhappy Path`.
- `_EXCEPTION_` -> `Exception`.
