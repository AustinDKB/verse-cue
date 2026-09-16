#!/usr/bin/env python3
# Copyright (C) 2026 Austin Bakanec
"""Gate agent edits to pyproject.toml — always ask the user first."""

from __future__ import annotations

import re
import sys
import json
from typing import Any
from pathlib import Path

PROTECTED_NAME = "pyproject.toml"

# Shell patterns that can rewrite pyproject.toml (not mere reads).
_SHELL_WRITE_HINTS = re.compile(
    r"""(?ix)
    (
        \btee\b
        | \bsed\b
        | \bperl\b
        | \bruby\b
        | \bpython3?\b
        | \buv\b
        | \bpoetry\b
        | \bpip\b
        | \bprintf\b
        | \bcat\b.*>
        | >>?
        | \bmv\b
        | \bcp\b
        | \brm\b
        | \btouch\b
        | \btruncate\b
        | \bed\b
    )
    """,
)


def _norm(path: str) -> str:
    return path.replace("\\", "/").rstrip("/")


def _targets_pyproject(path: str | None) -> bool:
    if not path:
        return False
    name = Path(_norm(path)).name
    return name.lower() == PROTECTED_NAME


def _tool_paths(tool_input: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for key in ("path", "file_path", "filePath", "target_notebook"):
        value = tool_input.get(key)
        if isinstance(value, str):
            paths.append(value)
    return paths


def _shell_touches_pyproject(command: str) -> bool:
    if PROTECTED_NAME not in command:
        return False
    if _SHELL_WRITE_HINTS.search(command):
        return True
    # Still ask if the command clearly redirects into pyproject.toml.
    return bool(re.search(rf">{{1,2}}\s*[\"']?[^\"'\s]*{PROTECTED_NAME}", command))


def _ask(message: str) -> dict[str, str]:
    return {
        "permission": "ask",
        "user_message": message,
        "agent_message": (
            "Editing pyproject.toml requires explicit user approval. Do not retry until the user approves this change."
        ),
    }


def _allow() -> dict[str, str]:
    return {"permission": "allow"}


def main() -> None:
    """Read a Cursor hook payload from stdin and print an allow/ask/deny decision."""
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Fail closed on garbage input when failClosed is set in hooks.json.
        json.dump(
            {
                "permission": "deny",
                "user_message": "protect-pyproject hook received invalid JSON.",
                "agent_message": "Hook input was invalid; pyproject.toml edit blocked.",
            },
            sys.stdout,
        )
        return

    event = payload.get("hook_event_name") or ""
    tool_name = payload.get("tool_name") or ""
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        tool_input = {}

    # File-edit tools (Write / StrReplace / Delete / EditNotebook).
    if event == "preToolUse" or tool_name in {
        "Write",
        "StrReplace",
        "Delete",
        "EditNotebook",
    }:
        for path in _tool_paths(tool_input):
            if _targets_pyproject(path):
                json.dump(
                    _ask(
                        f"Agent wants to modify protected file `{PROTECTED_NAME}` "
                        f"via {tool_name or 'tool'}. Approve this edit?"
                    ),
                    sys.stdout,
                )
                return

    # Shell commands that may rewrite pyproject.toml.
    command = ""
    if isinstance(tool_input.get("command"), str):
        command = tool_input["command"]
    elif isinstance(payload.get("command"), str):
        command = payload["command"]

    if command and _shell_touches_pyproject(command):
        json.dump(
            _ask(
                "Agent shell command may modify `pyproject.toml`. "
                "Review and approve before it runs:\n\n"
                f"```\n{command}\n```"
            ),
            sys.stdout,
        )
        return

    json.dump(_allow(), sys.stdout)


if __name__ == "__main__":
    main()
