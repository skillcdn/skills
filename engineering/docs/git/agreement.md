# The working agreement: AGENTS.md, section by section

What `AGENTS.md` holds in every repository of this pack, so that developers, planners and designers, each with their own agent, keep working in it from session to session without being told and without rules piling up. Its shape follows the agreements of working repositories that agents build every day; its words are the repository's own, in English. Read when a repository's agreement is written, and before a section of one is changed.

## The two files

- `AGENTS.md` is the agreement. Codex and most agents read this name directly; it is the one file a rule is written in.
- `CLAUDE.md` holds the import Claude Code reads as the file's own, and a line that keeps rules out of it:

  ```markdown
  # CLAUDE.md

  The working agreement for this repository is [`AGENTS.md`](AGENTS.md), for every agent and every person. It is imported here so that Claude Code reads it as its own:

  @AGENTS.md

  Do not duplicate rules into this file. Change `AGENTS.md` instead.
  ```

A folder with rules of its own (a package of a monorepo) keeps them in its `README.md`, and the root map says so.

## The sections

The opening paragraph says what the file is: "The working agreement for this repository. It applies to AI agents and humans alike. Keep it short and true: when a rule here turns out to be wrong or stale, fix it in the same change." Then, in this order:

1. **Project.** One paragraph: what it is, for whom, who runs it, where it runs. Then three lines: status (not released, or live at its address), shape (the language, the framework, the database, the host), and links to `README.md`, `docs/brief.md`, `docs/architecture.md`.
2. **Commands.** A table, the check first and bold: "**Verify (run before every commit)**". Then install, dev, test by layer, build, migrations, and whatever the stack adds. Every command run from the root.
3. **Map.** The top folders, one line each, and the single sources (configuration, the dictionaries, the database schema), each with what it holds. Dependencies between folders where they have a direction.
4. **Workflow.** The binding sentence first, then the loop (below), the definition of done, and commits and pushes.
5. **Rules.** At most eight, numbered, each with its why in the same sentence. The setup writes the two that hold for every repository from its first commit (secrets never in the repository, logs or chat; the check green before every commit) and those the code's structure already implies, a boundary a scaffold drew or a single source it keeps; every later rule enters after a slip that repeated or a correction made with emphasis, never in advance.
6. **Testing.** Four to six lines, as testing.md "What the agreement says about tests".
7. **Documentation protocol.** A table, "When you change ... / update in the same change": a command or a requirement: `README.md` and the command table; how parts fit: `docs/architecture.md`; a choice someone might undo: a line in `docs/decisions.md`; the scope: `docs/brief.md`; a procedure done for the first time: a page in `docs/guides/`; a document added (`DEPLOY.md`, a page of `docs/`): its row in `docs/README.md`; a folder: the map; a rule: this file; a gotcha learned the hard way: the Gotchas. Then: "One topic, one file. Link instead of restating. Current facts, not history: git is the changelog."
8. **Working alongside others.** Two lines and a third: concurrent work on one machine in separate worktrees, each on a short-lived branch rebased onto the main branch; hot files (the lockfile, this file, the migrations) edited small and rebased before a push, the second of two new migrations renumbered; another task's work never fixed in passing, written as a task instead.
9. **Skills.** The connection to the pack the repository was set up with (below).
10. **Gotchas.** "None yet." at first. One line each, what was learned the hard way and what to do; removed when the code makes it impossible.

Under 300 lines, always: when it nears the limit a rule is merged or a gotcha retired before a new one enters.

## The workflow section

It opens with the sentence that binds every checkout to the console, copied as it is (console.md "The sentence"):

> **Bound to a console?** When `.skillcdn-console.json` is in this checkout, or `console whoami` names a project, work the task through that SkillCDN console (`console help` says how).

Then the lines that are this repository's own, and no more, since the console's rules arrive with every task and the command's help says how a run goes:

