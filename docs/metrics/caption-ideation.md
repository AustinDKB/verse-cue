# Ideation — LAN captions for hard of hearing (2026-09-20)

Notes only. Do not code from this file unless a later prompt asks. Came out of the Sep 20 rehearsal chat, after the morning set and before / during the service sim.

Goal: after worship, people on **church WiFi only** can read the **sermon** on a phone. Not a camera. Not the lyric slides (unless they happen to be up). Live **captions** for hard of hearing.

## What it is not

- **Not a video stream.** OBS / HLS / NDI to phones is overkill and will melt guest WiFi. NDI is ~100 Mbps; this is words.
- **Not “show the current ProPresenter slide.”** Useful as a bonus, but the ask is the **spoken** sermon. If the pastor talks with no slides, slide-repeat is blank.
- **Not opening port 50001 to guest phones.** That API can fire Next and macros. Any phone page talks to a **read-only** caption server on the LAN.

WiFi-only = bind to a private address, no port-forward. Anyone on that SSID can open the URL. Guest **AP isolation** will block phones from reaching the box — same failure as any LAN page.

## What we already have

verse-cue already eats the house vocal mic and runs Faster-Whisper every hop (`small.en`, window 4 s, hop 1 s). `slide.raw` is the last window’s words. That is the hard part.

Do **not** ship the hop dump to phones as-is:

- The 4 s window **overlaps**. Raw hops repeat the same words.
- Live path **lowercases and strips punctuation** (`WORD_RE`) for lyric align.
- `condition_on_previous_text=False` on purpose so the clicker does not parrot the last slide.
- Pause **stops transcription**. Captions need to keep running when Next is paused.
- Blank-slide hallucination (pads / room) is a worship problem. Sermon-only start (or VAD-gate) avoids inventing sentences over silence.

Spoken sermon is an easier job for Whisper than singing. Latency today is about **2–5 s** behind the pulpit (4 s window + infer + 1 s hop). That is normal for this kind of caption. Not CART.

## Hop and window (for captions)

- **Window** = how many seconds of tape one gulp hears.
- **Hop** = how often we take a new gulp.

Worship clicker stays **4 / 1**. It only needs the last few lyric words.

Captions can use a **longer window** (8–12 s) and **rewrite words already on the phone**. Operator is fine with a flicker when the next gulp fixes `cavalry` → `Calvary`. That is the product: draft line, then correct the tail. Longer window is one bigger bite stepping forward, **not** extra streams.

## Medium, and why lyrics / sermon must not share VRAM

Lyrics and sermon **will never overlap**. One GPU can do both, **one model at a time**.

- **Do not** put `medium.en` on the worship clicker. Bigger models heard more words and armed Next earlier (distil raised false; medium was never on the live pick). Keep `small.en` + current gates for songs.
- **Do** unload `small.en` and load `medium.en` when the sermon starts. Same mic. Caption page only. No Next.
- Swap cost is load-to-GPU, usually **10–30 s** after the weights exist. Use the hole after the last song (talk / prayer / welcome). Pause the clicker first so a leftover hop cannot fire.

This box has **no `medium.en` RTF number**. Speech should hold hop 1–2 s. If a hop’s infer is > ~0.8 s, bump hop to 1.5–2 s. Captions can sit 3–6 s behind. The clicker cannot.

Sunday shape:

1. Worship — `small.en`, verse-cue as today.
2. Gap — pause, unload small, load medium.
3. Sermon — medium captions to `http://10.x.x.x/captions`. No slide firing.
4. Done — unload, or leave medium until next week’s worship load.

Keep this **off** a change to `[model].name` in `verse-cue.toml`. Caption mode is a second path that only loads after pause.

## Offset streams (the original brain-dump idea)

Staggered windows (0–3, 1.5–4.5, 3.5–7) “at once” were already dropped for the clicker: **one Faster-Whisper on one GPU serializes**. That is the same work as `window_s` / `hop_s`. Hop 0.5 vs 1 was the real “sample more often” test; it barely moved miss and dipped two songs under 4× RTF.

N offset copies of the same audio do not invent new signal. Today already overlaps 75% (window 4 / hop 1) and `merge()` keeps older words.

If we still want “two qualities” after the swap:

1. **Fast partial** — even medium on 8–12 s / hop 1–2, append + revise the tail.
2. **Final line** — when VAD says the sentence ended, one decode of that whole phrase **replaces** the draft.

That is two jobs, not three identical replicas. Voting three medium windows can cut hallucinations and also drop a correct name that only one window heard. For a sermon, **condition on the previous committed sentence** is the cheaper quality win. Clicker’s `condition_on_previous_text=False` stays. Captions want the opposite.

Chopping speech into fixed 3 s slices is what makes Whisper splice badly. VAD-cut phrases into medium beat staggered slices.

A second GPU would be the only reason to run a live small partial and a medium final **at the same time**. Until then, sequential swap is enough.

## Mic

Captions only work if the verse-cue input still hears the preacher (same vocal bus, or a house mix that includes the pulpit). A singing-only channel will miss the sermon.

## Logging we would want if we build this

Not for this PR. If captions ship later: one JSON line per gulp with `heard` (cased, punctuated), `revised` (which prior tokens changed), `infer_s`, `paused_clicker`, `model`. Still no full audio on Sunday.

## Status

Ideation only. No click-loop change. No page, no model swap, no hop-log yet. Telemetry for the day that produced this is `live-session-2026-09-20.jsonl` / `live-notes-2026-09-20.md`.
