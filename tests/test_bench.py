"""Bench = offline eval. A scripted model replays a silent wav against LRC ground truth."""

import json
import math

import pytest

import harvest as hv
import verse_cue as vc
from tests.conftest import ScriptedModel
from tests.test_lrc import write_wav

LRC = "[00:02.00] our god is an awesome god\n[00:06.00] he reigns from heaven above\n[00:10.00] with wisdom power and love\n[00:14.00] our god is an awesome god\n"


def words_at(offsets_words):
    return [(o, o + 0.3, w) for o, w in offsets_words]


def scripted_windows():
    # 20 frames of 1 s. Window 5 (start 1.0) hears slide 0's first five words at 0.4 s/word (capture 3.0..4.6):
    # predicted = 4.6 + 1*0.4 - 0.3 = 4.7 -> fired at ~5.0, truth 6.0 -> delta ~ -1.0.
    # Window 9 (start 5.0) hears slide 1's first four words (capture 7.0..8.2): predicted 8.3 -> fired ~9.0, truth 10 -> -1.0.
    # Slide 2 hears nothing -> the operator (FakePP) advances at 14 + 2 s -> nan.
    w = [[] for _ in range(20)]
    w[4] = words_at([(2.0, "our"), (2.4, "god"), (2.8, "is"), (3.2, "an"), (3.6, "awesome")])
    w[8] = words_at([(2.0, "he"), (2.4, "reigns"), (2.8, "from"), (3.2, "heaven")])
    return w


def test_bench_song_deltas_lengths_rtf_timeline(tmp_path, cfg):
    write_wav(tmp_path / "s.wav", 20.0)
    (tmp_path / "s.lrc").write_text(LRC)
    cfg["bench"]["lines_per_slide"] = 1
    r = hv.bench_song(tmp_path / "s.wav", ScriptedModel(scripted_windows()), cfg)
    assert r["deltas"][0] == pytest.approx(-1.0, abs=0.05)
    assert r["deltas"][1] == pytest.approx(-1.0, abs=0.05)
    assert math.isnan(r["deltas"][2])
    assert r["lengths"] == [4.0, 4.0, 4.0]
    assert r["rtf"] > 0
    assert r["timeline"]["starts"] == [2.0, 6.0, 10.0, 14.0]
    assert len(r["timeline"]["fires"]) == 3


def test_summarize():
    s = hv.summarize([-1.0, -0.5, 2.0, math.nan, -3.0], [4.0, 4.0, 4.0, 4.0, 4.0])
    assert s["n"] == 5
    assert s["median_delta"] == pytest.approx(-0.75)
    assert s["p90_abs_delta"] == pytest.approx(2.7)
    assert s["early_pct"] == 60.0
    assert s["late_pct"] == 20.0
    assert s["missed_pct"] == 20.0
    assert s["false_pct"] == 20.0  # -3.0 fired before the slide's midpoint (-2.0)


def test_summarize_all_missed():
    s = hv.summarize([math.nan, math.nan], [4.0, 4.0])
    assert s["median_delta"] is None
    assert s["p90_abs_delta"] is None
    assert s["missed_pct"] == 100.0


def test_grid_is_the_cartesian_product():
    b = {"models": ["a", "b"], "window_s": [3.0], "hop_s": [0.5, 1.0], "prompt_mode": ["none"]}
    g = hv.grid(b)
    assert len(g) == 4
    assert g[0] == {"name": "a", "window_s": 3.0, "hop_s": 0.5, "prompt_mode": "none"}


def test_select_requires_rtf_and_false_pct_then_min_p90():
    b = {"min_rtf": 4.0, "max_false_pct": 5.0}
    rows = [
        {"name": "slow", "rtf": 1.0, "false_pct": 0.0, "p90_abs_delta": 0.1},
        {"name": "trigger-happy", "rtf": 9.0, "false_pct": 9.0, "p90_abs_delta": 0.2},
        {"name": "good", "rtf": 5.0, "false_pct": 1.0, "p90_abs_delta": 0.8},
        {"name": "better", "rtf": 4.0, "false_pct": 4.0, "p90_abs_delta": 0.6},
        {"name": "dead", "rtf": 9.0, "false_pct": 0.0, "p90_abs_delta": None},
    ]
    assert hv.select(rows, b)["name"] == "better"
    assert hv.select([rows[0]], b) is None


def test_write_auto_and_summary(tmp_path):
    row = {
        "name": "small.en",
        "compute_type": "int8",
        "window_s": 4.0,
        "hop_s": 1.0,
        "prompt_mode": "slide",
        "rtf": 5.2,
        "median_delta": -0.4,
        "p90_abs_delta": 0.9,
        "early_pct": 80.0,
        "late_pct": 5.0,
        "missed_pct": 2.0,
        "false_pct": 1.0,
    }
    hv.write_auto(row, tmp_path / "auto.toml")
    merged = vc.load_config(tmp_path / "missing.toml", tmp_path / "auto.toml")["model"]
    assert merged["name"] == "small.en"
    assert merged["prompt_mode"] == "slide"
    assert merged["hop_s"] == 1.0
    hv.write_summary([row, {**row, "name": "worse", "p90_abs_delta": None}], tmp_path / "summary.md")
    text = (tmp_path / "summary.md").read_text()
    assert text.splitlines()[0].startswith("| name | window_s |")
    assert text.index("small.en") < text.index("worse")


def test_bench_and_report_end_to_end(tmp_path, monkeypatch, cfg):
    write_wav(tmp_path / "s.wav", 20.0)
    (tmp_path / "s.lrc").write_text(LRC)
    monkeypatch.setattr(hv, "get_model", lambda name, ct: ScriptedModel(scripted_windows()))
    monkeypatch.setattr(hv, "METRICS_DIR", tmp_path / "metrics")
    monkeypatch.setattr(vc, "AUTO", tmp_path / "auto.toml")
    cfg["bench"].update(
        models=["tiny.en"], window_s=[4.0], hop_s=[1.0], prompt_mode=["none"], lines_per_slide=1, min_rtf=0.0
    )
    rows = hv.bench(cfg, [tmp_path / "s.wav"])
    assert len(rows) == 1
    assert rows[0]["missed_pct"] == pytest.approx(33.3, abs=0.1)
    hv.report(rows, cfg)
    assert (tmp_path / "auto.toml").exists()
    saved = json.loads((tmp_path / "metrics" / "bench.json").read_text())
    assert saved["best"]["name"] == "tiny.en"
    assert (tmp_path / "metrics" / "summary.md").exists()
