from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DESTRUCTIVE_BASH_PATTERNS = [
    r"\brm\s+-rf\b",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+push\b.*\s--force(?:-with-lease)?\b",
    r"\bgit\s+branch\s+-D\b",
    r"\bgit\s+clean\s+-f\b",
    r"\bdrop\s+table\b",
]

EXTERNAL_WRITE_PATTERNS = [
    r"\bgh\s+pr\s+create\b",
    r"\bgh\s+pr\s+comment\b",
    r"\bgh\s+issue\s+comment\b",
    r"\bcurl\b.*\s-X\s*(POST|PUT|PATCH|DELETE)\b",
]

PROTECTED_PATH_PARTS = (
    "BIDV/template/",
    "BIDV/Prompt/",
    "examples/golden-outputs/",
)


@dataclass(frozen=True)
class PolicyDecision:
    allow: bool
    reason: str


def inspect_bash_command(command: str, explicit_approval: bool = False) -> PolicyDecision:
    lowered = command.lower()
    for pattern in DESTRUCTIVE_BASH_PATTERNS:
        if re.search(pattern, lowered):
            return PolicyDecision(False, f"blocked destructive command pattern: {pattern}")
    for pattern in EXTERNAL_WRITE_PATTERNS:
        if re.search(pattern, lowered) and not explicit_approval:
            return PolicyDecision(False, f"external write requires explicit approval: {pattern}")
    return PolicyDecision(True, "command allowed by policy")


def inspect_write_path(path: str, explicit_approval: bool = False) -> PolicyDecision:
    normalized = Path(path).as_posix()
    for protected in PROTECTED_PATH_PARTS:
        if protected in normalized and not explicit_approval:
            return PolicyDecision(False, f"protected path requires explicit approval: {protected}")
    return PolicyDecision(True, "path allowed by policy")


def require_prompt_mirror_verification(ok: bool) -> PolicyDecision:
    if not ok:
        return PolicyDecision(False, "handoff requires passing prompt mirror verification")
    return PolicyDecision(True, "prompt mirror verification passed")


def require_output_review(artifact_paths: list[str]) -> PolicyDecision:
    has_review = any(Path(path).name.lower() == "outputreview.md" for path in artifact_paths)
    if not has_review:
        return PolicyDecision(False, "handoff requires OutputReview.md")
    return PolicyDecision(True, "OutputReview.md present")


def build_sdk_hooks() -> dict[str, list[dict[str, Any]]]:
    """Return a placeholder hook config shape for ClaudeAgentOptions.

    Projects should adapt this to the exact SDK hook callback interface used by
    their installed `claude-agent-sdk-python` version.
    """
    return {
        "PreToolUse": [],
        "PostToolUse": [],
        "SubagentStop": [],
        "Stop": [],
    }
