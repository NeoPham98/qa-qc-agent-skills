# Test Plan

**Test Plan ID**: TP-CCTG-ONLINE-001
**Project**: CCTG_Online
**Squad**: Squad_Customer
**Epic**: Customer_Validate
**Environment**: SIT
**Build/Release**: 2026.05.20-rc1

## Scope In

- Validate API customer condition checking (`POST /v1/customer/validate`) for the CCTG Online scope.
- Include API Test Design, manual testcase export, and formatted Excel delivery.

## Scope Out

- Production deployment sign-off and external system integration certification are excluded.

## Source Baseline

| Source Ref | Source Kind | Scope |
|---|---|---|
| source-manifest#source-1 | runtime_input | API check điều kiện KH mua CCTG OL PDF |

## Requirement Baseline

| Requirement ID | Source Ref | Included | Note |
|---|---|---|---|
| REQ-CCTG-001 | source-manifest#source-1 | Yes | Check conditions: citizenship (101), age (102), customer type (103), residency (104), COT (109) |

## Test Levels / Phases

| Phase | Purpose | Owner | Environment | Entry Dependency | Exit Evidence |
|---|---|---|---|---|---|
| SIT | Verify API validation codes and error priorities | QA Lead | SIT | Approved source document | Validated test design and test cases |
| UAT | Verify business scenarios and integration correctness | BA Owner | UAT | SIT sign-off | UAT sign-off documentation |

## Entry Criteria

- Target PDF document is normalized and available.
- SIT environment is ready with customer CIF mock data.

## Exit Criteria

- 100% of planned test cases are executed.
- No blocker or major defects are open.
- Generated Test Plan, Test Design, and Test Case outputs are signed off.

## Deliverables

| Deliverable | Required | Owner | Output |
|---|---|---|---|
| Test Plan | Yes | QA Lead | TestPlan.md and TestPlan.generated.xlsx |
| Test Design | Yes | QA Lead | API_TestDesign.md and API_TestDesign.generated.xlsx |
| Testcases | Yes | Tester | TestCaseSource.md and Legacy19TestCase.generated.xlsx |

## Roles and Responsibilities

| Role | Responsibility | Owner |
|---|---|---|
| QA Lead | Plan validation scope, approve deliverables | QA Lead |
| Tester | Design, execute tests, report defects | Tester |

## Environment / Test Data / Dependencies

| Item | Value | Owner | Status |
|---|---|---|---|
| SIT Environment | SIT-cctg-online | Env Team | Ready |
| Test Data | Customer CIFs matching validation rules | Data Team | Ready |

## Risks and Mitigations

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|
| SIT Environment downtime | Delay in validation | Deploy local mocks for API validation codes | QA Lead |

## Schedule / Milestones

| Milestone | Planned Date | Owner | Exit Evidence |
|---|---|---|---|
| Test Plan Approval | 2026-05-20 | QA Lead | Signed TestPlan.md/xlsx |
| Test Design & Test Cases | 2026-05-21 | Tester | Signed Test Design/Cases |

## Coverage Strategy

Traceability between requirements and test items will be maintained. Every business error code (101, 102, 103, 104, 109) must have at least one test design node.

## Open Questions

| Question ID | Source Ref | Question | Owner | Needed By |
|---|---|---|---|---|
| OQ-001 | source-manifest#source-1 | Are there any extra COT rules for non-residents? | BA Owner | 2026-05-21 |
