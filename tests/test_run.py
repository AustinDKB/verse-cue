"""End-to-end loop with scripted model and fake ProPresenter. Times are the capture clock (seconds)."""

import json
from pathlib import Path

import pytest

import verse_cue as vc
from tests.conftest import ScriptedModel, ScriptedPP, silent_frames

SLIDE = "Our God is an awesome God He reigns from heaven above"  # 11 words


def words_at(offsets_words):
    """[(offset_in_window, word)] -> scripted window [(start, end, word)]."""
    return [(o, o + 0.3, w) for o, w in offsets_words]


def run_with(windows, pp, cfg, t_ends):
    waits = []
    model = ScriptedModel(windows)
    vc.run(silent_frames(t_ends), pp, model, cfg, wait=waits.append)
    return model, waits


def test_opening_words_do_not_fire(cfg):
    # first five words of an 11-word slide — still the first half; an operator would wait.
    windows = [[]] * 4 + [words_at([(1.0, "our"), (1.4, "god"), (1.8, "is"), (2.2, "an"), (2.6, "awesome")])]
    pp = ScriptedPP([("A", SLIDE), ("B", "something completely different here")])
    _, waits = run_with(windows, pp, cfg, [1, 2, 3, 4, 5, 6, 7, 8])
    assert pp.fires == []
    assert waits == []


def test_deadline_fire_clicks_after_expected_duration(cfg):
    cfg["decide"]["deadline_fire"] = True
    opening = words_at([(1.0, "our"), (1.4, "god"), (1.8, "is"), (2.2, "an"), (2.6, "awesome")])
    windows = [[]] * 4 + [opening] + [[]] * 6
    pp = ScriptedPP([("A", SLIDE), ("B", "something completely different here")])
    run_with(windows, pp, cfg, [1, 2, 3, 4, 5, 6, 7, 8])
    # entered t=1; 11 * 0.45s = 4.95s; first eligible tick is t=6 even if the tail never arrived
    assert pp.fires == [pytest.approx(6.0, abs=0.05)]


