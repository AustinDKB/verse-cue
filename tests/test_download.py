"""Download pipeline with subprocess and HTTP faked. Nothing touches the network."""

import json
from types import SimpleNamespace

import harvest as hv

LRC = (
    "[00:12.50] Our God is an awesome God\n[00:16.00] He reigns from heaven above\n[00:20.25]\n[00:40.00] With wisdom\n"
)
REC = {"trackName": "Awesome God", "artistName": "Rich Mullins", "syncedLyrics": LRC, "plainLyrics": None}


class FakeResponse:
    def __init__(self, body):
        self.body = body

    def read(self):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False


def test_slug():
    assert hv.slug("Rich Mullins - Awesome God!") == "rich-mullins-awesome-god"


def test_parse_lrc_keeps_empty_marker_lines():
    assert hv.parse_lrc(LRC) == [
        (12.5, "Our God is an awesome God"),
        (16.0, "He reigns from heaven above"),
        (20.25, ""),
        (40.0, "With wisdom"),
    ]


def test_fetch_lyrics_uses_search_and_prefers_synced(monkeypatch):
    hits = [{"syncedLyrics": None, "plainLyrics": "x"}, REC]
    seen = {}

    def fake_urlopen(req, timeout):
        seen["url"] = req.full_url
        seen["ua"] = req.get_header("User-agent")
        return FakeResponse(json.dumps(hits).encode())

    monkeypatch.setattr(hv.urllib.request, "urlopen", fake_urlopen)
    assert hv.fetch_lyrics("Rich Mullins", " Awesome God ") == REC
    assert seen["url"].startswith("https://lrclib.net/api/search?")
    assert "artist_name=Rich+Mullins" in seen["url"]
    assert "track_name=Awesome+God" in seen["url"]
    assert "verse-cue" in seen["ua"]


def test_fetch_lyrics_network_error_is_none(monkeypatch):
    def boom(req, timeout):
        raise OSError("offline")

    monkeypatch.setattr(hv.urllib.request, "urlopen", boom)
    assert hv.fetch_lyrics("a", "b") is None


def test_save_lyrics_writes_lrc_and_plain_text_from_lrc(tmp_path):
    base = tmp_path / "song"
    assert hv.save_lyrics(REC, base) is True
    assert (tmp_path / "song.lrc").read_text() == LRC
    assert (tmp_path / "song.txt").read_text() == "Our God is an awesome God\nHe reigns from heaven above\nWith wisdom"


def test_save_lyrics_none_skips(tmp_path, capsys):
    assert hv.save_lyrics(None, tmp_path / "song") is False
    assert "no synced lyrics" in capsys.readouterr().out


def test_download_audio_builds_yt_dlp_command(tmp_path, monkeypatch):
    calls = []

    def fake_run(cmd, check):
        calls.append(cmd)
        (tmp_path / "x.wav").write_bytes(b"")
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(hv.subprocess, "run", fake_run)
    assert hv.download_audio("Rich Mullins - Awesome God", tmp_path / "x.wav") is True
    cmd = calls[0]
    assert cmd[:2] == ["yt-dlp", "ytsearch1:Rich Mullins - Awesome God"]
    assert "--postprocessor-args" in cmd
    assert cmd[cmd.index("--postprocessor-args") + 1] == "ffmpeg:-ar 16000 -ac 1"
    assert cmd[cmd.index("-o") + 1] == str(tmp_path / "x") + ".%(ext)s"


def test_download_skips_existing_and_malformed_lines(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "songs.txt").write_text("Rich Mullins - Awesome God\nno separator here\nA - B\n")
    data = tmp_path / "data"
    data.mkdir()
    (data / "rich-mullins-awesome-god.wav").write_bytes(b"")
    (data / "rich-mullins-awesome-god.lrc").write_text(LRC)
    (data / "rich-mullins-awesome-god.txt").write_text("x")
    audio_calls, lyric_calls = [], []
    monkeypatch.setattr(hv, "download_audio", lambda q, wav: audio_calls.append(q) or True)
    monkeypatch.setattr(hv, "fetch_lyrics", lambda a, t: lyric_calls.append((a, t)) or None)
    hv.download(limit=10)
    assert audio_calls == ["A - B"]
    assert lyric_calls == [("A", "B")]
    assert "1 songs ready" in capsys.readouterr().out


def test_songs_requires_all_three_files(tmp_path, monkeypatch):
    monkeypatch.setattr(hv, "DATA", tmp_path)
    for stem in ("full", "nolrc"):
        (tmp_path / f"{stem}.wav").write_bytes(b"")
        (tmp_path / f"{stem}.txt").write_text("x")
    (tmp_path / "full.lrc").write_text("x")
    assert [p.stem for p in hv.songs(10)] == ["full"]
