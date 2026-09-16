"""Shared fakes. No model downloads, no network, no audio hardware."""

from __future__ import annotations

import shutil
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

import verse_cue as vc

REPO = Path(__file__).resolve().parents[1]

D = {
    "lead_s": 0.3,
    "guard_s": 0.3,
    "default_sec_per_word": 0.45,
    "rate_bounds": [0.15, 1.5],
    "min_matched": 4,
    "tail_words": 3,
    "fuzzy_cutoff": 0.8,
}
M = {"name": "tiny.en", "compute_type": "int8", "window_s": 4.0, "hop_s": 1.0, "beam_size": 1, "prompt_mode": "none"}


class ScriptedModel:
    """Fake WhisperModel. Each transcribe() returns the next scripted window: [(start, end, word), ...]."""

    def __init__(self, windows):
        self.windows = list(windows)
        self.calls: list[dict] = []

    def transcribe(self, audio, **kw):
        self.calls.append(kw)
        words = self.windows.pop(0) if self.windows else []
        segment = SimpleNamespace(words=[SimpleNamespace(start=s, end=e, word=w, probability=1.0) for s, e, w in words])
        return iter([segment]), None


class ScriptedPP:
    """Fake ProPresenter: a list of (uuid, text); next() advances; set(i) simulates the operator."""

    def __init__(self, slides):
        self.slides = list(slides)
        self.i = 0
        self.fires: list[float] = []
        self.reads = 0

    def slide(self):
        self.reads += 1
        return self.slides[self.i] if self.i < len(self.slides) else ("", "")

    def next(self, at):
        self.fires.append(at)
        self.i += 1

    def set(self, i):
        self.i = i


def silent_frames(t_ends, hop_s=1.0):
    """Yield (t_end, zeros) frames like the microphone would."""
    for t in t_ends:
        yield t, np.zeros(int(hop_s * vc.SR), dtype=np.float32)


@pytest.fixture
def cfg(tmp_path):
    """The bundled default config, with aliases empty and metrics redirected to tmp."""
    c = vc.load_config(REPO / "verse-cue.toml", tmp_path / "none.toml")
    c["aliases"] = {}
    c["metrics_file"] = str(tmp_path / "metrics.jsonl")
    return c


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    """A working directory holding a copy of the default config."""
    shutil.copy(REPO / "verse-cue.toml", tmp_path / "verse-cue.toml")
    monkeypatch.chdir(tmp_path)
    return tmp_path
