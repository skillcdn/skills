# The layout every repository of this pack has

The files and folders a repository set up with this pack's skills carries from its first commit, who reads each, the language each is written in, and what the pack's other skills add later. The same layout in every repository means a person or an agent who has worked in one finds everything in the next, and nothing about how the work is done has to be explained twice. Read when a repository is set up, and before a skill adds a file to one.

## The tree

```
README.md              people: what it is, quick start, how we work           readers' language
AGENTS.md              the working agreement, for every agent and person       English
CLAUDE.md              one import of AGENTS.md, nothing else                   English
docs/
  README.md            the map of the documents: each file, its use, when it changes
  brief.md             what is built, for whom, scope and non-goals, the domain's words
  architecture.md      how it is built now: parts, data, boundaries, outside services, main flows
  decisions.md         one dated line per decision, with its reason
  guides/<topic>.md    how a thing is done here, added the first time it is needed
  assets/              the pictures the README and the documents show
<code>                 the stack's own layout (src/, app/, cmd/, a package per folder)
tests/ or beside code  per testing.md
e2e/                   end-to-end journeys, where the product has a screen or a client
.github/workflows/check.yml    the check on every push and pull request
.claude/settings.json  secret files denied to agents; the check and read-only commands allowed
.mcp.json  .cursor/mcp.json  .codex/config.toml    the skills connection
.gitignore  .gitattributes  .editorconfig  .env.example  <runtime version file>  <the stack's configuration files>
.skillcdn-console.json the console binding (console.md says when it is committed)
```

Everything in `docs/` is in English. `docs/assets/`, `e2e/` and `docs/guides/` appear when their first file does; git keeps no empty folder.

## Who reads what

| File | Read by | When | It holds | It never holds |
|---|---|---|---|---|
| `README.md` | People on the git host | First visit, setting up a machine | What it is, the quick start, how the team works, the license (readme-guide.md) | Rules, architecture, history |
| `AGENTS.md` | Every agent, every person who changes the code | Before the first change of a session | How the work is done here (agreement.md) | Product description beyond a paragraph, how-tos longer than a line |
| `CLAUDE.md` | Claude Code, which reads this name | Every session | The import of `AGENTS.md`, as agreement.md gives it | Rules of its own |
| `docs/brief.md` | Everyone, planners first | When the scope is in question | The purpose, the users, what is in and out of the first version, the domain's words and what each means | Tasks, dates (the board's) |
| `docs/architecture.md` | Whoever changes how parts fit | Before a change across parts | The parts and their boundaries, the data and where it lives, outside services and why, the main flows; current design only | History, plans |
| `docs/decisions.md` | Everyone, before undoing something | Before reversing a choice | `2026-11-15 · <decision> · <why>`, newest last; superseded by a later line, never deleted | Debate, options not taken at length |
| `docs/guides/<topic>.md` | Whoever does that thing | When doing it | Steps that worked, in the imperative | Facts about the code that belong next to it |

Work in progress, what is next and what is open live on the console project the repository is bound to (console.md): its tasks, goals, decisions and run reports. A repository with no console keeps them in `docs/status.md` (done, next, open), rewritten at the end of every session; it is the only file whose presence depends on the console.

## The languages

- Every file of the repository an agent reads is in English: `AGENTS.md`, `CLAUDE.md`, everything in `docs/`, code, comments, identifiers, commit messages, test names; and the console project's rules, which agents read with every task. One language for agents keeps a rule from being read two ways and a search from missing half the documents.
- `README.md` is in the language of its readers, the user's unless they name another. A second language is a second file (`README.en.md`), linked from the first line of each, and only when asked.
- What the product says to its users is in their languages, in the product's own dictionaries.
- What people read on the console (the project's name, the goal, tasks, reports, decisions) is in the board's language: the one the workspace's rules name, else the user's.

## What grows later

A file is added when its first content exists, never as an empty placeholder:

| Added | When | By |
|---|---|---|
| `docs/brand.md` | The product has a look and a tone | `cloudflare-new-app`, or the person who sets it |
| `DEPLOY.md` | The product is deployed | `cloudflare-deploy` |
| `docs/payments.md` | The product takes payments | `stripe-payments` |
| `docs/specs/<name>.md` | A contract has a caller outside the repository (a public API, a file format, a protocol) | Whoever publishes the contract |
| `docs/guides/<topic>.md` | A procedure was done once and will be done again | Whoever did it |
| A folder's own `README.md` | A folder has rules of its own (a package of a monorepo, a generated folder) | Whoever creates the folder |

Each addition gets a row in `docs/README.md` and, when it changes how work is done, a line in the agreement's documentation protocol, in the same commit.

## What stays out

Secrets and real environment files (only `.env.example` with safe example values); generated output and build folders; editor and machine settings other than `.editorconfig`; a personal note or an agent's memory (what the team needs is in the repository or on the board); a second copy of anything that has a home here.
