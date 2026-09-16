"""Config merge, bundled default fallback, hardware table."""

from types import SimpleNamespace

import verse_cue as vc


def test_load_config_merges_auto_over_model(tmp_path):
    main = tmp_path / "verse-cue.toml"
    main.write_text('[model]\nname = ""\nwindow_s = 4.0\n')
    auto = tmp_path / "verse-cue.auto.toml"
    auto.write_text('[model]\nname = "small.en"\n')
    assert vc.load_config(main, auto)["model"] == {"name": "small.en", "window_s": 4.0}


def test_load_config_falls_back_to_bundled_default(tmp_path):
    cfg = vc.load_config(tmp_path / "missing.toml", tmp_path / "none.toml")
    assert cfg["propresenter"]["port"] == 1025
    assert cfg["model"]["prompt_mode"] == "none"
    assert cfg["model"]["name"] == "small.en"
    assert cfg["model"]["window_s"] == 4.0
    assert cfg["model"]["hop_s"] == 1.0
    assert cfg["decide"]["tail_words"] == 3
    assert cfg["decide"]["first_half"] is True
    assert cfg["decide"]["min_matched"] == 4
    assert cfg["decide"]["deadline_fire"] is False


def test_pick_model_walks_gpu_table_then_cpu():
    hw = {"gpu": [[8, "big", "float16"], [0, "small.en", "int8"]], "cpu": ["base.en", "int8"]}
    assert vc.pick_model(hw, 12.0) == ("big", "float16")
    assert vc.pick_model(hw, 3.9) == ("small.en", "int8")
    assert vc.pick_model(hw, 0.0) == ("base.en", "int8")


def test_gpu_gb_is_zero_without_nvidia_smi(monkeypatch):
    def boom(*_a, **_k):
        raise FileNotFoundError

    monkeypatch.setattr(vc.subprocess, "run", boom)
    assert vc.gpu_gb() == 0.0


def test_gpu_gb_parses_mebibytes(monkeypatch):
    monkeypatch.setattr(vc.subprocess, "run", lambda *_a, **_k: SimpleNamespace(stdout="12288\n"))
    assert vc.gpu_gb() == 12.0


def test_load_model_uses_table_when_name_empty(monkeypatch):
    seen = {}

    class FakeWhisper:
        def __init__(self, name, device, compute_type):
            seen.update(name=name, device=device, compute_type=compute_type)

    monkeypatch.setitem(__import__("sys").modules, "faster_whisper", SimpleNamespace(WhisperModel=FakeWhisper))
    monkeypatch.setattr(vc, "gpu_gb", lambda: 0.0)
    cfg = {"model": {"name": "", "compute_type": "auto"}, "hardware": {"gpu": [], "cpu": ["base.en", "int8"]}}
    vc.load_model(cfg)
    assert seen == {"name": "base.en", "device": "auto", "compute_type": "int8"}
