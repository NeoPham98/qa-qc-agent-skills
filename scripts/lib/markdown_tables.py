from __future__ import annotations


def parse_markdown_table(text: str) -> list[dict[str, str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        rows.append([cell.strip() for cell in stripped.strip("|").split("|")])
    if not rows:
        return []
    header = rows[0]
    return [dict(zip(header, row)) for row in rows[1:] if len(row) == len(header)]
