#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED_METADATA = [
    "source_path",
    "source_role",
    "canonical_status",
    "redaction_status",
]
ALLOWED_REDACTION_STATUS = {"unredacted", "redacted"}
RAW_SENSITIVE_PATTERNS = [
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}", re.IGNORECASE),
    re.compile(r"(?i)\b(password|passwd|pwd)\s*[:=]\s*[^\s;,&\]\)]+"),
    re.compile(r"(?i)\b(token|access_token|refresh_token|api_key|apikey|secret)\s*[:=]\s*[A-Za-z0-9._~+/=-]{12,}"),
]


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text
    metadata: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata, parts[2].lstrip("\n")


def validate_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    metadata, body = split_front_matter(text)
    errors: list[str] = []

    if not metadata:
        return [f"{path}: missing metadata front matter"]

    for key in REQUIRED_METADATA:
        if not metadata.get(key):
            errors.append(f"{path}: missing metadata field '{key}'")

    redaction_status = metadata.get("redaction_status", "")
    if redaction_status and redaction_status not in ALLOWED_REDACTION_STATUS:
        errors.append(f"{path}: unsupported redaction_status '{redaction_status}'")

    if not body.strip():
        errors.append(f"{path}: empty normalized body")

    if metadata.get("source_role") == "sensitive_config" and redaction_status != "redacted":
        errors.append(f"{path}: sensitive_config must be redacted before runtime use")

    if redaction_status == "redacted":
        for pattern in RAW_SENSITIVE_PATTERNS:
            for match in pattern.finditer(text):
                if "[REDACTED_" not in match.group(0):
                    errors.append(f"{path}: unredacted secret-like content remains")
                    break
            if errors and errors[-1].endswith("unredacted secret-like content remains"):
                break

    return errors


def validate_tree(input_dir: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(candidate for candidate in input_dir.rglob("*") if candidate.is_file() and candidate.suffix.lower() in {".md", ".txt"}):
        errors.extend(validate_file(path))
    if not errors and not any(path.is_file() for path in input_dir.rglob("*")):
        errors.append(f"{input_dir}: no files found")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate normalized/redacted BIDV knowledge metadata and secret safety")
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()

    if not args.input.exists() or not args.input.is_dir():
        raise SystemExit(f"input directory not found: {args.input}")

    errors = validate_tree(args.input)
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, ensure_ascii=True, indent=2))
        return 1
    print(json.dumps({"status": "passed", "input": str(args.input)}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
