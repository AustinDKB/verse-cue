# verse-cue — original plan (polished from the brain dump)

This is the first-person sketch that started the project, cleaned up for spelling
and headings. Ideas the shipped spec dropped are marked `(dropped: …)`.

## Goal

Use the ProPresenter API to read the current slide and advance to the next one
during live worship, driven by a **voice-only** audio input.

Useful API methods: current slide, next slide.
(`WhisperX for word-level timestamps` — dropped: faster-whisper word timestamps
are enough and keep the dependency list small.)

## Timing rule

When I change slides by hand I wait until the singer has started the last
syllable of the last word (or the last word if it is one syllable), then I
switch. Early is always preferred to late.

Some slides repeat words or whole sentences. The matcher has to live with that.

There will be transcription latency, so when the 3rd or 4th last word is heard,
add a delay and fire so the last syllable is not already gone.

## Aliases from hallucinations

These models were not built for sung lyrics. Harvest aliases: run a tiny model
with the worst settings so it hallucinates, then store 10–20 mis-hearings per
real word for the error-prone ones (hallelujah, etc.). Lookup has to be cheap.

How many songs until the alias set saturates? It can run overnight if the
pipeline is deterministic and tested.

## Windows

Each slide is about 12–20 seconds. I guessed 3 s chunks, overlapping:
0–3, then 1.5–4.5, then 3.5–7, all running at once. After a slide changes,
scrap anything still transcribing from the previous slide.

(dropped: three parallel streams. The shipped loop is one sliding window; the
bench grid tries several `window_s` / `hop_s` pairs instead.)

Multiple words can start a timer; prefer the word closest to the end of the
slide. A later keyword overwrites an earlier timer. A slide change resets
everything.

## Blank slides

Instrumental / blank slides need voice activity detection to leave them when
the singer starts again.

No song files in the runtime. The current slide text *is* the lyric.

## Constraints

- Production logic small (originally < 500 SLOC, later 1000 across two files)
- Human-readable
- Anti-slop metrics
- Minimal libraries
- One TOML config for model and loop parameters
- Two production scripts
- Tests and aliases do not count toward the SLOC cap
- Install in five steps on Mac or Windows
- Almost any hardware should work: pick the model from CPU/GPU, then from a
  local bench

## Deliverables

- Public GitHub repo with a real README and rendered graphs
- Metrics recorded and published after several live runs
- Explainer video, max 180 s, local voice, no model attribution
- Short posts for the ProPresenter Facebook group
- Publish this original plan, the Superpowers spec/plan, and the cost to build

## Additional notes

The old V2 folder is reference only. This dump is canon for what to build.
Use Superpowers before building. Ask people for input after it ships.
