---
name: git-desk-setup
description: "Sets up a member's own desk as a private git repository: the folder that console desk writes for a person of a SkillCDN Console, or that an agent account is set up with (their agent's instructions, their projects under work/), committed and pushed to their own git host account, and for a person a dashboard of their work served on their own machine. Use when a user says \"set up my desk\", \"desk setup\", \"make my desk a repository\", \"show me a dashboard of my work\", \"내 데스크 세팅해줘\", or when an agent account reads the desk item of its onboarding task. For a project's repository, git-repo-setup; to change the dashboard's pages, the console's own skill building-a-console. Asks which git host account the desk goes to and which projects to check out, shows the plan, creates the private remote on the user's word, pushes, and opens the dashboard. Nothing is bought, and a desk is never public."
license: MIT
compatibility: Needs a shell with git, and the console command (npm install -g @skillcdn/console, Node.js 24 or newer) signed in as the member whose desk it is. The git host's command (gh for GitHub), signed in as that member, to create the remote; without it the member creates an empty private repository and gives its address. For the dashboard, npm and a browser on the same machine. Works in any agent that can run a shell and write files.
metadata:
  author: skillcdn
  version: "1.0"
  tools: git
skillcdn:
  translations:
    ko:
      title: 구성원 자신의 데스크를 비공개 깃 저장소로 세팅하기
      description: "구성원 자신의 데스크를 비공개 깃 저장소로 세팅합니다. 데스크는 SkillCDN 콘솔의 사람에게 console desk가 써 주거나 에이전트 계정이 세팅될 때 받는 폴더로, 자기 에이전트의 지침과 work/ 아래의 프로젝트가 들어 있습니다. 이것을 커밋해 자신의 깃 호스트 계정에 푸시하고, 사람에게는 내 작업 현황·통계·아카이브를 보여 주는 대시보드를 자기 PC에서 띄웁니다. '내 데스크 세팅해줘', '데스크 레포 만들어줘', '내 작업 대시보드 보여줘'라고 하거나, 에이전트 계정이 온보딩 작업의 데스크 항목을 읽을 때 쓰세요. 프로젝트의 저장소는 git-repo-setup이 만들고, 대시보드 페이지를 바꾸는 일은 콘솔의 building-a-console 스킬이 합니다. 데스크를 둘 깃 호스트 계정과 체크아웃할 프로젝트를 묻고, 계획을 보여 주고, 사용자의 승인으로 비공개 원격 저장소를 만들어 푸시하고, 대시보드를 엽니다. 구매는 없고, 데스크는 공개하지 않습니다."
---
# A member's own desk, set up as a repository

What goes in: a member of a SkillCDN Console, a person or an agent account, with the `console` command signed in as them, and a folder: the desk `console desk` wrote, an empty one, or the desk an agent account was set up with. What comes out: the desk as a private repository at the member's own git host account, committed and pushed; the instructions of their agent in it, true to them; the repositories they asked for cloned under `work/`; and, for a person who wants it, a dashboard of their work built and served on their own machine and opened for them. A desk is where a member's agent starts from when the work is not yet in a project's checkout, and what outlives a session or a machine, so it is a repository from its first day. The console writes the desk's files; this skill makes them a repository and changes only what is untrue for the member.

## How the user is involved

- **Questions:** one message, only what the folder and the commands leave open (Inputs). An agent account asks nobody in chat: what it cannot settle from its onboarding task it asks as a decision on the board.
- **Checkpoints:** the plan, before anything is written or created outside the machine: the folder, the remote by its full name and that it is private, each repository to clone, the dashboard or none. One word proceeds. The delivery.
- **Go-ahead:** the questions with defaults are not asked and the defaults are shown in the plan; the plan still waits, because it creates a remote.
- **Changes mid-run:** another account or name before the remote exists rewrites the plan; after, the remote is renamed or moved at the git host by the member, never made a second time. A repository to clone, or the dashboard, asked for later is done then, from its phase.

## Requirements

| What | Used for |
|---|---|
| A shell with git | The repository, the commit, the push, the clones |
| The `console` command, signed in as the member (`console whoami`) | The desk's files (`console desk`), the member's projects, the dashboard's server |
| The git host's command, signed in as the member (`gh auth status` for GitHub) | Creating the private remote; without it, the member creates an empty private repository and gives its address |
| For the dashboard: npm, and a browser on this machine | Building it and looking at it ([dashboard.md](references/dashboard.md)) |

