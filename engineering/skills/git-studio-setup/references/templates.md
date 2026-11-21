# The studio's files, as templates

The files phase 3 writes, each as a template to fill from the plan. A line in angle brackets is replaced or removed; nothing in angle brackets is committed. What each file is for is [studio.md](/engineering/docs/git/studio.md) and [studio-know-how.md](/engineering/docs/git/studio-know-how.md); this page is their text.

## studio.json

For a card news account, whose paths are the card news set's:

```json
{
  "unit": "post",
  "folder": "posts",
  "states": ["idea", "brief", "draft", "review", "approved", "scheduled", "published"],
  "person": ["approved"],
  "filed": "published",
  "ledger": "topics/covered.md",
  "needs": { "brief": ["topic-brief.json"], "draft": ["slide-plan.json", "caption.txt"], "review": ["review.md"] },
  "previews": ["out/*.png"],
  "shows": ["scheduled_for"],
  "large": ["img", "out"]
}
```

For rounds of ongoing work, which have no previews:

```json
{
  "unit": "round",
  "folder": "rounds",
  "states": ["planned", "running", "read", "decided"],
  "person": ["decided"],
  "filed": "decided",
  "ledger": "ledger.md",
  "needs": { "read": ["readings.md"] },
  "shows": ["change", "running_for", "decision"]
}
```

## The template folder

`<folder>/_template/<unit>.json`, with the fields of the kind after the shared ones (a round: `"change": ""`, `"why": ""`, `"running_for": null`, `"decision": ""`):

```json
{ "slug": "", "title": "", "status": "<first state>", "owner": "", "task": null, "created_at": "", "format": "<the format's folder, or leave the field out>", "notes": "" }
```

`<folder>/_template/README.md`, the next steps in the readers' language, four lines at most: which studio skill makes the unit, which command renders or reads it, where its review record goes, and `npm run file` after a change of state.

## The ledger

```markdown
# <What the studio has made | tried>

One row per <unit> from the moment it is started. `npm run new` adds the row and `npm run file` writes its state; `keys` are two to four specific names of what is <made | tried>, and a <unit> that holds a key of another row is made only on <the approver>'s word, kept in `note`. The table ends this file.

| slug | state | what | keys | who | note |
|---|---|---|---|---|---|
```

## SKILLCDN.md

```markdown
---
name: <The studio's name>
description: <What is produced here and for whom, in one sentence>. Use its skills when <the jobs, in the words a task uses>.
language: en
exclude:
  - <folder>
  - gallery
---
# Rules for every job in this studio

**<A rule about the work itself, in two or three words>.** <The rule, with its reason, in a sentence. Three to five rules: what a result never contains, what only <the approver> decides, what a run does before it ends.>

**Fold back.** A run ends with what it learned in the sentence it bears on: the guide page of the step, the policy's line, or the job's skill.
```

## A studio skill

`skills/<job>/SKILL.md`, an extension of one pack skill:

```markdown
---
name: <job>
description: "<What this job delivers here, from what>. Use when <the words a task or a person uses in this studio>. Extends <pack skill> of the pack."
skillcdn:
  include:
    - /docs/policy.md
---
# <The job, in the studio's words>

One <unit> of <the studio>, from <its input> to `<the state this job ends in>`. This skill extends `<area>/skills/<pack skill>/SKILL.md` of the pack and holds only what this studio answers and does differently.

## Before anything

Load the pack skill as served, every part of it: `console skill <area>/skills/<pack skill>/SKILL.md`. Run it as written, with the answers and the differences below. Where it and this page disagree, this page holds for what it states. Where the pack skill no longer has what an answer names, say so and mend this page in the same session.

## Standing answers

| The pack skill asks or names | Here |
|---|---|
| <its question, in its words> | <the policy's heading that answers it> |
| <a folder it names> | `<folder>/<slug>/` |
| <a helper it names> | `npm run <command>` |
| <a checkpoint of its> | <answered by the policy | by the task | stops for <the approver>, asked <where>> |

## What this studio does differently

- <One sentence with its reason.> Detail: [<step>](/docs/guides/<step>.md).

## Pages by phase

| Phase of the pack skill | Read first |
|---|---|
| <phase> | [<step>](/docs/guides/<step>.md) |

## The record

Starts from `<state>`, written by `npm run new`. Sets `<state>` when <what is done>, and never `<person state>`. `npm run file` after each change of state.
```

## docs/policy.md

```markdown
# The policy

<The approver>'s standing answers. A word of theirs that changes a line changes the line.

## <A heading per question the studio's skills would otherwise ask each run, and per standing choice>

<The answer, in their words.>

## Approval

<Who approves a <unit>, what they are shown, where they answer.>

## New techniques

<How often someone looks for a better way, and who decides a trial.>
```

