<p align="center">
  <a href="https://skillcdn.ai"><img alt="SkillCDN" src="https://raw.githubusercontent.com/skillcdn/skillcdn/main/apps/web/public/brand/symbol.svg" width="72"></a>
</p>
<h1 align="center">marketing/</h1>
<p align="center">
  <a href="https://skillcdn.ai/gh/skillcdn/skills/marketing"><img alt="SkillCDN: skillcdn.ai/gh/skillcdn/skills/marketing" src="https://skillcdn.ai/badge/gh/skillcdn/skills/marketing"></a>
  <a href="../LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-3a6dd4"></a>
</p>

Skills for marketing and growth work: ads, ad and product research, promotional video, content, campaigns, social posts. The area manifest next to this file ([SKILLCDN.md](SKILLCDN.md)) says who these skills are for and adds the rules every marketing skill follows on top of the repository's. The area mounts alone at `skillcdn.ai/gh/skillcdn/skills/marketing` and installs as the `marketing` plugin of the repository's Claude Code marketplace.

| Skill | Tool family | What it does |
|---|---|---|
| [`skills/higgsfield-shorts-ad/`](skills/higgsfield-shorts-ad/) | Higgsfield | A vertical short-form AI ad from just a reference video and a product link. Learn what makes the reference work (its hook, the rule its story runs on, its measured pacing), write an original story on the product's own world in its medium (live action or animation), derive the rest, approve generated cast portraits and a first frame per shot, confirm a recommended model with its credit estimate, animate one directed draft take at a time, edit and caption in the brand's type in code. With no reference, it first finds one among running ads, with the creative research skill. |
| [`skills/meta-ad-library-creative-research/`](skills/meta-ad-library-creative-research/) | Meta Ad Library | Research on the ad creatives running for a keyword, a product or a competitor, read from the public library with a browser. Find the ads that show proof of working (their place in the impressions order, days running, reuse of the creative, the advertiser's volume), recent ones first, read videos frame by frame, and deliver a report: the landscape, a linked shortlist, a breakdown of each hook, angle, structure and offer, the patterns across them, and directions for the user's own ads. |
| [`skills/meta-ad-library-rising-products/`](skills/meta-ad-library-rising-products/) | Meta Ad Library | What advertisers are putting the most new advertising behind in a sector or a field, read from the public library with a browser: items, each one seller's (goods by default; apps, tools, services or courses where the sector is made of them), and the themes several sellers share. Group ads by seller, count each entry's active ads and those started in the last 7, 30 and 90 days, class it as a breakout, a new push or proven with its pace this week, and deliver a ranked report with the ads, the sellers, the offer and the risks, with a snapshot the next run measures real growth against. |

The skills chain. "Make an ad for this product", with no reference, has `higgsfield-shorts-ad` find one first with `meta-ad-library-creative-research` and choose among its shortlist; the research skill itself stays general.

Documents for this area live in [`docs/`](docs/), discovered next to this file. The first set, [`docs/meta-ad-library/`](docs/meta-ad-library/), holds what the two Meta Ad Library skills share (the routes into the library and their code, the URL parameters, the record a result yields, counting by age, manners and limits); each of the two skills includes `ad-library.md`, and the rest is read through the repository or the area connection and shipped with the `marketing` plugin.

How to write a skill: [guide/skill-authoring.md](../guide/skill-authoring.md). How to add one here: [guide/adding.md](../guide/adding.md). The `node scripts/check.mjs` check fails when a skill directory is missing from this table.
