#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import email
from email import policy
from html.parser import HTMLParser
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "office_rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "ppt": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "draw": "http://schemas.openxmlformats.org/drawingml/2006/main",
}


def load_manifest(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text)
    except ImportError:
        return json.loads(text)


def metadata_block(entry: dict) -> str:
    return "\n".join([
        "---",
        f"source_path: {entry['path']}",
        f"source_role: {entry['role']}",
        f"canonical_status: {entry['canonical_status']}",
        "redaction_status: unredacted",
        "---",
        "",
    ])


def normalized_path(output: Path, source_path: str, suffix: str = ".md") -> Path:
    rel = Path(source_path)
    name = rel.name
    if rel.suffix:
        name = name[: -len(rel.suffix)] + suffix
    else:
        name = name + suffix
    return output / rel.parent / name


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def normalize_entry(source_root: Path, output: Path, entry: dict) -> list[dict]:
    source_file = source_root / entry["path"]
    ext = source_file.suffix.lower()
    if ext in {".txt", ".md"}:
        target = normalized_path(output, entry["path"])
        body = source_file.read_text(encoding="utf-8", errors="replace")
        write_text(target, metadata_block(entry) + body)
        return [{"source_path": entry["path"], "output_path": str(target), "status": "converted", "strategy": "text"}]
    if ext == ".doc":
        target = normalized_path(output, entry["path"])
        body = doc_to_markdown(source_file)
        write_text(target, metadata_block(entry) + body)
        return [{"source_path": entry["path"], "output_path": str(target), "status": "converted", "strategy": "mhtml_doc"}]
    if ext == ".xlsx":
        target = normalized_path(output, entry["path"])
        profile, snapshots = xlsx_to_profile(source_file, output, entry)
        write_text(target, metadata_block(entry) + profile)
        results = [{"source_path": entry["path"], "output_path": str(target), "status": "converted", "strategy": "xlsx_profile"}]
        results.extend(snapshots)
        return results
    if ext == ".pptx":
        target = normalized_path(output, entry["path"])
        body = pptx_to_markdown(source_file)
        write_text(target, metadata_block(entry) + body)
        return [{"source_path": entry["path"], "output_path": str(target), "status": "converted", "strategy": "pptx_text"}]
    if ext == ".pdf":
        target = normalized_path(output, entry["path"])
        body = pdf_report(source_file)
        write_text(target, metadata_block(entry) + body)
        return [{"source_path": entry["path"], "output_path": str(target), "status": "reported", "strategy": "pdf_report"}]
    target = normalized_path(output, entry["path"])
    write_text(target, metadata_block(entry) + f"# Conversion report\n\nNo converter is configured for `{ext or '[no extension]'}`.\n")
    return [{"source_path": entry["path"], "output_path": str(target), "status": "reported", "strategy": "unsupported_extension"}]


