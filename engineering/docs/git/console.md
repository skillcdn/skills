# The repository and its console project

How a repository of this pack is worked through a SkillCDN Console: which console and which project, the people in it, the binding that keeps every checkout in that project and no other, the rules the project carries for its agents, the first goal and tasks, and what lives on the board and what in the repository. How a task is worked and how a board is planned are the console's own skills, working-the-board and planning-the-board, shipped with the command in folders beside each other (`console whoami` prints where); this page says what a repository adds, with the commands in the order a setup runs them: who may do what, the project's pack and the binding among them. Read when a repository is set up or bound, and when a team wonders where something belongs. The commands are the console's 0.5 line (checked 2026-11); `console help <command>` is the reference at run time, and every id and task number is read from what a command prints, never assumed, since other agents write on the same board.

## Which console

- `console whoami` says which console a command in this folder talks to; `console logins` lists every console this machine is signed in to, with the default, never a token.
- The repository works in the console the user names, else the one `whoami` talks to. One that `console logins` lists is used with `--url <origin>` on each command until the checkout is bound; from then on the binding file names it. Only a console the list lacks takes a sign-in (`console login --url <origin>`), which the person approves on the console's own pages ("Without a console").

## Which project

- A project is the work of a product or a team, and several repositories may share it (an app, its site and its tools on one board). The repository joins the project its work belongs to: the user picks it from what `console projects` lists, the one whose name or description fits the product proposed first. A new project is made only when none fits, its key a short slug of the product's name (lowercase letters, digits and hyphens, at most 40 characters, never changed once made) and its name the product's in the board's language.
- Making one is an administrator's: `console project new <key> "<name>" --description "<one line>"`, private unless `--visibility workspace` puts the whole workspace in it; whoever makes it becomes its owner. `console project <key>` answers `project.not_found` for a key that is free, and for one that is not the person's to see, so a key the command then refuses (`project.key_taken`) gets another, chosen with the person.

## Who may do what

`console whoami` prints the user's role in the workspace after their login, and `console projects` what they are in each project, so the plan knows what the user may do before it is shown.

- **An administrator** makes a project. Anyone else chooses among the projects they are in, or has an administrator make one first.
- **An owner of the project** adds a member, writes its rules, sets a goal and names its skills address. **Anyone in it** writes tasks, takes them and binds a checkout.
- Where the user does not own the project, each owner's step is a line of the plan marked as the owner's, with its command, and the run writes them as one task on the project for its owner, in the board's language: `console members --project <key>` names who, and the task is theirs with `--worker <their login> --state ready`. The run goes on with what a member may do: the binding, the setup task, the next tasks. The owner's word is that task, not a question in chat to someone who is not there, and a refusal is never worked around or asked a second time.

## The project's pack

The project reads the organization's pack unless it names a skills address of its own, and the repository's skills are read from it (agreement.md "The skills section"). Which pack that is, and whether this setup came from it:

- The pack a project reads is the address `console project <key>` prints as `skills:` and `console skills --project <key>` on its first line (`skills at <address>`); the organization's, which a new project reads, is the `skills:` line of `console workspace`.
- The pack the setup skill came from is the `Source:` line at the head of what `console skill` printed for it (`<owner>/<name>`, with the commit). It is the same pack when the address ends with that repository: nothing is to do, and the plan says so in a line.
- Another pack (the skill was loaded with `--project` of another project, through a connection of the host's, from a plugin or a copy): the skills the agreement names by path would be missing from the project's pack. The plan shows the row that holds, done on the user's word:

  | The project | What the setup does |
  |---|---|
  | New | Made reading that pack: `console project new <key> "<name>" --skills <address>` |
  | Existing, and only this repository's | Its owner names the address: `console project edit <key> --skills <address>` |
  | Shared with other repositories | Left as it is, since the address is every repository's; the agreement's Skills section names the address the skills are served at, and a host's own connection is offered (agreement.md) |

## The people

- Each teammate the user named is listed in a private project by its owner: `console member add <login> --project <key>`. The person must already be of the workspace (`console people` lists who is; `member.invalid_person` otherwise): one who is not is let in by an administrator first, which the plan names. In a project open to the workspace everyone is a member already.
- On the git host each teammate is a collaborator of a private repository, invited when the remote is made; the invitation waits for them to accept it.
- Both are actions others see, listed one per line in the plan and made only on its word.

## The binding

- `console use <key>` in the repository's root writes `.skillcdn-console.json`: the project's key and the console's address, never a token (with `--url <origin>` where the console is not the machine's default). Every `console` command run in the checkout or below it then works in that project at that console, on every machine. `--account` is not given for a file that will be committed: an account is each person's.
- A private repository commits the file, so that every clone is bound from its first command. A public repository lists it in `.gitignore`, because it names the organization's console, and each maintainer runs `console use <key>` once in their own checkout; the agreement and the README's "How we work" say so.
- `console use` prints the sentence the agreement carries. It goes at the head of the workflow section of `AGENTS.md`, word for word, so that an agent that reads the agreement before anything else is sent to the board:

  > **Bound to a console?** Before the first step, run `console whoami`: when it names a project, or `.skillcdn-console.json` is in this checkout, work the task through that SkillCDN console (`console help` says how).

