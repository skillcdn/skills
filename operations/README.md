<p align="center">
  <a href="https://skillcdn.ai"><img alt="SkillCDN" src="https://raw.githubusercontent.com/skillcdn/skillcdn/main/apps/web/public/brand/symbol.svg" width="72"></a>
</p>
<h1 align="center">operations/</h1>
<p align="center">
  <a href="https://skillcdn.ai/gh/skillcdn/skills/operations"><img alt="SkillCDN: skillcdn.ai/gh/skillcdn/skills/operations" src="https://skillcdn.ai/badge/gh/skillcdn/skills/operations"></a>
  <a href="../LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-3a6dd4"></a>
</p>

Skills for running the company's and its clients' work day to day: the minutes of a meeting sent the same day, status reports, visit logs, handovers, the records an engagement keeps. The area manifest next to this file ([SKILLCDN.md](SKILLCDN.md)) says who these skills are for and adds the rules every operations skill follows on top of the repository's. The area mounts alone at `skillcdn.ai/gh/skillcdn/skills/operations` and installs as the `operations` plugin of the repository's Claude Code marketplace.

| Skill | Tool family | What it does |
|---|---|---|
| [`skills/html-meeting-minutes-from-notes/`](skills/html-meeting-minutes-from-notes/) | Browser | The minutes of a client meeting as one self-contained HTML file and an A4 PDF, from the notes a person brings back, for sending the same day. Sort the notes into decisions, questions and answers, items to confirm, actions and the next meeting, with what was said for the organization's own ears kept out and listed; write one minutes file with a four-row header table and numbered sections; render it in grayscale with the client's logo before the organization's, check the wording against the declared house style, print the PDF with a Chromium-family browser, look at the preview and the page breaks, and deliver both files into the client's folder with what to confirm before sending. Sending is the user's own step. Nothing is spent. |

Documents for this area go in `docs/` next to this file, where SkillCDN discovers them by default; there are none yet. The minutes skill reads what every browser skill shares from the repository's [`docs/browser/`](../docs/browser/README.md), as the deck and card news skills in `design/` do.

How to write a skill: [guide/skill-authoring.md](../guide/skill-authoring.md). How to add one here: [guide/adding.md](../guide/adding.md). The `node scripts/check.mjs` check fails when a skill directory is missing from this table.
