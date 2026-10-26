<p align="center">
  <a href="https://skillcdn.ai"><img alt="SkillCDN" src="https://raw.githubusercontent.com/skillcdn/skillcdn/main/apps/web/public/brand/symbol.svg" width="72"></a>
</p>
<h1 align="center">product/</h1>
<p align="center">
  <a href="https://skillcdn.ai/gh/skillcdn/skills/product"><img alt="SkillCDN: skillcdn.ai/gh/skillcdn/skills/product" src="https://skillcdn.ai/badge/gh/skillcdn/skills/product"></a>
  <a href="../LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-3a6dd4"></a>
</p>

Skills for product planning and management: discovery, research synthesis, concept directions and alternatives, requirements, specifications, roadmaps, prioritization. The area manifest next to this file ([SKILLCDN.md](SKILLCDN.md)) says who these skills are for and adds the rules every product skill follows on top of the repository's. The area mounts alone at `skillcdn.ai/gh/skillcdn/skills/product` and installs as the `product` plugin of the repository's Claude Code marketplace.

| Skill | Tool family | What it does |
|---|---|---|
| [`skills/web-concept-variations/`](skills/web-concept-variations/) | Web | Four to six concept directions that get a reference's effect by other means, for a product, a post, a page, a deck or a campaign, from a reference the user gives or one found among what is working now. Read the reference for its intent, effect, aesthetics, fun, expected effect and the prior knowledge it rests on, find other references that get the same effect on the open web, place candidates on the concept axes with one near and one far, judge each for the AI feel before it is shown, compare them on one sheet with a recommendation and a runner-up, and hand the user's pick to the skill that produces. Nothing is spent. |

Documents for this area go in `docs/` next to this file, where SkillCDN discovers them by default; there are none yet. The concept skill reads what every variation skill shares from the repository's [`docs/variation/`](../docs/variation/README.md).

How to write a skill: [guide/skill-authoring.md](../guide/skill-authoring.md). How to add one here: [guide/adding.md](../guide/adding.md). The `node scripts/check.mjs` check fails when a skill directory is missing from this table.
