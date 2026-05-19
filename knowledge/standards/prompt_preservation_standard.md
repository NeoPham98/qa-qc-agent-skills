# Prompt Preservation Standard

## Purpose

This standard defines how source prompts are preserved, mirrored, and enhanced without degrading their core intent.

## Preservation rule

Prompt samples that are accepted as strong source assets should be preserved as golden prompts or provenance mirrors.

## Enhancement rule

Enhancement is allowed only as an additive layer, for example:

- pre-flight checklist,
- source evidence checklist,
- anti-hallucination guardrail,
- senior-QC coverage checklist,
- post-generation self-check,
- reviewer rubric.

These additions must strengthen fidelity and quality without rewriting the underlying prompt into a weaker or less specific form.

## Runtime usage pattern

Runtime prompt execution should follow this order when applicable:

```text
source evidence package -> preserved prompt -> enhancement layer -> validator -> output review -> supervisor approval
```

## Fidelity rules

- Preserve original technical intent and coverage logic.
- Preserve detailed generation structure when it materially affects quality.
- Record provenance or source references for mirrored prompts.
- Detect drift between mirrored prompts and source prompts with validator support when available.

## Forbidden behavior

- Do not normalize prompts into vague summaries.
- Do not remove detailed guidance that improves coverage quality.
- Do not claim a mirrored prompt is equivalent if meaningful constraints were dropped.
- Do not let enhancement layers override authoritative source logic.
