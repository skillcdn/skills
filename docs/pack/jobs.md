# Jobs this pack does

What you can ask for, in your own words, and which skill does it. One section per job: the sentence a user says, what comes back, the skill's path (load it with `load_skill` as it is), other ways the job is asked for, and the skill that looks alike but does something else. An agent searches this page first, with `search_repo` scoped to `docs/pack`, then the whole pack; [finding-a-skill.md](finding-a-skill.md) says how. Every skill in the pack has a section here.

## Marketing

### "Make an ad for this product."

- You get: a captioned vertical ad built on a reference that is working now, its story the product's own, its lines spoken by the video model, approved shot by shot with a credit estimate before anything is generated.
- Skill: [`marketing/skills/higgsfield-shorts-ad/`](/marketing/skills/higgsfield-shorts-ad/SKILL.md)
- Also asked as: "make a short video ad from this reference", "a promo or a commercial for TikTok, Reels or Shorts", "an ad like this one but for my product".
- Not this one when: you want to see which ads others are running (the creative research below), or a story with no product in it (the short drama under Media).

### "Research the ads running for this keyword."

- You get: the creatives that show proof of working in the Meta Ad Library, each broken down into hook, angle, structure and offer, the patterns across them, and directions for your own ads.
- Skill: [`marketing/skills/meta-ad-library-creative-research/`](/marketing/skills/meta-ad-library-creative-research/SKILL.md)
- Also asked as: "competitor ad research", "ad references or a swipe file for this product", "what hooks are working in Facebook and Instagram ads for this".
- Not this one when: you want to know which products or services are being advertised more and more (rising products under Product), or to make the ad itself (the ad above).

## Media

### "Make episode one of a short drama from this premise."

- You get: an episode of an original vertical short drama with every line spoken by the video model and verified, subtitles and name cards in code, and a series bible and a log the next episode starts from.
- Skill: [`media/skills/higgsfield-shorts-drama/`](/media/skills/higgsfield-shorts-drama/SKILL.md)
- Also asked as: "a vertical drama episode from this series bible", "a scripted short with characters and dialogue", "the next episode".
- Not this one when: the video sells a product (the ad under Marketing).

## Design

### "Put this PDF into this deck, as it is."

- You get: new slides in an existing Figma Slides deck, one per page of the document, in the deck's own measured design system, every alignment and element checked by numbers and zoomed renders before you see them.
- Skill: [`design/skills/figma-slides-from-content/`](/design/skills/figma-slides-from-content/SKILL.md)
- Also asked as: "add these pages to the Figma deck in its style", "slides from this document in the deck's design", "move this proposal into our slides file".
- Not this one when: there is no deck yet and the slides are drafted from notes (the deck below).

### "Draft the slides for this meeting from these notes."

- You get: a first-draft deck as one HTML file and a PDF: every slide a type and its blocks from your notes, in your own colors and font, the wording checked against your house style, every page looked at before you see it; a designer polishes the structure instead of starting blank.
- Skill: [`design/skills/html-deck-from-outline/`](/design/skills/html-deck-from-outline/SKILL.md)
- Also asked as: "a presentation from this outline", "slides for the kickoff from the meeting plan", "a proposal deck as PDF", "a status report deck".
- Not this one when: the slides go into an existing Figma deck in its design (the Figma skill above).

### "Show me four looks for this."

- You get: four looks for one design (a page's first screen, a deck's cover with a body slide, a post's cover, a card news format's cover and body slide) as HTML rendered in a browser and tiled on one contact sheet, each judged for the AI feel at desktop and phone size (a post at feed width) before you see it, with a recommendation and a runner-up, and your pick's tokens handed to the skill that builds the thing.
- Skill: [`design/skills/html-design-variations/`](/design/skills/html-design-variations/SKILL.md)
- Also asked as: "design directions for this landing page", "variations of this cover", "how else could this deck look", "alternatives to this layout".
- Not this one when: you want the idea behind the piece varied rather than its look (the concept directions under Product), or a still a generative tool must make.

### "Look at this account's posts and make ours the same way."

- You get: a card news format measured into a spec, from a reference account, one reference post or a few accounts of a genre, read without signing in: the canvas, every slide type's anatomy, the text density as counts, the register as patterns, the caption's parts, what the account never does.
- Skill: [`design/skills/instagram-card-news-format-study/`](/design/skills/instagram-card-news-format-study/SKILL.md)
- Also asked as: "analyze this account's card news format", "make ours like this post", "what are this account's categories and format", "what do card news in this genre look like", "a reference for a card-news series", "study these carousel posts".
- Not this one when: you want the post itself built (the build below), the story researched (the brief under Product), or the reference varied into a look of your own (the next section, which the build offers first); a request for the whole post starts with the build, which runs this study first.

### "Make our card news like this account's, but ours."

