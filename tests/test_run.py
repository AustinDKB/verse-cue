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


TAIL = [(2.0, "reigns"), (2.4, "from"), (2.8, "heaven"), (3.2, "above")]  # capture times of one sung pass


def heard_again(t_ends, window_s=4.0):
    """Whisper re-hears the same tail in every overlapping window: same capture times, shifted offsets."""
    return [words_at([(c - (t - window_s), w) for c, w in TAIL if c >= t - window_s]) for t in t_ends]


def test_same_uuid_slides_fire_once_per_sung_pass(cfg):
    # ProPresenter can show consecutive slides under one uuid; one pass of the tail is one Next, not one per hop.
    windows = [[]] * 4 + heard_again([5, 6, 7, 8])
    pp = ScriptedPP([("A", SLIDE)] * 3 + [("B", "x")])
    run_with(windows, pp, cfg, [1, 2, 3, 4, 5, 6, 7, 8])
    assert pp.fires == [pytest.approx(5.0, abs=0.05)]


class LaggingPP(ScriptedPP):
    """/status/slide keeps reporting the old slide for two reads after a trigger."""

    def __init__(self, slides):
        super().__init__(slides)
        self.lag = 0

    def slide(self):
        if self.lag:
            self.lag -= 1
            self.reads += 1
            return self.slides[self.i - 1]
        return super().slide()

    def next(self, at):
        super().next(at)
        self.lag = 2


def test_lagging_status_after_trigger_does_not_fire_again(cfg):
    windows = [[]] * 4 + heard_again([5, 6, 7, 8])
    pp = LaggingPP([("A", SLIDE), ("B", "something completely different here")])
    run_with(windows, pp, cfg, [1, 2, 3, 4, 5, 6, 7, 8])
    assert len(pp.fires) == 1


def test_same_uuid_slides_with_different_text_fire_once_each(cfg):
    # each same-uuid slide aligns against its own words, not the words of the slide that just fired
    second = "we will sing your praise forever and ever amen"
    third = "holy holy holy lord god almighty early in the morning"
    a_tail = words_at([(1.0, "reigns"), (1.4, "from"), (1.8, "heaven"), (2.2, "above")])  # window t=5, start 1
    b_tail = words_at([(2.5, "forever"), (2.9, "and"), (3.3, "ever"), (3.7, "amen")])  # window t=8, start 4
    c_tail = words_at([(2.5, "early"), (2.9, "in"), (3.3, "the"), (3.7, "morning")])  # window t=11, start 7
    windows = [[]] * 4 + [a_tail, [], [], b_tail, [], [], c_tail, [], []]
    pp = ScriptedPP([("A", SLIDE), ("A", second), ("A", third), ("B", "x")])
    run_with(windows, pp, cfg, list(range(1, 14)))
    assert pp.fires == [pytest.approx(5.0, abs=0.05), pytest.approx(8.0, abs=0.05), pytest.approx(11.0, abs=0.05)]


def test_lagging_status_after_blank_fire_does_not_fire_again(cfg, monkeypatch):
    # the congregation sings the next slide while the status still reports the blank one
    monkeypatch.setattr(vc, "speech_in", lambda chunk, blank: True)
    pp = LaggingPP([("BL", ""), ("A", SLIDE)])
    run_with([[]] * 10, pp, cfg, [1, 2, 3, 4, 5, 6])
    assert pp.fires == [2]


def test_consecutive_same_uuid_blank_slides_both_advance(cfg, monkeypatch):
    # after the fire at t=2 the second blank waits max(1.0, 2 * 1.0) + 1.0 = 3s, then fires on voice
    monkeypatch.setattr(vc, "speech_in", lambda chunk, blank: True)
    pp = ScriptedPP([("BL", ""), ("BL", ""), ("A", SLIDE)])
    run_with([[]] * 10, pp, cfg, [1, 2, 3, 4, 5, 6, 7, 8])
    assert pp.fires == [2, 5]


class FailingPP(ScriptedPP):
    """/status/slide times out on the reads listed in `fail` (1-based read count), like ProPresenter.slide()."""

    def __init__(self, slides, fail):
        super().__init__(slides)
        self.fail = set(fail)

    def slide(self):
        read = super().slide()
        return None if self.reads in self.fail else read


