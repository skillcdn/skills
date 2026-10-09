---
name: skillcdn-skill-authoring
description: Turns work a person and an agent have already done together into a skill in the SkillCDN Format, in a checkout of this repository or a fork of it. Reads the session it runs in first (the request, the steps, the questions, the user's corrections, what was approved, what a draft was rejected for), then earlier transcripts, memory and results where the user points; keeps the method and leaves the product and the people out; designs what is asked, what is derived, where the user is consulted and what makes a result accepted; writes the skill in this layout with discovery in place of values; checks it; has a fresh agent follow the files alone; ships it with its catalog rows. Also folds a run's findings back into an existing skill. Use when the user says to make what was just done into a skill, to add a skill for a tool or a job to the skills repository, or to improve a skill from a run. For a skill that will not live in a repository of this layout, the host's own skill creator is the better choice.
license: MIT
compatibility: Needs a shell with git and Node.js in a checkout of the target repository, and the host's transcripts and memory where the user points to earlier sessions. The tool the new skill drives is needed for the test run. The example script needs Python; a transcript can be read without it. Works in any agent that can read files and run a shell.
metadata:
  author: skillcdn
  version: "1.2"
  tools: skillcdn
skillcdn:
  include:
    - references/evidence.md
    - references/distillation.md
    - references/testing.md
    - /engineering/docs/skillcdn/serving.md
    - /engineering/docs/skillcdn/fresh-agents.md
  translations:
    ko:
      title: 이미 한 일로 만드는 SkillCDN 스킬
      description: 사람과 에이전트가 이미 함께 한 일을 SkillCDN 포맷의 스킬로 만듭니다. 이 저장소나 포크의 체크아웃에서, 지금 세션의 요청·단계·질문·수정·승인·거절된 초안을 먼저 읽고, 사용자가 가리키는 이전 트랜스크립트·메모리·결과물을 더해, 방법은 남기고 제품과 사람은 뺀 채로 스킬을 설계하고(무엇을 묻고 무엇을 유도하는지, 어디서 사용자에게 확인하는지, 무엇이 결과를 통과시키는지), 이 저장소의 꼴로 값 대신 찾는 법을 적어 쓰고, 검사하고, 새 에이전트가 파일만 보고 실행하게 한 뒤, 카탈로그 행과 함께 올립니다. 기존 스킬에 실행 결과를 반영하는 데도 씁니다. 방금 한 일을 스킬로 만들어 달라고 할 때, 도구나 일을 위한 스킬을 스킬 저장소에 추가할 때, 실행 결과로 스킬을 고칠 때 쓰세요. 이 레이아웃의 저장소에 들어가지 않을 스킬이라면 호스트 자체의 스킬 생성기가 더 맞습니다.
---
# A skill from work already done

What goes in: a job that was done with a tool, in this session or in others, with what the user said along the way. What comes out: a skill directory at `<area>/skills/<name>/` in a checkout of this repository or a fork of it, its rows in the catalogs, a passing check, one run by a fresh agent that followed the files alone, and a commit. The skill is written from evidence, not from a description of the job: the steps actually taken, the questions actually asked, the corrections the user actually made, the result they actually accepted. The same skill folds a run's findings back into a skill that exists. The format is SkillCDN's and is not restated here; the conventions are the checkout's and are read from it; this skill carries the method, from the evidence to the design, and the know-how of composing a skill that a fresh agent can run alone.

## How the user is involved

- **Questions:** three, written under "Inputs", asked only when the session leaves them open: which job, where the evidence is, which area. Everything else is derived and shown.
- **Checkpoints:** the design, before anything is written; the draft, after the dry read and before it is committed; every push, the first with the test plan and its cost, because a push to `main` is a public release; the delivery. Each is one short message in plain words, and "OK" continues.
- **Go-ahead:** when the user says to go ahead alone, the draft checkpoint is skipped. Every push and any spend are confirmed in every mode.
- **Changes mid-run:** applied from that point on. A change to the design after the draft rewrites the draft, not the sheet.

## Requirements

| What | Used for |
|---|---|
| A shell in a checkout of the target repository, this one or a fork, with git and Node.js | The conventions, the existing skills whose shape is kept, `node scripts/check.mjs`, the commit and the push. |
| This session's context | The first and main evidence. |
| The host's transcripts and memory | Evidence from sessions this one did not see, read when the user points to them or the session refers to work it does not hold; [transcripts.md](/engineering/docs/skillcdn/transcripts.md) says where each host keeps them. |
| The tool the new skill drives | Its catalog today, for the discovery instructions; the test run. |
| A way to run a fresh agent: a subagent tool, or a second session the user starts | The dry read and the fresh run. |
| Optional: the SkillCDN connection to the repository (`skillcdn.ai/gh/<owner>/<repo>`); `npx @skillcdn/cli check`, which needs npm and the network | Loading the pushed skill as a fresh agent does, and `search_repo` over the skills' descriptions; the indexer's own check, which prints what an agent is told and the skill's size as served. |

Check these before the first message. Without a checkout, stop: say that the skill is written into a checkout of the repository, give the clone command (`git clone https://github.com/skillcdn/skills` for this collection; a fork gives its own), and go on to the design only if the user wants it handed over as text. Without the tool but with a run, write from the evidence and report the test as not run. Without the tool and without a run, stop and say what to connect: there is nothing to write from. Without a way to run a fresh agent, the user runs it: give them the brief.

What the SkillCDN skills share is in the area's document set [`engineering/docs/skillcdn/`](/engineering/docs/skillcdn/README.md). [serving.md](/engineering/docs/skillcdn/serving.md) (which commit an agent is served, how long a push takes) and [fresh-agents.md](/engineering/docs/skillcdn/fresh-agents.md) (how an agent with none of this session's context is started on each host), which every run reads, are included and arrive with this skill wherever SkillCDN serves it. [transcripts.md](/engineering/docs/skillcdn/transcripts.md) (where a session's record is kept) is linked from the phases that read it and read with `read_repo_file` through the repository or the engineering connection, or as a file: under `docs/skillcdn/` of the engineering plugin, or at `engineering/docs/skillcdn/` of a checkout of this repository. A copy of this skill's directory lacks all three, and a mount of it alone lacks the linked one: say so in the first message, fetch what is missing from `engineering/docs/skillcdn/` of the repository this skill comes from (for this collection, `github.com/skillcdn/skills`) where the agent can, and otherwise run on this skill's own files, which carry its workflow and its rules.

What to read in the checkout, and when. The format is the [SkillCDN Format specification](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/skill-repo.md) in the SkillCDN repository: the layout, the front-matter, what is served and searched. It is not restated here; the guide says what this layout adds and the two checks apply the format's rules, so read the specification when the checkout's agreement asks for it or when a check reports what the guide does not explain. `CLAUDE.md` is the working agreement for every change, with its documentation protocol and its gotchas: it is in the agent's context in this checkout, and read first elsewhere. `guide/adding.md` has the list of areas and the steps for an area, a tool family and a document set: read in phase 1. The root `SKILLCDN.md` and the target area's `SKILLCDN.md` carry the rules the new skill inherits and must not restate; the rules that arrived with this skill are the engineering area's, so read the target area's before the design. `guide/skill-authoring.md` holds what this layout adds to the format, the body skeleton, the style and the shape of a knowledge page, `guide/roadmap.md` the row the skill gets, and `guide/tools/<family>.md`, where one exists, what the family's skills do the same way: read before phase 4. Where they differ from this skill, follow them: a fork changes its conventions there, not here.

## Inputs

| Input | Source |
|---|---|
| The job | "This", "what we just did": the work in this session from the user's first request on it to the result they accepted. A named job: the user's sentence, and the session searched for a run of it. One job per skill. |
| The evidence | This session's context, always, and a memory note already in the context that concerns the job. Earlier transcripts, the memory store and the results folder when the user points to them, or when the session refers to work it does not hold. The tool's catalog today. |
| The target | The checkout the agent is in. The area, derived from who does this work and the area manifests' descriptions, shown at the design checkpoint. The name, `<family>-<job>`. |
| Everything else | Derived and shown at the design checkpoint: the tool family, what the skill asks and what it derives, its checkpoints, its verdicts, its rules, what it includes and what it links, what the family shares. |

The questions, asked in one message at the start and only when the session leaves them open:

- More than one job in the session and the request does not say which: "This session holds two jobs, <A> and <B>. Which one becomes the skill?"
- The request names work the session does not hold: "Where is that work: a transcript, a memory note, an outputs folder, or should I take only what this session holds?"
- Two areas fit the job equally: "This job fits <X> and <Y>. Which area owns it?" Otherwise the area is derived, and the design checkpoint shows it.

When no run of the job is in the session or where the user pointed, ask, in one message: "No run of this job is in this session or where you pointed, and a skill here is written from a run. Shall I do the job once now, with <tool>, under the repository's rules, and make the skill from that run?" Then do the job as a run of its own, with every rule of the repository (the estimate before any spend, every step shown), and continue from phase 2 with that run as the evidence.

## Workflow

Each phase produces a named artifact. The sheet, the design and the run record are scratch files outside the repository; nothing of a run is committed.

### Phase 1: Frame

Produces the **frame**: the job as one line of each kind ("You say", "You get"), the tool family, the area, the name, and the skill that already does the job when one exists.

1. Find the job in the session: the user's first request for it and the result they accepted. A run that did two jobs (a research, then a production from it) is two skills; the seam, which result the second takes and how it chooses, is written in the skill that needs the other's result, and the other stays general.
2. Look for a skill that already does the job: the root `README.md` and the area READMEs in the checkout, and `search_repo` over the skills' descriptions where the repository is connected (a README is not searched). The test is the "You get" line: the same deliverable from the same family is the same job, and the run improves that skill ("Improving a skill from a run", below); a different deliverable from the same tool is a new skill, with the seam written in the one that needs the other's result. The design checkpoint says which it is.
3. The family is the tool the run drove: an MCP server, a website, a CLI, a document tool. The area is the people who do this work, by the area manifests' descriptions in the checkout; none fits: a new area, named from the list in `guide/adding.md` and added as that page says. The name is `<family>-<job>`, lowercase letters and hyphens, the job said as the user would say it.

### Phase 2: Evidence

Produces the **evidence sheet** ([evidence.md](references/evidence.md); its shape in [evidence-sheet.example.json](assets/evidence-sheet.example.json)).

1. This session first: walk the context from the first request on the job to the accepted result and record each item evidence.md "This session" lists, in order. The thinking behind a step is gone; what the user saw and said is what counts.
2. Then the other sources, each as evidence.md says for it: a memory note in the context that concerns the job; the transcripts, the memory store and the results folder the user pointed to; the tool today, for the calls that find each value the run used.
3. Tag every item **invariant** or **instance** by the test in evidence.md "Invariant or instance". Instance items stay on the sheet and never enter the skill. A secret, a hostname or an account identifier is written nowhere, not even on the sheet.

### Phase 3: Design

Produces the **skill design** by [distillation.md](references/distillation.md), one section per decision, shown at the design checkpoint.

1. The description ("The description"), the inputs asked and derived ("Asked or derived"), the phases with their artifacts ("Phases"), the stops ("Where the user is consulted"), the verdicts ("Verdicts"), the hard rules ("Hard rules"), the discovery instructions ("Discovery in place of values"), and what goes where ("Placement in this layout").
2. A correction counts as made with emphasis when the user repeated it, called it a rule or something that must not happen again, or stopped the run for it; those and the repeated ones become hard rules, and no other.
3. The test plan: the one request a fresh agent will get, on a stand-in subject (the user's own test product where they have one, never the run's); the folder outside the repository its outputs go to; the one-line answers to each checkpoint the plan foresees; what the run will cost, estimated with the tool's own cost call where it has one; what the run can and cannot verify. The first run of a new skill goes to the end, because the skill is done only when a fresh agent reached the result; a rerun may stop at the cost checkpoint.

Checkpoint, in plain words: the job in both lines; the area and the name; the description; what is asked and what is derived; the phases and where they stop; the verdicts; the rules; what stayed out as instance material; the test plan with its cost. "OK" writes it. The user may change anything, and a changed design is written, not argued.

### Phase 4: Write and check

Produces the **draft**: the skill directory, its rows in the catalogs, its row in the roadmap.

1. Read, in the checkout, `guide/skill-authoring.md`, `guide/roadmap.md` and `guide/tools/<family>.md` where one exists. Open the existing skill closest to this one and keep its shape, or the one `guide/adding.md` names first for a job of a new kind.
2. Write `SKILL.md` in the skeleton and the style the guide gives, and the files the design placed: references linked from their phases and listed in `skillcdn.include` when every run reads them, `references/tool-notes.md` by topic, assets as small JSON with placeholder values, a script only as an example an agent may run locally. `metadata.author` as the repository's manifest has it; `version` starts at "1.0"; a `translations` entry in the user's language when it is not English, and in each language the neighbouring skills carry.
3. The catalog rows `guide/adding.md` lists for a skill, an area's first skill and a new family, and the skill's row in `guide/roadmap.md` with the status `next`.
4. `node scripts/check.mjs` until it reports nothing; then `npx @skillcdn/cli check` until it prints `ok: no index diagnostics` and lists the skill under the extension with no warnings. Without npm or the network, say so and go on with the first check alone.
5. Self-review by distillation.md "Before the draft is shown"; fix what it finds.

### Phase 5: Dry read

Produces the **dry-read report** and the draft checkpoint ([testing.md](references/testing.md) "Dry read"). A fresh agent that reads and does nothing else, with none of this session's context and told to use nothing it remembers, reads the skill's files as if about to run them and reports every place where it would have to guess, ask or look something up. Run it as a subagent where the host has one, with the brief testing.md gives; otherwise the user opens a session for it. Fix each finding in the files; a finding about the format or about a manifest is reported to the user, not patched into the skill. No cost.

Checkpoint, skipped on a go-ahead: the tree of the skill, the description, the check's last line, what the dry read found and what changed.

### Phase 6: Fresh run

Produces the **run record** and the folded-in skill ([testing.md](references/testing.md)).

Checkpoint, in every mode: "Pushing publishes the skill at <address>. The run then gives a fresh agent only '<request>', answers its checkpoints with <answers>, and spends about <estimate> on <tool>. OK?"

1. Commit the skill's files and the catalog rows and nothing else, naming any unrelated change left in the tree; `git pull --rebase`; push; wait until the service serves the commit, as testing.md "Push first" says.
2. Run the fresh agent as testing.md "The runner" says: only the request and the environment facts; the skill through the SkillCDN connection, never the local files; its checkpoints answered in one line each with the answers the user approved, and no more. A stop the plan did not foresee, or an estimate above the approved one, goes to the user. An agent that does not pick the skill gets one line of direction, and that miss is a finding about the description.
3. Read the run against the skill, phase by phase, and fold back by testing.md "Where a finding goes": what had to be said in chat goes into the skill; what the tool did differently into `tool-notes.md` or the family page; a step improvised into its phase; a one-time slip, and a wrong language, into the maintainer list only.
4. One rerun at most without being asked, and only for a change that would alter the run; offer further reruns, never start them. What no run verified is said so at the delivery.

### Phase 7: Ship

Show the fold-in as one line per change and confirm the push. Commit as the conventions say, with the body saying what the run verified, the roadmap row set to `done`; push. Deliver in one message: the skill's address; what it does, in the two lines; what the run verified and what it did not; what stayed out as instance material; and, for whoever maintains this skill, the **maintainer list**: what had to be said beyond what these files say.

### Improving a skill from a run

The user has run a skill of the repository and wants what the run taught in it, or asks for a change. Phase 2 reads the run against the skill: what the agent had to guess, what the user corrected, what the tool did differently, the maintainer list in the delivery where the skill asks for one. Phase 3 designs the change only: each finding to the sentence it bears on, as distillation.md "Folding a run in" says, never a note appended; a fact that can go stale with its source and month; a rule only from a correction that meets the test of phase 3. Then phases 4 to 7, with the minor version raised when the change alters a run and left when it only mends wording, the catalogs changed only where the one-line summary changed, and one rerun at most.

## Hard rules

1. A skill is written from a run. With no run, the job is done once first, under the repository's rules, and the skill is written from that.
2. Instance material never enters the skill, its notes or its examples: the product, the people, the lines, the references, the customers, the prices paid, the secrets. Behavior goes in; words stay out.
3. A value is replaced by how to find it today; a value that must stand names its source and the month it was checked.
4. The format is the specification's and the conventions are the checkout's; neither is restated in the skill, and the checkout's win where they differ from this skill.
5. The rules of the repository and of the area are not restated; what the skill cannot work without is inside its directory, and only a shared page of the repository's or the area's document sets is reached outside it.
6. A rule comes from a correction the user made more than once or with emphasis, or from a spend or a safety fact. A single slip of one run goes to the maintainer list, not into the skill.
7. The design is approved before anything is written; the draft is shown before it is committed; every push and any spend are confirmed in every mode.
8. A skill is delivered as done only after a fresh agent followed the files alone; until then its roadmap row says `next`, and what no run verified is said so. One rerun at most without being asked.
9. Nothing of a run is committed: not the sheet, not the transcript, not the outputs.

## Terminology

| Term | Meaning |
|---|---|
| Job | One thing a user asks for and gets, said in their words; one skill does one job. |
| Run | The job done once with the tool, by a person with an agent; the only source a skill is written from. |
| Evidence sheet | The scratch record of a run: steps, questions, corrections, approvals, failures, costs, drafts, result, each tagged invariant or instance. |
| Invariant, instance | What holds for the next run of the job, and what belonged to this one. |
| Design | The skill before it is written: trigger, inputs, phases, checkpoints, verdicts, rules, placement, test plan. |
| Checkpoint | A stop where the user is consulted; one word continues. |
| Verdict | The condition on which a result is accepted, accepted with a change, or redone. |
| Discovery | The instruction that finds a value at run time, in place of the value. |
| Preflight | A cost call that prices a step before it runs; the shape of a spend checkpoint. |
| Reserve | The part of an estimate kept for retries, so that a redo does not exceed what was approved. |
| Fresh agent | An agent with none of the authoring session's context, given only the request. |
| Dry read | A fresh agent reading the files without running them, for every place it would guess. |
| Fresh run | A fresh agent running the pushed skill through the service, its checkpoints answered as the user would. |
| Fold back | Changing the sentence a finding bears on, in the skill or in a shared page. |
| Maintainer list | The short list at the end of a delivery of what had to be said beyond the files, for whoever keeps the skill. |
| Family page | A page of the document set the skills of one tool family share. |
| Go-ahead | The user's word that the draft checkpoint may be skipped; never a push or a spend. |