class SimpleHTMLToMarkdown(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.heading_level: int | None = None
        self.in_cell = False
        self.current_cell: list[str] = []
        self.current_row: list[str] = []
        self.rows: list[list[str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.heading_level = int(tag[1])
            self.parts.append("\n" + "#" * self.heading_level + " ")
        elif tag in {"p", "div"}:
            self.parts.append("\n")
        elif tag in {"br"}:
            self.parts.append("\n")
        elif tag == "tr":
            self.current_row = []
        elif tag in {"td", "th"}:
            self.in_cell = True
            self.current_cell = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.parts.append("\n")
            self.heading_level = None
        elif tag in {"td", "th"}:
            self.in_cell = False
            self.current_row.append(clean_inline("".join(self.current_cell)))
        elif tag == "tr" and self.current_row:
            self.rows.append(self.current_row)
        elif tag == "table" and self.rows:
            self.parts.append("\n" + table_to_markdown(self.rows) + "\n")
            self.rows = []
        elif tag in {"p", "div"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.current_cell.append(data)
        else:
            self.parts.append(data)

    def markdown(self) -> str:
        text = "".join(self.parts)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"


def clean_inline(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def table_to_markdown(rows: list[list[str]]) -> str:
    width = max(len(row) for row in rows)
    padded = [row + [""] * (width - len(row)) for row in rows]
    header = padded[0]
    lines = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * width) + " |"]
    for row in padded[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def doc_to_markdown(path: Path) -> str:
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    if "Content-Type:" in text[:500] or "MIME-Version:" in text[:500]:
        msg = email.message_from_bytes(raw, policy=policy.default)
        html_parts = []
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type in {"text/html", "text/plain"}:
                    html_parts.append(part_content(part))
        else:
            html_parts.append(part_content(msg))
        text = "\n".join(str(part) for part in html_parts)
    parser = SimpleHTMLToMarkdown()
    parser.feed(text)
    markdown = parser.markdown()
    if markdown.strip():
        return markdown
    return text.strip() + "\n"


def part_content(part: email.message.EmailMessage) -> str:
    try:
        return str(part.get_content())
    except LookupError:
        payload = part.get_payload(decode=True)
        if isinstance(payload, bytes):
            return payload.decode("utf-8", errors="replace")
        return str(part.get_payload())


def xlsx_to_profile(path: Path, output: Path, entry: dict) -> tuple[str, list[dict]]:
    lines = [f"# Workbook profile: {path.name}", ""]
    snapshots: list[dict] = []
    with zipfile.ZipFile(path) as z:
        shared = read_shared_strings(z)
        formulas_by_sheet = read_formulas(z)
        for sheet_name, sheet_path in workbook_sheets(z):
            rows = read_sheet_rows(z, sheet_path, shared)
            non_empty = [row for row in rows if any(cell.strip() for cell in row)]
            header = next((row for row in non_empty if any(cell.strip() for cell in row)), [])
            formulas = formulas_by_sheet.get(sheet_path, [])
            statuses = sorted({cell for row in rows for cell in row if looks_like_status(cell)})
            lines.extend([
                f"## Sheet: {sheet_name}",
                "",
                f"- Row count: {len(non_empty)}",
                f"- Column count: {max((len(row) for row in rows), default=0)}",
                f"- Headers: {', '.join(header)}" if header else "- Headers: [none detected]",
                f"- Status values: {', '.join(statuses)}" if statuses else "- Status values: [none detected]",
                "- Formulas:",
            ])
            if formulas:
                lines.extend(f"  - {formula}" for formula in formulas)
            else:
                lines.append("  - [none detected]")
            lines.append("")
            if non_empty:
                snapshot = write_sheet_snapshot(output, entry["path"], sheet_name, non_empty[:50])
                snapshots.append({"source_path": entry["path"], "output_path": str(snapshot), "status": "converted", "strategy": "xlsx_sheet_tsv", "sheet": sheet_name})
    return "\n".join(lines).rstrip() + "\n", snapshots


def read_shared_strings(z: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    values = []
    for item in root.findall("main:si", NS):
        values.append("".join(text.text or "" for text in item.findall(".//main:t", NS)))
    return values


def workbook_sheets(z: zipfile.ZipFile) -> list[tuple[str, str]]:
    workbook = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rel_by_id = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels.findall("rel:Relationship", NS)}
    sheets = []
    for sheet in workbook.findall(".//main:sheets/main:sheet", NS):
        rel_id = sheet.attrib.get(f"{{{NS['office_rel']}}}id")
        target = rel_by_id.get(rel_id or "", "")
        clean_target = target.lstrip("/")
        sheet_path = clean_target if clean_target.startswith("xl/") else "xl/" + clean_target
        sheets.append((sheet.attrib.get("name", "Sheet"), sheet_path))
    return sheets


def read_sheet_rows(z: zipfile.ZipFile, sheet_path: str, shared: list[str]) -> list[list[str]]:
    root = ET.fromstring(z.read(sheet_path))
    rows = []
    for row_node in root.findall(".//main:sheetData/main:row", NS):
        row = []
        current_col = 1
        for cell_node in row_node.findall("main:c", NS):
            col_idx = column_index(cell_node.attrib.get("r", "")) or current_col
            while current_col < col_idx:
                row.append("")
                current_col += 1
            row.append(cell_value(cell_node, shared))
            current_col += 1
        rows.append(row)
    return rows


def column_index(ref: str) -> int | None:
    match = re.match(r"([A-Z]+)", ref.upper())
    if not match:
        return None
    index = 0
    for char in match.group(1):
        index = index * 26 + ord(char) - 64
    return index


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


def read_formulas(z: zipfile.ZipFile) -> dict[str, list[str]]:
    formulas = {}
    for name in z.namelist():
        if not name.startswith("xl/worksheets/") or not name.endswith(".xml"):
            continue
        root = ET.fromstring(z.read(name))
        sheet_formulas = []
        for cell_node in root.findall(".//main:c", NS):
            formula_node = cell_node.find("main:f", NS)
            if formula_node is not None and formula_node.text:
                sheet_formulas.append(f"{cell_node.attrib.get('r', '')}: ={formula_node.text}")
        formulas[name] = sheet_formulas
    return formulas


def looks_like_status(value: str) -> bool:
    normalized = value.strip().lower()
    known = {"ready to uat", "read to uat", "pending", "in-test", "completed", "in-progress", "in - progress", "ai gen", "manual", "api", "ui", "web ui", "pass", "fail", "untested"}
    return normalized in known


def write_sheet_snapshot(output: Path, source_path: str, sheet_name: str, rows: list[list[str]]) -> Path:
    rel = Path(source_path)
    safe_sheet = re.sub(r"[^A-Za-z0-9_.-]+", "_", sheet_name).strip("_") or "Sheet"
    target = output / rel.parent / f"{rel.stem}.{safe_sheet}.tsv"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)
    return target


def pptx_to_markdown(path: Path) -> str:
    lines = [f"# Slide deck profile: {path.name}", ""]
    with zipfile.ZipFile(path) as z:
        slides = sorted(name for name in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml", name))
        for idx, slide in enumerate(slides, start=1):
            root = ET.fromstring(z.read(slide))
            texts = [node.text or "" for node in root.findall(".//draw:t", NS)]
            lines.extend([f"## Slide {idx}", "", "\n".join(texts).strip() or "[no text detected]", ""])
    return "\n".join(lines).rstrip() + "\n"


def pdf_report(path: Path) -> str:
    return f"# PDF conversion report: {path.name}\n\nPDF text extraction is not available in the default runtime. Preserve this source for a converter-backed pass.\n"


def normalize_manifest(manifest_path: Path, output: Path, source_root: Path | None = None) -> dict:
    manifest = load_manifest(manifest_path)
    root = source_root or Path(manifest.get("source_root", manifest_path.parent))
    results = []
    for entry in manifest.get("sources", []):
        results.extend(normalize_entry(root, output, entry))
    return {"status": "success", "total_sources": len(manifest.get("sources", [])), "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize sources into Markdown/TSV profiles")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    report = normalize_manifest(args.manifest, args.output, args.source_root)
    if args.report:
        write_text(args.report, json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({"status": report["status"], "total_sources": report["total_sources"], "outputs": len(report["results"]), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
