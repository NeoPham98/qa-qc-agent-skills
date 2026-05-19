from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = ["workflow.json", "workflow.yml", "classifiers.yml", "output_profiles.yml", "validators.yml", "README.md"]


def validate_pack(pack_dir: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        if not (pack_dir / name).exists():
            errors.append(f"missing required file: {name}")
    workflow_path = pack_dir / "workflow.json"
    if workflow_path.exists():
        try:
            workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return [f"workflow.json invalid JSON: {exc}"]
        routes = workflow.get("routes") or {}
        stages = workflow.get("stages") or {}
        if not routes:
            errors.append("workflow.json has no routes")
        if not stages:
            errors.append("workflow.json has no stages")
        for route_id, route in routes.items():
            final_outputs = route.get("final_outputs") or []
            if not final_outputs:
                errors.append(f"route {route_id} has no final_outputs")
            for stage_id in route.get("stages", []):
                if stage_id not in stages:
                    errors.append(f"route {route_id} references missing stage {stage_id}")
        for stage_id, stage in stages.items():
            prompt = stage.get("prompt")
            if prompt and not (pack_dir / prompt).exists():
                errors.append(f"stage {stage_id} prompt missing: {prompt}")
    return errors


def main() -> int:
    pack = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "workflow-packs" / "default"
    errors = validate_pack(pack)
    if errors:
        print(json.dumps({"status": "errors_found", "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"status": "success", "pack": str(pack)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
