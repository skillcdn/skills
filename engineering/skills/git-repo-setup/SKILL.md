---
name: git-repo-setup
description: "Sets up a new git repository so a team and its agents keep developing in it: the working agreement (AGENTS.md, CLAUDE.md), a README in the team's language, the documents under docs/, one check with tests and CI, and a SkillCDN console project the repository is bound to, with its rules, first goal and tasks. Use when a user says \"set up a new repo\", \"start a repository for this project\", \"make this repo ready for the team and agents\", \"connect this repo to the console\", \"레포 초기 세팅해줘\". The structure only, no app: for a new web app built and put live, cloudflare-new-app, which runs this skill for its repository; for a member's own desk, git-desk-setup. Asks what the repository is for and who works in it, shows the plan, creates the console project, the remote and the teammates' access on the user's word, commits, pushes and hands the commit in on the board. Nothing is bought."
license: MIT
compatibility: Needs a shell with git, and the runtime of the stack the repository will hold (Node.js, Python, Go, Rust) where it holds code. The console command, signed in, for the console project (recommended; without it the repository tracks its work in a file). The git host's command (gh for GitHub), signed in, to create the remote and give teammates access. Works in any agent that can run a shell and write files.
metadata:
  author: skillcdn
  version: "1.13"
  tools: git
skillcdn:
  translations:
    ko:
      title: 팀과 에이전트가 계속 개발하는 깃 저장소 초기 구성
      description: "팀과 에이전트가 세션이 바뀌어도 계속 개발할 수 있게 새 깃 저장소를 구성합니다. 작업 합의(AGENTS.md, CLAUDE.md), 팀의 언어로 쓴 README, docs/ 아래 문서, 테스트와 CI를 갖춘 하나의 검사 명령, 그리고 저장소가 묶이는 SkillCDN 콘솔 프로젝트와 그 규칙, 첫 목표, 작업까지 만듭니다. '새 레포 세팅해줘', '이 프로젝트 저장소 시작해줘', '팀이랑 에이전트가 쓰게 레포 잡아줘', '이 레포 콘솔에 연결해줘'라고 할 때 쓰세요. 앱은 만들지 않고 구조만 잡습니다. 새 웹앱을 만들어 올리는 일은 cloudflare-new-app이 하고, 그 스킬이 저장소 구성에 이 스킬을 씁니다. 구성원 자신의 데스크는 git-desk-setup이 만듭니다. 저장소의 용도와 함께 일할 사람을 묻고, 계획을 보여 주고, 사용자의 승인으로 콘솔 프로젝트, 원격 저장소, 팀원 접근을 만들고, 커밋하고 푸시하고, 커밋을 보드에 제출합니다. 구매는 없습니다."
---
# A new repository, set up for a team and its agents

What goes in: a folder (empty, freshly scaffolded, or holding code with no agreement yet) and a sentence on what the repository is for. What comes out: the repository in the layout every repository of this pack shares, committed and pushed: `AGENTS.md` as the working agreement with `CLAUDE.md` importing it, a `README.md` in the readers' language, the documents under `docs/` that let a session pick up where the last one ended, one check run by continuous integration, the teammates' access, and a console project the checkout is bound to, with its rules, its first goal and its tasks, so that the work is on the board from the first commit and every agent reads the same skills through it. No product is built: code that is there stays as it is, and nothing is written that nobody said.

## How the user is involved

- **Questions:** one message, only what the request and the folder leave open (Inputs). Everything else is derived and shown in the plan.
- **Checkpoints:** the plan (phase 2), whose message lists everything made or changed outside the machine; a public remote on its own, after the files exist; the delivery.
- **Go-ahead:** the questions with defaults are not asked and the defaults are shown in the plan; the plan still waits, because it creates things others see.
- **Changes mid-run:** a change before the files are written rewrites the plan; after, it changes the files it touches and the commit says so. A project or a remote already created is changed, not created again; a project's key never changes.

## Requirements

