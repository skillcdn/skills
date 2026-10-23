# Roadmap

What this repository plans to add, stage by stage of a consumer product's life, from finding what to build to running it. Each row is one job an agent will do with a real tool: the job as the user would say it, the area that owns it, the tool family it is likely to drive, and its status. A row enters as a job with candidate tools; the skill's name is fixed when it is built, because a skill here is written from the job done once with the tool ([skill-authoring.md](skill-authoring.md)). The order is the product's order; what is built next is the stage the real work is in.

Jobs and tools only. No product, no market and no plan of any business is named here: the repository is public, and a fork replaces this page with its own plan or deletes it.

| Status | Meaning |
|---|---|
| done | Shipped, and exercised at least once from a fresh session that followed the files alone. What that run did not cover is in the row, or in the skill's notes. |
| next | Being built, or the next to build. |
| candidate | The job is known. The tool is chosen when the job is first done with it. |

A row changes in the commit that ships, changes or retires its skill (the documentation protocol in [CLAUDE.md](../CLAUDE.md)).

## M0: Making skills

Skills about the skills: how work already done becomes a skill, and how a skill is verified and kept true.

| Job | Area | Tool family | Status |
|---|---|---|---|
| "Make what we just did into a skill." A skill in this repository from the session's own work, earlier transcripts, memory and results: designed, written in this layout, checked, run once by a fresh agent, shipped. [`skillcdn-skill-authoring`](../engineering/skills/skillcdn-skill-authoring/). A fresh run reached the push checkpoint; the push, the fresh run and the fold-in as a fresh agent does them, and the skill as it reads the shared pages, are untried. | engineering | SkillCDN | done |
| "Verify this skill." A fresh agent dry-reads the files, a fresh agent runs the served skill with its checkpoints answered as the user would, and the findings are folded back; also for the rounds after a tool, a model or a shared page changes. [`skillcdn-skill-verification`](../engineering/skills/skillcdn-skill-verification/). Used once by the authoring session on the four skills below (2026-10); its own fresh run is untried. | engineering | SkillCDN | next |

## M1: Discovery

What to build: where demand is moving, what people complain about, what is worth a try.

| Job | Area | Tool family | Status |
|---|---|---|---|
| "What is taking off in this market?" [`meta-ad-library-rising-products`](../marketing/skills/meta-ad-library-rising-products/). A fresh run on the US market reached the delivery (2026-10); a second run against a snapshot, the EU and UK series and the broad sweep are untried. | marketing | Meta Ad Library | done |
| "What do people want and complain about in this kind of app?" Charts, rankings and reviews of the app stores, read with a browser: the unmet needs and the words people use for them. | product | The App Store and Google Play as websites | candidate |
| "Is anyone asking for this?" Demand in communities, Reddit, Hacker News and Product Hunt: the threads, the recurring asks, the workarounds people built. | product | The sites, with a browser or their APIs | candidate |
| "Write up the opportunity." A brief from the research in the team's document tool, with the evidence kept apart from the inference. | product | The document tool in use, Confluence, Notion or Claude Docs | candidate |

## M2: Definition and validation

Deciding what it is, and finding out cheaply whether anyone wants it.

| Job | Area | Tool family | Status |
|---|---|---|---|
| "Put up a landing page with a waitlist." | marketing | Higgsfield website builder | candidate |
| "Run a small test campaign on this creative." Covered by the campaign phase of [`meta-ads-setup`](../engineering/skills/meta-ads-setup/): one ad set per creative at a small daily budget, the spend confirmed before activation. | engineering | Meta Marketing API | next |
| "Turn the brief into a PRD and a backlog." Requirements with their assumptions and open questions, and the stories that follow from them. | product | Jira and Confluence, or Linear and Notion | candidate |
| "Translate and localize the product into this language." The strings, the store listing and the site, with a glossary and the product's voice kept per product and reused on the next pass. | product | The codebase's localization files; Crowdin or Lokalise where used | candidate |

## M3: Brand and design

The `design` area was created with its first skill.

| Job | Area | Tool family | Status |
|---|---|---|---|
| "Make slides from this content, in the style of this deck." A document moved into an existing deck as new slides in the deck's own measured design system, audited by numbers and zoomed renders. [`figma-slides-from-content`](../design/skills/figma-slides-from-content/). A fresh run on a ten-page company profile into a deck of twelve styled slides reached the delivery (2026-10): thirteen slides, two pages split, two local fonts substituted, both checkpoints as written. Untried: a slide the user edits mid-run, a document in a script with spaces, a deck with a single content slide. Figma's MCP server writes to Slides with `use_figma`; writing needs a paid Full seat (checked 2026-10). | design | Figma | done |
| "Make the brand kit." Name options, logo, palette and type, explored as images and fixed in a design file. | design | Higgsfield and Figma | candidate |
| "Make the app icon and the store screenshots." | design | Figma | candidate |

