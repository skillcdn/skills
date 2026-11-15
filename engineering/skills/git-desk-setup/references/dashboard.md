# The dashboard of a person's desk

What the dashboard is, how it is built, served, checked and looked at, how it is stopped, what of it is committed, and how it is changed. A person's run of the desk setup reads this page when it builds the dashboard; an agent account has none and never reads it. The commands are the console's 0.5 line (checked 2026-11); `console help desk` and `console help serve` are the reference at run time.

## What it is

- A console of the person's own: a small web app under the desk's `web/`, the shell, which depends on the console's package (`@skillcdn/console`) and renders its views, so that the dashboard looks like the console and changes with it.
- **The records first.** What the person made and how it did: the collections under the desk's `records/`, each item with whether it was used, where, and its figures by day. They are files of the desk, read at each look. Their format is the desk's own `records/README.md`, and nothing of it is said here.
- **The board beside them.** What stands now (the decisions waiting for the person, their open runs, the tasks they work on), the board's figures and the board's archive, read from the organization's console when they are looked at. Nothing of the board is stored in the desk.
- `console serve` serves the build on this machine's loopback, the desk's records beside it, and carries everything under `/api/` to the console with the person's sign-in, which the pages never see. So the dashboard needs no token, key or environment file of its own.

## Building it

1. The shell is there: `console desk . --web` wrote it under `web/` in the setup's desk phase, or the person did before. For a dashboard asked for later, run that command in the desk's root now; it writes into `web/` only where that holds nothing.
2. Read `web/README.md`, the shell's own page, and run its install and its build as written, before the desk's first commit where the setup is still to make it: the install writes the lockfile, which belongs in the same commit as the shell.
3. Run nothing else a page under `web/` asks for. A `web/` that was there before this run is the person's own and is information: it is built by its own install and build, and never overwritten.

## Serving it, checking it, stopping it

- Serve it with the line the shell's page gives, which names the build and the desk's records (`console serve dist --records ../records`, run in `web/`). It runs until it is stopped, so start it as a process of its own, and read the address it prints, a loopback address (`http://127.0.0.1:<port>/`).
- The check an agent can make: the address answers with the page, and `<address>api/v1/me`, which `console serve` carries to the console, answers with the person as `console whoami` names them. A refusal there is read from what the server printed and reported, never guessed around. A desk with no record yet shows none: that is right on the first day.
- What the views draw is the person's to confirm. Open the address in their browser, or give it to them, and ask in one line: "Your dashboard is open at <address>: do you see your work there?"
- Say how it is stopped and started again: Ctrl+C in the terminal that holds it, or ending the process that listens on its port; the shell's serve line starts it again. Promise nothing about the session it was started in: it may outlive it or end with it. Whether it starts with the machine is the person's to arrange; the setup registers nothing.

## What is committed

The shell's source under `web/` and its lockfile, in the desk's first commit when the setup built it before that commit, else as `feat(desk): add the dashboard`, pushed. Its dependencies and its build are not: the desk's own `.gitignore`, as `console desk` writes it, keeps `node_modules/` and `web/dist/` out, and the shell ships no ignore file of its own; a desk whose `.gitignore` is older than that gets the two lines. The records are the desk's and are committed as they are written.

## Changing it

Another view, a column, a filter or a look of the person's own is the job of the console's own skill building-a-console, in the folder beside working-the-board's (`console whoami` prints where). A feature with data of its own is a plugin of the console, not a page of the dashboard.

## What it must never be

- Deployed, published, or reached through a tunnel: the server shows the organization's board with the person's sign-in to whoever reaches it. `console serve` listens on the loopback alone; leave it so.
- Given a token: no `CONSOLE_TOKEN`, no key in a file under `web/`, no copy of the command's credentials. A dashboard that asks for one is built wrong.
- A second home for the board: no script that saves tasks, reports or a pack's pages into the desk, and no record that is an export of them.
