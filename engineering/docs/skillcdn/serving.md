# Serving: from a push to what an agent gets

How a repository in the SkillCDN Format becomes what an agent is served: which branch, which commit and how to see it, how long it takes, what each way of receiving a skill brings with it, and the two checks that show what an agent will be told. Read before a push, and before a fresh agent loads what was pushed.

## The default branch is what is served

SkillCDN serves the repository's default branch, so a push to it is a public release, and nothing in a checkout, committed or not, reaches an agent until it is pushed and served. A fork is served at its own address in the same way. An address that pins a commit (`skillcdn.ai/gh/<owner>/<repo>@<commit>`) keeps serving that commit whatever is pushed later.

## Which commit an agent gets

- On the connection: `browse_repo`, `load_skill` and `read_repo_file` name the served commit in their `Source` line, as `Source: <owner>/<repo> (commit <short sha>)`. The instructions an agent received when it connected name the commit served at that moment and are not refreshed; a later call's `Source` line names the current one (checked 2026-10).
- Over HTTP: `https://skillcdn.ai/api/v1/mounts/<address>`, the address without the host (`gh/<owner>/<repo>`; `gh/skillcdn/skills` for this collection), returns the mount's `commit`, its `index.status` (`ready` when the skills can be loaded), the counts of skills and documents, and the diagnostics when there are any (checked 2026-10).
- Against the checkout: `git rev-parse HEAD` and `git status` say what is local; `git diff <served commit> HEAD -- <paths>` says whether what an agent gets differs from the checkout for a skill's directory, the manifests above it and the shared pages it reads; `git show <served commit>:<path>` prints a file as it was at the served commit.

## How long serving takes

A push to the default branch is served within a few minutes (checked 2026-10). Check about once a minute, from a background command that polls the status or between other work, since a host may block a foreground sleep (Claude Code does, checked 2026-10); a status still not `ready` after ten minutes names diagnostics, which say what to fix. Do not push again while an agent is loading a skill: `load_skill` continues a long skill with a cursor into the served commit, and the cursor stops matching once another commit is served.

## What each way of receiving a skill brings

| The agent receives the skill through | It gets |
|---|---|
| The connection at the repository root | The rules of the manifests above the skill, the skill, and the files its `skillcdn.include` lists (its own references, and the shared pages named by their root-relative paths) in `load_skill`; any other served file with `read_repo_file` |
| The connection at an area | The same, except that `read_repo_file` reads only inside the area: a page of the area's `docs/` can be read, a page of the root `docs/` only when the skill includes it |
| The connection at one skill | The rules, the skill and its included files; nothing it only links outside its directory |
| The MCP skills extension | Each `SKILL.md` as a plain Agent Skills document with the rules and the included files inside, with a digest per file; a host without `read_repo_file` reads no linked page |
| The area's Claude Code plugin | The area's `skills/` and `docs/` as files, without the rules of the manifests and without the root `docs/` |
| A copy of the skill's directory | That directory alone |

A skill's Requirements say which of these lack what it reads, and where to fetch it. A change to a manifest or to a shared page a skill includes changes the served digest of every skill below the manifest or including the page, so a host that verified those skills through the extension asks its user again.

## The two checks

- `node scripts/check.mjs` in the checkout: the repository's own check of the manifests, the front-matter, the catalogs, the links, the includes and the text, the one its CI runs. It prints `ok:` with the counts when it passes, and each problem when it does not.
- `npx @skillcdn/cli check` in the checkout: the indexer's own reading, with the parser and the limits the service uses. It prints what an agent is told on connect, each skill's license, the shared pages it includes, its size as served and whether the skills extension lists it, and `ok: no index diagnostics` when it passes. It needs npm, the network and the Node.js version the package asks for (24 or newer, checked 2026-10).
