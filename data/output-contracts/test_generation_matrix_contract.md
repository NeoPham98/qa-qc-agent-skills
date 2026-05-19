# Test Generation Matrix Contract

This contract defines the traceability layer used by coverage audit and TD/TC generation routes. It explains how one source rule can expand into many Test Design nodes and testcase rows without creating a native generator outside the workflow pack.

## Runtime dependency rule

- Runtime artifacts must not require or reference a raw sample folder path.
- Bootstrap or migration sources from legacy reference folders must be normalized into workflow pack prompts, contracts, templates, golden examples, or normalized knowledge before runtime.
- `source_ref` must point to a source manifest id, normalized knowledge id, workflow pack contract id, prompt contract id, or current run input section/page/sheet.

## Canonical matrix dimensions

```text
Business/payment variant
× UI flow/screen
× API endpoint
× field/business rule
× testing technique
× concrete test value
```

## Canonical output columns

| Column | Required | Purpose |
|---|---:|---|
| Matrix Row ID | Yes | Stable id for the matrix row, e.g. `MTRX-API-001`. |
| Source Ref | Yes | Runtime source manifest id, normalized artifact id, workflow pack contract id, or current run source section/page/sheet. |
| Source Kind | Yes | `runtime_input`, `normalized_knowledge`, `workflow_pack_contract`, `prompt_contract`, or `golden_example`. |
| Business Variant | No | Payment/product/domain variant when applicable. |
| Flow Or Screen | No | UI flow, screen, tab, state, or API-only flow. |
| API Endpoint | No | Endpoint and method when applicable. |
| Field Or Rule | Yes | Field, schema rule, business rule, error row, state rule, or file-structure rule. |
| Rule Type | Yes | `required`, `type`, `length`, `format`, `enum`, `min`, `max`, `business`, `cross_field`, `state`, `error`, `file_structure`, or `other`. |
| Technique | Yes | `ECP`, `BVA`, `DT`, `ST`, `EG`, `schema`, or `contract`. |
| Value Class | Yes | Concrete partition or boundary class such as `valid`, `missing`, `empty`, `max+1`, `invalid_enum`, `invalid_date`. |
| TD ID | No | Test Design node id generated from or covering this matrix row. |
| Test Case ID | No | Testcase id generated from or covering this matrix row. |
| Coverage Status | Yes | `covered`, `gap`, `open_question`, `pruned`, `duplicate`, or `unmapped`. |
| Rationale | Yes | Why this row exists, was pruned, is a gap, or is unmapped. |

## Expansion rules

- Matrix rows guide and audit prompt-compatible generation; they do not replace prompt behavior.
- One source rule may map to multiple matrix rows when it has multiple techniques or value classes.
- One Test Design node may map to one or many testcase rows.
- Required/schema coverage must follow the active prompt contract; do not add null mandatory cases when the prompt prohibits them.
- Decision Table rows must include only meaningful combinations with distinct expected results or explain pruning in `Rationale`.
- Error Guessing rows must follow the active prompt limits, such as exactly two free-text EG cases when that contract applies.
- Missing business facts must be `open_question`; do not infer them from naming conventions.

## Duplicate detection key

A potential duplicate is identified by the tuple:

```text
Business Variant + Flow Or Screen + API Endpoint + Field Or Rule + Rule Type + Technique + Value Class + expected result intent
```

Duplicates may remain only when `Rationale` explains distinct source refs, roles, states, or execution contexts.

## Required deliverables

Routes that produce TD/TC artifacts should maintain at least a support artifact:

- Markdown matrix: `CoverageMatrix.md` or `TestGenerationMatrix.md`.
- Optional TSV export: `CoverageMatrix.generated.tsv`.
- Validation result from `scripts/validate_test_generation_matrix.py`.

Coverage audit routes should produce the matrix as a final output with a companion gap analysis.

## Dense matrix quality gate

For testcase-generation routes, the matrix must be detailed enough to drive additional senior-QC testcase creation:

- Do not stop at requirement-level rows when field/rule/value/state/role expansion is possible.
- Split each field/rule into concrete value classes and techniques: ECP, BVA, DT, ST, EG, schema, contract, permission, pairwise/cross-field, regression/smoke when applicable.
- Boundary rows should name the exact boundary class such as `min-1`, `min`, `min+1`, `max-1`, `max`, `max+1`, `empty`, `zero`, or `invalid_date`.
- Decision-table rows should represent meaningful combinations with distinct expected outcomes; pruned combinations require a rationale.
- State-transition rows should distinguish allowed, forbidden, repeated, expired, cancelled, approved, rejected, or stale states when applicable.
- Permission rows should distinguish allowed role, denied role, missing scope, expired session/token, and unauthenticated access when source evidence supports it.
- Every covered row should map to a TD ID and Test Case ID; every uncovered row should be `gap` or `open_question` with a concrete owner/rationale in GapAnalysis.
- Reject `1 TD = 1 TC` patterns when a TD covers multiple value classes, boundaries, states, roles, headers, error codes, or business outcomes that can be split into focused testcase rows.
- Matrix rationale must state why the row exists as a QC risk or defect pattern, not only repeat the field/rule name.
- Covered rows must be specific enough for a tester to derive exact mutation/input and expected observable outcome without guessing undocumented facts.
