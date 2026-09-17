# Live notes — 2026-09-16

Operator session on the locked live pick (`small.en`, window 4s, hop 1s, `lead_s` 0.3, `min_speech_ms` 300, `blank_settle_s` 1.0). Notes only unless a later prompt asks for code. Source: `metrics.jsonl` plus feel from the set.

## Songs so far

- **I Know That My Redeemer Liveth**
- **Glory to God Forever**
- **He Reigns**
- **Holy Is the Lord** — one slide did not auto-advance; the rest of the song was good. First miss-style hold this set, not a whole-song sit-out.
- **Mighty to Save** — early (lead) felt decent. **Intra-slide vocal rests:** they sing a few words of the current slide, mini-pause (nobody singing, slide does not change), then a few more words of that **same** slide. Not a blank, not a new cue, not operator space. Today the rate-wait treats the quiet as if they kept singing.

## Next in the set

- **Jesus Keep Me Near the Cross** — on screen while these notes were written (Ending: “Till my raptured soul shall find / Rest beyond the river”). API probe did not trigger Next.

## How the telemetry looked

About **14.5 minutes** on the clock (873 s wall). **36 slide enters**, **23 fires**. Unique ProPresenter uuids: 17.

| | lyric slides | blank slides |
|---|---:|---:|
| enters | 31 | 5 |
| auto-fires | 18 | 5 |

**15 enters never got a fire row.** Several of those were the first long slides (27–30 words) sitting 8–61 s, plus a couple of 10-word slides that later did fire on a repeat. Mix of: operator Next, bounce/back, pause, or a real miss. Live log cannot tell those apart.

Lyric fires (the Whisper path):

- Dwell on slide before click: median **10.1 s** (range 6–94 s; the 45–94 s rows are long verses, not stuck hops).
- **fired_at − predicted**: median **+1.55 s**, p90 **+2.52 s**, max **+4.91 s**. Zero of 18 lyric fires were early vs the timer. The hop (1 s) plus inference is eating the 0.3 s lead.
- Matches at fire: 4–21 words. `idx_from_end` was 0, 1, or 2 every time — tail gate is doing its job; the click is still late vs the singer.

Blank / VAD fires:

- First blank sat **15 s** before voice counted.
- Later blanks clicked at **4–8 s** dwell.
- One blank uuid fired **three times** in a row (5 s, 7 s, 8 s). Next may not have landed, or ProPresenter was still reporting blank.
- Operator: it is **hallucinating on blanks** — pads / tails / room read as singing, so empty slides get fake detections. That is the opposite failure from “slow to leave the blank when they actually start.”

Bench Sunday numbers (false / miss / p90 vs lyric *truth* times) are **not** in this file. Live only logs enter/fire. Operator feel is the ground truth for this session.

## Tune next (do not code yet)

1. **Blank → lyrics VAD should be more sensitive *when they actually start singing*.** Leaving an instrumental / empty slide for the first sung line felt late. Today: Silero needs **300 ms** of speech and **1.0 s** settle after entering the blank. Want: pick up the first real vocal sooner (lower `min_speech_ms` and/or `blank_settle_s`). That fights item 3 — do not just crank sensitivity.

2. **Advance slightly sooner on lyric slides (not the last one into a blank).** Earlier songs wanted Next a bit earlier than it fired on normal lyric→lyric. Data agrees: clicks landed ~1.5–2.5 s after the predicted last-word time, with `lead_s` only 0.3. *Mighty to Save*: **early felt decent** — do not keep adding lead as a blunt global. Candidates (later): bump `lead_s` only where songs still feel late, or accept that hop 1 s cannot hit “as they sing the last word” without more lead. Do not turn on `deadline_fire` without a new bench — that one blows up false %.

3. **Hallucinating on blanks.** Instrumental / empty slides are getting fake voice or fake words — VAD and/or Whisper inventing speech over pads, tails, clap, or room noise, then clicking Next. Live log already shows one blank uuid firing **three times** (5 s, 7 s, 8 s). So: slower to *leave* a blank for a real first lyric is still true, but while *on* a blank it is too eager. Need a higher bar for “this is singing” on empty slides (maybe Whisper must agree, or ignore the 4 s window’s leftover lyric bleed, or raise VAD only on blanks). Do not transcribe blank slides into the hop view as if they had words.

