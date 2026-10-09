<p align="center">
  <a href="https://skillcdn.ai"><img alt="SkillCDN" src="https://raw.githubusercontent.com/skillcdn/skillcdn/main/apps/web/public/brand/symbol.svg" width="72"></a>
</p>
<h1 align="center">engineering/</h1>
<p align="center">
  <a href="https://skillcdn.ai/gh/skillcdn/skills/engineering"><img alt="SkillCDN: skillcdn.ai/gh/skillcdn/skills/engineering" src="https://skillcdn.ai/badge/gh/skillcdn/skills/engineering"></a>
  <a href="../LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-3a6dd4"></a>
</p>

Skills for software development and for the tooling an agent works with: writing and changing code, keeping a codebase's documents true to it, building apps, testing, debugging, and making skills from work done. The area manifest next to this file ([SKILLCDN.md](SKILLCDN.md)) says who these skills are for and adds the rules every engineering skill follows on top of the repository's. The area mounts alone at `skillcdn.ai/gh/skillcdn/skills/engineering` and installs as the `engineering` plugin of the repository's Claude Code marketplace.

| Skill | Tool family | What it does |
|---|---|---|
| [`skills/skillcdn-skill-authoring/`](skills/skillcdn-skill-authoring/) | SkillCDN | A skill in this repository, or in a fork of it, from work a person and an agent have already done. Read the session first, then earlier transcripts, memory and results where the user points; keep the method and leave the product and the people out; design what is asked, what is derived, where the user is consulted and what makes a result accepted; write the skill in this layout with discovery in place of values; validate it; have a fresh agent follow the files alone; ship it with its catalog rows. Also folds a run's findings back into an existing skill. |
| [`skills/skillcdn-skill-verification/`](skills/skillcdn-skill-verification/) | SkillCDN | A skill of this repository, or of a fork of it, verified the way a user's agent will meet it. A fresh agent dry-reads its files for every place it would have to guess; a fresh agent runs the served skill through SkillCDN with its checkpoints answered as the user would; each finding is folded into the sentence it bears on, checked, and pushed on the user's word. Works on what is served, on a local change before it is pushed, and after a tool, a model or a shared page changed under the skill. |

Documents for this area are in [`docs/`](docs/README.md) next to this file, where SkillCDN discovers them by default: [`docs/skillcdn/`](docs/skillcdn/README.md) holds what the SkillCDN skills share.

How to write a skill: [guide/skill-authoring.md](../guide/skill-authoring.md). How to add one here: [guide/adding.md](../guide/adding.md), or the authoring skill above, which does those steps from the work already done; the verification skill tries a skill again from a fresh session after it changed. The `node scripts/check.mjs` check fails when a skill directory is missing from this table.
