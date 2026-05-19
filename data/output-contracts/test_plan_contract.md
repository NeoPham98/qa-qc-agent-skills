# Test Plan Contract

This contract defines the runtime output shape for `TestPlan.md` in prompt-compatible workflow routes. Runtime artifacts must use current source inputs, source manifests, workflow pack contracts, prompt contracts, or normalized knowledge references; they must not require a raw sample folder path.

## Required metadata

The top section must include these fields with non-empty values or explicit pending markers in the form `[PENDING_DOC:<field>]`:

- `Test Plan ID`
- `Project`
- `Squad`
- `Epic`
- `Environment`
- `Build/Release`

## Required sections

`TestPlan.md` must include these Markdown sections:

- `## Scope In`
- `## Scope Out`
- `## Source Baseline`
- `## Requirement Baseline`
- `## Test Levels / Phases`
- `## Entry Criteria`
- `## Exit Criteria`
- `## Deliverables`
- `## Roles and Responsibilities`
- `## Environment / Test Data / Dependencies`
- `## Risks and Mitigations`
- `## Schedule / Milestones`
- `## Coverage Strategy`
- `## Open Questions`

## Required table expectations

- Source Baseline must list source references with `Source Ref`, `Source Kind`, and `Scope`.
- Requirement Baseline must list requirement references, included status, and notes.
- Test Levels / Phases must include phases such as SIT, UAT, regression, API, UI, manual, or automation when applicable.
- Deliverables must include at least one downstream testing artifact such as Test Design, testcase, execution, dashboard, coverage matrix, or automation feature output.
- Open Questions must be used for missing business facts instead of inventing details.

## Runtime rules

- Do not reference raw sample paths in runtime output.
- Source references must point to source manifest ids, normalized knowledge ids, workflow pack contract ids, prompt contract ids, or current run input sections/pages/sheets.
- Missing metadata is allowed only when explicitly marked as `[PENDING_DOC:<field>]`.
- If source facts are incomplete, record them in Open Questions rather than inferring them from naming conventions.
