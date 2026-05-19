# Test Plan

**Test Plan ID**: TP-PAYGATES-CCTG-001
**Project**: PAYGATES_E2E
**Squad**: Squad_Base
**Epic**: CCTG_API
**Environment**: SIT
**Build/Release**: 2026.05.18-rc1

## Scope In

- Validate API payment inquiry and domestic transfer testcase delivery for the CCTG API scope.
- Include API Test Design, manual testcase export, coverage matrix, execution status import readiness, and API automation support.

## Scope Out

- Production execution and external integration certification are excluded from this plan.

## Source Baseline

| Source Ref | Source Kind | Scope |
|---|---|---|
| source-manifest#api-cctg-source | runtime_input | API source and testcase seed for the current run |
| workflow-pack-contract#test_generation_matrix_contract | workflow_pack_contract | Coverage matrix traceability rules |

## Requirement Baseline

| Requirement ID | Source Ref | Included | Note |
|---|---|---|---|
| REQ-API-CCTG-001 | source-manifest#api-cctg-source | Yes | POST /payments/domestic validates method/header, schema, and business result handling |

## Test Levels / Phases

| Phase | Purpose | Owner | Environment | Entry Dependency | Exit Evidence |
|---|---|---|---|---|---|
| SIT | Verify API behavior against source rules | QA Lead | SIT | Approved source baseline | Validated testcase export |
| UAT | Confirm business acceptance coverage | BA Owner | UAT | SIT-ready build | UAT sign-off evidence |
| Regression | Protect existing payment flows | QA Lead | SIT | Regression scope approved | Regression dashboard |
| API Automation | Generate phase-specific feature files | Automation Engineer | SIT | Valid API testcase analysis | Validated `.feature` files |

## Entry Criteria

- Source baseline is available in the current run manifest.
- Environment SIT and build 2026.05.18-rc1 are available.
- Test data owner confirms seeded payment customer data.

## Exit Criteria

- Required Test Design and testcase deliverables pass validators.
- Coverage Matrix has no unresolved high-severity gaps.
- Output review has no blocker or major findings.
- Supervisor decision is approved.

## Deliverables

| Deliverable | Required | Owner | Output |
|---|---|---|---|
| Test Design | Yes | QA Lead | API_TestDesign.md |
| Testcase | Yes | Tester | TestCaseSource.md and Legacy19TestCase.generated.tsv/xlsx |
| Coverage Matrix | Yes | QA Lead | CoverageMatrix.md or TestGenerationMatrix.md |
| Execution Status | When execution is in scope | Tester | TestExecution.from-manual.tsv |
| Dashboard | When status reporting is in scope | QA Lead | PaygatesDashboard.generated.tsv/xlsx |
| API Automation | Yes | Automation Engineer | API_TestCase_Analysis.md and `.feature` files |

## Roles and Responsibilities

| Role | Responsibility | Owner |
|---|---|---|
| QA Lead | Own planning, review gates, and exit recommendation | QA Lead |
| BA/Product Owner | Confirm scope, requirement baseline, and open questions | BA Owner |
| Tester | Design and execute cases within assigned scope | Tester A |
| Automation Engineer | Generate and maintain automation support artifacts | Automation A |

## Environment / Test Data / Dependencies

| Item | Value | Owner | Status |
|---|---|---|---|
| Environment | SIT | Environment Owner | Ready |
| Build/Release | 2026.05.18-rc1 | Release Owner | Ready |
| Test Data | Customer CIF CCTG0001 with active payment account | Test Data Owner | Ready |
| External Dependencies | Domestic payment simulator | Integration Owner | Ready |

## Risks and Mitigations

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|
| Payment simulator unavailable | Blocks SIT execution | Use approved simulator maintenance window | Integration Owner |

## Schedule / Milestones

| Milestone | Planned Date | Owner | Exit Evidence |
|---|---|---|---|
| Test planning approval | 2026-05-18 | QA Lead | Approved TestPlan.md |
| Test Design ready | 2026-05-19 | QA Lead | Validated Test Design |
| Testcase ready | 2026-05-20 | Tester A | Validated testcase export |
| Execution complete | 2026-05-22 | Tester A | Execution report |

## Coverage Strategy

Coverage will be traced through `CoverageMatrix.md` or `TestGenerationMatrix.md`, mapping source rules to Test Design nodes, testcase rows, execution evidence, and open gaps. API automation coverage is split by `TD_P1`, `TD_P2`, and `TD_P3` testcase phases.

## Open Questions

| Question ID | Source Ref | Question | Owner | Needed By |
|---|---|---|---|---|
| OQ-001 | source-manifest#api-cctg-source | Confirm whether production-like timeout simulation is required for regression | BA Owner | 2026-05-19 |
