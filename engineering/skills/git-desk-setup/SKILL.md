---
name: git-desk-setup
description: "Sets up a member's own desk as a private git repository: the folder that console desk writes for a person of a SkillCDN Console, or that an agent account is set up with (their agent's instructions, the records of what they keep, their projects under work/), committed and pushed to their own git host account, with git LFS where they keep large files, and for a person the desk's pages, their own dashboard on the console's UI, served on their machine. Use when a user says \"set this desk up as a repository of mine\", \"bring its pages up\", \"set up my desk\", \"desk setup\", \"my dashboard\", \"내 데스크 세팅해줘\", or when an agent account reads the desk item of its onboarding task. For a project's repository, git-repo-setup; to change the desk's pages, the console's own skill building-a-console. Asks which account the desk goes to, what to keep there and which repositories to check out, shows the plan, creates the private remote on the user's word and pushes. Nothing is bought, and a desk is never public."
license: MIT
compatibility: Needs a shell with git, and the console command (npm install -g @skillcdn/console, Node.js 24 or newer) signed in as the member whose desk it is. The git host's command (gh for GitHub), signed in as that member, to create the remote; without it the member creates an empty private repository and gives its address. git-lfs where the desk keeps pictures or video. For the desk's pages, npm and a browser on the same machine. Works in any agent that can run a shell and write files.
metadata:
  author: skillcdn
  version: "1.7"
  tools: git
skillcdn:
  translations:
    ko:
      title: 구성원 자신의 데스크를 비공개 깃 저장소로 세팅하기
      description: "구성원 자신의 데스크를 비공개 깃 저장소로 세팅합니다. 데스크는 SkillCDN 콘솔의 사람에게 console desk가 써 주거나 에이전트 계정이 세팅될 때 받는 폴더로, 자기 에이전트의 지침, 남겨 두려는 것의 기록(records/), work/ 아래의 프로젝트가 들어 있습니다. 이것을 커밋해 자신의 깃 호스트 계정에 푸시하고, 큰 파일을 둘 곳에는 git LFS를 잡고, 사람에게는 콘솔 UI를 자기 것으로 확장한 데스크 페이지(내 대시보드)를 자기 PC에서 띄웁니다. '이 데스크를 내 저장소로 세팅해줘', '내 데스크 세팅해줘', '내 대시보드 띄워줘'라고 하거나, 에이전트 계정이 온보딩 작업의 데스크 항목을 읽을 때 쓰세요. 프로젝트의 저장소는 git-repo-setup이 만들고, 데스크 페이지를 바꾸는 일은 콘솔의 building-a-console 스킬이 합니다. 데스크를 둘 계정, 거기에 남길 것, 체크아웃할 저장소를 묻고, 계획을 보여 주고, 사용자의 승인으로 비공개 원격 저장소를 만들어 푸시합니다. 구매는 없고, 데스크는 공개하지 않습니다."
---
# A member's own desk, set up as a repository

What goes in: a member of a SkillCDN Console, a person or an agent account, with the `console` command signed in as them, and a folder: the desk `console desk` wrote, an empty one, or the desk an agent account was set up with. What comes out: the desk as a private repository at the member's own git host account, wholly theirs, committed and pushed; what they said they want kept there written into its instructions, with the first collection of its records; the repositories they asked for cloned under `work/`; and, for a person who asks for them, the desk's pages served on their own machine and opened. A desk is where a member's agent starts when the work is not yet in a project's checkout, and where what they made is kept, files and all. The console writes its files; this skill makes them a repository.

## How the user is involved

- **Questions:** one message, only what the folder and the commands leave open (Inputs). An agent account asks nobody in chat.
- **Checkpoints:** the plan (phase 2), before anything is written or made outside the machine; the delivery.
- **Go-ahead:** the questions with defaults are not asked and the defaults are shown in the plan, which still waits, because it creates a remote. The pages and what the desk keeps are no defaults: they follow the request (Inputs).
- **Changes mid-run:** another account or name before the remote exists rewrites the plan; after, the member renames or moves the remote at the git host. A repository to clone, something to keep, or the pages, asked for later is done then, from its phase.

