---
name: git-studio-setup
description: "Sets up a studio, the shared git repository in which a team and its agents keep producing one kind of thing (card news for an account, ad creatives, the episodes of a series) or keep running one kind of round (ad optimization, a market watch), or both, with what it learns kept where the next session finds it. Use when a user says \"set up a repository where we keep making our card news\", \"make this repo our ad creative studio\", \"a repo for the team to run ad optimization in\", \"우리 계정 카드뉴스를 계속 만들 저장소 세팅해줘\". It extends git-repo-setup, which it runs for the agreement, the README, the documents and the console project; a repository that holds code or documents and produces nothing daily needs that skill alone. Adds each unit with its states and the ones only a person gives, a ledger so that nothing is made or tried twice, a review screen, one check, and the studio's own small pack: a start page, a skill per job that extends a skill of the pack, the policy and the know-how by topic. Nothing is bought."
license: MIT
compatibility: Needs a shell with git and Node.js, git-lfs where a unit holds pictures or video, and what git-repo-setup needs (the console command and the git host's command, signed in). Works in any agent that can run a shell and write files.
metadata:
  author: skillcdn
  version: "1.2"
  tools: git
skillcdn:
  translations:
    ko:
      title: 팀과 에이전트가 계속 만들어 내는 스튜디오 저장소 구성
      description: "스튜디오를 구성합니다. 스튜디오는 팀과 에이전트가 한 종류의 결과물(계정의 카드뉴스, 광고 소재, 시리즈의 회차)을 계속 만들거나 한 종류의 회차 작업(광고 최적화, 시장 감시)을 계속 돌리거나, 둘을 함께 하는 공용 깃 저장소이고, 일하며 알게 된 것을 다음 세션이 찾는 자리에 남깁니다. '우리 계정 카드뉴스를 계속 만들 저장소 세팅해줘', '이 레포를 광고 소재 스튜디오로 만들어줘', '팀이 광고 최적화를 돌릴 레포 잡아줘'라고 할 때 쓰세요. git-repo-setup의 확장 스킬이라 작업 합의, README, 문서, 콘솔 프로젝트는 그 스킬을 돌려 만듭니다. 매일 무엇을 만들어 내지 않는 저장소는 그 스킬만으로 충분합니다. 여기에 제작 단위와 상태, 사람만 줄 수 있는 상태, 같은 것을 두 번 만들거나 시도하지 않게 하는 장부, 검수 화면, 하나의 검사, 그리고 스튜디오 자신의 작은 팩을 더합니다. 팩에는 시작 페이지, 팩의 스킬을 확장하는 작업별 스킬, 사람의 방침, 주제별 노하우 문서가 들어갑니다. 구매는 없습니다."
---
# A studio: the repository a team keeps producing in

What goes in: a folder and a sentence on what is produced there. What comes out: a studio, committed and pushed. It is the repository `git-repo-setup` lays out, with three things added: the structure of production (each kind of unit with its states and its ledger, a review screen, a check that also says where the studio stands), a small pack of the studio's own in which each job has a skill that extends a skill of the pack, and the pages that keep what the studio learns, laid out by what a session reads: a start page every session, one skill a job, a page a phase. Nothing is produced by this skill: the first unit is made afterwards, with the studio skill it wrote.

## How the user is involved

- **Questions:** one message, only what the request and the folder leave open (Inputs). The questions the extended pack skills would ask on every run are asked once, here, and their answers become the policy; what `git-repo-setup` would ask is asked in the same message, so that the user is asked once.
- **Checkpoints:** the studio's plan (phase 2); `git-repo-setup`'s own plan, which lists what is made outside the machine; the delivery.
- **Go-ahead:** told to go ahead alone, the studio's plan is shown and not waited on; `git-repo-setup`'s plan still waits, and so does every person state from then on.
- **Changes mid-run:** before the files, a change rewrites the plan. After, a unit's name, a state or a job changes `studio.json`, the template, the studio skill, the start page and `docs/architecture.md` in one commit.

## Requirements

| What | Used for |
|---|---|
| A shell with git and Node.js | The studio's commands, which have no dependency |
| git-lfs, where a unit holds pictures or video | The outputs; `git lfs version` says whether it is there, and without it the plan says how it is had and no large file is committed until it is |
| [git-repo-setup](/engineering/skills/git-repo-setup/SKILL.md) | The repository itself. Load it with this skill, before the first message: its Requirements say how the run starts (`console whoami`, the git host's command) and those checks are this run's |
| The pack skills the studio will extend | Their questions, inputs and checkpoints, read in phase 2. Found by a search of the pack for the words of the job |

The scripts are this skill's `scripts/`, read as text and written into the studio; where they cannot be read, the commands are written to what studio.md "The commands" and "The check" say of each. Links that start with `/` are files of the pack this skill is from: a copy of this directory, a plugin or a mount below the root that lacks one reads it through the pack's connection (`https://skillcdn.ai/gh/skillcdn/skills`) or at `github.com/skillcdn/skills`.

## Inputs

| Input | Source |
|---|---|
| The folder | As `git-repo-setup` takes it. Its state decides the route: empty or new; a repository with this pack's layout (an agreement of ten sections, `docs/`); or production already under way in its own shape |
| What is produced, for whom, how often | The request; what it leaves open is asked: "What will be made or run here, for whom, and how often?" |
| The units, their states and each kind's values | Derived from studio.md "Starting values by kind" and shown in the plan: one unit per kind of thing the request says is made or run again and again. Kinds where one works on another (creatives and the rounds that tune them) are units of one studio |
| Who approves | Asked: "Who says a <unit> may go out, and where do they answer: on the board or in chat?" |
| The jobs | Derived and shown in the plan: one per step that a pack skill does for this kind, with the skill it extends. A job no pack skill covers is named as one to be written whole, after the setup |
| The standing answers | Each extended pack skill's Inputs and questions, asked once in the same message, in that skill's own wording, with "leave it open" as an answer; and what the request and the folder already say |
| What the team already knows | Asked: "Is there anything the team has already settled or learned about this work: a guide, corrections you keep repeating, a format? Point me to it." |
| Who works in it (people, agent accounts), the console project, the remote's owner | `git-repo-setup`'s inputs, asked here in its wording, in the same message, and handed to it as settled |
| Everything else | Derived and shown in the plan: the folder's and the ledger's names, a standing file, `needs`, `previews`, `shows`, `large`, the pack's address for the skills' links (`console skills` names it), which changes go straight to the main branch |

## Workflow

Each phase produces a named artifact and ends with one line to the user.

### Phase 1: Frame

Produces the **frame**: the tools found, `git-repo-setup`'s checks, what the request settles, the folder's state. Where production is under way, map it and move nothing: which folder holds the units, which file is a unit's record and which of its fields is the state, the states in use, and what a session reads there before any job, in bytes (the agreement, the pages it sends to, a page of lessons). Note each fact kept twice (a unit's state in a record and in a page of status, a rule in the agreement and in a brief), each page that restates a pack skill, and each instruction of the person's that contradicts another or lives only in a session's memory.

### Phase 2: Plan

Produces the **plan**. Read [studio.md](/engineering/docs/git/studio.md) and [studio-know-how.md](/engineering/docs/git/studio-know-how.md) before this phase, each in a call of its own. Find and load each pack skill the studio extends, far enough to list what it asks, what it names (folders, helpers) and where it stops; where the kind's own set already lists them (a card news account's record), that page stands in for the reading. Ask what remains in one message, `git-repo-setup`'s questions among them. Then show:

