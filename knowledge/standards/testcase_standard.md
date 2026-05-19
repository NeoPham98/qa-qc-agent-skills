# Testcase Standard

## Purpose

This standard defines the minimum quality and traceability requirements for generated or curated testcases.

## Non-skip rule

Testcases must be created from approved upstream artifacts.

Required order:

```text
Source Inventory -> Source Analysis -> Test Plan -> Test Design -> Test Generation Matrix -> Test Case
```

## Primary testcase rule

One testcase must have one primary condition and one primary expected outcome.

A testcase may include setup and verification detail, but it must not merge multiple unrelated negative paths into one row.

## Required testcase quality

Every testcase must be:

- traceable,
- executable,
- measurable,
- atomic enough for execution reporting,
- aligned with upstream source logic.

## Mandatory content expectations

- Preconditions must be concrete when needed.
- Test Data must identify values or value classes clearly.
- Steps must describe action, input, and verification flow in executable order.
- Expected Result must be specific enough to determine pass/fail.
- If the expected behavior is undocumented, use `[PENDING_DOC:<fact>]`, `gap`, or `open_question` instead of guessing.

## Coverage obligations

When evidence supports them, testcase sets must cover:

- happy path,
- exception paths,
- negative validation,
- required / missing / empty / null where contract allows,
- type / format / enum rules,
- boundaries,
- business rules,
- cross-field logic,
- state or time behavior,
- role / permission or session behavior,
- response or error envelope behavior.

## Technique expectations

Use applicable techniques such as:

- ECP,
- BVA,
- Decision Table,
- State Transition,
- Error Guessing,
- Pairwise / Cross-field,
- Permission / Role,
- Regression / Smoke.

## Traceability

Each testcase row should be traceable back to:

- Project / Squad / Epic,
- TD ID,
- matrix row or source rule,
- source ref where applicable.

## Forbidden behavior

- Do not generate testcase rows directly from raw prompts without upstream artifacts.
- Do not write vague steps like "perform validation" without naming the target.
- Do not write vague expected results like "system works correctly".
- Do not change documented business logic.
- Do not approve generator-owned output in the same role.

## Standard & Language Compliance
- **Default Language**: Vietnamese (`Tiếng Việt`) must be used for all test case steps, preconditions, data, and expected results.
- **Verification Verbs**: Every test case must use verification action verbs (e.g. `kiểm tra` or `verify` / `assert`) in the `Test Steps` or `Expected result` column.
- **Exact HTTP Status Format**: Expected results must state the expected HTTP status matching the regex (e.g. `HTTP Status: 200` or `HTTP 200` or `Status: 400`). Avoid writing `HTTP Status Code: 200`.
- **Primary Condition Marker**: Every testcase row must explicitly contain a `Primary Condition: <condition>` marker in the `Test Case Summary` column.
- **Negative Condition Specificity**: For negative testcases, the `Primary Condition` must specify the exact target name (e.g. `requestCif`, `authToken`) and include keywords like `field`, `rule`, `method`, `header`, `body`, or `param`.
- **Coverage Category Marker**: Every row must include `Coverage: <CATEGORY>` in the `Notes` column matching the exact required categories (e.g. `METHOD`, `CONTENT_TYPE`, `AUTH`, `MANDATORY_HEADERS`, `LANGUAGE`, `BODY_SCHEMA`, `BOUNDARY`, `BUSINESS_ERROR`, `RESPONSE_SCHEMA`, `ERROR_PRIORITY`).
- **Newline Word Boundary Rule**: Since newline `\n` in markdown tables is escaped to `\n` literal in TSVs, always put spaces around `\n` when writing keywords (e.g. `\n response` instead of `\nresponse`) to prevent merging into `nresponse` and failing word boundary checks.
- **Forbidden Phrases**: Vague phrases such as `valid data`, `invalid data`, `data hợp lệ`, `data không hợp lệ`, `correct response`, `appropriate error`, `như trên`, `tương tự` are strictly banned.