The tools of the compatibility line. Before the first message, `gh auth status` (without the git host's command the user creates an empty repository and gives its address) and `console whoami`, which decides how the run starts:

| `console whoami` | The run |
|---|---|
| Names no project | The usual start for a new repository: go on. The role it prints after the login says whether the user is an administrator |
| Names a project, named by the folder's own `.skillcdn-console.json` | The folder is bound already: that project is the repository's, shown in the plan instead of asked |
| Names a project, named by a `.skillcdn-console.json` in a folder above or by `CONSOLE_PROJECT` | Say so in a line and stop: a repository is not set up inside another bound checkout, and the variable would bind the new one's commands |
| Is refused | As the pack's rule on a console says: say what it printed, and do not start as if there were no console |
| No `console` command | Say what it is for and how to get it (console.md "Without a console"), and offer the route without a console, taken only on the user's word |

What every repository of this pack shares is the area's set [`engineering/docs/git/`](/engineering/docs/git/README.md), each page read before the phase that needs it:

| Page | Read before | For |
|---|---|---|
| [layout.md](/engineering/docs/git/layout.md) | The plan | The tree, who reads what, the languages |
| [console.md](/engineering/docs/git/console.md) | The plan, where a console answers | The console and the project, who may do what, the project's pack, the binding, the rules, the goal and the tasks |
| [testing.md](/engineering/docs/git/testing.md) | The plan | The check by stack, the tests, the versions |
| [agreement.md](/engineering/docs/git/agreement.md) | The files | `AGENTS.md` section by section |
| [readme-guide.md](/engineering/docs/git/readme-guide.md) | The files | The README |

A page is read the way this skill was: through a console with `console skill --file <path from the pack's root>`, through a connection of the host's with its file read, as the file at `docs/git/` of the engineering plugin, or in a checkout of the pack; each page in a call of its own, since a host hands on only so much of one call's output. Read it from the folder this skill was loaded in, or before the new folder is bound: a bound checkout reads its own project's pack, which may be another. A mount of this skill alone, or a copy of its directory, lacks the pages: fetch them from `engineering/docs/git/` of the repository this skill comes from (`github.com/skillcdn/skills` for this pack). A page that cannot be read stops the phase that needs it, said to the user; nothing of it is written from memory.

## Inputs

| Input | Source |
|---|---|
| The folder | In a member's desk, the folder `console desk` wrote (its `AGENTS.md` says whose desk it is, and it names no project): a new folder under its `work/`, once `git -C <desk> check-ignore -q work/` shows that a desk that is a repository keeps it out. Elsewhere the current directory when it is empty or the one the user names, and a new folder named after the repository when the current one holds something else |
| What the repository is for, who uses it, and what its first version does and leaves out | The request; what it leaves open is asked: "Who will use it, and what must the first version do (and leave out)? A sentence each is enough; 'not decided yet' is an answer too." What stays open is written as open in `docs/brief.md` and becomes a task |
| The repository alone, or the app too | Asked with the others when the folder is empty and the request is for a product whose code starts from a framework's scaffold: "This is a web app. Shall I set up the repository alone now, with the code scaffolded into it later, or do you want the app built too, which is the job of cloudflare-new-app? I suggest <one of them, and why>." The repository alone: the stack is still asked or derived, no skeleton is made, and the check is the content check of testing.md "By stack" |
| Who works in it, and who owns the remote | The request; asked when others are named: "What are <their> logins on GitHub and on the console? I will give them access when you approve the plan. Which account or organization at the git host should own the repository? Yours, `<login>`, unless you say another." Nobody named: the user alone, the remote under the account `gh` is signed in to. A teammate `console people` does not list is not of the workspace yet: the plan names letting them in as an administrator's step |
| The stack | Derived from the files; for an empty folder, asked only when the request does not say: "What will the code be written in? If you have no preference, I suggest <default> for <kind>." |
| The console project | Asked when a console answers: "Which console project does this repository's work belong to? <the projects `console projects` lists, the one that fits the product first>", with "Or a new one?" only for an administrator; anyone else is told there that a new project is an administrator's to make first. Several repositories may share a project; a new one is made only when none fits |
| Everything else | Derived and shown in the plan: the repository's name (the folder's, else a slug of the product's name) and the project's key (console.md "Which project"), each checked to be free (`gh repo view <owner>/<name>`, `console project <key>`) and changed where it is taken; the README's language (the user's); the remote (private); who pushes and how (directly to `main` after the check: this is the default and is not asked or advised against; through pull requests only when the user says the team reviews); the license (none for a private repository; asked for a public one); the goal and the tasks; the check |

