"""Live hop view: transcript plus the current slide, cue words (tail matches) highlighted."""

import io

import verse_cue as vc


def test_paint_dims_unmatched_greens_heard_yellows_cue_tail():
    words = ["our", "god", "is", "an", "awesome", "god", "he", "reigns", "from", "heaven", "above"]
    matched = {0, 1, 7, 8, 9, 10}  # our god … reigns from heaven above
    cue = {8, 9, 10}  # last 3, the words that can arm Next
    out = vc.paint(words, matched, cue)
    assert "\033[2mour\033[0m" not in out  # matched opening is green, not dim
    assert "\033[32mour\033[0m" in out
    assert "\033[2mis\033[0m" in out
    assert "\033[33mheaven\033[0m" in out
    assert "\033[33mabove\033[0m" in out
    assert "\033[32mheaven\033[0m" not in out  # cue wins over heard


def test_cue_set_is_matched_words_at_or_past_the_arm_index():
    # 11 words, tail 3, first_half on -> need max(8, 5) = 8
    assert vc.cue_set(11, {0, 1, 7, 8, 10}, tail=3, first_half=True) == {8, 10}
    assert vc.cue_set(11, {0, 1, 7}, tail=3, first_half=True) == set()


def test_show_prints_transcript_and_painted_current_slide():
    slide = vc.Slide("A", ["our", "god", "reigns", "from", "heaven", "above"])
    slide.raw = ["our", "god", "is", "great"]
    slide.pairs = [(0, 1.0), (4, 2.0), (5, 2.4)]
    buf = io.StringIO()
    vc.show(slide, {"tail_words": 3, "first_half": True}, file=buf)
    text = buf.getvalue()
    assert "heard  our god is great" in text
    assert "slide  " in text
    assert "\033[33mabove\033[0m" in text
    assert "\033[32mour\033[0m" in text


def test_run_writes_display_each_lyric_hop(cfg, tmp_path):
    from tests.conftest import ScriptedModel, ScriptedPP, silent_frames

    buf = io.StringIO()
    cfg["display"] = buf
    windows = [[]] * 4 + [[(1.0, 1.3, "reigns"), (1.4, 1.7, "from"), (1.8, 2.1, "heaven"), (2.2, 2.5, "above")]]
    pp = ScriptedPP([("A", "Our God is an awesome God He reigns from heaven above"), ("B", "x")])
    vc.run(silent_frames([1, 2, 3, 4, 5]), pp, ScriptedModel(windows), cfg, wait=lambda _t: None)
    assert "heard  " in buf.getvalue()
    assert "heaven" in buf.getvalue()
