# SkillCDN skills

Skills for an AI agent to do real company work. From marketing to design, engineering and customer support.

| You say | You get |
|---|---|
| "Make an ad for this product." | A captioned vertical ad built on a reference that is working now. |
| "What is taking off in this market?" | A ranked report of what advertisers are putting new money behind, with a snapshot the next run measures growth against. |
| "Research the ads running for this keyword." | The creatives that show proof of working, each broken down, with directions for your own ads. |
| "Make episode one of a short drama from this premise." | A vertical short-drama episode with every line spoken by the video model and verified, subtitles and name cards in code, and a series bible and log the next episode starts from. |

Each folder is an area of work with the skills that do it and the documents its people read: marketing and media have the first skills, product and engineering are next, and more areas will follow. This is also the reference repository for the [SkillCDN Format](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/skill-repo.md): the shape SkillCDN proposes for a skill repository, kept working against real tools. Fork it to publish your own skills in the same shape.

[SkillCDN](https://github.com/skillcdn/skillcdn) turns a git repository into an MCP server. Point an agent at an address and it gets what the address covers:

```
skillcdn.ai/gh/skillcdn/skills                                        the whole repository (recommended)
skillcdn.ai/gh/skillcdn/skills/marketing                              one area
skillcdn.ai/gh/skillcdn/skills/marketing/skills/higgsfield-shorts-ad  one skill
skillcdn.ai/gh/skillcdn/skills@<commit>                               pinned to a commit
```

A host that implements the MCP skills extension receives these skills as skills: each `SKILL.md` arrives as a plain Agent Skills document with the repository's rules, the area's rules and the references every run needs inside it, listed with a digest per file under `skill://gh/skillcdn/skills/<path>`. Any other MCP client reaches the same skills through the server's tools: `browse_repo`, `search_repo`, `load_skill` and `read_repo_file`.

The same folders work without SkillCDN. Every skill is a plain [Agent Skills](https://agentskills.io/specification) folder: copy `<area>/skills/<name>/` into any agent that reads `SKILL.md`. Every area with skills is a [Claude Code](https://code.claude.com/docs/en/plugins) plugin: `claude plugin marketplace add skillcdn/skills`, then `claude plugin install marketing@skillcdn`. Only through SkillCDN do the rules in [SKILLCDN.md](SKILLCDN.md) and the area's manifest arrive with every skill; a copied or installed skill relies on its own hard rules, and reads the pages its tool family shares (`docs/<family>/`) from this repository on the git host.

## Areas

One folder per area of work. Each carries a `SKILLCDN.md` that says who its skills are for and adds the rules they share, a `README.md` that lists them, its skills under `skills/`, and the documents its people read under `docs/`.

| Area | For | Skills |
|---|---|---|
| [`marketing/`](marketing/) | Ads, ad and product research, promotional video, content, campaigns, social posts. | 3 |
| [`product/`](product/) | Discovery, research synthesis, requirements, specifications, roadmaps, prioritization. | none yet |
| [`engineering/`](engineering/) | Software development: writing and changing code, building apps, code review, testing, debugging. | none yet |
| [`media/`](media/) | Original video and audio content: scripted short dramas, series episodes, story-driven shorts. | 1 |

Areas to come, each with its first skill: design, sales, support, operations, data, finance, legal, people. The naming rule and the steps are in [guide/adding.md](guide/adding.md).

## Skills

| Skill | Area | Tool family | What it does |
|---|---|---|---|
| [`marketing/skills/higgsfield-shorts-ad/`](marketing/skills/higgsfield-shorts-ad/) | Marketing | Higgsfield | Makes a vertical short-form AI ad from just a reference video and a product link: learns what makes the reference work (its hook, the rule its story runs on, its measured pacing) and writes an original story on the product's own world, derives language, length, medium and the brand's typography itself, has the user approve generated cast portraits and a still first frame per shot, directs each performance, recommends the latest Kling or Seedance model with a credit estimate, animates one draft-quality take at a time, and adds captions, text and the end card with code-based editing. With no reference, it first finds one among running ads, with the creative research skill. |
| [`marketing/skills/meta-ad-library-creative-research/`](marketing/skills/meta-ad-library-creative-research/) | Marketing | Meta Ad Library | Researches the ad creatives running for a keyword, a product or a competitor by reading the public library with a browser: finds the ads that show proof of working (their place in the impressions order, days running, reuse of the creative, the advertiser's volume), puts recent ones first, reads videos frame by frame, and delivers a report with the landscape, a linked shortlist, a breakdown of each hook, angle, structure and offer, the patterns across them, and directions for the user's own ads. |
| [`marketing/skills/meta-ad-library-rising-products/`](marketing/skills/meta-ad-library-rising-products/) | Marketing | Meta Ad Library | Finds what is taking off in a market or a field by where advertisers are putting new money, reading the public library with a browser: sweeps a sector or purchase phrases, groups ads by seller, counts for each item (a product, or an app, a tool, a service or a course) and for each theme several sellers share the active ads and those started in the last 7, 30 and 90 days, classes it as a breakout, a new push or proven with its pace this week, and delivers a ranked report with the ads, the sellers, the offer and the risks, plus a snapshot the next run measures real growth against. |
| [`media/skills/higgsfield-shorts-drama/`](media/skills/higgsfield-shorts-drama/) | Media | Higgsfield | Makes one episode of an original vertical short drama (9:16, about 150 seconds) from a premise or a series bible: writes or updates the bible and the episode's cut table, keeps a who-knows-what table so every twist holds for the viewer, confirms the latest qualifying model with its credit estimate before anything is generated, has the user approve portraits, sets and a still first frame per cut, animates one cut at a time with the model speaking every line, verifies each line with two plain speech-to-text decodes, regenerates only failed cuts, burns subtitles, name cards and inserts in code, and delivers the episode with a credit ledger and a production log the next episode starts from. |

## Document sets

Directories of Markdown without a `SKILL.md`, read by an agent through `search_repo` and `read_repo_file` without any skill: the playbooks, handbooks and product documentation an area's people work from, and what the skills of one tool family share. They live in [`docs/`](docs/) when they serve every area and in `<area>/docs/` when they serve one.

| Document set | What it holds |
|---|---|
| [`docs/higgsfield/`](docs/higgsfield/) | What the skills that drive Higgsfield share, whichever area they are in: how the sandbox behaves, how models and credits are found and quoted, how portraits and first frames are made, how a take is decoded, and what the video models do with the sounds of each language, as real runs showed it. One file per topic, organized by what holds now; each skill links it from the phase that reads it. |

## Where things live

Four scopes, each with one place, so that nothing is written twice and a finding is kept current where every reader looks:

| What | Where | How it reaches the agent |
|---|---|---|
| A rule for every skill | The body of [`SKILLCDN.md`](SKILLCDN.md) | Paged before every skill, on every mount |
| A rule for every skill of one area | The body of `<area>/SKILLCDN.md` | Paged before every skill of the area |
| What the skills of one tool family share: how its tools behave, what they did in runs, the knowledge every run adds to | `docs/<family>/`, one file per topic | Read on demand through the repository connection, from the phase that links it |
| A skill's own workflow, checkpoints, verdicts, hard rules and craft | `<area>/skills/<name>/` | With the skill, wherever it is mounted, installed or copied |

Areas are by function, and a tool family can serve several of them, which is why what its skills share sits at the root; a family whose skills all sit in one area keeps it in that area's `docs/`, which travels with the area's mount and its plugin. A skill carries what it cannot work without, so that it still works alone; what it shares it reads from one place, so that a run's finding is written once. A rule the family shares (the model speaks, overlays are code, two plain decodes decide what was said) stays in each skill's hard rules, in the form that skill gives it, because a manifest's rules reach only the skills below it.

## Tool families

| Family | What it is | How the user connects it | Documentation |
|---|---|---|---|
| Higgsfield | AI image, video and audio generation with a cloud sandbox for editing. | Add the Higgsfield MCP server to the agent. Skills check for the tools they need and ask for the server when it is missing. | [higgsfield.ai](https://higgsfield.ai) |
| Meta Ad Library | Meta's public library of the ads running on Facebook, Instagram, Messenger, Threads and WhatsApp, read as a website because its API leaves out most commercial ads. | Nothing to connect. The agent needs a shell with a Chromium-family browser, or a browser it can drive; skills check which one it has and say what to add when it has neither. | [facebook.com/ads/library](https://www.facebook.com/ads/library) |

## Using a skill

1. Add an address above as a remote MCP server in your agent, install an area as a Claude Code plugin, or copy a skill folder into your agent's skills directory.
2. Ask for what the skill does, in your own words. The skill's `description` is what the agent matches on.
3. Connect the tools the skill names under "Requirements". A skill stops and asks when one is missing.

Skills that spend money or credits always estimate first and wait for your approval.

## Make it yours

This repository takes no pull requests. It is meant to be forked: the layout, the checks, the CI and the rules for agents come with the fork, and your skills go in.

1. Fork the repository, or copy it into a new one.
2. In `SKILLCDN.md`, set `name`, `description`, `translations` and `metadata.author` to yours. Keep the rules that hold for you; change the rest.
3. Keep a license SkillCDN can pass on. It serves a skill in full only under a license it recognizes as permissive, taken from the skill's directory, its `license` field, the manifests above it or the repository's license file; under a restrictive or unrecognized license the skill is only described, with a link to its source.
4. Keep the areas you need and delete the others. A new area is a folder with a `SKILLCDN.md` and a `README.md`; the steps are in [guide/adding.md](guide/adding.md).
5. Write your skills at `<area>/skills/<name>/`, following [guide/skill-authoring.md](guide/skill-authoring.md); put what the skills of one tool share in `docs/<tool>/`. Run `node scripts/check.mjs`; CI runs it on every push.
6. Rewrite this README for your repository. In `.claude-plugin/marketplace.json`, set `name` and `owner` to yours and list the areas that have skills.
7. Connect it at `skillcdn.ai/gh/<you>/<repo>`. A public repository needs no setup.

The rules for changing anything, for people and agents alike, are in [CLAUDE.md](CLAUDE.md); a fork keeps them or changes them. A skill here that no longer works can be reported in an issue.

## Repository layout

```
SKILLCDN.md       the repository manifest: name, description, document roots, the rules for every skill
README.md         this introduction
<area>/           one folder per area of work: marketing/, media/, product/, engineering/, ...
  SKILLCDN.md     the area manifest: who its skills are for, the rules its skills add
  README.md       the area's catalog
  skills/<name>/  one directory per skill: SKILL.md, references/, assets/, optional scripts/
  docs/           the area's document sets
docs/             document sets that serve every area, docs/<family>/ for what a tool family's skills share
guide/            how skills in this layout are written and how to add to a repository like this one
scripts/          check.mjs, the validation CI runs
.claude-plugin/   the Claude Code marketplace: one plugin per area with skills
```

What an agent connected through SkillCDN gets: the skills, the manifests and the document sets are discoverable with `browse_repo` and `search_repo`, and the skills are listed through the MCP skills extension; this README, an area's README and the pages they link are readable on demand with `read_repo_file`; everything else stays on the git host.

```sh
node scripts/check.mjs    # validates manifests, front-matter, catalogs, links and text; needs Node.js 24, no install
```

From a checkout of SkillCDN, `pnpm --filter @skillcdn/server run start check ../skills` reads the repository with the indexer itself and prints what an agent is told.

## License

The content of this repository is under the [MIT License](LICENSE.md), a license SkillCDN recognizes as permissive, which is why it serves these skills in full. "SkillCDN" is a trademark of KDX Labs Corp.; its [trademark policy](https://github.com/skillcdn/skillcdn/blob/main/TRADEMARKS.md) allows everyone the file name `SKILLCDN.md`, the `skillcdn` front-matter key and the name of the format, so a fork keeps them. The tools the skills drive are third-party products with their own terms.

Built by KDX Labs. Copyright (c) 2026 KDX Labs Corp.
