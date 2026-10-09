# SkillCDN skills

How the skills that work on a repository in the SkillCDN Format (`skillcdn-…`) are written and kept in step, for authors. What they share at run time is the document set [`engineering/docs/skillcdn/`](../../engineering/docs/skillcdn/README.md), which agents read; this page says what goes there, what stays in a skill, and how the family is tested.

## The tool is the repository and its service

The skills drive a checkout (git, Node.js and the repository's own check), the SkillCDN connection to the same repository, and a way to start an agent with none of the session's context. They name the connection's tools by their exact names (`browse_repo`, `search_repo`, `load_skill`, `read_repo_file`) and the rest as capabilities (a shell, a subagent tool, a second session the user starts), because every host names its subagent and shell tools differently and changes them; a host's tool name appears only as a dated example.

## What is shared and what stays in the skill

| In `engineering/docs/skillcdn/` | In the skill |
|---|---|
| `serving.md`: the default branch, the served commit and how to see it, how long serving takes, what each way of receiving a skill brings, the two checks | When the skill pushes, what it confirms first, what it checks before a commit |
| `fresh-agents.md`: what fresh means and what still reaches an agent, a subagent, a second session, its stops | The brief's request, what the agent is asked to report, how its stops are answered |
| `transcripts.md`: where a host keeps a session's record and memory, their shape, reading them as data | What is taken from them: the evidence sheet, the run record |

The method both skills use to test a skill (the dry-read brief, reading a run, where a finding goes, the rounds) is written in each: the authoring skill's `references/testing.md`, and the verification skill's `references/dry-read.md` and `references/fresh-run.md`. It is the skills' workflow, which stays inside each so that a skill mounted alone or copied still has it; a change to it in one skill is made in the other in the same round.

The set sits in the area's `docs/` because both skills are engineering skills: it travels with the engineering mount and plugin; a skill mounted alone cannot read its linked page, and a copy lacks all of them, which each skill's Requirements say. The test for a sentence: would it be true in the next skill that works on a repository in this format? Then it belongs in the set. A page of the set is reached by a root-relative path. `serving.md` and `fresh-agents.md`, which every run of both skills reads, are in each skill's `skillcdn.include` and arrive with it wherever SkillCDN serves it; `transcripts.md` is linked from the phases that read it and costs one `read_repo_file` when they come. A change to an included page changes the served digest of both skills, as a change to a manifest does: edit it deliberately.

## Facts are dated

A host's paths, tool names and limits, and the service's endpoints and timings, change without notice. A sentence that states one names its source and the month it was checked; a sentence about how the service works carries no date. When a run finds one wrong, the sentence changes ([skill-authoring.md](../skill-authoring.md) "Knowledge pages").

## Examples name no one

Paths, sessions, addresses and requests in the set and the skills are placeholders (`<slug>`, `<session id>`, `<address>`, `<path>`), apart from this repository's own address and paths. No run's subject, person or customer, and no path of anyone's machine.

## Testing

The authoring skill is exercised by making a skill from a job and having its fresh agent run it; the verification skill by verifying a skill that is already served, with a request that costs nothing to run where one exists, to the end. A change to either skill is dry-read before it is pushed. A run is read against the files as the verification skill's `references/fresh-run.md` says; what a host or the service did differently goes into the sentence of the set it bears on.
