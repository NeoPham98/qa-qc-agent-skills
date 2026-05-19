---
name: output-verify
description: Reviews BIDV prompt-compatible outputs against prompt fidelity, source fidelity, traceability, and output contracts.
role_affinity: [qa_lead, reviewer]
domain: [review, verification, bidv]
lifecycle_stage: [handoff]
produces: [md, review_report]
consumes: [generated_artifacts, output_contracts]
maturity: draft
tier: 1
languages: [vi, en]
---

# BIDV Output Verify

## Operating mode

This skill is invoked only inside **Prompt-Compatible Orchestration Mode**. It verifies that outputs follow the selected prompt/workflow and output contracts.

## Selection criteria

Use this skill before any BIDV artifact handoff.

## Required inputs

- Generated Markdown artifacts.
- Derived TSV/Excel-style outputs when present.
- Selected source BIDV prompt and runtime verbatim prompt paths.
- Prompt mirror manifest and verification result.
- Output contracts.
- Source docs/open questions.

## Workflow

1. Verify prompt selection matches request type and phase sequence.
2. Verify runtime prompt mirror matches the selected source prompt exactly.
3. Verify API Test Design structure and IDs against BIDV phase contract.
4. Verify Test Case source derivation from TD nodes and ID policy.
5. Verify automation-support routing (analysis -> phase-specific script generation).
6. Verify source fidelity and no invented facts.
7. Verify Markdown normalization and traceability.
8. Verify TSV/Excel-style output contracts.
9. Produce review report and handoff decision.

## Outputs

- OutputReview Markdown.
- Pass/fail/open-question findings.
- Hard-fail findings list with blocking reasons.

## Hard-fail conditions

Any item below must force overall decision to `FAIL` until corrected:

1. API Test Design is not Markmap-style structure aligned with BIDV API TD fragments.
2. API Test Design does not preserve phase separation `TD_P1`, `TD_P2`, `TD_P3`.
3. Test Case IDs do not follow `TD_Px_NNN_TC_NNN` derivation from TD nodes.
4. Automation support output bypasses testcase analysis or skips phase-specific script prompts.
5. Prompt/source mismatch: artifact is generated with a different prompt family than requested phase.
6. Runtime prompt mirror does not match the selected source prompt exactly.
7. Artifact uses a non-runtime summarized `skills/*/prompts/*.md` note as the runtime prompt.
8. Artifact does not record selected source BIDV prompt and runtime verbatim prompt path.
9. Invented API/business/schema/header facts not traceable to source docs.

## API specificity hard-fail conditions

For API TD/testcase deliverables, structural validation is not enough. Any item below must fail output review:

- API testcase rows pass the legacy 19-column contract but lack concrete method/path/request execution details.
- `Test Datas` remains generic or placeholder-only while source/enrichment provides fields.
- `Expected result` lacks HTTP status or response/error assertion.
- Negative tests do not identify the exact field, header, parameter, rule, or error code under test.
- Required fields from operation cards are not covered by missing-field tests or a documented representative-set rationale.
- Documented business error codes are not covered or explicitly marked out of scope.
- Known source facts are replaced by `[PENDING_DOC]` without an open-question reason.
- Formatted XLSX output shows escaped `\n` instead of real line breaks in manual-step cells.

## Review gates

- Prompt fidelity.
- Phase fidelity (`setup/context -> TD_P1 -> TD_P2 -> TD_P3 -> TC -> analysis -> automation support`).
- Source fidelity.
- Contract compliance.
- Traceability.
- Open questions visible.

## Verification checklist (API-focused)

- API TD has explicit sections/nodes for `TD_P1`, `TD_P2`, `TD_P3` and no collapsed summary-table substitute.
- Each TD node referenced by testcase source has at least one matching testcase ID pattern `TD_Px_NNN_TC_NNN`.
- No testcase uses generic/non-derived IDs such as `TC-API-*`.
- Automation support contains all required components in order:
  1) testcase analysis table,
  2) method/header feature output,
  3) schema validation feature output,
  4) logic/business feature output.
- Feature outputs are filtered by correct testcase groups (`TD_P1`, `TD_P2`, `TD_P3`) with no cross-component leakage.
- Missing source details are represented as explicit placeholders/open questions (for example `[PENDING_DOC]`), never invented.
