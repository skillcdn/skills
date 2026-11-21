# A studio's know-how: a small pack of its own

What a studio knows outlasts what it made, and it lasts only when the next session reads little and still finds the right sentence. So a studio keeps its know-how as a pack in the SkillCDN Format inside the repository: a manifest with the few rules of every job, one small skill per job that extends a skill of the organization's pack, and pages by topic that each skill links from the phase that reads them. This page says how each is written, what an agent reads when, how a run's findings are folded back, and how a new technique is tried and adopted. Read when a studio is set up, when a studio skill or a page of its `docs/` is written, and at the end of a run that learned something. The repository's structure is [studio.md](studio.md).

## The manifest

`SKILLCDN.md` at the root: a `name`, a `description` of two sentences (what the studio produces and for whom, then when to use its skills), `language`, and `exclude` naming each unit's folder and `gallery`, so that a search of the studio finds what it knows and never an old unit. Its body holds only the rules that hold for every job here and are about the work itself: what a result must never contain, what a person alone decides, that a run ends with its findings folded back. A rule about the repository (secrets, the check, commits) is the agreement's, and neither file restates the other. The body arrives before every studio skill, so it stays within its bound ([studio.md](studio.md) "studio.json").

## A studio skill extends a pack skill

A job done here has one skill, `skills/<job>/SKILL.md`, and it is an extension: it runs a skill of the pack with this studio's standing answers and adds only what this studio does differently. It never copies the pack skill. The pack skill is loaded as served at the start of every run, every part of it, so a technique the pack gains reaches the studio without an edit, and the studio's own text stays small enough to keep true.

A job that uses one phase of a pack skill (a round reads `meta-ads-setup` for its monitoring alone) loads less, and its skill says which parts: the pack's rules, which a whole load would have brought (`SKILLCDN.md` at the pack's root and the area's), then the pack skill's hard rules and that one phase, each read as a section. The file's outline gives the sections (`console skills <path>`, or `browse_repo` on the file through a connection), and one is read with `console skill --file <path> --offset <n> --limit <n>`, or with `read_repo_file` and the same two numbers (console and SkillCDN 0.5, checked 2026-11).

| Goes in the studio skill | Stays in the pack skill |
|---|---|
| Which pack skill it extends, by its path in the pack, and that it is loaded first | The method: the phases, how a thing is found, made, measured and reviewed |
| The standing answers to that skill's questions and inputs: the policy's lines, the format's folder, the unit's folder in place of the folders it names, the studio's scripts in place of its helpers | The questions themselves, and the defaults for whoever has no studio |
| How its checkpoints are answered here: which the policy answers, which the task answers, which stops for the person and where they are asked | The checkpoints and what each message holds |
| What this studio does differently, each as one sentence with its reason, and the page that holds the detail | Its verdicts and hard rules |
| The states of the unit this job writes, and the ledger | |
| A table of its phases with the page of `docs/guides/` each reads | |

Where the two disagree, the studio skill holds for what it states and the pack skill for everything else. An extension narrows and adds; it never loosens what the pack's rules say of spending, of what leaves, of what a person confirms, and a step it wants skipped is written as a difference with its reason, never left out in silence. Where the pack skill changed under an answer (an input renamed, a phase gone), the run says so and the extension is mended in the same session. A difference that would serve every user of the pack skill is a task for the pack's maintainers, not a local patch that the next release contradicts.

A job no pack skill covers gets a skill written whole, in the format's shape, and stays as small: its method in the body, its detail in the pages.

## The policy and the pages

