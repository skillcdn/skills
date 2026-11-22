<p align="center">
  <a href="https://skillcdn.ai"><img alt="SkillCDN" src="https://raw.githubusercontent.com/skillcdn/skillcdn/main/packages/brand/symbol.svg" width="72"></a>
</p>
<h1 align="center">product/</h1>
<p align="center">
  <a href="https://skillcdn.ai/gh/skillcdn/skills/product"><img alt="SkillCDN: skillcdn.ai/gh/skillcdn/skills/product" src="https://skillcdn.ai/badge/gh/skillcdn/skills/product"></a>
  <a href="../LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-3a6dd4"></a>
</p>

Skills for product planning and research: discovery (what is taking off in a market), research synthesis, a sourced brief of a story, concept directions and alternatives, requirements, specifications, roadmaps, prioritization. The area manifest next to this file ([SKILLCDN.md](SKILLCDN.md)) says who these skills are for and adds the rules every product skill follows on top of the repository's. The area mounts alone at `skillcdn.ai/gh/skillcdn/skills/product` and installs as the `product` plugin of the repository's Claude Code marketplace.

<!-- skillcdn:catalog -->
| Skill | What it does |
|---|---|
| [dart-company-figures](skills/dart-company-figures/SKILL.md) | Finds a Korean company's revenue and operating profit in its filings on DART, the Financial Supervisory Service's disclosure site, and checks what the company announced against them. |
| [meta-ad-library-rising-products](skills/meta-ad-library-rising-products/SKILL.md) | Finds what is taking off in a market or a field of work, such as AI tools, by what its advertisers are putting new money behind, read from the public Meta Ad Library with a browser. |
| [web-card-news-topic-brief](skills/web-card-news-topic-brief/SKILL.md) | Finds what is worth a card news post now in the categories an account covers, in the outlets and where people are talking, lets the user pick, and turns the pick into a sourced topic brief a post can… |
| [web-concept-variations](skills/web-concept-variations/SKILL.md) | Shows four to six concept directions that get a reference's effect by other means, for a product, a post, a page, a deck or a campaign, from a reference the user gives or one found among what is work… |
| [web-item-deep-dive](skills/web-item-deep-dive/SKILL.md) | Reviews one business idea in depth before anything is built, as one document with what exactly is sold to whom and who pays, how big the market is and when in the year it buys, who already sells it (… |
| [web-market-entry-signals](skills/web-market-entry-signals/SKILL.md) | Finds which markets are worth entering now, from official statistics, filings, app stores and the ads running, in Korea and the US by default, and measures the watched markets again later. |

6 skills.
<!-- /skillcdn:catalog -->

Documents for this area go in `docs/` next to this file, where SkillCDN discovers them by default; there are none yet. The concept skill reads what every variation skill shares from the repository's [`docs/variation/`](../docs/variation/README.md); the research skill reads the shape of the brief it writes from the repository's [`docs/card-news/`](../docs/card-news/README.md), shared with the card news build in `design/`, and how a page is read in full from [`docs/browser/`](../docs/browser/README.md); the rising products skill reads what the two Meta Ad Library skills share from [`docs/meta-ad-library/`](../docs/meta-ad-library/README.md), the other being the creative research in `marketing/`.

How to write a skill: [guide/skill-authoring.md](../guide/skill-authoring.md). How to add one here: [guide/adding.md](../guide/adding.md). The table is written by `npx @skillcdn/cli@latest catalog --write`, from each skill's first sentence; `node scripts/check.mjs` fails when a skill is missing from it.
