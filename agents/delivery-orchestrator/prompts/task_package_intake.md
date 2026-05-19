# Task Package Intake

Collect enough information to select the correct prompt-compatible route before generation.

## Required intake fields

- Project
- Squad
- Epic
- Requested artifact
- Request type: API TD, UI TD, API TC, UI TC, UAT TC, Execution, Automation Support, Coverage, Review
- Source prompt path, if known
- Runtime verbatim prompt path
- Source business/spec/UI/test design files
- Required input checklist for the selected runtime prompt
- Missing input checklist
- Expected Markdown artifact
- Expected export contract: markdown only, legacy 19-column TSV, UAT 16-column TSV, execution TSV, XRAY/TestLink-style TSV, or both markdown and TSV
- Output folder
- Open assumptions/questions

## Intake rules

- Select a source prompt and runtime verbatim prompt using `data/source-inventory/prompt_fragment_registry.md` before generation.
- Verify the runtime prompt mirror matches the source prompt before generation.
- If the selected prompt requires an input that is missing, ask for it or record an open question.
- Do not generate native/freeform output outside the selected prompt rules.
- Keep source prompt path and runtime verbatim prompt path visible in downstream artifacts.
