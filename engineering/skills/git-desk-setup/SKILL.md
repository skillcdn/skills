---
name: git-desk-setup
description: "Sets up a member's own desk as a private git repository: the folder that console desk writes for a person of a SkillCDN Console, or that an agent account is set up with, committed and pushed to their own git account as <account>/desk, with git LFS where large files will be kept and, where the request asks, its pages built and served on their machine. Use when a user says \"set this desk up as a repository of mine\", \"bring its pages up\", \"set up my desk\", \"desk setup\", \"내 데스크 세팅해줘\", or when an agent account reads the desk item of its onboarding task. What the desk then keeps and shows is the console's own skill keeping-a-desk, which this one hands over to; a project's repository is git-repo-setup. Asks which account the desk goes to, shows the plan, creates the private remote on the user's word and pushes. Nothing is bought, and a desk is never public."
license: MIT
compatibility: Needs a shell with git, and the console command (npm install -g @skillcdn/console, Node.js 24 or newer) signed in as the member whose desk it is. The git host's command (gh for GitHub), signed in as that member, to create the remote; without it the member creates an empty private repository and gives its address. git-lfs where large files will be kept. For the desk's pages, npm and a browser on the same machine. Works in any agent that can run a shell and write files.
metadata:
  author: skillcdn
  version: "1.9"
  tools: git
skillcdn:
  translations:
    ko:
      title: 구성원 자신의 데스크를 비공개 깃 저장소로 세팅하기
      description: "구성원 자신의 데스크를 비공개 깃 저장소로 세팅합니다. 데스크는 SkillCDN 콘솔의 사람에게 console desk가 써 주거나 에이전트 계정이 세팅될 때 받는 폴더입니다. 이것을 커밋해 자신의 깃 계정에 <account>/desk로 푸시하고, 큰 파일을 둘 곳에는 git LFS를 잡고, 요청한 경우 데스크 페이지를 빌드해 자기 PC에서 띄웁니다. '이 데스크를 내 저장소로 세팅해줘', '데스크 페이지도 띄워줘', '내 데스크 세팅해줘'라고 하거나, 에이전트 계정이 온보딩 작업의 데스크 항목을 읽을 때 쓰세요. 데스크에 무엇을 남기고 무엇을 볼지는 콘솔의 keeping-a-desk 스킬이 이어받고, 프로젝트의 저장소는 git-repo-setup이 만듭니다. 데스크를 둘 계정을 묻고, 계획을 보여 주고, 사용자의 승인으로 비공개 원격 저장소를 만들어 푸시합니다. 구매는 없고, 데스크는 공개하지 않습니다."
---
# A member's own desk, set up as a repository

What goes in: a member of a SkillCDN Console, a person or an agent account, with the `console` command signed in as them, and a folder: the desk `console desk` wrote, an empty one, or the desk an agent account was set up with. What comes out: the desk as a private repository at the member's own git account, wholly theirs, committed and pushed; and, where the request asks for them, its pages built and served on their machine. This is the first of the two lines `console desk` prints, and no more. What the desk keeps and shows is the second line, the console's own skill keeping-a-desk, which the run hands over to at its end.

## How the user is involved

- **Questions:** one message, only what the folder and the commands leave open (Inputs). An agent account asks nobody in chat.
- **Checkpoints:** the plan (phase 2), before anything is written or made outside the machine; the delivery.
- **Go-ahead:** the questions with defaults are not asked and the defaults are shown in the plan, which still waits, because it creates a remote.
- **Changes mid-run:** another account or name before the remote exists rewrites the plan; after, the member renames or moves the remote at the git host.

## Requirements

The tools of the compatibility line. Before the first message: `console whoami` and `gh auth status`; where the request asks for the pages, `node --version`, `npm --version` and `console help desk`, which must name `--web`, and without one of the three the pages are left out, said so.

