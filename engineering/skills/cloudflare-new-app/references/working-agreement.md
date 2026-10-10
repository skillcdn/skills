# The working agreement

What the new project carries so that developers, planners and designers keep working in it, each with their own agent, without rules piling up or a shared file being changed by accident. The shape comes from the reference projects of this collection; the words are the project's, in the team's language, with code, identifiers and commit messages in English.

## The files

| File | For | Holds |
|---|---|---|
| `CLAUDE.md` | Every agent and person, read first | The agreement below; under 300 lines |
| `AGENTS.md` | Agents that look for this name | Three lines: the agreement is `CLAUDE.md`, read it first, do not duplicate rules here |
| `README.md` | People on the git host | What the app is in two sentences, how to run it (install, local secrets, migrations, dev), the check, links to the docs; no rules |
| `docs/brief.md` | Everyone | The brief, kept current when scope changes |
| `docs/brand.md` | The designer, everyone who writes copy | The look and the tone, with the reason for each choice; what the copy never does |
| `docs/status.md` | The next session, whoever starts it | Three lists: done (last changes), next (what to do, in order), open (questions for the user, placeholders to replace, checks not run); rewritten at the end of every session |
| `docs/decisions.md` | Everyone, before undoing something | One dated line per decision with its reason (the adapter taken, the routing scheme, the crawler policy); never deleted, superseded by a newer line |
| `DEPLOY.md` | Whoever deploys | Written by the deploy skill at the launch: what exists, how secrets are set, how deploys and rollbacks happen |
| `.claude/settings.json` | Agents on this host | Denies reading secret files; allows the check and read-only git commands |

## `CLAUDE.md`, section by section

1. **Project.** One paragraph: what it is, for whom, who runs it, where it runs, the link to the brief and the brand. Status in one line (not launched, live at `<address>`).
2. **Stack.** A table: framework and adapter, styling, data, sign-in, email, analytics, deploy; each with the file where it is configured.
3. **Commands.** A table with `check` first and bold: "run before every commit"; then dev, typecheck, lint, test, build, migrations local and remote, brand render, deploy.
4. **Map.** The folders and the single sources (`config/i18n.ts`, `config/site.ts`, `config/features.ts`, `lib/cf.ts`), one line each.
5. **Rules.** At most eight, each with its why in the same sentence: secrets never in the repository; a fact lives in its single source; every locale from the first commit (the dictionary test); the server never imports a client value; money and dates formatted with the locale; a schema change is applied live before the code that needs it is pushed; nothing invented in the pages; the check is green before a commit.
6. **Localization.** How a locale is added (localization.md "Adding a language later"), and what differs per market.
7. **Working here.** The loop and the roles (below).
8. **Documentation protocol.** A table: when you change X, update Y in the same change (a page or route: the sitemap and the dictionary; a locale: the formats and the share image; a secret: `.dev.vars.example`, `secrets.required` and `DEPLOY.md`; a rule: this file; a decision: `docs/decisions.md`; the scope: `docs/brief.md`).
9. **Gotchas.** What was learned the hard way, one line each, removed when fixed in code.

A rule enters only with its why and after a slip repeated or a correction made with emphasis; when the file nears 300 lines, a rule is merged or a gotcha retired before a new one is added. A rule that turns out wrong is fixed in the same change that found it.

## Working here: the loop

- **Start.** `git pull --rebase`; read `docs/status.md`; look at the last build or deploy (the deploy skill's record says where). Work on `main` for small changes; a longer or risky one goes on a branch, which gets a preview address on push.
- **During.** One task, one commit, Conventional Commits in English (`feat(scope): summary`); `npm run check` green before each; the documentation protocol applied in the same commit.
- **End.** Rewrite `docs/status.md` (done, next, open); commit; push when you have the right to, since a push to `main` deploys. Nothing the next person needs stays in chat or in an agent's private memory; an agent's memory keeps personal preferences (editor, tone), not project facts.
- **Roles.** A planner writes in `docs/brief.md` and `docs/`; a designer changes the tokens in the stylesheet, `docs/brand.md` and `public/brand/`; a developer changes `src/`, `migrations/` and tests; everyone's agent reads `CLAUDE.md` first. The shared files (`CLAUDE.md`, `config/`, `migrations/`, the dictionaries' keys) are changed on purpose and named in the commit message; an agent that finds itself editing one for a side reason stops and asks.
- **Parallel work.** Two people on one machine use two checkouts or worktrees; two people adding migrations: the second renumbers after a rebase; hot files (`CLAUDE.md`, the lockfile, `docs/status.md`) are edited small and rebased before pushing.
- **Push rights.** Each person pushes their own approved work; who may push to `main` is written in this section when the team decides it; everyone else pushes branches and opens a pull request.

## `.claude/settings.json`

```json
{
  "permissions": {
    "deny": ["Read(**/.env)", "Read(**/.env.local)", "Read(**/.env.*.local)", "Read(**/.dev.vars)", "Read(**/.cf-token)", "Read(**/*.pem)"],
    "allow": ["Bash(npm run check)", "Bash(npm run typecheck)", "Bash(npm run lint)", "Bash(npm test)", "Bash(npm run build)", "Bash(git status *)", "Bash(git diff *)", "Bash(git log *)"]
  }
}
```

The patterns name the secret files exactly, so that `.dev.vars.example` and `.env.example` stay readable. Writes are not denied: the agent writes generated values into `.dev.vars` at the launch, through the shell, without reading the file back. A host with another settings file gets the same two lists in its own format.