- You get: four looks for a card news format (each a cover and a body slide), from a reference measured as it is, near the reference or far from it as you ask, on one contact sheet with a recommendation, and your pick written as a format spec the card news build follows slide by slide; with no reference, from accounts of your kind found for you to pick one, and only where none can be read, from the genre's card news.
- Skill: [`design/skills/html-design-variations/`](/design/skills/html-design-variations/SKILL.md)
- Also asked as: "like this account's card news but a little different", "something new from this account's format", "design our card news look from references", "a card news format for our new magazine".
- Not this one when: you want a reference's format exactly as it is (the study above); the build below offers this route first when it has no spec.

### "Make the card news and show it here."

- You get: the carousel of a card news post as PNG slides built in the format spec's slide types (a reference's, or a format of your own) from a sourced brief, previewed, reviewed slide by slide at phone size, delivered with the caption, the credits and a pre-publish checklist.
- Skill: [`design/skills/html-card-news-from-brief/`](/design/skills/html-card-news-from-brief/SKILL.md)
- Also asked as: "build the finished post from this brief", "make this one the same way as the last", "the slides of this post as images", "a card news carousel from these facts".
- Not this one when: there is no brief yet (the brief under Product) or no format spec (the study and the variations above); the skill asks for the reference, offers the routes to a spec in their order, the reference varied first, and says what to run first. A request for the whole post ("make a card news post about this, the way that account does it") runs them in order: the study (once per account), the brief, the variations unless the reference is wanted as it is, then this build.

## Product

### "What is taking off in this market?"

- You get: a ranked report of what advertisers are putting new money behind in a sector, item by item and theme by theme, with the ads, the sellers, the offers and the risks, and a snapshot the next run measures growth against.
- Skill: [`product/skills/meta-ad-library-rising-products/`](/product/skills/meta-ad-library-rising-products/SKILL.md)
- Also asked as: "winning or trending products", "what is hot in this field right now", "new product ideas from what people are buying", "which AI tools are being pushed".
- Not this one when: you want the creatives of one keyword or competitor studied (the creative research under Marketing).

### "Show me five different ways to get this reference's effect."

- You get: four to six concept directions that keep a reference's mechanism and change what the viewer would recognize, each a position on the concept axes with its opening lines, judged for the AI feel before you see it, on one sheet with a recommendation and a runner-up, and your pick written for the skill that makes the thing.
- Skill: [`product/skills/web-concept-variations/`](/product/skills/web-concept-variations/SKILL.md)
- Also asked as: "concept directions for this product", "alternatives to this idea that still work the same way", "variations on this reference", "directions before we make the post or the deck".
- Not this one when: you want the looks of one direction (the looks under Design), or the thing itself made (the producing skill, which the handoff names).

### "Find some hot issues in these categories and I will pick one."

- You get: a ranked list of this week's candidate stories to pick from, then, for the pick, a topic brief: every fact traced to the sentence of an article read in full, the angle as a published interpretation, numbers cross-checked, what no article confirmed, and the images that show the story with captions, credits, sizes, legibility and licence terms.
- Skill: [`product/skills/web-card-news-topic-brief/`](/product/skills/web-card-news-topic-brief/SKILL.md)
- Also asked as: "research this topic for a post with sources and images", "fact-check this story before it is designed", "a sourced brief for a card news post", "what happened this week in these categories".
- Not this one when: you have the facts and want the slides (the build under Design), or you want the format (the study and the variations under Design).

## Engineering

### "Make what we just did into a skill."

- You get: a skill in this repository, or a fork of it, that a fresh agent runs from the files alone: designed from the session's own work, checked, tried once, listed in the catalogs.
- Skill: [`engineering/skills/skillcdn-skill-authoring/`](/engineering/skills/skillcdn-skill-authoring/SKILL.md)
- Also asked as: "write a skill from this work", "turn this workflow into a skill", "fold what this run taught back into the skill".
- Not this one when: the skill exists and the question is whether it still works (the verification below).

### "Verify this skill."

- You get: what a fresh agent had to guess in the skill's files, a run of the served skill with its checkpoints answered as you would, and the findings folded back into it.
- Skill: [`engineering/skills/skillcdn-skill-verification/`](/engineering/skills/skillcdn-skill-verification/SKILL.md)
- Also asked as: "dry-read this skill", "test the skill from a fresh session", "does the fix hold", "check the skill after the tool changed", "bring the skills up to date after the new release".
- Not this one when: the skill is not written yet (the authoring above).

### "Make these documents searchable for our agents."

- You get: your PDFs, Word files, slides and exports as a pack of documents in your own repository: one file per document or chapter with a title and a description, each original kept beside its chapters, a map per set, figures kept with their words and scans transcribed, checked and committed; an agent then finds a section by its words, reads it in one call and reaches the original behind it.
- Skill: [`engineering/skills/skillcdn-document-pack/`](/engineering/skills/skillcdn-document-pack/SKILL.md)
- Also asked as: "turn these files into a pack", "a handbook our agents can search", "add these documents to the pack", "make the manual readable by agents".
- Not this one when: the pack exists and you have a question for it (the question and the research below).

### "What does the handbook say about this?"

