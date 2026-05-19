---
name: xray-test-workflow
description: Governs Prompt-Compatible Orchestration Mode, artifact separation, traceability, and handoff gates.
role_affinity: [qa_lead, qc_middle, tester, ba]
domain: [qa, testing, banking, bidv, xray]
lifecycle_stage: [test_planning, test_design, testcase_authoring, test_execution, coverage_audit]
produces: [md, requirement_inventory, test_plan, test_design, testcase, test_set, test_execution, coverage_matrix, review_report]
consumes: [md, txt, pdf, docx, xlsx, srs, api_spec, ui_spec, test_design]
maturity: draft
tier: 1
languages: [vi, en]
---

# BIDV XRAY Test Workflow

## Operating mode

This skill governs the only supported package mode: **Prompt-Compatible Orchestration Mode**.

XRAY/TestLink is an output and traceability target, not a separate operating mode. Native/freeform generation outside selected BIDV prompt rules is unsupported.

## When to use

Use this skill when a BIDV delivery task needs prompt-compatible orchestration, artifact separation, traceability, TSV/Excel-style export, and review before handoff.

## Required inputs

- Project/Squad/Epic context.
- Requested artifact and request type.
- Selected source prompt and runtime verbatim prompt path.
- Source business/spec/UI/test design files required by the selected prompt.
- Upstream IDs where applicable.
- Expected markdown artifact and export contract.
- Expected output path.

## Workflow

1. Classify request/artifact type.
2. Identify the BIDV workflow step using `../../data/source-inventory/workflow_map.md`.
3. Select the prompt/workflow path from the prompt fragment registry.
4. Gather prompt-required inputs.
5. If mandatory inputs are missing, ask or record open questions; do not improvise.
6. Generate according to selected BIDV prompt rules and prohibitions.
7. Normalize output to Markdown source-of-truth.
8. Export TSV/Excel-style rows when the selected output contract requires them.
9. Check testcase/status/dashboard output against `../../data/output-contracts/excel_output_similarity.md` when applicable.
10. Run output verification before handoff.

## Prompt-compatible routing categories

- API Test Design.
- UI Test Design.
- API/UI Testcase from Test Design.
- UAT Testcase.
- Test Set and Test Execution.
- API automation support.
- Coverage audit and output review.

## Core rules

- Use raw BIDV prompts and verified runtime prompt mirrors as behavior definitions.
- Use approved BIDV source documents as business input.
- Preserve Requirement ID and Test Condition ID in downstream artifacts where applicable.
- Keep Test Case definition separate from Test Execution status.
- Output must be maintainable Markdown; testcase/execution skills must also support TSV export compatible with BIDV Excel usage.
- Missing or ambiguous details become open questions, not invented logic.

## Quality gates

- Selected prompt fragment matches request type.
- Mandatory prompt inputs are present or explicitly missing.
- Identity fields are present.
- Traceability fields are populated.
- Source reference exists for business logic.
- BIDV output contract is satisfied when TSV export is expected.
- XRAY separation rules are not violated.

## Related references

- `../../data/source-inventory/orchestration_mode.md`
- `../../data/source-inventory/workflow_map.md`
- `../../data/source-inventory/prompt_fragment_registry.md`
- `../../data/output-contracts/markdown_normalization_rules.md`
- `../../data/output-contracts/excel_output_similarity.md`
- `../../data/output-contracts/legacy_19_column_testcase_contract.md`
- `../../data/output-contracts/uat_16_column_testcase_contract.md`
- `../../data/output-contracts/testcase_excel_columns.md`
- `../../data/output-contracts/test_status_excel_columns.md`
- `../../data/output-contracts/xray_field_mapping.md`
