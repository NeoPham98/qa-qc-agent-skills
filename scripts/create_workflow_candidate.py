from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def slugify(value: str) -> str:
    chars = []
    for ch in value.lower().strip():
        if ch.isalnum():
            chars.append(ch)
        elif ch in {" ", "-", "_"}:
            chars.append("-")
    slug = "".join(chars).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "custom-workflow"


def create_candidate(name: str, prompt_files: list[Path], example_inputs: list[Path], example_outputs: list[Path], description: str | None) -> Path:
    pack_id = f"custom-{slugify(name)}"
    pack_dir = ROOT / "workflow-packs" / pack_id
    if pack_dir.exists():
        raise FileExistsError(f"Candidate workflow pack already exists: {pack_dir}")
    for sub in ["prompts", "contracts", "examples/inputs", "examples/outputs"]:
        (pack_dir / sub).mkdir(parents=True, exist_ok=True)
    for path in prompt_files:
        shutil.copy2(path, pack_dir / "prompts" / path.name)
    for path in example_inputs:
        shutil.copy2(path, pack_dir / "examples" / "inputs" / path.name)
    for path in example_outputs:
        shutil.copy2(path, pack_dir / "examples" / "outputs" / path.name)
    (pack_dir / "workflow.json").write_text(candidate_workflow_json(pack_id, name), encoding="utf-8")
    (pack_dir / "workflow.yml").write_text(candidate_workflow_yaml(pack_id, name), encoding="utf-8")
    (pack_dir / "classifiers.yml").write_text("source_roles: {}\nprompt_intents: {}\n", encoding="utf-8")
    (pack_dir / "output_profiles.yml").write_text("profiles: {}\n", encoding="utf-8")
    (pack_dir / "validators.yml").write_text("validators: {}\n", encoding="utf-8")
    (pack_dir / "review_notes.md").write_text(review_notes(name, description), encoding="utf-8")
    return pack_dir


def candidate_workflow_json(pack_id: str, name: str) -> str:
    return '{\n  "id": "' + pack_id + '",\n  "version": "0.1.0-candidate",\n  "name": "' + name + '",\n  "routes": {},\n  "stages": {}\n}\n'


def candidate_workflow_yaml(pack_id: str, name: str) -> str:
    return f"id: {pack_id}\nversion: 0.1.0-candidate\nname: {name}\nroutes: {{}}\nstages: {{}}\n"


def review_notes(name: str, description: str | None) -> str:
    return f"""# Candidate Workflow Pack Review

Name: {name}
Created: {datetime.now().isoformat(timespec='seconds')}

## Description

{description or 'TBD'}

## Before enabling

- Define source role classifier rules.
- Define prompt intent classifier rules.
- Define routes and stages in workflow.json/workflow.yml.
- Define output contracts and validators.
- Add golden examples and expected final outputs.
- Run scripts/validate_workflow_pack.py against this pack.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Create candidate workflow pack from user-provided prompts/examples")
    parser.add_argument("--name", required=True)
    parser.add_argument("--description")
    parser.add_argument("--prompt-file", action="append", default=[])
    parser.add_argument("--example-input", action="append", default=[])
    parser.add_argument("--example-output", action="append", default=[])
    args = parser.parse_args()
    pack_dir = create_candidate(
        args.name,
        [Path(p) for p in args.prompt_file],
        [Path(p) for p in args.example_input],
        [Path(p) for p in args.example_output],
        args.description,
    )
    print(pack_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
