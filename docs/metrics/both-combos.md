# Both-metrics pair (combo A / combo B)

Goal: cut **miss% and false% together**, vs the live pick
`small.en` + rate wait + `tail_words=3` + first-half on + `min_matched=4`
(**false 14.6 / miss 25.9 / p90 12.1** at hop 0.5).

The 4-way miss grid showed that loosening those gates (tail=6, first-half off,
min_matched=3) is the wrong family for this goal: miss 18.9 but false 24.9 and
p90 35. `prompt=slide` is the same trap (miss 1.9 / false 71). These two cells
keep the tight arming rules and change *hearing* or *late salvage*.

One Secure L4 (or A40), two processes, same GPU. 6 songs, hop 1, `prompt=none`,
aliases on, rate wait on.

| cell | model | window | deadline_fire | gates |
|---|---|---:|---|---|
| **A** | distil-large-v3 | 4 | off | tail=3, first-half on, min_matched=4 |
| **B** | small.en | **6** | **on** | same tight gates |

## Why A

Distil without the tight gates already has the best fair-prompt miss (13.4 no
tail, 22.2 with tail=6 and no wait) and high false (~30) because extra matches
armed too soon. The small.en rate-wait pass showed those gates halved false
(24.3→14.6) while miss held. Putting distil behind that wall should keep false
near ~15 and turn “never reached last-3” into an on-time click.

This pairing has not been run before.

## Why B

Keep small.en (already the false winner). Raise Whisper `window` 4→6 so the
tail is more often actually in the transcript. Add **deadline fire**: if we
ever matched this slide and it has been up longer than
`n_words × default_sec_per_word` (0.45s), click now. That salvage is meant to
be late, so it should not count as false (`false` = fired before half the
*truth* slide duration). Neither lever was in the 4-way grid.

Wait-cap is **not** in B: clamping a long remaining wait fires *sooner* and
spends false.

`deadline_fire` defaults **off** in `verse-cue.toml`. Combo B turns it on in
the live cfg only.

## Next moves (decision tree, filled after the run)

Baseline to beat: false **14.6** / miss **25.9**. A “win” is both better, or
one down ≥3 pts with the other not worse by >1.

**Landed on 5.** B cut miss hard and exploded false. A did not cut miss.

1. **A wins, B does not.** Live pick → distil + current gates. Do not ship
   deadline. Optional follow-up: distil + window 6 (isolate B’s window).
2. **B wins, A does not.** Live pick stays small.en; ship window 6 +
   `deadline_fire`. Split B next (window-only vs deadline-only) so we know
   which lever carried it.
3. **Both win.** Next GPU cell: stack them (distil + window 6 + deadline +
   tight gates). Ship the stack if false stays near 15.
4. **A cuts miss, raises false.** Distil still arms last-3 too soon on
   repeats. Do not ship A. Stay on small.en; next miss-only lever is wait-cap,
   not another size bump.
5. **B cuts miss, raises false.** ← **this run.** Deadline at 0.45s/word
   fired ~22s early (median). Next: deadline at 1.0s/word and at
   `rate_bounds` hi (1.5s/word), plus a **window-6-only** small.en cell so we
   know whether the 6s window did any of the miss work. Keep tight gates.
   Do not ship `deadline_fire` at 0.45.
6. **Neither moves.** Misses are not “didn’t hear last-3” / “sat too long”.
   Next: wait-cap (lever 4) on small.en with tight gates. Do not restack the
   4-way “all three”.
7. **Either cell RTF < 4.** Drop B to window 5, or run the two cells
   sequentially on the same card. (Did not hit: A 5.7×, B 7.5×.)

## Results

Secure L4 `vdvj6i4fjbkhd1`, both processes one GPU. GHCR hot image failed to
pull (401), so this used a public pytorch image + yt-dlp of 6 songs (**mix**,
not vocal stems; **203 cues** vs the old 185). Compare directionally, not as
a paired A/B against the A40 14.6/25.9 cell.

Raw: `docs/metrics/combo-A.json` / `combo-B.json`.

| cell | model | window | deadline | rtf | false% | **miss%** | p90 | vs 14.6 / 25.9 |
|---|---|---:|---|---:|---:|---:|---:|---|
| baseline (A40, hop 0.5, stems) | small.en | 4 | off | 4.87 | 14.6 | 25.9 | 12.1 | — |
| **A** | distil-large-v3 | 4 | off | 5.70 | **13.3** | 30.5 | **6.5** | false −1.3, miss **+4.6 worse** |
| **B** | small.en | 6 | **on 0.45s/word** | 7.54 | 88.2 | **3.9** | 51.7 | miss −22, false **+73.6** |

A kept false and tightened p90; it did not hear more last-3s. B’s deadline
is the `prompt=slide` shape: almost never misses because it clicks ~22s early.

Do not ship either cell as the live pick. Next GPU: slower deadline +
window-6-only, still on small.en tight gates.
