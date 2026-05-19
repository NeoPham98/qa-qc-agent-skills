from __future__ import annotations

import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "office_rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def read_xlsx_table(path: Path, sheet_name: str | None = None) -> list[list[str]]:
    with zipfile.ZipFile(path) as z:
        shared = read_shared_strings(z)
        sheet_path = resolve_sheet_path(z, sheet_name)
        root = ET.fromstring(z.read(sheet_path))
    rows: list[list[str]] = []
    for row_node in root.findall(".//main:sheetData/main:row", NS):
        values: list[str] = []
        current_col = 1
        for cell_node in row_node.findall("main:c", NS):
            col_idx = column_index(cell_node.attrib.get("r", "")) or current_col
            while current_col < col_idx:
                values.append("")
                current_col += 1
            values.append(cell_value(cell_node, shared))
            current_col += 1
        rows.append(values)
    return trim_empty_rows(rows)


def read_shared_strings(z: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    values: list[str] = []
    for item in root.findall("main:si", NS):
        values.append("".join(text.text or "" for text in item.findall(".//main:t", NS)))
    return values


def resolve_sheet_path(z: zipfile.ZipFile, sheet_name: str | None) -> str:
    workbook = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rel_by_id = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels.findall("rel:Relationship", NS)}
    sheets = workbook.findall(".//main:sheets/main:sheet", NS)
    if not sheets:
        raise ValueError("workbook has no sheets")
    selected = sheets[0]
    if sheet_name:
        selected = next((sheet for sheet in sheets if sheet.attrib.get("name") == sheet_name), None)
        if selected is None:
            raise ValueError(f"sheet not found: {sheet_name}")
    rel_id = selected.attrib.get(f"{{{NS['office_rel']}}}id")
    target = rel_by_id.get(rel_id or "")
    if not target:
        raise ValueError("worksheet relationship not found")
    clean_target = target.lstrip("/")
    return clean_target if clean_target.startswith("xl/") else "xl/" + clean_target


def cell_value(cell_node: ET.Element, shared: list[str]) -> str:
    cell_type = cell_node.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(text.text or "" for text in cell_node.findall(".//main:t", NS))
    value_node = cell_node.find("main:v", NS)
    if value_node is None or value_node.text is None:
        return ""
    value = value_node.text
    if cell_type == "s":
        try:
            return shared[int(value)]
        except (ValueError, IndexError):
            return ""
    return value


def rows_to_dicts(rows: list[list[str]]) -> list[dict[str, str]]:
    header_index = next((idx for idx, row in enumerate(rows) if any(cell.strip() for cell in row)), None)
    if header_index is None:
        return []
    headers = [cell.strip() for cell in rows[header_index]]
    dicts: list[dict[str, str]] = []
    for row in rows[header_index + 1:]:
        padded = row + [""] * max(0, len(headers) - len(row))
        values = padded[: len(headers)]
        if any(cell.strip() for cell in values):
            dicts.append(dict(zip(headers, values)))
    return dicts


def column_index(ref: str) -> int | None:
    match = re.match(r"([A-Z]+)", ref.upper())
    if not match:
        return None
    index = 0
    for char in match.group(1):
        index = index * 26 + ord(char) - 64
    return index


def trim_empty_rows(rows: list[list[str]]) -> list[list[str]]:
    while rows and not any(cell.strip() for cell in rows[-1]):
        rows.pop()
    return rows
