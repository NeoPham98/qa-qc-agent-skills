# Test Generation Matrix Standard

## Purpose

This standard defines the mandatory traceability layer between Test Design and Test Case artifacts.

## Non-skip rule

Any testcase-generation route that expands Test Design into executable cases must produce or consume a Test Generation Matrix or Coverage Matrix first.

Required order:

```text
Test Design -> Test Generation Matrix -> Test Case
```

## Matrix role

The matrix is the bridge between source rule coverage and testcase generation. It must be detailed enough to explain why each testcase exists or why a gap remains unresolved.

## Mandatory coverage dimensions

Expand rows when evidence supports variation across:

- business variant,
- flow or screen,
- API endpoint,
- field or business rule,
- technique,
- concrete value class,
- state,
- role or permission,
- distinct error intent.

## Minimum matrix behavior

- one source rule may map to many matrix rows,
- one TD may map to many testcase rows,
- each covered row should map to a TD ID and Test Case ID,
- uncovered rows must remain visible as `gap`, `open_question`, `pruned`, or `unmapped` with rationale.

## Boundary and decision rules

Boundary rows should name concrete classes such as `min-1`, `min`, `min+1`, `max-1`, `max`, `max+1`, `empty`, `zero`, `invalid_date`, or `invalid_enum` when applicable.

Decision table rows should include only meaningful combinations with distinct outcomes; pruned combinations require rationale.

## Quality rules

- Do not stop at requirement-level rows when field/rule/value expansion is possible.
- Do not hide uncovered rules.
- Do not claim coverage without a TD ID and testcase mapping when the row is marked `covered`.
- If behavior is undocumented, use `open_question` instead of inference.

## Relationship to contract

This standard complements the canonical contract in `data/output-contracts/test_generation_matrix_contract.md` and should be enforced together with it.
