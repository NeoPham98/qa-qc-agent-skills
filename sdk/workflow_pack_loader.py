from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_workflow_pack(root: Path, pack_id: str = "default") -> dict[str, Any]:
    pack_dir = root / "workflow-packs" / pack_id
    workflow_json_path = pack_dir / "workflow.json"
    workflow_yaml_path = pack_dir / "workflow.yml"
    if workflow_json_path.exists():
        workflow = json.loads(workflow_json_path.read_text(encoding="utf-8"))
    elif workflow_yaml_path.exists():
        try:
            import yaml  # type: ignore
            workflow = yaml.safe_load(workflow_yaml_path.read_text(encoding="utf-8"))
        except ImportError:
            workflow = parse_simple_yaml(workflow_yaml_path.read_text(encoding="utf-8"))
    else:
        raise FileNotFoundError(f"Workflow pack not found: {workflow_json_path} or {workflow_yaml_path}")
    workflow["pack_dir"] = str(pack_dir)
    return workflow


def parse_simple_yaml(text: str) -> dict[str, Any]:
    try:
        import subprocess, sys, tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
            f.write("import sys, yaml, json; print(json.dumps(yaml.safe_load(sys.stdin.read())))")
        proc = subprocess.run([sys.executable, f.name], input=text, text=True, capture_output=True, check=False)
        if proc.returncode == 0:
            return json.loads(proc.stdout)
    except Exception:
        pass
    raise RuntimeError("PyYAML is required to load workflow.yml")
