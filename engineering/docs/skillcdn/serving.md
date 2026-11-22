# Serving: from a push to what an agent gets

What a skill of this pack acts on between a push and a fresh agent's first call: which commit is served and how to see it, how long to wait, what each way of receiving a skill brings, and how the two checks are read. Read before a push, and before a fresh agent loads what was pushed. How the service works is SkillCDN's own specification and is not restated here: each section names the page that holds it by its skill URI, a file of the pack `skillcdn/skillcdn`, read over a connection to `https://skillcdn.ai/gh/skillcdn/skillcdn` or with `skillcdn file gh/skillcdn/skillcdn <path>` in a shell, and at `github.com/skillcdn/skillcdn/blob/main/<path>` on the git host.

## The default branch is what is served

A push to the default branch is a release: to everyone for a public repository, to the people the git host shows it to for a private one. Nothing in a checkout, committed or not, reaches an agent until it is pushed and served. A fork is served at its own address the same way, and an address that pins a commit (`skillcdn.ai/gh/<owner>/<repo>@<commit>`) keeps answering from that commit whatever is pushed later ([the address](skill://gh/skillcdn/skillcdn/docs/specs/address.md)).

## Which commit an agent gets

- Over HTTP: `https://skillcdn.ai/api/v1/mounts/<address>`, the address without the host (`gh/skillcdn/skills` for this pack). `commit` is the commit the mount answers from. `newest` is `null` when that is the branch's newest commit, and otherwise names the newer one with its `status`, `indexing` or `failed`, and an `errorCode` when it failed. `index.status` is `ready` when the skills can be loaded ([the REST API](skill://gh/skillcdn/skillcdn/docs/specs/rest.md), the `mounts` route). A private repository's route answers only a request that carries a token the deployment issued, and `404` otherwise.
- On the connection: every result's `Source` line names the commit it was read from, with one clause more while another commit is the newest: `newest <commit> indexing`, `newest <commit> failed (<code>)`, or `being reindexed`. The mount then answers from the last indexed commit, so an agent that loads a skill meanwhile gets the previous text. The instructions an agent received when it connected name the commit of that moment and are not refreshed ([the tools](skill://gh/skillcdn/skillcdn/docs/specs/tools.md), "Indexing and trust").
- Against the checkout: `git status -sb` says whether the branch is ahead of its remote, and it is read first, because a commit that was never pushed looks from the mount like a served one, with `newest` still `null`. `git diff <served commit> HEAD -- <paths>` says whether what an agent gets differs from the checkout, for a skill's directory, the manifests above it and the shared pages it reads; `git show <served commit>:<path>` prints a file as it is served.

## How long serving takes

On the hosted service a push is indexed within about a minute and the time its index takes, a minute or a few, without anyone asking; a deployment that is not told of pushes looks the branch up again when a request finds its last look-up older than a minute (checked 2026-11). Read the mount route before a fresh run instead of assuming the push is served: about once a minute, from a background command or between other work, since a host may block a foreground sleep (Claude Code does, checked 2026-10). A `newest` that says `failed` names the code to fix; one that still says `indexing` after ten minutes is reported to the user. A fresh run that must find a skill the push added or renamed waits for the meaning index as well, until a search's last line no longer says `embedded so far` (the find route's `ranking.embedding` counts the same): until then a search may leave that skill out even when asked for by its own name, while `browse_repo` already lists it (a renamed skill, about ten minutes after the push, hosted service, 2026-11). Push nothing while an agent is loading a skill: a long skill continues with a cursor into the served commit, and the cursor stops matching once another commit is served.

## What each way of receiving a skill brings

| The agent receives the skill through | It gets |
|---|---|
| The connection at the repository root | The rules of the manifests above the skill, the skill and the files its `skillcdn.include` lists, in `load_skill`; any other served file with `read_repo_file`, a linked page and another skill of the pack among them |
| The connection at an area | The same, except that `read_repo_file` reads only inside the area: a page of the area's `docs/` is read, a page of the root `docs/` only where the skill includes it |
| The connection at one skill | The rules, the skill and its included files; nothing it only links outside its directory |
| The MCP skills extension, or the REST listing (`/api/v1/listing/<address>`) | Each `SKILL.md` as one document with the rules and the included files inside, and every file of the skill's directory, each with a digest; no page it only links outside its directory |
| The area's Claude Code plugin | The area's `skills/` and `docs/` as files, without the rules of the manifests and without the root `docs/` |
| A copy of the skill's directory | That directory alone |

A link that starts with `/` names a file of the pack by its path from the repository root; each skill's Requirements say in one sentence where a route that lacks such a file reads it. A skill is read in pages of 16 KiB, and a page that is not the last says how many follow: an agent reads every page before it acts on any ([the tools](skill://gh/skillcdn/skillcdn/docs/specs/tools.md), "Loading a skill"). The digest of a served skill changes only when its `SKILL.md`, a file it includes or a manifest above it changes, so a push that touches none of them leaves a host's approval of the skill standing ([the format](skill://gh/skillcdn/skillcdn/docs/specs/skill-repo.md), "What the skills extension serves").

## The two checks

`node scripts/check.mjs` in the checkout is this repository's own check, the one its CI runs first: the manifests, the front-matter, the listings, the links, the includes and the text. It prints `ok:` with the counts when it passes, and each problem when it does not.

`npx @skillcdn/cli@latest check` in the checkout is the indexer's own reading, with the parser and the limits the service uses ([the format](skill://gh/skillcdn/skillcdn/docs/specs/skill-repo.md), "Checking a repository before pushing"). Name `@latest`: without it `npx` runs whichever copy its cache holds, and an older one reads the pack by older rules; the first line of the report names the command's version and the reading rules it applied. It needs npm, the network and Node.js 24 or newer. Read in the report:

| Line | What it says, and what to do |
|---|---|
| `context: N bytes, read in P pages (rules R, instructions I, included C)`, under each skill | What an agent reads before it starts. Over 16,384 bytes of instructions and included files, one line more lists the included files with their sizes, the largest first: cut the body, or link from its phase a page not every run needs. |
| `page N ends inside a table`, `a code block` or `a line`, with the file and the line the next page begins at | A block an agent must read in one piece is shortened or split under a heading of its own: a page keeps a table or a code block whole up to 4,096 bytes. |
| `extension: listed`, or `not listed (<reason>)` | Whether a host of the skills extension gets the skill, and why not. |
| `shared pages returned with the skill, outside its directory:` | The pages of a `docs/` set the skill includes: a copy of its directory lacks them. |
| `References to other packs:` | The files the pack links by skill URI. `check --references` asks the deployment whether each is there: one its pack does not have fails the check, and one that could not be asked about is `not known`. |
| `What a client is told on connect (N of 2000 characters ...)` | The connection instructions as a client gets them: the root description, the page the manifest's `start` names in place of the README, a line per folder, and beside the length whether the folder lines were shortened or some left out. |
| `Index diagnostics:` and `Notes:` | A diagnostic (a link or a `start` that names no file, a fragment that names no section, a picture without words, a quotation of a derived document not found in its source) fails the check with exit `1`: fix it in the file it names. A note (`skill_large`, `page_cut`, `section_large`) fails nothing. |

The report ends `ok: no index diagnostics` when it passes. `npx @skillcdn/cli@latest catalog --check <README files>` says whether the skill tables of those READMEs, between `<!-- skillcdn:catalog -->` and `<!-- /skillcdn:catalog -->`, are what `catalog --write` would make of the pack, and exits with `1` when one is not.
