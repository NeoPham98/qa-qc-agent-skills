from __future__ import annotations

import html
import zipfile
from pathlib import Path


def write_xlsx(headers: list[str], rows: list[list[str]], output: Path, sheet_name: str = "Sheet1") -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("xl/workbook.xml", workbook_xml(sheet_name))
        z.writestr("xl/_rels/workbook.xml.rels", WORKBOOK_RELS)
        z.writestr("xl/styles.xml", STYLES)
        z.writestr("xl/worksheets/sheet1.xml", sheet_xml(headers, rows))


def col_name(index: int) -> str:
    name = ""
    while index:
        index, rem = divmod(index - 1, 26)
        name = chr(65 + rem) + name
    return name


def cell(ref: str, value: str, style: int = 0) -> str:
    escaped = html.escape(value or "")
    return f'<c r="{ref}" t="inlineStr" s="{style}"><is><t>{escaped}</t></is></c>'


def workbook_xml(sheet_name: str) -> str:
    escaped = html.escape(sheet_name[:31] or "Sheet1", quote=True)
    return XML_DECL + f'<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="{escaped}" sheetId="1" r:id="rId1"/></sheets></workbook>'


def sheet_xml(headers: list[str], rows: list[list[str]]) -> str:
    sheet_rows = []
    header_cells = [cell(f"{col_name(i)}1", value, 1) for i, value in enumerate(headers, start=1)]
    sheet_rows.append(f'<row r="1">{"".join(header_cells)}</row>')
    for r_idx, row in enumerate(rows, start=2):
        cells = [cell(f"{col_name(c_idx)}{r_idx}", value) for c_idx, value in enumerate(row, start=1)]
        sheet_rows.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
    return XML_DECL + f'<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>{"".join(sheet_rows)}</sheetData></worksheet>'


XML_DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
CONTENT_TYPES = XML_DECL + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>'
RELS = XML_DECL + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'
WORKBOOK = XML_DECL + '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Paygates Dashboard" sheetId="1" r:id="rId1"/></sheets></workbook>'
WORKBOOK_RELS = XML_DECL + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'
STYLES = XML_DECL + '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="11"/><name val="Arial"/></font><font><b/><sz val="11"/><name val="Arial"/></font></fonts><fills count="1"><fill><patternFill patternType="none"/></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0"/></cellXfs></styleSheet>'
