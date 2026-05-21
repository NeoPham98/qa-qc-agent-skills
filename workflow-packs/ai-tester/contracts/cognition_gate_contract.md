# Cognition Gate Contract

## Purpose

The cognition gate prevents direct raw-input-to-output generation.

## Required artifacts before output generation

A route must provide these artifacts before final output skills run:

- `SourceInventory.md`
- `DocumentMap.md`
- `FactInventory.md`
- `BusinessRuleModel.md` or blocker `OpenQuestions.md`
- `RiskModel.md`
- `CoveragePlan.md`
- `TesterStrategyPlan.md`
- `QuestionBacklog.md`

## Pass criteria

- Source inventory exists and classifies source roles.
- Document map identifies important sections, tables, APIs, UI flows, rules, and gaps.
- Fact inventory separates confirmed facts from assumptions.
- Business rules include condition, action, outcome, exception when available, and source refs.
- Risks are linked to source facts, rules, memory, or explicit hypotheses.
- Coverage plan includes happy, exception, negative, boundary, response/error, business, cross-logic, state/time, permission, and regression coverage when applicable.
- Tester strategy defines scope, priority, output order, and blocker handling.
- Question backlog marks blocker questions and proceed rules.

## Block conditions

- Output generation is requested with only raw input and no cognition artifacts.
- Blocker questions have no proceed rule.
- Business rules lack source refs or pending markers.
- Risk or defect hypotheses are presented as confirmed requirements.
- Required coverage is removed without rationale.
- Artifact contains unredacted secrets.

## Allowed proceed-with-pending rule

The route may continue with explicit pending markers only when:

- blocker status is downgraded with reviewer-visible rationale,
- affected output sections include `[PENDING_DOC:<fact>]`, and
- `QuestionBacklog.md` records the unresolved decision.
