<p align="center">
  <a href="https://skillcdn.ai"><img alt="SkillCDN" src="https://raw.githubusercontent.com/skillcdn/skillcdn/main/packages/brand/symbol.svg" width="72"></a>
</p>
<h1 align="center">marketing/</h1>
<p align="center">
  <a href="https://skillcdn.ai/gh/skillcdn/skills/marketing"><img alt="SkillCDN: skillcdn.ai/gh/skillcdn/skills/marketing" src="https://skillcdn.ai/badge/gh/skillcdn/skills/marketing"></a>
  <a href="../LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-3a6dd4"></a>
</p>

Skills for marketing and growth work: ads, ad research, promotional video, content, campaigns, posting to social accounts. The area manifest next to this file ([SKILLCDN.md](SKILLCDN.md)) says who these skills are for and adds the rules every marketing skill follows on top of the repository's. The area mounts alone at `skillcdn.ai/gh/skillcdn/skills/marketing` and installs as the `marketing` plugin of the repository's Claude Code marketplace.

| Skill | Tool family | What it does |
|---|---|---|
| [`skills/higgsfield-shorts-ad/`](skills/higgsfield-shorts-ad/) | Higgsfield | A vertical short-form AI ad from just a reference video and a product link. Learn what makes the reference work (its hook, the rule its story runs on, its measured pacing), write an original story on the product's own world in its medium (live action or animation), derive the rest, approve generated cast portraits and a first frame per shot, confirm a recommended model with its credit estimate, animate one directed draft take at a time, edit and caption in the brand's type in code. With no reference, it first finds one among running ads, with the creative research skill. |
| [`skills/meta-ad-library-creative-research/`](skills/meta-ad-library-creative-research/) | Meta Ad Library | Research on the ad creatives running for a keyword, a product or a competitor, read from the public library with a browser. Find the ads that show proof of working (their place in the impressions order, days running, reuse of the creative, the advertiser's volume), recent ones first, read videos frame by frame, and deliver a report: the landscape, a linked shortlist, a breakdown of each hook, angle, structure and offer, the patterns across them, and directions for the user's own ads. |

The skills chain. "Make an ad for this product", with no reference, has `higgsfield-shorts-ad` find one first with `meta-ad-library-creative-research` and choose among its shortlist; the research skill itself stays general.

Documents for this area go in `docs/` next to this file, where SkillCDN discovers them by default; there are none yet. The creative research reads what the two Meta Ad Library skills share from the repository's [`docs/meta-ad-library/`](../docs/meta-ad-library/README.md), the other being the rising products skill in [`product/`](../product/); card news is made by skills of the [`design/`](../design/) and [`product/`](../product/) areas, and a skill that posts the finished slides to an Instagram account is planned here.

How to write a skill: [guide/skill-authoring.md](../guide/skill-authoring.md). How to add one here: [guide/adding.md](../guide/adding.md). The `node scripts/check.mjs` check fails when a skill directory is missing from this table.