def test_failed_reads_after_trigger_do_not_fire_on_stale_slide(cfg):
    # read 5 is the pre-Next check; reads 6 and 7 time out right after the trigger
    windows = [[]] * 4 + heard_again([5, 6, 7, 8])
    pp = FailingPP([("A", SLIDE), ("B", "something completely different here")], fail={6, 7})
    run_with(windows, pp, cfg, [1, 2, 3, 4, 5, 6, 7, 8])
    assert len(pp.fires) == 1


def test_failed_read_skips_the_tick_and_the_cue_retries_next_hop(cfg):
    # tick t=5 would fire, but its status read (read 5) fails: skip it, fire on the t=6 hop instead of never
    windows = [[]] * 4 + heard_again([6, 7])
    pp = FailingPP([("A", SLIDE), ("B", "x")], fail={5})
    run_with(windows, pp, cfg, [1, 2, 3, 4, 5, 6, 7])
    assert pp.fires == [pytest.approx(6.0, abs=0.05)]


def test_failed_read_before_next_holds_the_press_and_retries(cfg):
    # read 6 is the check right before Next at t=5: unreadable, so no press; the t=6 hop fires
    windows = [[]] * 4 + heard_again([5, 6, 7])
    pp = FailingPP([("A", SLIDE), ("B", "x")], fail={6})
    run_with(windows, pp, cfg, [1, 2, 3, 4, 5, 6, 7])
    assert pp.fires == [pytest.approx(6.0, abs=0.05)]


def test_operator_next_during_fire_wait_does_not_double_advance(cfg):
    windows = [[]] * 4 + heard_again([5])
    pp = ScriptedPP([("A", SLIDE), ("B", "other"), ("C", "third")])
    # the operator presses Next while fire() sleeps toward the fire time
    vc.run(silent_frames([1, 2, 3, 4, 5]), pp, ScriptedModel(windows), cfg, wait=lambda _t: pp.set(1))
    assert pp.fires == []
    assert pp.i == 1


B_SUNG = [(5.5, "something"), (5.9, "completely"), (6.3, "different"), (6.7, "here")]  # sung right after the t=5 Next


def test_line_sung_while_status_lags_still_fires_the_next_slide(cfg):
    # slide B's whole line is sung while /status/slide still reports A; B dates from the Next, not the first fresh read
    b = [words_at([(c - (t - 4.0), w) for c, w in B_SUNG]) for t in (7, 8)]
    windows = [[]] * 4 + [heard_again([5])[0], [], *b]
    pp = LaggingPP([("A", SLIDE), ("B", "something completely different here"), ("C", "x")])
    run_with(windows, pp, cfg, [1, 2, 3, 4, 5, 6, 7, 8])
    assert pp.fires == [pytest.approx(5.0, abs=0.05), pytest.approx(8.0, abs=0.05)]


def test_line_sung_while_status_reads_fail_still_fires_the_next_slide(cfg):
    # read 6 is the check before the t=5 Next; the t=6 and t=7 reads time out while B is sung
    windows = [[]] * 4 + [heard_again([5])[0], words_at([(c - 4.0, w) for c, w in B_SUNG])]
    pp = FailingPP([("A", SLIDE), ("B", "something completely different here"), ("C", "x")], fail={7, 8})
    run_with(windows, pp, cfg, [1, 2, 3, 4, 5, 6, 7, 8])
    assert pp.fires == [pytest.approx(5.0, abs=0.05), pytest.approx(8.0, abs=0.05)]


def test_line_sung_while_status_lags_after_blank_fire_still_fires(cfg, monkeypatch):
    # blank fires at t=2; A's tail is sung at 2.5-3.7 while the status still reports the blank
    monkeypatch.setattr(vc, "speech_in", lambda chunk, blank: True)
    a_tail = words_at([(1.5, "reigns"), (1.9, "from"), (2.3, "heaven"), (2.7, "above")])  # window t=5, start 1
    pp = LaggingPP([("BL", ""), ("A", SLIDE), ("B", "x")])
    run_with([a_tail], pp, cfg, [1, 2, 3, 4, 5])
    assert pp.fires == [2, pytest.approx(5.0, abs=0.05)]


