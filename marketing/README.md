<p align="center">
  <a href="https://skillcdn.ai"><img alt="SkillCDN" src="https://raw.githubusercontent.com/skillcdn/skillcdn/main/packages/brand/symbol.svg" width="72"></a>
</p>
<h1 align="center">marketing/</h1>
<p align="center">
  <a href="https://skillcdn.ai/gh/skillcdn/skills/marketing"><img alt="SkillCDN: skillcdn.ai/gh/skillcdn/skills/marketing" src="https://skillcdn.ai/badge/gh/skillcdn/skills/marketing"></a>
  <a href="../LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-3a6dd4"></a>
</p>

Skills for marketing and growth work: ads, ad research, promotional video, content, campaigns, posting to social accounts. The area manifest next to this file ([SKILLCDN.md](SKILLCDN.md)) says who these skills are for and adds the rules every marketing skill follows on top of the repository's. The area mounts alone at `skillcdn.ai/gh/skillcdn/skills/marketing` and installs as the `marketing` plugin of the repository's Claude Code marketplace.

<!-- skillcdn:catalog -->
| Skill | What it does |
|---|---|
| [higgsfield-shorts-ad](skills/higgsfield-shorts-ad/SKILL.md) | Makes a short-form vertical AI ad, promo or commercial on Higgsfield from a product link and a reference video, found among the ads running now when the user has none. |
| [instagram-post-scheduling](skills/instagram-post-scheduling/SKILL.md) | Schedules approved Instagram posts (card news carousels of images and video slides with their captions) on the account's web interface, in the browser the person is signed in to, reads each booking b… |
| [meta-ad-library-creative-research](skills/meta-ad-library-creative-research/SKILL.md) | Researches ad creatives in the Meta Ad Library for a keyword, a product or a competitor by reading the public library with a browser, because its API leaves out most commercial ads. |

3 skills.
<!-- /skillcdn:catalog -->

The skills chain. "Make an ad for this product", with no reference, has `higgsfield-shorts-ad` find one first with `meta-ad-library-creative-research` and choose among its shortlist; the research skill itself stays general.

Documents for this area go in `docs/` next to this file, where SkillCDN discovers them by default; there are none yet. The creative research reads what the two Meta Ad Library skills share from the repository's [`docs/meta-ad-library/`](../docs/meta-ad-library/README.md), the other being the rising products skill in [`product/`](../product/); card news is made by skills of the [`design/`](../design/) and [`product/`](../product/) areas, and `instagram-post-scheduling` here books the approved posts on the account, reading the repository's [`docs/instagram/`](../docs/instagram/README.md) and the account record in [`docs/card-news/`](../docs/card-news/README.md).

How to write a skill: [guide/skill-authoring.md](../guide/skill-authoring.md). How to add one here: [guide/adding.md](../guide/adding.md). The table is written by `npx @skillcdn/cli@latest catalog --write`, from each skill's first sentence; `node scripts/check.mjs` fails when a skill is missing from it.
