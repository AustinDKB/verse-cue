"""TTY hop view: one heard/slide block per ProPresenter slide, rewritten in place."""

from __future__ import annotations

import sys

LIVE = {"rows": 0, "uuid": None, "paused": False}


def paint(words: list[str], matched: set[int], cue: set[int]) -> str:
    """Dim unmatched, green heard-on-slide, yellow tail matches that can arm Next."""
    parts = []
    for i, w in enumerate(words):
        code = "\033[33m" if i in cue else "\033[32m" if i in matched else "\033[2m"
        parts.append(f"{code}{w}\033[0m")
    return " ".join(parts) or "(blank)"


def cue_set(n: int, matched: set[int], *, tail: int, first_half: bool) -> set[int]:
    """Slide indexes that are both matched and far enough along to arm a click."""
    need = n - tail
    if first_half:
        need = max(need, n // 2)
    return {i for i in matched if i >= need}


def _enable_vt() -> None:
    """Turn on Windows virtual-terminal sequences so in-place redraw works in conhost."""
    if sys.platform != "win32":
        return
    import ctypes

    kernel = ctypes.windll.kernel32
    mode = ctypes.c_uint32()
    for n in (-11, -12):
        handle = kernel.GetStdHandle(n)
        kernel.GetConsoleMode(handle, ctypes.byref(mode))
        kernel.SetConsoleMode(handle, mode.value | 4)


def redraw(file, lines: tuple[str, ...]) -> None:
    """Replace the current slide's block on a TTY; append when piped (tests, logs)."""
    tty = hasattr(file, "isatty") and file.isatty()
    if not tty:
        print("\n".join(lines), file=file)
        return
    if LIVE["rows"]:
        file.write(f"\033[{LIVE['rows']}F")
    for line in lines:
        file.write(f"\033[2K{line}\n")
    file.flush()
    LIVE["rows"] = len(lines)


def hush(slide, *, paused: bool) -> bool:
    """True when this hop would reprint the same pause block."""
    return paused and LIVE["paused"] and LIVE["uuid"] == slide.uuid


def heard_line(slide, *, paused: bool) -> str:
    """Pause hint, or the latest Whisper tokens."""
    return "paused  space to resume" if paused else f"heard  {' '.join(slide.raw) or '…'}"


def show(slide, d: dict, file=sys.stderr, *, paused: bool = False) -> None:
    """Keep one heard/slide block per ProPresenter slide; rewrite it as words match."""
    if file is None or hush(slide, paused=paused):
        return
    if LIVE["uuid"] != slide.uuid:
        LIVE["rows"] = 0
        LIVE["uuid"] = slide.uuid
    LIVE["paused"] = paused
    matched = {i for i, _ in slide.pairs}
    cues = cue_set(len(slide.words), matched, tail=d["tail_words"], first_half=d.get("first_half", True))
    redraw(file, (heard_line(slide, paused=paused), f"slide  {paint(slide.words, matched, cues)}"))
