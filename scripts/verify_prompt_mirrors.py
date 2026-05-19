#!/usr/bin/env python3
"""Verify runtime prompt mirrors match source prompts exactly."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
MANIFEST = ROOT / "data" / "source-inventory" / "prompt_mirror_manifest.json"


def resolve_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    if path.parts and path.parts[0] in {"BIDV", "QC"}:
        return WORKSPACE / path
    return ROOT / path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()

    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors: list[str] = []
    for entry in data.get("prompts", []):
        source = resolve_path(entry["source_path"])
        runtime = resolve_path(entry["runtime_prompt_path"])
        if not source.exists():
            errors.append(f"missing source: {source}")
            continue
        if not runtime.exists():
            errors.append(f"missing runtime mirror: {runtime}")
            continue
        source_hash = sha256(source)
        runtime_hash = sha256(runtime)
        if source_hash != runtime_hash:
            errors.append(f"mirror drift: {entry['request_type']} source={source_hash} runtime={runtime_hash}")
        expected_hash = entry.get("sha256")
        if expected_hash and expected_hash != source_hash:
            errors.append(f"manifest hash stale: {entry['request_type']} manifest={expected_hash} source={source_hash}")

    if errors:
        print("prompt mirror verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"prompt mirror verification passed ({len(data.get('prompts', []))} prompts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
