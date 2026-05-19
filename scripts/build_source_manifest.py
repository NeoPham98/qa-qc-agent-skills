#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

ROLE_NAMES = {
    "api_prompt",
    "ui_prompt",
    "template",
    "pdf_spec",
    "xlsx_tracker",
    "xlsx_testcase",
    "pptx_workshop",
    "automation_scaffold",
    "sensitive_config",
    "legacy_prompt",
    "unknown",
}

CANONICAL_API_PROMPTS = {
    "Prompt/API/API_TD_1_Setup_Context.txt",
    "Prompt/API/API_TD_2_Method_Header_BreakDown.txt",
    "Prompt/API/API_TD_3_Schema_Validation_BreakDown.txt",
    "Prompt/API/API_TD_4_Value_Business_Cross_Logic_BreakDown.txt",
    "Prompt/API/API_Gen_TC_From_TD_v2.txt",
    "Prompt/API/Gen Script/API_TestCase_Analysis.txt",
    "Prompt/API/Gen Script/API_Gen_Script_Method_Header_Validation_Feature.txt",
    "Prompt/API/Gen Script/API_Gen_Script_Validation_Feature.txt",
    "Prompt/API/Gen Script/API_Gen_Script_Logic_Business_Feature.txt",
}

CANONICAL_UI_PROMPTS = {
    "UI/UI_Gen_TD.txt",
    "UI/UI_Gen_TC_From_TD.txt",
    "UI/UI_Gen_TC_For_UAT.txt",
    "Prompt/UI/UI_Gen_TD.txt",
    "Prompt/UI/UI_Gen_TC_From_TD.txt",
    "Prompt/UI/UI_Gen_TC_For_UAT.txt",
}

CONTROL_SOURCES = {
    "Prompt/API/API_NewParameterGuideline.xlsx",
}

TEMPLATE_SOURCES = {
    "template/Template_PTTK_AI.doc",
    "template/Template_PTTK_AI_ChiTiet_API.doc",
    "template/Template_RSD_AI.doc",
    "template/Template_RSD_ChiTiet_AI.doc",
}

SENSITIVE_SOURCES = {
    "Prompt/API/Gen Script/properties.txt",
}

IGNORED_NAMES = {".DS_Store", "Thumbs.db"}


@dataclass(frozen=True)
class SourceEntry:
    path: str
    extension: str
    role: str
    canonical_status: str
    sensitive: bool
    conversion_required: bool


def normalize_rel(path: Path) -> str:
    return path.as_posix()


def classify(relative_path: str) -> tuple[str, str, bool, bool]:
    lower = relative_path.lower()
    suffix = Path(relative_path).suffix.lower()
    sensitive = relative_path in SENSITIVE_SOURCES or "properties.txt" in lower

    if sensitive:
        return "sensitive_config", "sensitive_reference", True, True

    if relative_path in CANONICAL_API_PROMPTS:
        return "api_prompt", "canonical", False, True

    if relative_path in CANONICAL_UI_PROMPTS:
        return "ui_prompt", "canonical", False, True

    if relative_path in CONTROL_SOURCES:
        return "api_prompt", "control_source", False, True

    if relative_path in TEMPLATE_SOURCES:
        return "template", "canonical", False, True

    if "/[old]_" in f"/{lower}" or "\\[old]_" in lower or "[old]_" in lower:
        return "legacy_prompt", "legacy_reference", False, True

    if lower.startswith("prompt/api/"):
        return "api_prompt", "reference", False, suffix in {".txt", ".docx", ".xlsx"}

    if lower.startswith("prompt/ui/") or lower.startswith("ui/"):
        return "ui_prompt", "reference", False, suffix in {".txt", ".docx", ".xlsx"}

    if lower.startswith("api_automation/"):
        return "automation_scaffold", "reference", False, suffix in {".py", ".md", ".txt", ".json", ".yml", ".yaml"}

    if lower.endswith(".pptx"):
        return "pptx_workshop", "reference", False, True

    if suffix == ".pdf":
        return "pdf_spec", "business_source", False, True

    if suffix == ".xlsx":
        if "tổng hợp trạng thái test case paygates" in lower:
            return "xlsx_tracker", "canonical", False, True
        if lower.endswith("-tcs.xlsx") or "testcase" in lower or "test case" in lower:
            return "xlsx_testcase", "schema_evidence", False, True
        return "xlsx_tracker", "reference", False, True

    if suffix == ".doc":
        return "template", "reference", False, True

    return "unknown", "reference", False, suffix in {".txt", ".md", ".doc", ".docx", ".pdf", ".xlsx", ".pptx"}


def iter_files(source: Path) -> Iterable[Path]:
    for path in sorted(source.rglob("*")):
        if path.is_file() and path.name not in IGNORED_NAMES:
            yield path


def build_manifest(source: Path) -> dict:
    entries: list[SourceEntry] = []
    for path in iter_files(source):
        relative = normalize_rel(path.relative_to(source))
        role, canonical_status, sensitive, conversion_required = classify(relative)
        if role not in ROLE_NAMES:
            role = "unknown"
        entries.append(SourceEntry(
            path=relative,
            extension=path.suffix.lower(),
            role=role,
            canonical_status=canonical_status,
            sensitive=sensitive,
            conversion_required=conversion_required,
        ))
    return {
        "schema_version": "1.0",
        "source_root": str(source),
        "total_files": len(entries),
        "roles": sorted(ROLE_NAMES),
        "sources": [asdict(entry) for entry in entries],
    }


def write_manifest(data: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        import yaml  # type: ignore
        output.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    except ImportError:
        output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build source inventory manifest")
    parser.add_argument("--source", type=Path, default=ROOT.parent / "QC")
    parser.add_argument("--output", type=Path, default=ROOT / "knowledge" / "default" / "manifests" / "source-manifest.yml")
    args = parser.parse_args()

    source = args.source.resolve()
    if not source.exists() or not source.is_dir():
        raise SystemExit(f"source directory not found: {source}")

    data = build_manifest(source)
    write_manifest(data, args.output)
    unknown_count = sum(1 for entry in data["sources"] if entry["role"] == "unknown")
    print(json.dumps({"status": "success", "total_files": data["total_files"], "unknown_files": unknown_count, "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
