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


def test_predict_min_matched_shrinks_for_short_slides():
    # 3-word slide: min(4, ceil(3/2)=2) = 2 matched words is enough
    assert vc.predict([(0, 1.0), (1, 1.4)], 3, D) is not None


def test_predict_extrapolates_with_measured_rate():
    pairs = [(0, 1.0), (1, 1.4), (2, 1.8), (3, 2.2), (4, 2.6)]  # 0.4 s/word
    # last word is idx 10, six words after idx 4: 2.6 + 6*0.4 - lead 0.3
    assert vc.predict(pairs, 11, D) == pytest.approx(4.7)


def test_predict_uses_default_rate_when_span_too_short():
    d = {**D, "min_matched": 2}
    assert vc.predict([(8, 5.0), (9, 5.5)], 11, d) == pytest.approx(5.5 + 1 * 0.45 - 0.3)


def test_predict_clamps_absurd_rate():
    d = {**D, "min_matched": 3}
    pairs = [(0, 0.0), (1, 10.0), (2, 20.0)]  # 10 s/word -> clamped to 1.5
    assert vc.predict(pairs, 11, d) == pytest.approx(20.0 + 8 * 1.5 - 0.3)


def test_predict_last_word_heard_is_already_due():
    pairs = [(7, 1.0), (8, 1.4), (9, 1.8), (10, 2.2)]
    assert vc.predict(pairs, 11, D) <= 2.2
