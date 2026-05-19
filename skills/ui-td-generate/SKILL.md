---
name: ui-td-generate
description: Generates UI Test Design only through the BIDV UI TD runtime verbatim prompt.
role_affinity: [qc_middle, tester, ba]
domain: [ui, testing, bidv]
lifecycle_stage: [test_design]
produces: [md, ui_test_design]
consumes: [ui_spec, runtime_verbatim_prompt, source_docs]
maturity: draft
tier: 1
languages: [vi, en]
---

# BIDV UI Test Design Generate

## Operating mode

This skill is invoked only inside **Prompt-Compatible Orchestration Mode**. Native/freeform UI TD generation outside selected BIDV prompt rules is unsupported.

## Selection criteria

Use this skill when the requested artifact is UI Test Design.

## Prompt compatibility

Owned BIDV source/runtime prompt mapping:

- `BIDV/Prompt/UI/UI_Gen_TD.txt` -> `prompts-verbatim/UI/UI_Gen_TD.txt`

Runtime execution must load the `Runtime Verbatim Prompt` from `../../data/source-inventory/prompt_fragment_registry.md`. Files under `prompts/*.md` are non-runtime notes unless verified as content-equivalent to the source prompt.

## Required inputs

- Project/Squad/Epic.
- UI/RSD/PTTK source docs, screen scope, fields, buttons, messages, business rules.
- Source BIDV prompt path.
- Runtime verbatim prompt path.
- Prompt mirror verification result.
- Expected output path.

## Workflow

1. Receive selected UI TD runtime verbatim prompt from orchestrator.
2. Verify prompt mirror fidelity before generation.
3. Verify required UI/source inputs.
4. Generate UI TD according to BIDV UI prompt rules.
5. Normalize output to Markdown.
6. Record missing UI/source values as open questions.
7. Send output to review.

## Outputs

- UI Test Design Markdown.

## Review gates

- Correct UI TD runtime verbatim prompt selected.
- No invented screens, fields, messages, or flows.
- Source references preserved.
