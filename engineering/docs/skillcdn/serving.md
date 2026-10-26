# Serving: from a push to what an agent gets

How a repository in the SkillCDN Format becomes what an agent is served: which branch, which commit and how to see it, how long it takes, what each way of receiving a skill brings with it, and the two checks that show what an agent will be told. Read before a push, and before a fresh agent loads what was pushed.

## The default branch is what is served

SkillCDN serves the repository's default branch, so a push to it is a public release, and nothing in a checkout, committed or not, reaches an agent until it is pushed and served. A fork is served at its own address in the same way. An address that pins a commit (`skillcdn.ai/gh/<owner>/<repo>@<commit>`) keeps serving that commit whatever is pushed later.

## Which commit an agent gets

- On the connection: `browse_repo`, `load_skill` and `read_repo_file` name the served commit in their `Source` line, as `Source: <owner>/<repo> (commit <short sha>)`. While the branch's newest commit is not the one served, the line carries one clause more: `newest <commit> indexing` while its index is built, `newest <commit> failed (<code>)` when it could not be, and `being reindexed` while the same commit is rebuilt under newer reading rules; the mount then answers from the last indexed commit of the branch, so an agent that loads a skill meanwhile gets the previous text (SkillCDN 0.4.0, checked 2026-10). The instructions an agent received when it connected name the commit served at that moment and are not refreshed; a later call's `Source` line names the current one (checked 2026-10).
- Over HTTP: `https://skillcdn.ai/api/v1/mounts/<address>`, the address without the host (`gh/<owner>/<repo>`; `gh/skillcdn/skills` for this pack), returns the mount's `commit` (the commit it answers from), `newest` (the branch's newest commit with its `status`, `indexing` or `failed`, and its `errorCode`, while another is served in its place; `null` when the served commit is the newest), its `index.status` (`ready` when the skills can be loaded), `index.search` (whether the mount is searched by meaning as well as by words, and how far its embedding has come), the counts of skills and documents, and the diagnostics when there are any (SkillCDN 0.4.0, checked 2026-10).
- Against the checkout: `git rev-parse HEAD` and `git status` say what is local; `git diff <served commit> HEAD -- <paths>` says whether what an agent gets differs from the checkout for a skill's directory, the manifests above it and the shared pages it reads; `git show <served commit>:<path>` prints a file as it was at the served commit.

## How long serving takes

A push to the default branch is served once the deployment has looked the branch up again and indexed the new commit: a branch is looked up again after a short while (`REF_TTL_SECONDS` of the deployment, 60 seconds by default) or at once where the deployment's GitHub App is installed on the repository, and the indexing takes a minute or a few (checked 2026-10). Until then the mount keeps answering from the last indexed commit and says so in its `Source` line and in `newest` (on the hosted service, a push was answered from the previous commit with `newest` naming the pushed one as `indexing` for a few minutes, 2026-10-26), so read the mount route before a fresh run rather than assuming the push is served; and read `git status -sb` first, because a commit that was never pushed looks the same from the mount, with `newest` still `null`. Check about once a minute, from a background command that polls the route or between other work, since a host may block a foreground sleep (Claude Code does, checked 2026-10); a `newest` that says `failed` names the code to fix, and one that still says `indexing` after ten minutes is reported. Do not push again while an agent is loading a skill: `load_skill` continues a long skill with a cursor into the served commit, and the cursor stops matching once another commit is served.

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
- `npx @skillcdn/cli check` in the checkout: the indexer's own reading, with the parser and the limits the service uses. It prints the version of the reading rules it applied, what an agent is told on connect, each skill's license, the shared pages it includes, its size as served and whether the skills extension lists it, every document with how many sections its headings make and whether it is too large to be searched, and `ok: no index diagnostics` when it passes. It needs npm, the network and the Node.js version the package asks for (24 or newer; under 22 it ran with an engine warning, checked 2026-10).
