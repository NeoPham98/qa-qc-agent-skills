# Paygates Dashboard Contract

This contract digitizes the Paygates status workbook behavior so agents can generate and maintain dashboard/status outputs without an external Excel template.

## Canonical output columns

| Column | Required | Purpose |
|---|---:|---|
| Project / Product Scope | Yes | Project, product, or delivery scope |
| Squad | Yes | Owning squad/team |
| Sprint | Yes | Sprint/release grouping |
| Epic / Function | Yes | Epic, feature, function, or API group |
| Requirement ID | No | Requirement trace when available |
| Test Condition ID | No | Test design/test condition trace when available |
| Test Set ID | No | Test set trace when available |
| Detail Artifact Link | Yes | Path/link to testcase detail artifact |
| Passed | Yes | Count of passed testcases |
| Failed | Yes | Count of failed testcases |
| Untested | Yes | Count of not-run/pending/empty-result testcases |
| Accepted | Yes | Count of accepted testcases |
| N/A | Yes | Count of not-applicable testcases |
| Total Test cases | Yes | Total testcase count |
| Current test status | Yes | Aggregated execution status |
| Test case generate type | No | Manual / AI gen / Mixed / [PENDING_DOC:test_case_generate_type] |
| Automation test status | No | Not Started / In Progress / Completed / N/A / [PENDING_DOC:automation_status] |
| Open Questions | No | Missing metadata, source gaps, or unresolved assumptions |

## Status normalization

| Input value | Normalized value |
|---|---|
| `PASS`, `Pass`, `Passed`, `pass` | `Passed` |
| `FAIL`, `FAILED`, `Fail`, `Failed`, `failed` | `Failed` |
| empty, `Not Run`, `Pending`, `PENDING`, `Untested` | `Untested` |
| `Accepted`, `ACCEPTED` | `Accepted` |
| `N/A`, `NA`, `Not Applicable` | `N/A` |

Unsupported status values must be reported as validation errors unless they are preserved in `Open Questions` and mapped explicitly by a future contract revision.

## Aggregation rules

- If execution/status artifact is absent, every testcase is counted as `Untested`.
- If execution/status artifact exists, aggregate the latest status available per `Test Case ID`.
- `Total Test cases = Passed + Failed + Untested + Accepted + N/A`.
- Current status rules:
  - `Failed` if `Failed > 0`.
  - `Untested` if all cases are untested.
  - `Completed` if `Untested = 0` and `Failed = 0`.
  - `In-Test` for all other mixed states.
  - `N/A` if all cases are `N/A`.
- Missing Project/Squad/Sprint/Epic/Detail Artifact Link must be written as `[PENDING_DOC:<field>]` and repeated in `Open Questions`.
- Do not infer automation readiness from manual execution. Use `[PENDING_DOC:automation_status]` when not provided.

## Source hierarchy

1. User-provided metadata and generated testcase/execution artifacts.
2. Internal Markdown/TSV contracts in `data/output-contracts/`.
3. Historical workbook samples only as optional parity references.

## Required deliverables

A Paygates dashboard route should produce at least:

- Markdown source-of-truth: `PaygatesDashboard.md`.
- TSV export: `PaygatesDashboard.generated.tsv`.
- Optional XLSX export: `PaygatesDashboard.generated.xlsx`.
- Validation result from `scripts/validate_paygates_dashboard.py`.
