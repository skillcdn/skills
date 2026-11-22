<p align="center">
  <a href="https://skillcdn.ai"><img alt="SkillCDN" src="https://raw.githubusercontent.com/skillcdn/skillcdn/main/packages/brand/symbol.svg" width="72"></a>
</p>
<h1 align="center">operations/</h1>
<p align="center">
  <a href="https://skillcdn.ai/gh/skillcdn/skills/operations"><img alt="SkillCDN: skillcdn.ai/gh/skillcdn/skills/operations" src="https://skillcdn.ai/badge/gh/skillcdn/skills/operations"></a>
  <a href="../LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-3a6dd4"></a>
</p>

Skills for running the company's and its clients' work day to day: the minutes of a meeting sent the same day, status reports, visit logs, handovers, the records an engagement keeps. The area manifest next to this file ([SKILLCDN.md](SKILLCDN.md)) says who these skills are for and adds the rules every operations skill follows on top of the repository's. The area mounts alone at `skillcdn.ai/gh/skillcdn/skills/operations` and installs as the `operations` plugin of the repository's Claude Code marketplace.

<!-- skillcdn:catalog -->
| Skill | What it does |
|---|---|
| [html-meeting-minutes-from-notes](skills/html-meeting-minutes-from-notes/SKILL.md) | Writes the minutes of a client meeting as one HTML file and an A4 PDF from the notes a person brings back (what was decided, what is still to be confirmed, who does what by when, the next meeting), f… |

1 skill.
<!-- /skillcdn:catalog -->

Documents for this area go in `docs/` next to this file, where SkillCDN discovers them by default; there are none yet. The minutes skill reads what every browser skill shares from the repository's [`docs/browser/`](../docs/browser/README.md), as the deck and card news skills in `design/` do.

How to write a skill: [guide/skill-authoring.md](../guide/skill-authoring.md). How to add one here: [guide/adding.md](../guide/adding.md). The table is written by `npx @skillcdn/cli@latest catalog --write`, from each skill's first sentence; `node scripts/check.mjs` fails when a skill is missing from it.
