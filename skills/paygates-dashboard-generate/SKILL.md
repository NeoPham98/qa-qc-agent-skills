---
name: paygates-dashboard-generate
description: Generates BIDV Paygates-style dashboard/status artifacts from testcase and execution metadata without requiring an external workbook template.
role_affinity: [qa_lead, tester, qc_middle]
domain: [dashboard, status, testing, bidv]
lifecycle_stage: [test_execution, reporting]
produces: [md, tsv, xlsx, dashboard]
consumes: [testcase, test_execution, test_set, metadata]
maturity: draft
tier: 1
languages: [vi, en]
---

# BIDV Paygates Dashboard Generate

## Operating mode

This skill is invoked inside Prompt-Compatible Orchestration Mode, but it is contract/tool-driven because BIDV did not have a source prompt for Paygates dashboard generation.

The historical Paygates workbook is a digitized baseline, not a runtime dependency. Use `../../data/output-contracts/paygates_dashboard_contract.md` as the canonical behavior.

## Selection criteria

Use this skill when the user asks to:

- generate a Paygates-style summary/status dashboard;
- summarize testcase execution by Project/Squad/Sprint/Epic;
- create a dashboard when no `Tổng hợp Trạng Thái Test Case Paygates.xlsx` workbook exists;
- export dashboard status to Markdown, TSV, or XLSX.

## Required inputs

Minimum:

- testcase artifact path: Markdown or TSV.
- Project/Product, Squad, Sprint, Epic/Function metadata or explicit pending markers.

Optional:

- TestExecution Markdown/TSV.
- TestSet Markdown.
- detail artifact link/path.
- testcase generate type.
- automation test status.

## Workflow

1. Receive route from orchestrator with testcase/execution sources and metadata.
2. Load `paygates_dashboard_contract.md`.
3. Normalize testcase IDs and execution statuses.
4. Aggregate counts: Passed, Failed, Untested, Accepted, N/A, Total.
5. Derive `Current test status` using the contract.
6. Generate `PaygatesDashboard.md` using `templates/PaygatesDashboard.md`.
7. Export TSV with `scripts/export_paygates_dashboard_tsv.py` when requested.
8. Export XLSX with `scripts/export_paygates_dashboard_xlsx.py` when requested.
9. Validate with `scripts/validate_paygates_dashboard.py` before handoff.
10. Report open questions for missing metadata instead of inventing values.

## Outputs

- `PaygatesDashboard.md`.
- `PaygatesDashboard.generated.tsv`.
- Optional `PaygatesDashboard.generated.xlsx`.
- Validation report or command output.

## Review gates

- Dashboard columns match `paygates_dashboard_contract.md`.
- Total count reconciles with status counts.
- Source testcase/execution artifact paths are recorded.
- Missing squad/sprint/epic/function values are explicit `[PENDING_DOC:<field>]` markers.
- External workbook is not required for generation.
- Historical workbook content is not treated as business source beyond this digitized contract.
