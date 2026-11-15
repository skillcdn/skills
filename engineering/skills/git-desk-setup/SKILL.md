---
name: git-desk-setup
description: "Sets up a member's own desk as a private git repository: the folder that console desk writes for a person of a SkillCDN Console, or that an agent account is set up with (their agent's instructions, the records of what they made, their projects under work/), committed and pushed to their own git host account, and for a person a dashboard of their records and their work served on their own machine. Use when a user says \"set this desk up as a repository of mine\", \"set up my desk\", \"desk setup\", \"bring my dashboard up\", \"내 데스크 세팅해줘\", or when an agent account reads the desk item of its onboarding task. For a project's repository, git-repo-setup; to change the dashboard's pages, the console's own skill building-a-console. Asks which git host account the desk goes to and which repositories to check out, shows the plan, creates the private remote on the user's word, pushes, and opens the dashboard where it was asked for. Nothing is bought, and a desk is never public."
license: MIT
compatibility: Needs a shell with git, and the console command (npm install -g @skillcdn/console, Node.js 24 or newer) signed in as the member whose desk it is. The git host's command (gh for GitHub), signed in as that member, to create the remote; without it the member creates an empty private repository and gives its address. For the dashboard, npm and a browser on the same machine. Works in any agent that can run a shell and write files.
metadata:
  author: skillcdn
  version: "1.2"
  tools: git
skillcdn:
  translations:
    ko:
      title: 구성원 자신의 데스크를 비공개 깃 저장소로 세팅하기
      description: "구성원 자신의 데스크를 비공개 깃 저장소로 세팅합니다. 데스크는 SkillCDN 콘솔의 사람에게 console desk가 써 주거나 에이전트 계정이 세팅될 때 받는 폴더로, 자기 에이전트의 지침, 만든 것의 기록(records/), work/ 아래의 프로젝트가 들어 있습니다. 이것을 커밋해 자신의 깃 호스트 계정에 푸시하고, 사람에게는 만든 것의 기록과 보드의 내 작업을 보여 주는 대시보드를 자기 PC에서 띄웁니다. '이 데스크를 내 저장소로 세팅해줘', '내 데스크 세팅해줘', '내 대시보드 띄워줘'라고 하거나, 에이전트 계정이 온보딩 작업의 데스크 항목을 읽을 때 쓰세요. 프로젝트의 저장소는 git-repo-setup이 만들고, 대시보드 페이지를 바꾸는 일은 콘솔의 building-a-console 스킬이 합니다. 데스크를 둘 깃 호스트 계정과 체크아웃할 저장소를 묻고, 계획을 보여 주고, 사용자의 승인으로 비공개 원격 저장소를 만들어 푸시하고, 요청한 경우 대시보드를 엽니다. 구매는 없고, 데스크는 공개하지 않습니다."
---
# A member's own desk, set up as a repository

What goes in: a member of a SkillCDN Console, a person or an agent account, with the `console` command signed in as them, and a folder: the desk `console desk` wrote, an empty one, or the desk an agent account was set up with. What comes out: the desk as a private repository at the member's own git host account, committed and pushed; the repositories they asked for cloned under `work/`; and, for a person who asks for it, the dashboard served on their own machine and opened for them. A desk is where a member's agent starts when the work is not yet in a project's checkout, and where what the member made is kept and followed (`records/`), with their work on the board beside it; so it has to outlive a session and a machine. The console writes its files; this skill makes them a repository.

## How the user is involved

- **Questions:** one message, only what the folder and the commands leave open (Inputs). An agent account asks nobody in chat.
- **Checkpoints:** the plan (phase 2), before anything is written or made outside the machine; the delivery.
- **Go-ahead:** the questions with defaults are not asked and the defaults are shown in the plan, which still waits, because it creates a remote. The dashboard is no default: it follows the request (Inputs).
- **Changes mid-run:** another account or name before the remote exists rewrites the plan; after, the member renames or moves the remote at the git host. A repository to clone, or the dashboard, asked for later is done then, from its phase.

## Requirements

The tools of the compatibility line. Before the first message: `console whoami` and `gh auth status`; and, where the request asks for the dashboard or `web/` is there, `node --version`, `npm --version` and `console help desk`, which must name `--web`. Without one of those three the dashboard is left out, said so.