## Workflow

Each phase produces a named artifact and ends with one line to the user.

### Phase 1: Frame

Produces the **frame**: the tools found, what the request settles, and the folder's state: empty or absent; a fresh scaffold; code without an agreement; or an agreement already there (`AGENTS.md`, `CLAUDE.md`, `docs/`), which is mapped onto the layout in the plan (which file becomes which, what moves, every rule it holds kept word for word). Nothing is moved before the plan.

### Phase 2: Plan

Produces the **plan**. Read the pages of the plan. Ask the questions of Inputs that remain, in one message. Derive the rest and show, one line each where one does:

- the repository: the name, the folder, the remote (`<owner>/<name>`, private) or the one that exists, who pushes and how;
- the people: each teammate, with the access each gets (collaborator on the remote, member of the project);
- the tree of layout.md, with the files this run writes, those it keeps, and the brief's open items;
- the check: the command, what it runs, the test it starts with (testing.md "The check"), the continuous integration job;
- the console project: the existing one the user picked, with the line its rules gain, or a new one (`<key>`, its name) with its rules, in the five things console.md gives them; the goal, where there is one, and the tasks, one line each; its pack, where this skill came from another (console.md "The project's pack");
- the steps that are the project's owner's where the user is not (console.md "Who may do what"), each marked as theirs with its command;
- what the README says, in its language, in two lines.

Checkpoint: "Here is the plan. Outside this machine, I will:", then each line that holds on a line of its own: create the console project `<key>`, or add this repository's line to the rules of `<key>`; change its skills address to `<address>`; add `<login>` to it; write the goal and `<n>` tasks; write one task for its owner, `<login>`, with the steps I may not do; create the private repository `<owner>/<name>`; add `<login>` as a collaborator; push the first commit. "OK?" One word proceeds. A public remote is asked after the files exist: "Create `<owner>/<name>` as a public repository? Everything committed becomes readable by anyone."

### Phase 3: Board

Produces the **board**, with console.md's commands in its order. First the folder: created when new, `git init -b main`. Then: the project made, or the existing one chosen; where the user owns it, the teammates added, its rules written or the repository's line added to them, and the goal for a new project; where they do not, those steps written as one task for its owner; the checkout bound (`console use <key>`) and checked with `console whoami` (hard rule 2); the setup task written and taken, so that the rest of the run reports on it; the next tasks, each naming the repository. Without a console, this phase writes nothing and `docs/status.md` takes the board's place in phase 4.

### Phase 4: Files

Produces the **repository**. Read the pages of the files. Then, in this order, each step a line to the user and, at the end of the phase, one report on the setup task:

1. The stack's skeleton, for an empty folder with a stack: the package manager's own init, and the test runner, the linter, the type checker and the runtime version file of testing.md, each at the version it says how to find. A scaffold keeps its own choices, and a file already there is kept and completed, never replaced. The repository alone of a web app skips this step and says so: its code is scaffolded in later (agreement.md "Code that arrives later").
2. The files of the root: `.gitignore` (with `.skillcdn-console.json` in it for a public repository), `.gitattributes` (`* text=auto eol=lf`), `.editorconfig`, `.env.example` where the code reads an environment.
3. The check as testing.md "The check" says, and `.github/workflows/check.yml`. Run the check until it is green; a step that cannot run on this machine is named, and so is a runtime here that is not the one the repository pins.
4. The documents of layout.md, with content from the answers and the code: `docs/README.md`, `docs/brief.md` (what was answered, and an "Open" list of what was not), `docs/architecture.md` (for an empty folder, the parts the stack implies and "nothing else yet"), `docs/decisions.md` with the setup's choices as its first lines.
5. `AGENTS.md` by agreement.md, section by section, with the binding sentence `console use` printed at the head of its workflow and its Skills section for the project's pack, and `CLAUDE.md` importing it.
6. `README.md` by readme-guide.md, in the readers' language.
7. Only where the user asked for the skills in their tools through a connection of the host's, or the plan showed it: the connection files of agreement.md "A host's own connection, on request".
8. A last read: every link resolves; every command the README and the agreement give runs as written, apart from those that need the remote; nothing is a placeholder or a fact nobody gave; every item of the brief's "Open" list names its task (`#<number>`).