4. **Too quick on the very last lyric slide → blank.** The final sung slide of a section/song jumps to the blank early. Different from mid-song lyric→lyric (those felt late). Last slide often has a held last word, ritard, tag, or applause — measured sec-per-word from earlier in the song is too fast here. Extra guard before firing into a blank: e.g. only if the next slide is blank, wait for silence / require the last word actually heard / ignore rate-wait that was computed on the verse tempo.

5. **Pause must stop transcription too.** Pause means the box is idle: no Whisper, no VAD, no Next, no GPU on a 4 s window. If anything still transcribes while paused (hop loop, leftover ring, blank VAD), that is a bug. Resume should start clean (empty ring), not dump audio captured during the pause into the decoder.

6. **Pause UI: say it once, then wait.** Do not rewrite `paused  space to resume` every hop. Print it **once** when entering pause, leave the last heard/slide block on screen, and wait for a key (space/p) until resume. No hop-view flicker, no stream of paused lines.

7. **Anchor / detector words: not every match may set the timer.** Alignment today maps *any* heard word onto the slide (`min_matched` 4, then tail + first-half). Repeated chorus glue (“holy”, “lord”, “you”, “god”) lights up too many indexes and can arm the wrong place. Prefer a small set of **detectors** — distinctive words that appear **1–2 times** on that slide — and time the click off those, not off the whole bag of matches. If a word shows up four times on the slide, it is a bad detector.

   Hop-view color should show the difference (today: dim = not heard, green = heard, yellow = tail that can arm Next). **Want:** a fourth color (or yellow only) for words that actually **set or updated the fire time**. Green = heard but not a detector. If we scheduled Next off `redeemer` / `calvary`, those light as “timer”, not the same green as `the` / `and`. Operator can see whether the click is riding a real anchor or chorus glue.

8. **Pauses inside one slide.** Same ProPresenter slide the whole time. They sing a few words → short rest (mini pause, no vocal) → sing the next few words of **that slide**. Repeat as needed. The remaining lyric is still on screen; there is no blank and no Next in the gap. Freeze the click timer while they are not singing, then keep matching when the next words of the same slide start. Do not average the rest into sec-per-word. Do not fire Next because the measured rate says the leftover words “should” already have been sung. Operator pause (space) is the wrong tool — the operator is not pausing the system; the singers are pausing mid-line.

9. **Normalize punctuation in words.** Slide text and Whisper tokens must match after stripping punctuation, not as raw strings. Tonight’s *Jesus Keep Me Near the Cross* already has `Calv'ry's`, `o'er`, `I'll`. Also expect curly quotes, em-dashes, ellipses, slashes, and trailing commas. Apostrophes in contractions/elisions should fold to the same word (`calvary` / `calvry` / `calv'ry`). If “cross,” and “cross” are two tokens, alignment and anchors break. Do this on both slide words and heard words before matching.

## ProPresenter API (read-only probe, did not move the slide)

Official docs: https://openapi.propresenter.com/. verse-cue today: `GET /v1/status/slide` (uses **current** only) and `GET /v1/trigger/next`. ProPresenter 18.2 on this box (`GET /version`: host MediaOneLive, api v1). Port 50001 works.

Tried **GET only** (no trigger) against `127.0.0.1:50001` while *Jesus Keep Me Near the Cross* was on the Ending slide. Slide did not change.

| Endpoint | Result | Why it matters |
|---|---|---|
| `GET /version` | ProPresenter 18.2, api v1 | Health check for `--setup`. `/v1/version` is 404. |
| `GET /v1/status/slide` | `current` + **`next`** + **`notes`** | **Next is already here.** Current Ending lyric; **next text is empty** (blank uuid `311c2b7e-…`). This is the last-lyric→blank case. verse-cue ignores `next` today. |
| `GET /v1/presentation/active` | **Song identity** | `id.name` = `Jesus Keep Me Near The Cross (Near The Cross)`. Groups: Blank (label `Lush Waterfalls Life`, empty text), Verse 1–4, Chorus 1, Ending. Full lyric of every slide. `has_timeline`: false. Same body as `/v1/presentation/current`. |
| `GET /v1/presentation/slide_index` | `index`: 10 | Cue index inside this presentation. Combine with `active` to know last slide of a group vs last of the song. |

