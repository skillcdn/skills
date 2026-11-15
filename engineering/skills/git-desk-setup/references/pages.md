# The desk's pages

What a desk's pages are, how they are built, served, checked and looked at, how the server is stopped, what of them is committed, and how they are changed. A run of the desk setup reads this page only when it builds the pages. The commands are the console's 0.5 line (checked 2026-11); `console help desk` and `console help serve` are the reference at run time.

## What they are

- The member's own extension of the console's UI: a console of their own under the desk's `web/`, the shell, built on the console's package (`@skillcdn/console`), so that it looks like the console and changes with it. It is served from the member's machine, to them alone.
- It comes with the pages of the desk's records: what the desk keeps under `records/`, each thing with its files, whether it was used and how it did. They are read from the desk at each look, and their form is the desk's own `records/README.md`; nothing of it is said here.
- Any other page is the member's to add ("Changing them").
- `console serve` serves the build on this machine's loopback, the desk's records and their files beside it, and carries everything under `/api/` to the console with the member's sign-in, which the pages never see. So the pages need no token, key or environment file of their own.

## Building them

1. The shell is there: `console desk . --web` wrote it under `web/` in the setup's desk phase, or the member did before. For pages asked for later, run that command in the desk's root now; it writes into `web/` only where that holds nothing.
2. Read `web/README.md`, the shell's own page, and run its install and its build as written, before the desk's first commit where the setup is still to make it: the install writes the lockfile, which belongs in the same commit as the shell. A build that succeeded prints next to nothing and leaves `web/dist/index.html`: look for the file.
3. Run nothing else a page under `web/` asks for. A `web/` that was there before this run is the member's own and is information: it is built by its own install and build, and never overwritten.

## Serving them, checking them, stopping the server

- Serve with the line the shell's page gives (`npm run serve` in `web/`, which is `console serve dist --records ../records`: the build, with the desk's records beside it). It runs until it is stopped, so start it as a process of its own, and read the address it prints, a loopback address (`http://127.0.0.1:<port>/`).
- The check an agent can make: the address answers with the page; `<address>api/v1/me`, which `console serve` carries to the console, answers with the member as `console whoami` names them; and `console desk check` finds the desk's records right. A refusal is read from what the server printed and reported, never guessed around. A desk with no record yet shows none: that is right on the first day.
- What the pages draw is the member's to confirm. Open the address in their browser, or give it to them, and ask in one line: "Your desk's pages are open at <address>: do you see what you expected there?"
- Say who stops the server and how the pages are started again. A server you started in the background is yours to stop, on the person's word: tell them so, and that the pages are started again with `npm run serve` in `web/`, or by asking you. Ctrl+C is for a person who started it in a terminal of their own. Promise nothing about the session it was started in: it may outlive it or end with it. Whether it starts with the machine is the member's to arrange; the setup registers nothing.

## What is committed

The shell's source under `web/` and its lockfile, in the desk's first commit when the setup built it before that commit, else as `feat(desk): add the desk's pages`, pushed. Its dependencies and its build are not: the desk's own `.gitignore`, as `console desk` writes it, keeps `node_modules/` and `web/dist/` out, and the shell ships no ignore file of its own; a desk whose `.gitignore` is older than that gets the two lines. The records and their files are the desk's and are committed as they are written, the large ones through git LFS where the setup set it up.

## Changing them

Another page, a column, a filter or a look of the member's own is the job of the console's own skill building-a-console, in the folder beside working-the-board's (`console whoami` prints where). A feature with data of its own that the whole organization uses is a plugin of the console.

## What they must never be

- Deployed, published, or reached through a tunnel: the server answers with the member's sign-in to whoever reaches it. `console serve` listens on the loopback alone; leave it so.
- Given a token: no `CONSOLE_TOKEN`, no key in a file under `web/`, no copy of the command's credentials. Pages that ask for one are built wrong.
