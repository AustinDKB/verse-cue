"""Per-window transcription mapped onto the capture clock, and the commit/latest-wins merge."""

import numpy as np

import verse_cue as vc
from tests.conftest import M, ScriptedModel


def test_transcribe_maps_word_starts_to_capture_clock_and_normalizes():
    model = ScriptedModel([[(0.2, 0.5, " Amazing,"), (0.6, 0.9, " Grace")]])
    words, infer = vc.transcribe(model, np.zeros(vc.SR, np.float32), 100.0, M, "")
    assert words == [(100.2, "amazing"), (100.6, "grace")]
    assert infer >= 0.0


def test_transcribe_passes_runtime_settings():
    model = ScriptedModel([[]])
    vc.transcribe(model, np.zeros(vc.SR, np.float32), 0.0, {**M, "beam_size": 3}, "")
    kw = model.calls[0]
    assert kw["beam_size"] == 3
    assert kw["word_timestamps"] is True
    assert kw["condition_on_previous_text"] is False
    assert kw["vad_filter"] is False
    assert kw["temperature"] == 0.0
    assert "initial_prompt" not in kw
    assert "hotwords" not in kw


def test_transcribe_prompt_modes():
    slide_mode = ScriptedModel([[]])
    vc.transcribe(slide_mode, np.zeros(vc.SR, np.float32), 0.0, {**M, "prompt_mode": "slide"}, "our god")
    assert slide_mode.calls[0]["initial_prompt"] == "our god"
    hot = ScriptedModel([[]])
    vc.transcribe(hot, np.zeros(vc.SR, np.float32), 0.0, {**M, "prompt_mode": "hotwords"}, "our god")
    assert hot.calls[0]["hotwords"] == "our god"


def test_transcribe_temperature_override_for_harvest():
    model = ScriptedModel([[]])
    vc.transcribe(model, np.zeros(vc.SR, np.float32), 0.0, {**M, "temperature": 1.0}, "")
    assert model.calls[0]["temperature"] == 1.0


def test_merge_commits_words_that_left_the_window_and_latest_wins():
    s = vc.Slide("u", ["a", "b"], entered=0.0)
    s.previous = [(0.5, "x"), (2.5, "y")]
    out = vc.merge(s, [(2.6, "y2"), (3.5, "z")], window_start=2.0, guard_until=0.0)
    assert s.committed == [(0.5, "x")]
    assert s.previous == [(2.6, "y2"), (3.5, "z")]
    assert out == [(0.5, "x"), (2.6, "y2"), (3.5, "z")]


def test_merge_drops_bleed_before_guard():
    s = vc.Slide("u", ["a"], entered=10.0)
    out = vc.merge(s, [(10.1, "held"), (10.9, "new")], window_start=8.0, guard_until=10.3)
    assert out == [(10.9, "new")]
