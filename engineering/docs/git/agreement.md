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
4. **Workflow.** The binding sentence first, then where the work is tracked and the loop (below), the definition of done, and commits and pushes.
5. **Rules.** At most eight, numbered, each with its why in the same sentence. The setup writes the two that hold for every repository from its first commit (secrets never in the repository, logs or chat, a secret file never opened or printed, `.env.example` saying what one holds; the check green before every commit) and those the code's structure already implies, a boundary a scaffold drew or a single source it keeps; every later rule enters after a slip that repeated or a correction made with emphasis, never in advance.
6. **Testing.** Four to six lines, as testing.md "What the agreement says about tests".
7. **Documentation protocol.** A table, "When you change ... / update in the same change": a command or a requirement: `README.md` and the command table; how parts fit: `docs/architecture.md`; a choice someone might undo: a line in `docs/decisions.md`; the scope: `docs/brief.md`; a procedure done for the first time: a page in `docs/guides/`; a document added (`DEPLOY.md`, a page of `docs/`): its row in `docs/README.md`; a folder: the map; a rule: this file; a gotcha learned the hard way: the Gotchas. Then: "One topic, one file. Link instead of restating. Current facts, not history: git is the changelog."
8. **Working alongside others.** Two lines and a third: concurrent work on one machine in separate worktrees, each on a short-lived branch rebased onto the main branch, one task to a checkout; hot files (the lockfile, this file, the migrations) edited small and rebased before a push, the second of two new migrations renumbered; another task's work never fixed in passing, written as a task instead.
9. **Skills.** Where the skills the repository is worked with are read, and the ones its work needs (below).
10. **Gotchas.** "None yet." at first. One line each, what was learned the hard way and what to do; removed when the code makes it impossible.

Under 300 lines, always: when it nears the limit a rule is merged or a gotcha retired before a new one enters.

## The workflow section

It opens with the binding sentence: the one `console use` printed when the checkout was bound, copied from there as it is and never typed from memory (console.md "The binding"). Then the lines that are this repository's own, and no more. How work is put on the board, followed up, decided and reported is the console's to say: its rules arrive with every task and the skill `console whoami` names says how a run goes, so the agreement restates none of it.

- **Where the work is tracked.** "This repository works in the console project `<key>`, which other repositories may share. `console whoami`, the first command of a session, names `<key>`, named by this checkout's `.skillcdn-console.json`. Anything else it says (another project, a project named by something outside this checkout, a refusal) means the checkout is bound wrong. Tell the person what `console whoami` printed, whole, and do no board work until they fix it, name the key to bind to, or leave the choice to you. Left the choice, bind the checkout to `<key>` (`console use <key>`), say so at once and again at the end, and never bind it to another key. A task is worked here only when it is this repository's. Work asked for here that names no task is looked for on the board by one word a title would hold (`console tasks --search <word>`) and, where none is there, written and taken in one command before it is done (`console task new "<title>" --body <markdown> --category <category> --take`), its number told; where the take fails, `console take <number>`, never a second task. What is next and what is open is on the board and in no file here; a `TODO` in the code names its task, `TODO(#<number>)`." A public repository, whose binding file is not committed, names the key in no file either, since the key names the organization's project as the file names its console. Its line opens instead: "This repository is public, so no file in it names the console project its maintainers work in: `<key>` below stands for that project's key, which the person gives. `console whoami`, the first command of a session, names the project this checkout's own `.skillcdn-console.json` binds it to. In a fresh checkout it names none: ask the person for the key (`console projects` lists the projects they may work in), run `console use <key>` once, and write the key into no file here. A project named by something outside this checkout, or a refusal, means the checkout is bound wrong: tell the person what `console whoami` printed, whole, and do no board work until they name the key." It then goes on from "A task is worked here only when it is this repository's." Without a console the whole line is: "This repository's work in progress, what is next and what is open is `docs/status.md`, rewritten at the end of every session."
- **What goes where.** "What the code needs to be built, run and changed lives here, versioned with it. What the team needs beyond the code (accounts, operations of the live service, research, meeting notes) lives on the console project's pages, which link to files here rather than copying them."
- **Start.** "`console whoami`; `git pull --rebase`; in a fresh clone, the install the README's quick start gives; read the task; read the documents its area touches."
- **During.** "One task, small commits. The check green before every commit. The documentation protocol in the same commit."
- **End.** "Push as below; hand the commits in on the task as links; finish the run with what is left. Nothing the next person needs stays in chat or in an agent's memory."
- **A git command the host refuses.** "A host may keep an agent from writing under `.git`, so that a pull, a commit or a push is refused. The work and the check go on all the same: report what is changed and not committed, with the check's result, write out for the person, in the chat, the commands left to run, in order, and call nothing done that is not pushed."

