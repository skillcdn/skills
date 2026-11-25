<div align="center">
  <a href="https://skillcdn.ai"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/skillcdn/skillcdn/main/packages/brand/logo-white.svg"><img alt="SkillCDN" src="https://raw.githubusercontent.com/skillcdn/skillcdn/main/packages/brand/logo-black.svg" width="360"></picture></a>
  <p><strong>Skills for an AI agent to do real company work.</strong></p>
  <p>
  <a href="https://skillcdn.ai/gh/skillcdn/skills"><img alt="SkillCDN: skillcdn.ai/gh/skillcdn/skills" src="https://skillcdn.ai/badge/gh/skillcdn/skills"></a>
  <a href="https://github.com/skillcdn/skills/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/skillcdn/skills/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-3a6dd4"></a>
  </p>
  <p>
  <a href="https://skillcdn.ai">skillcdn.ai</a> · <a href="#what-you-can-ask-for">What you can ask for</a> · <a href="#for-an-agent-account">Agent accounts</a> · <a href="#skills">Skills</a> · <a href="#make-it-yours">Make it yours</a> · <a href="guide/skill-authoring.md">Authoring guide</a>
  </p>
</div>

Give an AI agent the job, not the instructions. This pack holds the skills of a marketer, a designer, a developer and a market researcher: each one takes a request in your own words, drives the real tool from the first question to the finished result, stops where a person must decide, and checks its work before you see it.

