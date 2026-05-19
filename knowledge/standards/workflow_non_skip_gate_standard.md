# Workflow Non-Skip Gate Standard

## Purpose

This standard defines hard workflow gates for company-style QA/QC delivery.

## Immutable workflow

The default end-to-end workflow is:

```text
Project -> Squad -> Epic/Module -> Source Inventory -> Source Analysis -> Test Plan -> Test Design -> Test Generation Matrix / Coverage Matrix -> Test Case -> formatted Excel artifact -> Manual Execution -> Execution import / Status update -> Dashboard / Review -> Supervisor Approval -> Publish approved artifact
```

No agent may skip, reorder, or silently merge mandatory predecessor stages.

## Mandatory gates

1. End-to-end requests must enter through the delivery orchestrator.
2. Project, Squad, and Epic/Module metadata must exist before downstream generation.
3. Source inventory and source analysis must exist before Test Plan.
4. Test Plan must exist before Test Design.
5. Test Design must exist before testcase generation.
6. Test Generation Matrix or Coverage Matrix must exist before testcase export in applicable routes.
7. Validators must run before output review.
8. Output review must complete before supervisor approval.
9. Supervisor approval must complete before artifact publish.
10. Automation support is downstream and must not replace manual-first workflow stages.

## Rejection rules

A route should be rejected or blocked when:

- required predecessor artifacts are missing,
- source refs are absent,
- business logic was inferred without evidence,
- testcase generation bypassed matrix/design requirements,
- generator and approver are the same role,
- publish is attempted before review or approval.

## Escalation rules

If evidence is incomplete, the workflow must record gaps or open questions and stop at the highest safe stage instead of fabricating downstream artifacts.
