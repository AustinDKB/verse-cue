# Cost to build verse-cue

Token and USD cells come from provider dashboards. `n/a` means the dashboard
was not available at write time — not an estimate.

| Session | Purpose | Model | Input tokens | Output tokens | USD | Wall time |
|---|---|---|---|---|---|---|
| 2026-09-14 planning | Spec + implementation plan | Claude Fable 5.1 (Cursor) | n/a | n/a | n/a | ~2 h |
| 2026-09-14 implement | Execute the plan on `main` | Cursor Grok 4.6 | n/a | n/a | n/a | see git log |
| harvest download | `verse-cue-harvest download --limit 100` | (local yt-dlp) | — | — | $0 | 12.3 min, 99 songs with synced lyrics |
| harvest bench | `tiny.en` 4s/1s, 5 songs | local Whisper | — | — | $0 | 4.2 min |
| harvest aliases | `verse-cue-harvest aliases --limit 100` | local Whisper | — | — | $0 | started in background after bench |

**Total USD (known):** n/a until dashboards are filled.

No cloud transcription API was used. Audio for aliases and bench is downloaded
from YouTube via yt-dlp; lyrics from lrclib.net.
