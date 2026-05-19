#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source-inventory" / "prompt_mirror_manifest.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify packaged runtime BIDV prompt mirrors using manifest hashes")
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()

    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors: list[str] = []
    for entry in data.get("prompts", []):
        runtime = ROOT / entry["runtime_prompt_path"]
        if not runtime.exists():
            errors.append(f"missing runtime prompt: {runtime}")
            continue
        runtime_hash = sha256(runtime)
        if runtime_hash != entry.get("sha256"):
            errors.append(f"runtime prompt hash mismatch: {entry['request_type']} manifest={entry.get('sha256')} runtime={runtime_hash}")
        if entry.get("external_source_required_for_runtime", False):
            errors.append(f"runtime unexpectedly requires external source: {entry['request_type']}")
    if errors:
        print("BIDV runtime prompt manifest verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"BIDV runtime prompt manifest verification passed ({len(data.get('prompts', []))} prompts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
