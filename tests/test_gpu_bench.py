"""Even replica counts: max of each size that fits in 60GB."""

import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parents[1] / "scripts")]

from gpu_bench import COST_MB, MODELS, VRAM_CAP_MB, max_even, plan_counts, replica_n  # noqa: E402


def test_max_even_is_nine_at_60gb():
    assert max_even() == 9
    assert replica_n("9") == 9


def test_plan_nine_of_each_fits_60gb_ten_does_not():
    counts = plan_counts(MODELS, free_mb=81_920, cost=COST_MB, headroom=0, replicas=9)
    used = sum(COST_MB[n] * c for n, c in counts.items())
    assert set(counts.values()) == {9}
    assert used <= VRAM_CAP_MB
    assert used + sum(COST_MB[n] for n in MODELS) > VRAM_CAP_MB
