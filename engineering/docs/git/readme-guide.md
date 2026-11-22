# The README: for people, in their language, good to look at

`README.md` is the one file of the repository written for people rather than for agents: whoever opens the repository on the git host, a new teammate, a user, a reviewer. It is written in the language of the people who will read it (the user's language unless they name another), while every file agents read is in English (layout.md). Read when a repository's README is written or rewritten.

## What it holds

In this order, each section only when the repository has something to put in it:

1. **The header.** The name, one line on what it does and for whom, the badges, and the picture where the product has a mark.
2. **What it is.** Two or three sentences: the problem, who it is for, what it does about it. Then a screenshot or a short animated capture once the product has a screen; never a placeholder picture.
3. **Quick start.** What to install first (the runtime and the package manager, with the versions the repository pins), then the commands to install, set the local configuration (copy `.env.example`, which values to fill and where they come from, never a value), run, and check. Every command copyable as it is.
4. **What is inside.** A short tree of the top folders, one line each; the full map is the agreement's.
5. **How we work.** Three lines: the working agreement is `AGENTS.md` (for agents and people alike); tasks, decisions and the plan are on the console project `<key>` (in a public repository, "the team's console project", with no key; or `docs/status.md` where there is no console); the documents start at `docs/README.md`. How a newcomer joins: clone, sign in to the console and, in a public repository, bind the checkout (console.md "The binding"); where the repository declares a connection for the skills, approve it when their tool asks.
6. **License**, or a line that the repository is private and its terms are the owner's.

What stays out: rules for changing the code (the agreement's), the architecture (`docs/architecture.md`), history and changelogs (git's), the team's internal reasoning, and anything secret. A README that restates the agreement goes stale twice.

## The template

The shape, with the words written in the readers' language; `<>` marks what the repository fills:

````markdown
<div align="center">

<img src="docs/assets/logo.svg" alt="<name>" width="88">

# <Name>

**<What it does, for whom, in one line>**

[![check](https://github.com/<owner>/<repo>/actions/workflows/check.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/check.yml)
[![license](https://img.shields.io/badge/license-<license>-blue)](LICENSE)

</div>

<Two or three sentences: the problem, who it is for, what this does about it.>

<p align="center"><img src="docs/assets/screenshot.png" alt="<what the screen shows>" width="720"></p>

## Quick start

```bash
<install command>
cp .env.example .env.local
<run command>
```

| Command | What it does |
|---|---|
| `<check command>` | Everything a commit must pass |
| `<dev command>` | The local server at `http://localhost:<port>` |

## What is inside

```
src/      <one line>
tests/    <one line>
docs/     how it is built and why
```

## How we work

- The working agreement for agents and people: [AGENTS.md](AGENTS.md)
- Tasks and decisions: the console project `<key>`
- Documents: [docs/README.md](docs/README.md)

## License

<license line>
````

## Making it look good

- **One centered header.** The name as the only level-one heading, the line under it in bold, the badges on one line. On GitHub, Markdown inside `<div align="center">` renders only with a blank line after the opening tag and before the closing one.
- **Few badges, each true.** The check's status and the license; a version or a live address where there is one. Four at most: a wall of badges reads as noise, and a badge for something the repository does not do is a lie. A private repository's status badge needs a token to show, so it is left out there.
- **A picture early.** A product with a screen shows it right after the opening sentences, at a real width (720 px or less, so it does not overflow), with words in `alt` that say what it shows. The pictures live in `docs/assets/`. A command-line tool shows a short session as a code block instead.
- **Commands that run when copied**: one per line, no prompt sign, and a value the reader fills written `<like-this>`.
- **Two screens at most.** What is longer belongs in `docs/` and is linked.
- **Links relative** to the repository, so that they work on every branch and in every fork.
- **The readers' language as its readers write it**; code, commands, file names and identifiers stay as they are in the code.

## Keeping it true

The agreement's documentation protocol names the README for what it holds: a new command people run, a change to the quick start, a new requirement, a new screen worth showing. The quick start is tried from a clean clone before the README says it works; a step not tried is left out of the README until it is.

A repository that is itself a pack in the SkillCDN Format (a `SKILLCDN.md` at its root, as a studio has) lists its skills in a table nobody keeps by hand: `npx @skillcdn/cli@latest catalog --write README.md` writes it between `<!-- skillcdn:catalog -->` and `<!-- /skillcdn:catalog -->`, each skill's name linked to its `SKILL.md` with the first sentence of its description, and `npx @skillcdn/cli@latest catalog --check README.md` in the check fails when the table and the pack have parted ([writing a pack](skill://gh/skillcdn/skillcdn/docs/guide/write-a-repository.md), `docs/guide/write-a-repository.md` of `github.com/skillcdn/skillcdn`; SkillCDN 0.6, checked 2026-11).
