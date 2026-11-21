---
name: git-studio-setup
description: "Sets up a studio, the shared git repository in which a team and its agents keep producing one kind of thing (card news for an account, ad creatives, the episodes of a series) or keep running one kind of round (ad optimization), with what it learns kept where the next session finds it. Use when a user says \"set up a repository where we keep making our card news\", \"make this repo our ad creative studio\", \"a repo for the team to run ad optimization in\", \"우리 계정 카드뉴스를 계속 만들 저장소 세팅해줘\". It extends git-repo-setup, which it runs for the agreement, the README, the documents and the console project; a repository that holds code or documents and produces nothing day after day needs that skill alone. Adds the unit with its states and the ones only a person gives, a ledger so that nothing is made or tried twice, a review screen, one check, and the studio's own small pack, a skill per job that extends a skill of the pack with the person's policy and the know-how by topic. Nothing is bought."
license: MIT
compatibility: Needs a shell with git and Node.js, git-lfs where a unit holds pictures or video, and what git-repo-setup needs (the console command and the git host's command, signed in). Works in any agent that can run a shell and write files.
metadata:
  author: skillcdn
  version: "1.0"
  tools: git
skillcdn:
  translations:
    ko:
      title: 팀과 에이전트가 계속 만들어 내는 스튜디오 저장소 구성
      description: "스튜디오를 구성합니다. 스튜디오는 팀과 에이전트가 한 종류의 결과물(계정의 카드뉴스, 광고 소재, 시리즈의 회차)을 계속 만들거나 한 종류의 회차 작업(광고 최적화)을 계속 돌리는 공용 깃 저장소이고, 일하며 알게 된 것을 다음 세션이 찾는 자리에 남깁니다. '우리 계정 카드뉴스를 계속 만들 저장소 세팅해줘', '이 레포를 광고 소재 스튜디오로 만들어줘', '팀이 광고 최적화를 돌릴 레포 잡아줘'라고 할 때 쓰세요. git-repo-setup의 확장 스킬이라 작업 합의, README, 문서, 콘솔 프로젝트는 그 스킬을 돌려 만듭니다. 매일 무엇을 만들어 내지 않는 저장소는 그 스킬만으로 충분합니다. 여기에 제작 단위와 상태, 사람만 줄 수 있는 상태, 같은 것을 두 번 만들거나 시도하지 않게 하는 장부, 검수 화면, 하나의 검사, 그리고 스튜디오 자신의 작은 팩을 더합니다. 팩에는 팩의 스킬을 확장하는 작업별 스킬, 사람의 방침, 주제별 노하우 문서가 들어갑니다. 구매는 없습니다."
---
# A studio: the repository a team keeps producing in

What goes in: a folder (empty, a repository already laid out, or one in which production runs in a shape of its own) and a sentence on what is produced there. What comes out: a studio, committed and pushed. It is the repository `git-repo-setup` lays out, with three things added: the structure of production (one unit with its states, a ledger, a review screen, a check), a small pack of the studio's own in which each job has a skill that extends a skill of the pack, and the pages in which what the studio learns is kept so that a session reads little and finds the right sentence. Nothing is produced by this skill: the first unit is made afterwards, with the studio skill it wrote.

## How the user is involved

- **Questions:** one message, only what the request and the folder leave open (Inputs). The questions the extended pack skills would ask on every run are asked once, here, and their answers become the policy.
- **Checkpoints:** the studio's plan (phase 2); `git-repo-setup`'s own plan, which lists what is made outside the machine; the delivery.
- **Go-ahead:** the studio's plan is shown and not waited on; `git-repo-setup`'s plan still waits, and so does every person state from then on.
- **Changes mid-run:** before the files, a change rewrites the plan. After, a unit's name, a state or a job changes `studio.json`, the template, the studio skill and `docs/architecture.md` together, in one commit.

## Requirements

| What | Used for |
|---|---|
| A shell with git and Node.js | The studio's commands, which have no dependency |
| git-lfs, where a unit holds pictures or video | The outputs; `git lfs version` says whether it is there, and without it the plan says how it is had and no large file is committed until it is |
| `git-repo-setup` | The repository itself. Load it with this skill, before the first message: its Requirements say how the run starts (`console whoami`, the git host's command) and those checks are this run's |
| The pack skills the studio will extend | Their questions, inputs and checkpoints, read in phase 2 so that the studio's skills answer them. Found with a search of the pack by the words of the job |

Two pages of the area's set [`engineering/docs/git/`](/engineering/docs/git/README.md) are read before the plan: [studio.md](/engineering/docs/git/studio.md) (the tree, `studio.json`, the record, the ledger, the review screen, the commands, the check, working together, the starting values by kind) and [studio-know-how.md](/engineering/docs/git/studio-know-how.md) (the manifest, how a studio skill extends a pack skill, the pages, what is read when, folding work back, trying a technique). [templates.md](references/templates.md) is read before the files. They are read as `git-repo-setup`'s Requirements say its pages are, each in a call of its own; a mount of this skill alone, or a copy of its directory, lacks the two pages of the set: fetch them from `engineering/docs/git/` of the repository this skill comes from (`github.com/skillcdn/skills` for this pack). The scripts are this skill's `scripts/`, read as text and written into the studio; where they cannot be read, the commands are written to what studio.md "The commands" and "The check" say of each.

## Inputs

| Input | Source |
|---|---|
| The folder | As `git-repo-setup` takes it. Its state decides the route: empty or new; a repository with this pack's layout (an agreement of ten sections, `docs/`); or production already under way in its own shape |
| What is produced, for whom, how often | The request; what it leaves open is asked: "What will be made or run here, for whom, and how often?" |
| The unit, its states and the kind's values | Derived from studio.md "Starting values by kind" and shown in the plan |
| Who approves | Asked: "Who says a <unit> may go out, and where do they answer: on the board or in chat?" |
| The jobs | Derived: one per step that a skill of the pack does for this kind, each with the pack skill it extends, shown in the plan. A job no pack skill covers is named as one to be written whole, after the setup |
| The standing answers | Each extended pack skill's Inputs and questions, asked once in the same message, in that skill's own wording, with "leave it open" as an answer; and what the request and the folder already say |
| What the team already knows | Asked: "Is there anything the team has already settled or learned about this work: a guide, corrections you keep repeating, a format? Point me to it." |
| Who works in it, the console project, the remote | `git-repo-setup`'s inputs, asked by it |
| Everything else | Derived and shown in the plan: the folder's and the ledger's names, `needs`, `previews`, `shows`, `large`, which changes go straight to the main branch |

## Workflow

Each phase produces a named artifact and ends with one line to the user.

### Phase 1: Frame

Produces the **frame**: the tools found, `git-repo-setup`'s checks, what the request settles, and the folder's state. Where production is under way, map it and move nothing: which folder holds the units, which file is a unit's record and which of its fields is the state, the states in use, where the person's instructions are written (and which of them contradict each other or live only in a session's memory), where what was learned is kept and how large it has grown.

### Phase 2: Plan

Produces the **plan**. Read the two pages. Find and load each pack skill the studio extends, far enough to list what it asks, what it names (folders, helpers) and where it stops; where the kind's own set already lists them (a card news account's record), that page stands in for the reading. Ask what remains, in one message. Then show:

- the unit: its name and folder, the states in order with who writes each, the person's states, the last state and where a unit is filed;
- the ledger: its path and what a key names here;
- the jobs: each studio skill, the pack skill it extends, and what it answers for it;
- the policy: its headings with the answers given, and those left open;
- the know-how brought in: which page of `docs/guides/` each thing the team already knows goes to, and what is left where it is;
- the review screen and what a card shows; the large files and where they are stored, with what the git host's page says of its storage;
- for a repository in production: what is renamed or moved, and that finished units stay where they are unless the user says otherwise.

Checkpoint: "Here is the studio. OK, or change something?" One word proceeds.

### Phase 3: Lay out

Produces the **studio's files**, from [templates.md](references/templates.md), in this order, each a line to the user:

1. `git init -b main` where the folder is no repository; with large files, `git lfs install` and the patterns in `.gitattributes`. `.gitignore`, `package.json`, the continuous integration workflow with its two jobs.
2. `studio.json`, the template folder, the ledger.
3. `scripts/`: the six files of this skill's `scripts/`, as they are.
4. `SKILLCDN.md`, and one `skills/<job>/SKILL.md` per job, written as studio-know-how.md "A studio skill extends a pack skill" says, from what phase 2 read of the pack skill. A standing answer nobody gave is left out of the table, so that the pack skill still asks it.
5. `docs/policy.md` from the answers, in the person's words; `docs/guides/<step>.md` for what the team already knows, one fact in one page, and no page for a step nothing is known about yet; a format the team has, under `formats/`.
6. `docs/architecture.md`: the parts, and the unit's path as a table of the states with what each means, who writes it and what the check asks from it.
7. `npm run check`, then `npx --yes @skillcdn/cli@latest check`, until both pass; the first still warns that the agreement and the documents' map are not written, which phase 4 does. `npm run new` on a throwaway slug, `npm run gallery`, then that unit's folder and row removed.

In a repository in production, a step changes what the plan said and nothing else, and step 5 moves each standing instruction to its one line of the policy and each lesson to the sentence of its guide page, the dated log they came from removed in the same commit.

### Phase 4: The repository

Produces the **pushed repository**.

- **A new folder:** run `git-repo-setup` on it and hand it what this run settled: what the studio is for and for whom, who works in it, the stack (documents and data with Node.js scripts) and its check (`npm run check`), the README's language, what the agreement and the documents' map gain (templates.md, the last section), the tasks that come next (the first format where there is none, the first unit, each job to be written whole), and that the remote is left to it. It stops once, for its own plan, then writes its files around these, commits, pushes, watches continuous integration and hands the commit in on its setup task.
- **A repository that has the layout:** the agreement and the map gain the same lines, the second job is added to the workflow, and the commit and the push go as that repository's agreement says, on a task of the board.

### Phase 5: Delivery

Produces the **delivery**, one message: the repository; the unit and its states in a line; each studio skill with the pack skill it extends and the command that loads it; what the policy holds and what it leaves open; `npm run serve` and the address it prints (started now only if the user wants to look, with how it is stopped); the two checks and their results; the first thing to do, which is one unit made with the studio skill; what was not tried, said so. The next tasks are on the board.

## Adding a job later

A second job, or a job no pack skill covers, is one more `skills/<job>/SKILL.md` written by studio-know-how.md, with its line in the agreement's Skills section, in a commit of its own. A studio whose skills have run is changed from its runs, by folding them back as that page says, not by running this skill again.

## Verdicts

| Result | Verdict |
|---|---|
| Both checks pass; a throwaway unit went from the new command to the review screen; every studio skill names a pack skill that exists and answers only what was said; `git-repo-setup` delivered | Delivered |
| A pack skill to extend could not be loaded | Delivered without that studio skill, the job named as a task |
| git-lfs is missing and units hold large files | Delivered with the patterns written and no large file committed, the install named |
| A policy line, a guide's sentence or a standing answer holds what nobody said | Not delivered: removed, or asked |
| A finished unit was moved or changed without the plan saying so | Not delivered: put back first |

## Hard rules

1. A person state is written only on that person's answer, with their words in the record. No script, schedule or go-ahead sets it: it is the one place the studio waits for a person.
2. A studio skill never copies a pack skill and never loosens one. A copy stops receiving what the pack learns, and a loosened rule on spending or on what leaves is the pack's rule broken.
3. The policy and the guides hold what the person said and what a run showed. A line written to fill a heading teaches every later session to trust it.
4. No large file is committed before its pattern is in `.gitattributes` and git-lfs is installed: a binary once in history stays there.
5. What the setup of a repository in production moves or rewrites is what the plan listed. Finished units are a record.
6. The gallery is generated and never committed: committed, it conflicts on every parallel unit.

## Terminology

| Term | Meaning |
|---|---|
| Studio | A repository in which one kind of unit is produced or run again and again, with its own skills and pages. |
| Unit | One thing made (a post, a creative, an episode) or one round of ongoing work, as a folder with a record. |
| Person state | A state only a named person gives: an approval, a decision. |
| Ledger | The table with one row per unit, by which nothing is made or tried twice. |
| Studio skill | A skill of the studio's own pack that extends a pack skill with the studio's answers and differences. |