- You get: the answer now, in two or three sentences, then the quotes that support it, each with the path, the heading and the offset of its section, every quote read once more before it is sent so that a reader who opens the citation finds the words, and what the pack does not say stated plainly with the nearest passage. Nothing is written into the pack and nothing is spent.
- Skill: [`engineering/skills/skillcdn-document-answer/`](/engineering/skills/skillcdn-document-answer/SKILL.md)
- Also asked as: "answer this from our documents", "is this true according to the manual", "which document covers this", "what do our documents say about this".
- Not this one when: the answer is to be kept in the pack as a note, or a reference compiled across many documents (the research below); the documents are not in a pack yet (the document pack above).

### "Research this in our documents and keep the note."

- You get: a question answered, a reference compiled or a claim checked from a large pack, quoted from the sections that say it with the path and the heading of each, what the pack does not say stated plainly, and a research note kept in the pack for the next time.
- Skill: [`engineering/skills/skillcdn-document-research/`](/engineering/skills/skillcdn-document-research/SKILL.md)
- Also asked as: "compile a reference from the archive", "check this claim against the manual and keep the result", "research this across our documents", "write up what the handbook says about this".
- Not this one when: you want the answer now and nothing kept (the question above); the documents are not in a pack yet (the document pack above).

### "Build me an app for this and put it online."

- You get: a TypeScript web app in a repository with its working agreement: mobile-first, every language in from the first commit, ready for search and AI engines, with a share image and favicon set, sign-in, a database, analytics, tests and one check; then live on Cloudflare.
- Skill: [`engineering/skills/cloudflare-new-app/`](/engineering/skills/cloudflare-new-app/SKILL.md)
- Also asked as: "make a website for this idea", "a new web app with sign-in and a database", "build and launch this service".
- Not this one when: the project exists and only needs to go live (the deploy below).

### "Put this project live on Cloudflare."

- You get: the project at its address on Workers with its database, storage, secrets and domain in place, deploying itself on every push, with a record in the project of what exists and how to run it.
- Skill: [`engineering/skills/cloudflare-deploy/`](/engineering/skills/cloudflare-deploy/SKILL.md)
- Also asked as: "deploy this to Cloudflare Workers", "attach the domain and make every push deploy", "set up the database and the secrets for production".
- Not this one when: there is no project yet (the new app above).

### "Take payments on the site."

- You get: a buy flow on Stripe's hosted Checkout with the order ledger, the webhook and refunds handled, the products and prices registered by the agent, proven in a sandbox and then switched to live money, with the few dashboard items only the owner can set listed for them.
- Skill: [`engineering/skills/stripe-payments/`](/engineering/skills/stripe-payments/SKILL.md)
- Also asked as: "add checkout to the site", "sell this with Stripe", "charge for this feature", "add a subscription".
- Not this one when: you want the screens that show the money and refund orders (the admin dashboard below).

### "Connect Meta ads and run them."

- You get: the site measuring leads, checkouts and purchases without sending anything private, the datasets and the domain set up, and campaigns built from finished creatives the way a working account runs them, turned on only after the budget is confirmed, with the rules by which they are watched and changed.
- Skill: [`engineering/skills/meta-ads-setup/`](/engineering/skills/meta-ads-setup/SKILL.md)
- Also asked as: "set up the Meta pixel and the Conversions API", "run Facebook and Instagram ads for the site", "launch campaigns from these creatives".
- Not this one when: you want to research other advertisers' ads (the Meta Ad Library skills under Marketing and Product) or make the creative (the ad under Marketing).

### "Give me an admin to watch sales and ads."

- You get: a separate Worker only the operator can open, behind Cloudflare Access, with the funnel, the orders, the campaigns with their controls, the costs and the system's health, an audit log of every action and a daily digest in a chat.
- Skill: [`engineering/skills/cloudflare-admin-dashboard/`](/engineering/skills/cloudflare-admin-dashboard/SKILL.md)
- Also asked as: "an operator dashboard for orders and campaigns", "an admin panel behind a login", "a back office for the site".
- Not this one when: payments or ads are not wired yet (the payments and the Meta ads above).

## Operations

### "Write up today's client meeting from my notes and make the minutes to send."

- You get: the minutes as one HTML file and an A4 PDF from your notes: decisions, questions and answers, items to confirm, actions with owners and planned dates, and the next meeting, each in one plain sentence, in grayscale with the client's logo first, checked against your house style and looked at page by page before you see them, with what stayed internal and what to confirm before you send them. Sending is your own step.
- Skill: [`operations/skills/html-meeting-minutes-from-notes/`](/operations/skills/html-meeting-minutes-from-notes/SKILL.md)
- Also asked as: "meeting minutes for the client", "a 회의록 to send today", "write up the kickoff meeting", "turn these meeting notes into minutes as a PDF", "a meeting record for the partner".
- Not this one when: you want slides from the meeting (the deck under Design), or a note for your own team that need not leave the organization.

## Jobs with no skill yet

What the pack plans next is kept in its guide on the git host, which the mount does not serve. For a job no section above covers, the agent says so and names the nearest one above.
