"""Four PNGs from the bench and alias JSON, and the CLI dispatch."""

import json
import math

import harvest as hv


def sample_bench():
    best = {
        "name": "small.en",
        "window_s": 4.0,
        "hop_s": 1.0,
        "prompt_mode": "none",
        "rtf": 5.0,
        "deltas": [-1.0, -0.4, 0.2, math.nan],
        "timeline": {"song": "s", "starts": [2.0, 6.0, 10.0], "fires": [5.0, math.nan]},
    }
    rows = [best, {**best, "name": "tiny.en", "rtf": 20.0}, {**best, "name": "tiny.en", "hop_s": 0.5, "rtf": 18.0}]
    return {"rows": rows, "best": best}


def test_graphs_writes_four_pngs(tmp_path):
    (tmp_path / "bench.json").write_text(json.dumps(sample_bench()))
    (tmp_path / "alias_saturation.json").write_text(json.dumps([10, 30, 45, 50, 52]))
    hv.graphs(tmp_path)
    for name in ("delta_hist.png", "rtf_vs_model.png", "alias_saturation.png", "timeline.png"):
        assert (tmp_path / name).stat().st_size > 1000


def test_graphs_without_saturation_file_still_writes_bench_graphs(tmp_path):
    (tmp_path / "bench.json").write_text(json.dumps(sample_bench()))
    hv.graphs(tmp_path)
    assert (tmp_path / "delta_hist.png").exists()
    assert not (tmp_path / "alias_saturation.png").exists()


def test_main_dispatches(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    calls = []
    monkeypatch.setattr(hv, "download", lambda limit: calls.append(("download", limit)))
    monkeypatch.setattr(hv, "songs", lambda limit: [f"song{i}" for i in range(limit)])
    monkeypatch.setattr(hv, "aliases", lambda cfg, wavs: calls.append(("aliases", len(wavs))))
    monkeypatch.setattr(hv, "bench", lambda cfg, wavs: calls.append(("bench", len(wavs))) or [])
    monkeypatch.setattr(hv, "report", lambda rows, cfg: calls.append(("report", rows)))
    monkeypatch.setattr(hv, "graphs", lambda: calls.append(("graphs",)))
    hv.main(["download", "--limit", "3"])
    hv.main(["aliases", "--limit", "2"])
    hv.main(["bench"])  # limit defaults to [bench].songs = 5
    hv.main(["graphs"])
    assert calls == [("download", 3), ("aliases", 2), ("bench", 5), ("report", []), ("graphs",)]
