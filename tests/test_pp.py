"""HTTP client against ProPresenter's two endpoints, and the VAD gate."""

import json

import numpy as np

import verse_cue as vc


class FakeResponse:
    def __init__(self, body):
        self.body = body

    def read(self):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False


def patch_urlopen(monkeypatch, bodies):
    """bodies: list of bytes or Exception instances, consumed in order. Returns the list of URLs hit."""
    urls = []

    def fake(url, timeout):
        urls.append((url, timeout))
        body = bodies.pop(0)
        if isinstance(body, Exception):
            raise body
        return FakeResponse(body)

    monkeypatch.setattr(vc.urllib.request, "urlopen", fake)
    return urls


def test_slide_reads_current_uuid_and_text(monkeypatch):
    body = json.dumps({"current": {"uuid": "A", "text": "Amazing grace", "notes": ""}, "next": None}).encode()
    urls = patch_urlopen(monkeypatch, [body])
    pp = vc.ProPresenter("127.0.0.1", 50001)
    assert pp.slide() == ("A", "Amazing grace")
    assert urls == [("http://127.0.0.1:50001/v1/status/slide", 1)]


def test_slide_null_current_means_no_slide(monkeypatch):
    patch_urlopen(monkeypatch, [json.dumps({"current": None, "next": None}).encode()])
    assert vc.ProPresenter("h", 1).slide() == ("", "")


def test_slide_unreachable_keeps_last_known_and_warns(monkeypatch, capsys):
    ok = json.dumps({"current": {"uuid": "A", "text": "x", "notes": ""}}).encode()
    patch_urlopen(monkeypatch, [ok, OSError("down"), b"not json"])
    pp = vc.ProPresenter("h", 1)
    assert pp.slide() == ("A", "x")
    assert pp.slide() == ("A", "x")
    assert pp.slide() == ("A", "x")
    assert "unreachable" in capsys.readouterr().err


def test_next_hits_trigger_endpoint(monkeypatch):
    urls = patch_urlopen(monkeypatch, [b"{}"])
    vc.ProPresenter("h", 2).next(at=1.0)
    assert urls[0][0] == "http://h:2/v1/trigger/next"


def test_next_survives_errors(monkeypatch, capsys):
    patch_urlopen(monkeypatch, [OSError("down")])
    vc.ProPresenter("h", 2).next(at=1.0)
    assert "trigger failed" in capsys.readouterr().err


def test_speech_in_silence_is_false():
    assert vc.speech_in(np.zeros(vc.SR, dtype=np.float32), {"min_speech_ms": 300}) is False
