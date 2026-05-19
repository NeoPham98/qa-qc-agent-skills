#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_APPROVED_FILES = [
    "OutputReview.md",
    "SupervisorApproval.md",
]
REQUIRED_APPROVED_KEYS = [
    "validation_report",
    "no_secret_report",
    "source_trace",
]
ALLOWED_DECISIONS = {"approved", "rejected", "retry_required"}


def load_manifest(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text)
    except ImportError:
        return json.loads(text)


def validate_manifest(path: Path) -> list[str]:
    manifest = load_manifest(path)
    errors: list[str] = []
    status = manifest.get("status") or manifest.get("lifecycle_state")
    if status != "approved":
        errors.append(f"{path}: manifest lifecycle_state/status must be approved for publish validation")

    files = manifest.get("files", {})
    for name in REQUIRED_APPROVED_FILES:
        if name not in files and name not in manifest:
            errors.append(f"{path}: missing required approved artifact '{name}'")

    for key in REQUIRED_APPROVED_KEYS:
        value = manifest.get(key) or files.get(key)
        if not value:
            errors.append(f"{path}: missing required evidence '{key}'")

    decision = manifest.get("supervisor_decision") or manifest.get("decision")
    if decision and decision not in ALLOWED_DECISIONS:
        errors.append(f"{path}: unsupported supervisor decision '{decision}'")
    if decision != "approved":
        errors.append(f"{path}: supervisor decision must be approved")

    approved_path = manifest.get("approved_artifact_path") or files.get("approved_artifact_path")
    previous_path = manifest.get("previous_approved_artifact_path") or files.get("previous_approved_artifact_path")
    if approved_path and previous_path and approved_path == previous_path:
        errors.append(f"{path}: approved artifact would overwrite existing approved artifact in place")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate approved artifact manifest")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    errors = validate_manifest(args.path)
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, ensure_ascii=True, indent=2))
        return 1
    print(json.dumps({"status": "passed", "path": str(args.path)}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
