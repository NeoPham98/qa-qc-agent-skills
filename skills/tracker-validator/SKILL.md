---
name: tracker-validator
description: Audits BIDV Paygates tracker workbooks for expected sheets, status aliases, unknown statuses, and suspicious formulas.
role_affinity: [qa_lead, validator]
domain: [bidv, validation, tracker]
lifecycle_stage: [validation]
produces: [validation_report]
consumes: [xlsx_tracker, tracker_artifact]
maturity: draft
tier: 1
languages: [vi, en]
---

# BIDV Tracker Validator

## Operating mode

Use this skill before review or publish when a BIDV route produces or audits Paygates tracker/dashboard artifacts. It reports deterministic findings and never writes back to source workbooks.

## Required inputs

- Tracker workbook path.
- Expected sheet/status/formula contract from `workflow-packs/default/excel-contract.yml`.
- Status normalization rules from `workflow-packs/default/status-enums.yml`.

## Workflow

1. Run `python scripts/validate_tracker.py <path>`.
2. Require the workbook to classify as `paygates_tracker`.
3. Require all expected sheets from the Paygates contract.
4. Report known aliases such as `Read to UAT`, `AI Gen`, `In - Progress`, and `UI`.
5. Report suspicious formulas where criteria range references `Squad_CnR` but sum range references `Squad_VA`.

## Outputs

- Deterministic pass/fail report.
- Sheet-level alias and formula findings.
- Escalation-ready findings for reviewer/supervisor.

## Guardrails

- Do not auto-fix workbook formulas.
- Do not write back to Excel/Google Sheets without explicit user approval.
- Do not downgrade unknown statuses to warnings in final approved artifacts.
