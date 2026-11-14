# The web app's part of the working agreement

The repository's layout, its `AGENTS.md`, its README, its test structure and its console project are those every repository of this pack has, laid out by `git-repo-setup` as the area's set [`engineering/docs/git/`](/engineering/docs/git/README.md) says. This page says what a web app built by this skill puts into them, so that developers, planners and designers keep working in it, each with their own agent. Everything agents read is in English; the README is in the language of the people who read it.

## Running the setup skill

Phase 5 runs `git-repo-setup` on the project folder, as the pack's rule on skills that chain says. It is handed what this run already has, so that it asks nothing the brief answers: what the app is and for whom (the brief's first paragraph), who works in it (the team facts of the plan), the stack and the check (`npm run check`, found in the scaffold), the README's language (the user's), and that the remote is the deploy skill's (`cloudflare-deploy` creates the repository and connects it before the first push), so that the setup commits nothing and pushes nothing. Its own stop is the console project: the one the app's work belongs to, which other repositories may share, or a new one. It returns the files of the layout, the check's continuous integration job, the skills connection, the board with the setup task taken, and the setup task's number, on which this run's report and hand-in land.

Where the setup skill cannot be loaded, the files below are written as [layout.md](/engineering/docs/git/layout.md) and [agreement.md](/engineering/docs/git/agreement.md) say, read through the repository connection, and the delivery says that the console project was not made and how to make it (the setup skill's name and address).

## Files the app adds

| File | For | Holds |
|---|---|---|
| `docs/brand.md` | The designer, everyone who writes copy | The look and the tone, with the reason for each choice; what the copy never does |
| `.dev.vars.example` | Whoever runs the app locally | The names of the local secrets, with a comment each on where the value comes from; never a value |
| `DEPLOY.md` | Whoever deploys | Written by the deploy skill at the launch: what exists, how secrets are set, how deploys and rollbacks happen |

`docs/brief.md` is the brief of phase 1; `docs/decisions.md` starts with the plan's technical choices (the adapter, the routing scheme, the crawler policy, the AI model and its price where the app writes text), one dated line each.

## What `AGENTS.md` says for a web app

The sections are agreement.md's; a web app fills them so:

- **Project.** Status in one line: not launched, or live at `<address>`.
- **Commands.** `npm run check` first; then dev, typecheck, lint, test, build, migrations local and remote, brand render, deploy.
- **Map.** A Stack table first (framework and adapter, styling, data, sign-in, email, analytics, deploy, each with the file where it is configured), then the folders and the single sources (`config/i18n.ts`, `config/site.ts`, `config/features.ts`, `lib/cf.ts`).
- **Rules**, each with its why: secrets never in the repository; a fact lives in its single source; every locale from the first commit (the dictionary test); the server never imports a client value; money and dates formatted with the locale; a schema change is applied live before the code that needs it is pushed; nothing invented in the pages; the check is green before a commit.
- **Localization**, a section of its own after Rules: how a locale is added (localization.md "Adding a language later"), and what differs per market.
- **Documentation protocol**, rows beyond the shared ones: a page or a route: the sitemap and the dictionary; a locale: the formats and the share image; a secret: `.dev.vars.example`, `secrets.required` and `DEPLOY.md`; the look: `docs/brand.md`.
- **Workflow.** At the start, a look at the last build or deploy (`DEPLOY.md` says where); a longer or risky change goes on a branch, which gets a preview address on push; a push to `main` deploys, so it is made by whoever has the right to.
- **Working alongside others.** The roles: a planner writes in `docs/brief.md` and `docs/`; a designer changes the tokens in the stylesheet, `docs/brand.md` and `public/brand/`; a developer changes `src/`, `migrations/` and the tests. The shared files (`AGENTS.md`, `config/`, `migrations/`, the dictionaries' keys) are changed on purpose and named in the commit message; an agent that finds itself editing one for a side reason stops and asks.
- **Skills.** One line beyond the shared section: `cloudflare-deploy` for anything on Cloudflare (secrets, the domain, the database, builds, the deploy record), and the references of `cloudflare-new-app`, which are the conventions this code follows.

## `.claude/settings.json` for a web app

The shared file (agreement.md), with the app's secret files added to `deny` (`Read(**/.dev.vars)`, `Read(**/.cf-token)`, `Read(**/.gemini-key)`) and its checks to `allow` (`Bash(npm run check)`, `Bash(npm run typecheck)`, `Bash(npm run lint)`, `Bash(npm test)`, `Bash(npm run build)`). The patterns name the secret files exactly, so that `.dev.vars.example` stays readable.

## What is open, and placeholders

What the app leaves open (a key the user will supply later, an owner's details, content marked as a placeholder, a check not run) is written where the repository tracks its work: a task on the console project for each, in the shape the setup skill writes tasks, or `docs/status.md` where the repository has no console.