## M4: Engineering, documents and continuous development

Keeping a codebase one that an agent can keep working in: its documents true to the code, its agreement with agents written down, each session able to pick up where the last one ended.

| Job | Area | Tool family | Status |
|---|---|---|---|
| "Write the working agreement for this codebase." `CLAUDE.md` or `AGENTS.md` and `README.md`, written or refreshed from the code as it is: how to build, check and run it, what a change must update, the gotchas, so that a fresh agent works in it without being told. | engineering | git and the codebase | candidate |
| "Keep the docs true after this change." The pages a change touches, found and updated under a documentation protocol like this repository's, in the same commit. | engineering | git | candidate |
| "Hand over to the next session." What was decided and why, what is open, what the next session must know, recorded where the next agent looks first. | engineering | git | candidate |
| "Keep the project building as its tools move." Dependency and toolchain updates with the checks that prove them, one at a time, nothing merged on a green badge alone. | engineering | The git host and the package manager | candidate |
| "Build me an app for this and put it online." A new TypeScript web app from a few plain questions, with its working agreement for a team and its launch through the deploy skill. [`cloudflare-new-app`](../engineering/skills/cloudflare-new-app/). Two fresh runs (2026-10): a stand-in app to the launch handover, and a Korean app from a mockup link through the launch to a live address; a browser-driven look check, a run with a design skill and a run with the provider's real keys are untried. | engineering | Cloudflare | done |
| "Make these documents searchable for our agents." Documents in any format turned into a pack of documents in the SkillCDN Format, in the user's repository: one file per document or chapter, maps, figures described, the language declared, checked and committed. [`skillcdn-document-pack`](../engineering/skills/skillcdn-document-pack/). A fresh run turned six small sources (wiki pages as HTML, text and Markdown policies, a CSV of questions, one Korean policy) into a checked pack with a Korean folder, both checkpoints as written, the commit on the user's word (2026-10); untried: PDF, Word and slides, figures and scanned pages, adding to a pack that exists, and the check from version 0.4.0 of the command, which names the sections. | engineering | SkillCDN | done |
| "What does the handbook say about this?" A question answered, a reference compiled or a claim checked from a large pack through SkillCDN, quoted by path and heading, and kept as a research note in the pack. [`skillcdn-document-research`](../engineering/skills/skillcdn-document-research/). Two fresh runs, in English and in Korean, on a handbook of twenty documents read through the command on a directory: the maps, three searches each, the sections read by their offsets, the answer with what the handbook does not say, and the note committed on the user's word (2026-10); untried: a pack served by a deployment, a reference compiled across many documents, a claim checked, and a question whose note already exists. | engineering | SkillCDN | done |

## M5: Launch

| Job | Area | Tool family | Status |
|---|---|---|---|
| "Put this project live on Cloudflare." Access, resources, secrets, the first deploy, the domain, deploys on every push, logs and analytics, with a record in the project. [`cloudflare-deploy`](../engineering/skills/cloudflare-deploy/). A fresh run put the app of the new-app skill's second run live (2026-10): token, D1, secrets, first deploy, a hostname under an existing zone, the repository connection with a push-triggered build, analytics by host, `DEPLOY.md`, then two requests after the launch (sample data loaded into the live database, a secret changed); untried: a domain to buy, a zone to create, R2 and KV, the OpenNext path, a run on a project the new-app skill did not make. | engineering | Cloudflare | done |
| "Take payments on the site." Stripe from a sandbox to live money: the order ledger, the hosted Checkout, the webhook that settles once, products and prices registered by the agent, the live switch confirmed, the owner's dashboard items listed. [`stripe-payments`](../engineering/skills/stripe-payments/). A fresh run took a stand-in app through the sandbox end to end (2026-10): the ledger, the hosted Checkout, the webhook, a driven browser paying with the test cards, partial and full refunds, a free code, a dispute, a resent event, the deployed site with the buy surface off; untried: the live switch with restricted keys, subscriptions, Managed Payments, a second currency. | engineering | Stripe | done |
| "Deploy the site elsewhere." Vercel, or the Higgsfield website builder's deploy. | engineering | Vercel or the Higgsfield website builder | candidate |
| "Submit the app and write the listing." Metadata, screenshots, review notes, the listing's words and keywords. | engineering, marketing | App Store Connect and Google Play Console | candidate |
| "Launch on Product Hunt." The page, the assets, the schedule, the first comment. | marketing | Product Hunt | candidate |

