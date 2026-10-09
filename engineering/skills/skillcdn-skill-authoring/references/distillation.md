# From the sheet to the design

How the evidence becomes a skill a fresh agent can run alone: what to ask, what to derive, where to stop, what to accept, what to forbid, what to include, and what to leave out. The conventions of the layout (the skeleton, the style, the knowledge pages, the steps for an area or a family) are the checkout's `guide/`; this page is the method.

## The description

Search ranks the description first, and search and browse results show its first 200 characters. Write it as the user would say the job, then what comes out, then "Use when ..." with the phrases the user actually used, formal and casual. Name the tool, but open with the job: "Makes a vertical ad from a reference video and a product link" before "on Higgsfield". Say when another skill of the repository is the better choice, so that two skills with a shared word do not compete. Before the draft is shown, write five sentences a user would say that must reach this skill and three that sound alike and must not, and read the description against each.

## Asked or derived

A skill asks for what the run could not have known, in one message, and derives the rest. For each input the run used, decide:

| The run | The skill |
|---|---|
| The user gave it unasked in the request | An input; asked only when missing |
| The agent asked, and the answer could have been read from the request, the product, the reference or a sensible default | Derived, with the rule; stated at the first checkpoint, changed on request |
| The agent asked, and nothing at hand could have answered | Asked, as the written question |
| The user volunteered a preference the agent had not asked for | Derived, with that preference as the default |

Write the intake question as it will be asked. Ask once; an answer stands for the run.

## Phases

A phase consumes an artifact and produces a named one, in the order the run met them. Fold a step the user never saw into the phase it served; split a phase at a checkpoint. Name every artifact the next phase reads, because the name is the handle the checkpoint uses. The phase that reads a reference links it. Two phases the run did in parallel are written in order, with a note that the second may start first.

## Where the user is consulted

| Condition | Choice | Why |
|---|---|---|
| The step costs money or credits | Stop, with the estimate against the balance and the cheapest setting | The repository's rule; consent never lapses, even on a go-ahead |
| The step is irreversible or public: a push, a publish, a send, a delete, a payment | Stop, one step at a time | Cannot be taken back |
| The step is a matter of taste: a story, a portrait, a design, a plan | Stop, with a recommendation and one alternative | The user's call; the skill still recommends |
| The step derives a setting | Report at the next stop | Changeable on request; no stop needed |
| Anything else | Report in a line and go on | A stop that teaches nothing costs the user a turn |

A go-ahead ends the stops of taste and of reporting, never the stops of spend or of irreversible acts. "Takes are reported, not approved one by one" is the pattern: the unit the user judges is the plan and the result, not every intermediate.

## Verdicts

From every draft the run set aside and every retry: the condition that made it fail, the condition that would have passed it, and how many tries the run allowed. Write them as a table (accept, accept with a change, redo) that the agent reads before the costly step, with the retry budget and who pays for a second retry. Name what is close enough: a verdict that redoes everything imperfect spends without end, and one that accepts everything teaches nothing.

## Hard rules

A rule is read before every costly step, so there are few and each is short.

| Source | A rule? |
|---|---|
| A correction the user made twice, or once with emphasis | Yes, in the form the correction gave it |
| A rule the user stated as a rule | Yes |
| A spend or a safety fact: what is preflighted, what is confirmed before the push | Yes, as the specific form a repository rule takes in this skill |
| A `feedback` note in memory about the job | Yes, as above |
| A single slip of one run | No; it goes in the report |
| A preference about language or tone | No; the repository's manifest says to speak the user's language |
| A value, a limit, a model | No; a discovery instruction in the phase |
| What the repository's or the area's manifest already says | No; it arrives with the skill |

Say why where the why is not obvious: a fresh agent keeps a rule it understands and works around one it does not. Capitals and "never" carry no more weight than the reason next to them.

## Discovery in place of values

| The run used | The skill says |
|---|---|
| A model id | The catalog call, what the model must do, and how to choose when several qualify: the latest of a family, the lowest tier |
| A price | The cost call, once per distinct parameter set; a dated number only to show the shape, marked illustrative |
| A limit read from a tool's description | Where to read it, with the number and the month as a staleness mark |
| A parameter name | The name in backticks the first time, and where its parameters are listed |
| A route, a label, a selector on a website | The way to find it again, with the day it was checked; a website has no changelog |
| A capability every host offers under another name: a shell, a browser it drives | The capability and how to recognize it, never one product's tool name |

## Placement in this layout

Everything the skill cannot work without lives in its directory, because it may be mounted alone, installed as its area's plugin, or copied bare.

| What | Where | Why |
|---|---|---|
| The workflow, the checkpoints, the verdicts, the hard rules, the terms | `SKILL.md` | Read on every run |
| Anything longer than a paragraph that one phase reads | `references/<topic>.md`, linked from that phase | Read when the phase comes; no page of the load |
| A reference every run reads | Also in `skillcdn.include` | Arrives with the skill instead of costing a read per run |
| How the tool behaved in this skill's own phases | `references/tool-notes.md`, by topic, dated where a fact can go stale | Found where an agent looks for it, not where it was learned |
| What would be true word for word in the next skill of the family | The family's document set (`docs/<family>/` at the root, or the area's `docs/` when one area holds every skill of the family), once a second skill exists or is planned; the page every run needs included by its root-relative path, the rest linked | Written once, kept current in one place |
| A handover from another skill: which result it takes, how it chooses | This skill, in a sentence that names the other | The skill that is used stays general |
| An example of a data file the skill reads or writes | `assets/<name>.example.json`, placeholder values | Small JSON is indexed and read; outputs are not committed |
| A helper an agent may run locally | `scripts/<name>.example.<ext>`, optional | Served as text, never run by the service; the skill works without it |

Budget: the body and the includes together around 16 KiB before the inherited rules, which come first on every page. The repository's rules and the area's arrive with the skill; restating them costs a page and drifts.

## Folding a run in

A finding changes the sentence it bears on; nothing is appended as a log. A step the fresh agent guessed: the phase gains the sentence it lacked. A tool that behaved differently: the sentence in `tool-notes.md` or the family page changes, with the source and month where the fact can go stale. A word the agent did not understand: the term joins the terminology. A correction the user made for the second time: a rule. The run's product, persona, lines and references stay out; the behavior goes in.

## Before the draft is shown

Read the draft as a fresh agent, and fix:

- A value where a discovery instruction should be, or a dated fact without its source and month.
- Instance material: a product, a person, a line, a reference, a customer, a number that was paid.
- A sentence that restates the repository's or the area's manifest.
- A tool name that is one product's and will not carry over to another host, where a capability was meant.
- A link that leaves the skill's directory for anything but a shared page of the repository's or the area's document sets, or a link to a page that does not exist.
- A step a fresh agent must guess: an artifact used before it is named, a choice without its rule, a question without its wording.
- A checkpoint that stops for nothing, or a spend without one.
- A rule without its why, or in capitals.
- The description's first 200 characters without the job, or "Use when" missing anywhere in it.
- The size of the body and the includes against the target; what one phase needs, linked instead.

## What not to do

- Fit the skill to the run: a rule that makes sense only for this product, a phase order that only this reference required.
- Shout: "always", "never" and "must" in capitals in place of the reason.
- Narrate: "in the second run", "the first time"; a knowledge page says what holds now.
- Assume the authoring session's knowledge: a fresh agent did not see the run.
- Open the description with the tool, or leave "Use when" out.
- Add a language rule, a tone rule, or a rule for one slip.
