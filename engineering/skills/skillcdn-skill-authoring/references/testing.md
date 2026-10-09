# Testing: the dry read, the fresh run, the fold back

A skill is proven only when an agent with none of the authoring session's context follows the files alone to the result. Two tests, in this order: a dry read, which costs nothing and finds what a reader must guess, and a fresh run of the pushed skill through the service, answered as the user would. Then the findings go back into the files, once, in the sentence they bear on.

## Dry read

A fresh agent that reads and does nothing else. Start it as [fresh-agents.md](/engineering/docs/skillcdn/fresh-agents.md) says for the host: where the host has a subagent tool, a subagent with a capable model and this brief; otherwise the user opens a session with it. A subagent may arrive with the host's memory index or the checkout's agreement in its context; the brief tells it to use neither.

> You are about to run the skill at `<path>` in a fresh session, with only this request from the user: "<request>". Read only these files and nothing else: the files of that skill directory, the bodies of the manifests above it, and the shared pages its SKILL.md includes or links. Use nothing you remember, from memory or from an earlier context, and nothing from a working agreement such as `CLAUDE.md`; run nothing, call no tool except to read those files, change nothing. Walk the skill phase by phase as you would run it for that request. Report, as a numbered list, most important first, every place where you would have to guess, ask the user, or look something up to go on: an artifact used before it is named, a choice without its rule, a question without its wording, a value you would need and no way to find it, a term you do not know, a step whose result you cannot tell, an order you cannot follow, a contradiction between two sentences, a rule you could not keep, an instruction you could not carry out in this environment, a part you would be tempted to skip. Quote the sentence each finding is about and name the file. Say which findings you could resolve from the files on a second read and which you could not. End with the first 200 characters of the skill's description and whether this request would make you pick the skill.

Fix each finding in the files: the phase gains the sentence it lacked, the term joins the terminology, the rule gets its why. A finding about the format or about a manifest's rule is reported to the user and left in place. A dry read of a changed skill before its push catches most of what a fresh run would, at no cost.

## The fresh run

### Push first

The service serves the default branch, so the skill is pushed before the run: commit the skill's files and the catalog rows, `git pull --rebase`, push. Then wait until the commit is served, as [serving.md](/engineering/docs/skillcdn/serving.md) says: `browse_repo`'s `Source` line names the served commit, and that page says how long serving takes and what a status that stays not ready means. Do not push again while a fresh agent is loading the skill: its continuation cursors stop matching.

### The runner

The run gets only the request and a few facts about its environment, nothing of the authoring session. Start it as [fresh-agents.md](/engineering/docs/skillcdn/fresh-agents.md) says for the host: what can still reach a subagent, a directory of its own, a second session, a runner script.

- A subagent with a directory of its own, a copy of the checkout that the brief tells it not to read skills from; or a separate session the user starts in another directory, with the same brief. The strongest model the host offers for real work, at a high effort setting, never a pinned name. Its brief: the user's request in the user's words, on the stand-in subject the test plan names, verbatim and last; that the skills come from the SkillCDN connection at the repository root, `load_skill` followed through every `nextCursor` before the skill is used, never from local files; the folder outside the repository where outputs go; that it uses nothing it remembers, and no memory index or working agreement its host handed it; that it stops and ends its turn at every checkpoint with the checkpoint message as its report, never answers a checkpoint itself, never spends what was not accepted, and never pushes. Each stop comes back as its report, and the user's one-line answer sent to the same agent resumes it with its context intact.
- The first run of a new skill goes to the end: the skill is done only when a fresh agent reached the result. A rerun, when the point is the plan and not the product, stops at the cost checkpoint, left unanswered, so that nothing is spent.

Answer each checkpoint in one short line, with the answer the user approved in the test plan, and no more: a hint the user would not give masks a gap in the skill. A stop the plan did not foresee, and an estimate above the one the user approved, go to the user before the run goes on. An agent that does not pick the skill for the request gets one line of direction, as the user would give it ("use the <name> skill"), and that miss is a finding about the description.

### Reading the run

The run's record (the subagent's reports, and its transcript where [transcripts.md](/engineering/docs/skillcdn/transcripts.md) locates it) against the skill, phase by phase:

| Where the run | It means |
|---|---|
| Asked something the skill derives | The derivation rule is missing or buried |
| Improvised a step | The phase lacks the sentence |
| Ignored a sentence | Unclear, or in the wrong place; move it to the phase that needs it |
| Met what the tool notes or the family's pages do not say, or the opposite of what they say | A tool note or the family page changes, with the source and the month |
| Spent more than the estimate's shape allows | The estimate's shape, the reserve, or the stop before exceeding it |
| Delivered less than the verdicts ask | A verdict is missing, or the delivery's list is incomplete |
| Did not pick the skill, or strayed from it | The description, or the phase it left |
| Answered in another language, or slipped once | The maintainer list, not the skill |

### Where a finding goes

| Finding | Goes to |
|---|---|
| What had to be said in chat | The skill: the phase, the question or the rule it lacked |
| How the tool behaved in this skill's own phase | `references/tool-notes.md`, the sentence it bears on |
| How the tool behaved for every skill of the family | The family's page, the sentence it bears on, dated where it can go stale |
| A sound, a word, a pattern of the tool with a language | The family's page for it, as behavior, never the run's words |
| A one-time slip | The maintainer list in the delivery |
| The format, or a manifest's rule | The user, for a change of the rule; never a patch in the skill |

## Rounds

One rerun after the fold-in at most without being asked, with the same request, and only when a change would alter the run; to the cost checkpoint when the plan is what changed. Then say plainly what the last change was not exercised on, and offer another round. A run of a paid tool is estimated and confirmed before it starts, every time.

## An existing skill

The same, from the run the user brings: its record, or the maintainer list in its delivery, is the sheet. The change goes to the sentence it bears on, and the version is raised when the change alters a run; a rerun only then.
