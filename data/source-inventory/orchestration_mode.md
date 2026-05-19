# Prompt-Compatible Orchestration Mode

## Definition

`qc-agent-skills` supports exactly one operating mode: **Prompt-Compatible Orchestration Mode**.

In this mode, agent skills coordinate the packaged prompt/workflow system. The orchestrator selects the correct source prompt and verified runtime verbatim prompt mirror, gathers the required inputs, delegates generation to the owning skill, normalizes the output to Markdown, exports contract-compatible TSV/Excel-style files when required, and runs review before handoff.

## Unsupported mode

Native/freeform agent generation outside selected prompt rules is unsupported.

## Source priority

1. User-requested Project/Squad/Epic scope and requested artifact.
2. source documents: specs, UI docs, test design, Excel/source files.
3. source prompt provenance and verified runtime prompt mirror in `prompts-verbatim/**`.
4. Output contracts and validators in `data/output-contracts/` and `scripts/`.

## Mandatory orchestration rules

- Select a source prompt and runtime verbatim prompt mirror before generation.
- Verify prompt mirror fidelity before generation.
- Gather mandatory inputs for the selected runtime prompt.
- If mandatory input is missing, ask the user or record an open question; do not improvise.
- Generate according to selected prompt rules and prohibitions.
- Normalize prompt output into Markdown source-of-truth.
- Treat TSV/Excel-style files as derived exports.
- Review every deliverable against prompt fidelity, source fidelity, traceability, and output contracts.

## Standard flow

```text
user request
-> orchestrator intake
-> request classification
-> runtime verbatim prompt selection and verification
-> prompt-required input gathering
-> prompt-compatible generation
-> markdown normalization
-> TSV/Excel-style export
-> output review
-> handoff
```
