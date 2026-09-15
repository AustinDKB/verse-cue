# verse-cue — Design

Auto-advance ProPresenter lyric slides from a live voice feed. One loop:
listen, transcribe, align the transcript to the current slide's text,
predict when the last word starts, fire `/v1/trigger/next` a little early.

Source of truth for intent: `Pro Presenter Auto Advance System.md` (this
repo). `/home/austin/Desktop/PP AutoV2` is reference-only for "what we tried
before"; nothing from it is a dependency of this project.

## Goals

- Singer- and song-independent. No per-song training, no stored song data:
  slide text comes from ProPresenter at runtime.
- Early is better than late. Target fire time is the start of the last word
  of the slide (the operator's habit), biased earlier by a configurable lead.
- Runs on the ProPresenter machine itself (Windows + NVIDIA GPU in
  production), also on Mac and CPU-only Windows/Linux.
- User does at most: enable the ProPresenter network API, run `--setup`
  (pick the audio input, confirm port), run `verse-cue`.
- Everything the model does is configured in one TOML; the model, window, hop
  and prompt mode are chosen automatically by a bench, with a hardware table
  fallback before the bench has run.

## Non-goals

- Multi-input audio (only the vocal feed).
- GUI. Terminal only.
- MIDI or any ProPresenter integration other than the HTTP API.
- Real-time transcription display, chords, arrangements.

## Constraints

- Exactly two production Python files: `verse_cue.py` (runtime) and
  `harvest.py` (tool). Total production SLOC <= 1000; each file <= 450
  (anti-slop file cap). Config, `aliases.json`, `songs.txt`, tests, docs and
  media are not counted.
- Every production function passes `docs/guides/machine-readable-thresholds.yaml`
  (function <= 60 SLOC, cognitive <= 15, nesting <= 4, call depth from entry
  <= 3, no `*Manager`/`*Factory`/`Base*`, no protocol with one impl, no new
  private helper with fan-in 1 and <= 4 statements).
- Runtime dependencies: `faster-whisper`, `sounddevice`. Nothing else outside
  the standard library (`tomllib`, `urllib.request`, `difflib`, `json`,
  `subprocess`, `time`, `collections`).
- Tool dependency: `yt-dlp`. Dev-only: `matplotlib`, `pytest`, `pytest-xdist`,
  `pytest-cov`.
- Optional extra `verse-cue[cuda]` -> `nvidia-cublas-cu12`, `nvidia-cudnn-cu12`.
- Tests run only as `uv run pytest` (xdist + coverage from `pyproject.toml`).

## 1. Architecture

```
verse_cue.py    runtime: audio -> whisper -> align -> fire -> ProPresenter
harvest.py      tool:    download | aliases | bench
verse-cue.toml  all config (audio, PP host/port, model params, [hardware], [bench])
verse-cue.auto.toml  written by bench: chosen model/window/hop/prompt_mode
aliases.json    generated {canonical_word: {alias: count}}
songs.txt       "Artist - Title" per line (~100 worship songs)
data/           gitignored: <slug>.wav / .lrc / .txt from `harvest download`
metrics.jsonl   runtime log, one line per slide advanced
docs/metrics/   bench output: PNG graphs + summary table
```

### The seam

```python
def run(frames, pp, model, cfg, now=time.monotonic) -> None
```

- `frames`: iterator yielding `hop_s` seconds of 16 kHz mono float32 numpy
  per item. Production: `sounddevice.InputStream` queue. Bench/tests: a wav
  file sliced into hops.
- `pp`: duck-typed. `pp.slide() -> (uuid, text)` and `pp.next()`.
  Production: two `urllib` GETs to `http://{host}:{port}/v1/status/slide` and
  `/v1/trigger/next`. Bench/tests: `FakePP` built from a list of slide texts
  and a truth timeline.
- `model`: anything with
  `transcribe(audio, **kw) -> iterable of segments with .words[(start,end,word)]`.
  Production: `faster_whisper.WhisperModel`. Tests: scripted fake.
- `now`: clock, injectable so the bench can run faster than real time.

Production, bench, and tests all call the same `run`. No internal mocking.

Call depth from `main`: `main -> run -> {transcribe_window, align, decide,
pp.next, vad_speech}`. Nothing deeper.

## 2. Runtime loop

Every tick (one `frames` item):

1. Append the hop to a ring buffer of `window_s` seconds. Track the
   wall-clock time of the buffer's end so word offsets convert to capture time.
2. Read `pp.slide()`. If the uuid changed since last tick (our fire or the
   operator), reset: committed words, progress cursor, timer, blank-settle
   clock. If the change happened while a transcription was in flight, discard
   that result.
3. Blank slide (`text.strip() == ""`): skip transcription. Run Silero VAD
   (`faster_whisper.vad.get_speech_timestamps`) on the new hop. If speech
   >= `min_speech_ms` and we have been on this slide >= `blank_settle_s`,
   `pp.next()`. Continue.
4. Lyric slide: transcribe the window with `word_timestamps=True`,
   `beam_size=cfg.beam_size`, `language="en"`, `condition_on_previous_text=False`,
   and per `prompt_mode`:
   - `none`: no prompt
   - `slide`: `initial_prompt = text` (current slide)
   - `hotwords`: `hotwords = text`
5. Merge. Words from the previous window whose capture end < new window
   start are appended to `committed`. Transcript = `committed + latest_window`.
   Latest window wins for its own region; no agreement voting.
6. Drop transcript words with capture start < `last_fire_time + guard_s`
   (previous slide's held last word bleeding in).
7. Normalize tokens: lowercase, strip non-letters/apostrophes. Map each token
   through the inverted alias dict (`{alias: canonical}`, O(1)); tokens still
   not in the slide vocabulary go through `difflib.get_close_matches(token,
   slide_vocab, n=1, cutoff=cfg.fuzzy_cutoff)` (vocab is ~40 words; trivial).
8. Align: `difflib.SequenceMatcher(None, slide_words, tokens, autojunk=False)`.
   From `get_matching_blocks()` collect `(slide_idx, capture_start)` pairs.
   `progress = max(slide_idx)`, monotonic per slide (never decreases).
9. Decide:
   - `matched = number of matched pairs`. If
     `matched < min(cfg.min_matched, ceil(N/2))`: no fire. This is the guard
     against identical consecutive slides (chorus x2): a lone held last word
     from the previous slide matches one word and cannot fire.
   - `rate = (t_last - t_first) / (idx_last - idx_first)` when the matched
     span covers >= 3 slide words, else `cfg.default_sec_per_word`.
   - `predicted = t_last_start + (N - 1 - idx_last) * rate - cfg.lead_s`.
   - If `idx_last == N - 1` (last word heard): fire now.
   - Else fire when `now() >= predicted`.
   The timer is recomputed each tick, so a later, closer-to-the-end match
   overrides an earlier estimate — no explicit timer objects.
10. Fire: `pp.next()`, record `last_fire_time`, append a `metrics.jsonl` line,
    reset state (the uuid check on the next tick will confirm the change).

### Word-timestamp latency budget

`fire latency = hop_s + inference_time + HTTP (<50 ms localhost)`. On CPU
with RTF 4x and `window_s=4`: ~1 s inference, so `hop_s >= 1`. Extrapolation
from words 2–4 before the end is what makes early firing possible despite
this; the bench measures the result rather than assuming it.

### Multiple streams

The brain dump's three offset 3 s streams on one shared model serialize on
the GPU and are equivalent to a single loop with `window_s=3, hop_s~1.2`.
There is one code path; the bench grid `window_s in {3,4,5} x hop_s in
{0.5,1.0}` covers that configuration and its neighbours.

## 3. ProPresenter client

- `GET /v1/status/slide` -> `{current:{text,notes,uuid}, next:{...}}`.
  Empty `text` = blank slide. Polled once per tick (localhost, < 5 ms).
- `GET /v1/trigger/next` -> advances. Also used at end of song / playlist;
  whatever ProPresenter does is fine.
- Connection errors: log once, retry each tick with backoff capped at 5 s.
  Never crash the loop.

## 4. harvest.py

Subcommands: `download`, `aliases`, `bench`. Shared: reads the same TOML.

### download

For each `songs.txt` line `Artist - Title`:
- `yt-dlp "ytsearch1:Artist Title" -x` -> ffmpeg -> `data/<slug>.wav`
  16 kHz mono.
- `GET https://lrclib.net/api/get?artist_name=..&track_name=..` ->
  `syncedLyrics` to `data/<slug>.lrc`, `plainLyrics` to `data/<slug>.txt`.
  Fallback `GET /api/search?q=`. No lyrics -> skip song, log it.
- Resumable: skip files that exist. Deterministic given the same search
  results; one `--limit N`.

### aliases

Goal: a dictionary of how Whisper mishears sung words, so the runtime can
map a misheard token to its canonical lyric word in O(1).

For each downloaded song with lyrics:
- Hot pass: `tiny` (or `tiny.en`), `temperature in cfg.alias.temperatures`
  (default `[0.6, 1.0]`), `beam_size=1`, `condition_on_previous_text=False`,
  `vad_filter=False`, run over the audio in the runtime's window/hop.
- Real pass: the bench-selected model (from `verse-cue.auto.toml`, else the
  hardware table) at normal runtime settings. Its real errors matter more
  than tiny's.
- Align: `SequenceMatcher(None, lyric_tokens, heard_tokens, autojunk=False)
  .get_opcodes()`. For each `replace` where the two spans have equal length,
  pair tokens positionally -> `(canonical, alias)`. Unequal spans are skipped.
- Count pairs across all passes and songs. Keep `count >= 2`, top 20 aliases
  per canonical word, and drop an alias that is itself a canonical word with a
  higher own-count. Write `aliases.json` as `{canonical: {alias: count}}`.
- Saturation: after each song, record total distinct aliases -> curve
  `docs/metrics/alias_saturation.png`. Stop early when the last 10 songs each
  added < 1% new aliases. This answers "how many songs?" empirically;
  expectation 60–100 songs, 2–3 h on an 8-core CPU.

Known limitation (documented in README): YouTube audio is a full studio
mix; production audio is a voice-only feed. Hallucination patterns will
differ. Users can drop their own `<slug>.wav/.txt/.lrc` into `data/` to
harvest from real-domain audio.

### bench (= offline eval = published metrics)

Ground truth from LRC line timestamps:
- Group consecutive lyric lines into pseudo-slides of `cfg.bench.lines_per_slide`
  (default 2).
- A gap > `cfg.bench.blank_gap_s` (default 8) between lines inserts a blank
  pseudo-slide (exercises the VAD path).
- Truth time for slide k = start time of slide k+1's first line.

For each grid point (`models x window_s x hop_s x prompt_mode`) and each of
`cfg.bench.songs` songs: build `FakePP` (slide texts + truth timeline), slice
the wav into hops, run `verse_cue.run` with a fast clock, collect per slide
`delta = fire_time - truth`, plus RTF and per-window inference time.

Metrics per grid point:
- `median_delta`, `p90_abs_delta`
- `early_pct` (delta < 0), `late_pct` (delta > 1.0 s)
- `missed_pct` (never fired before the next slide's truth)
- `false_pct` (fired before the slide's midpoint in time)
- `rtf` (audio seconds / wall seconds)

Selection: among grid points with `rtf >= cfg.bench.min_rtf` (default 4),
pick the lowest `p90_abs_delta` with `false_pct <= cfg.bench.max_false_pct`.
Write `verse-cue.auto.toml` (`model, compute_type, window_s, hop_s,
prompt_mode, beam_size`) and `docs/metrics/`:
- `delta_hist.png` — distribution of delta for the chosen config
- `rtf_vs_model.png` — RTF bars per model
- `alias_saturation.png` — from `aliases`
- `timeline_<song>.png` — one song: truth vs fire markers
- `summary.md` — the grid table

Runtime `metrics.jsonl` (one line per fire): `ts, slide_uuid, n_words,
idx_from_end, matched, rate, predicted, fired_at, inference_s, blank,
model, window_s, hop_s, prompt_mode`. A uuid change we did not cause within
3 s after our fire is logged as `operator_override=true` on the previous
line. These are the numbers published after several live services.

## 5. Config

Single `verse-cue.toml`:

```toml
[propresenter]
host = "127.0.0.1"
port = 1025

[audio]
device = ""            # substring of the input device name; set by --setup
sample_rate = 16000

[model]                # overridden by verse-cue.auto.toml when present
name = ""              # "" -> pick from [hardware]
compute_type = "auto"
window_s = 4.0
hop_s = 1.0
beam_size = 1
prompt_mode = "none"   # none | slide | hotwords

[decide]
lead_s = 0.3
guard_s = 0.5
default_sec_per_word = 0.45
min_matched = 4
fuzzy_cutoff = 0.8

[blank]
min_speech_ms = 300
blank_settle_s = 1.0

[hardware]             # data table: VRAM GB threshold -> model, compute_type
gpu = [[8, "large-v3-turbo", "float16"], [4, "distil-large-v3", "int8_float16"], [0, "small.en", "int8"]]
cpu = ["small.en", "int8"]

[alias]
model = "tiny.en"
temperatures = [0.6, 1.0]
min_count = 2
max_per_word = 20

[bench]
models = ["tiny.en", "base.en", "small.en", "distil-large-v3", "large-v3-turbo"]
window_s = [3.0, 4.0, 5.0]
hop_s = [0.5, 1.0]
prompt_mode = ["none", "slide", "hotwords"]
songs = 5
lines_per_slide = 2
blank_gap_s = 8.0
min_rtf = 4.0
max_false_pct = 5.0
```

Model names are whatever `faster_whisper.WhisperModel` accepts: built-in
sizes (`tiny.en`, `small.en`, `distil-large-v3`) or Hugging Face CTranslate2
repo ids (e.g. `deepdml/faster-whisper-large-v3-turbo-ct2` for turbo). The
TOML uses the exact id; the table above abbreviates.

Hardware fallback: `nvidia-smi --query-gpu=memory.total --format=csv,noheader`
via `subprocess`; absent or fails -> CPU row. Used only until
`verse-cue.auto.toml` exists.

`verse-cue --setup`: lists input devices (`sounddevice.query_devices`),
prompts the user to choose one, prompts for the ProPresenter port (default
1025), writes both into `verse-cue.toml`, prints the hardware-table model
pick. This and enabling the ProPresenter network API are the only user
interactions.

## 6. Testing

- Unit tests drive `run()` with a scripted fake model (yields preset words
  with timestamps per window) and `FakePP`. No model download, deterministic,
  fast. Cover: merge/commit dedup; alias + fuzzy normalization; alignment
  progress monotonic; rate extrapolation and `predicted`; fire on last word;
  `min_matched` blocks a lone held word on identical consecutive slides;
  `guard_s` drops bleed; blank slide VAD gating and `blank_settle_s`;
  operator uuid change resets state; in-flight result discarded on change;
  PP client error does not crash the loop.
- Harvest: opcode -> alias pairing; alias filtering rules; LRC parse ->
  pseudo-slides with blank insertion; metric computation from a delta list;
  selection rule.
- One networked test downloads `tiny.en` and runs `run()` over a 10 s wav;
  skipped when offline or `VERSE_CUE_ONLINE` unset.
- `uv run pytest` only; `-n auto` and coverage from `pyproject.toml`.
- Pre-commit: `ruff`, `scripts/slop_gate.py`, `scripts/check_radon_gates.py`.

## 7. Publishing

Order: code green -> bench run -> graphs -> README -> video -> posts.

- `README.md`: what/why, mermaid data-flow, the four graphs, 5-step install
  (install `uv` -> `uv tool install verse-cue[cuda]` -> enable ProPresenter
  network API and note port -> `verse-cue --setup` -> `verse-cue`), metrics
  table, limitations, "how to help" (send us your `metrics.jsonl`, songs,
  hardware).
- `docs/ORIGINAL-PLAN.md`: the brain dump polished (typos fixed, voice kept),
  presented as "where we started". Spec and plan alongside.
- `docs/COST.md`: tokens and dollars per planning/build session, model names
  used to build (planning: Fable 5.1; build: DeepSeek V4.1 Flash). No AI
  attribution inside the product, README body, or video.
- `media/`: HyperFrames explainer <= 180 s, narration via Kokoro
  (`kokoro-onnx`) locally. Not production code.
- `docs/posts.md`: 3–5 short posts for the ProPresenter Facebook group,
  asking for testers and hardware reports.
- GitHub: `AustinDKB/verse-cue`, public, MIT.

## Open risks (tracked, not blocking)

- Whisper parroting `initial_prompt` -> fake progress. Mitigated by
  `min_matched` and by the bench measuring `false_pct` per `prompt_mode`.
- Word timestamps from faster-whisper (cross-attention DTW) are ~±100 ms;
  adequate because firing is extrapolated, not syllable-exact.
- Full-mix YouTube audio vs voice-only live feed for aliases and bench.
- CPU-only machines may not reach RTF 4 with `small.en`; the selection rule
  then falls to `base.en` and the README states the expected accuracy cost.
