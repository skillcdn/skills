<p align="center">
  <a href="https://skillcdn.ai"><img alt="SkillCDN" src="https://raw.githubusercontent.com/skillcdn/skillcdn/main/packages/brand/symbol.svg" width="72"></a>
</p>
<h1 align="center">engineering/</h1>
<p align="center">
  <a href="https://skillcdn.ai/gh/skillcdn/skills/engineering"><img alt="SkillCDN: skillcdn.ai/gh/skillcdn/skills/engineering" src="https://skillcdn.ai/badge/gh/skillcdn/skills/engineering"></a>
  <a href="../LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-3a6dd4"></a>
</p>

Skills for software development and for the tooling an agent works with: writing and changing code, keeping a codebase's documents true to it, building apps and taking them to live money (payments, ads, the operator's dashboard), testing, debugging, making skills from work done, turning a body of documents into a pack an agent searches and reads through SkillCDN, and answering from such a pack with every citation checked. The area manifest next to this file ([SKILLCDN.md](SKILLCDN.md)) says who these skills are for and adds the rules every engineering skill follows on top of the repository's. The area mounts alone at `skillcdn.ai/gh/skillcdn/skills/engineering` and installs as the `engineering` plugin of the repository's Claude Code marketplace.

<!-- skillcdn:catalog -->
| Skill | What it does |
|---|---|
| [cloudflare-admin-dashboard](skills/cloudflare-admin-dashboard/SKILL.md) | Builds the operator's admin dashboard as a separate Cloudflare Worker that only the operator can open, bound to the project's own database, protected by Cloudflare Access with a one-time email code a… |
| [cloudflare-deploy](skills/cloudflare-deploy/SKILL.md) | Puts a web project live on Cloudflare Workers and makes it deploy itself from then on. |
| [cloudflare-new-app](skills/cloudflare-new-app/SKILL.md) | Builds a new web app from an idea and puts it live on Cloudflare. |
| [git-desk-setup](skills/git-desk-setup/SKILL.md) | Sets up a member's own desk as a private git repository: the folder that console desk writes for a person of a SkillCDN Console, or that an agent account is set up with, committed and pushed to their… |
| [git-repo-setup](skills/git-repo-setup/SKILL.md) | Sets up a new git repository so a team and its agents keep developing in it: the working agreement (AGENTS.md, CLAUDE.md), a README in the team's language, the documents under docs/, one check with t… |
| [git-studio-setup](skills/git-studio-setup/SKILL.md) | Sets up a studio, the shared git repository in which a team and its agents keep producing one kind of thing (card news for an account, ad creatives, the episodes of a series) or keep running one kind… |
| [meta-ads-setup](skills/meta-ads-setup/SKILL.md) | Connects a web project to Meta ads and runs them end to end, with the agent doing every step a token allows. |
| [skillcdn-document-answer](skills/skillcdn-document-answer/SKILL.md) | Answers a question from a pack of documents served through SkillCDN (a handbook, a manual, a policy set, an archive), with every citation verified against the section it quotes, and says plainly what… |
| [skillcdn-document-pack](skills/skillcdn-document-pack/SKILL.md) | Turns documents a person has (PDF, Word, slides, spreadsheets, HTML, wiki and chat exports, plain text) into a pack of documents in the SkillCDN Format, in a repository they own, so that agents brows… |
| [skillcdn-document-research](skills/skillcdn-document-research/SKILL.md) | Answers a question from a large pack of documents (a handbook, a manual, an archive) through SkillCDN, compiles a reference or checks a claim, and keeps what it learned for the next time. |
| [skillcdn-skill-authoring](skills/skillcdn-skill-authoring/SKILL.md) | Turns work a person and an agent have already done together into a skill in the SkillCDN Format, in a checkout of this repository or a fork of it. |
| [skillcdn-skill-verification](skills/skillcdn-skill-verification/SKILL.md) | Verifies a skill in a repository of the SkillCDN Format the way a user's agent will meet it. |
| [stripe-payments](skills/stripe-payments/SKILL.md) | Takes payments on a web project with Stripe, from a sandbox to live money, with the agent doing every setup step a key allows. |

13 skills.
<!-- /skillcdn:catalog -->

Documents for this area are in [`docs/`](docs/README.md) next to this file, where SkillCDN discovers them by default: [`docs/skillcdn/`](docs/skillcdn/README.md) holds what the SkillCDN skills share, [`docs/git/`](docs/git/README.md) the layout every repository of the pack shares, [`docs/cloudflare/`](docs/cloudflare/README.md) what the Cloudflare skills share, [`docs/stripe/`](docs/stripe/README.md) what the skills that take payments share, and [`docs/meta-marketing-api/`](docs/meta-marketing-api/README.md) what the skills that run Meta ads share.

How to write a skill: [guide/skill-authoring.md](../guide/skill-authoring.md). How to add one here: [guide/adding.md](../guide/adding.md), or the authoring skill above, which does those steps from the work already done; the verification skill tries a skill again from a fresh session after it changed. The table is written by `npx @skillcdn/cli@latest catalog --write`, from each skill's first sentence; `node scripts/check.mjs` fails when a skill is missing from it.
