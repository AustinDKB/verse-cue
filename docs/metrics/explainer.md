# Metrics and config, line by line

Bench scores (fake ProPresenter + known lyric times). Live Sunday does not
print these; it just clicks. `delta = fire_time − truth_time`. Negative means
early.

`--setup` only writes **device**, **host**, and **port**. Everything else in
`verse-cue.toml` is the locked live pick.

What *moves* miss and false (the GPU findings): [miss-and-false.md](miss-and-false.md).

## Metrics

**n** — How many slide changes were scored. The GPU cells were 185 cues / 6
songs.

**rtf** — Song length ÷ how long the computer took. `1.0` = barely keeping up
with the singer. Gate is `4.0`. Live hop 1.0 is there so `small.en` stays
above that.

**median_delta** — Typical click vs truth, in seconds. Negative = usually
early. The live pick is a bit early on purpose.

**p90_abs_delta** — For the clicks that happened, 90% were within this many
seconds of truth (early or late). Big p90 means some clicks were way off,
even if the median looks fine.

**early_pct** — Share of *all* cues that fired before truth. Includes “a
little early” (good) and “way early” (bad).

**late_pct** — Share of *all* cues that fired more than **1 second after**
truth. An operator would already be reaching.

**missed_pct (miss)** — Share of cues that **never fired** before the next
real slide (+ 2s grace). You would have clicked. Prefer a slightly early
click over this.

**false_pct (false)** — Share of cues that fired **before the midpoint of
that slide** (`delta < −slide_length/2`). A human would not have clicked
yet — chorus still going, still on line 1. This is the “it jumped too soon”
number.

Those two fight each other: looser gates cut miss and raise false; tighter
gates do the reverse.

## `[propresenter]`

**host** — IP of the machine running ProPresenter. Same computer:
`127.0.0.1`. GPU box + ProPresenter on a Mac: the Mac’s LAN IP.

**port** — ProPresenter Network API port, default `1025`. Enable it under
Preferences → Network → Network API. verse-cue calls
`http://host:port/v1/status/slide` and `/v1/trigger/next`.

## `[audio]`

**device** — Substring of the input name (`--setup` writes the full name).
Empty = OS default, which is often the wrong mic.

**sample_rate** — Always 16000. Whisper’s rate. Don’t change it.

## `[model]` — what Whisper hears

**name** — Which weights. Locked to **`small.en`**. Tiny misses more;
distil/large hear more and click earlier (more false, more VRAM).

**compute_type** — `auto` (float16 on GPU, int8 on CPU). Speed/quality of
the math, not the click logic.

**window_s** — Seconds of audio in each transcription. **4**. A longer
window (we tried 6) heard more context, clicked later/cleaner, missed more.

**hop_s** — Seconds between transcriptions. **1**. Must stay ≥
`window / rtf` or you fall behind. Hop 0.5 sampled the tail twice as often
and cut false, but two songs dropped under 4× RTF.

**beam_size** — Whisper search width. **1** = greedy, faster. Higher is
slower, rarely worth it live.

**prompt_mode** — `none` / `slide` / `hotwords`. Locked **`none`**. `slide`
feeds the lyric into the decoder so it “hears” words that were not sung yet
→ miss ~2%, false ~70%. Unusable.

## `[decide]` — when a Next is allowed

This is the click brain. Every hop: transcribe → map words onto the slide →
maybe schedule a fire time.

**lead_s (0.3)** — Fire this many seconds *before* the predicted start of
the last word, so the slide changes as they sing it.

**guard_s (0.3)** — Ignore words in the first 0.3s of a new slide. That’s
bleed from the previous line still in the window.

**default_sec_per_word (0.45)** — Assumed seconds per word if we don’t have
enough matches to measure rate. Also the default deadline rate.

**rate_bounds [0.15, 1.5]** — Clamp on measured singing rate so one weird
pair doesn’t schedule a 10s or 0.01s wait.

**min_matched (4)** — Need at least this many aligned words (or half the
slide if the slide is shorter). Three mumbled words do not click.

**tail_words (3)** — The latest match must sit in the **last 3 words**.
Opening “Our God is…” cannot arm a timer. A later match in the tail
**replaces** the old timer.

**first_half (true)** — Also require that latest match is past the midpoint
of the slide text. Stops short-slide / chorus-repeat early clicks.

**deadline_fire (false)** — Off for live. If on: after any match, click once
the slide has lasted `n_words × deadline_sec_per_word` even if the tail
never aligned. Cuts miss, raises false (1.0 s/word → miss 15.7 / false 30;
0.45 s/word → false 88).

**deadline_sec_per_word (0.45)** — Only used if deadline is on. Smaller =
earlier salvage click.

**fuzzy_cutoff (0.8)** — If a heard word isn’t in the alias table, difflib
may snap it to a slide word at this similarity. Lower = more aggressive
“close enough,” more false matches.

## `[blank]` — instrumental / empty slides

**min_speech_ms (300)** — VAD: this much voice counts as “someone started
singing.”

**blank_settle_s (1.0)** — After entering a blank slide, ignore voice for 1s
so leftover sound doesn’t skip the instrumental. Then first real voice
advances.

No slide on screen (`uuid` empty): never clicks.

## `[hardware]`

Used **only if** `[model].name` is empty. Live name is `small.en`, so this
table is idle. GPU row: first threshold ≤ VRAM wins. CPU: `small.en` int8.

## `[alias]` — harvest only, not the Sunday loop

Builds `aliases.json` (“halleluia” → “hallelujah”). Live **loads** that
file; it does not re-mine.

**model / temperatures** — Which Whisper + randomness to invent
mis-hearings.

**min_count (2)** — Alias must appear at least twice.

**max_per_word (20)** — Cap aliases kept per canonical word.

## `[bench]` — harvest grid only

Which models/windows/hops/prompts to sweep, how many songs, 2 LRC lines per
fake slide, 8s gap → blank slide, and the auto-pick gates (`min_rtf` 4,
`max_false_pct` 5). Does not change live `verse-cue` unless you write
`verse-cue.auto.toml` — don’t, for a live run.

## Sunday path

Hop every 1s, transcribe the last 4s with `small.en`, map words through
aliases, and only then start a rate-wait timer if the match is in the last 3
words and past halfway — click 0.3s before the predicted last word. That is
why false is “first-half click” and miss is “timer never armed.”
