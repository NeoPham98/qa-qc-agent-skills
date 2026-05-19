# BIDV E2E Golden Examples

This folder contains maintainable golden examples that exercise the BIDV closed-loop delivery workflow without depending on the raw `BIDV/` folder at runtime.

## Included example routes

### `api-cctg/`

Golden API route proving:

- API operation inventory
- API test design with `TD_P1` / `TD_P2` / `TD_P3`
- Legacy 19-column testcase export
- Output review and supervisor approval
- Closed-loop publish to reviewed/approved artifact folders

Key artifacts:

- `API_OperationInventory.md`
- `API_TestDesign.md`
- `TestCaseSource.md`
- `Legacy19TestCase.generated.tsv`
- `Legacy19TestCase.generated.xlsx`
- `OutputReview.md`
- `SupervisorApproval.md`

### `ui-uat/`

Golden UI and UAT routes proving:

- canonical UI TD heading format `### TD_001 - [Technique] - Summary`
- legacy 19-column UI testcase export
- UAT 16-column testcase export
- output review and supervisor approval
- closed-loop publish for UI and UAT routes

Key artifacts:

- `UI_TestDesign.md`
- `UI_TestCaseSource.md`
- `UAT_TestCaseSource.md`
- `OutputReview.md`
- `SupervisorApproval.md`

### `paygates-tracker/`

Reserved for Paygates tracker/dashboard examples. Current coverage is exercised primarily by the automated audit test, which builds temporary tracker/testcase/execution/dashboard artifacts and verifies alias detection, formula warnings, dashboard export, and XLSX sync behavior.

## How to run the golden checks

Run the direct Python tests from `qc-agent-skills/`:

```bash
python tests/test_e2e_api_workflow.py
python tests/test_e2e_ui_uat_workflow.py
python tests/test_paygates_tracker_audit.py
python tests/test_supervisor_loop.py
```

## What these examples prove

- workflow routes can produce maintainable Markdown source-of-truth artifacts
- contract validators gate legacy 19-column, UAT 16-column, execution, and dashboard outputs
- review and supervisor artifacts are required before approval
- approved artifacts publish through the managed lifecycle instead of overwriting in place
- runtime outputs remain free of raw BIDV secrets/internal endpoints

## Runtime note

These examples are intended for validation and regression testing. Production routing should still go through `agents/delivery-orchestrator/AGENT.md` and the selected workflow pack.
