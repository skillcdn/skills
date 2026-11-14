# The repository and its console project

How a repository of this pack is worked through a SkillCDN Console: the console and the project it works in, the people in it, how every checkout is bound to that project and never another, the rules the project carries for its agents, the first goal and tasks, what lives on the board and what in the repository, and the mistakes this shape prevents. The console's own skill working-the-board, shipped with the command (`console whoami` prints where), says how a task is worked; this page says what a repository adds. Read when a repository is set up or bound, and when a team wonders where something belongs. The commands are the console's 0.5 line (checked 2026-11); `console help <command>` is the reference at run time, and every id and task number is read from what a command prints, never assumed, since other agents write on the same board.

## Which console

- A machine may be signed in to several consoles, one of them the default. `console whoami` says which one a command in this folder talks to; `console logins` lists every console signed in here, with the account and the default, never a token.
- The repository works in the console the user names, else the one `whoami` talks to. One that `console logins` lists is used with `--url <origin>` on each command until `console use <key> --url <origin>` binds the checkout; from then on the binding file names it, and no flag is needed. Only a console the list lacks takes a sign-in (`console login --url <origin>`), which the person approves on the console's own pages ("Without a console").

## Which project

- A project is the work of a product or a team, and several repositories may share it (an app, its site and its tools on one board). The repository joins the project its work belongs to: the user picks it from what `console projects` lists, the one whose name or description fits the product proposed first. A new project is made only when none fits, its key a short slug of the product's name (lowercase letters, digits and hyphens, at most 40 characters, never changed once made) and its name the product's in the board's language.
- In a project several repositories share, every task names the repository it is about in its body, and the project's rules list each repository under "Where the work lives" with what it holds.
- `console project <key>` answers `project.not_found` for a key that is free. Making one is an administrator's: `console project new <key> "<name>" --description "<one line>"`, private unless `--visibility workspace` puts the whole workspace in it; whoever makes it becomes its owner. A person who is not an administrator is told so, and either an administrator makes it or an existing project is chosen; a refusal is never worked around, and `project.key_taken` means another key, chosen with the person.
- The project reads the organization's pack unless `--skills <address>` names another; it is left so. The skills the repository itself works with are its own connection, which `AGENTS.md` names, and the project's rules send agents there.

## The people

- Each teammate the user named is listed in a private project by its owner: `console member add <login> --project <key>`. The person must already be of the workspace (`member.invalid_person` otherwise): one who is not is invited by an administrator first, which the plan names as the user's step. In a project open to the workspace everyone is a member already.
- On the git host each teammate is a collaborator of a private repository, invited when the remote is made (the setup skill's phase 5); the invitation waits for them to accept it.
- Both are actions others see, listed one per line in the plan and made only on its word.

## The right project, in every checkout

The command works in the project `--project <key>` names, else the one `CONSOLE_PROJECT` names in the environment, else the one in `.skillcdn-console.json` of the working directory or the nearest directory above it. A checkout works in the wrong project when one of the first two is set, when it has no binding of its own and a folder above it does, or when a task of another repository of the same project is worked in it. The shape below closes each way.

- `console use <key>` in the repository's root writes `.skillcdn-console.json`: the project's key, and the console's address or the account only where this machine needs them; never a token. Every `console` command run in the checkout or below it then works in that project.
- A private repository commits the file, so that every clone is bound from its first command; the committed file holds the key and, where the team's console is not everyone's default login, its address, and never an `account`, which is each person's (remove that key before committing). A public repository lists the file in `.gitignore`, because it names the organization's console, and each maintainer runs `console use <key>` once in their own checkout; the README's "How we work" says so.
- `console use` prints the sentence the agreement carries. It goes at the head of the workflow section of `AGENTS.md`, word for word, so that an agent that reads the agreement before anything else is sent to the board:

  > **Bound to a console?** When `.skillcdn-console.json` is in this checkout, or `console whoami` names a project, work the task through that SkillCDN console (`console help` says how).

- The agreement names the project by its key ("This repository works in the console project `<key>`"), so that the binding can be checked against something that does not come from the binding itself.
- Before the first board command of a session, `console whoami` names that key. No project named, in a public repository's fresh checkout: `console use <key>` with the agreement's key, said in a line. Another project named: something above the checkout decides (`CONSOLE_PROJECT`, `--project` in a script or an alias, a binding file of a folder above), and the agent says which and works no further on the board until the person fixes it; it never answers by setting another project itself.
- `--project` and `CONSOLE_PROJECT` are never used in the checkout, and a binding file is never copied from another repository.
- A task whose body names another repository of the project is not worked in this checkout: the agent says so and points to that repository.

## The project's rules

For a new project, its owner writes them from the bound checkout, `console rules write --file <path>`, because the user asked for the setup and the plan named them; they add to the workspace's rules for every agent at work in the project, which reads them with each task it takes. They are in English, like everything agents read, short, and hold nothing secret. Never `--workspace`: those rules are the whole organization's. An existing project's rules are its owner's: the repository's line under "Where the work lives" (and the line that a task names its repository, where the rules lack it) is added to what is there, shown in the plan, and written only on that owner's word, the user's own where they are the owner, from the version `console rules` printed and with `--base <version>`, so that nothing else changes.

```markdown
# Rules of this project

Adds to the workspace's rules, for the agents at work here.

## Where the work lives

- The repository <owner>/<name> on <git host>: <what it holds, in a few words>. Its AGENTS.md holds inside it: how a change is checked, committed and pushed. `<check command>` before every hand-in; the commits handed in as links.
- A task names the repository it is about in its body; it is worked only in a checkout of that repository.

## Skills to load first

- The skills the repository's AGENTS.md names in its Skills section, for any task in the repository.

## The pages

- What the code needs to be built, run and changed lives in the repository's docs/, never on a page. `guides/` here is for how a thing outside the code is done (an account, a service's console, a release announced); `notes/` for what was found and will be needed again. A page links to a file of the repository rather than copying it.

## Decide alone, or ask

- Alone: anything inside the task and the repository's agreement.
- Ask: a new dependency that costs money or changes the license; a change to live data; anything users would see that the task does not describe.

## Reports

- In <the board's language>, at the milestones the task names and when a check fails.
```

The board's language is the one the workspace's rules name for what people read, else the user's. The repository's own lines replace the placeholders; a line that has nothing to say for this repository is dropped, never left as a placeholder.

## The goal and the tasks

- **The goal.** In an existing project, the setup task joins the goal the user names, or none; a goal is made only when the user asks for one. In a new project, the goal is the first version, titled in the board's language from the brief ("<product>: the first version people can use", in the user's words where they gave some), written by an owner: `console goal new "<title>" --body <what reaching it means, from the brief> --state active`, with `--category` and `--due` only where the user gave them. The command prints `goal id:`.
- **The setup task** is written first and taken before the files are written, so that the run's reports, its hand-in and its finish land on it: `console task new "<set up the repository, in the board's language>" --file <body> --state ready --worker me`, with `--goal <goal id>` where there is a goal, then `console take <number>`. Its body says what to make (the layout, the agreement, the check, the binding), where (the repository by its name, the folder, the remote to be), and the milestones (the files, the push, the hand-in). Then `console report --file <path>` at the end of the files, `console hand-in <commit url> --label "<words>"`, `console finish --summary "<what was done, what is left>"`. With another run of the person's open in the project, each of these takes `--run <id>`, as `console take` says.
- **The next tasks** come from what the user said comes next and from the brief's open items (a first-version scope not yet decided is a task to decide it), one per piece a run can finish, each written with `--file`, `--state ready` (a task without it is only an idea) and `--goal <id>` where there is a goal. A body has five short parts, in the board's language: what to make, where (the repository by its name, the folder), the milestones, what to ask a person, what to read first. A category only where the workspace already keeps a fitting one (`console categories`); a missing one is proposed to an administrator, never made unasked. A list is not an order: `--parent` only for a part of another task. The planning skill shipped with the command, planning-the-board, holds the console's own guidance for a task.

