"""Alias mining: opcode pairing, table filtering, saturation stop rule, and the driver with fakes."""

import json
from collections import Counter

import harvest as hv
import verse_cue as vc
from tests.conftest import M, ScriptedModel
from tests.test_lrc import write_wav


def test_mishearings_pairs_equal_length_replacements_only():
    lyric = vc.tokens("hallelujah name above all names")
    heard = vc.tokens("halleluia name above all the names")  # 1 replace, 1 insert
    assert hv.mishearings(lyric, heard) == [("hallelujah", "halleluia")]


def test_mishearings_skips_unequal_spans():
    assert hv.mishearings(["a", "b", "c"], ["x", "c"]) == []


def test_alias_table_filters_and_caps():
    counts = Counter(
        {("god", "gone"): 5, ("god", "got"): 2, ("god", "gah"): 1, ("god", "god"): 9, ("grace", "grays"): 3}
    )
    table = hv.alias_table(counts, min_count=2, max_per_word=1)
    assert table == {"god": {"gone": 5}, "grace": {"grays": 3}}


def test_saturated_needs_window_plus_one_points():
    assert hv.saturated([100] * 10) is False


def test_saturated_true_when_last_window_grows_under_pct():
    curve = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
    assert hv.saturated(curve, window=10, pct=1.0) is True
    assert hv.saturated([*curve[:-1], 102], window=10, pct=1.0) is False


def test_song_tokens_concatenates_windows():
    model = ScriptedModel([[(0.0, 0.2, " Our"), (0.3, 0.5, " God,")], [(0.0, 0.2, " reigns")]])
    frames = [(1.0, None), (2.0, None)]
    assert hv.song_tokens(model, frames, M) == ["our", "god", "reigns"]


def test_aliases_writes_table_and_curve(tmp_path, monkeypatch, cfg):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(hv, "METRICS_DIR", tmp_path / "metrics")
    monkeypatch.setattr(vc, "ALIASES", tmp_path / "aliases.json")
    write_wav(tmp_path / "s.wav", 4.0)
    (tmp_path / "s.txt").write_text("our god is an awesome god")
    hot = ScriptedModel(
        [
            [
                (0.0, 0.2, "our"),
                (0.3, 0.5, "gone"),
                (0.6, 0.8, "is"),
                (0.9, 1.1, "an"),
                (1.2, 1.4, "awesome"),
                (1.5, 1.7, "god"),
            ]
        ]
        * 3
    )
    monkeypatch.setattr(hv, "alias_passes", lambda c: [(hot, 0.6), (hot, 1.0), (hot, 0.0)])
    cfg["alias"]["min_count"] = 2
    hv.aliases(cfg, [tmp_path / "s.wav"])
    table = json.loads((tmp_path / "aliases.json").read_text())
    assert table == {"god": {"gone": 3}}
    assert json.loads((tmp_path / "metrics" / "alias_saturation.json").read_text()) == [1]


def test_alias_passes_hot_then_real(monkeypatch, cfg):
    made = []
    monkeypatch.setattr(hv, "get_model", lambda name, ct: made.append((name, ct)) or f"M:{name}")
    monkeypatch.setattr(vc, "gpu_gb", lambda: 0.0)
    passes = hv.alias_passes(cfg)
    assert passes == [("M:tiny.en", 0.6), ("M:tiny.en", 1.0), ("M:small.en", 0.0)]
