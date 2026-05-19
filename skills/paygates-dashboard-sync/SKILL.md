---
name: paygates-dashboard-sync
description: Safely syncs or exports validated BIDV Paygates dashboard TSV to XLSX without overwriting the historical workbook.
role_affinity: [qa_lead, tester, qc_middle]
domain: [dashboard, status, excel, bidv]
lifecycle_stage: [test_execution, reporting]
produces: [xlsx]
consumes: [dashboard_tsv, workbook]
maturity: draft
tier: 1
languages: [vi, en]
---

# BIDV Paygates Dashboard Sync

## Operating mode

This skill is contract/tool-driven. It does not have a source prompt.

- Source BIDV Prompt: N/A
- Runtime Verbatim Prompt: N/A

Use `paygates-dashboard-generate` before this skill when dashboard Markdown/TSV has not been produced yet.

## Selection criteria

Use this skill when the user asks to:

- create a Paygates dashboard workbook from a validated dashboard TSV;
- sync status counts into an XLSX output artifact;
- preserve the historical `Tổng hợp Trạng Thái Test Case Paygates.xlsx` workbook while writing a separate output copy.

## Required inputs

- Valid Paygates dashboard TSV.
- Explicit output XLSX path.

Optional:

- Source Paygates workbook path for reference/preservation checks.

## Workflow

1. Verify dashboard TSV exists.
2. Validate with `scripts/validate_paygates_dashboard.py`.
3. If source workbook is provided, verify it exists and output path differs.
4. Export/sync XLSX with `scripts/sync_paygates_dashboard_xlsx.py`.
5. Never overwrite the source workbook in place.

## Outputs

- Paygates dashboard XLSX.

## Review gates

- Dashboard TSV validates before XLSX output.
- Counts reconcile with total test cases.
- Output path is explicit.
- Source workbook, when supplied, is preserved.
- Historical workbook is not required for self-contained generation.
