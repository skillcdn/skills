# The studio's files, as templates

The files phase 3 writes, each as a template to fill from the plan. A line in angle brackets is replaced or removed; nothing in angle brackets is committed. What each file is for is [studio.md](/engineering/docs/git/studio.md), [studio-know-how.md](/engineering/docs/git/studio-know-how.md) and [studio-operating.md](/engineering/docs/git/studio-operating.md); this page is their text.

## studio.json

For a card news account, one kind of unit, whose paths are the card news set's:

```json
{
  "units": [
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
  ]
}
```

For an ad studio, two kinds: creatives that are made, shown by their video, and the rounds that tune the running ones, which have no previews. A studio of rounds alone holds the second entry alone:

```json
{
  "units": [
    {
      "unit": "creative",
      "folder": "creatives",
      "states": ["idea", "script", "draft", "review", "approved", "launched"],
      "person": ["approved"],
      "filed": "launched",
      "ledger": "ledger/creatives.md",
      "needs": { "script": ["script.md"], "review": ["review.md"] },
      "previews": ["out/*.mp4", "out/*.png"],
      "shows": ["hook"],
      "large": ["ref", "out"]
    },
    {
      "unit": "round",
      "folder": "rounds",
      "states": ["planned", "running", "read", "decided"],
      "person": ["decided"],
      "filed": "decided",
      "ledger": "ledger/rounds.md",
      "needs": { "read": ["readings.md"] },
      "shows": ["change", "running_for", "decision"]
    }
  ]
}
```

A round that reads (a market watch) is the round entry with `"states": ["planned", "read", "reviewed"]`, `"person": ["reviewed"]`, `"filed": "reviewed"`, `"standing": ["market/watch.json"]`, `"needs": { "read": ["report.md"] }` and `"shows": ["planned_for", "moved"]`. The standing file is written by the pack skill's first run, or laid empty in that skill's shape, before the check is run.

## The template folder

One per unit: `<folder>/_template/<unit>.json`, with the fields of the kind after the shared ones (a creative: `"hook": ""`, `"reference": ""`; a round that changes: `"change": ""`, `"why": ""`, `"running_for": null`, `"decision": ""`, and `"creatives": []` where the studio makes them too; a round that reads: `"planned_for": null`, `"moved": ""`):

```json
{ "slug": "", "title": "", "status": "<first state>", "owner": "", "task": null, "created_at": "", "format": "<the format's folder, or leave the field out>", "notes": "" }
```

`<folder>/_template/README.md`, the next steps in the readers' language, four lines at most: which studio skill makes the unit, which command renders or reads it, where its review record goes, and `npm run file` after a change of state.

## The ledger

One per unit, at the path its entry names, outside the unit's folder, which the manifest keeps out of a search:

```markdown
# <What the studio has made | tried | read>

One row per <unit> from the moment it is started. `npm run new` adds the row and `npm run file` writes its state; `keys` are two to four specific names of what is <made | tried | read>, and a <unit> that holds a key of another row is made only on <the approver>'s word, kept in `note`. Search this table for a name; do not read it whole. The table ends this file.

| slug | state | what | keys | who | note |
|---|---|---|---|---|---|
```

## SKILLCDN.md

```markdown
---
name: <The studio's name>
description: <What is produced here and for whom, in one sentence>. Use its skills when <the jobs, in the words a task uses>.
language: en
start: docs/start.md
exclude:
  - <each unit's folder>
  - gallery
---
# Rules for every job in this studio

**<A rule about the work itself, in two or three words>.** <The rule, with its reason, in a sentence. Three to five rules: what a result never contains, what only <the approver> decides, what a run does before it ends.>

**Fold back.** A run ends with what it learned in the sentence it bears on: the guide page of the step, the policy's line, or the job's skill.
```

## docs/start.md

The one page of the studio every session reads; it routes and says nothing else. The link in its last row is to this pack, by its skill URI, as the studio's skills link theirs:

```markdown
# Start here

<What this studio makes or runs, and for whom, in one sentence.> Read this page, then the skill of your job, then only what that skill's phases link.

## Jobs

| The task says | Skill | Unit, and the state the job ends in |
|---|---|---|
| <the job, in the words a task uses> | [<job>](/skills/<job>/SKILL.md) | <unit>: `<state>` |

## Where a question is answered

| Question | Read |
|---|---|
| What is open, what waits for a person, what is due | The last lines of `npm run check` |
| Was this made or tried before | A search of `<ledger>` for the name; `npm run new` refuses a repeat |
| What has <the approver> settled | [policy.md](policy.md), which every skill here carries |
| What is known about <step> | [guides/<step>.md](guides/<step>.md) |
| Why is it this way | [decisions.md](decisions.md); a technique tried: [trials.md](trials.md) |
| How a skill here is written, a run folded back, a technique tried | [studio-know-how.md](skill://gh/skillcdn/skills/engineering/docs/git/studio-know-how.md) of the pack |
| How a batch is divided, what a session on a schedule may do | [studio-operating.md](skill://gh/skillcdn/skills/engineering/docs/git/studio-operating.md) of the pack |

## What no session reads

A filed unit no skill names as an example, `gallery/`, another job's skill, the history.
```

A row for a page that does not exist yet (`trials.md`, a guide) is left out until the page is written.

## A studio skill

`skills/<job>/SKILL.md`, an extension of one pack skill. `<pack>` is the address of the pack the console project reads, `gh/skillcdn/skills` for this one:

```markdown
---
name: <job>
description: "<What this job delivers here, from what>. Use when <the words a task or a person uses in this studio>. Extends <pack skill> of the pack."
skillcdn:
  include:
    - /docs/policy.md
---
# <The job, in the studio's words>

One <unit> of <the studio>, from <its input> to `<the state this job ends in>`. This skill extends [<pack skill>](skill://<pack>/<area>/skills/<pack skill>/SKILL.md): load it first, every part, then apply what differs below. It holds only what this studio answers and does differently.

## Before anything

Load the pack skill as served: `console skill <area>/skills/<pack skill>/SKILL.md`. <Or, where this job uses one phase of it: read the pack's rules, the skill's hard rules and its phase "<name>", each as a section, as studio-know-how.md "A studio skill extends a pack skill" says.> Run it as written, with the answers and the differences below. Where it and this page disagree, this page holds for what it states. Where the pack skill no longer has what an answer names, say so and mend this page in the same session.

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

<Once units are filed: "An example to open: `<folder>/<filed>/<day>/<slug>/`, for <what it shows>." Two at most.>

## The record

Starts from `<state>`, written by `npm run new`. Sets `<state>` when <what is done>, and never `<person state>`. `npm run file` after each change of state.
```

## docs/policy.md

```markdown
# The policy

<The approver>'s standing answers. A word of theirs that changes a line changes the line.

## <A heading per question the studio's skills would otherwise ask each run, and per standing choice>

<The answer, in the language of the documents; their own words, quoted, only where the wording itself is the rule or the reason.>

## Approval

<Who gives each person state, what they are shown, where they answer; who changes a format and this page. A class of units approved in advance, with their words.>

## Roles

<Which role does which part of the work when several units are made at once, and which model runs it at which effort; the row of trials.md that settled it. Left out until a batch is run.>

## New techniques

<How often someone looks for a better way, and who decides a trial.>
```

A card news account takes its headings from the card news set's account record, and adds none that record lacks before a run asks for it.

## A guide page

`docs/guides/<step>.md`, written when its first content exists, with its row in the start page:

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

`.gitattributes`, one line per subfolder that a unit's `large` names, and one per kind of large file wherever it lies:

```
<folder>/**/<subfolder>/** filter=lfs diff=lfs merge=lfs -text
*.mp4 filter=lfs diff=lfs merge=lfs -text
```

`.gitignore`: `gallery/`, `.cache/` (what a run fetches or installs for itself) and `node_modules/`.

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

`.github/workflows/check.yml`, with the actions' versions as testing.md "Versions" finds them. The checkout fetches no large file, which the check does not need; the second job runs on the Node.js version the `skillcdn` command asks for (`npm view @skillcdn/cli engines`). Where the pack the studio extends is private, the second job's step gains `env` with `SKILLCDN_URL` and `SKILLCDN_TOKEN` from the repository's secrets, which a person sets; without them that pack's files are reported as not known and nothing fails:

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
      - run: npx --yes @skillcdn/cli@latest check --references
```

## What the agreement and the map gain

Handed to `git-repo-setup`, which writes `AGENTS.md` by agreement.md; in a repository that has its agreement, added to the section named. The agreement says how the repository is worked and stays short: which job is which skill is the start page's, and what a job needs is in that job's skill.

- **Project.** What the studio produces, for whom, who approves, and its status.
- **Commands.** After the check ("its last lines say where the studio stands"): `npm run new` (with the unit's name first where the studio holds several kinds), `npm run file` ("after any change of state"), `npm run gallery` and `npm run serve` ("the review screen"), and the loading of a studio skill, `npx @skillcdn/cli@latest skill . skills/<job>/SKILL.md`.
- **Map.** The lines of studio.md's tree that exist, and the single sources: the design in `formats/`, a unit's state in its record, what was made or tried in the ledger, the person's answers in `docs/policy.md`, what the studio knows in `docs/guides/`.
- **Workflow.** The start and the end of a session as studio-operating.md "Which change goes where" gives them ("A session starts"), in the team's words, with a line that sends every session to the start page, its path written as a link: "Read docs/start.md before the task's first step."
- **Rules**, within the eight, each with its reason: a person state is written only on that person's answer, with their words; the design changes only in `formats/` and a generated file is never edited by hand; one unit has one owner at a time; nothing leaves but through a job's skill, after the person's state.
- **Documentation protocol.** A standing word of the person: the line of `docs/policy.md`. Something learned: the sentence of the guide page it bears on. What had to be said in chat: the job's skill. A rule a script can test: the kind's check. A technique tried: its row in `docs/trials.md`. A format changed so that finished work would render differently: a new folder and a line in `docs/decisions.md`. A state or a field: `studio.json`, the template and `docs/architecture.md`. A job or a guide page added: its row in `docs/start.md`.
- **Working alongside others.** The lines of studio-operating.md that hold for this team, in its own words: a clone each, which change goes where, the roles of a batch where one is run, what its sessions on a schedule do.
- **Skills.** Under the shared paragraph, one line: "The jobs of this studio and their skills are in `docs/start.md`; each skill names the pack skill it extends, read through the console."
- **`docs/README.md`.** Rows for `start.md`, `policy.md`, `guides/` and, once it exists, `trials.md`; the row of `architecture.md` says it holds the unit's states and who writes each.
- **`README.md`.** The quick start gains `git lfs install`, `git lfs pull`, `npm run check`, then `npm run gallery` and `npm run serve` with the address they print.