GAP_SLIDES = [("A", SLIDE), ("B", "something completely different here"), ("C", "x")]


def test_fire_inside_the_gap_waits_then_fires(cfg):
    # A fires at t=5; B's tail predicts t=6, inside the 2 s gap: wait until t=7 and press, never drop
    b_tail = words_at([(3.4, "something"), (3.5, "completely"), (3.6, "different"), (3.7, "here")])  # window t=6
    windows = [[]] * 4 + [heard_again([5])[0], b_tail]
    pp = ScriptedPP(GAP_SLIDES)
    _, waits = run_with(windows, pp, cfg, [1, 2, 3, 4, 5, 6])
    assert pp.fires == [pytest.approx(5.0, abs=0.05), pytest.approx(7.0, abs=0.05)]
    assert waits[-1] == pytest.approx(7.0, abs=0.05)


def test_fire_just_after_operator_change_waits_for_the_gap(cfg):
    # the operator moves to A at t=5 (first seen then); A's tail at t=6 waits until t=7
    a_tail = words_at([(3.4, "reigns"), (3.5, "from"), (3.6, "heaven"), (3.7, "above")])  # window t=6
    windows = [[]] * 5 + [a_tail]
    pp = ScriptedPP([("Z", "intro"), *GAP_SLIDES])
    frames = silent_frames([1, 2, 3, 4, 5, 6])

    def operator(frames):
        for t, chunk in frames:
            if t == 5:
                pp.set(1)
            yield t, chunk

    vc.run(operator(frames), pp, ScriptedModel(windows), cfg, wait=lambda _t: None)
    assert pp.fires == [pytest.approx(7.0, abs=0.05)]


def test_fire_outside_the_gap_is_unchanged(cfg):
    windows = [[]] * 4 + heard_again([5])
    pp = ScriptedPP(GAP_SLIDES)
    _, waits = run_with(windows, pp, cfg, [1, 2, 3, 4, 5])
    assert pp.fires == [pytest.approx(5.0, abs=0.05)]
    assert waits == [pytest.approx(5.0, abs=0.05)]


def test_operator_press_during_gap_wait_cancels_the_press(cfg):
    b_tail = words_at([(3.4, "something"), (3.5, "completely"), (3.6, "different"), (3.7, "here")])
    windows = [[]] * 4 + [heard_again([5])[0], b_tail]
    pp = ScriptedPP(GAP_SLIDES)

    def wait(t):
        if t > 6.5:  # the delayed wait for B: the operator presses Next meanwhile
            pp.set(2)

    vc.run(silent_frames([1, 2, 3, 4, 5, 6]), pp, ScriptedModel(windows), cfg, wait=wait)
    assert pp.fires == [pytest.approx(5.0, abs=0.05)]
    assert pp.i == 2


def test_operator_change_after_blank_startup_waits_for_the_gap(cfg):
    # nothing on screen at startup; the operator moves to A at t=5; A's tail at t=6 waits until t=7
    a_tail = words_at([(3.4, "reigns"), (3.5, "from"), (3.6, "heaven"), (3.7, "above")])  # window t=6
    windows = [[], a_tail]  # a blank screen never runs the model: windows start at t=5
    pp = ScriptedPP([("", ""), *GAP_SLIDES])

    def operator(frames):
        for t, chunk in frames:
            if t == 5:
                pp.set(1)
            yield t, chunk

    vc.run(operator(silent_frames([1, 2, 3, 4, 5, 6])), pp, ScriptedModel(windows), cfg, wait=lambda _t: None)
    assert pp.fires == [pytest.approx(7.0, abs=0.05)]


def test_config_without_min_gap_still_holds_two_seconds(cfg):
    del cfg["decide"]["min_gap_s"]
    b_tail = words_at([(3.4, "something"), (3.5, "completely"), (3.6, "different"), (3.7, "here")])  # window t=6
    windows = [[]] * 4 + [heard_again([5])[0], b_tail]
    pp = ScriptedPP(GAP_SLIDES)
    run_with(windows, pp, cfg, [1, 2, 3, 4, 5, 6])
    assert pp.fires == [pytest.approx(5.0, abs=0.05), pytest.approx(7.0, abs=0.05)]
