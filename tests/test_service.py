"""Service bundle (live side), review, commentary and service replay."""

import json
import math
import wave
from pathlib import Path

import numpy as np
import pytest

import harvest as hv
import verse_cue as vc
from tests.conftest import ScriptedModel, ScriptedPP
from tests.test_lrc import write_wav


def row(event, uuid, entered, fired_at=None, words=("a",)):
    return {
        "event": event,
        "uuid": uuid,
        "entered": entered,
        "fired_at": fired_at,
        "blank": not words,
        "words": list(words),
    }


def write_log(folder: Path, rows) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "slides.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (folder / "meta.json").write_text(json.dumps({"t0": 100.0}))
    return folder


def fake_service(tmp_path) -> Path:
    # A start; we fire A->B; operator B->C (B was a miss); we fire C->D, operator goes back D->C (early); operator C->E (miss).
    rows = [
        row("enter", "A", 100.0),
        row("fire", "A", 100.0, 110.0),
        row("enter", "B", 110.0),
        row("enter", "C", 120.0),
        row("fire", "C", 120.0, 126.0),
        row("enter", "D", 126.0),
        row("enter", "C", 128.0),
        row("enter", "E", 140.0),
    ]
    return write_log(tmp_path / "svc", rows)


def test_review_counts_and_per_slide_flags(tmp_path):
    r = hv.review(fake_service(tmp_path))
    assert r["counts"] == {"slide_changes": 5, "ours": 2, "operator_overrides": 3, "misses": 2, "early_reverted": 1}
    kinds = [s["change"] for s in r["slides"]]
    assert kinds == ["start", "ours", "operator", "ours", "operator", "operator"]
    assert r["slides"][1]["miss"] is True  # B: we never fired, the operator moved on
    assert r["slides"][2]["early_reverted"] is True  # the fire off C was undone within 5 s
    assert r["slides"][1]["start"] == 10.0
    assert json.loads((tmp_path / "svc" / "review.json").read_text())["counts"] == r["counts"]


def test_review_fire_that_changed_nothing_leaves_the_change_to_the_operator(tmp_path):
    # our press at 105 did nothing (trigger failed); the operator moved A->B by hand at 112
    svc = write_log(
        tmp_path / "svc", [row("enter", "A", 100.0), row("fire", "A", 100.0, 105.0), row("enter", "B", 112.0)]
    )
    r = hv.review(svc)
    assert [s["change"] for s in r["slides"]] == ["start", "operator"]
    assert r["slides"][0]["miss"] is True
    assert r["counts"]["operator_overrides"] == 1 and r["counts"]["misses"] == 1


def test_review_late_step_back_is_still_a_miss(tmp_path):
    # we fire A->B; B sits 10 s with no fire; the operator goes back to A: not an early fire, so B was missed
    svc = write_log(
        tmp_path / "svc",
        [row("enter", "A", 100.0), row("fire", "A", 100.0, 110.0), row("enter", "B", 110.0), row("enter", "A", 120.0)],
    )
    r = hv.review(svc)
    assert r["slides"][0]["early_reverted"] is False
    assert r["slides"][1]["miss"] is True


def test_review_cli_prints_summary(tmp_path, capsys, workdir):
    hv.main(["review", str(fake_service(tmp_path))])
    out = capsys.readouterr().out
    assert "ours 2" in out and "misses 2" in out and "early fires reverted 1" in out


def test_save_frames_streams_wav_and_meta(tmp_path):
    chunk = np.full(vc.SR, 0.5, dtype=np.float32)
    got = list(vc.save_frames(iter([(5.0, chunk), (6.0, chunk)]), tmp_path / "s"))
    assert [t for t, _ in got] == [5.0, 6.0]
    with wave.open(str(tmp_path / "s" / "audio.wav")) as w:
        assert (w.getframerate(), w.getnchannels(), w.getnframes()) == (vc.SR, 1, 2 * vc.SR)
    assert json.loads((tmp_path / "s" / "meta.json").read_text())["t0"] == pytest.approx(4.0)


def test_run_writes_transcript_and_slide_words(cfg, tmp_path):
    cfg["transcript_file"] = str(tmp_path / "transcript.jsonl")
    pp = ScriptedPP([("A", "hello there world")])
    words = [(0.0, 0.3, "hello")]
    from tests.conftest import silent_frames

    vc.run(silent_frames([1, 2]), pp, ScriptedModel([words, words]), cfg, wait=lambda _t: None)
    lines = [json.loads(x) for x in (tmp_path / "transcript.jsonl").read_text().splitlines()]
    assert lines == [{"t": 1, "text": "hello"}, {"t": 2, "text": "hello"}]
    first = json.loads(Path(cfg["metrics_file"]).read_text().splitlines()[0])
    assert first["words"] == ["hello", "there", "world"]


