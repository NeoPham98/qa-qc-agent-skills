---
name: api-automation-support-generate
description: Generates API automation support artifacts through BIDV API automation runtime verbatim prompts with deterministic analysis and Gherkin validation.
role_affinity: [automation_engineer, tester]
domain: [api, automation, bidv]
lifecycle_stage: [automation_support]
produces: [md, automation_support]
consumes: [testcase, runtime_verbatim_prompt, automation_context]
maturity: beta
tier: 2
languages: [vi, en]
---

# BIDV API Automation Support Generate

## Operating mode

This skill is invoked only inside **Prompt-Compatible Orchestration Mode**. Native/freeform automation generation outside selected automation prompt rules is unsupported, and runtime output must not require a raw `BIDV/` folder path.

## Selection criteria

Use this skill when API testcase analysis or automation support artifacts are requested.

## Prompt compatibility

Owned BIDV source/runtime prompt mapping:

- `BIDV/Prompt/API/Gen Script/API_TestCase_Analysis.txt` -> `prompts-verbatim/API/Gen Script/API_TestCase_Analysis.txt`
- `BIDV/Prompt/API/Gen Script/API_Gen_Script_Validation_Feature.txt` -> `prompts-verbatim/API/Gen Script/API_Gen_Script_Validation_Feature.txt`
- `BIDV/Prompt/API/Gen Script/API_Gen_Script_Method_Header_Validation_Feature.txt` -> `prompts-verbatim/API/Gen Script/API_Gen_Script_Method_Header_Validation_Feature.txt`
- `BIDV/Prompt/API/Gen Script/API_Gen_Script_Logic_Business_Feature.txt` -> `prompts-verbatim/API/Gen Script/API_Gen_Script_Logic_Business_Feature.txt`

Runtime execution must load the `Runtime Verbatim Prompt` from `../../data/source-inventory/prompt_fragment_registry.md`. Files under `prompts/*.md` are non-runtime notes unless verified as content-equivalent to the source prompt.

## Required inputs

- API testcase source.
- Automation scope.
- Project automation framework/context.
- Source BIDV prompt path.
- Runtime verbatim prompt path.
- Prompt mirror verification result.

## Workflow

1. Receive selected automation runtime verbatim prompt from orchestrator.
2. Verify prompt mirror fidelity before generation.
3. If request is full API automation support, enforce sequence:
   - testcase analysis runtime verbatim prompt
   - method/header feature runtime verbatim prompt
   - schema validation feature runtime verbatim prompt
   - logic/business feature runtime verbatim prompt
3. Verify testcase and framework inputs.
4. For testcase analysis, classify 100% testcase IDs into exactly one main component and output only the contract table.
5. For script generation fragments, filter testcase IDs by phase scope only:
   - Method/Header -> `TD_P1_*`
   - Schema Validation -> `TD_P2_*`
   - Value/Business/Cross Logic -> `TD_P3_*`
6. Generate automation support artifact according to selected BIDV runtime verbatim prompt rules/prohibitions.
7. Normalize to Markdown or project-specific automation artifact format.
9. Validate `API_TestCase_Analysis.md` with `scripts/validate_api_automation_analysis.py`.
10. Validate phase-specific `.feature` outputs with `scripts/validate_api_automation_feature.py`.
11. Send output to review.

## Outputs

- `API_TestCase_Analysis.md` table artifact.
- `api_method_header_validation.feature` for `TD_P1_*` cases.
- `api_validation.feature` for `TD_P2_*` cases.
- `api_logic_business.feature` for `TD_P3_*` cases.

## Hard-fail conditions

Any item below must force automation-support decision to `FAIL`:

1. Script generation is executed without testcase analysis when full support flow is requested.
2. Method/Header, Schema, and Logic/Business script outputs are mixed without phase filter (`TD_P1`/`TD_P2`/`TD_P3`).
3. A script fragment includes testcase IDs outside its allowed phase subset.
4. Output contains invented payload/response field names/SQL schema details not present in testcase/source docs.
5. Output contract violation: extra explanation outside required single table (analysis) or invalid Gherkin feature shape (script fragments).
6. Runtime output references raw BIDV paths.
7. Placeholder-only values such as `valid data`, `invalid data`, `TODO`, `TBD`, `như trên`, or `tương tự` appear where concrete values are expected.

## Review gates

- Selected automation prompt fidelity.
- Sequence fidelity: analysis before script generation for full flow.
- Phase-filter fidelity (`TD_P1`, `TD_P2`, `TD_P3`).
- Testcase traceability preserved.
- No unsupported framework assumptions.
- No cross-component leakage across runtime prompt phases.
