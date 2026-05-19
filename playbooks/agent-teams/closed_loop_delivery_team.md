# BIDV Closed-Loop Delivery Team Playbook

## Purpose

Coordinate a BIDV delivery run from routed source intake to reviewed, approved, and published artifacts.

Use this playbook when the request must behave like the BIDV company-machine workflow: generator agents create artifacts, validators and reviewers gate quality, the supervisor decides approval, and the runtime publishes only approved outputs into the managed artifact lifecycle.

Do not commit `.claude/teams` or runtime task-list files. This playbook is a reusable execution recipe only.

## When to use

Use this team route when the request spans a closed loop such as:

- Project / Squad / Epic intake -> API/UI/UAT test design -> testcase export -> review -> supervisor approval -> publish
- Testcase -> manual execution result ingestion -> dashboard/status sync -> review -> approval -> publish
- Repair loops where validator or review findings must route back to the owning generator before final approval

Use a narrower team recipe when the user needs only one artifact and does not need lifecycle publish gates.

## Runtime roles

| Runtime role | Agent definition / skill | Owns | Must not own |
|---|---|---|---|
| Lead | `delivery-orchestrator` | request classification, route selection, task assignment, final handoff | direct artifact generation |
| Knowledge retriever | `knowledge-retriever` | canonical source lookup from runtime-safe knowledge | raw sensitive source publication |
| Generator worker | artifact-specific BIDV generator agent/skill | draft Markdown/TSV/XLSX artifact creation | self-approval |
| Contract validator | `contract-validator` | deterministic validation evidence and contract failures | silent repairs unless assigned |
| Coverage auditor | `coverage-auditor` | source-to-output traceability and gap findings | source fact invention |
| Output reviewer | `output-reviewer` | OutputReview with pass/fail/open questions | generator-owned edits in parallel |
| Supervisor | `supervisor` | approval decision, retry instruction, publish authorization | draft generation |

## Closed-loop lifecycle

Managed artifact states:

1. `draft` - generator-owned working output
2. `reviewed` - validator/reviewer gates passed and review evidence captured
3. `approved` - supervisor explicitly approved and publish manifest passed
4. `rejected` - route exceeded retry budget or supervisor rejected the result
5. `archive` - previous approved output preserved before replacement

Publish paths must follow the workflow pack artifact policy. Approved artifacts must never overwrite an existing approved artifact in place.

## Standard task flow

1. Lead classifies the request with `data/source-inventory/workflow_map.md` and selects the route.
2. Knowledge retriever resolves canonical runtime-safe sources from workflow pack data and `knowledge/default/redacted/`.
3. Lead assigns the correct generator worker for API/UI/UAT/execution/dashboard output.
4. Generator creates draft Markdown source-of-truth artifacts and any required TSV/XLSX exports.
5. Contract validator runs route validators and records deterministic results.
6. Coverage auditor checks source -> design -> testcase -> execution/dashboard traceability where applicable.
7. Output reviewer writes `OutputReview.md` with blocking findings, open questions, and handoff status.
8. Supervisor checks validator evidence, review findings, source trace, and no-secret expectations.
9. If blockers exist, the lead routes repair back to the owning generator and increments retry count.
10. If supervisor approves, the runtime promotes artifacts to `reviewed` and `approved`, writes manifest/state files, and publishes to the managed artifact folders.
11. If retry budget is exhausted or supervisor rejects, the runtime moves artifacts to `rejected` with evidence.
12. If an approved artifact already exists, archive it before publishing the replacement.

## Required handoff evidence

- Route ID and workflow pack used
- Source manifest or equivalent source trace
- Generated artifact paths
- Validation report
- OutputReview decision
- SupervisorApproval decision
- No-secret evidence for runtime-safe outputs
- Published artifact manifest and lifecycle state

## Retry and escalation rules

- Generator agents never approve their own outputs.
- Validators and reviewers report findings; they do not silently change generator-owned outputs unless the lead reassigns repair.
- Missing business facts become open questions or `[PENDING_DOC]`, never assumptions.
- Critical validator/review failures route back to the owning generator until `max_retries` is reached.
- Default closed-loop retry budget is `2` unless the selected workflow route says otherwise.

## Execution notes

- Prefer runtime-safe knowledge and workflow-pack configuration over direct raw `BIDV/` reads at delivery time.
- Do not publish raw credentials, internal endpoints, or sensitive config.
- Report workbook formula issues first; do not auto-fix external source workbooks without explicit user approval.
- Use the closed-loop runner when deterministic publish evidence is required.
