<p align="center">
  <a href="https://skillcdn.ai"><img alt="SkillCDN" src="https://raw.githubusercontent.com/skillcdn/skillcdn/main/packages/brand/symbol.svg" width="72"></a>
</p>
<h1 align="center">writing/</h1>
<p align="center">
  <a href="https://skillcdn.ai/gh/skillcdn/skills/writing"><img alt="SkillCDN: skillcdn.ai/gh/skillcdn/skills/writing" src="https://skillcdn.ai/badge/gh/skillcdn/skills/writing"></a>
  <a href="../LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-3a6dd4"></a>
</p>

Skills whose result is the text itself, read or heard as it is: a news script, an article, a report, a self-introduction, a briefing. The area manifest next to this file ([SKILLCDN.md](SKILLCDN.md)) says who these skills are for and adds the rules every writing skill follows on top of the repository's. The area mounts alone at `skillcdn.ai/gh/skillcdn/skills/writing`, and installs as the `writing` plugin of the repository's Claude Code marketplace.

<!-- skillcdn:catalog -->
| Skill | What it does |
|---|---|
| [web-news-anchor-report-script](skills/web-news-anchor-report-script/SKILL.md) | Writes the script of a news anchor report from a sourced story, with the screen planned cut by cut for a video made later, about ninety seconds unless asked otherwise. |

1 skill.
<!-- /skillcdn:catalog -->

The other kinds of text planned here, each a job with its status, are in [guide/roadmap.md](../guide/roadmap.md) "M9: Writing". A skill is written from the job done once ([guide/adding.md](../guide/adding.md)).

What every text shares, whichever skill writes it, is the repository's document set [`docs/writing/`](../docs/writing/README.md): the reader and the register, sentences, facts and quotes, what leaves the organization, the house style. It sits at the root because skills of other areas write text too (a deck's slides, the minutes of a meeting, a post's script) and read the same pages. Documents for this area alone go in `docs/` next to this file, where SkillCDN discovers them by default; there are none yet.

How to write a skill: [guide/skill-authoring.md](../guide/skill-authoring.md). How to add one here: [guide/adding.md](../guide/adding.md). What went into the writing set and what stays in each skill: [guide/writing.md](../guide/writing.md). The table is written by `npx @skillcdn/cli@latest catalog --write`, from each skill's first sentence; `node scripts/check.mjs` fails when a skill is missing from it.
