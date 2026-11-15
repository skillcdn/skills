# Git skills

How the skills that set up or build a repository are written and kept in step, for authors. What every repository of the pack shares at run time is the document set [`engineering/docs/git/`](../../engineering/docs/git/README.md), which agents read; this page says what goes there, what stays in a skill, and how the family is tested.

## The tool is git, the git host and the console

The skills drive git in a shell, the git host's command for what only the host does (`gh` for GitHub: creating the remote, watching a run of continuous integration), and the SkillCDN Console's `console` command for the board the repository is worked through. They name git's commands exactly, because those are stable; they name `gh` and `console` commands with the version and the month they were checked, and point at `<command> help` as the reference at run time, because both move. A stack's tools (a test runner, a linter) are named as defaults with the way to find the current version; a framework's own choices win.

## What is shared and what stays in the skill

| In `engineering/docs/git/` | In the skill |
|---|---|
| `layout.md`: the tree, who reads what, the languages, what other skills add later | What the skill asks, in which words, and what it derives |
| `agreement.md`: `AGENTS.md` section by section, the binding sentence, the skills section (the project's pack through the console; a host's own connection on request), the agents' settings | The order of the phases, its stops, its verdicts |
| `console.md`: the project, the binding, the project's rules, the first goal and tasks, what lives where | How the setup task is written and taken, and what is handed in |
| `readme-guide.md`, `testing.md`: the README and the test structure | What a skill that builds adds to them (a web app's sections, its rules, its secret files) |

The test for a sentence: would it hold for every repository the pack makes, whatever it holds? Then it belongs in the set. A sentence that holds for one kind of product (a web app's localization section, a deploy record) stays in the skill that builds that product, in the reference that says what it adds to the shared shape, as `cloudflare-new-app`'s `references/working-agreement.md` does.

The set sits in the area's `docs/` because the skills that read its pages are engineering skills; neither includes one, so that each stays within what a command prints whole (`guide/skill-authoring.md`, on size). A skill of another area that writes into a repository (a document, a design file kept in git) reads `layout.md` through the repository connection before it adds a file, and adds its file to the layout's "What grows later" table in the same change.

## How the set's pages are written and kept

Each page says what holds now, by topic. A fact about a tool that can move (a command's flag, a host's file format) carries the month it was checked; a rule of the layout carries none, and changes when a run shows it wrong. The templates use placeholders (`<owner>`, `<key>`, `<check command>`), never a real repository, person or console. What a run taught goes into the sentence it bears on: a layout rule that did not hold in a real repository, a command of the console or of the git host that behaved differently, with the version and the month. What only the setup skill's method learned goes in its own `references/tool-notes.md`. None of this is in the set's own README, which a run may read.

## The desk skill

`git-desk-setup` makes a member's own desk a repository. The desk's files, the format of its records (the desk's own `records/README.md`) and its dashboard's shell are the console's, written by `console desk` and `console agent setup`, so the skill carries only its method (what it asks, the checks before the first commit, the private remote) and one reference for the dashboard, which a person's phase links and an agent account's run never reads; it reads none of the set, since a desk has no layout of the pack's and is bound to no project. What the console's command prints and writes changes with its version: the skill names the command and what it is for, and quotes of its output only the sentence it prints for a person to say to their agent, which is how a request for the skill arrives.

## Keeping every repository the same

- One layout. A skill that adds a file to a repository (`DEPLOY.md`, `docs/payments.md`) names it in `layout.md` "What grows later", so that the map of every repository can say what each file is.
- One agreement. A skill never writes a rule into `CLAUDE.md`; it adds to the section of `AGENTS.md` that agreement.md names, in English.
- One console shape. The binding sentence is the console's, copied as it is from `skills/working-the-board/references/the-sentence.md` of the console's repository; a release that changes it changes `console.md` and `agreement.md` in the same review, and the setup skill's version. How a task is worked, a board planned and an agent account run are the console's own skills, shipped with its command: the set says what a repository adds and points there, and a sentence that restates the console's rules or the command's help is cut, since both change with the console's version.
- One way to the skills. The pack is read through the console (`console skills`, `console skill <path>`), which needs nothing connected and reads a private pack with the project's token; the set writes a host's own connection only as the alternative a user asks for.

## Testing the family

The setup skill is exercised from a fresh session on an empty folder, with a console the run may write to: one private test project the tester keeps for every run, on a console where they are an administrator (the console deletes no project, so a project per run would stay in the list), its tasks archived afterwards, and no remote, or a private remote deleted afterwards. A headless run stops where the host asks a person before writing its own settings files (`engineering/docs/skillcdn/fresh-agents.md`), and the tester writes them. The run is read for the files against the layout, the check's result, the binding (`console whoami` in the new checkout names the key and says the checkout's own file named it), the project's rules, goal and tasks as written, the setup task's reports, hand-in and finish, and the language of every file. A run on a fresh scaffold, and the new-app skill's phase 5 running it, are the second and third cases. What a run taught about a command goes into the sentence of the set it bears on, with the version and the month. The desk skill is exercised from a fresh session in a folder `console desk` wrote, as a person signed in to a console, with a private remote deleted afterwards or none, once with the dashboard and once without; and as an agent account in the desk its setup wrote, on its onboarding task.
