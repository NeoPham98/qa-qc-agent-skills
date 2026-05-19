# Test Plan

**Test Plan ID**: {{test_plan_id}}
**Project**: {{project}}
**Squad**: {{squad}}
**Epic**: {{epic}}
**Environment**: {{environment}}
**Build/Release**: {{build_release}}

## Scope In

- {{scope_in}}

## Scope Out

- {{scope_out}}

## Source Baseline

| Source Ref | Source Kind | Scope |
|---|---|---|
| {{source_ref}} | runtime_input | {{source_scope}} |

## Requirement Baseline

| Requirement ID | Source Ref | Included | Note |
|---|---|---|---|
| {{requirement_id}} | {{source_ref}} | Yes | {{requirement_note}} |

## Test Levels / Phases

| Phase | Purpose | Owner | Environment | Entry Dependency | Exit Evidence |
|---|---|---|---|---|---|
| SIT | Verify integrated system behavior before handoff | {{sit_owner}} | {{environment}} | Approved requirement baseline | Passed SIT execution evidence |
| UAT | Confirm business acceptance coverage | {{uat_owner}} | {{environment}} | SIT-ready build and business test data | UAT sign-off evidence |
| Regression | Protect existing critical flows | {{regression_owner}} | {{environment}} | Stable regression scope | Regression status report |

## Entry Criteria

- {{entry_criteria}}

## Exit Criteria

- {{exit_criteria}}

## Deliverables

| Deliverable | Required | Owner | Output |
|---|---|---|---|
| Test Design | Yes | {{td_owner}} | API_TestDesign.md or UI_TestDesign.md |
| Testcase | Yes | {{tc_owner}} | TestCaseSource.md and generated TSV/XLSX when applicable |
| Coverage Matrix | Yes | {{coverage_owner}} | CoverageMatrix.md or TestGenerationMatrix.md |
| Execution Status | When execution is in scope | {{execution_owner}} | TestExecution.from-manual.tsv |
| Dashboard | When status reporting is in scope | {{dashboard_owner}} | PaygatesDashboard.generated.tsv/xlsx |
| API Automation | When automation is in scope | {{automation_owner}} | API_TestCase_Analysis.md and `.feature` files |

## Roles and Responsibilities

| Role | Responsibility | Owner |
|---|---|---|
| QA Lead | Own planning, review gates, and exit recommendation | {{qa_lead}} |
| BA/Product Owner | Confirm scope, requirement baseline, and open questions | {{ba_owner}} |
| Tester | Design and execute cases within assigned scope | {{tester_owner}} |
| Automation Engineer | Generate and maintain automation support artifacts when applicable | {{automation_owner}} |

## Environment / Test Data / Dependencies

| Item | Value | Owner | Status |
|---|---|---|---|
| Environment | {{environment}} | {{environment_owner}} | {{environment_status}} |
| Build/Release | {{build_release}} | {{release_owner}} | {{release_status}} |
| Test Data | {{test_data}} | {{test_data_owner}} | {{test_data_status}} |
| External Dependencies | {{dependencies}} | {{dependency_owner}} | {{dependency_status}} |

## Risks and Mitigations

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|
| {{risk}} | {{risk_impact}} | {{mitigation}} | {{risk_owner}} |

## Schedule / Milestones

| Milestone | Planned Date | Owner | Exit Evidence |
|---|---|---|---|
| Test planning approval | {{planning_date}} | {{qa_lead}} | Approved TestPlan.md |
| Test Design ready | {{td_date}} | {{td_owner}} | Validated Test Design |
| Testcase ready | {{tc_date}} | {{tc_owner}} | Validated testcase export |
| Execution complete | {{execution_date}} | {{execution_owner}} | Execution report |

## Coverage Strategy

Coverage will be traced through `CoverageMatrix.md` or `TestGenerationMatrix.md`, mapping source rules to Test Design nodes, testcase rows, execution evidence, and open gaps. Missing business facts remain open questions until confirmed by source owners.

## Open Questions

| Question ID | Source Ref | Question | Owner | Needed By |
|---|---|---|---|---|
| OQ-001 | {{source_ref}} | {{open_question}} | {{question_owner}} | {{needed_by}} |
