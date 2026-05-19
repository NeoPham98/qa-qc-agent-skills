# API Automation Analysis Contract

This contract defines the runtime shape for `API_TestCase_Analysis.md` generated from API testcase artifacts.

## Required output shape

The artifact must contain a Markdown table with these columns:

- `Test Case ID`
- `Main Component`
- `Phase`
- `Rationale`

## Classification rules

- Every testcase id from the source testcase artifact must appear exactly once.
- `TD_P1_*` testcases must classify as Method/Header with phase `TD_P1`.
- `TD_P2_*` testcases must classify as Schema/Validation with phase `TD_P2`.
- `TD_P3_*` testcases must classify as Logic/Business with phase `TD_P3`.
- Do not add prose outside the required table when the active prompt requires table-only output.
- Do not invent testcase ids, payload fields, SQL/schema details, or internal implementation markers.
- Do not reference raw sample paths in runtime output.

## Source handling

Source testcase artifacts may be Markdown tables, Markdown sections, TSV, or plain text. Runtime traceability must use current run inputs, source manifests, prompt contracts, workflow pack contracts, normalized knowledge, or golden examples.
