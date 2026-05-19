# Universal File + Prompt Workflow

Use this playbook when a user drops files into Antigravity/Claude or calls the universal runner with files plus a natural-language prompt.

## Runtime dependency rule

Do not require an external raw sample folder at runtime. Use `workflow-packs/default/` for prompts, workflow routes, contracts, output profiles, validators, and examples.

## User-facing outputs

Prioritize final QA/test artifacts:

- `API_TestDesign.md`
- `UI_TestDesign.md`
- `TestCaseSource.md`
- `Legacy19TestCase.generated.tsv`
- `Legacy19TestCase.generated.xlsx`
- `UAT_TestCaseSource.md`
- `UAT_TestCase.generated.tsv`
- `api_method_header_validation.feature`
- `api_validation.feature`
- `api_logic_business.feature`
- `TestExecution.from-manual.tsv`
- `PaygatesDashboard.generated.tsv`
- `PaygatesDashboard.generated.xlsx`
- `CoverageMatrix.md`
- `GapAnalysis.md`

Support artifacts such as `source_manifest.json`, `route_plan.json`, `validation_report.json`, `OutputReview.md`, and `handoff_summary.md` are audit/debug deliverables only.

## Flow

1. Build source manifest from local files and Google Sheet references.
2. Fingerprint source roles.
3. Classify prompt intent.
4. Resolve route from `workflow-packs/default/workflow.yml`.
5. Generate the route's final outputs.
6. Validate outputs with workflow-pack validators.
7. Produce handoff summary with user-facing outputs first.

## Ambiguity handling

If the route confidence is low or multiple routes are plausible, ask for one of:

- target output: Test Design, Test Case, Excel, API `.feature`, dashboard, coverage;
- domain: API, UI, UAT, execution/status;
- source meaning: spec, test design, testcase, executed workbook.

Do not guess business rules or missing expected results.

## Google Sheet safety

Read-only is default. Export the selected tab/range to local staging TSV and process that TSV like any other source. Write-back requires explicit approval and must target a new tab/new spreadsheet unless overwrite is explicitly allowed.
