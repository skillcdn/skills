---
name: git-repo-setup
description: "Sets up a new git repository so a team and its agents keep developing in it: the working agreement (AGENTS.md, CLAUDE.md), a README in the team's language, the documents under docs/, one check with tests and CI, and a SkillCDN console project the repository is bound to, with its rules, first goal and tasks. Use when a user says \"set up a new repo\", \"start a repository for this project\", \"make this repo ready for the team and agents\", \"connect this repo to the console\", \"레포 초기 세팅해줘\". The structure only, no app: for a new web app built and put live, cloudflare-new-app, which runs this skill for its repository; for a member's own desk, git-desk-setup. Asks what the repository is for and who works in it, shows the plan, creates the console project, the remote and the teammates' access on the user's word, commits, pushes and hands the commit in on the board. Nothing is bought."
license: MIT
compatibility: Needs a shell with git, and the runtime of the stack the repository will hold (Node.js, Python, Go, Rust) where it holds code. The console command, signed in, for the console project (recommended; without it the repository tracks its work in a file). The git host's command (gh for GitHub), signed in, to create the remote and give teammates access. Works in any agent that can run a shell and write files.
metadata:
  author: skillcdn
  version: "1.3"
  tools: git
skillcdn:
  include:
    - /engineering/docs/git/layout.md
  translations:
    ko:
      title: 팀과 에이전트가 계속 개발하는 깃 저장소 초기 구성
      description: "팀과 에이전트가 세션이 바뀌어도 계속 개발할 수 있게 새 깃 저장소를 구성합니다. 작업 합의(AGENTS.md, CLAUDE.md), 팀의 언어로 쓴 README, docs/ 아래 문서, 테스트와 CI를 갖춘 하나의 검사 명령, 그리고 저장소가 묶이는 SkillCDN 콘솔 프로젝트와 그 규칙·첫 목표·작업까지 만듭니다. '새 레포 세팅해줘', '이 프로젝트 저장소 시작해줘', '팀이랑 에이전트가 쓰게 레포 잡아줘', '이 레포 콘솔에 연결해줘'라고 할 때 쓰세요. 앱은 만들지 않고 구조만 잡습니다. 새 웹앱을 만들어 올리는 일은 cloudflare-new-app이 하고, 그 스킬이 저장소 구성에 이 스킬을 씁니다. 구성원 자신의 데스크는 git-desk-setup이 만듭니다. 저장소의 용도와 함께 일할 사람을 묻고, 계획을 보여 주고, 사용자의 승인으로 콘솔 프로젝트·원격 저장소·팀원 접근을 만들고, 커밋·푸시하고, 커밋을 보드에 제출합니다. 구매는 없습니다."
---
# A new repository, set up for a team and its agents

What goes in: a folder (empty, freshly scaffolded, or holding code with no agreement yet) and a sentence on what the repository is for. What comes out: the repository in the layout every repository of this pack shares, committed and pushed: `AGENTS.md` as the working agreement with `CLAUDE.md` importing it, a `README.md` in the readers' language that is good to look at, the documents under `docs/` that let a session pick up where the last one ended, one check run by continuous integration, the teammates' access, and a console project the checkout is bound to, holding the repository's rules, its first goal and its tasks, so that the work is tracked on the board from the first commit and every agent reads the same skills through it. No product is built: code that is there stays as it is, and nothing is written that nobody said.

## How the user is involved

- **Questions:** one message, only what the request and the folder leave open (Inputs). Everything else is derived and shown in the plan.
- **Checkpoints:** the plan, before any file is written or anything is created outside the machine. It lists each outside action on a line of its own (the console project, a change to its skills address, each person added to it, the remote, each collaborator, the first push), and the word on the plan confirms each line it lists. A public remote is confirmed on its own, after the files exist. The delivery.
- **Go-ahead:** the questions with defaults are not asked and the defaults are shown in the plan; the plan still waits, because it creates things others see.
- **Changes mid-run:** a change before the files are written rewrites the plan; after, it changes the files it touches and the commit says so. A project or a remote already created is changed, not created again; a project's key never changes.

## Requirements

| What | Used for |
|---|---|
| A shell with git | The repository, the commit, the push |
| The stack's runtime and package manager, where the repository holds code | The skeleton, the check |
| The `console` command, signed in | The console project, the binding, the rules, the goal and the tasks |
| The git host's command, signed in (`gh auth status` for GitHub) | Creating the remote, the collaborators, watching continuous integration; without it, the user creates an empty repository and gives its address |

