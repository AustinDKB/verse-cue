# verse-cue

Auto-advance ProPresenter lyric slides from a live vocal feed. No song files, no
training: verse-cue reads the **current** slide (that is all the ProPresenter
API exposes), listens, and triggers Next as the singer reaches the last words.

## How it works

```mermaid
flowchart LR
  A[Vocal input] --> B[4 s window every 1 s]
  B --> C[faster-whisper<br/>word timestamps]
  D[ProPresenter<br/>/v1/status/slide] --> E[Current slide words]
  C --> F[Alias table + difflib alignment]
  E --> F
  F --> G[Rate-wait to last word]
  G --> H[/v1/trigger/next<br/>0.3 s early]
  D -. blank slide .-> I[Silero VAD] --> H
```

Early beats late. Fire time is the last *heard* tail word, plus remaining
words × clamped singing rate, minus `lead_s`. A later, closer match overwrites
that timer. Blank (instrumental) slides advance on the first voice. A manual
slide change (new uuid) starts over.

## Copy-paste install

Drop `[cuda]` on a Mac or a PC without an NVIDIA GPU. Install uv first if
needed: https://docs.astral.sh/uv/getting-started/installation/

```
uv tool install --refresh "verse-cue[cuda] @ git+https://github.com/AustinDKB/verse-cue"
verse-cue --setup
verse-cue
```

`--setup` lists **input** devices, then asks for the ProPresenter computer's
IP (default `127.0.0.1` if it is this machine) and port (default `1025`). It
prints the `ip:port` verse-cue will call, this computer's LAN IP, and
**Preferences → Network → Network API** on that port. Setup only writes mic +
host/port. The rest of `verse-cue.toml` is the locked live pick below.

### Focusrite / Windows: many devices, one mic

Windows lists the same Scarlett through MME / DirectSound / WASAPI, plus
loopbacks that look like inputs. A 2i2 is one stereo pair; verse-cue records
**mono** from channel 1 — plug the vocal into **input 1**.

Confirm in **Settings → System → Sound → Input** (or `mmsys.cpl` → Recording):
talk into the Focusrite and pick the name whose **level bar jumps**.

- Use: `Analogue 1+2`, `Microphone (Focusrite…)`, `Line In (Focusrite…)`
- Skip: `Loopback`, `What U Hear`, `Stereo Mix`, `Speakers (Focusrite…)` as input
- Same analog name two or three times: any of those; prefer **WASAPI** if listed

`--setup` already hides pure outputs. Loopback still appears because Windows
marks it as capture.

### Live hop view

ProPresenter only reports the slide on screen. Each hop prints two lines:

```
heard  our god is awesome
slide  our god is an awesome god he reigns from heaven above
```

`heard` is this window's Whisper words. `slide` is that current lyric: dim =
not heard yet, **green** = heard on this slide, **yellow** = last-3 match that
can arm Next. Use a terminal that shows ANSI colors.

## Locked live config

Bundled `verse-cue.toml` (do not drop a `verse-cue.auto.toml` over it):

| key | value | why |
|---|---|---|
| `name` | `small.en` | Best both-metrics vs tiny; distil/large add false |
| `window_s` / `hop_s` | 4 / **1** | Hop 0.5 cut false but two songs ran 3.64× / 3.91× (under 4×) |
| `prompt_mode` | `none` | `slide` / `hotwords`: miss ~2%, false ~70% |
| `tail_words` | 3 | Opening words cannot arm |
| `first_half` | true | Match must be past slide midpoint |
| `min_matched` | 4 | Three mumbled words do not click |
| `deadline_fire` | false | 1.0 s/word: miss 15.7 / false 30; 0.45 s/word: false 88 |
| aliases | bundled `aliases.json` (138) | Loaded even if CWD has no copy |

Line-by-line keys and metric definitions:
[docs/metrics/explainer.md](docs/metrics/explainer.md).

## Measured (2026-09-16 GPU)

`false%` = fired before the slide midpoint. `miss%` = never fired before the
next truth slide. `p90` = 90th percentile \|fire − truth\| in seconds. `rtf` =
song seconds / wall; gate is 4.0. Prefer early to miss.

Unless noted: 6 songs, 185 cues, 138 aliases, `window=4`, `prompt=none`, rate
wait on. Raw rows linked.

| run | hop | false% | miss% | p90 | rtf | ship? |
|---|---:|---:|---:|---:|---:|---|
| **small.en + live gates** ([small-improve.json](docs/metrics/small-improve.json)) | 0.5 | **14.6** | **25.9** | **12.1** | 4.87 | **gates yes; hop 1.0 in toml** |
| tiny.en, same gates | 0.5 | 14.1 | 35.7 | 11.9 | 7.22 | no (miss) |
| original tiny, no tail ([dedicated-1replica.json](docs/metrics/dedicated-1replica.json)) | 1.0 | 26.5 | 28.6 | 38.0 | 24.3 | no |
| tiny + `prompt=slide` | 1.0 | 71.3 | 1.9 | 42.7 | 16.7 | no |
| window 6 only (split W, [split-b.json](docs/metrics/split-b.json)) | 1.0 | 7.6 | 30.3 | 5.9 | 4.36 | no |
| deadline 1.0 s/word (split D1) | 1.0 | 30.3 | 15.7 | 18.3 | 4.9 | no |
| deadline 1.5 s/word (split D15) | 1.0 | 12.4 | 28.1 | 10.8 | 4.97 | no |

Vs original dedicated tiny: live-gate small.en is false **−12**, miss **−3**,
p90 **−26**. None of the 2026-09-16 split / combo cells beat that pick on
**both** miss and false. What moves each metric:
[docs/metrics/miss-and-false.md](docs/metrics/miss-and-false.md).

Bench audio is studio mix, not a live vocal. Sunday numbers will move.

![fire timing](docs/metrics/delta_hist.png)
![RTF per model](docs/metrics/rtf_vs_model.png)
![one song](docs/metrics/timeline.png)

## Configuration

One file, `verse-cue.toml`. `--setup` writes `[audio].device` and
`[propresenter]` host/port only.

Harvest extras (optional): `verse-cue-harvest vocals` then
`verse-cue-harvest bench` (needs `ffmpeg` and `yt-dlp` on PATH).

## Limitations

- Mix-bench vs a church vocal feed will shift false / miss.
- Word timestamps are about ±100 ms; remaining words are a rate estimate, not
  syllable-exact.
- CPU-only `small.en` may sit under 4× RTF; hop 1.0 is the production floor,
  not a CPU guarantee.
- `prompt_mode = "slide"` makes Whisper parrot the lyric. Leave it `none`.

## Help wanted

Run a Sunday, send `metrics.jsonl` and your hardware. Open an issue.

## Project history

`docs/ORIGINAL-PLAN.md` is the plan this started from. `docs/superpowers/` has
the spec and the implementation plan. `docs/COST.md` has what it cost to build.
`docs/brain-dump.md` is the raw first dump. GPU narrative:
[docs/metrics/live-gpu-findings.md](docs/metrics/live-gpu-findings.md).
