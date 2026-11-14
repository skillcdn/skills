# Git: what every repository of this pack shares

The skills that set up or build a repository (`git-repo-setup`, and `cloudflare-new-app`, which runs it for an app's repository) give every repository the same layout, the same working agreement, the same test structure and the same binding to a console, so that a person or an agent who has worked in one finds everything in the next. That shape lives here once, one file per topic; each skill includes the page every run reads and links the rest from the phase that reads it, and carries its own method (what it asks, where it stops, what it accepts, its rules) itself.

| Document | Holds | Read |
|---|---|---|
| [`layout.md`](layout.md) | The tree, who reads each file and when, the languages (English for everything agents read, the readers' language for the README), what the pack's other skills add later, what stays out. | When a repository is set up, and before a skill adds a file to one; included with the setup skill. |
| [`agreement.md`](agreement.md) | `AGENTS.md` section by section, `CLAUDE.md` as its import, the workflow with the binding sentence, the skills connection, the agents' settings file. | When an agreement is written or a section of it changes; included with the setup skill, linked from the new-app skill. |
| [`console.md`](console.md) | The repository's console project: which project, binding every checkout, the project's rules, the first goal and tasks, what lives on the board and what in the repository, the mistakes the shape prevents, the route without a console and binding later. | When a repository is set up or bound to a console; included with the setup skill. |
| [`readme-guide.md`](readme-guide.md) | The README: what it holds in which order, a template, how to make it good to look at, how it stays true. | When a README is written; linked from the setup skill. |
| [`testing.md`](testing.md) | The test structure: one check, three layers with a place and a name each, the defaults by stack, continuous integration. | When the check or the first test is written; linked from the setup skill. |

## Who reads this

[`git-repo-setup`](../../skills/git-repo-setup/SKILL.md) and [`cloudflare-new-app`](../../skills/cloudflare-new-app/SKILL.md), both in this area. Each declares the pages every one of its runs reads in its `skillcdn.include` by their root-relative paths, so that they arrive with the skill wherever SkillCDN serves it, and reads the others with `read_repo_file` at `engineering/docs/git/<topic>.md` through the repository or the engineering connection, or as a file at `docs/git/` of the engineering plugin. A skill of another area that writes into a repository reads layout.md before it adds a file. A change to an included page changes the served digest of the skill that includes it: edit it deliberately.

## How these pages are written

Each page says what holds now, by topic. A fact about a tool that can move (a command's flag, a host's file format) carries the month it was checked; a rule of the layout carries none, and changes when a run shows it wrong. The templates use placeholders (`<owner>`, `<key>`, `<check command>`), never a real repository, person or console.

## Adding what a run taught

A layout rule that did not hold in a real repository changes here, in the sentence it bears on. A command of the console or of the git host that behaved differently from a sentence changes that sentence, with the version and the month. What only the setup skill's method learned goes in its own `references/tool-notes.md`.
