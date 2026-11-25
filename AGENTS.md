# AGENTS.md

The working agreement for this repository. It applies to AI agents and humans alike, whichever agent you are: Codex reads this file directly, Claude Code reads it through `CLAUDE.md`. Keep it short and true: when a rule here turns out to be wrong or stale, fix it in the same change.

## Project

This repository is SkillCDN's own pack, served as an MCP server at `skillcdn.ai/gh/skillcdn/skills`. A pack is what an agent receives whole at one address, a git repository of skills, documents and rules; this one holds skills for an AI agent to do real company work, one area at a time (marketing, media, product, engineering, more to come), each driving a real tool from the request to the finished result. The skills are meant to be used together, by one person who runs a whole company's work through them as one AI team, so a skill reads what another area documents wherever its work meets it. It is the reference pack for the [SkillCDN Format](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/skill-repo.md): the shape SkillCDN proposes for a pack. It takes no pull requests from outside; it is meant to be forked, so that a team publishes its own pack in the same shape with the same checks. Content, not code: Markdown that agents read, small JSON, and one dependency-free script that validates it. Every push to `main` is a public release, because SkillCDN indexes the default branch.

- **Format:** the SkillCDN Format, which is the [Agent Skills](https://agentskills.io/specification) layout plus manifests. A skill is a directory with a `SKILL.md`; an area is a directory with a `SKILLCDN.md` that describes its skills and adds their rules; a document set is a directory of Markdown under `docs/` at the root or in an area; `SKILLCDN.md` at the root names the pack and carries the rules for every skill.
- **Audience:** two readers at once. An agent that will execute a skill from a fresh session with no memory, and a person who wants to see how a skill for a given tool, or a pack in the format, is written, and to fork it.
- **License:** MIT. Public repository.

## Non-negotiables

1. **Everything committed is in English** (content, commit messages, pull request text), whatever language the conversation is in. Other languages appear only in `translations` fields.
2. **Public repository hygiene.** No secrets, tokens, account identifiers, private hostnames, customer material, real people's likeness or identity, or internal business reasoning. Fake-looking secrets trip the scanner too; use obvious placeholders like `<url>`.
3. **Content only.** No rendered media, screenshots, binaries or generated output. Skills ship text. Data files are small JSON or YAML that an agent reads. The one rendered file is the pack's own picture, `assets/banner.webp` at the root, which the root manifest's `image` names; `scripts/check.mjs` allows that path alone and holds it under 200 KiB.
4. **Skills declare; they never require executing repository code.** A `scripts/` directory inside a skill is optional help for agents that run locally. SkillCDN serves it as text. The skill must work from `SKILL.md` and `references/` alone.
5. **Skills spend only with consent.** Any step that costs the user money or credits is estimated first and gated on their approval. This and the other rules for every skill are the body of `SKILLCDN.md`.
6. **No pinned versions of models, products or APIs.** A skill tells the agent how to discover the latest through the tool's own catalog and how to choose among candidates. A dated snapshot may illustrate a number, marked as illustrative.
7. **Every skill belongs to an area.** `<area>/skills/<name>/`, never at the root. The area's `SKILLCDN.md` says who its skills are for and adds only the rules that hold for every skill in it. A rule for every skill in the repository goes in the root manifest; a rule for one skill stays in that skill.
8. **Each skill carries what it cannot work without.** It may be mounted alone (`.../skills/<area>/skills/<name>`), installed as part of its area's plugin, or copied into another agent, so its workflow, its checkpoints, its verdicts and its hard rules live inside its directory. From outside it links three things, each by a root-relative path. A page of a document set: what the skills of one tool family share (how its tools behave, the knowledge every run adds to) lives once in `docs/<family>/` at the root, or in an area's `docs/` when every skill that includes its pages is in that area; the page every run needs is declared in `skillcdn.include` and arrives with the skill, the rest are linked from the phase that reads them. Another skill of the pack it runs before, after or under itself, by its `SKILL.md`: the link names the skill for the agent and brings none of its rules. And a script or an asset of another skill that a step runs as it is. `scripts/check.mjs` rejects an include that leaves the skill, the root's `docs/` and its own area's, and any other link that leaves the skill. A skill's Requirements end with the one sentence that says where a copy, a plugin or a mount below the root reads what it lacks (`guide/skill-authoring.md`). A skill does not restate the repository's or the area's rules: SkillCDN hands the manifests to the agent with every skill.
9. **The format is SkillCDN's spec, not ours.** The spec is normative for layout, manifests, front-matter and what is served. This repository does not restate it; `guide/` holds only what it adds on top (style, process).
10. **Agents reach only what the format serves.** Discoverable: the skills, the manifests and the declared document directories. Readable on demand: a README at the root or in a served folder, and the pages it links. Everything else (`scripts/`, `.github/`, configuration) stays on the git host. Put content for agents where it is discoverable, and authoring material under `guide/`.

## Repository map

```
SKILLCDN.md       the repository manifest: the pack's name, description, documents: [docs], the rules for every skill
README.md         for people on the git host, including whoever forks it; readable by agents on demand
assets/           banner.webp, the pack's own picture: the root manifest's image, shown by the explorer and the address's page (git host)
<area>/           one folder per area of work (marketing, product, engineering, ...)               (served)
  SKILLCDN.md     the area manifest: who its skills are for, the rules its skills add
  README.md       the area's catalog
  skills/<name>/  one directory per skill: SKILL.md, references/, assets/, optional scripts/
  docs/           the area's document sets, Markdown only, discovered by default next to the manifest
docs/             document sets that serve every area, declared in the root manifest: handbooks, and       (served)
                  docs/<family>/ for what the skills of one tool family share
guide/            skill-authoring, adding, finding, roadmap, tools/<family>.md                         (git host)
scripts/          check.mjs (validation; CI runs it, then the indexer's own check and its check of the READMEs' tables)        (git host)
.claude-plugin/   marketplace.json: one Claude Code plugin per area with skills                        (hidden)
.github/          CI (validation, the indexer's check, secret scan), the pull request notice, dependabot                    (hidden)
```

## Commands

| Task | Command |
|---|---|
| **Verify (run before every commit)** | `node scripts/check.mjs` |
| The indexer's own reading (what an agent is told, what each skill weighs, the index diagnostics) | `npx @skillcdn/cli@latest check` |
| The skill tables of the READMEs, after a skill is added or its description's first sentence changes | `npx @skillcdn/cli@latest catalog --write README.md --write <area>/README.md` |

Node.js 24. No install step; the script has no dependencies. Name `@latest` for the indexer: a bare `npx @skillcdn/cli` runs whichever copy its cache holds, and an older one reads the pack by older rules; its first line names its version and the reading rules it used. CI runs the first two on every push and holds the READMEs' tables to the pack (`catalog --check`); the indexer's check also runs once a week. Do not add a package manager, a build or a framework to this repository. If validation needs more than one script can reasonably do, that is a sign the rule belongs in SkillCDN's own indexer instead.

## Workflow

**Bound to a console?** Before the first step, run `console whoami`: when it names a project, or `.skillcdn-console.json` is in this checkout, work the task through that SkillCDN console (its answer says how).

**The binding file is never committed, and no file here names a project's key.** This repository is public, and both name an organization's own console project: `.gitignore` lists `.skillcdn-console.json`, and `<key>` is a placeholder on purpose. In a fresh checkout `console whoami` names no project: ask the person for the key (`console projects` lists the projects they may work in), run `console use <key>` once, and write the key into no file of this repository.

**Before you start.** Read the spec, [guide/skill-authoring.md](guide/skill-authoring.md), the rules in [SKILLCDN.md](SKILLCDN.md) and the manifest of the area you are adding to. Read the existing skill closest to what you are adding. Read the tool's own documentation for the tool family you are writing for; the skill must reflect how the tool behaves today. An agent adds a skill with the authoring skill, `engineering/skills/skillcdn-skill-authoring/`, which does the steps below from the work already done; what is planned next is in [guide/roadmap.md](guide/roadmap.md).

**While working.**

- Follow [guide/adding.md](guide/adding.md) step by step. It ends with trying the skill from a fresh session, following only what the files say. Do not skip that.
- One skill, area or document set per change. Do not reformat or "improve" others in passing.
- Discover live values (model ids, parameters, costs) with the tool at write time to make sure the instructions are right, but write the *how to discover* into the skill, not the values.
- Where the tool has a choice the user should make (which model, how much to spend, which style), write the question the agent asks, and the default if any.

**Definition of done.**

- `node scripts/check.mjs` passes.
- A skill is in the tables of its area's `README.md` and of the root `README.md`, which `catalog --write` fills, and has its section in `docs/pack/jobs.md`. A new area is listed in the root `README.md` and, once it has a skill, in `.claude-plugin/marketplace.json`. A document set is listed in the `README.md` of its `docs/` and in the root `README.md`.
- A new tool family has a row in the root `README.md` "Tool families" table.
- The skill was exercised end to end with the real tool at least once, and what had to be said in chat was folded back into the files.
- Nothing in rules 1 to 10 is violated.

**Commits and pushes.**

- [Conventional Commits](https://www.conventionalcommits.org/): `type(scope): summary`, imperative, 72 characters or fewer. Types: `feat fix docs chore ci`. Scopes: `repo docs guide`, an area name for a change to one area (`feat(engineering): ...`), or a skill name for a change to one skill (`fix(higgsfield-shorts-ad): ...`). The body says why.
- Commit and push directly to `main` after `node scripts/check.mjs` passes and `git pull --rebase`. This repository takes no pull requests from outside: it is forked, and a fork sets its own process. Do not create branches or pull requests unless asked.
- A pull request of the maintainers' own agent accounts names its task by number; any other is closed as the notice says. It is reviewed as any change is and lands with its commits as they are (`git merge --ff-only`, a merge commit where `main` went on), what the review changes as commits on top in the same push, so that the host marks it merged; stacked ones land together. One whose commits hold what rule 2 keeps out goes back to its author first.
- Never force-push or rewrite `main`. Keep the `Co-Authored-By` trailer your agent's own product adds; where it adds none, write none.

## Documentation protocol

| When you change... | Update in the same change |
|---|---|
| A skill's behavior, inputs or tools | Its `SKILL.md` and references; its section in `docs/pack/jobs.md` if what a user asks for changed; the READMEs' tables (`catalog --write`) if the description's first sentence changed |
| A rule that applies to every skill | The body of `SKILLCDN.md`, kept short; skills do not restate it |
| A rule that applies to every skill of one area | The body of that area's `SKILLCDN.md`, kept to a few lines; it is paged before every skill of the area |
| What the repository is, or which directories hold documents | The front-matter of `SKILLCDN.md`; the repository map above |
| An area's purpose, or its first skill | The area's `SKILLCDN.md` front-matter and `README.md`; its row in the root `README.md`; `.claude-plugin/marketplace.json` |
| A file a fork must rename or rewrite (a name, an owner, an address) | The "Make it yours" steps in the root `README.md` |
| The badge, the brand files the READMEs link, or the pack's picture | The tops of the root `README.md` and of every area's `README.md`, step 6 of "Make it yours", and step 3 of "A new area" in `guide/adding.md`; the picture is one file, `assets/banner.webp`, encoded to stay under the check's limit |
| How skills are written or checked, beyond the spec | `guide/skill-authoring.md`; `scripts/check.mjs` if the rule is mechanical. A change to the format itself belongs in SkillCDN's spec, not here |
| The process for adding things | `guide/adding.md` |
| A skill you add, change in what it does, or retire | Its row in `guide/roadmap.md`: the status, and the name once it is built |
| A new tool family | Root `README.md` table; `docs/<family>/` once two skills share knowledge or a second skill of the family is planned, and `guide/tools/<family>.md` for how authors keep the skills and the set in step |
| What a run taught about a tool, where every skill of its family meets it | The sentence it bears on in `docs/<family>/<topic>.md`, with the model and the month where the fact can go stale, as behavior and never as the run's words (`guide/skill-authoring.md` "Knowledge pages"); an edge of one skill's own phase in that skill's `references/tool-notes.md`, in the same shape |
| A durable gotcha you learned the hard way | "Gotchas" below |

One topic, one file. Link instead of restating.

## Gotchas

How SkillCDN reads and serves a pack is the standard's to say: [the format](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/skill-repo.md) and [the tools](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/tools.md), with `npx @skillcdn/cli@latest check` for what it does with this pack today. Below is what this repository does about it, and what its own runs taught.

**What the standard's behavior asks of this pack**

- A page that must be searchable goes under a `docs/`; authoring material goes under `guide/`. Search sees skills, manifests and declared document directories; a README of a served folder and the pages it links are only readable ([Markdown references](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/skill-repo.md#markdown-references)).
- A document under `docs/` links only what an agent is meant to reach through the mount: skills, manifests, document directories, the README of a served folder. The format follows a served document's links, so a link into `guide/` would make authoring material readable there: the check rejects it.
- An area manifest declares `documents` only for a directory other than `docs`, and only one that exists.
- Rules travel with every skill and come first on its pages: keep an area's rules to a few lines. The reason is the page they cost, not the digest: a served skill's digest changes with its content, an included page or a manifest above it, and with nothing else (0.6.0).
- Keep `license: MIT` in every manifest and skill and `LICENSE.md` at the root: a skill is served in full only under a license the indexer recognizes as permissive, and the check prints the license it resolved for each ([Licenses](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/skill-repo.md#licenses)).
- Put a folder's jobs at the front of its manifest's `description`, two sentences at most: first the jobs in the words a user asks with, then when to use the folder; tool names and the list of skills belong in the README. The connection instructions quote only the front of each folder's description within 2,000 characters in all, shorter with every area added ([Connection and prompt](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/tools.md#connection-and-prompt)); the check prints exactly what a client is told. The root manifest's `start` names the page a client is told to read before a task, `docs/pack/finding-a-skill.md`, which is how a fresh agent finds a skill; [guide/finding.md](guide/finding.md) says what bounds the finding as the pack grows and how it is checked.
- A reference that matters is `.md`, and a data file an agent must read is small JSON: nothing else is indexed.
- In an unquoted `description`, a colon followed by a space or a space followed by a hash makes the whole `SKILL.md` unreadable, and the skill is not served. Rephrase or quote; `scripts/check.mjs` rejects both.
- What every run reads is in `skillcdn.include`; what one phase reads is linked from that phase and costs no page of the load. A shared page's text is part of every skill that includes it, so an edit to it reaches each of them on the next load. The check prints what each skill weighs and where a page ends inside a table or a code block ([guide/skill-authoring.md](guide/skill-authoring.md), on size).
- The rules a tool family shares stay in each skill's hard rules, in the form that skill gives them: a manifest's rules reach only the skills below it, and a family can span areas. A set whose pages skills of two areas include sits at the root, because the format drops an include of a sibling area's page; a set whose including skills are all of one area stays in that area's `docs/`.
- `scripts/check.mjs` checks that a link's file exists; a fragment that names no section is the indexer's to report, so `npx @skillcdn/cli@latest check` is the check for fragments, and `check --references` the one for links to other packs (`skill://...`). Both read a fenced code block as code, not links, so a template of another repository's file may show its links there.
- A push is served within about a minute, and until then the deployment answers from the last indexed commit. A commit that was never pushed looks the same from the mount: `git status -sb` says whether `main` is ahead of `origin/main`. Before a fresh run, read the mount as `engineering/docs/skillcdn/serving.md` says, and push nothing while an agent is loading a skill.
- The README's skill tables are written by `npx @skillcdn/cli@latest catalog --write`, between the `skillcdn:catalog` comments, from each skill's first sentence. Edit the description, not the table; CI fails on a table that is behind.

**What this pack's own runs taught**

- Tool catalogs change under the skills. When a skill breaks because a parameter or a model went away, fix the discovery instruction, not just the value, so it does not break the same way twice.
- Some file-writing tools decode escape sequences on the way in: an escape such as U+00AD typed into a source file can land as the invisible character itself, which `scripts/check.mjs` then rejects. Build such characters with `String.fromCodePoint` and never paste them. Shell heredocs on Windows have their own trouble: the command line is truncated past a few thousand characters, so a long file written that way fails to parse or lands incomplete. Prefer the editor's file tools and let `.gitattributes` normalize to LF.
- A tool that is a website has no tool names and no changelog. The skill names capabilities (a shell with a browser, a browser the agent drives) and how to recognize them, and every fact about the site carries the date it was checked and the way to find it again; a remembered parameter or label is the first thing to break.
- Two skills that are each complete alone say nothing of the seam between them: which researched ad becomes the reference, what is taken over, whether the run goes on. A fresh agent improvised all three, and well, which proves nothing about the next one. The seam is written in the skill that needs the other's result, with a link to the other's `SKILL.md`; the other stays general (`guide/skill-authoring.md`), and it is tested with one request that needs both skills.
- Notes from real runs and worked examples are public too. A run's product, its persona, its lines, the reference it used and the advertisers it read stay out of them: record the behavior (a final consonant lost before a particle, a hook that gave the ending away), not the words that would let a reader find the site or the ad.
- The lockup at the top of the root README and the symbol at the top of every area's README are the brand files of `skillcdn/skillcdn`, linked by their raw URLs on its default branch (`packages/brand/`), because rendered files stay out of here (rule 3): a file renamed or moved there goes blank here, so check the URLs with a request after a release of SkillCDN. The pack's own picture is `assets/banner.webp`, shown by the explorer and the page of the address, not by the READMEs; a fork puts its own file at the path. The area images are results of the pack's own showcase, served by the deployment at `/media/<sha>`. The badge is served by SkillCDN for the address (`https://skillcdn.ai/badge/<address>`), and a fork keeps it with its own address. The indexer skips the HTML block when it takes a README's introduction, so the first Markdown paragraph after it is what the explorer shows.
- A manifest rule that only states a condition is passed over by an agent that has not tested it. A fresh agent read the console clause in the root rules and went on as if unbound, because it had never looked at its folder and would not run a command nobody explained; the rule works since it says to check before the first step, with `console whoami`, and that the command only reads. State the check, not only the condition, and what each of its outcomes means.
- A secret scan is not a security review. Material derived from private projects went through a review subagent before each push, told that the reader does not know the source and must not learn it; it caught what no scanner flags: a dated incident readable as a policy breach, a list of a real admin's weaknesses that doubled as an attack checklist, vocabulary that named the product category, a price pair copied from a real list, a `same-origin` referrer policy that leaked private URLs. Run it before every push of such material, and once more on the fixes.
- An alternative named without its method is the stand-in in disguise. The card news skills said "an image search" for a reference whose site is walled from the host; a fresh agent with a text-only search tool went past it to the stand-in, and another measured thumbnails off a results page. Write an alternative with the tools it takes, its steps, what its result lacks and its place in the order of fallbacks, as fully as the main route, and say that a go-ahead takes the first way the host allows. The order itself, the go-ahead and the fall-through live once in `docs/browser/walls.md`; a site's set says where else its material is published, and a skill names its own rungs.
- A route list without a preference order is read as a menu, and a fresh agent picks the item that needs no input. The card news build listed its routes to a format by what the user wants, and sessions given no reference recommended a format of the user's own every time. Write routes in the order of preference with the default first, ask for the input the default needs before offering a lesser route, and keep the order where every skill reads it: the root rule on starting from a reference.
- A sentence that restates the standard goes stale without anyone touching it. This section said that a manifest edit changes every skill's digest and that a link from `docs/` to `guide/` cannot be followed; both were wrong by the time a review read them. Say what the pack does and link the standard's section for the rest.