def test_stt_text_prefers_text_then_final_segments():
    assert hv.stt_text({"text": " hi there "}) == "hi there"
    assert (
        hv.stt_text(
            {"segments": [{"text": "one", "is_final": True}, {"text": "x", "is_final": False}, {"text": "two"}]}
        )
        == "one two"
    )


def test_load_key_env_then_file_and_missing(tmp_path):
    keyfile = tmp_path / "k.env"
    keyfile.write_text("OTHER=1\nXAI_API_KEY='sekret'\n")
    cfg = {"commentary": {"key_file": str(keyfile)}}
    assert hv.load_key(cfg, env={"XAI_API_KEY": "fromenv"}) == "fromenv"
    assert hv.load_key(cfg, env={}) == "sekret"
    with pytest.raises(SystemExit):
        hv.load_key({"commentary": {"key_file": str(tmp_path / "nope")}}, env={})


def test_comment_with_file_saves_txt_and_json(tmp_path, monkeypatch):
    monkeypatch.setenv("XAI_API_KEY", "k")
    clip = tmp_path / "in.wav"
    write_wav(clip, 1.0)
    svc = tmp_path / "svc"
    svc.mkdir()
    seen = {}

    def post(audio, key):
        seen["key"], seen["n"] = key, len(audio)
        return {"text": "the second verse came late", "duration": 1.0}

    text = hv.comment(svc, {}, clip, post=post)
    assert text == "the second verse came late"
    assert seen["key"] == "k" and seen["n"] > 44
    (take,) = svc.glob("commentary-*.wav")
    assert take.with_suffix(".txt").read_text() == "the second verse came late\n"
    assert json.loads(take.with_suffix(".json").read_text())["duration"] == 1.0
    assert (svc / "commentary.txt").read_text() == f"[{take.stem}] the second verse came late\n"


def test_comment_second_take_keeps_the_first(tmp_path, monkeypatch):
    monkeypatch.setenv("XAI_API_KEY", "k")
    clip = tmp_path / "in.wav"
    write_wav(clip, 1.0)
    svc = tmp_path / "svc"
    svc.mkdir()
    replies = iter(["first thought", "second thought"])
    hv.comment(svc, {}, clip, post=lambda _a, _k: {"text": next(replies)})
    hv.comment(svc, {}, clip, post=lambda _a, _k: {"text": next(replies)})
    assert sorted(t.read_text() for t in svc.glob("commentary-*.txt")) == ["first thought\n", "second thought\n"]
    assert len(list(svc.glob("commentary-*.wav"))) == 2
    lines = (svc / "commentary.txt").read_text().splitlines()
    assert [x.split("] ", 1)[1] for x in lines] == ["first thought", "second thought"]


def test_comment_network_failure_keeps_take_and_names_it(tmp_path, monkeypatch):
    monkeypatch.setenv("XAI_API_KEY", "k")
    clip = tmp_path / "in.wav"
    write_wav(clip, 1.0)
    svc = tmp_path / "svc"
    svc.mkdir()

    def down(_audio, _key):
        raise hv.urllib.error.URLError("no route to host")

    with pytest.raises(SystemExit) as e:
        hv.comment(svc, {}, clip, post=down)
    (take,) = svc.glob("commentary-*.wav")
    assert str(take) in str(e.value)
    assert not (svc / "commentary.txt").exists()
    assert hv.comment(svc, {}, take, post=lambda _a, _k: {"text": "retried"}) == "retried"
    assert list(svc.glob("commentary-*.wav")) == [take]
    assert (svc / "commentary.txt").read_text() == f"[{take.stem}] retried\n"


def test_pick_device_matches_name_any_case_else_default(capsys):
    devices = [
        {"name": "Speakers (Realtek)", "max_input_channels": 0},
        {"name": "Microphone (Realtek)", "max_input_channels": 2},
        {"name": "Microphone (Blue Snowball)", "max_input_channels": 1},
    ]
    assert hv.pick_device(devices, "snowball") == 2
    assert capsys.readouterr().out == ""
    assert hv.pick_device(devices, "Yeti") is None
    out = capsys.readouterr().out
    assert "Yeti" in out and "Microphone (Realtek)" in out and "Speakers" not in out
    assert hv.pick_device(devices, "") is None


