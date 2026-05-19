from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_source_manifest import build_manifest, classify


def touch(path: Path, content: str = "sample") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_classifies_known_sources() -> None:
    assert classify("Prompt/API/API_TD_1_Setup_Context.txt") == ("api_prompt", "canonical", False, True)
    assert classify("Prompt/API/[Old]_API_Gen_TC_From_TD.txt") == ("legacy_prompt", "legacy_reference", False, True)
    assert classify("Prompt/API/Gen Script/properties.txt") == ("sensitive_config", "sensitive_reference", True, True)
    assert classify("UI/UI_Gen_TD.txt") == ("ui_prompt", "canonical", False, True)
    assert classify("template/Template_RSD_AI.doc") == ("template", "canonical", False, True)
    assert classify("Tổng hợp Trạng Thái Test Case Paygates (1).xlsx") == ("xlsx_tracker", "canonical", False, True)
    assert classify("Faker_upd/PTTK/1/NMS-[KH-660] API check điều kiện KH-tcs.xlsx") == ("xlsx_testcase", "schema_evidence", False, True)
    assert classify("Prompt/Side Workshop/Workshop Hướng dẫn sử dụng AI sinh test case.pptx") == ("pptx_workshop", "reference", False, True)
    assert classify("api_automation/nms_sdk/endpoints.py") == ("automation_scaffold", "reference", False, True)


def test_build_manifest_includes_all_fixture_files(tmp_path: Path) -> None:
    touch(tmp_path / "Prompt" / "API" / "API_TD_1_Setup_Context.txt")
    touch(tmp_path / "Prompt" / "API" / "[Old]_API_Gen_TD_v1.2.txt")
    touch(tmp_path / "Prompt" / "API" / "Gen Script" / "properties.txt", "token=secret")
    touch(tmp_path / "Prompt" / "UI" / "UI_Gen_TC_For_UAT.txt")
    touch(tmp_path / "template" / "Template_PTTK_AI.doc")
    touch(tmp_path / "Tổng hợp Trạng Thái Test Case Paygates (1).xlsx")
    touch(tmp_path / "api_automation" / "README.md")
    touch(tmp_path / "unknown.bin")
    touch(tmp_path / ".DS_Store")

    manifest = build_manifest(tmp_path)
    entries = {entry["path"]: entry for entry in manifest["sources"]}

    assert manifest["total_files"] == 8
    assert entries["Prompt/API/API_TD_1_Setup_Context.txt"]["canonical_status"] == "canonical"
    assert entries["Prompt/API/[Old]_API_Gen_TD_v1.2.txt"]["canonical_status"] == "legacy_reference"
    assert entries["Prompt/API/Gen Script/properties.txt"]["sensitive"] is True
    assert entries["unknown.bin"]["role"] == "unknown"
