# Prompt-Compatible Orchestration Playbook

## One operating mode

This package has one operating mode only: **Prompt-Compatible Orchestration Mode**.

Native Agent Mode is unsupported. The orchestrator must not generate outside the selected packaged runtime prompt. Runtime prompts must come from `prompts-verbatim/**` or workflow-pack prompt assets, not from summarized normalized notes.

## Standard pipeline

1. Intake request.
2. Classify request type and workflow step using `data/source-inventory/workflow_map.md`.
3. Select source prompt and `Runtime Verbatim Prompt` from the registry.
4. Verify the runtime prompt mirror matches the source prompt exactly.
5. Gather prompt-required inputs.
6. Generate according to selected prompt rules.
7. Normalize output to Markdown source-of-truth.
8. Export TSV/Excel-style output if required.
9. Compare output shape against `data/output-contracts/excel_output_similarity.md` when producing testcase/status/dashboard output.
10. Review against prompt fidelity, source fidelity, traceability, output contract, and baseline similarity.
11. Handoff with open questions if any.

## API prompt-phase routing

When the available upstream input is an API spec/source document and the user requests API Test Design, API Testcase, or API Automation Support, the orchestrator must route through the API prompt phases in order. Do not collapse these into a single native/freeform generation step.

Required order:

1. `API_TD_1_Setup_Context.txt`: load PTTK/RSD/DB knowledge and identify API scope only.
2. `API_TD_2_Method_Header.txt`: generate only `TD_P1_*` Method/Header Markmap nodes.
3. `API_TD_3_Schema_Validation.txt`: generate only `TD_P2_*` Schema Validation Markmap nodes.
4. `API_TD_4_Value_Business_Cross_Logic.txt`: generate only `TD_P3_*` Value/Business/Cross Logic Markmap nodes.
5. `API_Gen_TC_From_TD_v2.txt`: generate manual testcase rows strictly from the `TD_P1/TD_P2/TD_P3` nodes.
6. `API_TestCase_Analysis.txt`: analyze reviewed testcase source before any automation support.
7. `API_Gen_Script_*.txt`: generate automation support by testcase subset: Method/Header from `TD_P1`, Schema from `TD_P2`, Logic/Business from `TD_P3`.

Each listed `.txt` prompt must be resolved through the registry to its `Runtime Verbatim Prompt` mirror before execution. Matching `.md` files under `skills/*/prompts/` are non-runtime notes only.

Rules:

- If only API spec exists and the user asks for testcase or automation, first generate the required API TD phases.
- API TD output must be Markmap-style Markdown with `# <Method> <Endpoint> - <API name>`, `## Method & Header`, `## Schema Validation`, `## Value, Business Logic, Cross Logic`, and `TD_P1/TD_P2/TD_P3` IDs.
- Standalone API TD summary tables are not valid prompt-compatible TD output.
- A separate `Error Handling` TD lane is not valid for API TD; error scenarios must stay inside the owning phase: auth/header in `TD_P1`, schema validation in `TD_P2`, business/state/error-code logic in `TD_P3`.
- Testcase IDs generated from API TD must follow `TD_Px_NNN_TC_NNN`; `TC-API-*` IDs are not valid for API TD-derived testcase output.

## Execution mode guidance

Use the smallest coordination mode that preserves prompt fidelity:

- Single-agent route: one artifact, narrow fix, or one runtime verbatim prompt.
- Review-team route: multiple artifacts need independent prompt/source/contract/coverage review.
- Full-delivery-team route: source docs must flow through TD, testcase, automation support, validation, and handoff.
- SDK-runner route: repeatable/headless execution is needed with deterministic validators and guardrails.

Reusable team recipes live under `playbooks/agent-teams/`. Runtime `.claude/teams` and task-list state must not be committed to this repository.

## Request routing matrix

| Request type | Owning skill | Runtime prompt selection | Primary output | Export contract |
|---|---|---|---|---|
| API Test Design | `api-td-generate` | Registry-selected API TD `Runtime Verbatim Prompt` bundle | API Test Design Markdown | Markdown normalization |
| UI Test Design | `ui-td-generate` | Registry-selected UI TD `Runtime Verbatim Prompt` | UI Test Design Markdown | Markdown normalization |
| API Testcase from TD | `tc-generate-from-td` | Registry-selected API TC `Runtime Verbatim Prompt` | TestCase source Markdown | Legacy 19-column TSV |
| UI Testcase from TD | `tc-generate-from-td` | Registry-selected UI TC `Runtime Verbatim Prompt` | TestCase source Markdown | Legacy 19-column TSV |
| UAT Testcase | `uat-tc-generate` | Registry-selected UAT TC `Runtime Verbatim Prompt` | UAT TestCase source Markdown | UAT 16-column TSV |
| Test Execution Pack | `test-execution-pack-generate` | execution pack skill rules | TestExecution Markdown | Execution TSV |
| Manual Execution Reader / Import | `manual-execution-reader` | N/A contract/tool route | TestExecution TSV | Manual execution reader + Execution TSV |
| Paygates Dashboard / Status Summary | `paygates-dashboard-generate` | N/A contract/tool route | PaygatesDashboard Markdown | Paygates dashboard TSV/XLSX |
| Legacy 19-column XLSX Export | `legacy-xlsx-exporter` | N/A contract/tool route | Legacy testcase XLSX | Legacy 19-column XLSX derived from TSV contract |
| Paygates Dashboard Sync | `paygates-dashboard-sync` | N/A contract/tool route | Paygates dashboard XLSX | Paygates dashboard contract |
| API Automation Support | `api-automation-support-generate` | Registry-selected API automation `Runtime Verbatim Prompt` bundle | Automation support Markdown/features | Project-specific automation output |
| Coverage Audit | `coverage-audit` | coverage skill rules | Coverage Matrix Markdown | XRAY/TestLink-style if needed |
| Output Review | `output-verify` | output verification rules | Review report | N/A |

## Input gathering checklist

For every route, collect:

- Project/Squad/Epic.
- Requested artifact and target output folder.
- source prompt path and runtime verbatim prompt path.
- Prompt mirror verification result.
- Required source docs for the selected prompt.
- Upstream artifact IDs where applicable.
- Expected export contract.
- Open questions/missing inputs.

If a mandatory input is missing, stop generation or mark the missing value explicitly. Do not create native/freeform replacements for missing prompt input.

## Normalization rules

- Preserve stable IDs from prompt output or create deterministic IDs when the prompt requires them.
- Preserve source prompt path, runtime verbatim prompt path, prompt mirror evidence, and source docs in artifact metadata.
- Move assumptions and missing values to explicit Open Questions sections.
- Keep Markdown as source-of-truth.
- Generate TSV/Excel-style files only from normalized Markdown or reviewed source tables.

## Review gates

- Prompt selection matches request type and selected runtime mirror matches the source prompt.
- Required inputs are present or explicitly listed as missing.
- Output follows selected prompt rules/prohibitions.
- Source facts are traceable.
- Markdown normalization preserves IDs and traceability.
- Export matches selected output contract.
- No native/freeform content outside selected prompt/source boundaries.
