# UI Manual Test Case From Test Design

**Original source**: `BIDV/Prompt/UI/UI_Gen_TC_From_TD.txt`

## Objective

Convert UI Test Design Markdown into detailed manual UI test cases using BIDV legacy 19-column TSV contract.

## Inputs

- Test Design Markdown is the coverage source of truth.
- RSD/PTTK-UI enrich concrete field names, screen names, button labels, API calls, messages, DB behavior when documented.
- Error list enriches exact codes/messages.

## Mapping rules

- One `###` Test Condition can generate one or more testcases when concrete data coverage requires it.
- Function comes from nearest `##` header.
- Group Tests maps technique: ECP, BVA, Decision Table, State Transition, Error Guessing.
- Scenario Outline is the core phrase from Test Condition Summary.
- Assumption only goes in Test Case Summary.

## Output contract

Use `data/output-contracts/legacy_19_column_testcase_contract.md`.

Rules:

- One testcase per physical TSV line.
- 19 columns, quote all cells, delimiter tab, use `
` inside cells.
- Result columns and Notes blank initially.

## Required detail rules

- Test Data must be concrete: values, dates, role, field values; never `data hợp lệ`.
- Test Steps must be numbered `1.`, `2.`, `3.` and include exact screen/field/button labels when source provides them.
- Expected result must map to verify steps and describe visible UI result, message, API result, or DB state only if documented.
- Do not test UI layout/color/responsive unless documented.
