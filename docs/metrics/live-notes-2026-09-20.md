# Live notes — 2026-09-20

Sunday rehearsal plus a later service-sim block. Locked live pick unchanged (`small.en`, window 4s, hop 1s, `lead_s` 0.3, `min_speech_ms` 300, `blank_settle_s` 1.0). Notes only. Source: `docs/metrics/live-session-2026-09-20.jsonl` (today’s rows sliced from the live `metrics.jsonl`). Same enter/fire shape as Sep 16 — still no `skip`, hop, pause, song, or group.

Clock on the box is Mountain Time. verse-cue had been appending since Sep 16 (`entered` is a long monotonic clock). Do not mix Sep 16 rows from `metrics.jsonl` into these counts.

## Blocks

| | clock | span | rows | lyric enter / fire | blank enter / fire | inferred skip |
|---|---|---:|---:|---|---|---:|
| 1 rehearsal | 08:42–09:08 | 26.3 min | 143 | 70 / 55 | 16 / 2 | 31 |
| 2 blank flip | 09:23–09:33 | 10.3 min | 26 | 0 / 0 | 26 / 0 | 25 |
| 3 paused walk? | 10:12–10:45 | 32.4 min | 133 | 111 / **0** | 22 / 0 | 132 |
| 4 service sim | 10:52–11:27 | 35.0 min | 145 | 69 / 53 | 22 / 1 | 36 |

**Inferred skip** = uuid changed and we never logged a `fire` on that visit. Operator Next, remote, bounce, or a real miss. Live log still cannot tell those apart.

Block 3 is the tell: 111 lyric visits, **zero fires**. That is pause, or detection off, while someone clicked the deck. Treat block 4 as the “coming in hot” sim, block 1 as the morning rehearsal.

## How the clicker did (blocks 1 and 4)

Same picture both times.

Lyric first-fire (Whisper path):

| | block 1 | block 4 | Sep 16 all |
|---|---:|---:|---:|
| lyric visits that fired | 52 / 70 (74%) | 53 / 69 (77%) | 136 / 174 (78%) |
| dwell median | 11.6 s | 12.1 s | 12.3 s |
| fired − predicted median | **+0.45 s** | **+0.57 s** | +0.53 s |
| p90 lag | +2.11 s | +2.14 s | +2.20 s |
| early vs timer | **0 / 52** | **0 / 53** | 0 / 136 |
| `idx_from_end` | 0–2 only | 0–2 only | 0–2 only |
| matched at fire | 3–27, median 11.5 | 4–25, median 12 | 3–26, median 12 |

The 0.3 s lead is still eaten by hop + infer. Tail gate held. Mid-song lyric→lyric is tighter than the first Sep 16 notes (+1.55 s on the first 18 fires), not a new model.

Blanks (VAD):

- Block 1: 16 blank visits, **2 fires**, both on `735c6864` at 2 s and 3 s (just after settle).
- Block 2: 26 blank enters, **0 fires**, including one ~3.5 min sit. Pause or a quiet room.
- Block 4: 22 blank visits, **1 fire** at 2 s.
- Sep 16 had **12 blank fires** and a uuid that fired three times. Today the desk mostly did **not** punch through instrumentals.

Last lyric → blank: 6 in block 1, 6 in block 4. Lags 0–1.4 s on the timer. Still cannot see a held last note.

## Messy stretch (block 1, ~09:02–09:08)

Same 20-word uuid `261c34dc` as the late Sep 16 song:

- Fired on several visits (18 s, 20 s, 15 s).
- Operator bounced `261c34dc` ↔ `292c874d` ↔ `36e06e0e`. `292c874d` had **3 visits, 0 fires**.
- **09:04:50:** four `fire` rows in 3 seconds on `261c34dc` (`idx` 0/1/0/0). Next did not land, so it kept clicking. Live risk: stuck last slide becomes a machine gun.
- Last 20-word visit sat 61 s with no fire, then blank.
- New 33-word `65ba0705` sat **79 s**, never fired, then blank. Talk / scripture / miss — log cannot say.

Long sits that **did** fire in block 1: 32 s, 57 s, 54 s, 75 s, and **179 s** on `84ebf2a2` (8:58 → 9:01, 12 matches). Intro / talk / pause, then it caught the tail.

Opening 20 s of block 1 were jumps (`8e879596` 5 s skip, `9bccb418` 1 s skip), not misses.

## What the log still cannot tell a service

Same hole as Sep 16. `metrics.jsonl` writes. The **shape** of each line is still too thin:

- Miss vs operator Next (no `skip`; enter rows have `matched: 0`).
- Whether pause was on (block 3 and the 179 s lyric both look like pause).
- Song / group (`presentation.active` unused).
- Intra-slide rests or blank hallucination at hop resolution.
- Whether a fire went into a blank (`next` is in the API; we do not log it).

Minimum before the next scored Sunday: `skip` on external uuid change, `pause` / `resume`, and `song` / `group` / `next_blank` on enter and fire. Hop-per-second can wait.

## Locked knobs this day used

`lead_s = 0.3` · `tail_words = 3` · `first_half = true` · `min_matched = 4` · `deadline_fire = false` · `prompt_mode = none` · `min_speech_ms = 300` · `blank_settle_s = 1.0` · `default_sec_per_word = 0.45`
