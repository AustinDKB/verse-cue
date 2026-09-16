"""Vocal stems for official bench. Mix wavs stay put for alias mining."""

from types import SimpleNamespace

import harvest as hv
from tests.test_lrc import write_wav


def test_isolate_skips_when_dest_exists(tmp_path, monkeypatch):
    dest = tmp_path / "out.wav"
    dest.write_bytes(b"keep")
    monkeypatch.setattr(hv.subprocess, "run", lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("ran")))
    assert hv.isolate(tmp_path / "mix.wav", dest) is True
    assert dest.read_bytes() == b"keep"


def test_isolate_runs_demucs_then_ffmpeg(tmp_path, monkeypatch):
    src = tmp_path / "mix.wav"
    src.write_bytes(b"x")
    dest = tmp_path / "vocals" / "mix.wav"
    calls = []

    def fake_run(cmd, check):
        calls.append(cmd)
        if "-m" in cmd:
            stem = dest.parent / "_demucs" / "htdemucs" / "mix" / "vocals.wav"
            stem.parent.mkdir(parents=True)
            stem.write_bytes(b"stem")
            return SimpleNamespace(returncode=0)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b"16k")
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(hv.subprocess, "run", fake_run)
    assert hv.isolate(src, dest) is True
    assert calls[0][:5] == ["uv", "run", "--with", "demucs", "python"]
    assert calls[0][-1] == str(src)
    assert calls[1][:3] == ["ffmpeg", "-y", "-i"]
    assert calls[1][-1] == str(dest)


def test_vocals_writes_beside_mix_not_over_it(tmp_path, monkeypatch):
    monkeypatch.setattr(hv, "DATA", tmp_path)
    mix = tmp_path / "s.wav"
    mix.write_bytes(b"mix")
    (tmp_path / "s.lrc").write_text("x")
    (tmp_path / "s.txt").write_text("x")
    monkeypatch.setattr(hv, "isolate", lambda src, dest: dest.write_bytes(b"v") or True)
    hv.vocals(10)
    assert mix.read_bytes() == b"mix"
    assert (tmp_path / "vocals" / "s.wav").read_bytes() == b"v"


def test_bench_song_prefers_vocal_stem(tmp_path, monkeypatch, cfg):
    write_wav(tmp_path / "s.wav", 3.0)
    (tmp_path / "s.lrc").write_text("[00:00.00] a b c d\n[00:02.00] e f g h\n")
    (tmp_path / "vocals").mkdir()
    write_wav(tmp_path / "vocals" / "s.wav", 3.0)
    monkeypatch.setattr(hv, "DATA", tmp_path)
    seen = []

    def wrapped(path, hop_s, cell):
        seen.append(path)
        return []

    monkeypatch.setattr(hv, "wav_frames", wrapped)
    monkeypatch.setattr(hv.vc, "run", lambda *_a, **_k: None)
    hv.bench_song(tmp_path / "s.wav", object(), cfg)
    assert seen == [tmp_path / "vocals" / "s.wav"]
