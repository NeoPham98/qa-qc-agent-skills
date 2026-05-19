# BIDV Output Review Team Playbook

## Purpose

Run parallel review of generated BIDV artifacts without modifying generator-owned files.

Do not commit `.claude/teams` or runtime task-list files. This playbook is a reusable recipe only.

## When to use

Use this review team before handoff when output includes multiple artifacts or derived TSV/Excel-style files.

## Runtime roles

| Review lane | Agent definition | Focus |
|---|---|---|
| Prompt fidelity reviewer | `output-reviewer` | selected prompt, fragment rules, phase separation |
| Source fidelity reviewer | `output-reviewer` | no invented API/UI/business/DB facts |
| Contract validator | `contract-validator` | TSV/output contract scripts and row-level failures |
| Coverage auditor | `coverage-auditor` | requirement -> TD -> testcase -> automation traceability |
| Supervisor handoff owner | `supervisor` | approval decision after review evidence is complete |

## Review checklist

1. Prompt selection matches request type and upstream artifact.
2. Runtime prompt mirror matches the source BIDV prompt exactly.
3. No worker used non-runtime summarized `skills/*/prompts/*.md` notes as the runtime prompt.
4. API TD is Markmap-style and preserves `TD_P1`, `TD_P2`, `TD_P3` separation.
5. API TD-derived testcase IDs follow `TD_Px_NNN_TC_NNN`.
6. Automation support includes testcase analysis before feature script support.
7. Feature/script support is filtered by phase: Method/Header `TD_P1`, Schema `TD_P2`, Logic/Business `TD_P3`.
8. Derived TSV/XLSX files pass selected validators.
9. Legacy XLSX exports preserve the 19-column contract and do not mutate external BIDV templates.
10. Manual execution reader outputs valid execution TSV and preserves actual result/BugID/notes.
11. Paygates dashboard sync validates dashboard TSV first and writes only to explicit output workbook paths.
12. All missing source details are explicit open questions or `[PENDING_DOC]` placeholders.
13. `OutputReview.md` records pass/fail decision, blocking fixes, and retry guidance for the owning generator.
14. Supervisor handoff includes validation evidence, no-secret evidence, and source trace before any artifact reaches `approved`.

## Parallel review rules

- Reviewers do not edit artifact files in parallel.
- Each reviewer reports findings with artifact path, line/section if available, violated rule, and recommended owner.
- The lead merges review findings into one OutputReview.
- If a blocker is found, route repair back to the owning generator worker, then rerun validator/review lane.
