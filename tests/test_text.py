"""Word normalization, alias inversion, canonicalization order: alias -> fuzzy -> passthrough."""

import json

import verse_cue as vc


def test_tokens_lowercases_strips_punctuation_keeps_apostrophes():
    text = "Hallelujah, Name above ALL Names!\n(He's) -- good"
    assert vc.tokens(text) == ["hallelujah", "name", "above", "all", "names", "he's", "good"]


def test_tokens_drops_empty_pieces():
    assert vc.tokens(" -- ... 10,000 ' ") == []


def test_load_aliases_inverts_and_highest_count_wins(tmp_path):
    p = tmp_path / "aliases.json"
    p.write_text(json.dumps({"hallelujah": {"halleluia": 3, "holy": 2}, "holy": {"wholly": 5}, "jesus": {"wholly": 1}}))
    inv = vc.load_aliases(p)
    assert inv["halleluia"] == "hallelujah"
    assert inv["wholly"] == "holy"
    assert "holy" not in inv  # a canonical word is never remapped


def test_load_aliases_missing_file_is_empty(tmp_path):
    assert vc.load_aliases(tmp_path / "nope.json") == {}


def test_load_aliases_cwd_missing_uses_bundled(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    inv = vc.load_aliases()
    assert inv
    assert inv == vc.load_aliases(vc.DEFAULT_ALIASES)


def test_canon_alias_then_fuzzy_then_passthrough():
    heard = [(0.0, "grays"), (0.5, "amazin"), (1.0, "xylophone"), (1.5, "grace")]
    out = vc.canon(heard, {"amazing", "grace"}, {"grays": "grace"}, 0.8)
    assert out == [(0.0, "grace"), (0.5, "amazing"), (1.0, "xylophone"), (1.5, "grace")]
