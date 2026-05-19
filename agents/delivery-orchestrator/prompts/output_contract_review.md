# Output Contract Review Prompt

Review generated artifacts before handoff.

## Prompt-Compatible Orchestration checks

- Selected source prompt and runtime verbatim prompt match the request type.
- Runtime prompt mirror verification passed by `scripts/verify_prompt_mirrors.py` or manifest SHA evidence.
- Required prompt inputs are present or explicitly marked missing.
- Output follows the selected prompt rules and prohibitions.
- No native/freeform facts were introduced outside source docs or selected prompt boundaries.
- Markdown normalization preserves source prompt path, runtime verbatim prompt path, stable IDs, and traceability.
- Hard-fail if a non-runtime `skills/*/prompts/*.md` note was used as the runtime prompt.
- TSV/Excel-style export matches the selected output contract.
- Contract/tool-driven routes with no source prompt explicitly record `Source Prompt = N/A` and `Runtime Verbatim Prompt = N/A`.
- Legacy XLSX exports preserve canonical 19-column headers and manual execution result fields.
- Manual execution reader output preserves Actual Result, BugID/Defect Link, Notes, and explicit missing metadata markers.
- Paygates dashboard sync validates the dashboard TSV before XLSX output and never overwrites a source workbook in place.
- Testcase/status/dashboard outputs satisfy `excel_output_similarity.md` at contract level.
- Open questions are explicit, not hidden.

## Artifact quality checks

- Stable IDs are present.
- Requirement traceability is preserved where applicable.
- Test Case definition and Test Execution status remain separated.
- TSV column contract is satisfied when TSV export is expected.
- XRAY field mapping readiness is preserved when XRAY-style output is expected.
- Source fidelity is maintained.
