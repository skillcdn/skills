<p align="center">
  <a href="https://skillcdn.ai"><img alt="SkillCDN" src="https://raw.githubusercontent.com/skillcdn/skillcdn/main/packages/brand/symbol.svg" width="72"></a>
</p>
<h1 align="center">design/</h1>
<p align="center">
  <a href="https://skillcdn.ai/gh/skillcdn/skills/design"><img alt="SkillCDN: skillcdn.ai/gh/skillcdn/skills/design" src="https://skillcdn.ai/badge/gh/skillcdn/skills/design"></a>
  <a href="../LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-3a6dd4"></a>
</p>

Skills for design work: slides and decks, card news posts and the formats they are built in, brand assets, icons and store graphics, made in the team's design tool, drafted as HTML and PDF before the tool, or varied as looks compared on a contact sheet. The area manifest next to this file ([SKILLCDN.md](SKILLCDN.md)) says who these skills are for and adds the rules every design skill follows on top of the repository's. The area mounts alone at `skillcdn.ai/gh/skillcdn/skills/design` and installs as the `design` plugin of the repository's Claude Code marketplace.

<!-- skillcdn:catalog -->
| Skill | What it does |
|---|---|
| [figma-slides-from-content](skills/figma-slides-from-content/SKILL.md) | Moves a document (a proposal, a report, any PDF) into an existing Figma Slides deck as new slides, one per page, built in the deck's own design system rather than a generic one. |
| [html-card-news-batch](skills/html-card-news-batch/SKILL.md) | Makes several card news posts at once from picked topics and one format. |
| [html-card-news-from-brief](skills/html-card-news-from-brief/SKILL.md) | Builds an Instagram card news carousel from a sourced topic brief in a format spec's format, as HTML rendered to PNG, with an mp4 for a slide whose picture is a clip of the brief's; with no spec or b… |
| [html-deck-from-outline](skills/html-deck-from-outline/SKILL.md) | Drafts a slide deck as one HTML file and a PDF from notes, a meeting plan or an idea, as a corporate report (a business plan, a plan for investors, a company presentation, an internal report) or an e… |
| [html-design-variations](skills/html-design-variations/SKILL.md) | Shows four looks for one design (a page's first screen, a deck's cover, a card news format) as HTML rendered in a browser and tiled on one contact sheet, from a reference, a concept or the thing as i… |
| [html-product-deck](skills/html-product-deck/SKILL.md) | Makes a product deck that sells a product or one of its features to buyers, as one HTML file and a PDF, every slide one message in a scene composed for it (a real screen, a scene drawn in the product… |
| [html-signal-magazine](skills/html-signal-magazine/SKILL.md) | Makes one issue of a market signal magazine as a deck, one HTML file and a PDF, from market research already done: every slide one message carried by a chart or a picture composed for it, in the look… |
| [instagram-card-news-format-study](skills/instagram-card-news-format-study/SKILL.md) | Studies the card news of a reference Instagram account, of one reference post, or of a few accounts of a genre, and writes the format as a spec a new post can be built in, from the posts visible with… |

8 skills.
<!-- /skillcdn:catalog -->

The card news skills chain. `html-card-news-from-brief` takes its format from `instagram-card-news-format-study`, as measured or as `html-design-variations` varied it at the user's pick, and its facts and images from the product area's `web-card-news-topic-brief`; with no spec it asks for the reference and offers the routes to one in their order, the reference varied first, with no brief the research, and runs what the user chooses before its plan; the study, the variations and the research stay general. `html-card-news-batch` runs the research and the build for several posts at once through worker agents, and is the orchestration alone.

Documents for this area go in `docs/` next to this file, where SkillCDN discovers them by default; there are none yet, and the Figma skill keeps what it knows about its tool in its own `references/` until a second Figma skill shares it. The card news skills read the routes to a format spec and the shape of the spec and the brief they pass between them from the repository's [`docs/card-news/`](../docs/card-news/README.md), shared with the research skill in `product/`; the deck and the card news skills read what every browser skill shares from [`docs/browser/`](../docs/browser/README.md), the variations what every variation skill shares from [`docs/variation/`](../docs/variation/README.md), and the study how Instagram is read without signing in from [`docs/instagram/`](../docs/instagram/README.md).

How to write a skill: [guide/skill-authoring.md](../guide/skill-authoring.md). How to add one here: [guide/adding.md](../guide/adding.md). The table is written by `npx @skillcdn/cli@latest catalog --write`, from each skill's first sentence; `node scripts/check.mjs` fails when a skill is missing from it.