- **Where the work is tracked.** "This repository works in the console project `<key>`, which other repositories may share: its tasks are the work, its goals the milestones, its decisions what a person must choose, and its runs the record. Before the first board command of a session, `console whoami` names `<key>`; another project named means the checkout is bound wrong, and board work stops until a person fixes it. A task is worked here only when its body names this repository. A change that is not yet a task is written as one before it is made. Follow-up work found on the way is a new task, never a line in a document; a `TODO` in the code names its task, `TODO(#<number>)`." Without a console: "This repository's work in progress, what is next and what is open is `docs/status.md`, rewritten at the end of every session."
- **What goes where.** "What the code needs to be built, run and changed lives here, versioned with it. What the team needs beyond the code (accounts, operations of the live service, research, meeting notes) lives on the console project's pages, which link to files here rather than copying them."
- **Start.** "`git pull --rebase`; read the task; read the documents its area touches."
- **During.** "One task, small commits. The check green before every commit. The documentation protocol in the same commit."
- **End.** "Push as below; hand the commits in on the task as links; finish the run with what is left. Nothing the next person needs stays in chat or in an agent's memory."

**Definition of done**, as a list: the check passes; new behavior has tests and a fix starts with a failing one; the documents the protocol names are updated in the same change; nothing secret is committed.

**Commits and pushes**, as a list: Conventional Commits (`type(scope): summary`, imperative, 72 characters or fewer; the types `feat fix docs refactor test perf build ci chore`), the body saying why; one logical change per commit, each passing the check; who pushes to the main branch and how (directly after the check and `git pull --rebase`, or through a branch and a pull request), as the team decided at setup; never a force-push to the main branch, never a skipped hook; the trailer the agent adds kept.

## Code that arrives later

A repository set up before its code (the layout and the documents now, a framework's scaffold later) gets the code without losing its files: the scaffold is made in a folder beside the repository and its files are moved in, where a file of both (`.gitignore`, `README.md`) keeps the repository's content with the scaffold's lines merged in, and a scaffold's own `AGENTS.md` or `CLAUDE.md` guidance moves to `docs/guides/<tool>.md`, linked from the agreement. Then the agreement's Commands, Map and Testing sections, the check and `docs/architecture.md` are filled from the code, in the same commit.

## The skills section

The repository keeps the connection to the pack it was set up with, so that every person's agent works from the same skills. The files are committed:

| File | Tool | Content |
|---|---|---|
| `.mcp.json` | Claude Code | `{"mcpServers":{"<server name>":{"type":"http","url":"<address>"}}}`; the tool asks each person to approve the project's servers the first time it opens the folder (checked 2026-10) |
| `.cursor/mcp.json` | Cursor | `{"mcpServers":{"<server name>":{"url":"<address>"}}}` (checked 2026-10) |
| `.codex/config.toml` | Codex CLI | `[mcp_servers.<server name>]` with `url = "<address>"`, read for trusted projects (checked 2026-10) |

The address is the one the setting-up skill was loaded from (`https://skillcdn.ai/gh/skillcdn/skills` for this pack; a fork writes its own), and the server name is the pack's (`skillcdn-skills` for this one). The section says this and no more:

> This repository was set up, and is kept, with the skills served at <address>. The connection is declared for each tool in the repository (`.mcp.json`, `.cursor/mcp.json`, `.codex/config.toml`); your tool asks you to approve it the first time it opens this folder, as for any project server, and another tool takes the address as an HTTP MCP server the way it documents. An agent that finds the server missing from its connections says so in one line and asks the person before any connection is added; no agent adds one on its own. The skills do not override this file: where they differ, this file wins. Without the connection, work goes on by this file alone.

Written this way, the section is the team's own setup and reads as such to a person and to a host's injection filters: it names who wrote it and why, points at files the tool itself asks the person to approve, forbids an agent from adding a connection on its own, keeps the agreement above the skills, and carries no urgency, no secrecy and no instruction to ignore anything. A skill that built product code in the repository adds one line naming itself and what it is for (`cloudflare-deploy` for anything on Cloudflare); the setup adds none for itself.

## `.claude/settings.json`

```json
{
  "permissions": {
    "deny": ["Read(**/.env)", "Read(**/.env.local)", "Read(**/.env.*.local)", "Read(**/*.pem)", "Read(**/*.key)"],
    "allow": ["Bash(<check command>)", "Bash(git status *)", "Bash(git diff *)", "Bash(git log *)", "Bash(console whoami)"]
  }
}
```

The patterns name the secret files exactly, so that `.env.example` stays readable; a skill that adds a secret file adds its pattern here (`.dev.vars`, `.cf-token`). Writes are not denied: an agent writes a generated value through the shell without reading the file back. A host with another settings file gets the same two lists in its own format.
