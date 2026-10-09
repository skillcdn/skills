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

Documents for this area go in `docs/` next to this file, where SkillCDN discovers them by default; there are none yet.

How to write a skill: [guide/skill-authoring.md](../guide/skill-authoring.md). How to add one here: [guide/adding.md](../guide/adding.md), or the authoring skill above, which does those steps from the work already done. The `node scripts/check.mjs` check fails when a skill directory is missing from this table.
