# Output template: video-derived skill

The generated skill must follow the book-skill format used in `.agents/skills/`
(getting-real, shape-up). Match the structure exactly. Fill every field with
content grounded in the transcript. Do not invent content.

## Directory layout

```
<skill-name>/
├── SKILL.md            # Required
├── chapters/           # One file per video section (3+ sections only)
│   └── chNN-slug.md
├── glossary.md         # Terms from the video
├── patterns.md         # Techniques from the video
└── cheatsheet.md       # Decision rules and quick reference
```

Skip `chapters/` when the video has fewer than 3 distinct sections. Put all
content in `SKILL.md` instead, and keep `glossary.md`, `patterns.md`, and
`cheatsheet.md`.

## SKILL.md template

````markdown
---
name: <skill-name>
description: "Knowledge base from the video \"<Title>\" by <Channel>. Use when <the situations the video's method applies to>, applying <method names>, or referencing the video's concepts."
---

<!-- argument-hint: [topic, framework name, or section number] -->

# <Video Title>
**Source**: <Channel> | <Duration> | <Published date if known>

## How to Use This Skill

- **Without arguments** — load the core frameworks and decision rules.
- **With a topic** — ask about `<framework>` or another indexed topic.
- **With a section** — ask for `ch03` to load that section.
- **Browse** — ask which sections or supporting files cover a topic.

When a question needs detail outside Core Frameworks, read the relevant section file before answering.

## Core Frameworks & Mental Models

### 1. <Framework name>
Use **<framework>** when <condition>. <2-4 concrete rules from the video, each
one sentence>. <Named sub-technique from the video> covers <what it does>.
Keep each rule short and actionable. Number each framework.

### 2. <Framework name>
...

### Default decision sequence

1. <First step of the video's method>
2. <Second step>
3. <Remaining steps, max 6>

## Section Index

| File | Section | Frameworks |
|------|---------|------------|
| [ch01](chapters/ch01-slug.md) | <Section title> | <frameworks it introduces> |
| [ch02](chapters/ch02-slug.md) | <Section title> | <frameworks it introduces> |

## Topic Index

- **<Topic>** → ch01, ch03
- **<Topic>** → ch02

## Supporting Files

- [glossary.md](glossary.md) — key terms and definitions.
- [patterns.md](patterns.md) — techniques and design patterns.
- [cheatsheet.md](cheatsheet.md) — decision rules and quick reference.

## Scope & Limits

This skill covers *<Video Title>* content and navigation to its section files.
It reflects the video's method only. It does not replace domain research or
project-specific instructions. Transcript quality limits: <note auto-caption
uncertainty if the captions were auto-generated>. Read a section file for
detail when a decision needs more context.
````

## Section file template (`chapters/chNN-slug.md`)

````markdown
# Section N: <Section Title>

## Core Idea
<One paragraph. State what this section teaches and when to use it.>

## Frameworks Introduced
- **<Framework>**: <What it is, when to use it, and the rules the video gives.>
- **<Sub-technique>**: <Details.>

## Key Concepts
- **<Term>**: <Definition from the video.>

## Mental Models
- **<Model>**: <The way of thinking the video teaches.>

## Anti-patterns
- **<Mistake>**: <What it is and why it fails.>

## Worked Example
<The example from the video. Write it as a short narrative with a concrete
outcome. If the video has no example, write a brief scenario that follows the
method.>

## Key Takeaways
1. <Takeaway from the video>
2. <Max 6 items>

## Connects To
- **Section N, <Title>**: <How they relate.>
````

## glossary.md

One entry per term the video defines or uses as a concept:

```markdown
# Glossary

- **<Term>**: <Definition, one or two sentences.>
```

## patterns.md

One entry per technique the video teaches. Name the pattern, state when to use
it, and give the steps:

```markdown
# Patterns

## <Pattern name>
Use when <condition>.
1. <Step>
2. <Step>
```

## cheatsheet.md

A quick-reference file. Use the video's own decision rules:

```markdown
# Cheatsheet

## Decision rules
- <Condition> → <Action>
- <Condition> → <Action>

## Quick reference
| Topic | Rule | Section |
|-------|------|---------|
| <Topic> | <Rule> | ch01 |
```

## Naming rules

- Skill name: lowercase letters, numbers, hyphens. Max 64 characters. Derive
  it from the video's method, for example `shape-up` or `system-design-talks`.
- Section files: `chNN-slug.md`. Use `ch01`, `ch02` in source order. Slug from
  the section title, for example `ch05-whats-your-problem.md`.
- Use one term per concept. Do not switch synonyms.

## Grounding rules

- Base every framework, rule, and example on the transcript.
- Write clear, concise prose: short sentences and active voice.
- Where the transcript is unclear, write `[transcript unclear]` at that spot.
  Do not guess the content.
- Attribute examples to the video's own cases when it gives them.

## Verification checklist

Run this checklist before reporting completion:

- [ ] SKILL.md has valid frontmatter: lowercase-hyphen name, specific
      third-person description under 1024 characters.
- [ ] SKILL.md is under 500 lines.
- [ ] Every section index entry points to an existing file, one level deep.
- [ ] Frameworks, rules, and examples come from the transcript.
- [ ] Glossary, patterns, and cheatsheet files exist and match the index.
- [ ] Prose is clear and concise (short sentences, active voice).
- [ ] The gate decision is reported to the user first.
