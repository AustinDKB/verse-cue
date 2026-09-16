# Miss% levers

Goal: cut **miss%** (never fired before the next truth slide + 2s grace).
Current live pick after the A40 improve pass: `small.en`, rate wait, `tail_words=3`,
first-half gate on, `min_matched=4`, hop 1.0 in production (hop 0.5 on that
pass). **false 14.6 / miss 25.9 / p90 12.1 / rtf 4.87** at hop 0.5.

A later, closer-to-the-end match already **overwrites** the fire time
(`decide()` keeps the newest `predict()`). Expanding last-N only changes
*when the first timer is allowed to start*. The 9th-last word currently
starts nothing.

Prefer early to miss. Every miss cut spends some false budget.

## This 4-way live test

Shared: `small.en`, `window=4`, `hop=1`, `prompt=none`, rate wait on,
aliases on, 6 songs. Baseline gates otherwise.

| run | lever | tail_words | first_half | min_matched |
|---|---|---:|---|---:|
| 1 | widen last-N | **6** | on | 4 |
| 2 | drop first-half gate | 3 | **off** | 4 |
| 3 | lower min_matched | 3 | on | **3** |
| 4 | 1+2+3 | **6** | **off** | **3** |

Results: `docs/metrics/miss-levers-runs.json`. Four pods in parallel (2×L4, 2×L40S), then terminated.

| run | tail | half | min_m | rtf | false% | **miss%** | p90 | vs miss 25.9 |
|---|---:|---|---:|---:|---:|---:|---:|---|
| baseline (hop 0.5) | 3 | on | 4 | 4.87 | 14.6 | 25.9 | 12.1 | — |
| 1 widen last-N | 6 | on | 4 | 13.9 | 15.1 | 25.9 | 10.7 | 0 |
| 2 drop first-half | 3 | off | 4 | 14.1 | **10.8** | 32.4 | 10.0 | +6.5 worse |
| 3 lower min_matched | 3 | on | 3 | 18.7 | 11.9 | 28.1 | 10.0 | +2.2 worse |
| **4 all three** | 6 | off | 3 | 25.2 | 24.9 | **18.9** | 35.4 | **−7.0** |

Only combining all three cut miss. Alone, widen-N held miss flat; dropping the
first-half gate or min_matched *raised* miss (and improved false). All-three
spends the false budget (14.6→24.9) and blows p90 (12→35): more clicks, many
of them early.

For miss-first: run 4. For keeping the 14.6 false: stay on baseline / run 1.
Simulation notes for every option, including earlier GPU passes, are under
each heading below.

## All options (ranked for miss)

Each option below notes whether we ran a live GPU simulation and what it did
to miss%. Baseline for the 4-way grid: `small.en` hop 1, rate wait, aliases
138, 6 songs / 185 cues, unless a note says otherwise.

### 1. Widen `tail_words` (3 → 6, later 9)

Misses are mostly “never reached the last 3 words,” so no timer ever armed.
9th-last starts a wait of ~8×rate; 5th-last **replaces** it (already how
`decide()` works). False will rise on repeats.

**Simulated (4-way run 1):** `tail_words=6`, first-half on, `min_matched=4`,
hop 1. **miss 25.9 (unchanged)**, false 15.1 (was 14.6), p90 10.7. Widening
N alone did not cut miss. `tail_words=9` was not run.

### 2. Drop the first-half gate

`pairs[-1][0] < n_words // 2` blocks arming on short slides even when the
match is inside `tail_words`.

**Simulated (4-way run 2):** first-half off, `tail_words=3`, `min_matched=4`.
**miss 32.4 (+6.5 worse)**, false 10.8 (better), p90 10.0. Alone this did
not help miss.

### 3. Lower `min_matched` (4 → 3)

A mumbled line that only landed 3 tail words never fires.

**Simulated (4-way run 3):** `min_matched=3`, tail=3, first-half on.
**miss 28.1 (+2.2 worse)**, false 11.9, p90 10.0. Alone this did not help
miss.

### 1+2+3 together

**Simulated (4-way run 4):** tail=6, first-half off, min_matched=3.
**miss 18.9 (−7.0)**, false 24.9, p90 35.4. Only this combination cut miss.
Cost: false back to ~25 and p90 12→35.

### 4. Cap the wait, don’t refuse to arm

If 9th-last is heard, start a timer but clamp remaining wait (e.g. 2.5s) so a
slow rate doesn’t sleep through the slide end.

**Not simulated.**

### 5. Deadline fire

If we have any matches and the slide has been up longer than
`n_words × default_sec_per_word` with no fire, click anyway.

**Simulated (combo B, L4, small.en window 6, tight gates):** miss **3.9**,
false **88.2**, p90 51.7, median −22s. The 0.45s/word deadline clicks before
half the truth slide. Unusable. See `docs/metrics/both-combos.md`.

### 6. Longer Whisper window (5–8s)

More of the line in one pass → better chance the tail is in the transcript.

**Simulated (combo B) paired with deadline**, not as a window-only cell.
Miss 3.9 / false 88.2 is the deadline, not proof the 6s window helped.
Window-6-only is the next split.

### 7. `prompt=slide` (or hotwords)

Decoder is biased with the slide text. Buys miss, copies the lyric and
clicks early.

**Simulated (dedicated A100, no tail gate, hop 1):**
- tiny.en slide: **miss 1.9 / false 71.3 / p90 42.7**
- tiny.en hotwords: **miss 1.9 / false 72.6**
- distil slide: **miss 8.9 / false 37.6**
- tiny.en + tail_words=6 + slide: **miss 14.1 / false 60.5**

Lowest miss we have ever measured. Unusable false.

### 8. Bigger model

Better WER so the tail is more likely to match.

**Simulated:**
- Dedicated A100, no tail gate, hop 1, prompt=none: tiny miss **28.6** vs
  distil **13.4** (false 26.5 vs 30.6).
- L4 tail=6 no-extrapolate hop 1: tiny 28.6 / small **24.9** / distil **22.2**.
- A40 rate-wait tail=3 hop 0.5: tiny **35.7** vs small **25.9**.

Size cuts miss when the gate is loose. After a tight last-3 gate, small.en
already hears most of what the gate will accept.

**Simulated (combo A):** distil-large-v3 + tight rate-wait gates (tail=3,
first-half on, min_matched=4, hop 1). **false 13.3 / miss 30.5 / p90 6.5 /
rtf 5.7.** False held; miss did not improve vs 25.9. Distil behind the last-3
wall is not the miss lever. See `docs/metrics/both-combos.md`.

### 9. Offset streams / extra replicas / hop 0.5

Same as a smaller hop on one GPU. Original 3× offset 3s streams were
dropped as equivalent to `window_s` / `hop_s`.

**Simulated (hop 0.5 vs 1.0, not extra replicas):**
- tiny.en no tail: hop 0.5 miss **25.9** vs hop 1.0 miss **28.6**.
- small.en rate-wait tail=3: hop 0.5 miss **25.9** (false 14.6) vs the 4-way
  hop-1 baseline-shaped cells still ~26–32 miss. Hop 0.5 on small dipped two
  songs under 4× RTF (3.64, 3.91). Did not unlock a big miss win. No true
  multi-stream live run.
