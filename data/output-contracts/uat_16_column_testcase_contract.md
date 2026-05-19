# UAT 16-Column Testcase Contract

This contract is used when the selected prompt workflow is UAT testcase generation.

## Purpose

UAT testcase output is business-facing and should be readable by business users. It must follow the selected UAT prompt rules and avoid unnecessary technical validation unless the source business flow requires it.

## Columns

| # | Column | Requirement |
|---:|---|---|
| 1 | Test Case ID | Required stable ID |
| 2 | Business Process | Required |
| 3 | Function | Required |
| 4 | Scenario Outline | Required |
| 5 | Test Case Summary | Required business-readable summary |
| 6 | Pre-conditions | Required business setup |
| 7 | Test Data | Required concrete business data when source provides it |
| 8 | Test Steps | Required user/business steps |
| 9 | Expected Result | Required business expected result |
| 10 | Environment | Required when known |
| 11 | Priority | Required when known |
| 12 | Regression | Yes/No or blank if not applicable |
| 13 | UAT Round 1 Result | Blank before execution or valid status after execution |
| 14 | UAT Round 2 Result | Blank before execution or valid status after execution |
| 15 | Actual Result | Blank before execution or observed result after execution |
| 16 | Notes | Optional |

## Rules

- Output must follow the selected UAT prompt fragment.
- Use business language rather than internal implementation detail unless source requires it.
- Do not invent business rules, UI behavior, data, or acceptance criteria.
- Missing source values must be explicit open questions.
- TSV export should preserve 16 columns exactly.

## Dense UAT coverage rules

- UAT testcase generation should be driven by a business-facing Coverage Matrix when the route produces testcase artifacts.
- Expand by actor/persona, business process, rule, state transition, permission, data class, and expected business outcome.
- Apply ECP for valid/invalid/missing business data groups, BVA for amount/date/limit/range, Decision Table for combined business rules, and State Transition for application/transaction lifecycle.
- Keep UAT business-readable: do not over-split into CSS/DOM/API internals, but do split separate actor, transition, rule, exception, and outcome.
- Pre-conditions must specify actor/role, business data, current record/transaction status, configuration, and dependency when source provides it.
- Test Steps must be executable business actions. Expected Result must state message/status/business outcome and downstream notification/state when source provides it.
- Missing business facts must be explicit open questions or `[PENDING_DOC:<fact>]`.