# BIDV API Delivery Team Playbook

## Purpose

Coordinate a full BIDV API delivery chain with runtime Claude Code Agent Teams while preserving Prompt-Compatible Orchestration Mode.

Do not commit `.claude/teams` or runtime task-list files. Team state is created only at execution time.

## When to use

Use this team route when the request spans multiple artifacts, for example API spec -> API TD -> testcase -> automation support -> review.

Use a single-agent route instead when the request is limited to one artifact or one narrow correction.

## Runtime roles

| Runtime role | Agent definition | Owns | Must not own |
|---|---|---|---|
| Lead | `delivery-orchestrator` | routing, task split, handoff decision | artifact generation details |
| TD worker | `api-test-design-agent` | API TD Markdown, `TD_P1/TD_P2/TD_P3` nodes | testcase rows, script features |
| Testcase worker | `testcase-generator` | TestCase source, legacy TSV export input | TD scope changes, review decision |
| Automation worker | `api-automation-support-generate` skill route | testcase analysis and phase-specific feature support | TD/testcase invention |
| Contract validator | `contract-validator` | validator evidence and contract failures | artifact repair unless assigned |
| Coverage auditor | `coverage-auditor` | traceability and gap matrix | source fact invention |
| Output reviewer | `output-reviewer` | final OutputReview and blocking findings | parallel edits to generator-owned files |
| Supervisor | `supervisor` | approval decision, retry instruction, publish authorization | draft generation |

## Standard task flow

1. Lead classifies request using `data/source-inventory/workflow_map.md`.
2. Lead selects source BIDV prompts and `Runtime Verbatim Prompt` paths using `data/source-inventory/prompt_fragment_registry.md`.
3. Contract validator verifies prompt mirrors with `scripts/verify_prompt_mirrors.py` before generation.
4. TD worker creates API Requirement Inventory / Operation Cards from source docs and approved enrichment references.
5. TD worker creates or updates API TD using setup/context -> `TD_P1` -> `TD_P2` -> `TD_P3`, grounded in operation cards.
6. Contract validator runs API TD specificity validation before testcase generation.
7. Testcase worker derives testcase rows only from approved detailed TD nodes.
8. Automation worker runs testcase analysis before any phase-specific script support.
9. Contract validator runs deterministic validators for derived TSV/output contracts, including API testcase specificity when applicable.
10. Coverage auditor checks source -> operation card -> TD -> testcase -> automation traceability.
11. Output reviewer writes pass/fail/open-question findings for handoff in `OutputReview.md`.
12. Supervisor verifies validator evidence, review findings, source trace, and no-secret expectations before publish.
13. If blockers remain, the lead routes repair back to the owning generator worker and reruns validation/review.
14. If approval passes, publish through the managed lifecycle `draft -> reviewed -> approved`, archiving any previous approved artifact before replacement.

## Ownership rules

- Assign exactly one writer per artifact path.
- Reviewer and validator roles should be read-only unless the lead explicitly assigns repair work.
- Do not split one Markdown artifact across parallel writers.
- Missing source facts must become open questions, not assumptions.

## Required handoff evidence

- Selected source BIDV prompt and runtime verbatim prompt path.
- Prompt mirror verification result and sha256 evidence.
- Source documents used.
- Generated/updated artifact paths.
- Validator command results.
- Coverage gaps or explicit no-gap finding.
- OutputReview decision.