Check before the first message: `git --version`; `console whoami`; `gh auth status`. A `whoami` that is refused is reported and nothing starts. A `whoami` that names a project means the folder sits in a project's checkout, or `CONSOLE_PROJECT` is set: say what named it and ask for a folder outside that checkout, or for the variable to be unset, because a desk is bound to no project. Without the `console` command, say what it is and how it is had (`npm install -g @skillcdn/console`, then `console login --url <the console's address>`, which a person approves on the console's pages), and stop: a desk is a console member's.

How the board is worked, how an agent account is run and how a console of one's own is built are the console's own skills, working-the-board, running-an-agent and building-a-console, shipped with the command in folders beside each other (`console whoami` prints where the first is). This skill points to them and restates none. Its one reference is in its own directory, so a mount of this skill alone, the area's plugin and a copy all carry it.

## Inputs

| Input | Source |
|---|---|
| Whose desk | `console whoami` says who the command acts as. An agent account's desk holds `runner.json` and its `AGENTS.md` says it is an agent account: go to "An agent account's desk". Anyone else is a person |
| The folder | The current one when it holds a desk (`AGENTS.md` says it is a member's desk) or is empty; otherwise the folder `console desk` makes in the current one, named `<handle>-desk`. A folder inside another repository's working tree (`git rev-parse --show-toplevel` answers) is not used: say so and ask where the desk should be |
| The git host account, and whether the desk is there already | Asked: "Which account at your git host should hold your desk? `gh` is signed in as `<login>`, so it would be the private repository `<login>/<folder name>`. Say another account or organization if you prefer, or that the desk is already there, with its address." An existing desk is cloned, not made again |
| The repositories to check out | Asked: "Which repositories you work on should I clone under `work/` now? None is fine: one can be cloned when its first task comes." For a project the user names, its repositories are those its rules list under where the work lives (`console rules --project <key>`) |
| The dashboard | Asked of a person: "Do you want a dashboard of your work, a page on this machine that shows your open tasks, your figures and what you finished, read from the console when you look?" Default: yes where npm is there |
| Everything else | Derived and shown in the plan: the repository's name (the folder's), the branch (`main`), what the member's `AGENTS.md` gains (the git host account, and what they say of how their agent should work with them) |

## Workflow

Each phase produces a named artifact and ends with one line to the user.

### Phase 1: Frame

Produces the **frame**: the tools found, who the desk is for, and the folder's state: no desk yet; a desk `console desk` wrote and no repository; a repository already, with or without a remote (`git remote -v`). An agent account goes on in "An agent account's desk".

### Phase 2: Plan

Produces the **plan**. Ask the questions of Inputs that remain, in one message, then show, one line each: the folder; the files `console desk` will write and those that are there; the remote (`<account>/<name>`, private) or the one to clone; each repository to clone and where; the dashboard or none; what `AGENTS.md` gains.

Checkpoint: "Here is the plan. Outside this machine, I will: create the private repository `<account>/<name>`; push the desk to it. OK?" One word proceeds.

### Phase 3: Desk

Produces the **desk's files**.

1. An existing desk at the git host is cloned into the folder first (`git clone <address> <folder>`).
2. Run `console desk` where the folder holds no desk yet: with no argument in the folder's parent, where it makes `<handle>-desk`; as `console desk .` inside an empty or cloned folder. It writes `README.md`, `AGENTS.md`, `CLAUDE.md` and `.gitignore`, each only where no file of that name is there, and says which it wrote and which it left. The dashboard's shell is phase 6's to write.
3. Read `AGENTS.md` and `README.md` back against `console whoami` and the answers. Change a line that is untrue for this member; add the git host account the desk goes to, and what the user said of how their agent should work with them, each in a line under the section it belongs to. Nothing else is added, and the file's shape stays the console's, so that a later `console desk` and the desk agree.

### Phase 4: Repository

Produces the **pushed desk**.

1. `git init -b main` where the folder is no repository yet.
2. Before the first commit: `git check-ignore -q work/` succeeds, so that no project is ever committed into the desk; no `.skillcdn-console.json` is in the desk's root; nothing secret is staged (`git status`, `git diff --cached --stat`).
3. Commit as `chore(desk): set up the desk`.
4. Create the remote as the plan approved (`gh repo create <account>/<name> --private --source . --remote origin`), or add the address the member gave of an empty private repository (`git remote add origin <address>`). A remote that exists is checked before anything is pushed to it: `gh repo view <account>/<name> --json visibility` says `PRIVATE` (or the host's own word for it); a public one is never pushed to, and the member is told.
5. `git push -u origin main`, then `git status -sb` shows nothing ahead.

Where the member keeps the remote for later, steps 4 and 5 wait, and the delivery names the local commit by its hash.

### Phase 5: Work

Produces the **checkouts**: each repository of the plan cloned as `work/<name>` (`git clone <address> work/<name>`). In each, `console whoami` names its project, named by that checkout's own `.skillcdn-console.json`; a checkout whose `whoami` names no project is bound as its own agreement says (`console use <key>`, for a public repository), and one that names another project is said to the user and left. A repository's own agreement holds inside it from then on. No repository to clone: nothing is done, and `work/` is made when the first one comes.

### Phase 6: Dashboard, for a person who asked for it

Produces the **dashboard, served and looked at**, as [dashboard.md](references/dashboard.md) says: the shell `console desk --web` wrote under `web/` installed and built, served by `console serve` on this machine, opened in the person's browser, and `web/` committed and pushed. An agent account's run, and a person who said no, skip this phase and never read the page.

### Phase 7: Deliver

Produces the **delivery**, one message: the desk's folder and its remote, private; what `AGENTS.md` says of the member, in two lines; the checkouts under `work/`; the dashboard's address and the one command that starts it again, or that there is none; how to go on (open the agent in the desk; `console work` is the plate; a new repository is set up from here with `git-repo-setup`); and what was not verified, said so.

## An agent account's desk

An agent account's desk is settled by `console agent setup`, which writes or clones it, and its onboarding task lists what the account then does itself; `console desk` writes nothing for it and says so, and an account with no desk yet is set up first, as running-an-agent says. This skill does the desk item of that task and nothing else, on the task's run, as the account:

1. The checks of phase 4, step 2.
2. A first commit where the desk has none.
3. The remote, named as the onboarding task names it, private, made with the account's own sign-in at its git host: the host's command signed in as the account, or handed the account's token for that one command from its store (`GH_TOKEN="$(console secret git.token)" gh repo create <name> --private --source . --remote origin` for GitHub), the value never printed, written to a file or put in the remote's address. Where the account has no sign-in or no token at the git host yet, or may not make the repository there, that is asked as a decision on the board with the exact name, and the rest of the onboarding goes on meanwhile.
4. The credential helper for its own pushes, as running-an-agent gives it, then the push.
5. A report on the run: the remote's name, that it is private, and the pushed commit. No dashboard, and no question in chat.

## Verdicts

| Result | Verdict |
|---|---|
| The desk is pushed, the remote is private, `git status -sb` shows nothing ahead; `work/` is ignored and no binding file is in the desk's root; `AGENTS.md` says who the member is as `console whoami` does; each checkout's `whoami` names its own project; the dashboard, where asked for, answered at its address and showed the person's own work | Delivered |
| The remote waits for the member, or the git host's command is missing | Delivered locally, the commit named by its hash and the commands that finish it given |
| The dashboard could not be built or looked at (no npm, no browser the agent can open, a `console desk` without `--web`) | Delivered without it, the reason said and how to add it later |
| The remote is public, something secret is staged, or `work/` is not ignored | Not delivered: fixed first, and a public remote is the member's to make private or replace |

## Hard rules

1. A desk is private. It is never created public and never pushed to a public remote: it says how a member works, and may hold notes on the organization's work.
2. No secret in the desk, ever: no token, key or environment file is staged, and no token is in a remote's address. A person's sign-ins stay with their git host's command and their system; an agent account's in its store in the console.
3. A desk is bound to no project: no `console use` in its root and no `.skillcdn-console.json` there, since every checkout under `work/` without a binding of its own would inherit it. A board command in the desk names its project (`--project <key>`).
4. `work/` stays out of the desk's repository, checked before the first commit: a project lives in its own repository, with its own agreement.
5. Nothing of the board is copied into the desk: no task, report or page of a private pack. The dashboard reads the console when it is looked at; the desk keeps what the member writes.
6. Nothing is created outside the machine (the remote, the push) unless the plan listed it and the user said yes; an agent account asks as a decision what it may not do itself.
7. The dashboard is served on this machine by `console serve` and nowhere else: never deployed, never put behind a tunnel, never given a token of its own, because it shows the organization's board with the person's sign-in.
8. The desk's files are the console's to write: this skill changes what is untrue for the member and adds what they said, and never rewrites the template.

## Terminology

| Term | Meaning |
|---|---|
| Desk | A member's own repository: the instructions of their agent, their projects checked out under `work/`, and what should outlive a session or a machine. Written by `console desk` for a person, by `console agent setup` for an agent account. |
| Member | Whoever the `console` command is signed in as: a person, or an agent account, which is a member of its own. |
| `work/` | The folder of the desk where project repositories are cloned, each with its own agreement and binding; ignored by the desk's repository. |
| Dashboard | A console of the person's own in the desk's `web/`, served on their machine, showing their open work, their figures and their archive from the organization's console. |
