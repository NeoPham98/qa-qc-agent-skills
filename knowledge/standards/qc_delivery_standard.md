# Knowledge Standard: QC Delivery

This knowledge standard is distilled from terminal sample documents, historical prompts, Excel outputs, and senior-QC review expectations. It is portable product knowledge for QA/QC generation. It must not require any local sample folder on a user machine.

## Purpose

Use this standard to generate consistent QA artifacts across projects, squads, epics, APIs, UI flows, test designs, test cases, Excel testcase management, manual execution import, and status update workflows.

## Runtime rule

- Sample documents and sample prompts are knowledge/provenance inputs only.
- Runtime execution must use packaged prompts, skills, contracts, validators, golden examples, and normalized knowledge inside this repository.
- Final artifacts must not reference developer-local sample paths.
- If a source fact is missing, keep coverage and mark the missing expected behavior as `[PENDING_DOC]` with an Open Question.

## Delivery lifecycle

The default lifecycle is:

`Project → Squad → Epic → Source Intake → Requirement/Coverage Analysis → Test Plan → Test Design → Test Case → Excel Testcase Management → Manual Execution Import/Status Update → Validation → Output Review → Supervisor Approval → Artifact Publish`

## Agent team model

- `delivery-orchestrator`: QC Lead; selects route, assigns owners, enforces gates.
- `knowledge-retriever` / source intake stage: reads approved user sources or packaged knowledge.
- `requirement-coverage-analyst`: maps requirements to coverage obligations and gaps.
- `api-test-design-agent`: writes API TD with `TD_P1`, `TD_P2`, `TD_P3` phases.
- `ui-test-design-agent`: writes UI TD with screen/flow/action/state coverage.
- `testcase-generator`: converts TD into atomic testcase rows.
- `format-normalizer`: preserves contract shape and output hygiene.
- `test-set-execution-manager`: imports/updates manual execution/status data.
- `output-reviewer`: reviews prompt fidelity, source trace, coverage, granularity, and contract compliance.
- `supervisor`: final approval/retry/reject gate.

## Universal quality rules

1. The workflow route must be selected by the orchestrator; users do not need to name workflows.
2. Generator agents write draft artifacts only.
3. Reviewers and supervisors must not silently fix generator-owned artifacts.
4. Validators run before review.
5. `OutputReview.md` is required before supervisor approval.
6. `SupervisorApproval.md` is required before publish.
7. Approved artifacts must be versioned or archived, not overwritten in place.
8. Direct specialist invocation is allowed only for narrow tasks; end-to-end generation must use the orchestrator.

## Test Design standard

### API Test Design

API TD must preserve the phase model:

- `TD_P1`: Method/Header.
- `TD_P2`: Schema Validation.
- `TD_P3`: Value, Business Logic, Cross Logic.

Every API operation should be decomposed into:

- method and content-type controls;
- required/optional headers;
- request body/query/path fields;
- type, format, enum, requiredness, empty/null, min/max/below/above boundary checks;
- success response envelope;
- failure response envelope;
- documented error codes and business rules;
- cross-field, state, time, environment, role, or fixture-dependent rules when applicable.

### UI Test Design

UI TD must decompose:

- screen and navigation flow;
- user action;
- visible state;
- validation message;
- permission or role behavior;
- happy path;
- exception path;
- cancel/back/retry behavior when applicable;
- state transition when applicable.

## Test Case standard

1. `1 testcase = 1 primary condition`.
2. Every testcase must expose `Primary Condition:`, `Primary Target:`, or `Atomic Target:` in the source row.
3. Happy case alone is never enough for final QC handoff.
4. Each applicable flow must include happy path plus exception, negative, boundary, response/error, business-rule, cross-logic, and state/time coverage.
5. Do not combine multiple invalid inputs into one testcase unless the source defines a combined decision-table rule.
6. Do not combine multiple business outcomes into one testcase unless the source defines one combined rule.
7. Do not repurpose canonical testcase IDs across regenerations.
8. Initial manual execution result fields must remain blank unless execution data is explicitly supplied.

## Coverage rule set

Use `data/output-contracts/mandatory_test_coverage_rules.yml` as the machine-readable coverage rule source.

Required coverage families:

- happy path;
- exception path;
- negative validation;
- required/missing/empty/null;
- type/format/enum;
- boundary value;
- response success/failure envelope;
- business rule/error code;
- cross-logic/decision-table;
- state/time/environment;
- permission/role/session when applicable.

## Matrix standard

Use `data/output-contracts/test_generation_matrix_contract.md` to prove coverage expansion.

A matrix row should trace:

`source_ref → source_kind → field_or_rule → rule_type → technique → value_class → TD ID → Test Case ID → coverage status → rationale`

For final QC handoff:

- requirement-level matrix rows are not enough if field/rule/value/state expansion is possible;
- uncovered rows must be `gap` or `open_question` with rationale;
- covered rows must map to TD ID and Test Case ID.

## Excel standard

Use packaged contracts rather than sample files:

- Legacy API/UI testcase: `data/output-contracts/legacy_19_column_testcase_contract.md` and `data/output-contracts/testcase_excel_columns.md`.
- UAT testcase: `data/output-contracts/uat_16_column_testcase_contract.md`.
- Manual execution import/update: `data/output-contracts/manual_execution_reader_contract.md` and `data/output-contracts/test_status_excel_columns.md`.
- Dashboard/status summary: `data/output-contracts/paygates_dashboard_contract.md`.

The legacy 19-column contract is fixed. Do not add columns because a sample workbook contains overflow fields.

## Review standard

`output-reviewer` must block:

- happy-case-only outputs;
- broad testcase rows;
- bundled independent conditions;
- missing exception cases for documented errors;
- missing negative validation for documented required inputs;
- missing boundary cases for documented length/range;
- missing response/error coverage;
- repurposed testcase IDs;
- artifacts missing validator evidence;
- artifacts missing review/supervisor gates.

## Packaging standard

When converting new sample materials into reusable skills:

1. Extract durable knowledge and rules, not local paths.
2. Move reusable prompt behavior into workflow-pack prompts or agent instructions.
3. Move output shape into contracts.
4. Move quality gates into validators.
5. Move examples into golden examples.
6. Keep source/provenance notes only where useful for maintainers.
7. Do not make user runtime depend on the sample material folder.