**Song identity (the useful one):** do not scrape the current lyric line to guess the title. `presentation.active.id.name` is the library name. Use that for BPM lookup / catalog. Groups name structure (Blank / Verse / Chorus / Ending). Empty-text slides still have a **label** (background media name) — that is a blank, not a lyric.

**Also unused, still worth later:** `?chunked=true` on `/status/slide` (push on change instead of 1s poll). `/v1/presentation/active/next/trigger` stays inside this song; `/v1/trigger/next` can jump to the next **playlist** item — possible cause of last-slide weirdness. **No BPM in the API.** Intra-slide vocal rests are not visible to ProPresenter.

**Not useful:** chord chart (JPEG), presentation timeline play/pause (not musical rest).

## Idea: BPM from the song, not from the last few heard words

Today `default_sec_per_word` is **0.45** and live rate is whatever two matched timestamps imply, clamped to `[0.15, 1.5]`. That is local and noisy. It cannot know a held last note, a chorus that is slower than the verse, or that the next slide is a blank rest.

**Want (later, not this session):** use the **current slide lyrics** to look up the song, get **BPM** (and maybe time signature / feel), and derive seconds-per-word from that as the singing-rate prior.

Sketch, not a spec:

- Identify the song from ProPresenter **`GET /v1/presentation/active` → `id.name`** (confirmed live: `Jesus Keep Me Near The Cross (Near The Cross)`). Fuzzy match on current slide text is the fallback. Catalog so far: *I Know That My Redeemer Liveth*, *Glory to God Forever*, *He Reigns*, *Holy Is the Lord*, *Mighty to Save*, *Jesus Keep Me Near the Cross*.
- Look up BPM (operator-entered, song database, or on-disk table). Church arrangements drift; prefer “this house’s BPM” over Spotify.
- Map BPM → sec/word with a simple assumption (e.g. one stressed syllable per beat, or words-per-bar from the lyric + meter). Use that as `default_sec_per_word` / rate prior instead of 0.45.
- Still let live alignment *nudge* the timer, but do not let a fast early match make the last slide dump into a blank.
- Blank slides: BPM does not mean “click when the next downbeat would have a word.” Blank is rest. VAD / silence should own blank→lyrics; BPM should own how long a *lyric* slide is expected to last.

Risks to write down before anyone builds it: wrong song match, wrong arrangement BPM, spoken tags, free-time endings, key changes that do not change BPM. Lookup must fail open to today’s measured rate.

## Locked knobs this session used

`lead_s = 0.3` · `tail_words = 3` · `first_half = true` · `min_matched = 4` · `deadline_fire = false` · `prompt_mode = none` · `min_speech_ms = 300` · `blank_settle_s = 1.0` · `default_sec_per_word = 0.45`

## Logging we need (do not code yet)

Today `metrics.jsonl` is only `enter` and `fire`. After ~44 min this session: 109 enters, 80 fires. That cannot tell miss vs operator Next vs pause, last-lyric→blank, blank hallucination, mid-slide vocal rest, which song/group, or heard vs slide words. Bench false%/miss% needs truth times; live has no LRC. Closest proxy: **uuid changed and we did not fire**.

### Must detect: UUID change we did not cause

When ProPresenter’s current slide uuid changes, classify it:

- **`fire`** — we just called `/v1/trigger/next` (or presentation next) and then saw the new uuid. Ours.
- **`skip` (external)** — uuid changed **and** we have **not** fired since the last `enter` on the old uuid. Someone else moved the slide: operator Next, remote, Companion, a second verse-cue, or ProPresenter itself. This is the row we are missing. Log old uuid, new uuid, dwell, `matched` / `idx_from_end` at the moment of the change, `next_blank`, song/group.

Without that split, “34 enters with no fire” is a junk drawer. With it:

- `skip` + `idx_from_end` still high → you jumped early / they weren’t at the tail (or a miss you covered).
- `skip` + `idx_from_end` 0–2 → we were about to click and you beat us, or we missed the tail.
- uuid change immediately after our `fire` → do **not** also emit `skip`.

Implementation sketch (later): remember `last_fire_uuid` / `pending_our_next`. On uuid change, if `pending_our_next` matches, it is ours; else `event: skip` with `who: external`.

### Hop log (`event: hop`, ~1 line/s)

Keep enter/fire. Add one JSON line per hop (same file or `hops.jsonl`). ~2700 lines per 45 min set is fine.

Fields: `ts`, `t_end`, `paused`, `infer_s`, `speech` (VAD), `uuid`, `blank`, `n_words`, `matched`, `idx_from_end`, `predicted`, `heard`, `slide_words`, `next_blank`, `next_uuid`, `song`, `group`, `cue_index`.

Drop `slide_words` after the first hop on that uuid if the file gets fat.

### Lifecycle events (not every hop)

- `pause` / `resume`
- **`skip`** — uuid changed, system did not do it (see above)
- `song` — when `GET /v1/presentation/active` name/group changes (GET does not move the slide)

### Richer `enter` / `fire`

Enter: `song`, `group`, `cue_index`, `next_text` / `next_blank`, `n_words`, slide word list.

Fire: `reason` (`lyric` | `blank_vad` | `deadline`), `next_blank`, `lead_s`, `rate`, `speech`.

Uses APIs already probed: `/v1/status/slide` **next**, `/v1/presentation/active` name/groups, `/v1/presentation/slide_index`.

### What that unlocks

- Mid-slide rest: hops with `matched` stuck, `speech: false`, uuid unchanged, no fire.
- Blank hallucination: blank hops with `speech: true` and leftover `heard`.
- Last slide → blank: `next_blank: true` on the fire row.
- Operator vs miss: **`skip`**, not “enter without fire”.
- Late vs singer: still no lyric truth live; proxy is last matched tail word → fire, plus `skip` vs `fire`.
- Song/BPM later: `song` + `group` on rows, not guessed from lyrics.
- Punctuation/anchors: `heard` vs `slide_words` after a normalizer.

Do **not** log full audio, Whisper segments, or GPU traces on Sunday. Do not turn hop logging on by restarting mid-set; add it after this round.

## Use telemetry to adjust timings (ideas, not a spec)

Locked `lead_s = 0.3` and `default_sec_per_word = 0.45` are global. Tonight proved they are not one-size: lyric→lyric often late, last lyric→blank often early, *Mighty to Save* early felt decent, mid-slide rests break rate-wait. After hop + `skip` logging exists, **nudge timings from the log**, not from a new bench every week.

Unsure which prior wins. Candidates, can mix:

- **Per song.** Key off `GET /v1/presentation/active` name. Store `lead_s`, sec/word, blank VAD for *Mighty to Save* vs *Near the Cross*. Start from house defaults; update after each Sunday’s `skip`/`fire` rows for that name.
- **Word rate from hops.** While `speech` is true, matched-index vs time → live sec/word. Freeze that clock when `speech` is false (intra-slide rest). Better than two timestamps on chorus glue.
- **Detected / catalog BPM.** No BPM in the ProPresenter API. Options: operator table per song, tap-tempo, or estimate from word rate × assumed syllables-per-beat. BPM is a prior; live word rate overrides during a phrase.
- **Skip vs fire error.** If `skip` happens with `idx_from_end` still high, we were going to be late or they jumped — maybe more lead next time on that song. If we `fire` and they hammer previous, we were early — less lead, especially when `next_blank`.
- **Group-aware.** Verse vs chorus vs ending from `active` groups. Ending / last-before-blank uses a larger hold, chorus uses the measured rate.
- **Detector-only rate.** Compute sec/word only from words that are allowed to set the timer (item 7), not from `the`/`you`/`holy`.

Fail open: if the song is unknown or the log is thin, keep tonight’s locked knobs. Do not online-learn `deadline_fire` back on. Write any learned per-song numbers next to the hop log so a bad Sunday can be rolled back.