def test_deadline_fire_does_not_click_without_matches(cfg):
    cfg["decide"]["deadline_fire"] = True
    pp = ScriptedPP([("A", SLIDE), ("B", "x")])
    run_with([[]] * 20, pp, cfg, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    assert pp.fires == []


def test_deadline_fire_uses_configured_sec_per_word(cfg):
    cfg["decide"]["deadline_fire"] = True
    cfg["decide"]["deadline_sec_per_word"] = 1.0
    opening = words_at([(1.0, "our"), (1.4, "god"), (1.8, "is"), (2.2, "an"), (2.6, "awesome")])
    windows = [[]] * 4 + [opening] + [[]] * 12
    pp = ScriptedPP([("A", SLIDE), ("B", "something completely different here")])
    run_with(windows, pp, cfg, list(range(1, 15)))
    # entered t=1; 11 * 1.0s = 11s; first eligible tick is t=12
    assert pp.fires == [pytest.approx(12.0, abs=0.05)]


def test_identical_consecutive_slides_do_not_double_fire(cfg):
    tail = words_at([(2.0, "reigns"), (2.4, "from"), (2.8, "heaven"), (3.2, "above")])  # window t_end=5, start 1
    held = words_at([(3.5, "above")])  # window t_end=7, start 3 -> capture 6.5, one word only
    windows = [[]] * 4 + [tail, [], held, [], []]
    pp = ScriptedPP([("A", SLIDE), ("B", SLIDE), ("C", "x")])
    run_with(windows, pp, cfg, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert len(pp.fires) == 1


def test_blank_slide_fires_on_voice_after_settle(cfg, monkeypatch):
    monkeypatch.setattr(vc, "speech_in", lambda chunk, blank: True)
    pp = ScriptedPP([("BL", ""), ("A", SLIDE)])
    run_with([[]] * 10, pp, cfg, [1, 2, 3, 4])
    # entered at t=1, blank_settle_s=1.0 -> first eligible tick is t=2
    assert pp.fires == [2]


def test_no_slide_showing_never_fires(cfg, monkeypatch):
    monkeypatch.setattr(vc, "speech_in", lambda chunk, blank: True)
    pp = ScriptedPP([("", "")])
    run_with([[]] * 10, pp, cfg, [1, 2, 3, 4, 5])
    assert pp.fires == []


def test_operator_change_during_inference_cancels_fire(cfg):
    class SwitchingPP(ScriptedPP):
        def slide(self):
            if self.reads == 5:  # the re-check inside fire() after the 5th window
                self.set(1)
            return super().slide()

    # window t_end=5 (start 1.0): the whole tail at captures 2.0..3.2 -> matched 4 -> would fire at ~5.0
    windows = [[]] * 4 + [words_at([(1.0, "reigns"), (1.4, "from"), (1.8, "heaven"), (2.2, "above")])]
    pp = SwitchingPP([("A", SLIDE), ("B", "other")])
    run_with(windows, pp, cfg, [1, 2, 3, 4, 5])
    assert pp.fires == []


def test_operator_change_resets_progress(cfg):
    # The operator jumps to slide B at t=4. Hearing slide A's tail afterwards must not fire;
    # hearing slide B's tail must.
    slide_b = "we will sing your praise forever and ever amen"  # 9 words -> min_matched = min(4, 5) = 4
    a_tail = words_at([(3.0, "reigns"), (3.4, "from"), (3.8, "heaven"), (4.2, "above")])  # window t=6, start 2
    b_tail = words_at([(2.0, "forever"), (2.4, "and"), (2.8, "ever"), (3.2, "amen")])  # window t=8, start 4
    windows = [[]] * 5 + [a_tail, [], b_tail, [], []]
    pp = ScriptedPP([("A", SLIDE), ("B", slide_b), ("C", "x")])

    def frames():
        for t in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            if t == 4:
                pp.set(1)
            yield from silent_frames([t])

    vc.run(frames(), pp, ScriptedModel(windows), cfg, wait=lambda _t: None)
    # b_tail captures 6.0..7.2 -> predicted 7.2 - 0.3 = 6.9 -> fired at now ~= 8.0
    assert len(pp.fires) == 1
    assert pp.fires[0] == pytest.approx(8.0, abs=0.05)
    rows = [json.loads(line) for line in Path(cfg["metrics_file"]).read_text().splitlines()]
    assert [(r["event"], r["uuid"]) for r in rows] == [("enter", "A"), ("enter", "B"), ("fire", "B"), ("enter", "C")]


def test_metrics_log_has_enter_and_fire_rows(cfg):
    windows = [[]] * 4 + [words_at([(1.0, "reigns"), (1.4, "from"), (1.8, "heaven"), (2.2, "above")])]
    pp = ScriptedPP([("A", SLIDE), ("B", "other")])
    run_with(windows, pp, cfg, [1, 2, 3, 4, 5, 6])
    rows = [json.loads(line) for line in Path(cfg["metrics_file"]).read_text().splitlines()]
    events = [r["event"] for r in rows]
    assert events == ["enter", "fire", "enter"]
    fire = rows[1]
    assert fire["uuid"] == "A"
    assert fire["n_words"] == 11
    assert fire["matched"] == 4
    assert fire["idx_from_end"] == 0
    assert fire["window_s"] == 4.0


def test_sleep_until_does_not_sleep_for_the_past(monkeypatch):
    slept = []
    monkeypatch.setattr(vc.time, "sleep", slept.append)
    vc.sleep_until(vc.time.monotonic() - 10)
    assert slept == [0.0]


def _keys(*hops):
    seq = iter(hops)
    return lambda: next(seq, [])


def test_toggle_pause_flips_once_per_hop():
    assert vc.toggle_pause(pause=False, keys=lambda: [" "]) is True
    assert vc.toggle_pause(pause=True, keys=lambda: ["p"]) is False
    assert vc.toggle_pause(pause=False, keys=lambda: ["x"]) is False
    assert vc.toggle_pause(pause=True, keys=lambda: [" ", "p"]) is False


def test_pending_keys_empty_when_stdin_is_not_a_tty(monkeypatch):
    monkeypatch.setattr(vc.sys.stdin, "isatty", lambda: False)
    assert vc.pending_keys() == []


def test_pause_skips_detection_and_does_not_fire(cfg):
    tail = words_at([(1.0, "reigns"), (1.4, "from"), (1.8, "heaven"), (2.2, "above")])
    windows = [[]] * 4 + [tail]
    pp = ScriptedPP([("A", SLIDE), ("B", "other")])
    cfg["keys"] = _keys([" "], [], [], [], [], [])
    vc.run(silent_frames([1, 2, 3, 4, 5, 6]), pp, ScriptedModel(windows), cfg, wait=lambda _t: None)
    assert pp.fires == []


def test_resume_detects_again_after_pause(cfg):
    tail = words_at([(1.0, "reigns"), (1.4, "from"), (1.8, "heaven"), (2.2, "above")])
    windows = [[]] * 4 + [tail]
    pp = ScriptedPP([("A", SLIDE), ("B", "other")])
    cfg["keys"] = _keys([" "], [], [], [], [" "], [], [], [], [])
    vc.run(silent_frames([1, 2, 3, 4, 5, 6, 7, 8, 9]), pp, ScriptedModel(windows), cfg, wait=lambda _t: None)
    assert len(pp.fires) == 1
