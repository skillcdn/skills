# Finding a skill in this pack

This pack holds skills for an AI agent to do real company work, one area at a time, each driving a real tool from the request to the finished result. An agent that has connected and holds a request needs to answer one question before anything else: is there a skill for this job, and which one? This page says how the pack is laid out, the three ways to find a skill, how a result is read, and what to do when nothing fits. The pack's words are English; the examples at the end are what the search returned on the day named.

## How the pack is laid out

- **An area is who does the work.** `marketing/`, `media/`, `design/`, `engineering/` and `product/` are the folders, one per kind of work, each with a manifest that says who its skills are for, a `README.md` that lists them, its skills under `skills/` and the documents its people read under `docs/`. The connection instructions list the areas with a line each.
- **A skill's name is its tool family and its job.** `<area>/skills/<tool>-<job>/`: `higgsfield-shorts-ad` is the Higgsfield tools making a shorts ad, `html-card-news-from-brief` is HTML rendering a card news post from a brief, `skillcdn-document-research` is SkillCDN itself researching a pack of documents, `meta-ad-library-creative-research` is the Meta Ad Library website read for ad creatives. Read a name as "with this tool, this job"; the words are hyphenated one by one so that a search matches each of them.
- **A document set is not a skill.** `docs/<family>/` at the root and `<area>/docs/<family>/` hold what the skills of one tool family share (how a browser behaves, what the Higgsfield tools do, the shape of a card news brief); `docs/pack/`, this set, is about the pack itself. A search returns them as `document:` results beside the `skill:` results.
- **What each area holds today.** Marketing: a shorts ad from a reference, research in the Meta Ad Library (ad creatives, rising products), and card news (a reference account's format measured, a sourced topic brief, the carousel built). Media: an episode of a short drama. Design: slides added to a Figma deck in its own design, and a first-draft deck as HTML and PDF. Engineering: a skill written from work already done and a skill verified, documents turned into a searchable pack and a pack researched, a web app built and put live on Cloudflare, payments with Stripe, Meta ads connected and run, the operator's admin dashboard. Product: concept directions and alternatives, planning; its first skills are next.

## Three ways to find a skill

1. **The jobs index, first.** [`jobs.md`](jobs.md) has one section per job, headed by the sentence a user says, with the skill's path. Search it with the job's words scoped to this set (`search_repo` with `path` set to `docs/pack`), or read it whole with `read_repo_file`; a section that matches names the skill, and the skill's path goes to `load_skill` as it is.
2. **Browse by area.** When the request says what kind of work it is, `browse_repo` on `<area>/skills` lists every skill of the area with its description, and the description's first lines say what the skill makes and when to use it. Two areas take two calls.
3. **Search the whole pack.** `search_repo` with two or three English nouns of the job, the way a user would name it ("card news post", "slides from notes", "payments on the site"), not a sentence of instructions. The pack's words are English: a request in Korean, Japanese or any other language is translated to the English words first (카드뉴스 is "card news", 발표자료 is "slides" or "deck", 광고 is "ad", 결제 is "payments", 핸드북 is "handbook"); the translations a skill carries are for people and are not searched. How the ranking works, so that the words are chosen well: a word that few entries hold decides the order and a word every entry repeats decides next to nothing, so the distinctive noun of the job matters most; a match in a skill's name counts twice a match in its body, and a hyphenated name is matched by its parts as well as whole; where the deployment searches by meaning as well, a question asked in other words still finds the passage, and the result's last line says so (`Ranked by words and meaning.`). When that line says `by words alone this time`, ask once more with other words for the same job before concluding.

## Reading a result

- A `skill:` result names the skill's path and its description: load the path with `load_skill` and follow it to the end before applying it. A `document:` result is a page with the sections that matched; it may name the skill (the jobs index does), and it is never run as one.
- A description says what comes out from what, then when to use the skill in the user's own phrases ("Use when a user says ..."), and, where a neighbouring skill does a job that looks alike, which one to use instead. Read that last sentence before choosing between two.
- A skill result that says `described only` is served without its content under its license; its source link says where to read it.

## When no skill fits

Say so plainly: there is no skill in this pack for this job. Name the nearest skill and what it would not do, so that the user can decide whether a part of the job is still worth it; do not stretch a skill past what its description says, because its checkpoints and verdicts are written for its own job. Where the work has been done once by hand, in this session or another, `skillcdn-skill-authoring` (engineering) turns it into a skill in a fork of this pack or in this one. What the pack plans to add next is kept in its guide on the git host, which the mount does not serve.

## Examples

What `search_repo` returned for ten requests, five said in English and five translated from Korean to English words first, scoped to `docs/pack` and then unscoped, and what `browse_repo` showed for two areas, on the day named. Checked again when the search changes or a skill is renamed.

- Checked 2026-10: the examples are written after the index of the commit that adds this page has been built; see the next version of this page.
