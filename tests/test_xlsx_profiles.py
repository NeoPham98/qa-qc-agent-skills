from __future__ import annotations

from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

from extract_xlsx_profiles import normalize_header, profile_workbook
from minimal_xlsx import XML_DECL, CONTENT_TYPES, RELS, STYLES, col_name, workbook_xml, cell


def write_fixture_xlsx(path: Path, headers: list[str], rows: list[list[str]], formula: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    width = max(len(headers), *(len(row) for row in rows))
    header_cells = [cell(f"{col_name(i)}1", headers[i - 1], 1) for i in range(1, len(headers) + 1)]
    sheet_rows = [f'<row r="1">{"".join(header_cells)}</row>']
    for r_idx, row in enumerate(rows, start=2):
        cells = [cell(f"{col_name(c_idx)}{r_idx}", value) for c_idx, value in enumerate(row, start=1)]
        sheet_rows.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
    if formula:
        sheet_rows.append(f'<row r="10"><c r="A10"><f>{formula}</f><v>1</v></c></row>')
    sheet_xml = XML_DECL + f'<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>{"".join(sheet_rows)}</sheetData></worksheet>'
    workbook_rels = XML_DECL + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("xl/workbook.xml", workbook_xml("Squad_VA"))
        z.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        z.writestr("xl/styles.xml", STYLES)
        z.writestr("xl/worksheets/sheet1.xml", sheet_xml)


def test_header_alias_normalization() -> None:
    assert normalize_header("Test Case / Summary") == "Test Case Summary"
    assert normalize_header("Expected / result") == "Expected result"
    assert normalize_header("Manual Test Results / Round 1") == "Manual Test Results Round 1"
    assert normalize_header("Notes ") == "Notes"


def test_profile_detects_overflow_header_alias_and_id_findings(tmp_path: Path) -> None:
    headers = [
        "Test Case ID",
        "Function",
        "Group Tests",
        "Scenario Outline",
        "Test Case / Summary",
        "Pre-conditions",
        "Test Data",
        "Test Steps",
        "Expected / result",
        "Environment",
        "Priority",
        "Regression",
        "Automation",
        "Manual Test Results / Round 1",
        "Manual Test Results Round 2",
        "Automation Test Results",
        "Actual result",
        "BugID",
        "Notes ",
    ] + [f"Overflow {idx}" for idx in range(1, 31)]
    rows = [[" TD_P1_001_TC_001 "] + ["sample"] * 48]
    workbook = tmp_path / "sample-tcs.xlsx"
    write_fixture_xlsx(workbook, headers, rows)

    profile = profile_workbook(workbook)
    sheet = profile["sheets"][0]

    assert profile["workbook_type"] == "legacy_testcase"
    assert sheet["normalized_headers"][:19][4] == "Test Case Summary"
    assert sheet["normalized_headers"][:19][8] == "Expected result"
    assert sheet["overflow_columns"] == 30
    assert {alias["source"] for alias in sheet["header_aliases"]} >= {"Test Case / Summary", "Expected / result", "Manual Test Results / Round 1", "Notes ", "Test Data"}
    assert any(finding["type"] == "leading_or_trailing_space" for finding in sheet["id_findings"])


def test_profile_detects_status_aliases_and_formula_warning(tmp_path: Path) -> None:
    workbook = tmp_path / "Tổng hợp Trạng Thái Test Case Paygates (1).xlsx"
    write_fixture_xlsx(
        workbook,
        ["Feature", "Status", "Generate Type", "Automation Status", "Automation Type"],
        [["VA", "Read to UAT", "AI Gen", "In - Progress", "UI"]],
        "SUMIFS(Squad_VA!A:A,Squad_CnR!B:B,\"Ready\")",
    )

    profile = profile_workbook(workbook)
    sheet = profile["sheets"][0]

    assert profile["workbook_type"] == "paygates_tracker"
    assert {item["source"] for item in sheet["status_aliases"]} >= {"Read to UAT", "AI Gen", "In - Progress", "UI"}
    assert profile["formula_warnings"]
