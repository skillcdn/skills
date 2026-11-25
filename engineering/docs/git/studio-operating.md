# Operating a studio: people, agent accounts and sessions

A studio is worked by several people and agents at once, some of them with nobody at the terminal. This page says who works in it and where, which change goes where, how a batch divides the work between a lead, workers and a reviewer, what a session on a schedule may do, and how an approval is asked and what leaves is sent. Read when a studio is set up, before the agreement's lines are written, and by whoever leads a batch or puts a session on a schedule. The structure is [studio.md](studio.md); what a session reads is [studio-know-how.md](studio-know-how.md).

## Who works in it

- **People and agent accounts** are members of the console project the repository is bound to ([console.md](console.md)). A person works with an agent of their own; an agent account is a member of its own, assigned a task as a colleague is and woken once the task is `ready`, with nobody in its chat. Either works a task of the studio in a checkout of the studio. An agent account clones the repository under its desk and works there by the studio's agreement; its desk names no project, so the board commands of a studio's task are run inside that checkout, which names it.
- **A clone each, one task in it at a time.** Units do not collide, since each has its folder; two sessions in one clone do.
- **Who decides what** is the policy's Approval heading: who gives each person state, who changes a format, who changes the policy itself. A decision is asked of that person on the board, addressed to them; an agent account asks its manager where the policy names nobody. What a person answered elsewhere is written on the decision in their name.

## Which change goes where

- **One unit, one worker.** A unit's folder is changed by its `owner` alone.
- **A unit** (a change inside one unit's folder, with its ledger row) goes straight to the main branch after the check: folders do not collide.
- **What every unit rests on** (formats, scripts, `studio.json`, the studio's skills and its pages) is changed in a commit of its own, through a pull request where the team reviews, and never in the middle of a batch: a worker that wants one changed says so in its return. A commit that changes a format or a script names the units that render differently and were rendered again.
- **The files everyone touches** (the ledgers, the standing files, `AGENTS.md`, the lockfile) are edited small and rebased right before the push. A ledger's row is added by the new command and its state by the file command, so two sessions rarely touch the same line.
- **A session starts** with `console whoami`, a pull (with `git lfs pull` where it will look at previews), the check, whose warnings are dealt with first and whose last lines say where the studio stands, then the task, the start page and the studio skill of its job. It ends with what the run learned folded back (studio-know-how.md "Folding work back"), the file command, the check, the commit and the push. The agreement's Workflow says this in the team's words, and no other page restates it.

## A batch: a lead, workers and a reviewer

Several units made at once are made by roles, and each role's limits are what keep the batch from colliding.

| Role | Does | Never |
|---|---|---|
| Lead | Takes the board task. Chooses what is made, from the task and the policy. Starts every unit with the new command, so that no two workers pick one name or one subject. Starts the workers side by side, gathers their returns, runs the check and the gallery, commits once, reports, asks the approval | Writes a unit's sentences in a worker's place, changes a format or a script during the batch |
| Worker | Makes one unit with its job's studio skill, to the state the lead named | Writes outside its unit's folder, commits, runs a board command, fills a gap: after two failed tries of the check, or where the material is missing, it returns `blocked` |
| Reviewer | An agent that made none of the units. Reads one unit against its inputs, looks at every output at the size it is seen at, returns a verdict and what to fix. The same reviewer sees the fix | Fixes anything itself |

What a reviewer's findings change beyond wording (how many parts a unit has, which picture, whether it is made at all) the lead decides; wording goes back to the worker. A unit is moved to the state before the person's only after a reviewer passed it.

A role's brief is a block of a few lines, never a document: everything else reaches the role through the skill it loads. A brief that summed up the rules was one more place to change with every rule.

```
unit: <folder>/<slug>
skill: skills/<job>/SKILL.md, read as it is served, then the pack skill it names, every part
given: <the subject in a line>; <its sources>
write: this unit's folder and nothing else; no commit, no board command
stop: after two failed tries of the check, or where the material is missing; return blocked and fill nothing
return: slug | state reached, or blocked | check: errors, warnings | what you could not verify | what you would change outside the unit | minutes
```

```
unit: <folder>/<slug>, of which you made nothing
read: its record and its inputs, then every output at the size it is seen at
return: slug | pass, fix or reject | each finding: where, what, why | you fix nothing
```

Which model runs each role, and at which effort, is the studio's own choice: the policy's Roles line says it, with the row of `docs/trials.md` that settled it, and a change of it is tried as any technique is. Where the pack has a skill for the batch of a kind (`html-card-news-batch` for card news), the studio's batch skill extends it and these blocks are that skill's. How a host starts agents side by side, and what an agent started that way does not know, is [fresh-agents.md](/engineering/docs/skillcdn/fresh-agents.md).

## A session on a schedule

A studio that books things for a time needs a session after that time, and one that looks for the day's subject needs one in the morning. An agent account keeps a wake for the hour, or takes it with its day's briefing; a person's machine keeps a scheduled task of their agent's product, made on their word, which runs only while that product is open.

- **It does three things.** It reads the check's warnings. For each unit whose time has passed it looks where the unit stands in the place it left for (the account, the ad account), writes the record, runs the file command and commits to the main branch. It reports on the board. A morning look may also start a unit at its first state and propose it.
- **It decides nothing.** It gives no person state, except for a class the person approved in advance, by the policy's line and with that line named in the record. It changes no format, script, skill or page, and it sends nothing out.
- **Nothing depends on it having run.** Where it did not, the next session's check shows the same warnings and that session does them first. Its checkout is left on the main branch, since that is where it commits.
- **One browser, one session.** Two sessions that drive one signed-in browser stall each other: the hour of a scheduled session is kept free of other work in that browser.

## Approval, and what leaves

- **The ask.** A unit waits one state before the person's. The lead asks once for a batch or once for a unit, on the board, with the previews handed in (a contact sheet a unit) and with whatever the policy says the person is shown before they answer. Whoever sits at a checkout looks on the review screen instead. A batch waits silently on a person the console does not tell, so whoever approves turns the kind `decision` on for themselves ([console.md](console.md) "The people").
- **The answer** is written into the record by whoever received it: `at`, and `by` with who said it, where, and their words.
- **What leaves** (a post booked, an ad launched, an issue sent) is a job of its own, whose studio skill extends the pack's skill for that place. It runs only on units at the person's state and writes the next state with its time. No script of the studio sends anything.
- **After it left**, the unit is filed when it was seen there, never when its time passed.

## Storage

What a unit renders goes to large-file storage, and continuous integration fetches none of it. A studio that renders video grows by tens of megabytes a unit, and reached a gigabyte in three weeks: the plan of a setup says what the git host's page gives for storage and transfer, and `docs/architecture.md` names who watches it.