def test_to_16k_resamples_length_and_tone():
    rate = 48000
    t = np.arange(rate) / rate
    out = hv.to_16k(np.sin(2 * np.pi * 440 * t).astype(np.float32), rate)
    assert len(out) == vc.SR
    expected = np.sin(2 * np.pi * 440 * np.arange(vc.SR) / vc.SR)
    assert np.max(np.abs(out - expected)) < 0.01
    assert len(hv.to_16k(np.zeros(44100, np.float32), 44100)) == vc.SR


def test_unused_never_reuses_a_taken_name(tmp_path):
    first = tmp_path / "2026-10-25_0930"
    assert vc.unused(first) == first
    first.mkdir()
    assert vc.unused(first) == tmp_path / "2026-10-25_0930-2"
    (tmp_path / "2026-10-25_0930-2").mkdir()
    assert vc.unused(first) == tmp_path / "2026-10-25_0930-3"
    (tmp_path / "commentary-093000.wav").write_bytes(b"")
    assert vc.unused(tmp_path / "commentary-093000.wav") == tmp_path / "commentary-093000-2.wav"


def test_stt_post_builds_multipart(monkeypatch):
    sent = {}

    class Resp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self, *a):
            return b'{"text": "ok"}'

    def fake_open(req, timeout):
        sent["req"] = req
        return Resp()

    monkeypatch.setattr(hv.urllib.request, "urlopen", fake_open)
    assert hv.stt_post(b"RIFFdata", "k") == {"text": "ok"}
    req = sent["req"]
    assert req.full_url == "https://api.x.ai/v1/stt" and req.get_header("Authorization") == "Bearer k"
    assert b"grok-voice-transcribe-2.0" in req.data and b"RIFFdata" in req.data and b'name="file"' in req.data


def test_bench_service_scores_operator_changes_only(tmp_path):
    svc = write_log(
        tmp_path / "svc",
        [
            row("enter", "A", 100.0, words=("our", "god", "is", "an", "awesome", "god")),
            row("enter", "B", 104.0, words=("he", "reigns", "from", "heaven")),
            row("enter", "C", 108.0, words=("x",)),
        ],
    )
    write_wav(svc / "audio.wav", 12.0)
    cfg = vc.load_config(hv.Path(__file__).resolve().parents[1] / "verse-cue.toml", tmp_path / "none.toml")
    cfg["aliases"], cfg["display"] = {}, None
    r = hv.bench_service(svc, ScriptedModel([]), cfg)
    assert r["operator_changes"] == 2
    assert all(math.isnan(d) for d in r["deltas"])  # silence: the model never fires, both are misses
    assert r["lengths"] == [4.0, 4.0]


def test_bench_service_replays_a_step_back_as_one_slide(tmp_path):
    # we fire A->B at 104, the operator steps back to A at 106, then moves A->C at 110: truth for A is 110
    svc = write_log(
        tmp_path / "svc",
        [
            row("enter", "A", 100.0, words=("our", "god")),
            row("fire", "A", 100.0, 104.0),
            row("enter", "B", 104.0, words=("he", "reigns")),
            row("enter", "A", 106.0, words=("our", "god")),
            row("enter", "C", 110.0, words=("x",)),
        ],
    )
    write_wav(svc / "audio.wav", 14.0)
    cfg = vc.load_config(hv.Path(__file__).resolve().parents[1] / "verse-cue.toml", tmp_path / "none.toml")
    cfg["aliases"], cfg["display"] = {}, None
    r = hv.bench_service(svc, ScriptedModel([]), cfg)
    assert r["operator_changes"] == 1
    assert r["lengths"] == [10.0]


def test_bench_services_resolves_empty_model_name_from_hardware(tmp_path, monkeypatch):
    seen = []
    monkeypatch.setattr(hv, "get_model", lambda *a: seen.append(a) or "model")
    monkeypatch.setattr(vc, "gpu_gb", lambda: 0.0)
    monkeypatch.setattr(hv, "bench_service", lambda _s, _m, _c: {"deltas": [], "lengths": [], "operator_changes": 0})
    cfg = {"model": {"name": "", "compute_type": "auto"}, "hardware": {"gpu": [], "cpu": ["small.en", "int8"]}}
    hv.bench_services(cfg, tmp_path)
    assert seen == [("small.en", "int8")]


def test_bench_service_refuses_old_log(tmp_path):
    svc = write_log(tmp_path / "svc", [{**row("enter", "A", 100.0), "words": None}])
    write_wav(svc / "audio.wav", 2.0)
    with pytest.raises(SystemExit):
        hv.bench_service(svc, ScriptedModel([]), {"model": {"hop_s": 1.0}})
