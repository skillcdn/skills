# Dry read: the files, read as a fresh agent would

A fresh agent reads the skill under test as if about to run it, runs nothing and changes nothing, and reports every place where it would have to guess, ask or look something up. This page holds what it reads, its brief, the brief for a change, how its report is checked, and the shape of the findings. It costs nothing and finds most of what a fresh run would.

## What it reads

What an agent will be served: the skill's `SKILL.md`, the files its `skillcdn.include` lists, the references, assets and scripts in its directory, the bodies of the manifests above it, and every shared page its phases link. Read them at the served commit: give the agent their paths in the checkout when the checkout matches the served commit for every one of them ([serving.md](/engineering/docs/skillcdn/serving.md) "Which commit an agent gets"), and otherwise tell it to read each through the connection with `read_repo_file`. For a change, the files as they are in the checkout. Note which pages arrive with the load and which are only linked: a sentence in a linked page reaches only an agent that follows the link, and a contradiction between the two kinds is a finding of its own. The brief names the environment from the skill's Requirements, each tool present or missing on the machine the run will use, so that a finding about a missing tool is the environment's and not the brief's omission: a brief that left a present tool out once drew a high finding about its absence.

## The brief

Start the fresh agent as [fresh-agents.md](/engineering/docs/skillcdn/fresh-agents.md) says for the host, with this brief, filled in:

> You are about to run the skill at `<path>` in a fresh session, with only this request from the user: "<the request for the run>". Your environment: <each tool or capability the skill's Requirements name, present or missing>. Read only these files and nothing else: <the files above, as paths, or how to read them through the connection>. Use nothing you remember, from memory or from an earlier context, and nothing from a working agreement such as `CLAUDE.md`; run nothing, call no tool except to read those files, change nothing. Walk the skill phase by phase as you would run it for that request. Report, as a numbered list, most important first, every place where you would have to guess, ask the user, or look something up to go on: an artifact used before it is named, a choice without its rule, a question without its wording, a value you would need and no way to find it, a term you do not know, a step whose result you cannot tell, an order you cannot follow, a contradiction between two sentences, a rule you could not keep, an instruction you could not carry out in this environment, a part you would be tempted to skip. Quote the sentence each finding is about and name the file. Say which findings you could resolve from the files on a second read and which you could not. End with the first 200 characters of the skill's description and whether this request would make you pick the skill.

## The brief for a change

For a change to the skill or to a page it reads, the brief also gives the old text (`git show <commit before the change>:<path>` for each file) and asks, under these headings: lost facts, every fact an agent needs in the old text that the new text no longer holds, quoting the old sentence; contradictions between the skill and a shared page; dangling references, a link, a section name or a "the shared page" that points to nothing; self-containment, anything an agent must do to run safely that now lives only in a shared page; public hygiene, a run's subject, people, lines or references, a secret or a private hostname; and whether the catalogs and the guide agree with what is on disk. Each finding with its file and line and a one-line fix, "none found" under a heading with nothing, and the three that matter most at the end.

## Checking the report

- Look up every quoted sentence in its file before using it, and record its line. A quote that does not match word for word is set aside: a fix aimed at a misquote changes the wrong sentence.
- A finding the files answer on a second read is marked resolved, not fixed, unless the run stumbles on it too.
- A finding about the format or a manifest's rule is for the user, not for the skill.

## The findings

Numbered, ordered by the phase where a run meets them, each tagged:

| Tag | When |
|---|---|
| high | It costs money or credits, breaks a rule, or touches every run |
| medium | It changes what the result looks like, or how consistent it is |
| low | Wording, a rare case, a term |

Each finding: the quoted sentence with its file and line, what an agent would have to guess or ask, and whether it sits in a page that arrives with the load or one that is only linked. The report ends with the few to fix first. Quotes stay in the language of the files. When the user asked for the dry read alone, this report is the delivery.