A card news account takes its headings from the card news set's account record.

## A guide page

`docs/guides/<step>.md`, written when its first content exists:

```markdown
# <The step, as the studio calls it>

<What this page holds, in one sentence.>

## <One thing an agent would search for>

<What holds now: a procedure in the imperative, a fact as a statement with its evidence in the same sentence. A fact about an outside tool or site ends with the month it was last seen true.>
```

## docs/trials.md

Written with the first trial:

```markdown
# Techniques tried

One row per technique, rewritten as it moves. A dropped one is tried again only when its reason changed.

| Technique, and where it was found | Tried on | Compared against | What differed (result, time, cost) | State and why |
|---|---|---|---|---|
```

## The root's files

Added to what `git-repo-setup` writes, in files it keeps and completes.

`.gitattributes`, one line per subfolder that `large` names, and one per kind of large file wherever it lies:

```
<folder>/**/<subfolder>/** filter=lfs diff=lfs merge=lfs -text
*.mp4 filter=lfs diff=lfs merge=lfs -text
```

`.gitignore`: `gallery/` and `node_modules/`.

`package.json`, with the Node.js major that testing.md "Versions" finds:

```json
{
  "name": "<the repository's name>",
  "private": true,
  "type": "module",
  "engines": { "node": ">=<major>" },
  "scripts": {
    "check": "node scripts/check.mjs",
    "new": "node scripts/new.mjs",
    "file": "node scripts/file.mjs",
    "gallery": "node scripts/gallery.mjs",
    "serve": "node scripts/serve.mjs"
  }
}
```

`.github/workflows/check.yml`, with the actions' versions as testing.md "Versions" finds them. The checkout fetches no large file, which the check does not need; the second job runs on the Node.js version the `skillcdn` command asks for (`npm view @skillcdn/cli engines`):

```yaml
name: check
on:
  push:
    branches: [main]
  pull_request:
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v<major>
      - uses: actions/setup-node@v<major>
        with:
          node-version: <the major the repository pins>
      - run: npm run check
  pack:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v<major>
      - uses: actions/setup-node@v<major>
        with:
          node-version: <the version the command asks for>
      - run: npx --yes @skillcdn/cli@latest check
```

## What the agreement and the map gain

Handed to `git-repo-setup`, which writes `AGENTS.md` by agreement.md; in a repository that has its agreement, added to the section named. The agreement routes and stays short: what a job needs is in that job's skill.

- **Project.** What the studio produces, for whom, who approves, and its status.
- **Commands.** After the check: `npm run new`, `npm run file` ("after any change of state"), `npm run gallery` and `npm run serve` ("the review screen"), and the loading of a studio skill, `npx @skillcdn/cli@latest skill . skills/<job>/SKILL.md`.
- **Map.** The lines of studio.md's tree that exist, and the single sources: the design in `formats/`, a unit's state in its record, what was made or tried in the ledger, the person's answers in `docs/policy.md`, what the studio knows in `docs/guides/`.
- **Workflow.** Start gains: `git lfs pull` where previews are needed; `npm run check`, whose warnings are dealt with before the task; then the studio skill of the job. End gains: what the run learned folded back, `npm run file`, then the check, the commit and the push.
- **Rules**, within the eight, each with its reason: a person state is written only on that person's answer, with their words; the design changes only in `formats/` and a generated file is never edited by hand; one unit has one owner at a time.
- **Documentation protocol.** A standing word of the person: the line of `docs/policy.md`. Something learned: the sentence of the guide page it bears on. What had to be said in chat: the job's skill. A technique tried: its row in `docs/trials.md`. A format changed so that finished work would render differently: a new folder and a line in `docs/decisions.md`. A state or a field: `studio.json`, the template and `docs/architecture.md`.
- **Working alongside others.** The lines of studio.md "Working together" that hold for this team, in its own words.
- **Skills.** Under the shared paragraph, one line per studio skill: "`skills/<job>/`: <the job>. It names the pack skill it extends, loaded through the console." Then one line for the page that says how a studio skill is written, how a run is folded back and how a technique is tried: "`engineering/docs/git/studio-know-how.md` of the pack, read with `console skill --file <that path>`."
- **`docs/README.md`.** Rows for `policy.md`, `guides/` and, once it exists, `trials.md`; the row of `architecture.md` says it holds the unit's states and who writes each.
- **`README.md`.** The quick start gains `git lfs install`, `git lfs pull`, `npm run check`, then `npm run gallery` and `npm run serve` with the address they print.
