---
name: manual-execution-reader
description: Reads BIDV manual execution results from VA-style testcase workbook or legacy tables and emits normalized TestExecution TSV.
role_affinity: [tester, qa_lead, qc_middle]
domain: [test_execution, excel, bidv]
lifecycle_stage: [test_execution]
produces: [execution_tsv]
consumes: [xlsx, tsv, csv, testcase]
maturity: draft
tier: 1
languages: [vi, en]
---

# BIDV Manual Execution Reader

## Operating mode

This skill is contract/tool-driven. It does not have a source prompt.

- Source BIDV Prompt: N/A
- Runtime Verbatim Prompt: N/A

## Selection criteria

Use this skill when the user asks to:

- import tester execution result from a BIDV/VA-style testcase workbook;
- read `Manual Test Results Round 1` or `Manual Test Results Round 2`;
- convert execution results into TestExecution TSV;
- feed manual execution counts into Paygates dashboard generation.

## Required inputs

- Executed legacy testcase workbook, TSV, or CSV.
- Execution metadata when known: Test Execution ID, Test Set ID, tester, build/version, environment.
- Status source: round 1, round 2, automation result, or explicit status column.

## Workflow

1. Load `manual_execution_reader_contract.md` and `test_status_excel_columns.md`.
2. Read the source table with `scripts/read_manual_execution_results.py`.
3. Extract testcase ID, selected status column, actual result, BugID, notes, and traceability fields.
4. Normalize status deterministically.
5. Emit TestExecution TSV.
6. Validate with `scripts/validate_output_contract.py --execution`.
7. Report missing metadata as `[PENDING_DOC:<field>]`; do not invent it.

## Outputs

- TestExecution TSV suitable for Paygates dashboard aggregation.

## Review gates

- Status mapping is deterministic.
- Execution TSV satisfies `test_status_excel_columns.md`.
- Actual result, BugID, and Notes are preserved.
- Missing metadata is explicit.
- The source workbook/table is read-only.