It works in the AI you already use, and it is what an **agent account** on a [SkillCDN Console](https://github.com/skillcdn/console) starts work with: a member of your team with a name, a role and a manager, who takes a task from the board and finds the skill for it here.

**Try it now.** Add `https://skillcdn.ai/gh/skillcdn/skills` as a remote MCP server in ChatGPT, Claude, Cursor, VS Code, Claude Code, Codex CLI, Gemini CLI or any other MCP client ([the page of the address](https://skillcdn.ai/gh/skillcdn/skills) has the steps for each), and say:

> Make a card news post about this week's biggest AI story.

The agent finds the story with its sources, asks which account's look to work in, builds the slides, reviews them at phone size and shows you the post. Nothing is spent and nothing is posted until you say so.

---

## What you can ask for

Say it in your own words. Each line is a job the pack does end to end.

| You say | You get |
|---|---|
| **Marketing** | |
| "Make an ad for this product." | A captioned vertical video ad built on a reference that is working now, approved shot by shot, with the credits estimated before anything is generated. |
| "Research the ads running for this keyword." | The creatives that show proof of working in the Meta Ad Library, broken down into hook, angle, structure and offer, with directions for your own. |
| "Make this week's batch of card news, and book the ones I approve." | Topics with sources, a post each made side by side and reviewed by an agent that made none of them, then each approved post booked on your Instagram and filed once it is live. |
| **Design** | |
| "Make a product deck that sells this to our customers." | A deck as one HTML file and a PDF, every slide one message, measured for overlaps and cut text before you see it. |
| "Draft the slides for this meeting from these notes." | A report or a proposal deck in your organization's tokens, at 16:9, with a PDF. |
| "Show me four looks for this." | Four rendered directions on one contact sheet, each judged for the AI feel first, with a recommendation. |
| "Put this PDF into this deck, as it is." | New slides inside your Figma deck, built in the deck's own type scale, colors and spacing. |
| **Product and market research** | |
| "Find a market we could enter." | Every theme judged per country on four questions, with the sources behind each verdict and a watch list that is measured again by the same yardstick. |
| "Look into this idea properly." | One review: the market and when it buys, who already sells it and what they earn, where the material can come from, the legal risks with a design around each, and a pilot plan. |
| "Turn the research into this month's market report." | One issue of a market report in your brand, every number traced to its source. |
| "What is taking off in this market?" | The products and services advertised more and more, counted in the public ad library. |
| **Engineering** | |
| "Build me an app for this and put it online." | A web app live on your own domain, then payments, ads and an admin to watch them, each a skill that takes over from the last. |
| "Make these documents searchable for our agents." | A handbook or a body of specifications as a pack an agent searches and answers from, with checked citations. |
| "Set up a repository for this project." | A repository laid out the way every agent expects, with its agreement, its check and its board; or a studio that keeps producing, with its know-how kept where the next session reads it. |
| "Make what we just did into a skill." | A skill written from the work already done, then run again by a fresh agent before it ships. |
| **Media, operations, writing** | |
| "Make episode one of a short drama from this premise." | A vertical episode, every line spoken by the video model and checked by two plain decodes. |
| "Write up today's client meeting from my notes." | The minutes as a PDF to send the same day: what was decided, what is open, who does what by when. |
| "Write an anchor report on this." | A news script from a sourced story, written to be heard once. |

Every job, with the other ways it is asked for and the skill that does it, is one page: [docs/pack/jobs.md](docs/pack/jobs.md).

## For an agent account

On a [SkillCDN Console](https://github.com/skillcdn/console) an agent is a member of its own: it is assigned a task as a colleague is, takes it, reports as it goes, hands in what it made, and asks a person when a person must decide. What it knows how to do comes from a pack. This is the pack a team starts with.

- **A role is a set of skills.** An account whose job is marketing works with the ad, the ad research and the card news chain; one whose job is development with the app, the deploy, payments and the admin; one that watches markets with the survey, its rounds and the market report.
- **The skill's stops are the board's decisions.** Where a skill would stop for you in a chat (a plan, a cost, what is posted), an agent account raises a decision to the person who can make it and goes on with other work until it is answered. Nothing is spent, posted or deployed in passing.
- **Work that continues has a place.** [`git-studio-setup`](engineering/skills/git-studio-setup/SKILL.md) lays out a repository where people and agent accounts keep producing the same kind of thing (posts, ad creatives, optimization rounds, market rounds) with the policy, each unit's state and what the runs taught kept where the next session reads them. [`git-desk-setup`](engineering/skills/git-desk-setup/SKILL.md) makes a member's own desk a private repository.
- **The pack is read through the board.** A console's project names this pack, or your fork of it; an agent there finds a skill with `console skills --search` and loads it with `console skill`, with no connection of its own to set up.

```sh
# an administrator makes the account
console agent new mira --name "Mira" --title "Marketing" --manager me
# assign it a task as you would a colleague
console task new "This week's card news batch, five posts" --worker "@mira" --state ready
```

The console's own README has [an agent account from invitation to first task](https://github.com/skillcdn/console#an-agent-account-from-invitation-to-first-task).

## Why these skills hold up

- **Written from work done once, with the real tool.** A skill here is a job that was carried through by hand first, then run again by a fresh agent that had only the files. What that run had to be told went back into the skill.
- **Checked before you see it.** Every skill ends in a review with verdicts: slides measured for overlap and cut text, spoken lines decoded twice, numbers read again in their source, a reviewer that made nothing.
- **A person decides what a person should.** A skill asks only what it cannot derive, shows each step briefly, estimates before it spends, and confirms one by one what leaves: a post, a deploy, a message.
- **Nothing pinned.** A skill tells the agent how to find today's models, prices and parameters in the tool's own catalog, so it does not break when they change.
- **They chain.** A skill that needs what another makes names it and runs it first: the brief becomes the post, the post joins the batch, the batch is booked. One person, or one team of agent accounts, runs the skills of every area together.
- **Plain files, yours to fork.** Every skill is an [Agent Skills](https://agentskills.io/specification) folder of Markdown under MIT. No code runs on a server or on your machine unless the agent you trust runs it.

## Skills

By area of work. A row is the skill's own first sentence; its `SKILL.md` says the rest.

### Marketing

Ads, ad research, promotional video, posting to social accounts. [`marketing/`](marketing/)

<!-- skillcdn:catalog folder=marketing -->
| Skill | What it does |
|---|---|
| [higgsfield-shorts-ad](marketing/skills/higgsfield-shorts-ad/SKILL.md) | Makes a short-form vertical AI ad, promo or commercial on Higgsfield from a product link and a reference video, found among the ads running now when the user has none. |
| [instagram-post-scheduling](marketing/skills/instagram-post-scheduling/SKILL.md) | Schedules approved Instagram posts (card news carousels of images and video slides with their captions) on the account's web interface, in a browser signed in to it, reads each booking back on the sc… |
| [meta-ad-library-creative-research](marketing/skills/meta-ad-library-creative-research/SKILL.md) | Researches ad creatives in the Meta Ad Library for a keyword, a product or a competitor by reading the public library with a browser, because its API leaves out most commercial ads. |

3 skills.
<!-- /skillcdn:catalog -->

### Design

Slides and decks, card news posts and the formats they are built in, looks on a contact sheet. [`design/`](design/)

<!-- skillcdn:catalog folder=design -->
| Skill | What it does |
|---|---|
| [figma-slides-from-content](design/skills/figma-slides-from-content/SKILL.md) | Moves a document (a proposal, a report, any PDF) into an existing Figma Slides deck as new slides, one per page, built in the deck's own design system rather than a generic one. |
| [html-card-news-batch](design/skills/html-card-news-batch/SKILL.md) | Makes several card news posts at once from picked topics and one format. |
| [html-card-news-from-brief](design/skills/html-card-news-from-brief/SKILL.md) | Builds an Instagram card news carousel from a sourced topic brief in a format spec's format, as HTML rendered to PNG, with an mp4 for a slide whose picture is a clip of the brief's; with no spec or b… |
| [html-deck-from-outline](design/skills/html-deck-from-outline/SKILL.md) | Drafts a slide deck as one HTML file and a PDF from notes, a meeting plan or an idea, as a corporate report (a business plan, a plan for investors, a company presentation, an internal report) or an e… |
| [html-design-variations](design/skills/html-design-variations/SKILL.md) | Shows four looks for one design (a page's first screen, a deck's cover, a card news format) as HTML rendered in a browser and tiled on one contact sheet, from a reference, a concept or the thing as i… |
| [html-market-report-deck](design/skills/html-market-report-deck/SKILL.md) | Makes one issue of a market report a brand hands out, as a slide deck in one HTML file and a PDF, from market research already done: every slide one message carried by a chart or a picture composed f… |
| [html-product-deck](design/skills/html-product-deck/SKILL.md) | Makes a product deck that sells a product or one of its features to buyers, as one HTML file and a PDF, every slide one message in a scene composed for it (a real screen, a scene drawn in the product… |
| [instagram-card-news-format-study](design/skills/instagram-card-news-format-study/SKILL.md) | Studies the card news of a reference Instagram account, of one reference post, or of a few accounts of a genre, and writes the format as a spec a new post can be built in, from the posts visible with… |

8 skills.
<!-- /skillcdn:catalog -->

### Product

What is worth building before anything is built: markets, signals, a sourced brief, concept directions. [`product/`](product/)

<!-- skillcdn:catalog folder=product -->
| Skill | What it does |
|---|---|
| [dart-company-figures](product/skills/dart-company-figures/SKILL.md) | Finds a Korean company's revenue and operating profit in its filings on DART, the Financial Supervisory Service's disclosure site, and checks what the company announced against them. |
| [meta-ad-library-rising-products](product/skills/meta-ad-library-rising-products/SKILL.md) | Finds what is taking off in a market or a field of work, such as AI tools, by what its advertisers are putting new money behind, read from the public Meta Ad Library with a browser. |
| [web-business-idea-deep-dive](product/skills/web-business-idea-deep-dive/SKILL.md) | Reviews one business idea in depth before anything is built, as one document with what exactly is sold to whom and who pays, how big the market is and when in the year it buys, who already sells it (… |
| [web-card-news-topic-brief](product/skills/web-card-news-topic-brief/SKILL.md) | Finds what is worth a card news post now in the categories an account covers, in the outlets and where people are talking, lets the user pick, and turns the pick into a sourced topic brief a post can… |
| [web-concept-variations](product/skills/web-concept-variations/SKILL.md) | Shows four to six concept directions that get a reference's effect by other means, for a product, a post, a page, a deck or a campaign, from a reference the user gives or one found among what is work… |
| [web-market-entry-signals](product/skills/web-market-entry-signals/SKILL.md) | Finds which markets are worth entering now, from official statistics, filings, app stores and the ads running, in Korea and the US by default, and measures the watched markets again later. |

6 skills.
<!-- /skillcdn:catalog -->

### Engineering

Apps put live with payments, ads and an admin; repositories and studios set up; documents made searchable; skills made from work done. [`engineering/`](engineering/)

<!-- skillcdn:catalog folder=engineering -->
| Skill | What it does |
|---|---|
| [cloudflare-admin-dashboard](engineering/skills/cloudflare-admin-dashboard/SKILL.md) | Builds the operator's admin dashboard as a separate Cloudflare Worker that only the operator can open, bound to the project's own database, protected by Cloudflare Access with a one-time email code a… |
| [cloudflare-deploy](engineering/skills/cloudflare-deploy/SKILL.md) | Puts a web project live on Cloudflare Workers and makes it deploy itself from then on. |
| [cloudflare-new-app](engineering/skills/cloudflare-new-app/SKILL.md) | Builds a new web app from an idea and puts it live on Cloudflare. |
| [git-desk-setup](engineering/skills/git-desk-setup/SKILL.md) | Sets up a member's own desk as a private git repository: the folder that console desk writes for a person of a SkillCDN Console, or that an agent account is set up with, committed and pushed to their… |
| [git-repo-setup](engineering/skills/git-repo-setup/SKILL.md) | Sets up a new git repository so a team and its agents keep developing in it: the working agreement (AGENTS.md, CLAUDE.md), a README in the team's language, the documents under docs/, one check with t… |
| [git-studio-setup](engineering/skills/git-studio-setup/SKILL.md) | Sets up a studio, the shared git repository in which a team and its agents keep producing one kind of thing (card news for an account, ad creatives, the episodes of a series) or keep running one kind… |
| [meta-ads-setup](engineering/skills/meta-ads-setup/SKILL.md) | Connects a web project to Meta ads and runs them end to end, with the agent doing every step a token allows. |
| [skillcdn-document-answer](engineering/skills/skillcdn-document-answer/SKILL.md) | Answers a question from a pack of documents served through SkillCDN (a handbook, a manual, a policy set, an archive), with every citation verified against the section it quotes, and says plainly what… |
| [skillcdn-document-pack](engineering/skills/skillcdn-document-pack/SKILL.md) | Turns documents a person has (PDF, Word, slides, spreadsheets, HTML, wiki and chat exports, plain text) into a pack of documents in the SkillCDN Format, in a repository they own, so that agents brows… |
| [skillcdn-document-research](engineering/skills/skillcdn-document-research/SKILL.md) | Answers a question from a large pack of documents (a handbook, a manual, an archive) through SkillCDN, compiles a reference or checks a claim, and keeps what it learned for the next time. |
| [skillcdn-skill-authoring](engineering/skills/skillcdn-skill-authoring/SKILL.md) | Turns work a person and an agent have already done together into a skill in the SkillCDN Format, in a checkout of this repository or a fork of it. |
| [skillcdn-skill-verification](engineering/skills/skillcdn-skill-verification/SKILL.md) | Verifies a skill in a repository of the SkillCDN Format the way a user's agent will meet it. |
| [stripe-payments](engineering/skills/stripe-payments/SKILL.md) | Takes payments on a web project with Stripe, from a sandbox to live money, with the agent doing every setup step a key allows. |

13 skills.
<!-- /skillcdn:catalog -->

### Media

Original video and audio content. [`media/`](media/)

<!-- skillcdn:catalog folder=media -->
| Skill | What it does |
|---|---|
| [higgsfield-shorts-drama](media/skills/higgsfield-shorts-drama/SKILL.md) | Makes one episode of an original vertical short drama (9:16, about 150 seconds by default) on Higgsfield from a premise or an existing series bible. |

1 skill.
<!-- /skillcdn:catalog -->

### Operations

The records a company and its clients' work keep day to day. [`operations/`](operations/)

<!-- skillcdn:catalog folder=operations -->
| Skill | What it does |
|---|---|
| [html-meeting-minutes-from-notes](operations/skills/html-meeting-minutes-from-notes/SKILL.md) | Writes the minutes of a client meeting as one HTML file and an A4 PDF from the notes a person brings back (what was decided, what is still to be confirmed, who does what by when, the next meeting), f… |

1 skill.
<!-- /skillcdn:catalog -->

### Writing

Text that is the result itself, read or heard as it is. [`writing/`](writing/)

<!-- skillcdn:catalog folder=writing -->
| Skill | What it does |
|---|---|
| [web-news-anchor-report-script](writing/skills/web-news-anchor-report-script/SKILL.md) | Writes the script of a news anchor report from a sourced story, with the screen planned cut by cut for a video made later, about ninety seconds unless asked otherwise. |

1 skill.
<!-- /skillcdn:catalog -->

Areas to come, each with its first skill: sales, support, data, finance, legal, people. What is planned is in [guide/roadmap.md](guide/roadmap.md).

## Document sets

What the skills of one tool family share is written once, as documents an agent searches and reads without a skill. A skill includes the page every run needs and links the rest.

| Set | What it holds |
|---|---|
| [`docs/pack/`](docs/pack/) | How an agent finds the skill for a job, and the jobs index. The page a client is told to read first. |
| [`docs/browser/`](docs/browser/) | A browser the agent drives or runs headless: an agent account's own sign-in, reading a page in full, the ways around a wall, rendering HTML to PNG and PDF, clips. |
| [`docs/writing/`](docs/writing/) | What every text shares: the reader, sentences, facts and figures, what stays inside, the house style. |
| [`docs/variation/`](docs/variation/) | Making variations: the effect brief, the axes, the signals of the AI feel, the comparison sheet. |
| [`docs/card-news/`](docs/card-news/) | The format spec, the topic brief, and the record an account that keeps posting holds. |
| [`docs/instagram/`](docs/instagram/) | Reading Instagram signed out, and booking posts in a session signed in to the account. |
| [`docs/meta-ad-library/`](docs/meta-ad-library/) | What the public ad library is evidence of, its routes and parameters, counting by age, manners. |
| [`docs/market-research/`](docs/market-research/) | The grades of a number, the watch list a market is measured on again, the public sources by country. |
| [`docs/higgsfield/`](docs/higgsfield/) | The sandbox, models and credits, first frames, decoding a take, the sounds of each language. |
| [`engineering/docs/cloudflare/`](engineering/docs/cloudflare/) | Accounts and tokens, the platform's parts, deploys, domains, mail, as the app skills use them. |
| [`engineering/docs/stripe/`](engineering/docs/stripe/) | Sandboxes and keys, the Checkout flow and its webhooks, the balance ledger. |
| [`engineering/docs/meta-marketing-api/`](engineering/docs/meta-marketing-api/) | Tokens, datasets and the Conversions API, campaigns, insights. |
| [`engineering/docs/git/`](engineering/docs/git/) | A repository's layout, agreement and README, its console project, a studio and how its know-how is kept. |
| [`engineering/docs/skillcdn/`](engineering/docs/skillcdn/) | From a push to what an agent gets, searching a pack of documents, fresh agents, transcripts. |

## Using the pack

```
skillcdn.ai/gh/skillcdn/skills                                        the whole pack (recommended)
skillcdn.ai/gh/skillcdn/skills/marketing                              one area
skillcdn.ai/gh/skillcdn/skills/marketing/skills/higgsfield-shorts-ad  one skill
skillcdn.ai/gh/skillcdn/skills@<commit>                               pinned to a commit
```

1. **Connect it.** Add an address as a remote MCP server in your agent. An agent with only a shell reads the same pack with the `skillcdn` command, and an agent on a console with `console skills`.
2. **Ask.** In your own words. The agent is told on connect to read [docs/pack/finding-a-skill.md](docs/pack/finding-a-skill.md) first, and finds the skill from there.
3. **Connect what the skill names.** Each skill lists the tools it drives under "Requirements", checks for them before its first message, and says exactly what to add when one is missing.

The same folders work without SkillCDN. Copy `<area>/skills/<name>/` into any agent that reads `SKILL.md`, or install an area as a [Claude Code](https://code.claude.com/docs/en/plugins) plugin: `claude plugin marketplace add skillcdn/skills`, then `claude plugin install marketing@skillcdn`. Through SkillCDN the rules in [SKILLCDN.md](SKILLCDN.md), the area's rules and the shared pages a skill includes arrive with every skill; a copy relies on the skill's own hard rules and reads the pages it links from this repository.

## Tool families

| Family | What it is | What you connect |
|---|---|---|
| Higgsfield | AI image, video and audio generation with a cloud sandbox for editing. | The Higgsfield MCP server. |
| Meta Ad Library | Meta's public library of running ads, read as a website because its API leaves out most commercial ads. | Nothing: a browser the agent drives, or a shell with a Chromium-family browser. |
| Instagram | A reference account's public posts read signed out; your own account's posts booked in its web interface. | Nothing to read. Booking needs a browser signed in to your account, by you or by an agent account that holds its sign-in. |
| Web | The open web read for a story or a market: search, pages read in full, public statistics, app stores. | Nothing: a web search tool and a page reader or a driven browser. |
| DART | The Korean Financial Supervisory Service's disclosure system, read for a company's audited figures. | Nothing for the public website; a free OpenDART key if you have one. |
| Browser (HTML) | A Chromium-family browser that renders a page the agent wrote to PNG or PDF. | Nothing: an installed Chrome, Edge or Chromium. |
| Figma | Figma Design and Figma Slides, written through the Figma MCP server. | The Figma MCP server, signed in to an account that can edit the file. |
| Cloudflare | Workers with D1, R2, KV, custom domains, builds, the Registrar and mail. | A Cloudflare account and an API token you create with the steps the skills give. |
| Stripe | Checkout, products and prices, webhooks, refunds, subscriptions, the balance ledger. | A Stripe account and a restricted key, sandbox first. |
| Meta Marketing API | Datasets and the Conversions API, campaigns, ad sets, creatives, insights. | A business portfolio with an ad account and a Page, and a system user token. |
| Git | git, a git host, and the console's board where a repository's work is tracked. | git and the host's command signed in; the `console` command where there is a console. |
| SkillCDN | A pack in the SkillCDN Format, this one or a fork, with its check. | A checkout with git and Node.js, and the pack's connection for a fresh agent. |

Each skill says what is missing and stops; none substitutes a tool that changes the result or the cost.

## From one skill to a whole team

The pack is one of three repositories built toward one thing: a team of AI agents working beside its people, each agent with the skills of its job, all of them on one board.

| | What it is | Start at |
|---|---|---|
| [**SkillCDN**](https://github.com/skillcdn/skillcdn)<br>`skillcdn/skillcdn` | The standard and the server: the format a pack is written in, the address that serves it to any agent, the command that reads it. | `skillcdn.ai/gh/<owner>/<repo>` |
| **SkillCDN Pack**<br>this repository | Skills for real company work, by area. What a team starts with, and forks into a pack of its own. | [`skillcdn.ai/gh/skillcdn/skills`](https://skillcdn.ai/gh/skillcdn/skills) |
| [**SkillCDN Console**](https://github.com/skillcdn/console)<br>`skillcdn/console` | Where that team works: the board, the agent accounts, the runs and the decisions. | [`skillcdn.ai/gh/skillcdn/console`](https://skillcdn.ai/gh/skillcdn/console) |

Put together: an organization keeps its skills in git, SkillCDN hands them to every agent, this pack is what the team starts with, and the console is where people and agent accounts take their work, report and get their decisions.

## Make it yours

This repository takes no pull requests. It is the reference pack for the [SkillCDN Format](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/skill-repo.md) and is meant to be forked: the layout, the checks, the CI and the rules for agents come with the fork, and your skills go in.

1. Fork the repository, or copy it into a new one.
2. In `SKILLCDN.md`, set `name`, `description`, `translations` and `metadata.author` to yours. Keep the rules that hold for you; change the rest.
3. Keep a license SkillCDN can pass on. It serves a skill in full only under a license it recognizes as permissive; under another, in a public repository, the skill is only described, with a link to its source.
4. Keep the areas you need and delete the others. A new area is a folder with a `SKILLCDN.md` and a `README.md`; the steps are in [guide/adding.md](guide/adding.md).
5. Write your skills at `<area>/skills/<name>/`, following [guide/skill-authoring.md](guide/skill-authoring.md), or have an agent write them from work already done with the authoring skill in [`engineering/`](engineering/). Put what the skills of one tool share in `docs/<tool>/`. Run `node scripts/check.mjs`, and `npx @skillcdn/cli@latest catalog --write README.md` to fill the tables above; CI runs both. Replace [guide/roadmap.md](guide/roadmap.md) with your own plan, or delete it.
6. Rewrite this README and each area's README for your repository, their tops first. The lockup and the symbol are SkillCDN's marks, so put your own there or none ([trademark policy](https://github.com/skillcdn/skillcdn/blob/main/TRADEMARKS.md)); keep the badge and give it your address, in its link and in its picture's URL (`https://skillcdn.ai/badge/gh/<you>/<repo>`). The `image` of `SKILLCDN.md` is the picture the explorer shows: put your own at `assets/banner.webp` (under 200 KiB) or an `https` URL in the field, or leave the field out. In `.claude-plugin/marketplace.json`, set `name` and `owner` to yours and list the areas that have skills. Where a skill's Requirements name this repository as the place a copy reads its pages, put yours.
7. Connect it at `skillcdn.ai/gh/<you>/<repo>`. A public repository needs no setup. On a console, name it as your project's pack.

The rules for changing anything, for people and agents alike, are in [AGENTS.md](AGENTS.md); a fork keeps them or changes them. A skill here that no longer works can be reported in an issue.

## Repository layout

```
SKILLCDN.md       the pack's manifest: its name, description, the page read first, the rules for every skill
README.md         this introduction
<area>/           one folder per area of work: marketing/, design/, product/, engineering/, ...
  SKILLCDN.md     the area manifest: who its skills are for, the rules its skills add
  README.md       the area's catalog
  skills/<name>/  one directory per skill: SKILL.md, references/, assets/, optional scripts/
  docs/           the area's document sets
docs/             document sets that serve every area
guide/            how skills here are written, added and found, and what is planned
scripts/          check.mjs, the validation CI runs
.claude-plugin/   the Claude Code marketplace: one plugin per area with skills
```

```sh
node scripts/check.mjs                 # manifests, front-matter, catalogs, links and text; Node.js 24, no install
npx @skillcdn/cli@latest check         # the indexer's own reading: what an agent is told, what each skill weighs
```

Name `@latest`: without it `npx` runs whichever copy its cache holds, and an older indexer reads the pack by older rules. CI runs both on every push and the indexer's once a week, so that a release of SkillCDN that reads the pack differently shows before an agent meets it.

## License

The content of this repository is under the [MIT License](LICENSE.md), a license SkillCDN recognizes as permissive, which is why it serves these skills in full. "SkillCDN" and its logos are trademarks of KDX Labs Corp.; its [trademark policy](https://github.com/skillcdn/skillcdn/blob/main/TRADEMARKS.md) allows everyone the file name `SKILLCDN.md`, the `skillcdn` front-matter key and the name of the format, so a fork keeps them. The tools the skills drive are third-party products with their own terms.
