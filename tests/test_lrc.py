"""Ground truth from LRC, the simulated ProPresenter, and wav framing."""

import math
import wave

import numpy as np
import pytest

import harvest as hv
import verse_cue as vc

LINES = [(2.0, "a b"), (6.0, "c d"), (10.0, "e f"), (14.0, "g h"), (30.0, "i j"), (34.0, "k l")]


def write_wav(path, seconds, rate=vc.SR):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(np.zeros(int(seconds * rate), dtype=np.int16).tobytes())


def test_group_lines_drops_empty_and_chunks():
    lines = [(1.0, "x"), (2.0, ""), (3.0, "y"), (4.0, "z")]
    assert hv.group_lines(lines, 2) == [[(1.0, "x"), (3.0, "y")], [(4.0, "z")]]


def test_pseudo_slides_inserts_blank_for_long_gaps_only():
    slides = hv.pseudo_slides(hv.group_lines(LINES, 2), gap_s=8.0)
    assert slides == [
        (2.0, "a b c d"),
        (10.0, "e f g h"),
        (19.0, ""),  # last line of previous slide at 14.0 + blank_after_s 5.0
        (30.0, "i j k l"),
    ]


def test_pseudo_slides_leading_blank_when_intro_is_long():
    slides = hv.pseudo_slides(hv.group_lines([(12.0, "a"), (14.0, "b")], 1), gap_s=8.0)
    assert slides[0] == (0.0, "")
    assert slides[1] == (12.0, "a")


def test_fakepp_records_fires_and_operator_advances_missed_slides():
    now = [0.0]
    pp = hv.FakePP([(0.0, "a"), (10.0, "b"), (20.0, "c")], lambda: now[0])
    assert pp.slide() == ("0", "a")
    pp.next(at=9.0)
    assert pp.slide() == ("1", "b")
    now[0] = 20.0 + hv.MISS_GRACE_S + 0.1  # slide b was never fired
    assert pp.slide() == ("2", "c")
    assert pp.fires[0] == 9.0
    assert math.isnan(pp.fires[1])
    pp.next(at=25.0)
    assert pp.slide() == ("", "")  # past the end: nothing to advance


def test_wav_frames_yields_hops_and_updates_cell(tmp_path):
    write_wav(tmp_path / "s.wav", 3.5)
    cell = [0.0]
    frames = list(hv.wav_frames(tmp_path / "s.wav", 1.0, cell))
    assert [t for t, _ in frames] == [1.0, 2.0, 3.0]
    assert all(chunk.shape == (vc.SR,) and chunk.dtype == np.float32 for _, chunk in frames)
    assert cell[0] == 3.0


def test_wav_frames_rejects_wrong_rate(tmp_path):
    write_wav(tmp_path / "bad.wav", 1.0, rate=44100)
    with pytest.raises(ValueError, match="16000"):
        list(hv.wav_frames(tmp_path / "bad.wav", 1.0, [0.0]))
