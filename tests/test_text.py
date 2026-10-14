"""Word normalization, alias inversion, canonicalization order: alias -> fuzzy -> passthrough."""

import json

import verse_cue as vc
from tests.conftest import M, ScriptedModel


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


def test_canon_keeps_slide_words_even_when_aliased():
    # bundled aliases map see->sing, no->new, on->of; a word that is on the slide must survive as heard
    heard = [(0.0, "see"), (0.5, "no"), (1.0, "on"), (1.5, "see")]
    aliases = {"see": "sing", "no": "new", "on": "of"}
    out = vc.canon(heard, {"see", "no", "on", "new"}, aliases, 0.8)
    assert out == heard
    # off the slide, the alias still applies
    assert vc.canon([(0.0, "see")], {"sing"}, aliases, 0.8) == [(0.0, "sing")]


def test_tokens_folds_curly_apostrophes_and_accents():
    assert vc.tokens("You\u2019re my Señor, José \u2018tis") == ["you're", "my", "senor", "jose", "'tis"]


def test_transcribe_folds_like_tokens():
    model = ScriptedModel([[(0.0, 0.2, " You\u2019re"), (0.3, 0.5, " SEÑOR,"), (0.6, 0.8, " you're")]])
    words, _ = vc.transcribe(model, None, 1.0, M, "")
    assert [w for _, w in words] == vc.tokens("You\u2019re Señor you're") == ["you're", "senor", "you're"]