- A `whoami` that is refused is reported and nothing starts. One that names a project means the folder sits in a project's checkout, or `CONSOLE_PROJECT` is set: say what named it and ask for a folder outside that checkout, or for the variable to be unset, because a desk is bound to no project and `console desk` refuses to make one there. Without the `console` command, say how it is had (`npm install -g @skillcdn/console`, then `console login --url <the console's address>`, approved by a person there), and stop.
- Setting a desk up is no project's work: no task is written for it, no run is taken and nothing goes on the board. An agent account's desk item rides on its onboarding task.
- The dashboard's page, [dashboard.md](references/dashboard.md), is read only by a person's run that builds the dashboard; through a console that is `console skill --file engineering/skills/git-desk-setup/references/dashboard.md`.

## Inputs

| Input | Source |
|---|---|
| Whose desk | `console whoami` says who the command acts as. A desk that holds `runner.json`, whose `AGENTS.md` says it is an agent account's: go to "An agent account's desk". Anyone else is a person |
| The folder | The current one when it holds a desk (its `AGENTS.md` says whose desk it is) or is empty; otherwise `<handle>-desk`, which `console desk` makes in the current one. A folder inside another repository (`git rev-parse --show-toplevel` answers a folder above this one) is not used: say so and ask where the desk should be |
| The git host account | Asked: "Which account at your git host should hold your desk? `gh` is signed in as `<login>`, so it would be the private repository `<login>/<folder name>`. Say another account or organization, that the desk is already there, with its address, or that the remote can wait." Before the plan, `gh repo view <account>/<name>` answers not found for a new one; a taken name gets another, shown in the plan |
| The repositories to check out | Asked: "Which repositories should I clone under `work/` now? Give each by its address or as `<owner>/<name>`. None is fine: one can be cloned when its first task comes." Where the user names a project and no repository, its rules list its repositories under where the work lives (`console rules --project <key>`); where they list none, ask. Nothing is guessed from a task's words |
| The dashboard | Built where the request asks for it (the sentence `console desk --web` prints does) or `web/` is there already. Otherwise asked of a person with the other questions: "Do you want the dashboard, a page on this machine that shows what you made and how it did, with your work on the board beside it?" Never built on a go-ahead that says nothing of it: the delivery then names it as one request away |
| Everything else | Derived and shown in the plan: the repository's name (the folder's), the branch (`main`), the one line `AGENTS.md` gains (the git host account the desk goes to) |

## Workflow

Each phase produces a named artifact and ends with one line to the user.

### Phase 1: Frame

Produces the **frame**: the tools found, who the desk is for, and the folder's state: no desk yet; a desk `console desk` wrote and no repository; a repository already, with or without a remote.

### Phase 2: Plan

Produces the **plan**. Ask the questions of Inputs that remain, in one message, then show, one line each: the folder; the files `console desk` will write and those that are there; the remote (`<account>/<name>`, private), the one to clone, or that it waits; each repository to clone and where; the dashboard or none; the line `AGENTS.md` gains.

Checkpoint: "Here is the plan. Outside this machine, I will: create the private repository `<account>/<name>`; push the desk to it. OK?" One word proceeds.

### Phase 3: Desk

Produces the **desk's files**.

1. A desk that is at the git host already is cloned into an empty folder. Where the current folder holds files `console desk` just wrote, clone beside it, say so, and go on in the clone.
2. Where the folder holds no desk yet, `console desk`: with no argument in the folder's parent, where it makes `<handle>-desk`; as `console desk .` inside an empty or cloned folder. It writes the desk's files, each only where no file of that name is there, and says which.
3. With the dashboard in the plan, `console desk . --web` in the desk also writes the dashboard's shell under `web/`, where that holds nothing; where it ends with `1` because the command carries no shell, nothing was written, and the dashboard is left out, said so. Then install and build the shell (dashboard.md "Building it") before the first commit, so that one commit carries the shell with its lockfile.
4. Read `AGENTS.md` and `README.md` back against `console whoami`. A line that is untrue for this member is changed, and the phase's line shows it, old and new; the line the plan named is added where the file says who the member is. Nothing else is written into them.

### Phase 4: Repository

Produces the **pushed desk**.

1. `git init -b main` where the folder is no repository yet, and stage everything.
2. In a command of its own, before any command that commits, read the staged list (`git status --short`): `git check-ignore -q work/` succeeds; no `.skillcdn-console.json` is in the desk's root; nothing secret, no `node_modules/` and no build folder is in the list.
3. Commit as `chore(desk): set up the desk`.
4. Create the remote as the plan approved (`gh repo create <account>/<name> --private --source . --remote origin`), or add the address of the empty private repository the member made. A remote that exists is checked before anything is pushed to it: `gh repo view <account>/<name> --json visibility`, which takes an address too, must say `PRIVATE`. Without `gh` the member's word stands, and the delivery names the privacy as not verified.
5. Push, and see that nothing is left ahead. A push refused for credentials is the git host command's to mend (`gh auth setup-git`), on the member's word.

Where the remote waits, steps 4 and 5 do too, and the delivery names the local commit by its hash.

### Phase 5: Work

Produces the **checkouts**: each repository of the plan cloned as `work/<name>`. In each, `console whoami` names its project, named by that checkout's own `.skillcdn-console.json`; a checkout whose `whoami` names no project is bound as its own agreement says (`console use <key>`, for a public repository), and one that names another project is said to the user and left. No repository to clone: nothing is done, and `work/` is made when the first one comes.

### Phase 6: Dashboard, for a person who asked for it

Produces the **dashboard, served and looked at**, as dashboard.md says: the build served by `console serve` with the desk's records beside it, checked, and opened for the person to say what they see.

### Phase 7: Deliver

Produces the **delivery**, one message: the desk's folder and its remote, private; what changed in `AGENTS.md`; the checkouts under `work/`; what `records/` is for (what the member's agent makes from now on that should be found again, a creative, a document, a result, is recorded there as its `README.md` says, which is the format, and `console desk check` says whether a record is right); the dashboard's address, how it is started again and how it is stopped, or that there is none and that it is one request away; how to go on (open the agent in the desk, whose `AGENTS.md` says the rest); and what was not verified, said so.

## An agent account's desk

`console agent setup` settles an agent account's desk: it clones the one the account pushed before, or writes the files and makes no repository; `console desk` refuses an agent account. The onboarding task lists what the account then does itself, and this skill does the desk item of it and nothing else, as the account, on that task's run: its reports and decisions are working-the-board's, and a board command in the desk names the task's project (`--project <key>`).

1. `git init -b main` where the desk is no repository yet, the staging and the checks of phase 4, steps 1 and 2, and a first commit where there is none. `runner.json` is the desk's and is committed: no secret is in it.
2. The token for the git host is `git.token` in the account's store: `console secrets` lists the names it keeps, never a value. It is handed to one command at a time and never read alone, since `console secret git.token` by itself prints it: `GH_TOKEN="$(console secret git.token)" gh <command>` in a POSIX shell; `$env:GH_TOKEN = console secret git.token; gh <command>; Remove-Item Env:GH_TOKEN` on one line in PowerShell. Never in a file, and never in the remote's address.
3. The remote, named as the onboarding task names it, private. Where `gh repo view <name> --json visibility`, handed the token so, finds it, it must say `PRIVATE` before anything is pushed; else `gh repo create <name> --private --source . --remote origin`, handed the token the same way. No account or token at the git host yet, or no right to make the repository there: asked as a decision with the exact name, and the rest of the onboarding goes on meanwhile.
4. The credential helper for its own pushes, as the console's skill running-an-agent gives it (in the folder beside working-the-board's, which `console whoami` prints; under "The agent: making the machine its own", the item "Make your desk a repository at your git host and push it"), then the push. From then on the runner commits and pushes the desk at the end of every session.
5. A report on the run: the remote's name, that it is private, the pushed commit. No dashboard; its `records/` is kept as a person's is.

## Verdicts

| Result | Verdict |
|---|---|
| The desk is pushed to a private remote, with nothing ahead; `work/` is ignored and no binding file is in the desk's root; `AGENTS.md` says who the member is as `console whoami` does; each checkout's `whoami` names its own project; the dashboard, where asked for, passed dashboard.md's check and the person said what they see | Delivered |
| The remote waits for the member, or the git host's command is missing | Delivered locally, the commit named by its hash, with the commands that finish it |
| The dashboard could not be built, or the person did not say what they see | Delivered, the dashboard left out or its look named as theirs to confirm |
| A checkout under `work/` names another project than its own, or one named from outside it | Delivered, that checkout named as bound wrong and left for the person |
| The remote is public, something secret is staged, or `work/` is not ignored | Not delivered: fixed first; a public remote is the member's to make private or replace |

## Hard rules

1. A desk is private: never created public, never pushed to a public remote. It says how a member works and what they made, and may hold notes on the organization's work.
2. No secret in the desk: no token, key or environment file is staged, and no token is in a remote's address. A person's sign-ins stay with their git host's command and their system; an agent account's in its store in the console.
3. A desk is bound to no project and holds none: no `console use` and no `.skillcdn-console.json` in its root, since every checkout under `work/` without a binding of its own would inherit it, and `work/` stays out of its repository.
4. Nothing of the board is copied into the desk: no task, report or page of a private pack. The dashboard reads the console when it is looked at; the desk records what the member made.
5. Nothing is created outside the machine unless the plan listed it and the user said yes; an agent account asks as a decision what it may not do itself.
6. The dashboard is served on this machine by `console serve` and nowhere else: never deployed, tunnelled or given a token of its own, because it shows the organization's board with the person's sign-in.
7. The desk's files are the member's once written: a line is changed only where it is untrue for them, and no file is overwritten.

## Terminology

| Term | Meaning |
|---|---|
| Member | Whoever the `console` command is signed in as: a person, or an agent account, which is a member of its own. |
| Records | What the member made and what became of it, kept as files under the desk's `records/`, whose `README.md` is the format. |