Check before the first message: `git --version`; the runtime of a stack the folder or the request names; `console whoami`; `gh auth status`. What `console whoami` says decides how the run starts:

| `console whoami` | The run |
|---|---|
| Names no project | The usual start for a new repository: go on |
| Names a project, named by the folder's own `.skillcdn-console.json` | The folder is bound already: that project is the repository's, shown in the plan instead of asked |
| Names a project, named by a `.skillcdn-console.json` in a folder above or by `CONSOLE_PROJECT` | Say so in a line and stop: a repository is not set up inside another bound checkout, and the variable would bind the new one's commands |
| Is refused | As the pack's rule on a console says: say what it printed, and do not start as if there were no console |
| No `console` command | Say what it is for and how to get it (console.md "Without a console"), and offer the route without a console, taken only on the user's word |

Without git, stop and say what to install. A console the user names that is not the one `whoami` talks to is found in `console logins` (console.md "Which console").

What every repository of this pack shares is the area's document set [`engineering/docs/git/`](/engineering/docs/git/README.md). [layout.md](/engineering/docs/git/layout.md) (the tree, who reads what, the languages) is included and arrives with this skill wherever SkillCDN serves it. The others are read when their phase comes: [console.md](/engineering/docs/git/console.md) (the console project, its commands, the binding) before the plan, and [agreement.md](/engineering/docs/git/agreement.md), [testing.md](/engineering/docs/git/testing.md) and [readme-guide.md](/engineering/docs/git/readme-guide.md) in phase 4. A linked page is read the way this skill was: through a console with `console skill --file <path from the pack's root>`, through a connection of the host's with its file read (`read_repo_file`), as the file at `docs/git/` of the engineering plugin, or as the file in a checkout of the pack. A mount of this skill alone lacks the four linked pages and a copy of its directory all five: say so in the first message, fetch them from `engineering/docs/git/` of the repository this skill comes from (`github.com/skillcdn/skills` for this pack) where the agent can, and otherwise run on this skill's own files, which carry its workflow and its rules.

## Inputs

| Input | Source |
|---|---|
| The folder | In a member's desk (a folder whose `AGENTS.md` says it is their desk; it names no project), a new folder under its `work/`, which the desk keeps out of its own repository. Elsewhere the current directory when it is empty or the one the user names, and a new folder named after the repository when the current one holds something else. Without a desk nothing else differs |
| What the repository is for, who uses it, and what its first version does and leaves out | The request; what it leaves open is asked: "Who will use it, and what must the first version do (and leave out)? A sentence each is enough; 'not decided yet' is an answer too." What stays open is written as open in `docs/brief.md` and becomes a task |
| Who works in it | The request; asked when others are named without their accounts: "What are <their> logins on GitHub and on the console? I will give them access when you approve the plan." Nobody named: the user alone |
| The stack | Derived from the files (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, a framework's configuration); for an empty folder, asked only when the request does not say: "What will the code be written in? If you have no preference, I suggest <default> for <kind>." |
| The console project | Asked when a console answers: "Which console project does this repository's work belong to? <the projects `console projects` lists, the one that fits the product first> Or a new one?" Several repositories may share a project; a new one is made only when none fits |
| Everything else | Derived and shown in the plan: the repository's name and the project's key (below), the board's language, the README's language (the user's), the remote (private, under the git host account `gh` is signed in to), who pushes and how (directly to `main` after the check, or through pull requests when the user says the team reviews), the license (none for a private repository; asked for a public one), the first goal and its tasks, the check |

**The name.** The folder's name when the user opened or named one; otherwise the product's name, or two or three English words of its purpose, as a slug of lowercase letters, digits and hyphens of at most 40 characters. A new project's key and name are chosen as console.md "Which project" says. Before the plan, check that what is to be made is free: `gh repo view <owner>/<name>` answers not found, and for a new project `console project <key>` answers `project.not_found`; a taken one gets another slug, shown in the plan.

## Workflow

Each phase produces a named artifact and ends with one line to the user. Working files for the board (a task's body, the rules) are written in the system's temporary folder, never in the repository, and removed when the run ends.

### Phase 1: Frame

Produces the **frame**: the tools found, the folder's state, and what the request settles.

1. Run the checks of Requirements.
2. Read the folder: empty or absent; a fresh scaffold (a framework's files, its first commit); code without an agreement; or an agreement already there (`AGENTS.md`, `CLAUDE.md`, `docs/`). Read the stack's manifest, its scripts, its test runner, the remote (`git remote -v`) and the default branch.
3. When an agreement is there, map it onto the layout: which file becomes which, what moves, what is kept word for word (every rule it holds). Nothing is moved before the plan.
4. When the request is for a product whose code starts from a framework's scaffold (a web app, a mobile app) and the folder is empty, say in a line that the code comes from the scaffold and that `cloudflare-new-app` builds a web app and sets its repository up with this skill. On the user's word for the repository alone, the repository holds the layout and the documents now, its check is the content check of testing.md "By stack", and the code is scaffolded into it later (agreement.md "Code that arrives later").

### Phase 2: Plan

Produces the **plan**. Read [console.md](/engineering/docs/git/console.md) where a console answers. Ask the questions of Inputs that remain, in one message. Derive the rest, run the name checks, and show, one line each where one does:

- the repository: the name, the folder, the remote (`<owner>/<name>`, private) or the one that exists, who pushes and how;
- the people: each teammate, with the access each gets (collaborator on the remote, member of the project);
- the tree of layout.md, with the files this run writes, those it keeps, and the brief's open items;
- the check: the command, what it runs, the test it starts with (testing.md "The check"), the continuous integration job;
- the console project: the existing one the user picked, with the line its rules gain, or a new one (`<key>`, its name) with its rules (console.md "The project's rules"); the goal, where there is one, and the tasks, one line each;
- the skills: the project's pack, read through the console. Where the repository `console skills --project <key>` names (for a new project, `console skills` in a folder that names none) is the `Source` this skill was loaded under, a line says so; where it is another, the row of agreement.md "The skills section" that holds;
- what the README says, in its language, in two lines.

Checkpoint: "Here is the plan. Outside this machine, I will: create the console project `<key>` (or: add this repository to the rules of `<key>`); add <login> to it; create the private repository `<owner>/<name>`; add <login> as a collaborator; push the first commit. OK?" One word proceeds. A public remote is asked after the files exist: "Create `<owner>/<name>` as a public repository? Everything committed becomes readable by anyone."

### Phase 3: Board

Produces the **board**, as console.md says, with the commands it gives. First the folder: created when new, `git init -b main`. Then: the project made, or the existing one chosen; the teammates added; the checkout bound (`console use <key>`) and `console whoami` checked to name that key, named by the new folder's own `.skillcdn-console.json`; the project's rules written for a new project, or the repository's line added to an existing project's on its owner's word; the goal, for a new project; the setup task written and taken, so that the rest of the run reports on it; the next tasks, each naming the repository. Each id and number is read from the command's output. Without a console, this phase writes nothing and `docs/status.md` takes the board's place in phase 4.

### Phase 4: Files

Produces the **repository**, in this order, each step a line to the user and, at the end of the phase, one report on the setup task:

1. The stack's skeleton, for an empty folder with a stack: the package manager's own init, the test runner, the linter and the type checker of [testing.md](/engineering/docs/git/testing.md) "By stack", the runtime version file, each at the version testing.md "Versions" says how to find. A scaffold keeps its own choices, and a file already there is kept and completed, never replaced.
2. The files of the root: `.gitignore` (the stack's, the secret files, the build output, and `.skillcdn-console.json` for a public repository), `.gitattributes` (`* text=auto eol=lf`), `.editorconfig`, `.env.example` where the code reads an environment, `.claude/settings.json` (agreement.md).
3. The check as testing.md "The check" says, and `.github/workflows/check.yml`. Run the check until it is green; a step that cannot run on this machine is named.
4. The documents of layout.md, with content from the answers and the code: `docs/README.md`, `docs/brief.md` (what was answered, and an "Open" list of what was not), `docs/architecture.md` (for an empty folder, the parts the stack implies and "nothing else yet"), `docs/decisions.md` with the setup's choices as its first lines.
5. `AGENTS.md` by [agreement.md](/engineering/docs/git/agreement.md), section by section, with the binding sentence at the head of its workflow and its Skills section for the project's pack, and `CLAUDE.md` importing it.
6. `README.md` by [readme-guide.md](/engineering/docs/git/readme-guide.md), in the readers' language.
7. Only where the user asked for the skills in their tools through a connection of the host's, or the plan showed it: the connection files of agreement.md "A host's own connection, on request".
8. A last read: every link resolves; every command the README and the agreement give runs as written, apart from those that need the remote; nothing is a placeholder or a fact nobody gave; every item of the brief's "Open" list names its task (`#<number>`); nothing secret is staged (`git status`, `git diff --cached --stat`).

