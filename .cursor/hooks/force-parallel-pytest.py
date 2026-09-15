#!/usr/bin/env python3
# Copyright (C) 2026 Austin Bakanec
"""Deny agent pytest runs that are not the full suite in parallel."""

from __future__ import annotations

import json
import re
import shlex
import sys
from typing import Any

_SEPARATORS = {"&&", "||", ";", "|"}
_INSPECT = {"-h", "--help", "--version", "--collect-only", "--fixtures", "--markers"}
_FULL_PATHS = {"tests", "tests/"}
_VALUE_FLAGS = {
    "-n",
    "--numprocesses",
    "-k",
    "-m",
    "-o",
    "--override-ini",
    "-p",
    "-c",
    "--tb",
    "--maxfail",
    "--dist",
    "-W",
    "--junitxml",
    "--cov",
    "--cov-report",
    "--rootdir",
    "--confcutdir",
    "--basetemp",
    "--override-ini",
}
_SHRINK = {"-k", "-m", "--lf", "--ff", "--sw", "-x", "--exitfirst", "--last-failed", "--failed-first", "--stepwise"}

_DENY = (
    "Run the full suite in parallel: `uv run pytest`. "
    "Do not pass paths, -k, -x, -n0, -n 1, or -o addopts=."
)


def _deny(reason: str) -> dict[str, str]:
    return {
        "permission": "deny",
        "user_message": f"Blocked a non-parallel or partial pytest run. {reason}",
        "agent_message": _DENY,
    }


def _allow() -> dict[str, str]:
    return {"permission": "allow"}


def _command(payload: dict[str, Any]) -> str:
    tool_input = payload.get("tool_input")
    if isinstance(tool_input, dict) and isinstance(tool_input.get("command"), str):
        return tool_input["command"]
    command = payload.get("command")
    return command if isinstance(command, str) else ""


def _pytest_argvs(command: str) -> list[list[str]]:
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        tokens = command.split()

    argvs: list[list[str]] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        start = None
        if token in {"pytest", "py.test"}:
            start = index + 1
        elif token in {"python", "python3"} and index + 2 < len(tokens) and tokens[index + 1] == "-m":
            module = tokens[index + 2]
            if module == "pytest" or module.startswith("pytest "):
                start = index + 3
        if start is None:
            index += 1
            continue
        args: list[str] = []
        cursor = start
        while cursor < len(tokens) and tokens[cursor] not in _SEPARATORS:
            args.append(tokens[cursor])
            cursor += 1
        argvs.append(args)
        index = cursor + 1
    return argvs


def _flag_name(token: str) -> str:
    if token.startswith("--") and "=" in token:
        return token.split("=", 1)[0]
    return token


def _worker_count(value: str) -> str | None:
    if value in {"auto", "logical"}:
        return None
    if re.fullmatch(r"[0-9]+", value) and int(value) >= 2:
        return None
    return f"worker count {value!r} is not parallel (-n auto)"


def _check_args(args: list[str]) -> str | None:
    if any(flag in args or any(arg.startswith(f"{flag}=") for arg in args) for flag in _INSPECT):
        return None

    positionals: list[str] = []
    index = 0
    while index < len(args):
        token = args[index]
        name = _flag_name(token)
        value = token.split("=", 1)[1] if name != token else None

        if name in _SHRINK or token in _SHRINK:
            return "that command does not run every test"

        if name == "-p" or token.startswith("-pno:"):
            plugin = token[2:] if token.startswith("-p") and token != "-p" else value
            if plugin is None:
                plugin = args[index + 1] if index + 1 < len(args) else ""
            if plugin.startswith("no:") and "xdist" in plugin:
                return "xdist is disabled"
            index += 1 if token != "-p" or value is not None else 2
            continue

        if name in {"-o", "--override-ini"}:
            setting = value or (args[index + 1] if index + 1 < len(args) else "")
            if "addopts" in setting or "numprocesses" in setting:
                return "addopts/xdist override is not allowed"
            index += 1 if value is not None else 2
            continue

        if name in {"-n", "--numprocesses"} or re.fullmatch(r"-n[0-9]+", token):
            count = value or token[2:] or (args[index + 1] if index + 1 < len(args) else "")
            reason = _worker_count(count)
            if reason:
                return reason
            index += 1 if value is not None or re.fullmatch(r"-n[0-9]+", token) else 2
            continue

        if token.startswith("-"):
            if name in _VALUE_FLAGS and value is None:
                index += 2
                continue
            index += 1
            continue

        positionals.append(token)
        index += 1

    extras = [path for path in positionals if path not in _FULL_PATHS]
    if extras:
        return "pass no test paths; `uv run pytest` already runs the suite"
    return None


def decision(command: str) -> dict[str, str]:
    if "pytest" not in command:
        return _allow()
    # Ignore mentions that are not an invocation (rg/grep/echo/docs).
    if not re.search(r"(?:^|[;&|]\s*|\s)(?:uv\s+run\s+)?(?:python3?\s+-m\s+)?pytest\b", command):
        return _allow()
    for args in _pytest_argvs(command):
        reason = _check_args(args)
        if reason:
            return _deny(reason)
    if not _pytest_argvs(command) and re.search(r"(?:^|\s)pytest\b", command):
        # Unparsed invocation that still looks like a filtered run.
        if re.search(r"-o\s+addopts=|-n\s*0|-n0|--numprocesses(?:=|\s+)[01]\b|-p\s+no:xdist", command):
            return _deny("that command does not run the full suite in parallel")
    return _allow()


def _self_check() -> None:
    allow = [
        "uv run pytest",
        "uv run pytest -q",
        "uv run pytest -v --tb=short",
        "uv run pytest tests",
        "uv run ruff check app && uv run pytest",
        "rg pytest tests",
        "uv run python scripts/run_mutmut.py",
    ]
    deny = [
        "uv run pytest tests/test_foo.py",
        "uv run pytest tests/test_foo.py::test_bar",
        "uv run pytest -k dues",
        "uv run pytest -x",
        "uv run pytest -n0",
        "uv run pytest -n 1",
        "uv run pytest -o addopts=",
        "uv run pytest -p no:xdist",
        "uv run ruff check app && uv run pytest tests/test_foo.py",
    ]
    for command in allow:
        result = decision(command)
        assert result["permission"] == "allow", command
    for command in deny:
        result = decision(command)
        assert result["permission"] == "deny", command


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--self-check":
        _self_check()
        print("OK: force-parallel-pytest")
        return
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        json.dump(_deny("hook input was invalid"), sys.stdout)
        return
    if not isinstance(payload, dict):
        json.dump(_deny("hook input was invalid"), sys.stdout)
        return
    json.dump(decision(_command(payload)), sys.stdout)


if __name__ == "__main__":
    main()
