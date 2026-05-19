# Markdown Normalization Rules

Markdown artifacts are the source-of-truth for `qc-agent-skills`. TSV/Excel-style files are derived operational exports.

## Required metadata

Each normalized Markdown artifact should identify:

- Project/Squad/Epic when applicable.
- Requested artifact type.
- Source prompt path or `N/A` if the step has no raw prompt.
- Runtime verbatim prompt path or owning skill path.
- Source business/spec/UI/test design files.
- Output contract used for derived exports.
- Open questions or missing mandatory input.

## Normalization requirements

- Preserve stable IDs from the selected prompt workflow.
- Preserve Requirement ID, Test Condition ID, Test Case ID, Test Set ID, and Test Execution ID where applicable.
- Convert prompt output into maintainable headings/tables without changing business meaning.
- Keep assumptions and missing values explicit in an Open Questions section.
- Do not hide `[PENDING_DOC]` or unresolved source gaps.
- Do not introduce native/freeform facts outside selected prompt/source boundaries.

## Export relationship

- Legacy 19-column testcase TSV is derived from normalized testcase Markdown.
- UAT 16-column TSV is derived from normalized UAT testcase Markdown.
- Execution TSV is derived from normalized TestExecution Markdown.
- XRAY/TestLink-style TSV is derived from normalized traceability artifacts.

## Review requirements

Before handoff, verify:

- selected source prompt and runtime prompt match request type,
- mandatory inputs are present or explicitly missing,
- source references are preserved,
- output contract is satisfied,
- open questions are visible.