**Definition of done**, as a list: the check passes; new behavior has tests and a fix starts with a failing one; the documents the protocol names are updated in the same change; nothing secret is committed.

**Commits and pushes**, as a list: Conventional Commits, the body saying why; one logical change per commit, each passing the check; who pushes to the main branch and how, as the team decided at setup (directly, in this order: the commit after a green check; `git pull --rebase`, run as a command of its own and its answer read; the check again where it brought commits; then the push; or through a branch and a pull request); never a force-push to the main branch, never a skipped hook; a trailer the agent's own product adds is kept, and an agent whose product adds none writes none.

## Code that arrives later

A repository set up before its code (the layout and the documents now, a framework's scaffold later) gets the code without losing its files: the scaffold is made in a folder beside the repository and its files are moved in, where a file of both (`.gitignore`, `README.md`) keeps the repository's content with the scaffold's lines merged in, and a scaffold's own `AGENTS.md` or `CLAUDE.md` guidance moves to `docs/guides/<tool>.md`, linked from the agreement. Then the agreement's Commands, Map and Testing sections, the check and `docs/architecture.md` are filled from the code, in the same commit. A repository set up before its code gets no section of the agreement for this: its Project section's status says that no code is there yet, and the scaffolding is one of its next tasks, with these steps in its body.

## The skills section

The skills a repository is worked with are the pack of its console project, read through the console by every person's agent with nothing to connect. The section says so, and names the skills that are this repository's:

> The skills this repository is worked with are the pack of its console project: `console skills --search <words> --limit 5` finds one, and `console skill <path>` loads it. A skill never overrides this file: where they differ, this file wins. Without a console, work goes on by this file alone.

- **A line per skill that is this repository's** (the one that built it, the one that deploys it), under that paragraph, by the path of its `SKILL.md` in the pack and what it is for: "`engineering/skills/cloudflare-deploy/SKILL.md`, for anything on Cloudflare". The setup adds none for itself; a skill that built product code in the repository adds its own. Its home is the agreement and not the project's rules, for three reasons: the agreement is handed to every session in the checkout before any step, a task taken or not; whoever sets the repository up can write it, while a project's rules are its owner's; and a project may be shared, so that a skill of one repository would need a qualifier there. A project's rules name only the skills that hold for every repository of the project (console.md "The project's rules").
- **A pack's first page.** Where the project's pack names one (console.md "The project's pack"), the paragraph ends with one sentence more: "Before the first job of a session, `console skill --file <path>` reads the pack's own page on finding a skill." A pack that names none adds nothing.
- **Which pack** the project reads, and what a setup that came from another does, is settled at the plan (console.md "The project's pack"). Where that leaves a shared project on another pack, the section names the address the skills are served at, and the connection below is written.

### A host's own connection, on request

Written only when the user asks for the skills in their tools without the console ("connect the skills in Cursor too"), or for a shared project whose pack is another. One file per tool, committed, each naming the address the pack is served at (`https://skillcdn.ai/gh/skillcdn/skills` for this pack; a fork writes its own) under the pack's server name (`skillcdn-skills` for this one):

| File | Tool | Content |
|---|---|---|
| `.mcp.json` | Claude Code | `{"mcpServers":{"<server name>":{"type":"http","url":"<address>"}}}`; the tool asks each person to approve the project's servers the first time it opens the folder (checked 2026-10) |
| `.cursor/mcp.json` | Cursor | `{"mcpServers":{"<server name>":{"url":"<address>"}}}` (checked 2026-10) |
| `.codex/config.toml` | Codex CLI | `[mcp_servers.<server name>]` with `url = "<address>"`, read for trusted projects (checked 2026-10) |

The section then ends with: "The same skills are served at <address>, declared for each tool in the repository (`.mcp.json`, `.cursor/mcp.json`, `.codex/config.toml`); your tool asks you to approve the connection the first time it opens this folder. An agent that finds the server missing says so in one line and asks the person; no agent adds a connection on its own." Said so, the files read as the team's own setup, to a person and to a host's injection filters.

What this route costs beside the console's: every person approves the connection in each tool; a private pack asks each of them for access of their own at SkillCDN, where the console reads it with the project's token; and Claude Code asks the person before an agent writes `.mcp.json`, so a session that cannot ask shows the content and the path and waits for the person to write it. The layout's map and the README's "How we work" then name the files (layout.md, readme-guide.md).
