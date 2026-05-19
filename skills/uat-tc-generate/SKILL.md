---
name: uat-tc-generate
description: Generates BIDV UAT testcase artifacts through the BIDV UAT runtime verbatim prompt.
role_affinity: [ba, tester, qa_lead]
domain: [uat, testing, bidv]
lifecycle_stage: [testcase_authoring]
produces: [md, uat_testcase, tsv]
consumes: [urd, business_docs, runtime_verbatim_prompt]
maturity: draft
tier: 1
languages: [vi, en]
---

# BIDV UAT Testcase Generate

## Operating mode

This skill is invoked only inside **Prompt-Compatible Orchestration Mode**. Native/freeform UAT testcase generation outside selected BIDV UAT prompt rules is unsupported.

## Selection criteria

Use this skill when generating UAT/business-facing testcase artifacts.

## Prompt compatibility

Owned BIDV source/runtime prompt mapping:

- `BIDV/Prompt/UI/UI_Gen_TC_For_UAT.txt` -> `prompts-verbatim/UI/UI_Gen_TC_For_UAT.txt`

Runtime execution must load the `Runtime Verbatim Prompt` from `../../data/source-inventory/prompt_fragment_registry.md`. Files under `prompts/*.md` are non-runtime notes unless verified as content-equivalent to the source prompt.

## Required inputs

- Project/Squad/Epic.
- URD/business source docs and UAT scope.
- Source BIDV prompt path.
- Runtime verbatim prompt path.
- Prompt mirror verification result.
- Expected UAT output contract.

## Workflow

1. Receive selected UAT runtime verbatim prompt from orchestrator.
2. Verify prompt mirror fidelity before generation.
3. Verify business/UAT inputs.
4. Generate UAT testcase according to BIDV UAT prompt rules.
5. Normalize to Markdown.
6. Export UAT 16-column TSV when required.
7. Send output to review.

## Outputs

- UAT TestCase Markdown.
- UAT 16-column TSV when required.

## Review gates

- UAT prompt fidelity.
- Business readability.
- 16-column contract compliance.
- No unsupported technical assumptions.
