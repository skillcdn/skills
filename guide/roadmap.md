# Roadmap

What this repository plans to add, stage by stage of a consumer product's life, from finding what to build to running it. Each row is one job an agent will do with a real tool: the job as the user would say it, the area that owns it, the tool family it is likely to drive, and its status. A row enters as a job with candidate tools; the skill's name is fixed when it is built, because a skill here is written from the job done once with the tool ([skill-authoring.md](skill-authoring.md)). The order is the product's order; what is built next is the stage the real work is in.

Jobs and tools only. No product, no market and no plan of any business is named here: the repository is public, and a fork replaces this page with its own plan or deletes it.

| Status | Meaning |
|---|---|
| done | Shipped, and exercised at least once from a fresh session that followed the files alone. What that run did not cover is in the skill's notes. |
| next | Being built, or the next to build. |
| candidate | The job is known. The tool is chosen when the job is first done with it. |

A row changes in the commit that ships, changes or retires its skill (the documentation protocol in [CLAUDE.md](../CLAUDE.md)).

## M0: Making skills

Skills about the skills: how work already done becomes a skill, and how a skill is verified and kept true.

| Job | Area | Tool family | Status |
|---|---|---|---|
| "Make what we just did into a skill." A skill in this repository from the session's own work, earlier transcripts, memory and results: designed, written in this layout, checked, run once by a fresh agent, shipped. [`skillcdn-skill-authoring`](../engineering/skills/skillcdn-skill-authoring/) | engineering | SkillCDN | next |
| "Verify this skill." A fresh session follows the files alone, its run is read against the skill, and the findings are folded back. Today a phase of the authoring skill; later a skill of its own, for the rounds after a tool or a shared page changes. | engineering | SkillCDN | candidate |

## M1: Discovery

What to build: where demand is moving, what people complain about, what is worth a try.

| Job | Area | Tool family | Status |
|---|---|---|---|
| "What is taking off in this market?" [`meta-ad-library-rising-products`](../marketing/skills/meta-ad-library-rising-products/) | marketing | Meta Ad Library | done |
| "What do people want and complain about in this kind of app?" Charts, rankings and reviews of the app stores, read with a browser: the unmet needs and the words people use for them. | product | The App Store and Google Play as websites | candidate |
| "Is anyone asking for this?" Demand in communities, Reddit, Hacker News and Product Hunt: the threads, the recurring asks, the workarounds people built. | product | The sites, with a browser or their APIs | candidate |
| "Write up the opportunity." A brief from the research in the team's document tool, with the evidence kept apart from the inference. | product | The document tool in use, Confluence, Notion or Claude Docs | candidate |

## M2: Definition and validation

Deciding what it is, and finding out cheaply whether anyone wants it.

| Job | Area | Tool family | Status |
|---|---|---|---|
| "Put up a landing page with a waitlist." | marketing | Higgsfield website builder | candidate |
| "Run a small test campaign on this creative." The M6 campaign skill at a small budget, the spend gated. | marketing | Meta Marketing API | candidate |
| "Turn the brief into a PRD and a backlog." Requirements with their assumptions and open questions, and the stories that follow from them. | product | Jira and Confluence, or Linear and Notion | candidate |
| "Translate and localize the product into this language." The strings, the store listing and the site, with a glossary and the product's voice kept per product and reused on the next pass. | product | The codebase's localization files; Crowdin or Lokalise where used | candidate |

## M3: Brand and design

The `design` area is created with its first skill.

| Job | Area | Tool family | Status |
|---|---|---|---|
| "Make slides from this content, in the style of this deck." The content exists; the skill applies the design of a reference or template deck, its layouts, type, color and the shapes of its slides. Figma's MCP server writes to Slides with `use_figma` and makes a deck from its own templates with `generate_deck`; writing needs a paid Full seat (checked 2026-10). | design | Figma | next |
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

## M5: Launch

| Job | Area | Tool family | Status |
|---|---|---|---|
| "Deploy the site." | engineering | Vercel or Cloudflare, or the Higgsfield website builder's deploy | candidate |
| "Submit the app and write the listing." Metadata, screenshots, review notes, the listing's words and keywords. | engineering, marketing | App Store Connect and Google Play Console | candidate |
| "Launch on Product Hunt." The page, the assets, the schedule, the first comment. | marketing | Product Hunt | candidate |

## M6: Promotion

| Job | Area | Tool family | Status |
|---|---|---|---|
| "Make an ad for this product." [`higgsfield-shorts-ad`](../marketing/skills/higgsfield-shorts-ad/) | marketing | Higgsfield | done |
| "Research the ads running for this keyword." [`meta-ad-library-creative-research`](../marketing/skills/meta-ad-library-creative-research/) | marketing | Meta Ad Library | done |
| "Post this short to TikTok." With a trending sound where one fits, through the connected account. | marketing | Higgsfield's TikTok tools | candidate |
| "Run a campaign on this creative." Campaign, ad set and ad from a finished creative, the budget estimated and gated, the results read back. | marketing | Meta Marketing API | candidate |
| "Make product-shot and UGC ads from these product images." | marketing | Higgsfield ads studio | candidate |
| "Write the launch posts and the launch email." A series for the channels the product uses. | marketing | Open | candidate |

## M7: Operations, support and data

The `support`, `operations` and `data` areas are created with their first skills.

| Job | Area | Tool family | Status |
|---|---|---|---|
| "Give me this week's numbers." A readout from the product's analytics and the stores against last week, with what moved and why it might have. | data | GA4 or PostHog, App Store Connect, Google Play Console | candidate |
| "Answer the store reviews." Replies in the product's voice, grouped by what they report, with the bugs filed. | support | App Store Connect and Google Play Console | candidate |
| "Write the support macros." From the tickets that repeat. | support | Intercom or Zendesk | candidate |
| "Make the weekly report deck." The M3 slides skill on the week's readout. | operations | Figma | candidate |

## M8: Content

| Job | Area | Tool family | Status |
|---|---|---|---|
| "Make episode one of a short drama from this premise." [`higgsfield-shorts-drama`](../media/skills/higgsfield-shorts-drama/); a second episode and a 150-second episode are not yet exercised. | media | Higgsfield | done |
| "Make an explainer video for this." | media | Higgsfield explainer presets | candidate |
