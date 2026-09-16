"""Sequence alignment of heard words to slide words, and the fire-time prediction."""

import pytest

import verse_cue as vc
from tests.conftest import D

SLIDE = vc.tokens("Our God is an awesome God He reigns from heaven above")  # 11 words, idx 0..10


def test_align_maps_slide_index_to_capture_time_in_order():
    heard = [(1.0, "our"), (1.4, "god"), (1.8, "is"), (2.2, "an"), (2.6, "awesome")]
    assert vc.align(SLIDE, heard) == [(0, 1.0), (1, 1.4), (2, 1.8), (3, 2.2), (4, 2.6)]


def test_align_skips_garbage_and_places_repeated_word_by_context():
    heard = [(1.0, "uh"), (1.4, "god"), (1.8, "is"), (2.2, "an"), (2.6, "awesome"), (3.0, "god"), (3.4, "he")]
    assert [i for i, _ in vc.align(SLIDE, heard)] == [1, 2, 3, 4, 5, 6]


def test_align_nothing_heard():
    assert vc.align(SLIDE, []) == []


def test_predict_none_below_min_matched():
    assert vc.predict([(0, 1.0), (1, 1.4)], 11, D) is None


def test_predict_none_until_heard_slide_tail():
    # first five words of an 11-word slide — a human would not click yet
    pairs = [(0, 1.0), (1, 1.4), (2, 1.8), (3, 2.2), (4, 2.6)]
    assert vc.predict(pairs, 11, D) is None


def test_predict_none_on_sixth_last_when_tail_is_three():
    d = {**D, "tail_words": 3}
    # idx 5 is 6th-last of 11; wait until 3rd-last (idx 8+)
    pairs = [(1, 1.0), (2, 1.4), (3, 1.8), (4, 2.2), (5, 2.6)]
    assert vc.predict(pairs, 11, d) is None


def test_predict_none_in_first_half_even_if_in_tail_window():
    # 8-word slide: last-6 starts at idx 2, but first half ends at idx 3
    d = {**D, "tail_words": 6, "min_matched": 4}
    pairs = [(0, 1.0), (1, 1.4), (2, 1.8), (3, 2.2)]
    assert vc.predict(pairs, 8, d) is None


def test_predict_min_matched_shrinks_for_short_slides():
    # 3-word slide: min(4, ceil(3/2)=2) = 2 matched words is enough
    assert vc.predict([(0, 1.0), (1, 1.4)], 3, D) is not None


def test_predict_waits_remaining_words_at_measured_rate():
    # last match is 2nd-last (idx 9 of 11); 0.4 s/word -> wait one word, minus lead
    pairs = [(5, 2.6), (6, 3.0), (7, 3.4), (8, 3.8), (9, 4.2)]
    assert vc.predict(pairs, 11, D) == pytest.approx(4.2 + 1 * 0.4 - 0.3)


def test_predict_uses_default_rate_when_span_too_short():
    d = {**D, "min_matched": 2, "tail_words": 3}
    assert vc.predict([(8, 5.0), (9, 5.5)], 11, d) == pytest.approx(5.5 + 1 * 0.45 - 0.3)


def test_predict_clamps_absurd_rate():
    d = {**D, "min_matched": 3, "tail_words": 3}
    pairs = [(7, 0.0), (8, 10.0), (9, 20.0)]  # 10 s/word -> clamped to 1.5
    assert vc.predict(pairs, 11, d) == pytest.approx(20.0 + 1 * 1.5 - 0.3)


def test_predict_last_word_heard_is_already_due():
    pairs = [(7, 1.0), (8, 1.4), (9, 1.8), (10, 2.2)]
    assert vc.predict(pairs, 11, D) <= 2.2