- **`docs/policy.md`** is the person's standing answers under headings: what is made and for whom, what the studio takes on and what it leaves, how it speaks, how often it delivers, who approves and what they are shown, how often new techniques are looked for. It is written in the language [layout.md](layout.md) gives every document an agent reads, and a line keeps the person's own words, as a quotation, only where the wording itself is the rule (a phrase the account never uses). A word of the person's that changes a line changes the line, never a note beside it, and a correction given twice goes in before the run ends. An answer that lives only in an agent's memory is not policy.
- **`docs/guides/<step>.md`** is one page per step of the work, named as the step is called (`sourcing`, `pictures`, `review`, `reading-results`). It says what holds now: a procedure in the imperative, a fact as a statement, with the evidence in the same sentence and one section per thing an agent would search for. A fact about an outside tool or site carries the month it was last seen true. There is no dated entry, no account of a run, and no list of lessons: a lesson replaces or sharpens the sentence it bears on, and where none bears on it, it becomes a sentence under the heading it belongs to.
- **A fact lives in one page.** Every other page and skill links there. A rule that hardened moves to where rules live (the policy, the manifest, the format's README) and leaves the guide.
- **`docs/decisions.md`** keeps the one dated line per decision that layout.md gives it: a format's new version, a technique adopted, a state added.

## What is read, and when

| When | An agent reads | Never |
|---|---|---|
| A session starts | `AGENTS.md`, which the host hands it and which only routes (the commands, the map, which skill does which job), and the task; what it then does first is [studio.md](studio.md) "Working together" | The guides, the policy, the ledger |
| One job | That job's studio skill, with the manifest's rules before it and the policy after it, which is the one page it includes; then the pack skill it names, or the parts of it the studio skill names; then, phase by phase, the guide page the phase links | Another job's skill, a guide no phase of this job links, the other kind's units beyond the slugs this unit names |
| A question whether something was made or tried | The ledger, by a search for the key | The filed folders |
| Before reversing a choice | The line of `docs/decisions.md`, the row of `docs/trials.md` | |

In the checkout a studio skill is read as it would be served, from the files as they are: `npx @skillcdn/cli@latest skill . skills/<job>/SKILL.md` prints the manifest's rules, the skill and its included page, with no deployment involved (`skillcdn` command 0.5.3, checked 2026-11). Where the command cannot run, the three are read as files: `SKILLCDN.md`, the skill, the pages its `skillcdn.include` names. The pack skill is read through the console (`console skill <path>`) or the host's connection to the pack, never from a copy in the studio.

## Folding work back

After a unit, a batch or a round, before the run finishes, each thing learned goes to one place:

| What the run met | Goes to |
|---|---|
| A fact about the work or a tool, a way that worked, a mistake with its cause | The sentence it bears on in the guide page of that step |
| A correction of the person's that holds from now on | The policy's line |
| What had to be said in chat for the job to go right, what the agent had to guess, a stop that was answered the same way again | The studio skill: a standing answer or a difference. The pack's `skillcdn-skill-authoring` does this from the work done ("Improving a skill from a run"); in a studio the shapes are this page's |
| Something every user of the pack skill would gain | A task for the pack's maintainers |
| A slip of one run | The run's report, nowhere else |

The fold is part of the job's end, in the same commit as the unit where the push goes straight to the main branch. The check then holds the bounds: a page that outgrew its limit is split by topic, not trimmed of what is true.

## Trying a new technique

Production moves with the newest technique the team finds: a tool, a model, a method, met in a run or looked for on the cadence the policy names. The pack skill's own gains arrive by themselves. Anything else enters through a trial, never straight into the skill:

1. **One unit, both ways.** The technique is used on one unit, beside the current way on the same input where that can be had, else against the last units made the current way. The unit's record says `trial` with the technique in a few words.
2. **The row.** `docs/trials.md` gains or updates one row per technique: what it is and where it was found, the unit it ran on, what it was compared against, what differed in the result, the time and the cost, and its state (`trying`, `adopted`, `dropped`) with the reason.
3. **The decision** is asked of the person the policy names, with both results side by side on the review screen.
4. **Adopted:** the studio skill and the guide page change in one commit with a line in `docs/decisions.md`, and the row names the section that now carries it. **Dropped:** the row keeps the reason, so the technique is tried again only when what made it fail has changed.

## Serving the pack, and the checks

A studio is worked in its checkout, so serving it is optional: SkillCDN serves a private repository in full to the people who can see it on the git host, once the deployment's app is installed on it, which lets a session outside the checkout load a studio skill and search the pages by meaning (SkillCDN 0.5, checked 2026-11; its guide "Use skills from your AI", "Private repositories"). The console project keeps reading the organization's pack, where the skills the studio extends live ([console.md](console.md) "The project's pack"). What a push then serves, and when, is [serving.md](/engineering/docs/skillcdn/serving.md).

**The checks.** The studio's own check holds the links, the bounds, the orphan pages and the routes ([studio.md](studio.md) "The check"). `npx @skillcdn/cli@latest check` reads the studio as the indexer would, served or not, and reports a front-matter that does not parse, an include that names no page, a fragment that names no section and a page too large to search; continuous integration runs it as a job of its own, since it needs the network. Documents the team already has in another form (a brand guide as a PDF, briefs in a wiki) are brought under `docs/` with `skillcdn-document-pack`.