- each unit: its name and folder, the states in order with who writes each, the person's states, the last state and where a unit is filed, its ledger's path and what a key names, a standing file where rounds read one; for several kinds, the field in which one names the other and which job reads it;
- the jobs: each studio skill, the pack skill it extends, and what it answers for it;
- the policy: its headings with the answers given, and those left open;
- the know-how brought in: which page of `docs/guides/` each thing the team already knows goes to;
- what a session will read: the agreement, the start page and the check's last lines, then one skill and the pages its phases link; for a repository in production, beside the bytes read today;
- what a card of the review screen shows; where the large files are stored, with what the git host's page says of its storage;
- for a repository in production: what is renamed or moved, which page keeps each doubled fact, and that finished units stay where they are unless the user says otherwise.

Checkpoint: "Here is the studio. OK, or change something?" One word proceeds.

### Phase 3: Lay out

Produces the **studio's files**. Read [templates.md](references/templates.md) and [studio-operating.md](/engineering/docs/git/studio-operating.md) before this phase. In this order, each a line to the user:

1. `git init -b main` where the folder is no repository; with large files, `git lfs install` and the patterns in `.gitattributes`. `.gitignore`, `package.json`, the workflow of continuous integration with its two jobs.
2. `studio.json`, and each unit's template folder and ledger; a standing file in the shape of the pack skill that reads it.
3. `scripts/`: the six files of this skill's `scripts/`, as they are.
4. `SKILLCDN.md` with its `start`, and one `skills/<job>/SKILL.md` per job, written as studio-know-how.md "A studio skill extends a pack skill" says, from what phase 2 read of the pack skill, its first paragraph linking that skill by its skill URI. A standing answer nobody gave is left out of the table, so that the pack skill still asks it.
5. `docs/policy.md` from the answers, in the language layout.md gives the documents; `docs/guides/<step>.md` for what the team already knows, one fact in one page, and none for a step nothing is known about yet; a format the team has, under `formats/`; then `docs/start.md`, a row for every skill and guide page.
6. `docs/architecture.md`: the parts, and each unit's states as a table: what each means, who writes it, what the check asks from it.
7. `npm run check`, then `npx --yes @skillcdn/cli@latest check --references`, until both pass and every pack skill linked is found; the first still warns that the agreement and the documents' map are not written, which phase 4 does. `npm run new` on a throwaway slug for each unit, `npm run gallery`, then those folders and rows removed.

