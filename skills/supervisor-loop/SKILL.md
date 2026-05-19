---
name: supervisor-loop
description: Runs the BIDV closed-loop lifecycle from validator/review evidence to reviewed, approved, rejected, and archived artifact states.
role_affinity: [orchestrator, supervisor, qa_lead]
domain: [bidv, lifecycle, approval]
lifecycle_stage: [review, approval, publish]
produces: [published_artifact_manifest, supervisor_state, approved_artifact]
consumes: [source_manifest, route_plan, validation_report, output_review, supervisor_approval]
maturity: draft
tier: 1
languages: [vi, en]
---

# BIDV Supervisor Loop

## Operating mode

Use this skill after generator outputs exist in the route output directory. It enforces the BIDV lifecycle `draft -> reviewed -> approved/rejected`, applies retry policy, and publishes only when validation, review, and supervisor approval all pass.

## Required inputs

- `source_manifest.json` produced for the run.
- `route_id` from `workflow-packs/default/workflow.yml`.
- Output directory containing route artifacts.
- Project / Squad / Epic identifiers for artifact placement.
- Current `retry_count`.

## Workflow

1. Run `python scripts/run_closed_loop.py --manifest <source_manifest.json> --route-id <route_id> --output-dir <output_dir> --project <project> --squad <squad> --epic <epic>`.
2. Re-run deterministic stage validators for outputs already present in the route output directory.
3. Require `OutputReview.md` to exist and block approval on blocker/major findings.
4. Require `SupervisorApproval.md` with one decision: `approved`, `retry_required`, or `rejected`.
5. Copy route outputs into `artifacts/default/reviewed/...` before final approval.
6. If approved, archive existing approved targets and then copy the new artifacts into `artifacts/default/approved/...`.
7. If retry limit is exceeded or supervisor rejects, copy the artifacts into `artifacts/default/rejected/...`.
8. Write `published-artifact-manifest.yml` and `closed-loop-state.json`.

## Outputs

- `published-artifact-manifest.yml`
- `closed-loop-state.json`
- reviewed/approved/rejected artifact copies under `artifacts/default/`
- lifecycle decision summary on stdout

## Guardrails

- Do not generate business content on behalf of generator agents.
- Do not approve artifacts with failed validators.
- Do not publish artifacts with blocker/major review findings.
- Do not overwrite approved artifacts in place; archive first.
- Do not write back to Google Sheets or external systems without explicit user approval.