A host may ask the person before an agent writes `.mcp.json`, where step 7 writes it, since it changes what agents may do in the folder. Where it refuses the write, show the person the file's content and its path, go on with the rest, and commit once they say the file is there; never write it by another route.

### Phase 5: Commit and push

Produces the **pushed repository**.

1. Commit as `chore(repo): set up the repository`.
2. Try the README's quick start from a clean clone of that commit in a temporary folder, fix what it finds before anything leaves, and remove the clone.
3. Create the remote as the plan approved, its visibility always said (`gh repo create <owner>/<name> --private --source . --remote origin`; `--public` in its place for a public one, after its own yes), and read back what it is (`gh repo view <owner>/<name> --json visibility`), add each collaborator (`gh api -X PUT repos/<owner>/<name>/collaborators/<login> -f permission=push`, which sends them an invitation), push.
4. Watch the first run of continuous integration to its result (`gh run watch <id> --exit-status`). A red run is fixed and pushed before the delivery.

Where the user keeps the remote for later, steps 3 and 4 wait: the remote is one of the next tasks, continuous integration is named as not run, and phase 6 hands nothing in, its last report naming the local commit by its hash.

### Phase 6: Hand in

Produces the **delivery**. On the board: the commit handed in on the setup task (`console hand-in <commit url> --label "<words>"`), a last report with the check and the continuous integration result, and `console finish --summary "<what was done, what is left>"`. To the user, one message: the repository's address, the tree in a few lines, the check and its result, the console project with its goal and tasks, what each teammate must accept or do (the invitation on the git host, `console login` and, for a public repository, `console use <key>` in their checkout), what waits for the project's owner or an administrator, and what was not verified, said so.

## Run by another skill

A skill that builds the product (`cloudflare-new-app`) runs this one on its project folder and hands it what its own run settled: what the product is and for whom, who works in it, the stack and its check, the README's language, the lines its Skills section gains, and whether it keeps the remote. Nothing handed is asked again, and the plan here shows only the console project and the teammates. Where the caller keeps the remote, this skill ends after phase 4 with the files written, the check green and the board set, and gives the caller the setup task's number, on which the caller reports, hands in and finishes.

## Verdicts

| Result | Verdict |
|---|---|
| The check is green locally, from a clean clone and in continuous integration; every file of the first commit holds what was said or found; the checkout is bound right (hard rule 2); the board holds the project with this repository in its rules, the setup task finished and the tasks after it | Delivered |
| The user does not own the project: what a member may do is done, and the owner's steps are one task of the owner's | Delivered, that task named |
| Continuous integration could not run (no git host command, a host without it) | Delivered, the run named as not run, its command given |
| The console was not available and the user chose to go on without it | Delivered with `docs/status.md`, saying how to bind the repository later (console.md "Binding later") |
| The check is red, or a file holds a fact nobody gave | Not delivered: fixed first |

## Hard rules

1. Every file of the repository an agent reads is in English, and `README.md` in its readers' language: agents read one language, and people read theirs.
2. The binding sentence is the one `console use` printed, copied from there word for word and never typed from memory or from the pack's rule, and the agreement names the project's key beside it: the sentence sends every agent to the console, and the key lets it see that the checkout is bound to the right project. A checkout is bound right when `console whoami` names that key, named by the checkout's own file; any other does no board work until a person fixes it or says to bind it to that key, and it is bound to no other.
3. Nothing is created or changed outside the machine unless the checkpoint listed it and the user said yes, and a public remote not without its own yes: others see it and it outlives the run. What the user may not do on the console is never worked around: it is written as a task for whoever may.
4. Nothing is invented: a document says what the user said or the code shows, and what is not known is written as open and becomes a task. An empty template or a guessed fact teaches every later agent to trust it.
5. `.env.example` carries names and safe example values only, and the binding file never a token or an account.
6. Versions come from where testing.md "Versions" says, on the day of setup, never from memory.
7. The repository does not restate the console's rules or the command's help: they come with every task and change with the console's version.

## Terminology

| Term | Meaning |
|---|---|
| Binding | The checkout's link to a console project: the project's key and the console's address in `.skillcdn-console.json`, written by `console use`. |
| Desk | A member's own repository, private and wholly theirs, whose files `console desk` writes; a project's repository set up from it lives under its `work/`. |
