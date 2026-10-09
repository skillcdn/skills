# SkillCDN: what its skills share

The skills that work on a repository in the SkillCDN Format (`skillcdn-…`) share how the service turns a push into what an agent is served, how an agent with none of the session's context is started on each host, and where a session's record and memory are kept. That lives here once, one file per topic, kept current in one place; each skill includes or links the page from the phase that reads it and carries its own method (what it asks, where it stops, what it accepts, its rules) itself.

| Document | Holds | Read |
|---|---|---|
| [`serving.md`](serving.md) | From a push to what an agent gets: the default branch, which commit an agent is served and how to see it, how long serving takes and why nothing is pushed while an agent loads, what each way of receiving a skill brings, the two checks. | Before a push, and before a fresh agent loads what was pushed; included with each skill. |
| [`fresh-agents.md`](fresh-agents.md) | Starting an agent with none of the session's context: what still reaches it, a subagent with a directory of its own, a second session the user starts, how its stops come back and how an answer resumes it. | Before a dry read or a fresh run; included with each skill. |
| [`transcripts.md`](transcripts.md) | Where a host keeps a session's transcript, a subagent's and the memory notes, their shape, and how to read them as data. | Before reading an earlier session or a fresh run's record. |

## Who reads this

[`skillcdn-skill-authoring`](../../skills/skillcdn-skill-authoring/SKILL.md) and [`skillcdn-skill-verification`](../../skills/skillcdn-skill-verification/SKILL.md), both in this area. Each declares `serving.md` and `fresh-agents.md`, which every run reads, in its `skillcdn.include` by their root-relative paths, so that they arrive with the skill wherever SkillCDN serves it, and reads `transcripts.md` with `read_repo_file` at `engineering/docs/skillcdn/transcripts.md` through the repository or the engineering connection, or as a file at `docs/skillcdn/` of the engineering plugin, two levels above its own folder. A skill mounted alone cannot read the linked page there, and a copy taken into another agent has none of the pages: its Requirements say so and name this directory in the repository, which is where to fetch them. What a skill cannot work without (its workflow, its checkpoints, its verdicts, its hard rules) stays in the skill. A change to an included page changes the served digest of both skills, as a change to a manifest does: edit it deliberately.

## What every SkillCDN skill does the same way

- **The checkout is where it writes; the connection is what an agent gets.** Nothing local reaches an agent before it is pushed and served.
- **A fresh agent gets only its brief: the request and the facts of its environment.** Nothing of the session that wrote or changed the skill, and no hint; what its host hands every agent (a memory index, a working agreement) is named in the brief as not to be used. A fresh run loads the skill through the connection, never the checkout's files; a dry read of a change that is not pushed yet reads the checkout, which alone holds it.
- **Its stops are answered as the user would, in one short line**, with the answers the user approved; a stop nobody foresaw goes to the user.
- **Every push is confirmed, one at a time**, because a push to the default branch is a public release. **A fresh run is a spend**, a model's time and the tested skill's own costs, estimated and confirmed first; a dry read, minutes of a model and nothing else, starts without a stop.
- **Nothing of a run is committed.** Its subject, its people, its lines, its references, local paths and its outputs stay out; the behavior goes in.
- **A finding changes the sentence it bears on.** A one-time slip goes to the maintainer list, not into a skill.
- **One rerun at most without being asked**, and a rerun that spends is confirmed like any spend.

Each skill states these in its hard rules, in the form its workflow gives them, so that they hold where these pages do not travel.

## How these pages are written

Each page is organized by topic and says what holds now. A fact that can go stale (a path a host uses, a host's tool name, a limit, an endpoint, a timing) names its source and the month it was checked at the end of the sentence; a fact about how the service works carries no date, and changes when a run finds it wrong. There is no chronological log and no run narrative.

## Adding what a run taught

A host or the service that behaved differently from a sentence here: that sentence changes, with the source and the month. Something one skill's method learned: that skill's own reference. Examples name no one and no project: placeholders for paths, sessions, addresses and requests. An agent running a skill without the repository at hand reports the finding in its delivery, for whoever maintains the skill.
