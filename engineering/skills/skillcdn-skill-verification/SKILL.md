---
name: skillcdn-skill-verification
description: Verifies a skill in a repository of the SkillCDN Format the way a user's agent will meet it. A fresh agent reads its files for every place it would have to guess, a fresh agent runs the served skill with its checkpoints answered as the user would, and what both find is folded into the sentences it bears on. Reads what is served, or a local change before it is pushed; compares old and new text after a tool, a model or a shared page changed; checks every quote; keeps the run's subject, lines and outputs out of the repository; pushes only with the user's word and reruns at most once unasked. Use when the user says to verify, test, dry-read or try a skill from a fresh session, to check that a skill still works after a change, or to see whether a fix holds. To make a new skill from work already done, use skillcdn-skill-authoring, which verifies its own draft.
license: MIT
compatibility: Needs a checkout of the repository the skill lives in, with git and Node.js, the SkillCDN connection to that repository, and a way to start a fresh agent (a subagent tool, or a second session the user starts). The run of the skill under test needs that skill's own tools. Works in any agent that can read files, run a shell and call MCP tools.
metadata:
  author: skillcdn
  version: "1.1"
  tools: skillcdn
skillcdn:
  include:
    - references/dry-read.md
    - references/fresh-run.md
    - /engineering/docs/skillcdn/serving.md
    - /engineering/docs/skillcdn/fresh-agents.md
  translations:
    ko:
      title: 새 세션으로 하는 스킬 검증
      description: SkillCDN 포맷 저장소의 스킬을 사용자의 에이전트가 만나는 그대로 검증합니다. 새 에이전트가 파일만 읽고 추측해야 할 곳을 찾고, 새 에이전트가 서빙된 스킬을 실제로 실행하며 체크포인트는 사용자처럼 한 줄로 답하고, 둘에서 나온 발견을 해당 문장에 반영합니다. 서빙된 버전도, 푸시 전의 로컬 변경도, 도구·모델·공유 문서가 바뀐 뒤의 변경 전후도 확인하고, 인용은 원문과 대조하며, 실행의 대상·대사·결과물은 저장소에 넣지 않고, 푸시는 사용자 승인 뒤에만 하며, 요청 없는 재실행은 한 번까지만 합니다. 스킬을 검증·테스트·드라이 리드하거나 새 세션으로 돌려 볼 때, 변경 뒤에도 스킬이 잘 되는지 확인할 때, 수정이 먹혔는지 볼 때 쓰세요. 이미 한 일로 새 스킬을 만들 때는 skillcdn-skill-authoring을 쓰세요.
---
# Verifying a skill from a fresh session

A skill of a repository in the SkillCDN Format goes in; a verdict on it comes out, the way a user's agent will meet it: what a fresh agent had to guess reading its files, what a fresh agent did running it through SkillCDN with its checkpoints answered as the user would, and each finding folded into the sentence it bears on, checked, and pushed on the user's word. It works on what is served, on a local change before it is pushed, and after a tool, a model or a shared page changed under the skill. The format is SkillCDN's and the conventions are the checkout's, read from it; this skill carries the method.

## How the user is involved

- **Question:** only which skill, when the request names none or names one ambiguously.
- **Checkpoints:** the plan, with the dry read's findings, the run's time and spend and any rerun, before any run or push; the fold-in, with its push; the delivery. One short message each in plain words; one word continues.
- **Go-ahead:** when the user says to go on without stopping, the fold-in is made without being shown first; the plan, every push and any spend are still confirmed. Asking for the fold-in ("fold in what comes out") is the full mode, not a go-ahead.
- **Dry read only:** when the request asks only for a dry read, its report is the delivery, and nothing is changed or run.
- **The run's own stops:** the fresh agent's checkpoints are answered by this agent, one line each, with the answers the user approved in the plan. Each stop and its answer are reported in a line as the run goes.

## Requirements

