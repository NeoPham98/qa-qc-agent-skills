#!/usr/bin/env python3
"""Mirror source prompts into prompts-verbatim."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
MANIFEST = ROOT / "data" / "source-inventory" / "prompt_mirror_manifest.json"

PROMPTS = [
    {
        "request_type": "API TD - Setup Context",
        "source_path": "BIDV/Prompt/API/API_TD_1_Setup_Context.txt",
        "runtime_prompt_path": "prompts-verbatim/API/API_TD_1_Setup_Context.txt",
        "owning_skill": "api-td-generate",
    },
    {
        "request_type": "API TD - Method/Header",
        "source_path": "BIDV/Prompt/API/API_TD_2_Method_Header.txt",
        "runtime_prompt_path": "prompts-verbatim/API/API_TD_2_Method_Header.txt",
        "owning_skill": "api-td-generate",
    },
    {
        "request_type": "API TD - Schema Validation",
        "source_path": "BIDV/Prompt/API/API_TD_3_Schema_Validation.txt",
        "runtime_prompt_path": "prompts-verbatim/API/API_TD_3_Schema_Validation.txt",
        "owning_skill": "api-td-generate",
    },
    {
        "request_type": "API TD - Value/Business/Cross Logic",
        "source_path": "BIDV/Prompt/API/API_TD_4_Value_Business_Cross_Logic.txt",
        "runtime_prompt_path": "prompts-verbatim/API/API_TD_4_Value_Business_Cross_Logic.txt",
        "owning_skill": "api-td-generate",
    },
    {
        "request_type": "API TD - Method/Header BreakDown",
        "source_path": "BIDV/Prompt/API/API_TD_2_Method_Header_BreakDown.txt",
        "runtime_prompt_path": "prompts-verbatim/API/API_TD_2_Method_Header_BreakDown.txt",
        "owning_skill": "api-td-generate",
    },
    {
        "request_type": "API TD - Schema Validation BreakDown",
        "source_path": "BIDV/Prompt/API/API_TD_3_Schema_Validation_BreakDown.txt",
        "runtime_prompt_path": "prompts-verbatim/API/API_TD_3_Schema_Validation_BreakDown.txt",
        "owning_skill": "api-td-generate",
    },
    {
        "request_type": "API TD - Value/Business/Cross Logic BreakDown",
        "source_path": "BIDV/Prompt/API/API_TD_4_Value_Business_Cross_Logic_BreakDown.txt",
        "runtime_prompt_path": "prompts-verbatim/API/API_TD_4_Value_Business_Cross_Logic_BreakDown.txt",
        "owning_skill": "api-td-generate",
    },
    {
        "request_type": "API TC from TD",
        "source_path": "BIDV/Prompt/API/API_Gen_TC_From_TD_v2.txt",
        "runtime_prompt_path": "prompts-verbatim/API/API_Gen_TC_From_TD_v2.txt",
        "owning_skill": "tc-generate-from-td",
    },
    {
        "request_type": "UI TD",
        "source_path": "BIDV/Prompt/UI/UI_Gen_TD.txt",
        "runtime_prompt_path": "prompts-verbatim/UI/UI_Gen_TD.txt",
        "owning_skill": "ui-td-generate",
    },
    {
        "request_type": "UI TC from TD",
        "source_path": "BIDV/Prompt/UI/UI_Gen_TC_From_TD.txt",
        "runtime_prompt_path": "prompts-verbatim/UI/UI_Gen_TC_From_TD.txt",
        "owning_skill": "tc-generate-from-td",
    },
    {
        "request_type": "UAT TC",
        "source_path": "BIDV/Prompt/UI/UI_Gen_TC_For_UAT.txt",
        "runtime_prompt_path": "prompts-verbatim/UI/UI_Gen_TC_For_UAT.txt",
        "owning_skill": "uat-tc-generate",
    },
    {
        "request_type": "API Testcase Analysis",
        "source_path": "BIDV/Prompt/API/Gen Script/API_TestCase_Analysis.txt",
        "runtime_prompt_path": "prompts-verbatim/API/Gen Script/API_TestCase_Analysis.txt",
        "owning_skill": "api-automation-support-generate",
    },
    {
        "request_type": "API Script Validation Feature",
        "source_path": "BIDV/Prompt/API/Gen Script/API_Gen_Script_Validation_Feature.txt",
        "runtime_prompt_path": "prompts-verbatim/API/Gen Script/API_Gen_Script_Validation_Feature.txt",
        "owning_skill": "api-automation-support-generate",
    },
    {
        "request_type": "API Script Method/Header Feature",
        "source_path": "BIDV/Prompt/API/Gen Script/API_Gen_Script_Method_Header_Validation_Feature.txt",
        "runtime_prompt_path": "prompts-verbatim/API/Gen Script/API_Gen_Script_Method_Header_Validation_Feature.txt",
        "owning_skill": "api-automation-support-generate",
    },
    {
        "request_type": "API Script Logic Business Feature",
        "source_path": "BIDV/Prompt/API/Gen Script/API_Gen_Script_Logic_Business_Feature.txt",
        "runtime_prompt_path": "prompts-verbatim/API/Gen Script/API_Gen_Script_Logic_Business_Feature.txt",
        "owning_skill": "api-automation-support-generate",
    },
]


def resolve_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    if path.parts and path.parts[0] in {"BIDV", "QC"}:
        return WORKSPACE / path
    return ROOT / path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    entries: list[dict[str, str]] = []
    for prompt in PROMPTS:
        source = resolve_path(prompt["source_path"])
        runtime = resolve_path(prompt["runtime_prompt_path"])
        if not source.exists():
            raise FileNotFoundError(source)
        runtime.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, runtime)
        entries.append({**prompt, "sha256": sha256(source)})

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps({"prompts": entries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Synced {len(entries)} BIDV prompts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
