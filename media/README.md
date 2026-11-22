<p align="center">
  <a href="https://skillcdn.ai"><img alt="SkillCDN" src="https://raw.githubusercontent.com/skillcdn/skillcdn/main/packages/brand/symbol.svg" width="72"></a>
</p>
<h1 align="center">media/</h1>
<p align="center">
  <a href="https://skillcdn.ai/gh/skillcdn/skills/media"><img alt="SkillCDN: skillcdn.ai/gh/skillcdn/skills/media" src="https://skillcdn.ai/badge/gh/skillcdn/skills/media"></a>
  <a href="../LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-3a6dd4"></a>
</p>

Skills for original video and audio content: scripted short dramas, series episodes and other story-driven shorts. The area manifest next to this file ([SKILLCDN.md](SKILLCDN.md)) says who these skills are for and adds the rules every media skill follows on top of the repository's. The area mounts alone at `skillcdn.ai/gh/skillcdn/skills/media` and installs as the `media` plugin of the repository's Claude Code marketplace.

<!-- skillcdn:catalog -->
| Skill | What it does |
|---|---|
| [higgsfield-shorts-drama](skills/higgsfield-shorts-drama/SKILL.md) | Makes one episode of an original vertical short drama (9:16, about 150 seconds by default) on Higgsfield from a premise or an existing series bible. |

1 skill.
<!-- /skillcdn:catalog -->

Documents for this area go in `docs/` next to this file, where SkillCDN discovers them by default; there are none yet.

How to write a skill: [guide/skill-authoring.md](../guide/skill-authoring.md). How to add one here: [guide/adding.md](../guide/adding.md). The table is written by `npx @skillcdn/cli@latest catalog --write`, from each skill's first sentence; `node scripts/check.mjs` fails when a skill is missing from it.