Claude Code asks the person before an agent writes `.claude/settings.json` (and `.mcp.json`, where step 7 writes it), since they change what agents may do in the folder; the plan says the tool will ask. A session that cannot ask (a headless or scheduled run) is refused the write: the agent shows the person each file's content and the path, goes on with the rest, and commits once the person says the files are there; it never writes them by another route.

### Phase 5: Commit and push

Produces the **pushed repository**.

1. Commit as `chore(repo): set up the repository`, the body naming what the layout holds.
2. Try the quick start from a clean clone of that commit (`git clone <folder> <temporary folder>`, then the README's install and check), and fix what it finds before anything leaves.
3. Create the remote as the plan approved (`gh repo create <owner>/<name> --private --source . --remote origin`), add each collaborator (`gh api -X PUT repos/<owner>/<name>/collaborators/<login> -f permission=push`, which sends them an invitation), push.
4. Watch the first run of continuous integration to its result: `gh run list --workflow check.yml --limit 1 --json databaseId,status` until it appears, then `gh run watch <id> --exit-status`, whose exit status says green or red. A red run is fixed and pushed before the delivery.

Where the user keeps the remote for later, steps 3 and 4 wait: the remote is one of the next tasks, continuous integration is named as not run, and phase 6 hands nothing in, its last report naming the local commit by its hash.

### Phase 6: Hand in

Produces the **delivery**. On the board: the commit handed in on the setup task (`console hand-in <commit url> --label "<words>"`), a last report with the check and the continuous integration result, and `console finish --summary "<what was done, what is left>"`. To the user, one message: the repository's address, the tree in a few lines, the check and its result, the console project with its goal and tasks, what each teammate must accept or do (the invitation on the git host, `console login` and, for a public repository, `console use <key>` in their checkout), and what was not verified, said so.

## Run by another skill

A skill that builds the product (`cloudflare-new-app`) runs this one on its project folder, as the pack's rule on skills that chain says, and hands it what its own run settled: what the product is and for whom, who works in it, the stack and its check, the README's language, the lines its Skills section gains, and whether it keeps the remote for a later step of its own. Then nothing it handed is asked again, its plan's word covers what it showed, and the plan here shows only the console project and the teammates. Where the caller keeps the remote, phases 5 and 6 are the caller's: this skill ends after phase 4 with the files written, the check green and the board set, and gives the caller the setup task's number, on which the caller reports, hands in and finishes.

## Verdicts

| Result | Verdict |
|---|---|
| The check is green locally, from a clean clone and in continuous integration; every file of the first commit holds what was said or found; the binding sentence and the project's key are in `AGENTS.md`, and `console whoami` in the checkout names that key, named by the checkout's own file; the board holds the project with this repository in its rules, the setup task finished and the tasks after it | Delivered |
| Continuous integration could not run (no git host command, a host without it) | Delivered, the run named as not run, its command given |
| The console was not available and the user chose to go on without it | Delivered with `docs/status.md`, saying how to bind the repository later (console.md "Binding later") |
| The check is red, or a file holds a fact nobody gave | Not delivered: fixed first |

## Hard rules

1. Every file of the repository an agent reads is in English, and `README.md` in its readers' language: agents read one language, and people read theirs.
2. The binding sentence is copied word for word, and the agreement names the project's key beside it: the sentence sends every agent to the console, and the key lets it see that the checkout is bound to the right project. A checkout whose `console whoami` names another project, or one named from outside the checkout, does no board work until a person fixes it.
3. Nothing is created or changed outside the machine (a console project or its skills address, a member, a remote, a collaborator, a push) unless the plan listed it and the user said yes, and a public remote not without its own yes: others see it and it outlives the run.
4. Nothing is invented: a document says what the user said or the code shows, and what is not known is written as open and becomes a task. An empty template or a guessed fact teaches every later agent to trust it.
5. A secret is never read, printed or committed: `.env.example` carries names and safe example values only, and the binding file never a token or an account.
6. Versions come from where testing.md "Versions" says, on the day of setup, never from memory.
7. The repository does not restate the console's rules or the command's help: they come with every task and change with the console's version.

## Terminology

| Term | Meaning |
|---|---|
| Binding | The checkout's link to a console project: the project's key and the console's address in `.skillcdn-console.json`, written by `console use`. |
| Binding sentence | The sentence at the head of the agreement's workflow that sends every agent through the console. |
| Setup task | The task on the board that holds this run's reports, its hand-in and its finish. |
| Board's language | The language of what people read on the console (tasks, the goal, the project's name and description, reports, hand-in labels): the one the workspace's rules name (`console rules` prints them), else the user's. The project's rules, like every file an agent reads, are in English. |
| Desk | A member's own folder for their agent's work, written by `console desk`; a repository made from it lives under its `work/`. |
