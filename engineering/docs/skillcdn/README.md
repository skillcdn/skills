# SkillCDN: what its skills share

The skills that work on a repository in the SkillCDN Format (`skillcdn-…`) share how the service turns a push into what an agent is served, how an agent with none of the session's context is started on each host, and where a session's record and memory are kept. That lives here once, one file per topic, kept current in one place; each skill includes or links the page from the phase that reads it and carries its own method (what it asks, where it stops, what it accepts, its rules) itself.

| Document | Holds | Read |
|---|---|---|
| [`serving.md`](serving.md) | From a push to what an agent gets: the default branch, which commit an agent is served (the last indexed one while a newer is indexed) and how to see it, how long serving takes and why nothing is pushed while an agent loads, what each way of receiving a skill brings, and how the two checks are read (a skill's size, a page that breaks a block, references to other packs, the README tables). | Before a push, and before a fresh agent loads what was pushed; included with the verification skill, linked from the push of the authoring and the document-pack skills. |
| [`fresh-agents.md`](fresh-agents.md) | Starting an agent with none of the session's context: what still reaches it, a subagent with a directory of its own, a second session the user starts, how its stops come back and how an answer resumes it. | Before a dry read or a fresh run; included with the verification skill, linked from the dry read of the authoring skill and from the skills of other areas that start agents. |
| [`transcripts.md`](transcripts.md) | Where a host keeps a session's transcript, a subagent's and the memory notes, their shape, and how to read them as data. | Before reading an earlier session or a fresh run's record. |
| [`searching.md`](searching.md) | How to ask a search over a pack so that it answers: words and meaning with the ranking line, path scoping, the page a pack says to read first, the pack's language and its stems, what to change when a search finds nothing, and how a found section is read and cited. | Before the first search of a pack; included with `skillcdn-document-research` and `skillcdn-document-answer`. |

## Who reads this

The five SkillCDN skills of this area. [`skillcdn-skill-verification`](../../skills/skillcdn-skill-verification/SKILL.md) declares `serving.md` and `fresh-agents.md` in its `skillcdn.include` by their root-relative paths, since every run of it reads both from its first phases on, and they arrive with it wherever SkillCDN serves it. [`skillcdn-skill-authoring`](../../skills/skillcdn-skill-authoring/SKILL.md) links each page from the phase that reads it (`fresh-agents.md` before its dry read, `serving.md` before its push) and reads it there, in the checkout it works in; [`skillcdn-document-pack`](../../skills/skillcdn-document-pack/SKILL.md) links `serving.md` from its push. [`skillcdn-document-research`](../../skills/skillcdn-document-research/SKILL.md) and [`skillcdn-document-answer`](../../skills/skillcdn-document-answer/SKILL.md) include `searching.md`, which every search they make follows. `transcripts.md` is linked from the phases that read a record. A linked page is read with `read_repo_file` through the repository or the engineering connection, or as a file in a checkout or under `docs/skillcdn/` of the engineering plugin; each skill's Requirements say in one sentence where a route that lacks it reads it. What a skill cannot work without (its workflow, its checkpoints, its verdicts, its hard rules) stays in the skill. An included page is part of every skill that includes it: a change to it changes what each of them is served as, and its digest with it, as a change to a manifest does, so edit it deliberately and keep it short.

The pages do not restate how the service works: where a sentence rests on SkillCDN's specification it names the page by its skill URI (`skill://gh/skillcdn/skillcdn/docs/specs/...`), a file of the pack `skillcdn/skillcdn`, and an agent that loads a skill is told which such files it links and how each is read. `npx @skillcdn/cli@latest check --references` asks whether each is still there.

## What every SkillCDN skill does the same way

- **The checkout is where it writes; the connection is what an agent gets.** Nothing local reaches an agent before it is pushed and served.
- **A fresh agent gets only its brief: the request and the facts of its environment.** Nothing of the session that wrote or changed the skill, and no hint; what its host hands every agent (a memory index, a working agreement) is named in the brief as not to be used. A fresh run loads the skill through the connection, never the checkout's files; a dry read of a change that is not pushed yet reads the checkout, which alone holds it.
- **Its stops are answered as the user would, in one short line**, with the answers the user approved; a stop nobody foresaw goes to the user.
- **Every push is confirmed, one at a time**, because a push to the default branch is a public release. **A fresh run is a spend**, a model's time and the tested skill's own costs, estimated and confirmed first; a dry read, minutes of a model and nothing else, starts without a stop.
- **Nothing of a run is committed.** Its subject, its people, its lines, its references, local paths and its outputs stay out; the behavior goes in.
- **A finding changes the sentence it bears on.** A one-time slip goes to the maintainer list, not into a skill.
- **One rerun at most without being asked**, and a rerun that spends is confirmed like any spend.

Each skill that does these things states them in its hard rules, in the form its workflow gives them, so that they hold where these pages do not travel; a skill that only reads a pack has none of them to state.

## How these pages are written

Each page is organized by topic and says what holds now. A fact that can go stale (a path a host uses, a host's tool name, a limit, an endpoint, a timing) names its source and the month it was checked at the end of the sentence; a fact about how the service works carries no date, and changes when a run finds it wrong. There is no chronological log and no run narrative.

## Adding what a run taught

A host or the service that behaved differently from a sentence here: that sentence changes, with the source and the month. Something one skill's method learned: that skill's own reference. Examples name no one and no project: placeholders for paths, sessions, addresses and requests. An agent that meets such a difference while running one of these skills without the repository at hand reports it in its delivery, for whoever maintains the skill.
