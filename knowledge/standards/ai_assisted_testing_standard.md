# AI-Assisted Testing Standard

## Purpose

This standard defines guardrails for AI-assisted QA/QC generation, review, and orchestration.

## Core principles

- AI assists the workflow but does not replace evidence.
- AI must preserve source logic.
- AI must not hallucinate missing business behavior.
- AI must respect workflow order and role boundaries.

## Required behavior

AI-assisted agents must:

1. use source evidence or approved upstream artifacts,
2. preserve Project / Squad / Epic context,
3. surface uncertainty as `open_question`, `gap`, or `[PENDING_DOC:<fact>]`,
4. keep traceability across source, design, matrix, testcase, and execution artifacts,
5. route generated output through validators, review, and supervisor approval before publish.

## Prompt handling rule

Prompt assets may be mirrored and preserved as golden prompts or provenance assets.

They may be strengthened with wrappers, checklists, guardrails, or reviewer criteria, but they must not be weakened by removing important intent, detailed coverage logic, or source-fidelity expectations.

## Human-style quality rule

AI output should reflect how a senior QC would work:

- read the source,
- analyze deeply,
- split modules into business operations and rules,
- design before generating cases,
- keep steps executable,
- keep expected results measurable,
- keep gaps visible.

## Forbidden behavior

- Do not skip predecessor artifacts.
- Do not change documented logic to make generation easier.
- Do not auto-approve generator-owned output.
- Do not use raw sensitive assets directly when redacted or packaged runtime artifacts are required.
- Do not treat automation as a substitute for manual-first workflow stages.
