# The dashboard of a person's desk

What the dashboard is, how it is put in a desk, built, served and looked at, what of it is committed, and how it is changed. A person's phase of the desk setup reads this page; an agent account has no dashboard and never reads it. The commands are the console's 0.5 line (checked 2026-11); `console help desk` and `console help serve` are the reference at run time.

## What it is

- A console of the person's own: a small web app under the desk's `web/` that depends on the console's package (`@skillcdn/console`) and shows the person's work in the organization's console in three views. What stands now: the open tasks they work on, the decisions waiting for them, their open runs. The figures: what they finished and how their runs ended, over time and by project. The archive: the tasks they worked on that are done or put away and their ended runs, found by words, each linking to the organization's console.
- The views are the package's, drawn with the parts the console's own pages are drawn with, so the dashboard looks like the console and changes with it. The shell under `web/` only renders them.
- Every view is read from the console when it is looked at. Nothing of the board is stored in the desk, so the desk's repository holds the shell and no data.
- `console serve` serves the build on this machine's loopback and carries everything under `/api/` to the console with the person's sign-in, which the pages never see. That is why the dashboard needs no token, no key and no environment file of its own.

## Before starting

| Need | Check | When missing |
|---|---|---|
| Node.js 24 or newer, with npm | `node --version`, `npm --version` | Say so; the desk is complete without the dashboard, and it is added later with the same steps |
| The `console` command signed in as the person | `console whoami` | The setup's own check |
| A `console desk` that writes the shell | `console help desk` names `--web` | The command is older than the dashboard: say so and how it is updated (`console --version` says how it was installed) |
| A browser on this machine | The agent can open an address in the person's browser, or the person opens it | The person opens the address themselves, and the look is theirs to confirm |

## Putting it in the desk

1. In the desk's root, `console desk . --web`. It writes the shell under `web/`, each file only where no file of that name is there, and says which it wrote and which it left. A `web/` that is there already is the person's own: it is built as it is, never overwritten.
2. Read `web/README.md`, the shell's own page, and run what it says, as written: the install, the build, and the command that serves the build. Where the shell has no such page, the shape is the one the console's skill building-a-console gives for a person's own console: `npm install` in `web/`, the build script its `package.json` names, then `console serve <the folder the build wrote>`.
3. Nothing is pinned by hand: the shell names the version of the console's package it was written for, which is the version of the `console` command that wrote it. After the command is updated, the package in `web/` is brought to the same version (`npm install @skillcdn/console@<that version>` in `web/`) before the next build.

## Serving it and looking at it

- `console serve` runs until it is stopped, so it is started as a process of its own, in the background of the session or in a terminal the person keeps open. Read the address it prints, a loopback address (`http://127.0.0.1:<port>/`), and use it as printed.
- Check that the address answers with the page, then open it in the person's browser (`start <address>` on Windows, `open <address>` on macOS, `xdg-open <address>` on Linux), or give them the address where the agent cannot.
- Look for the person's own work: their name, and the open tasks `console work` lists for them. An empty view for a person who has open work, or a refusal on the page, is a failed check: read what the server printed and what the page says, and report it instead of guessing.
- Tell the person the one command that starts the dashboard again, as the shell's page gives it, since the server ends with the terminal that holds it. Whether it should start with the machine is theirs to arrange; the setup registers nothing.

## What is committed

The shell's source under `web/` is committed with the desk; its dependencies and its build are not. Before the commit, `git status` shows no `node_modules/` and no build folder under `web/`: where one shows, its line is added to the desk's `.gitignore` (or the shell's own). Where the desk's first commit did not carry `web/`, commit it as `feat(desk): add the dashboard` and push. No file under `web/` holds a token, an address of the organization's console or a person's data: the server supplies the first two when it runs, and the third is never kept.

## Changing it

Another view, a column, a filter or a look of the person's own is the job of the console's own skill building-a-console, shipped with the command beside working-the-board (`console whoami` prints where): it says how a page is built from the package's components and parts, run against the real board and checked. A feature with data of its own is a plugin of the console, not a page of the dashboard.

## What it must never be

- Deployed, published, or reached through a tunnel: the build is harmless without the server, and the server shows the organization's board with the person's sign-in to whoever reaches it. `console serve` listens on the loopback alone; leave it so.
- Given a token: no `CONSOLE_TOKEN`, no key in a file under `web/`, no copy of the command's credentials. A dashboard that asks for one is built wrong.
- A second home for the board: no script that saves tasks, reports or a pack's pages into the desk.