## Requirements

The tools of the compatibility line. Before the first message: `console whoami` and `gh auth status`; where the request asks for the pages or `web/` is there, `node --version`, `npm --version` and `console help desk`, which must name `--web`, and without one of the three the pages are left out, said so.

- A `whoami` that is refused is reported and nothing starts. One that names a project means the folder sits in a project's checkout, or `CONSOLE_PROJECT` is set: say what named it and ask for a folder outside that checkout, or for the variable to be unset, because a desk is bound to no project and `console desk` refuses to make one there. Without the `console` command, say how it is had (`npm install -g @skillcdn/console`, then `console login --url <the console's address>`, approved by a person there), and stop.
- Work done in a desk for its member (its setting-up, a record, a page) is the member's own: it is no task and goes on no board unless the member asks for it there. An agent account's desk item is on the board already, in its onboarding task.
- The page on the desk's pages, [pages.md](references/pages.md), is read only by a run that builds them; through a console that is `console skill --file engineering/skills/git-desk-setup/references/pages.md`.

## Inputs

| Input | Source |
|---|---|
| Whose desk | `console whoami` says who the command acts as. A desk that holds `runner.json`, whose `AGENTS.md` says it is an agent account's: go to "An agent account's desk". Anyone else is a person |
| The folder | `desk` in the current folder, where `console desk` has just made it there: the usual start, with the session standing in its parent. Work inside it from here on, and read its `AGENTS.md` and its `records/README.md` there first, since a session not started in the desk was not handed them. Else the current one when it holds a desk (its `AGENTS.md` says whose desk it is) or is empty; otherwise `desk`, which `console desk` makes in the current one. A folder inside another repository (`git rev-parse --show-toplevel` answers a folder above this one) is not used: say so and ask where the desk should be |
| The git host account | Asked: "Which account at your git host should hold your desk? `gh` is signed in as `<login>`, so it would be the private repository `<login>/desk`. Say another account, organization or name, that the desk is already there, or that the remote can wait." Before the plan, `gh repo view <account>/desk` answers not found for a new one; where it is there, ask whether it is their desk, to be cloned, or whether this one takes another name |
| What the desk keeps | Asked with the others, and skippable: "Is there a kind of thing you make that you want collected here, with whether it was used and how it did: ad creatives, documents, designs? Say none and it can be added any day." Where what they name is pictures or video, the desk keeps the files themselves through git LFS (`git lfs version` says whether it is installed; without it, say how it is had, and the large files wait) |
| The repositories to check out | Asked: "Which repositories should I clone under `work/` now? Give each by its address or as `<owner>/<name>`. None is fine: one can be cloned when its first task comes." Where the user names a project and no repository, what it adds to the rules lists its repositories under "Where the work lives" (`console rules --project <key>`, where that stands first); where it lists none, ask. Nothing is guessed from a task's words |
| The pages | Built where the request asks for the dashboard or the pages (the sentence `console desk --web` prints asks to bring its pages up) or `web/` is there already. Otherwise asked of a person with the other questions: "Do you want your desk's pages, your own pages on the console's UI on this machine, which show what the desk keeps?" Never built on a go-ahead that says nothing of them: the delivery then names them as one request away |
| Everything else | Derived and shown in the plan: the repository's name (`desk`, as an agent account's is, unless the user gave another), the branch (`main`), the line `AGENTS.md` gains under "Who I am" for the git host account the desk goes to |

## Workflow

Each phase produces a named artifact and ends with one line to the user.

### Phase 1: Frame

Produces the **frame**: the tools found, who the desk is for, and the folder's state: no desk yet; a desk `console desk` wrote and no repository; a repository already, with or without a remote.

### Phase 2: Plan

Produces the **plan**. Ask the questions of Inputs that remain, in one message, then show, one line each: the folder; the files `console desk` will write and those that are there; the remote (`<account>/desk`, private), the one to clone, or that it waits; what the desk keeps, as the line `AGENTS.md` gains in the member's words and its first collection; git LFS, with the kinds of file it takes and what the git host's own page says of its LFS storage (a quota, a price), so that nothing large is pushed before the member knows; each repository to clone and where; the pages or none.

Checkpoint: "Here is the plan. Outside this machine, I will: create the private repository `<account>/desk`; push the desk to it. OK?" One word proceeds.

### Phase 3: Desk

Produces the **desk's files**.

1. A desk that is at the git host already is cloned into an empty folder. Where the current folder holds files `console desk` just wrote, clone beside it, say so, and go on in the clone.
2. Where the folder holds no desk yet, `console desk`: with no argument in the folder's parent, where it makes `desk`; as `console desk .` inside an empty or cloned folder. It writes the desk's files, each only where no file of that name is there, and says which.
3. With the pages in the plan, `console desk . --web` in the desk also writes their shell under `web/`, where that holds nothing; where it ends with `1` because the command carries no shell, nothing was written, and the pages are left out, said so. Then install and build the shell (pages.md "Building them") before the first commit, so that one commit carries the shell with its lockfile.
4. Read `AGENTS.md` and `README.md` back against `console whoami`. A line that is untrue for this member is changed, and the phase's line shows it, old and new; the line for the git host account is added under the heading the plan named, "Who I am" in the file `console desk` writes, and nowhere else.
5. Where the member named something to keep: a line in `AGENTS.md` for each kind, where the file names the kinds the desk keeps ("This desk"), in the member's words with nothing of the agent's added, and the first collection under `records/`, made as the desk's `records/README.md` says, which is the form. `console desk check` must find it right, and a note it prints is mended too. Nothing else is written into the desk's files.

### Phase 4: Repository

Produces the **pushed desk**.

1. `git init -b main` where the folder is no repository yet. With LFS in the plan, `git lfs install` in the repository and the patterns of the kinds of file in `.gitattributes`. Then stage everything.
2. In a command of its own, before any command that commits, read the staged list (`git status --short`): `git check-ignore -q work/` succeeds; no `.skillcdn-console.json` is in the desk's root; nothing secret, no `node_modules/` and no build folder is in the list.
3. Commit as `chore(desk): set up the desk`.
4. Create the remote as the plan approved (`gh repo create <account>/desk --private --source . --remote origin`), or add the address of the empty private repository the member made. A remote that exists is checked before anything is pushed to it: `gh repo view <account>/desk --json visibility`, which takes an address too, must say `PRIVATE`. Without `gh` the member's word stands, and the delivery names the privacy as not verified.
5. Push, and see that nothing is left ahead. A push refused for credentials is the git host command's to mend (`gh auth setup-git`), on the member's word.

Where the remote waits, steps 4 and 5 do too, and the delivery names the local commit by its hash.

### Phase 5: Work

Produces the **checkouts**: each repository of the plan cloned as `work/<name>`. In each, `console whoami` names its project, named by that checkout's own `.skillcdn-console.json`; a checkout whose `whoami` names no project is bound as its own agreement says (`console use <key>`, for a public repository), and one that names another project is said to the user and left. No repository to clone: nothing is done, and `work/` is made when the first one comes.

### Phase 6: Pages, for a person who asked for them

Produces the **pages, served and looked at**, as pages.md says: the build served by `console serve` with the desk's records beside it, checked, and opened for the person to say what they see.

### Phase 7: Deliver

Produces the **delivery**, one message: the desk's folder and its remote, private; what changed in `AGENTS.md`; what the desk keeps, with its first collection, or that nothing was named and that saying what to keep adds it any day; git LFS where it was set up, and what the host says of its storage; the checkouts under `work/`; the pages' address, who stops their server and how they are started again (pages.md), or that there are none and that they are one request away; how to go on (open the agent in the desk, whose `AGENTS.md` says the rest); and what was not verified, said so.

## An agent account's desk

An agent account's desk is the same kind of thing: its own repository, wholly its own, with records, and pages only where its manager wants them. `console agent setup` settles it: it clones the one the account pushed before, or writes the files and makes no repository; `console desk` refuses an agent account. The onboarding task lists what the account then does itself, and this skill does the desk item of it and nothing else, as the account, on that task's run: its reports and decisions are working-the-board's, and a board command in the desk names the task's project (`--project <key>`).

1. `git init -b main` where the desk is no repository yet, the staging and the checks of phase 4, steps 1 and 2, and a first commit where there is none. `runner.json` is the desk's and is committed: no secret is in it.
2. The token for the git host is `git.token` in the account's store: `console secrets` lists the names it keeps, never a value. It is handed to one command at a time and never read alone, since `console secret git.token` by itself prints it: `GH_TOKEN="$(console secret git.token)" gh <command>` in a POSIX shell; `$env:GH_TOKEN = console secret git.token; gh <command>; Remove-Item Env:GH_TOKEN` on one line in PowerShell. Never in a file, and never in the remote's address.
3. The remote, named as the onboarding task names it, private. Where `gh repo view <name> --json visibility`, handed the token so, finds it, it must say `PRIVATE` before anything is pushed; else `gh repo create <name> --private --source . --remote origin`, handed the token the same way. No account or token at the git host yet, or no right to make the repository there: asked as a decision with the exact name, and the rest of the onboarding goes on meanwhile.
4. The credential helper for its own pushes, as the console's skill running-an-agent gives it (in the folder beside working-the-board's, which `console whoami` prints; under "The agent: making the machine its own", the item "Make your desk a repository at your git host and push it"), then the push. From then on the runner commits and pushes the desk at the end of every session.
5. A report on the run: the remote's name, that it is private, the pushed commit.

## Verdicts

| Result | Verdict |
|---|---|
| The desk is pushed to a private remote, with nothing ahead; `work/` is ignored and no binding file is in the desk's root; `AGENTS.md` says who the member is as `console whoami` does, and what they said to keep; `console desk check` finds the records right; each checkout's `whoami` names its own project; the pages, where asked for, passed pages.md's check and the person said what they see | Delivered |
| The remote waits for the member, or the git host's command is missing | Delivered locally, the commit named by its hash, with the commands that finish it |
| The pages could not be built, or the person did not say what they see | Delivered, the pages left out or their look named as theirs to confirm |
| A checkout under `work/` names another project than its own, or one named from outside it | Delivered, that checkout named as bound wrong and left for the person |
| The remote is public, something secret is staged, or `work/` is not ignored | Not delivered: fixed first; a public remote is the member's to make private or replace |

## Hard rules

1. A desk is private: never created public, never pushed to a public remote. It is a member's own, and says how they work and what they made.
2. No secret in the desk: no token, key or environment file is staged, and no token is in a remote's address. A person's sign-ins stay with their git host's command and their system; an agent account's in its store in the console.
3. A desk is bound to no project and holds none: no `console use` and no `.skillcdn-console.json` in its root, since every checkout under `work/` without a binding of its own would inherit it, and `work/` stays out of its repository.
4. Nothing is created outside the machine unless the plan listed it and the user said yes, and nothing large is pushed before the member knows what the host's storage for it costs; an agent account asks as a decision what it may not do itself.
5. The desk's pages are served on this machine by `console serve` and nowhere else: never deployed, tunnelled or given a token of their own, because the server answers with the member's sign-in.
6. The desk's files are the member's once written: a line is changed only where it is untrue for them or they asked for it, and no file is overwritten.

## Terminology

| Term | Meaning |
|---|---|
| Member | Whoever the `console` command is signed in as: a person, or an agent account, which is a member of its own. |
| Records | What a desk keeps of what its member made, files and all, under `records/`, whose `README.md` is the form. |
| The desk's pages | The member's own extension of the console's UI, in `web/`, served on their machine: what a person calls their dashboard. |
