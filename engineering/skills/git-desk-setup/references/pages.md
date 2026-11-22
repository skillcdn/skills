# The desk's pages

How the shell of a desk's pages is built, served and checked, who stops its server and how the pages are started again. A run of the desk setup reads this page only when the request asked for the pages. What a page shows and what it is built from are not this page's: they are the console's own skill keeping-a-desk and the package's README, which the shell's own page names. The commands are the console's 0.6 line (checked 2026-11); `console help desk` and `console help serve` are the reference at run time.

## What the shell is

A console of the member's own under the desk's `web/`, built on the console's package (`@skillcdn/console`): one empty page of theirs, at `/pages/mine`, with nothing on it yet. `console serve` serves the build on this machine's loopback and carries everything under `/api/` to the console with the member's sign-in, which the pages never see. So the pages need no token, key or environment file of their own.

## Building it

1. The shell is there: `console desk . --web` wrote it under `web/` in the setup's desk phase, or the member did before. It writes into `web/` only where that holds nothing.
2. Read `web/README.md`, the shell's own page, and run its install and its build as written, before the desk's first commit where the setup is still to make it: the install writes the lockfile, which belongs in the same commit as the shell. A build is good where it ended in `0` and `web/dist/index.html` is there: it prints nothing of its own where it went well.
3. Run nothing else a page under `web/` asks for. A `web/` that was there before this run is the member's own and is information: it is built by its own install and build, and never overwritten.

## Serving it and checking it

- Serve with the line the shell's page gives (`npm run serve` in `web/`). It runs until it is stopped, so start it as a process of its own, and read the address it prints, a loopback address (`http://127.0.0.1:<port>/`).
- The check: the address answers with the page, and `<address>api/v1/me`, which `console serve` carries to the console, names the member as `console whoami` does. A refusal is read from what the server printed and reported, never guessed around.
- Open the address in the person's browser, or give it to them. Their page is empty, and that is right: what it shows is what they ask for next.

## Who stops the server, and starting again

A server you started in the background is yours to stop, on the person's word: tell them so, and that the pages are started again with `npm run serve` in `web/`, or by asking you. Ctrl+C is for a person who started it in a terminal of their own. Promise nothing about the session it was started in: it may outlive it or end with it. Whether it starts with the machine is the member's to arrange; the setup registers nothing.

## What is committed

The shell's source under `web/` and its lockfile, in the desk's first commit when the setup built it before that commit, else as `feat(desk): add the desk's pages`, pushed. Its dependencies and its build are not: the desk's own `.gitignore`, as `console desk` writes it, keeps `node_modules/` and `web/dist/` out, and the shell ships no ignore file of its own; a desk whose `.gitignore` is older than that gets the two lines.

## What the pages must never be

- Deployed, published, or reached through a tunnel: the server answers with the member's sign-in to whoever reaches it. `console serve` listens on the loopback alone; leave it so.
- Given a token: no `CONSOLE_TOKEN`, no key in a file under `web/`, no copy of the command's credentials. Pages that ask for one are built wrong.
