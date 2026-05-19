---
name: testcase-validator
description: Runs deterministic BIDV testcase validators for legacy 19-column API/UI and 16-column UAT contracts.
role_affinity: [qa_lead, validator]
domain: [bidv, validation, testcase]
lifecycle_stage: [validation]
produces: [validation_report]
consumes: [tsv, xlsx_profile, testcase_artifact]
maturity: draft
tier: 1
languages: [vi, en]
---

# BIDV Testcase Validator

## Operating mode

Use this skill after testcase generation and before output review. It validates contract shape only; it does not rewrite generator-owned testcase artifacts.

## Required inputs

- Testcase artifact path.
- Validation profile: `legacy_19_column_testcase` or `uat_16_column_testcase`.
- Contract references from `workflow-packs/default/excel-contract.yml`.

## Workflow

1. Run `python scripts/validate_testcase_contract.py <path> --profile <profile>`.
2. For legacy 19-column output, require exact 19 columns, exactly 18 tabs per row, quote-all cells, logical `\n`, and empty initial `Notes`.
3. Normalize known header aliases before validation, but report contract mismatch when exported headers are still wrong.
4. Enforce `TD_P[123]_NNN_TC_NNN` for API testcase IDs and `TD_NNN_TC_NNN` for UI testcase IDs.
5. For UAT output, require the configured 16-column contract.

## Outputs

- Deterministic pass/fail report.
- Row/column-level findings for contract violations.
- Owner recommendation back to testcase generator when blocking findings exist.

## Guardrails

- Do not silently trust overflow workbook columns as contract expansion.
- Do not change testcase content during validation.
- Do not approve artifacts; hand off results to reviewer and supervisor.