- A `whoami` that is refused is reported and nothing starts. One that names a project means the folder sits in a project's checkout, or `CONSOLE_PROJECT` is set: say what named it and ask for a folder outside that checkout, or for the variable to be unset, because a desk is bound to no project and `console desk` refuses to make one there. Without the `console` command, say how it is had (`npm install -g @skillcdn/console`, then `console login --url <the console's address>`, approved by a person there), and stop.
- Work done in a desk for its member is the member's own: setting it up is no task and goes on no board unless the member asks for it there. An agent account's desk item is on the board already, in its onboarding task.
- The page on the desk's pages, [pages.md](references/pages.md), is read only by a run that builds them; through a console that is `console skill --file engineering/skills/git-desk-setup/references/pages.md`.

## Inputs

| Input | Source |
|---|---|
| Whose desk | `console whoami` says who the command acts as. A desk that holds `runner.json` is an agent account's, whatever its other files say of their owner: go to "An agent account's desk". Anyone else is a person |
| The folder | `desk` in the current folder, where `console desk` has just made it there: the usual start, with the session standing in its parent. Work inside it from here on, and read its `AGENTS.md` there first, since a session not started in the desk was not handed it. Else the current one when it holds a desk (its `AGENTS.md` says whose desk it is) or is empty; otherwise `desk`, which `console desk` makes in the current one. A folder inside another repository (`git rev-parse --show-toplevel` answers a folder above this one) is not used: say so and ask where the desk should be |
| The git account | Asked: "Which account at your git host should hold your desk? `gh` is signed in as `<login>`, so it would be the private repository `<login>/desk`. Say another account, organization or name, that the desk is already there, or that the remote can wait." Before the plan, `gh repo view <account>/desk` answers not found for a new one; where it is there, ask whether it is their desk, to be cloned, or whether this one takes another name |
| Large files | Asked with it, and skippable: "Will large files be kept here, such as pictures or video? Then I set git LFS up now; it can be added any day." `git lfs version` says whether it is installed; without it, say how it is had, and LFS waits |
| The pages | Built where the request asks to bring the desk's pages up, as the first line `console desk --web` prints does. Not asked otherwise, and never built on a go-ahead that says nothing of them |
| Everything else | Derived and shown in the plan: the repository's name (`desk`, as an agent account's is, unless the user gave another) and the branch (`main`) |

## Workflow

Each phase produces a named artifact and ends with one line to the user.

### Phase 1: Frame

Produces the **frame**: the tools found, who the desk is for, and the folder's state: no desk yet; a desk `console desk` wrote and no repository; a repository already, with or without a remote.

### Phase 2: Plan

Produces the **plan**. Ask the questions of Inputs that remain, in one message, then show, one line each: the folder; the files that are there, which are the command's four (`README.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`), or that `console desk` will write them; the remote (`<account>/desk`, private), the one to clone, or that it waits; git LFS, with the kinds of file it takes and what the git host's own page says of its LFS storage (a quota, a price), so that nothing large is pushed before the member knows; the pages or none.

Checkpoint: "Here is the plan. Outside this machine, I will: create the private repository `<account>/desk`; push the desk to it. OK?" One word proceeds.

### Phase 3: Desk

Produces the **desk's files**, as the command writes them.

1. A desk that is at the git host already is cloned into an empty folder. Where the current folder holds files `console desk` just wrote, clone beside it, say so, and go on in the clone.
2. Where the folder holds no desk yet, `console desk`: with no argument in the folder's parent, where it makes `desk`; as `console desk .` inside an empty or cloned folder. It writes the four files, each only where no file of that name is there, and says which. Nothing is under `records/`, `web/` or `work/` in a new desk, and nothing is put there here: `console desk check` says that no collection is kept and ends `0`, which is right.
3. With the pages in the plan and `web/` holding nothing, `console desk . --web` in the desk writes their shell; where it ends with `1` because the command carries no shell, nothing was written, and the pages are left out, said so. Then install and build the shell (pages.md "Building it") before the first commit, so that one commit carries the shell with its lockfile.
4. Nothing is written into the desk's files: no line is added to `AGENTS.md`, which gains one when something is kept or shown, and that is keeping-a-desk's.

### Phase 4: Repository

Produces the **pushed desk**.

1. `git init -b main` where the folder is no repository yet. With LFS in the plan, `git lfs install` in the repository and the patterns of the kinds of file in `.gitattributes`. Then stage everything.
2. In a command of its own, before any command that commits, read the staged list (`git status --short`): `git check-ignore -q work/` succeeds; no `.skillcdn-console.json` is in the desk's root; nothing secret, no `node_modules/` and no build folder is in the list.
3. Commit as `chore(desk): set up the desk`.
4. Create the remote as the plan approved (`gh repo create <account>/desk --private --source . --remote origin`), or add the address of the empty private repository the member made. A remote that exists is checked before anything is pushed to it: `gh repo view <account>/desk --json visibility`, which takes an address too, must say `PRIVATE`. Without `gh` the member's word stands, and the delivery names the privacy as not verified.
5. Push, and see that nothing is left ahead. A push refused for credentials is the git host command's to mend (`gh auth setup-git`), on the member's word.

Where the remote waits, steps 4 and 5 do too, and the delivery names the local commit by its hash.

### Phase 5: Pages, where the request asked for them

Produces the **pages, served and checked**, as pages.md says: the build served by `console serve`, the member named at its address, and the page opened for the person. It is one empty page of their own; what it shows is the next phase's.

### Phase 6: Deliver, and hand over

Produces the **delivery**, one message: the desk's folder and its remote, private; git LFS where it was set up, and what the host says of its storage; the pages' address, who stops their server and how they are started again (pages.md), or that there are none; and what was not verified, said so. Then go on with the second line `console desk` printed: ask the member what they want to keep and to see here, and shape the desk to it, as the console's own skill [keeping-a-desk](skill://gh/skillcdn/console/skills/keeping-a-desk/SKILL.md) says. Its path on this machine is in that line, and `console help desk` names it.

## An agent account's desk

An agent account's desk is the same kind of thing: its own repository, wholly its own. `console agent setup` settles it before the account's first session: a desk that is there is left as it is, the one the account pushed before is cloned, and otherwise the files are written (the four and `runner.json`). Where the workspace names a git host, the setup also makes a desk it wrote a repository, on whatever branch the machine's git begins with, and sets the git of the desk it wrote or cloned to take `git.token` from the account's store when that host asks, in place of the machine's own helpers; a desk an older command wrote is no repository and has no such setting (since console 0.5.2, checked 2026-11). The account's sessions start in the desk. The git host's command is not signed in on its machine and is not signed in here: the check of the Requirements is made as step 2 hands the token (`gh auth status`, handed it). The onboarding task lists what the account then does itself, and this skill does the desk item of it and nothing else, as the account, on that task's run: its reports and decisions are working-the-board's, and a board command in the desk names the task's project (`--project <key>`).

1. Read how the desk stands first: `git status -sb` (a repository or none, its branch, a remote and what is ahead of it) and `git config --local --get-regexp '^credential'`, which lists the setting the setup made for the host, an empty value that leaves the machine's helpers out and then the command that reads the store; no value of a secret is in it. `git init -b main` where the desk is no repository yet. Then the staging and the checks of phase 4, steps 1 and 2, and a first commit where there is none, as step 3 there names it; a desk with no remote whose branch is not `main` is renamed once it has that commit (`git branch -M main`). `runner.json` is the desk's and is committed: no secret is in it.
2. The token for the git host is `git.token` in the account's store: `console secrets` lists the names it keeps, never a value. The git host's command does not ask git's setting, so the token is handed to it one command at a time and never read alone, since `console secret git.token` by itself prints it: `GH_TOKEN="$(console secret git.token)" gh <command>` in a POSIX shell; `$env:GH_TOKEN = console secret git.token; gh <command>; Remove-Item Env:GH_TOKEN` on one line in PowerShell. Never in a file, and never in the remote's address.
3. The remote, named as the onboarding task names it, private; where the task names no account, it is the token's own (`gh api user --jq .login`, handed the token). Where `gh repo view <name> --json visibility`, handed the token so, finds it, it must say `PRIVATE` before anything is pushed; else `gh repo create <name> --private --source . --remote origin`, handed the token the same way. No account or token at the git host yet, or no right to make the repository there: asked as a decision with the exact name, and the rest of the onboarding goes on meanwhile.
4. The push, `git push -u origin main`, and nothing left ahead after it. With the setting step 1 listed, git takes the token from the store itself and nothing is typed. Without it, give the desk that setting first, for the remote's host alone (`https://github.com` for a remote there) and in the desk's own configuration, from a POSIX shell (`bash`, which Git for Windows brings): `git config --local credential.https://<git host>.helper ''`, which leaves the machine's own helpers out so that none keeps a copy, then `git config --local --add credential.https://<git host>.helper '!f() { test "$1" = get && printf "username=x-access-token\npassword=%s\n" "$(console secret git.token)"; }; f'`, which reads the store each time git asks and writes nothing down. A push still refused for credentials is the token's to mend, renewed where it was made and set in the store again, or asked for as a decision; never the git host command's own helper, which the machine would keep. From then on the runner commits and pushes the desk at the end of every session.
5. A report on the run: the remote's name, that it is private, the pushed commit.

