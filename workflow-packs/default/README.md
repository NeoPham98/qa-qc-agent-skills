# Default Workflow Pack

Self-contained workflow pack for contract-style QA/test artifact generation. Runtime uses this pack instead of any external legacy source folder.

## User-facing final outputs

- Test Plan Markdown with source baseline, coverage strategy, review, and approval gates
- API/UI Test Design Markdown
- API/UI/UAT Test Case Markdown
- legacy 19-column TSV/XLSX
- API automation support analysis and `.feature` files
- Manual execution TSV
- Paygates dashboard TSV/XLSX
- Coverage/gap reports

## Technical support outputs

- source/route manifests
- validation reports
- OutputReview
- SupervisorApproval

## Contracts and validators

- `contracts/test_plan_contract.md` with `scripts/validate_test_plan.py`
- `contracts/api_automation_analysis_contract.md` with `scripts/validate_api_automation_analysis.py`
- `contracts/api_automation_feature_contract.md` with `scripts/validate_api_automation_feature.py`
- `contracts/test_generation_matrix_contract.md` with `scripts/validate_test_generation_matrix.py`

These support traceability and debugging but are not the primary user deliverables.
