#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

BIDV_PATH_RE = re.compile(r"(^|[\\/`\s])BIDV[\\/][^`\s]*", re.I)
DEFAULT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".txt", ".tsv", ".csv"}
PROVENANCE_PARTS = {"manifests", "normalized", "schemas"}
SUPPORT_ARTIFACT_NAMES = {
    "source_manifest.json",
    "route_plan.json",
    "validation_report.json",
    "handoff_summary.md",
    "closed-loop-state.json",
    "published-artifact-manifest.yml",
    "published-artifact-manifest.yaml",
}
ALLOWLIST_PHRASES = [
    "must not require or reference",
    "do not reference",
    "not any external raw sample folder",
    "raw `BIDV/`",
    "raw BIDV path",
]


def should_scan(path: Path, suffixes: set[str]) -> bool:
    return path.is_file() and path.suffix.lower() in suffixes


def is_provenance_path(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}
    return "knowledge" in parts and bool(parts & PROVENANCE_PARTS)


def is_support_artifact(path: Path) -> bool:
    return path.name in SUPPORT_ARTIFACT_NAMES


def validate(paths: list[Path], suffixes: set[str], include_provenance: bool = False) -> list[str]:
    errors: list[str] = []
    for root in paths:
        candidates = [root] if root.is_file() else [path for path in root.rglob("*") if should_scan(path, suffixes)]
        for path in candidates:
            if not should_scan(path, suffixes):
                continue
            if not include_provenance and (is_provenance_path(path) or is_support_artifact(path)):
                continue
            try:
                text = path.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError:
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                if BIDV_PATH_RE.search(line) and not any(phrase in line for phrase in ALLOWLIST_PHRASES):
                    errors.append(f"{path}:{line_no}: raw BIDV path reference is not allowed at runtime")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate runtime artifacts do not reference raw sample paths")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--suffix", action="append", default=[])
    parser.add_argument("--include-provenance", action="store_true", help="also scan bootstrap/provenance knowledge paths")
    args = parser.parse_args()

    suffixes = {suffix if suffix.startswith(".") else f".{suffix}" for suffix in args.suffix} or DEFAULT_SUFFIXES
    errors = validate(args.paths, suffixes, include_provenance=args.include_provenance)
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, ensure_ascii=True, indent=2))
        return 1
    print(json.dumps({"status": "passed", "paths": [str(path) for path in args.paths]}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