Pages, only where its manager asked for them: `console desk . --web` in the desk writes the shell, a desk written by an older command gets `web/dist/` added to its `.gitignore`, and the rest is pages.md's. What the desk keeps and shows is the account's to shape, as keeping-a-desk says.

## Verdicts

| Result | Verdict |
|---|---|
| The desk is pushed to a private remote, with nothing ahead; `work/` is ignored and no binding file is in the desk's root; the desk holds the command's files and nothing this skill wrote into them; the pages, where asked for, passed pages.md's check; the run went on to keeping-a-desk | Delivered |
| The remote waits for the member, or the git host's command is missing | Delivered locally, the commit named by its hash, with the commands that finish it |
| The pages could not be built or served | Delivered without them, the reason said |
| The remote is public, something secret is staged, or `work/` is not ignored | Not delivered: fixed first; a public remote is the member's to make private or replace |

## Hard rules

1. A desk is private: never created public, never pushed to a public remote. It is a member's own.
2. No secret in the desk: no token, key or environment file is staged, and no token is in a remote's address. A person's sign-ins stay with their git host's command and their system; an agent account's in its store in the console.
3. A desk is bound to no project and holds none: no `console use` and no `.skillcdn-console.json` in its root, since every checkout under `work/` without a binding of its own would inherit it, and `work/` stays out of its repository.
4. Nothing is created outside the machine unless the plan listed it and the user said yes, and nothing large is pushed before the member knows what the host's storage for it costs; an agent account asks as a decision what it may not do itself.
5. The desk's pages are served on this machine by `console serve` and nowhere else: never deployed, tunnelled or given a token of their own, because the server answers with the member's sign-in.
6. What a desk is for is its member's to say: this skill names no kind of thing to keep, makes no record and no page beside the empty one, and overwrites no file.

## Terminology

| Term | Meaning |
|---|---|
| Member | Whoever the `console` command is signed in as: a person, or an agent account, which is a member of its own. |
| The desk's pages | The member's own extension of the console's UI, in `web/`, served on their machine. |
