<p align="center">
  <a href="https://skillcdn.ai"><img alt="SkillCDN" src="https://raw.githubusercontent.com/skillcdn/skillcdn/main/apps/web/public/brand/symbol.svg" width="72"></a>
</p>
<h1 align="center">design/</h1>
<p align="center">
  <a href="https://skillcdn.ai/gh/skillcdn/skills/design"><img alt="SkillCDN: skillcdn.ai/gh/skillcdn/skills/design" src="https://skillcdn.ai/badge/gh/skillcdn/skills/design"></a>
  <a href="../LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-3a6dd4"></a>
</p>

Skills for design work: slides and decks, brand assets, icons and store graphics, made in the team's design tool, or drafted as HTML and PDF before the tool. The area manifest next to this file ([SKILLCDN.md](SKILLCDN.md)) says who these skills are for and adds the rules every design skill follows on top of the repository's. The area mounts alone at `skillcdn.ai/gh/skillcdn/skills/design` and installs as the `design` plugin of the repository's Claude Code marketplace.

| Skill | Tool family | What it does |
|---|---|---|
| [`skills/figma-slides-from-content/`](skills/figma-slides-from-content/) | Figma | A document (a proposal, a report, any PDF) moved into an existing Figma Slides deck as new slides, one per page, in the deck's own design system. Read the document's text with its sizes, positions and breaks and its images, measure the existing slides for the type scale, colors, margins, title treatment, bullet marks, cards and shadows, plan one slide per page with a layout type, build through the Figma MCP server, and audit every slide by numbers and zoomed renders: alignment on the glyphs, one spec per element role, nothing outside a card's padding, no word broken mid-way. Existing and user-edited slides stay untouched. |
| [`skills/html-deck-from-outline/`](skills/html-deck-from-outline/) | Browser | A first-draft slide deck (a kickoff presentation, a proposal, a status report) as one self-contained HTML file and a PDF from a content outline. Turn the outline into a deck file in which every slide is a type and a list of blocks (a statement beside a definition list, numbered rows, a loop, a Gantt-style schedule, a system diagram with a process strip, brand panels with real logos, team profiles), render it at a fixed 16:9 page size in the organization's own tokens, print the PDF with a Chromium-family browser, check the wording against the house style the deck declares, and review a contact sheet of every page before delivery; structure from type, rules and real marks, with no icon card grids. A designer then polishes a finished structure. Nothing is spent. |

Documents for this area will live in a `docs/` directory next to this file, discovered there once a second Figma skill shares knowledge with the first; until then each skill carries what it knows about its tool in its own `references/`, and the deck skill reads what every browser skill shares from the repository's [`docs/browser/`](../docs/browser/README.md).

How to write a skill: [guide/skill-authoring.md](../guide/skill-authoring.md). How to add one here: [guide/adding.md](../guide/adding.md). The `node scripts/check.mjs` check fails when a skill directory is missing from this table.
