<p align="center">
  <a href="https://skillcdn.ai"><img alt="SkillCDN" src="https://raw.githubusercontent.com/skillcdn/skillcdn/main/apps/web/public/brand/symbol.svg" width="72"></a>
</p>
<h1 align="center">media/</h1>
<p align="center">
  <a href="https://skillcdn.ai/gh/skillcdn/skills/media"><img alt="SkillCDN: skillcdn.ai/gh/skillcdn/skills/media" src="https://skillcdn.ai/badge/gh/skillcdn/skills/media"></a>
  <a href="../LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-3a6dd4"></a>
</p>

Skills for original video and audio content: scripted short dramas, series episodes and other story-driven shorts. The area manifest next to this file ([SKILLCDN.md](SKILLCDN.md)) says who these skills are for and adds the rules every media skill follows on top of the repository's. The area mounts alone at `skillcdn.ai/gh/skillcdn/skills/media` and installs as the `media` plugin of the repository's Claude Code marketplace.

| Skill | Tool family | What it does |
|---|---|---|
| [`skills/higgsfield-shorts-drama/`](skills/higgsfield-shorts-drama/) | Higgsfield | One episode of an original vertical short drama (9:16, about 150 seconds) from a premise or a series bible. Write or update the bible and the episode's cut table, keep a who-knows-what table so every twist holds for the viewer, confirm the latest qualifying model with its credit estimate before anything is generated, approve portraits, sets and a still first frame per cut, animate one cut at a time with the model speaking every line, verify each line with two plain speech-to-text decodes, regenerate only failed cuts, and burn subtitles, name cards and inserts in code. Delivers the episode, a contact sheet, the credit ledger and a production log the next episode starts from. |

Documents for this area go in `docs/` next to this file, where SkillCDN discovers them by default; there are none yet.

How to write a skill: [guide/skill-authoring.md](../guide/skill-authoring.md). How to add one here: [guide/adding.md](../guide/adding.md). The `node scripts/check.mjs` check fails when a skill directory is missing from this table.
