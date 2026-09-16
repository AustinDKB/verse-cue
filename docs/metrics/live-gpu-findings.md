# Live GPU findings (2026-09-16)

Dedicated 1-replica runs on CUDA. Packed-grid `docs/metrics/summary.md` is a
different experiment (many songs sharing one GPU); its RTF is not live speed.

`rtf` = song seconds / wall seconds. 1.0 keeps up with the singer. Official
gate is 4.0. `false%` = fired before the slide midpoint. `miss%` = never fired
before the next truth slide. `p90` = 90th percentile |fire − truth| in seconds.
Negative median delta means early.

Word timestamps are on (`word_timestamps=True`; fire math uses each word
**start**). Live testing loads `aliases.json` (138 entries) through
`load_aliases` → `canon` before align. Unit tests stub that table to `{}`.

There is one sliding window, not 3–5 offset streams. The original offset-stream
idea serializes on one GPU and is the same as `window_s` / `hop_s`.

## What the loop actually does

Every hop, Whisper transcribes the last `window_s` seconds. `merge()` keeps
older words for this slide, so alignment sees the slide-so-far. `predict()`
sets a fire time; `decide()` clicks when that time is due.

Until this write-up, `predict()` could arm from any 4 matched words and
**extrapolate** the last-word start. That is why opening words could click.

## Dedicated 1-replica, no tail gate

A100, `window=4`, `prompt=none` unless noted. Raw rows:
`docs/metrics/dedicated-1replica.json`.

| model | hop | prompt | rtf | false% | miss% | p90 | n |
|---|---:|---|---:|---:|---:|---:|---:|
| tiny.en | 0.5 | none | 12.27 | 26.5 | 25.9 | 37.6 | 185 |
| tiny.en | 1.0 | none | 24.31 | 26.5 | 28.6 | 38.0 | 185 |
| tiny.en | 1.0 | slide | 16.74 | 71.3 | 1.9 | 42.7 | 157 |
| tiny.en | 1.0 | hotwords | 11.64 | 72.6 | 1.9 | 44.9 | 157 |
| distil-large-v3 | 1.0 | none | 10.06 | 30.6 | 13.4 | 13.5 | 157 |
| distil-large-v3 | 1.0 | slide | 9.86 | 37.6 | 8.9 | 37.5 | 157 |
| distil-large-v3 | 1.0 | hotwords | 10.05 | 36.9 | 8.9 | 37.5 | 157 |

Speed is not the bottleneck. One tiny.en replica is ~12–24× realtime; distil
is still ~10×.

`prompt=slide` / `hotwords` buy miss by copying the slide text into the
decoder and clicking way too early. Live config stays `prompt=none`.

## tiny.en + tail_words=6

L4, `window=4 hop=1`, aliases on, last match must sit in the last 6 slide
words, still extrapolating remaining words. Raw rows:
`docs/metrics/tiny-tail.json`.

| prompt | rtf | false% | miss% | p90 | early% | vs no-tail false% |
|---|---:|---:|---:|---:|---:|---|
| none | 28.95 | 19.5 | 33.0 | 19.9 | 50.3 | was 26.5 |
| slide | 24.13 | 60.5 | 14.1 | 37.7 | 82.7 | was 71.3 |

The tail gate helped the way it should: fewer premature Nexts, tighter timing
on `none`, more misses because it waits. `slide` is still too eager.

## Model size vs cues

Bigger models hear more words. That cuts miss and p90. It does **not** cut
false Nexts — extra matches arm the timer earlier, including on repeats.

| | miss | false | p90 |
|---|---|---|---|
| tiny.en (dedicated, no tail) | 28.6 | 26.5 | 38.0 |
| distil-large-v3 (dedicated, no tail) | 13.4 | 30.6 | 13.5 |
| tiny.en + tail_words=6 | 33.0 | 19.5 | 19.9 |

Packed pass-1 (not live RTF) showed the same shape: small.en miss 24.9 / false
26.5 vs tiny miss 46.6 / false 15.1.

## How to move both false and miss

Prefer early to miss. Size bump alone trades miss for false. The combination
that can move both:

1. Hear better: `small.en` or `distil-large-v3` (both still >> 4× RTF).
2. Click later: `tail_words=6`.
3. Do not extrapolate from the first tail match. Fire from a word actually
   heard in the tail (`last heard start − lead_s`).

Do not use `prompt=slide`. Hop 0.5 still fits on tiny (~12×) if miss stays high.

## tiny / small / distil + tail_words=6, no remaining-word extrapolation

L4, `window=4 hop=1 prompt=none`, aliases on, fire at last *heard* tail-word
start minus lead (no rate guess). Raw rows:
`docs/metrics/model-compare-tail.json`. 744 s wall.

| model | rtf | false% | miss% | p90 | early% |
|---|---:|---:|---:|---:|---:|
| tiny.en | 15.29 | 28.1 | 28.6 | 38.1 | 57.3 |
| **small.en** | 8.97 | **24.3** | 24.9 | **11.9** | 65.4 |
| distil-large-v3 | 8.47 | 29.7 | **22.2** | 13.7 | 67.6 |

Versus dedicated tiny with no tail gate (false 26.5 / miss 28.6 / p90 38):
`small.en` moved all three the right way — false 26.5→24.3, miss 28.6→24.9,
p90 38→11.9 — and stayed ~9× realtime.

Versus tiny + tail + still-extrapolating (false 19.5 / miss 33.0 / p90 19.9):
dropping extrapolation made tiny *earlier* (false 19.5→28.1). Clicking at the
first tail hearing is sooner than guessing the last-word time. Distil still
wins miss; tiny+extrapolate still wins false.

`small.en` is the best single point if the goal is improve both versus the
original live tiny config. Going larger than small mostly buys a little more
miss at worse false. All three still smash the 4× RTF gate.
