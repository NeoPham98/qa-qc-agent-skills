# Source Inventory

This inventory is used by Prompt-Compatible Orchestration Mode. For detailed routing, use `prompt_fragment_registry.md`.

| Source path | Type | Priority | Runtime prompt / non-runtime reference | Used by | Trigger / required docs | Notes |
|---|---|---:|---|---|---|---|
| `BIDV/Prompt/API/API_TD_1_Setup_Context.txt` | API TD prompt | 2 | `prompts-verbatim/API/API_TD_1_Setup_Context.txt` | `api-td-generate` | API TD setup context, API spec | Setup context; `.md` wrappers are non-runtime notes |
| `BIDV/Prompt/API/API_TD_2_Method_Header.txt` | API TD prompt | 2 | `prompts-verbatim/API/API_TD_2_Method_Header.txt` | `api-td-generate` | Method/header/auth details | Method/header conditions; `.md` wrappers are non-runtime notes |
| `BIDV/Prompt/API/API_TD_3_Schema_Validation.txt` | API TD prompt | 2 | `prompts-verbatim/API/API_TD_3_Schema_Validation.txt` | `api-td-generate` | Request schema and constraints | Schema validation; `.md` wrappers are non-runtime notes |
| `BIDV/Prompt/API/API_TD_4_Value_Business_Cross_Logic.txt` | API TD prompt | 2 | `prompts-verbatim/API/API_TD_4_Value_Business_Cross_Logic.txt` | `api-td-generate` | Business rules, values, states | Value/business/cross logic; `.md` wrappers are non-runtime notes |
| `BIDV/Prompt/API/API_Gen_TC_From_TD_v2.txt` | API TC prompt | 2 | `prompts-verbatim/API/API_Gen_TC_From_TD_v2.txt` | `tc-generate-from-td` | API TD, API spec, endpoint/schema/error data | Legacy 19-column testcase; `.md` wrappers are non-runtime notes |
| `BIDV/Prompt/UI/UI_Gen_TD.txt` | UI TD prompt | 2 | `prompts-verbatim/UI/UI_Gen_TD.txt` | `ui-td-generate` | UI/RSD/PTTK source | UI Test Design; `.md` wrappers are non-runtime notes |
| `BIDV/Prompt/UI/UI_Gen_TC_From_TD.txt` | UI TC prompt | 2 | `prompts-verbatim/UI/UI_Gen_TC_From_TD.txt` | `tc-generate-from-td` | UI TD, UI/RSD/PTTK source | Legacy 19-column testcase; `.md` wrappers are non-runtime notes |
| `BIDV/Prompt/UI/UI_Gen_TC_For_UAT.txt` | UAT TC prompt | 2 | `prompts-verbatim/UI/UI_Gen_TC_For_UAT.txt` | `uat-tc-generate` | URD/business source | UAT 16-column testcase; `.md` wrappers are non-runtime notes |
| `BIDV/Prompt/API/Gen Script/*.txt` | Automation support prompts | 2 | `prompts-verbatim/API/Gen Script/*.txt` | `api-automation-support-generate` | API testcase source and automation framework context | Feature/spec skeleton; `.md` wrappers are non-runtime notes |
| `BIDV/template/*.doc*` | Template docs | 3 | `data/output-contracts/markdown_normalization_rules.md` | normalizer, planner | Format/reference docs | Reference format only |
| `BIDV/*.xlsx` | Sample workbook | 3 | output contracts and validators | output contract, export validation | Baseline workbook/output samples | Format/reference only unless user requests comparison |
| `BIDV/NMS-Đặc tả API cho SDK-170326-075931.pdf` | API spec | 1 | selected by request scope | API TD/TC route | API source doc | Candidate example input |