| What | Used for |
|---|---|
| A checkout of the repository the skill lives in, with git and Node.js | The skill's files and history, the fold-in, `node scripts/check.mjs`, the commit and the push |
| The SkillCDN connection to that repository (`browse_repo`, `search_repo`, `load_skill`, `read_repo_file`) | The commit an agent is served; the fresh run, which loads the skill through it |
| A way to start a fresh agent: a subagent tool, or a second session the user starts | The dry read and the fresh run |
| The tools the skill under test names in its Requirements | The fresh run |
| Optional: `npx @skillcdn/cli check`, which needs npm, the network and the Node.js version the package asks for | The indexer's own reading of the fold-in |

Check the first three before the first message, and the tools of the skill under test once phase 1 has read its Requirements, before the plan. Without a checkout, offer the dry read alone, from the files the connection serves, and say that a fold-in needs a checkout. Without the connection, nothing can be run as a user's agent gets it: offer the dry read of the checkout and say that no fresh run was possible. Without a way to start a fresh agent, the user starts it: give them the brief. Without the tools the skill under test needs, say what to connect, or offer the dry read alone.

What the SkillCDN skills share is in the area's document set [`engineering/docs/skillcdn/`](/engineering/docs/skillcdn/README.md). [serving.md](/engineering/docs/skillcdn/serving.md) (which commit an agent gets, how long serving takes, what each way of receiving a skill brings) and [fresh-agents.md](/engineering/docs/skillcdn/fresh-agents.md) (starting an agent with none of this session's context, on each host), which every run reads, are included and arrive with this skill wherever SkillCDN serves it. [transcripts.md](/engineering/docs/skillcdn/transcripts.md) (where a run's record is kept) is linked from phase 4 and read with `read_repo_file` through the repository or the engineering connection, or as a file: under `docs/skillcdn/` of the engineering plugin, or at `engineering/docs/skillcdn/` of a checkout of this repository. A copy of this skill's directory lacks all three, and a mount of it alone lacks the linked one: say so in the first message, fetch what is missing from `engineering/docs/skillcdn/` of the repository this skill comes from (for this collection, `github.com/skillcdn/skills`) where the agent can, and otherwise run on this skill's own files, which carry its workflow and its rules.

The checkout's own conventions decide how a fix is written and where it goes: its working agreement, its guide for skills and knowledge pages, and the guide page of the skill's tool family where there is one (in this repository `CLAUDE.md`, `guide/skill-authoring.md` and `guide/tools/<family>.md`). Read them before phase 5.

## Inputs

| Input | Source |
|---|---|
| The skill | Required: a path (`<area>/skills/<name>`), a name, or "this skill" in a session that has just worked on one. Asked only when missing or ambiguous: "Which skill should I verify? A path like `<area>/skills/<name>`, or its name." |
| The mode | Derived from the request: a dry read alone when only that is asked; otherwise a full verification (dry read, fresh run, fold-in). It is also a change review when the checkout holds an unpushed change to the skill or to a page it reads, or the user says a tool, a model or a shared page changed under it. |
| The request for the run | Optional: the user's own words for what the skill under test should be asked. Derived otherwise in phase 1. |
| Everything else | Derived and shown at the plan checkpoint: the order, the answers, how far the run goes, the runner, the outputs folder, the time and the spend, any rerun. |

## Workflow

Each phase produces a named artifact. The findings, the plan and the run record are scratch files outside the repository ([findings.example.json](assets/findings.example.json) shows the findings' shape); nothing of a run is committed.

### Phase 1: Frame

Produces the **frame**: the skill, its address, the served commit against the checkout, what changed, the mode, the order and the request for the run.

1. Find the skill: its directory, its `SKILL.md`, the manifests above it, the files its `skillcdn.include` lists and the pages its phases link. Its address is the repository's (`skillcdn.ai/gh/<owner>/<repo>`, from the root README or the git remote). Check the tools its Requirements name.
2. Compare what is served with the checkout, as [serving.md](/engineering/docs/skillcdn/serving.md) "Which commit an agent gets" says, for the skill's directory, the manifests above it and every page it includes or links. Read what changed since the skill was last verified: the git log of those paths, and the **coverage notes**, wherever the checkout records what no run has reached (in this repository, the skill's row in `guide/roadmap.md` and its tool notes).
3. Derive the order. Served and unchanged: the dry read and the run both read the served commit, and one fold-in follows them. A local change to the skill or to a page it reads: the change is dry-read first, its fixes are pushed with it on the plan's word, and the run reads the pushed commit.
4. Derive the request for the run, as [fresh-run.md](references/fresh-run.md) "The plan" says; the dry read uses it, and the plan shows it, where the user may change it.

### Phase 2: Dry read

Produces the **findings**, by [dry-read.md](references/dry-read.md). A fresh agent reads the files and does nothing else, with the request for the run and none of this session's context, and reports every place where it would have to guess; for a change, it also compares the old text with the new. Check every quoted sentence against its file before using it, then order the findings by the phase where a run meets them and tag each by what it costs. A dry read costs minutes of a model and nothing else, and starts without a stop. When only a dry read was asked, deliver the report and stop.

### Phase 3: Plan

Produces the **plan**, by fresh-run.md "The plan": the request for the run, the answer to each stop the skill names, how far the run goes, the runner, the outputs folder, the time and the spend, whether one rerun follows the fold-in, and what the run can and cannot verify. For a local change, also the fixes the findings call for, written into the sentences they bear on and shown as a diff.

Checkpoint, in every mode, because the run takes a model's time and may spend the skill's own costs, and may need a push: the findings in a few lines, with the ones to fix first; the fixes, for a local change; the plan; and, when something must be served first, "Pushing publishes <the files> at <address>." One word proceeds; the user may change the request, the answers, how far the run goes or the rerun.

On that word, for a local change: commit the change and its fixes and nothing else, and tell the user which other changes in the tree were left out; `git pull --rebase`; push; wait until the commit is served, as serving.md says.

### Phase 4: Fresh run

Produces the **run record**, by fresh-run.md "The run". Start a fresh agent as [fresh-agents.md](/engineering/docs/skillcdn/fresh-agents.md) says for the host, with only its brief. Answer each stop in one line with the answer the plan holds. A stop the plan did not foresee, and an estimate above the approved one, go to the user before the run goes on. An agent that does not pick the skill, or strays from it, gets one line of direction as the user would give it, and the miss is a finding. Push nothing while the agent is loading the skill. Keep the reports, the transcript's path ([transcripts.md](/engineering/docs/skillcdn/transcripts.md)) and where the outputs are.

### Phase 5: Fold back

Produces the **fold-in** and the **maintainer list**, by fresh-run.md "Reading the run" and "Where a finding goes".

1. Read the run against the skill, phase by phase, and mark for each dry-read finding whether the run met it. What the user finds when they review the result themselves is a finding too.
2. Give each finding its verdict (below) and change the sentence it bears on, in the shape the checkout's guide gives; a fact that can go stale carries its source and the month. Update the coverage notes to say what no run reached. Then read the whole diff for anything of the run.
3. `node scripts/check.mjs` until it reports no problem; `npx @skillcdn/cli check` until it prints `ok: no index diagnostics`, or say why it did not run. Raise the skill's minor version when a change alters what an agent does in a run (a step, a stop, a verdict, a rule, a value it uses); leave it when the same agent would do the same with the new wording.

Checkpoint, in every mode for the push: one line per change and where it went, the coverage notes included, then "Committing and pushing publishes <the files> at <address>. OK?" On a go-ahead the changes are already made, and only the push waits.

### Phase 6: Ship

On the word: commit as the checkout's conventions say, with the body saying what the run verified; `git pull --rebase`; push; wait until the commit is served. Rerun only as the plan approved: once at most, with the same request, when the fold-in alters the run; to the skill's cost checkpoint, left unanswered, when only its plan changed. A rerun the plan did not cover is offered, not started.

Deliver in one message: the skill's address and the served commit; what the dry read found and what the run confirmed; what changed, one line each; what no run reached; what stayed out as material of the run; and, for whoever maintains the skill, the maintainer list. Then offer another round; never start one.

## Verdicts

| Finding | Verdict | Where it goes |
|---|---|---|
| A sentence a fresh agent cannot act on (a choice without its rule, an artifact used before it is named, a contradiction, a value with no way to find it), confirmed by the run or by this agent's own second read | Fix | The sentence the phase lacks, in the skill or the shared page it bears on |
| The dry read and the run stumbled on the same sentence | Fix the wording | Even when the files answer it on a careful read |
| The files answer it on this agent's second read, and one reader alone missed it | No change | Listed as resolved |
| The run improvised a step, or asked what the skill derives | Fix | The phase, or the derivation rule |
| The tool or the service behaved differently from a sentence | Fix | The skill's `tool-notes.md`, or the family's page, with the source and the month |
| A one-time slip of the run, or an answer in another language | No change | The maintainer list |
| A rule of the format or of a manifest | No change | Reported to the user |
| A fix that fits only the run's subject, or tightens a near miss no user would notice | Not made | Generalized, or dropped |
| The agent did not pick the skill, or strayed from it | Fix | The description, or the phase it left |

## Hard rules

1. The fresh agent is given only its brief, the request and the facts of its environment; nothing of this session, not a finding, not an expected answer, not a hint. What its host hands every agent (a memory index, a working agreement) is named in the brief as not to be used. This session's context hides exactly the gaps a user's agent meets.
2. The fresh run loads the skill through the SkillCDN connection at the served commit, never from the checkout: what is served, with its rules and its included pages, is what users get.
3. Each stop of the run is answered in one line with the answer the user approved. A stop nobody foresaw, and an estimate above the approved one, go to the user: the approval covered only what the plan showed.
4. The fresh run is a spend of its own, a model's time and the skill's own costs: it is estimated and confirmed at the plan in every mode, a rerun with it, and every push is confirmed, one at a time.
5. A finding changes the sentence it bears on. A one-time slip goes to the maintainer list; no rule is made from one slip, and nothing is fitted to the run's subject, because every later run of the skill would carry it.
6. Nothing of a run enters the repository: its subject, its people, its lines, the references and the sites it used, local paths, its outputs. Behavior goes in and words stay out; the diff is read for it before every commit, because a push is public.
7. At most one rerun, and only as the plan approved it; then say what the last change was not exercised on, and offer another round without starting it. Each run costs the user time and money, and the user decides on the next.
8. Verified means what a fresh run reached. What no run reached is said so, in the delivery and in the coverage notes, so that the next maintainer knows what is still untried.

## Terminology

| Term | Meaning |
|---|---|
| Skill under test | The skill being verified. |
| Fresh agent | An agent with none of this session's context, given only its brief. |
| Brief | The facts of the fresh agent's environment and the request, verbatim; never a hint. |
| Dry read | A fresh agent reading the skill's files without running anything, for every place it would guess. |
| Change review | A dry read that also compares the old text of a change with the new. |
| Findings | The dry read's numbered list: each quoted sentence with its file and line, its phase and its tag, and from phase 5 its verdict. |
| Request for the run | What a user would say to the skill under test, on a subject that is neither a customer's nor this session's. |
| Fresh run | A fresh agent running the served skill through SkillCDN, its stops answered as the user would. |
| Run record | The fresh agent's reports, its transcript's path, the answers given, the spend and where the outputs are. |
| Coverage notes | Where the checkout records what no fresh run has reached; in this repository, the skill's roadmap row and its tool notes. |
| Fold-in | The changes the findings make, each in the sentence it bears on. |
| Maintainer list | What the run needed beyond the files, and its slips, listed in the delivery for whoever keeps the skill. |
| Served commit | The commit SkillCDN serves, named in the connection's `Source` line. |
| Rerun | A second fresh run after a fold-in, with the same request. |