In a repository in production, step 5 moves each standing instruction to its one line of the policy and each lesson to the sentence of its guide page, the dated log they came from removed in the same commit; a page that restated a pack skill becomes the lines that differ, in the job's skill.

### Phase 4: The repository

Produces the **pushed repository**.

- **A new folder:** run `git-repo-setup` on it and hand it what this run settled: what the studio is for and for whom, who works in it, the console project and the remote's owner as answered, the stack (documents and data with Node.js scripts) and its check (`npm run check`), the README's language, what the agreement and the documents' map gain (templates.md, the last section), the tasks that come next (the first format where there is none, the first unit, each job to be written whole), and that the remote is left to it. It stops once, for its own plan, then writes its files around these, commits, pushes and hands the commit in on its setup task.
- **A repository that has the layout:** the agreement and the map gain the same lines, the workflow its second job, and the commit and the push go as that repository's agreement says, on a task of the board.

### Phase 5: Delivery

Produces the **delivery**, one message: the repository; each unit and its states in a line; each studio skill with the pack skill it extends and the command that loads it; what the policy holds and leaves open; what a session reads at its start, in bytes; `npm run serve` and the address it prints (started now only if the user wants to look); the two checks and their results; the first thing to do, which is one unit made with the studio skill; what was not tried. The next tasks are on the board.

## Adding a job later

A second job is one more `skills/<job>/SKILL.md` written by studio-know-how.md, with its row in the start page; a second kind of unit, one more entry of `studio.json` with its template folder, its ledger and its jobs; each in a commit of its own. A studio whose skills have run is changed by folding its runs back as that page says, not by running this skill again.

## Verdicts

| Result | Verdict |
|---|---|
| Both checks pass and every linked pack skill was found; a throwaway unit went from the new command to the review screen; `git-repo-setup` delivered | Delivered |
| A pack skill to extend could not be loaded, or the check says its pack is "not known" | Delivered without that studio skill, or with its link unverified and said so; the job named as a task |
| A fact is kept in two pages, or a page restates a pack skill | Not delivered: one page keeps it and the other links |

## Hard rules

1. A person state is written only on that person's answer, with their words in the record: an answer about the unit, or the policy's line where they approved a class in advance. No script, schedule or go-ahead sets it: it is the one place the studio waits for a person.
2. A studio skill never copies a pack skill and never loosens one. A copy stops receiving what the pack learns, and a loosened rule on spending or on what leaves is the pack's rule broken.
3. The policy, the guides and the standing answers hold what the person said and what a run showed. A line written to fill a heading teaches every later session to trust it: it is removed, or asked.
4. No large file is committed before its pattern is in `.gitattributes` and git-lfs is installed: a binary once in history stays there.
5. The setup of a repository in production moves or rewrites only what the plan listed. Finished units are a record: one changed outside the plan is put back first.
6. The gallery is generated and never committed, and no page of the studio's state is kept by hand: either conflicts on every parallel unit.

## Terminology

| Term | Meaning |
|---|---|
| Unit | One thing made or one round of ongoing work, as a folder with a record. |
| Person state | A state only a named person gives: an approval, a decision. |
| Standing file | The record every round of a kind reads and adds to, outside any unit. |
| Start page | The one page of the studio every session reads, which only routes; the manifest's `start` names it. |
| Studio skill | A skill of the studio's own pack that extends a pack skill with the studio's answers and differences. |
