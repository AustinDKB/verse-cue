---
name: youtube-to-skill
description: >-
  Turns a YouTube video into a knowledge-base agent skill in the book-skill
  format (.agents/skills style). Use when the user gives a YouTube URL and
  asks to make a skill from the video, convert a talk or tutorial into a
  reusable skill, extract the method from a video, or learn a video deeply.
---

# YouTube To Skill

## Mission

You convert one YouTube video into a reusable agent skill. The output format
matches the book skills in `.agents/skills/` (getting-real, shape-up). You do
this only when the video contains a transferable method. You decline when it
does not.

## Feasibility facts (this server)

- This server's IP is blocked by YouTube. A direct fetch without cookies fails.
- The working recipe on this server: cookies (`--cookies cookies.txt`) plus the
  node JavaScript runtime and the ejs challenge-solver component. The fetch
  script already passes `--js-runtimes node --remote-components ejs:github`.
- Without cookies, the working paths are a pasted transcript or the oEmbed
  title and channel only.
- The oEmbed endpoint still returns the title and channel when blocked.
- On a residential IP, the direct fetch works without cookies.

## Gate: is this video skill-worthy?

Fetch first, then judge. A video is skill-worthy when all of these are true:

- It teaches a method, framework, process, decision rules, or technique.
- The transcript is readable and the language is known.
- The content has structure that transfers (steps, principles, examples).
- An agent would apply the knowledge after the video ends.

Refuse with a reason when:

- The video is music, news, entertainment, or a vlog with no method.
- The transcript is garbled or the captions are missing.
- The video is a rant or a pitch with no actionable content.
- The content is under 3 minutes with no substance.

State the gate decision to the user first. When you refuse, give the reason
and stop.

## Workflow

### 1. Fetch the transcript

Run the fetch script from the repository root:

```bash
python .pi/skills/youtube-to-skill/scripts/fetch_transcript.py "<URL>"
```

The script runs yt-dlp through `uvx`. It does not change project
dependencies. It writes to `tmp/youtube-to-skill/<video-id>/` by default:
`transcript.txt`, `metadata.json`, and the raw subtitle files.

Read the `FETCH_STATUS` line in the output:

- `OK` — continue to step 2.
- `BLOCKED` — YouTube blocks this IP. Use one of these paths:
  - Ask the user for a cookies.txt export (Netscape format, signed-in
    browser). Save it under `tmp/youtube-to-skill/cookies.txt`, retry with
    `--cookies`, then delete the file after the fetch.
  - Ask the user to paste the transcript. Save it as
    `tmp/youtube-to-skill/<video-id>/transcript.txt`, then continue.
  - The metadata.json from a blocked fetch holds the title and channel
    from oEmbed. Duration and chapters are absent. Ask the user for the
    duration when the skill header needs it.
- `UNAVAILABLE` — the video is private, removed, or region-locked. Report
  this and stop.
- `NO_CAPTIONS` — the video has no captions. Offer the cookie or paste
  paths, or decline when the user has no transcript.
- `NOT_YOUTUBE_URL` — the input is not a YouTube URL. Ask for a valid URL.

Never fabricate a transcript. Never invent the video's content.

### 2. Analyze the video deeply

Read the full transcript before you build anything. Do these steps:

1. Read `metadata.json`. Note the title, channel, duration, and chapters.
2. Read `transcript.txt` in full. Long transcripts need multiple reads.
3. Extract the method: frameworks, steps, principles, decision rules,
   examples, terms, and anti-patterns.
4. Use the video's chapter markers to segment the content. Without chapter
   markers, segment by topic change with timestamps.

A transcript that is only auto-captions may contain errors. When a section
is unclear, mark it `[transcript unclear]` in the output. Do not guess.

### 3. Build the skill

Follow `references/output-template.md` exactly. Write the generated skill to
`.agents/skills/<skill-name>/` unless the user names another location. When
`.agents/skills/` is not writable (root-owned), create the directory with
`sudo mkdir -p` and `sudo chown -R $USER` first, or use `.pi/skills/`.

The generated structure:

```
.agents/skills/<skill-name>/
├── SKILL.md
├── chapters/            # Only when the video has 3+ distinct sections
├── glossary.md
├── patterns.md
└── cheatsheet.md
```

Use the video's own method as the core frameworks. A 15-minute talk usually
yields 2-5 frameworks and no chapters directory. A course or long talk
yields the full structure.

### 4. Verify

Run the verification checklist at the end of `references/output-template.md`.
Fix every failed item before you report completion.

## Output rules

- Write clear, concise prose: short sentences and active voice.
- Ground every framework, rule, and example in the transcript.
- Derive the skill name from the video's method. Lowercase letters, numbers,
  hyphens, max 64 characters.
- Put the gate decision, the skill path, and the checks in the report.

## References

- `references/output-template.md` — the generated skill format and the
  verification checklist.