## M6: Promotion

| Job | Area | Tool family | Status |
|---|---|---|---|
| "Make an ad for this product." [`higgsfield-shorts-ad`](../marketing/skills/higgsfield-shorts-ad/). A fresh run with no reference reached the plan and cost checkpoint (2026-10); the production phases of this version are untried. | marketing | Higgsfield | done |
| "Research the ads running for this keyword." [`meta-ad-library-creative-research`](../marketing/skills/meta-ad-library-creative-research/). A fresh run on the US market reached the delivery (2026-10); the KR market, the driven-browser route and a shell without ffmpeg are untried. | marketing | Meta Ad Library | done |
| "Post this short to TikTok." With a trending sound where one fits, through the connected account. | marketing | Higgsfield's TikTok tools | candidate |
| "Connect Meta ads and run them." The site's measurement, the datasets and the domain, the ad accounts and spend, campaigns from finished creatives in the shape a working account runs them, created paused and activated after the budget is confirmed, and the rules by which they are watched. [`meta-ads-setup`](../engineering/skills/meta-ads-setup/). A fresh run wired a stand-in app without a token (2026-10): the pixel on public pages, the server events, attribution on the row and the order, the privacy switch, deployed switched off, and an independent code review folded back; untried: a run with a token (datasets, the domain, a campaign created paused and activated, the spend sync, the review). A marketing-only skill that runs a campaign on an account already wired stays a candidate. | engineering | Meta Marketing API | done |
| "Make product-shot and UGC ads from these product images." | marketing | Higgsfield ads studio | candidate |
| "Look at this account's posts and make ours the same way." A reference account's card-news format measured into a spec from the posts visible without signing in. [`instagram-cardnews-format-study`](../marketing/skills/instagram-cardnews-format-study/). Written from one run on one account (2026-10); a fresh run is untried. | marketing | Instagram | next |
| "Find some hot issues in these categories and I will pick one; then research it with sources and images." A ranked candidate list and, from the pick, a topic brief with every fact traced to an article sentence and the articles' photos credited. [`web-cardnews-topic-brief`](../marketing/skills/web-cardnews-topic-brief/). Written from two runs on a domestic audience (2026-10); a fresh run is untried. | marketing | Web | next |
| "Make the card news and show it here." The carousel from a brief in a reference format, as HTML rendered to PNG, each slide laid out for what it says. [`html-cardnews-from-brief`](../marketing/skills/html-cardnews-from-brief/). Written from two runs (2026-10), the second of which was sent back for repeating the first's layouts; a fresh run is untried. | marketing | HTML | next |
| "Write the launch posts and the launch email." A series for the channels the product uses. | marketing | Open | candidate |

## M7: Operations, support and data

The `support`, `operations` and `data` areas are created with their first skills.

| Job | Area | Tool family | Status |
|---|---|---|---|
| "Give me an admin to watch sales and ads." A separate Worker only the operator can open, behind Cloudflare Access, with the funnel, the orders, the campaigns and their controls, the costs, the system's health, an audit log and a daily digest. [`cloudflare-admin-dashboard`](../engineering/skills/cloudflare-admin-dashboard/). A fresh run built and deployed the admin locked on a stand-in app (2026-10): the guard, the audit log, confirmations, the funnel with a cookie-free visit counter, the payments panel with a capped refund proven in the sandbox, the syncs and the digest, then Access enabled by the person on the Worker's Access tab, the secrets set and the operator's sign-in seen in the audit log; untried: restricted live keys, the ads panel with a token, chat alerts. | engineering | Cloudflare | done |
| "Give me this week's numbers." A readout from the product's analytics and the stores against last week, with what moved and why it might have. | data | GA4 or PostHog, App Store Connect, Google Play Console | candidate |
| "Answer the store reviews." Replies in the product's voice, grouped by what they report, with the bugs filed. | support | App Store Connect and Google Play Console | candidate |
| "Write the support macros." From the tickets that repeat. | support | Intercom or Zendesk | candidate |
| "Make the weekly report deck." The M3 slides skill on the week's readout. | operations | Figma | candidate |

## M8: Content

| Job | Area | Tool family | Status |
|---|---|---|---|
| "Make episode one of a short drama from this premise." [`higgsfield-shorts-drama`](../media/skills/higgsfield-shorts-drama/). A fresh run reached the cost checkpoint with the fallback named (2026-10); a production of this version, a second episode and a 150-second episode are untried. | media | Higgsfield | done |
| "Make an explainer video for this." | media | Higgsfield explainer presets | candidate |