The files these commands read (a task's body, the rules) are written in the system's temporary folder, never in the repository, and removed when the run ends.

## What lives where

| What | Where |
|---|---|
| The work to do, its order and days, who is on it | Tasks and goals on the project |
| A choice a person must make | A decision on the board, asked with `console ask` |
| What was done in a session, the check that ran, what is left | The run's reports and its finish, on its task |
| What the code needs to be built, run and changed | The repository: `AGENTS.md`, `docs/`, next to the code |
| Why a choice was made that someone might undo | `docs/decisions.md` in the repository |
| How something outside the code is done; what was found | The project's pages, `guides/` and `notes/` |
| The commits a task made | Handed in on the task, as links |

## The mistakes this shape prevents

| Mistake | What prevents it |
|---|---|
| An agent works in the repository and the board never hears of it | The binding file committed (private) or bound once per checkout (public), and the sentence first in the agreement's workflow |
| Work asked in chat is done with no task | The agreement: a change that is not yet a task is written as one before it is made |
| What is next is kept twice, in a file and on the board, and the two drift | No `docs/status.md` in a bound repository |
| A follow-up found mid-task is lost | A new task, never a line in a document; a `TODO` in the code names its task, `TODO(#<number>)` |
| A page on the board copies a document of the repository and goes stale | The project's rules: a page links, the repository holds what the code needs |
| A reviewer cannot tell which commits a task made | The commits handed in as links on the task |
| The board is asked whether to push | The agreement says how a change is pushed; the console's rules leave that to it |
| Two tasks at once on one machine, reports landing on the wrong run | One task per checkout or worktree, as the agreement's "Working alongside others" says |
| A teammate's committed binding names someone else's account | The committed file holds no `account` |
| A checkout works in a project other than its own: an environment variable, a script's `--project`, a folder above bound elsewhere | The agreement names the key, `console whoami` is checked against it before the first board command, and a mismatch stops the board work until a person fixes it |
| A task of one repository is worked in another that shares the project | Every task names its repository; a checkout works only the tasks that name it |
| A rule of the board copied into the agreement drifts from the console's | The agreement carries the sentence and its own lines only |

## Without a console

The `console` command is installed with npm (`npm install -g @skillcdn/console`, on Node.js 24 or newer) and signed in with `console login --url <the console's address>`, which shows a code the person approves on the console's own pages; the console is the organization's, deployed as [its documentation](https://github.com/skillcdn/console) says. A user who has none and does not want one now gets the same layout with `docs/status.md` (three lists: done, next, open; rewritten at the end of every session) and the agreement's tracking line for a repository without a console (agreement.md "The workflow section").

## Binding later

When a console comes to a repository set up without one: the project made or chosen as above, `console use <key>`, the binding file committed or ignored, the sentence put at the head of the agreement's workflow and the tracking line replaced, what `docs/status.md` lists as next and open written as tasks, the file deleted, all in one commit (`chore(repo): work the repository through the console`).
