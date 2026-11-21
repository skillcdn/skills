# Tool notes: what batches met

What batches of five and ten posts met, by topic, with the month where a fact about a host or a model can go stale. How an agent is started, answered and resumed on each host is in [fresh-agents.md](/engineering/docs/skillcdn/fresh-agents.md); this page holds what a batch adds.

## Side by side

- Claude Code's `Agent` tool starts the calls sent in one message side by side, takes a `model` and an `effort` per call, and returns each agent's last message alone (checked 2026-11).
- A batch departs from fresh-agents.md in two things, which that page says for a verification run. A worker and a reviewer are started in this checkout, with no isolated copy of the repository, since a worker writes the account's own folders and its scratch folder is the directory of its own; and they run at the tiers the skill names, not on the strongest model the host offers.
- Ten workers ran at once on one desktop with no failed render, each with its own preview server and its own browser; five had run clean in every batch before (checked 2026-11). More than ten at once is untried.
- The build's preview server takes one fixed port unless it is given another as its argument, so workers side by side each get a port, and the export and the review are given that address.
- Two workers that shared one scratch folder overwrote each other's temporary script of the same name.

## One after another

The alternative on a host with no tool that starts agents side by side, offered at the first message and said again at the delivery. The posts are made one after another in this session: each by the research on its topic as a story handed over, then the build, with the plan's answers given and both skills' stops skipped as a go-ahead skips them, and phase 4 held against each before the next begins. It takes the time of one post times the batch. Its review is the build's own, by the agent that made the post, so nothing is read by an agent that made none of it, unless the person opens a second session per post and pastes the reviewer's brief there. The plan, the estimate (this session's own tokens, a post at a time), the ledger and the delivery are as written.

## What a batch costs

Illustrative, as one host counted them for a worker one tier below its top model at a high effort setting (checked 2026-11); the first return of the batch at hand replaces them in the running record, and where the host shows no count the record says so and counts agents.

| Agent | Tokens | Minutes |
|---|---|---|
| A worker, research and build of a post of five to seven slides | 290,000 to 380,000 | 16 to 22 |
| The same worker's fix round | to 460,000 in all | 3 to 7 |
| A reviewer, each pass | 100,000 to 150,000 | 1 to 3 |
| The research alone at the top tier, for a delicate topic | 220,000 to 360,000 | 20 to 45 |
| A worker that only builds, from a brief already written | Less than the first row; no count of its own yet | |

A batch of ten with two review passes took about two hours from the first worker to the gathered posts.

## What the roles did

- Workers one tier below the session's model wrote the briefs themselves with no factual error left after review, and corrected the topic line's premise in about half the posts; having the briefs written first at the session's tier doubled the time of the batch and cost about half as much again per post.
- Workers at a high and at the next higher effort setting drew as many fixes from their reviewers; what was left to fix after the lower was attributions and stray page furniture, after the higher the exactness of a quote, a reference date, a private detail inside a picture.
- A reviewer's first pass returned `fix` on eight to ten posts of ten, and its second passed nearly all: the estimate counts two passes.
- Most first-pass fixes were the slide count, a cover that said more than its sources, and a picture of something else read as the event's. With the ceiling as the first line of the block the count fixes fell by half and did not end, which is why the orchestrator rules on the count.
- A reviewer that read the phone-size slides before any text named the slide where it halted at once; reviewers that began with the brief passed posts the person then could not follow.

## Resuming and what comes back

- A message to the worker's id resumes it with its context (Claude Code's `SendMessage`, checked 2026-11): a fix took the worker that made the post minutes, where a new agent would start from nothing. The ids are in the batch record for that.
- Only an agent's last message comes back, or what it hands back through the host's hand-back tool where its session has one, which is why both briefs end in a fixed block and name both ways (checked 2026-11).
- Claude Code refuses a subagent's write of a Markdown report file (fresh-agents.md); the post's own Markdown files (`facts.md`, `credits.md`, `review.md`) are not reports, and the worker's brief says they are written. A worker that still cannot write one names it under `left`, and this session writes it from the return.
- A subagent is also handed what its host gives every subagent, the checkout's working agreement among it (fresh-agents.md "What fresh means"). In an account's repository that is wanted: the worker reads the same rules the team does.

## The repository while agents write

- A pull that stashes the working tree takes the workers' folders into the stash and back while they write. Fetch, pull, commit and push wait for the last return.
- A ledger rewritten by a script is read back as a diff before it is kept: a pattern that lost an escape rewrote the table's heading in place of ten rows, and no check noticed. Find a row by its slug at the start of the line and change only its state cell.
