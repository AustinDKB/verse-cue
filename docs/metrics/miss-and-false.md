# What moves miss% and false%

Locked live config (tonight): `small.en`, `window=4`, `hop=1`, `prompt=none`,
`tail_words=3`, `first_half=true`, `min_matched=4`, `deadline_fire=false`,
aliases on. Best dedicated pass at hop 0.5: **false 14.6 / miss 25.9 / p90 12.1**.
Prefer early to miss. Do not ship `prompt=slide`, combo B (0.45s/word deadline),
or “all three levers.”

`false%` = fired, and the click was before the slide midpoint
(`delta < -(slide_length / 2)`). A human would not have clicked yet.

`miss%` = never fired before the next truth slide (+ 2s operator grace).
The operator had to click.

`p90` = 90th percentile |fire − truth| in seconds. Negative median = early.

## The two knobs that dominate both

Almost every large swing came from **when the timer is allowed to arm**, not
from Whisper WER.

1. **How much of the slide must be heard before a click can be scheduled.**
   `min_matched`, `tail_words`, `first_half`. Loose gates → fewer misses, more
   first-half clicks (false). Tight gates → the opposite.
2. **Whether the decoder is allowed to copy the slide.** `prompt=slide` /
   `hotwords` makes Whisper emit the lyric it was handed, so alignment “matches”
   opening words and clicks ~20s early. Miss collapses; false explodes
   (tiny: miss 1.9 / false 71). Live stays `prompt=none`.

A later, closer-to-the-end match already **overwrites** the fire time
(`decide()` keeps the newest `predict()`). Expanding last-N only changes when
the first timer may start, not whether a later hearing replaces it.

## false% — largest factors

Ranked by how hard they hit false in the GPU runs:

| Factor | Direction | Evidence |
|---|---|---|
| `prompt=slide` / `hotwords` | **huge up** | tiny 26.5 → 71; combo-B-shaped early clicks |
| `deadline_fire` too fast (0.45–1.0 s/word) | **huge up** | combo B false 88; split D1 false 30.3 |
| Bigger model (no extra gates) | up | distil 30.6 vs tiny 26.5 (no tail) |
| Widen last-N **and** drop first-half **and** min_matched=3 | up | all-three false 14.6 → 24.9 |
| Rate wait from a real tail hearing (`predict` remaining×rate) | **down** | small.en false 24.3 → 14.6 |
| `tail_words=3` + `first_half` | **down** | opening words cannot arm |
| Wider window, no deadline (split W, window=6) | down | false 7.6, but miss 30.3 |

False is “clicked in the first half.” Anything that arms a timer from the
opening line, a chorus repeat, or a salvage deadline will raise it. The live
gates exist to refuse that arm until the match is in the last 3 words *and*
past the midpoint.

## miss% — largest factors

| Factor | Direction | Evidence |
|---|---|---|
| Never reaching the last N words | **the miss** | most misses never armed a timer |
| `prompt=slide` | huge down (cheating) | miss 1.9, unusable |
| Aggressive `deadline_fire` (1.0 s/word) | down | split D1 miss 15.7, false 30.3 |
| All three loose gates together | down | miss 25.9 → 18.9, false 24.9, p90 35 |
| Bigger model | down | distil miss 13.4 vs tiny 28.6 (no tail) |
| `small.en` vs `tiny.en` (same gates) | down | miss 24.9 vs 28.6; live pick small.en |
| Drop first-half **alone** | **up** | miss 32.4 |
| `min_matched=3` **alone** | **up** | miss 28.1 |
| Widen `tail_words` 3→6 **alone** | none | miss stayed 25.9 |
| Window=6, no deadline | up | split W miss 30.3 |
| 1.5 s/word deadline | none-ish | split D15 miss 28.1 / false 12.4 |

Misses are mostly “the tail never aligned.” Hearing more of the line (bigger
model, looser gates, a late salvage click) cuts miss and spends false. Tightening
one gate at a time often *raised* miss without helping false much.

## What we locked, and what we will not

Live `verse-cue.toml` (also the bundled default):

- **Model** `small.en`. Size bump from tiny cut miss and p90. Distil/large did
  not earn the extra false or VRAM.
- **Window 4s / hop 1s.** Hop 0.5 halved false on small.en but two songs dipped
  under 4× RTF. Production hop is 1.0.
- **`prompt=none`.** Slide/hotwords are a false bomb.
- **`tail_words=3`, `first_half=true`, `min_matched=4`.** How an operator waits.
- **`deadline_fire=false`.** Split D1 cut miss by firing on a clock; false
  doubled. Combo B (0.45 s/word) was 88% false.
- **Aliases on** (bundled `aliases.json`).

Rejected for live: window=6-only, deadline 1.0 / 1.5, all-three levers,
`prompt=slide`, distil as the default, firing at first tail hearing with no
rate wait (false 24.3).

Raw rows: `live-gpu-findings.md`, `miss-levers.md`, `both-combos.md`,
`split-b.json`.
