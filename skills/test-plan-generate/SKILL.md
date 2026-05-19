---
name: test-plan-generate
description: Produces BIDV test planning artifacts as an orchestration step under selected BIDV workflow rules.
role_affinity: [qa_lead, ba]
domain: [testing, planning, bidv]
lifecycle_stage: [test_planning]
produces: [md, test_plan]
consumes: [source_docs, source_manifest, workflow_pack_contract]
maturity: beta
tier: 2
languages: [vi, en]
---

# BIDV Test Plan Generate

## Operating mode

This skill is invoked only inside **Prompt-Compatible Orchestration Mode**. It must not create a native/freeform plan outside workflow pack rules, and runtime output must not require a raw `BIDV/` folder path.

## Selection criteria

Use this skill when the requested artifact is a test plan or planning summary for a Project/Squad/Epic scope, or when a delivery route needs an approved planning artifact before Test Design, testcase, execution, dashboard, or automation work.

## Required inputs

- Project/Squad/Epic.
- Environment and Build/Release, or explicit `[PENDING_DOC:<field>]` markers.
- Source docs and scope with source manifest ids or current run source sections/pages/sheets.
- Requirement baseline or open questions for missing requirement facts.
- Target output path.

## Workflow

1. Receive planning route from orchestrator.
2. Verify planning scope, source baseline, and requirement baseline.
3. Generate `TestPlan.md` using `test_plan_contract.md` and the workflow template.
4. Preserve source references and record missing business facts in Open Questions.
5. Link the coverage strategy to `CoverageMatrix.md` or `TestGenerationMatrix.md`.
6. Validate with `scripts/validate_test_plan.py`.
7. Send output to review and supervisor approval.

## Outputs

- `TestPlan.md`.
- `OutputReview.md`.
- `SupervisorApproval.md`.

## Review gates

- Required metadata is present or explicitly pending.
- Scope in/out and requirement baseline are traceable to approved source refs.
- Test phases, entry/exit criteria, deliverables, roles, environments, dependencies, risks, and milestones are explicit.
- Coverage strategy references the generation/coverage matrix.
- Planning output does not invent missing requirements.
- Runtime output does not reference raw BIDV paths.