- The agreement names the project by its key ("This repository works in the console project `<key>`"), so that the binding is checked against something that does not come from the binding itself. `console whoami` does the rest: it asks the console for the project, says what named it (`.skillcdn-console.json in <directory>`, `CONSOLE_PROJECT` or `--project`), and ends with `project.not_found` where the console has no such project for this person.
- A checkout is bound right when `whoami` names the agreement's key, named by the checkout's own file. Anything else (another key; the key named by a folder above the checkout or by `CONSOLE_PROJECT`; a refusal) is said to the person as `whoami` printed it, and no board work is done until they fix it. The agent never answers by naming another project itself: `--project` and `CONSOLE_PROJECT` are not used in a bound checkout, and a binding file is never copied from another repository.

## The project's rules

Before the plan, `console rules --project <key>` is read to its end: a project's own rules stand after the workspace's, and a project that has some gains a line, never a new set. For a new project, its owner writes them from the bound checkout, `console rules write --file <path>`, because the user asked for the setup and the checkpoint listed them; they add to the workspace's rules for every agent at work in the project, which reads them with each task it takes. They are in English, like everything agents read, short, and hold nothing secret. Never `--workspace`: those rules are the whole organization's. An existing project's rules are its owner's: the repository's line under "Where the work lives" is added to what is there, shown in the plan, and written only on that owner's word, the user's own where they are the owner, from the version `console rules` printed and with `--base <version>`, so that nothing else changes.

```markdown
# Rules of this project

Adds to the workspace's rules, for the agents at work here.

## Where the work lives

- The repository <owner>/<name> on <git host>: <what it holds, in a few words>. Its AGENTS.md holds inside it: how a change is checked, committed and pushed. `<check command>` before every hand-in; the commits handed in as links.

## Skills to load first

- For a task in a repository: the skills its AGENTS.md names in its Skills section, each by its path in this project's pack (`console skill <path>`).

## The pages

- What the code needs to be built, run and changed lives in the repository's docs/, never on a page. `guides/` here is for how a thing outside the code is done (an account, a service's console, a release announced); `notes/` for what was found and will be needed again. A page links to a file of the repository rather than copying it.

## Decide alone, or ask

- Alone: anything inside the task and the repository's agreement.
- Ask: a new dependency that costs money or changes the license; a change to live data; anything users would see that the task does not describe.
```

The repository's own lines replace the placeholders; a line that has nothing to say for this repository is dropped, never left as a placeholder. What the workspace's rules already say is not said again: which repository a task is for, how work found on the way is followed up, and the language of what people read on the board. A `## Reports` section is written only to name a language where the workspace's rules name none, or another for this project.

## The goal and the tasks

- **The goal.** In an existing project, the setup task joins the goal the user names (`console goals --project <key>` lists them), or none; a goal is made only when the user asks for one. In a new project, the goal is the first version, titled in the board's language from the brief ("<product>: the first version people can use", in the user's words where they gave some), written by an owner: `console goal new "<title>" --body <what reaching it means, from the brief> --state active`, with `--category` and `--due` only where the user gave them. The command prints `goal id:`.
- **The setup task** is written first and taken before the files are written, so that the run's reports, its hand-in and its finish land on it: `console task new "<set up the repository, in the board's language>" --file <body> --state ready --worker me`, with `--goal <goal id>` where there is a goal, then `console take <number>`. Its body says what to make (the layout, the agreement, the check, the binding), where (the repository by its name, the folder, the remote to be), and the milestones (the files, the push, the hand-in). Then `console report --file <path>` at the end of the files, `console hand-in <commit url> --label "<words>"`, `console finish --summary "<what was done, what is left>"`. With another run of the person's open in the project, each of these takes `--run <id>`, as `console take` says.
- **The next tasks** come from what the user said comes next and from the brief's open items (a first-version scope not yet decided is a task to decide it), one per piece a run can finish, each written with `--file`, `--state ready` (a task without it is only an idea) and `--goal <id>` where there is a goal. A body has five parts, each under a heading of its own, in the board's language: what to make, where (the repository by its name), the milestones, what to ask a person, what to read first. A category only where the workspace already keeps a fitting one (`console categories`); `--parent` only for a part of another task, since a list is not an order. A body names who decides a question only where the user said who; otherwise the question is for the person whose agent takes the task.

The board's language is layout.md's ("The languages"). The files these commands read (a task's body, the rules) are written in the system's temporary folder, never in the repository, and removed when the run ends.

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
| Whether and how a change is pushed | The agreement; the board is not asked |

A bound repository keeps no `docs/status.md` and no list of what is next in any file: kept twice, the file and the board drift. The agreement carries the binding sentence and its own lines only, never a copy of the console's rules or of the command's help, which change with the console's version.

## Without a console

The `console` command is installed with npm (`npm install -g @skillcdn/console`, on Node.js 24 or newer) and signed in with `console login --url <the console's address>`, which shows a code the person approves on the console's own pages; the console is the organization's, deployed as [its documentation](https://github.com/skillcdn/console) says. A user who has none and does not want one now gets the same layout with `docs/status.md` (three lists: done, next, open; rewritten at the end of every session) and the agreement's tracking line for a repository without a console (agreement.md "The workflow section").

## Binding later

When a console comes to a repository set up without one: the project made or chosen as above, `console use <key>`, the binding file committed or ignored, the sentence put at the head of the agreement's workflow and the tracking line replaced, the agreement's Skills section rewritten for the project's pack, what `docs/status.md` lists as next and open written as tasks, the file deleted, all in one commit (`chore(repo): work the repository through the console`).
