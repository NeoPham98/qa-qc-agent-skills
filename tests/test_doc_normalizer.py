from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

from minimal_xlsx import write_xlsx
from normalize_docs import doc_to_markdown, normalize_entry, xlsx_to_profile


def test_txt_normalization_preserves_body_after_metadata(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    output = tmp_path / "out"
    source = source_root / "Prompt" / "API" / "API_TD_1_Setup_Context.txt"
    body = "Dòng 1\nDòng 2\n"
    source.parent.mkdir(parents=True)
    source.write_text(body, encoding="utf-8")
    entry = {
        "path": "Prompt/API/API_TD_1_Setup_Context.txt",
        "role": "api_prompt",
        "canonical_status": "canonical",
        "sensitive": False,
        "conversion_required": True,
    }

    normalize_entry(source_root, output, entry)
    normalized = (output / "Prompt" / "API" / "API_TD_1_Setup_Context.md").read_text(encoding="utf-8")

    assert normalized.startswith("---\nsource_path: Prompt/API/API_TD_1_Setup_Context.txt")
    assert normalized.split("---\n", 2)[2].lstrip("\n") == body


def test_mhtml_doc_conversion_preserves_headings_and_tables(tmp_path: Path) -> None:
    source = tmp_path / "Template_RSD_AI.doc"
    source.write_text(
        "MIME-Version: 1.0\nContent-Type: text/html; charset=utf-8\n\n"
        "<html><body><h1>RSD Template</h1><table><tr><th>Field</th><th>Value</th></tr>"
        "<tr><td>Actor</td><td>User</td></tr></table></body></html>",
        encoding="utf-8",
    )

    markdown = doc_to_markdown(source)

    assert "# RSD Template" in markdown
    assert "| Field | Value |" in markdown
    assert "| Actor | User |" in markdown


def test_xlsx_profile_includes_sheet_headers_statuses_and_snapshots(tmp_path: Path) -> None:
    source = tmp_path / "tracker.xlsx"
    output = tmp_path / "out"
    write_xlsx(["Test Case ID", "Status", "Notes"], [["TC_001", "Read to UAT", ""]], source, "Squad_VA")
    entry = {
        "path": "Tổng hợp Trạng Thái Test Case Paygates (1).xlsx",
        "role": "xlsx_tracker",
        "canonical_status": "canonical",
        "sensitive": False,
        "conversion_required": True,
    }

    profile, snapshots = xlsx_to_profile(source, output, entry)

    assert "## Sheet: Squad_VA" in profile
    assert "Headers: Test Case ID, Status, Notes" in profile
    assert "Status values: Read to UAT" in profile
    assert snapshots
    assert Path(snapshots[0]["output_path"]).exists()
