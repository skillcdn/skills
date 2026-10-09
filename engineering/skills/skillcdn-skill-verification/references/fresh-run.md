# Fresh run: the plan, the run, reading it, and where a finding goes

How the run of the skill under test is planned, started, answered and read, and where each finding goes in the files. How to start an agent on each host is in [fresh-agents.md](/engineering/docs/skillcdn/fresh-agents.md); where its record is kept, in [transcripts.md](/engineering/docs/skillcdn/transcripts.md); this page is the method.

## The plan

| Item | Derived from |
|---|---|
| Request for the run | The user's own words when they gave some. Otherwise what a user would say to the skill under test, from its description and its Inputs, written the way the user writes. Its subject is the user's own test subject where the user named one in this session, or pointed to a note that names one; a memory index the host handed over does not count as pointing. Else a plausible subject the skill can work on, real where the skill reads real data (a product category, a keyword, a market), invented where it makes something new. Never a customer's, and never the subject this session already worked on, so that the run cannot lean on what this session learned. |
| Answers | One short line per stop the skill names, as the user would write it, accepting the recommendation: "OK", "Good, go on", "Go with the recommendation". A go-ahead goes into the request only when that path is what must be tested. |
| How far | To the end when the skill is new, has no fresh run to the end in its coverage notes, or changed in a late phase. To its cost checkpoint, left unanswered, when only its plan changed or the user wants no spend. When the skill has an early stop where the quality shows (a story, a shortlist), a run to that stop first is a cheaper look before a costly production; offer it. |
| Runner | A subagent with a directory of its own, on the strongest model the host offers for real work at a high effort setting. A second session the user starts in another directory where there is no subagent tool, or where the memory the host hands every subagent holds notes on the skill under test; offer that choice in the plan. |
| Outputs | The folder the user named, or the one a note the user pointed to names for runs; else a scratch folder of the host's, outside the repository, named after the skill under test. |
| Time and spend | How long a run takes, from the skill's own notes where they give one (its tool notes, its coverage notes), else from its phases and the waits it names, said as a range and marked as an estimate. Its own spend from its cost checkpoint, which the run reaches before anything is spent, within any cap the user set. |
| Rerun | Whether one rerun follows the fold-in when the fold-in alters the run, to the end or to the cost checkpoint, with its time and spend. |
| What it verifies | The phases the run will reach, the stops it will answer, the route it will take; and what it will not: the phases past where it stops, the routes for other hosts, the paths only another request takes. |

Two more checks cost little; offer them in the plan when they fit. When the skill offers routes for hosts with different capabilities (a shell, or a browser it drives), a second run in a deliberately limited environment tests the other route. When a fold-in changes a verdict table, a fresh agent given only the changed rules and the run's case, without its outcome, shows whether the rules alone lead to the right verdict.

## The run

- The brief: the facts of the environment, then the request for the run, verbatim and last. The facts: the skills come from the SkillCDN connection, its tools by name, `load_skill` followed through every `nextCursor` before the skill is used, never the local files of a checkout or a worktree; which tool servers are connected; the outputs folder; that it uses nothing it remembers, and no memory index or working agreement its host handed it; and that at every checkpoint the skill names it ends its turn with the checkpoint message as its report, never answers a checkpoint itself, never spends what was not accepted, and never pushes.
- Each stop comes back as the agent's report. Answer with the planned line and nothing more: a hint the user would not give hides the gap the run exists to find.
- A stop the plan did not foresee (a refusal that changes the plan, a question the skill should have derived), and an estimate above the approved one, go to the user with what the agent said; answer only with the user's word.
- An agent that does not load the skill, loads another, or leaves a phase gets one line of direction, as the user would give it ("Use the <name> skill", "Show me the estimate first"); record the miss.
- Push nothing while the agent is loading the skill: its continuation cursors stop matching once another commit is served.
- Keep a running record: each stop and its answer, the spend against the plan, the time, where the outputs are, the transcript's path.

## Reading the run

Read the run record against the skill, phase by phase, and mark for each dry-read finding whether the run met it.

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

A dry-read finding the run also met is confirmed and fixed first. One the run did not meet is still fixed when it is real, and reconsidered when the run passed the same point without trouble. What the user finds by reviewing the result themselves (a line that sounds wrong, a hook that does not land) is weighed the same way: fix how the skill prevents it and how its checks catch it, not only the one case, and leave alone the near misses a listener would not notice.

## Where a finding goes

| Finding | Goes to |
|---|---|
| What had to be said in chat | The skill: the phase, the question or the rule it lacked |
| How the tool behaved in this skill's own phase | The skill's `references/tool-notes.md`, the sentence it bears on |
| How the tool behaved for every skill of its family | The family's page, the sentence it bears on, dated where it can go stale |
| A sound, a word, a pattern of the tool with a language | The family's page for it, as behavior, never the run's words |
| A one-time slip | The maintainer list in the delivery |
| The format, or a manifest's rule | The user, for a change of the rule; never a patch in the skill |

Write each change as the checkout's guide says for a skill or a knowledge page: the sentence it bears on changes, nothing is appended as a log, and nothing says which run taught it.

## Rounds

One rerun after the fold-in at most, as the plan approved it, with the same request, and only when a change would alter the run; to the cost checkpoint, left unanswered, when the plan is what changed. Then say plainly what the last change was not exercised on, and offer another round. A run of a paid tool is estimated and confirmed before it starts, every time.
