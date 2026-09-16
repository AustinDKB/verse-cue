"""Real tiny.en over synthetic audio. Runs only with VERSE_CUE_ONLINE=1 (downloads ~75 MB once)."""

import os

import numpy as np
import pytest

import verse_cue as vc
from tests.conftest import M

pytestmark = pytest.mark.skipif(os.environ.get("VERSE_CUE_ONLINE") != "1", reason="set VERSE_CUE_ONLINE=1")


def test_tiny_en_transcribes_and_vad_runs():
    from faster_whisper import WhisperModel

    model = WhisperModel("tiny.en", device="auto", compute_type="int8")
    tone = (0.1 * np.sin(np.linspace(0, 2 * np.pi * 220 * 2, 2 * vc.SR))).astype(np.float32)
    words, infer = vc.transcribe(model, tone, 0.0, M, "")
    assert isinstance(words, list)
    assert infer < 10
    assert vc.speech_in(tone, {"min_speech_ms": 300}) in (True, False)
