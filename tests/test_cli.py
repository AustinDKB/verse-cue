"""--setup rewrites device, host, and port; main wires config -> aliases -> PP -> model -> run."""

import sys
from types import SimpleNamespace

import verse_cue as vc

DEVICES = [
    {"name": "Monitor of Built-in", "max_input_channels": 0},
    {"name": "Focusrite USB", "max_input_channels": 2},
    {"name": "Webcam Mic", "max_input_channels": 1},
]


def fake_sounddevice(monkeypatch):
    sd = SimpleNamespace(query_devices=lambda: DEVICES, InputStream=None)
    monkeypatch.setitem(sys.modules, "sounddevice", sd)
    return sd


def test_setup_prompts_for_input_device_and_port(workdir, monkeypatch, capsys):
    fake_sounddevice(monkeypatch)
    answers = iter(["1", "10.0.0.5", "1030"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    monkeypatch.setattr(vc, "lan_ip", lambda: "192.168.1.50")
    vc.setup()
    text = (workdir / "verse-cue.toml").read_text()
    assert 'device = "Focusrite USB"' in text
    assert 'host = "10.0.0.5"' in text
    assert "port = 1030" in text
    out = capsys.readouterr().out
    assert "1: Focusrite USB" in out
    assert "0: Monitor of Built-in" not in out  # outputs are not offered
    assert "10.0.0.5:1030" in out
    assert "192.168.1.50" in out
    assert "Network API" in out
    assert "small.en" in out


def test_setup_keeps_default_port_on_empty_answer(workdir, monkeypatch):
    fake_sounddevice(monkeypatch)
    answers = iter(["2", "", ""])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    monkeypatch.setattr(vc, "lan_ip", lambda: "127.0.0.1")
    vc.setup()
    text = (workdir / "verse-cue.toml").read_text()
    assert 'device = "Webcam Mic"' in text
    assert 'host = "127.0.0.1"' in text
    assert "port = 50001" in text


def test_main_creates_config_from_bundled_default_then_runs_setup(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    called = []
    monkeypatch.setattr(vc, "setup", lambda: called.append(True))
    vc.main(["--setup"])
    assert (tmp_path / "verse-cue.toml").exists()
    assert called == [True]


def test_main_wires_run(workdir, monkeypatch):
    seen = {}
    monkeypatch.setattr(vc, "load_model", lambda cfg: "MODEL")
    monkeypatch.setattr(vc, "mic_frames", lambda device, hop_s: iter([]))
    monkeypatch.setattr(vc, "run", lambda frames, pp, model, cfg, wait=None: seen.update(pp=pp, model=model, cfg=cfg))
    vc.main([])
    assert seen["model"] == "MODEL"
    assert seen["pp"].base == "http://127.0.0.1:50001/v1"
    assert seen["cfg"]["aliases"] == vc.load_aliases(vc.DEFAULT_ALIASES)


def test_main_help_does_not_start_the_loop(monkeypatch, capsys):
    monkeypatch.setattr(vc, "run", lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("run started")))
    vc.main(["--help"])
    assert "verse-cue [--setup]" in capsys.readouterr().out
