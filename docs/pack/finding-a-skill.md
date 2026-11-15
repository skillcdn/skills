# Finding a skill in this pack

This pack holds skills for an AI agent to do real company work, one area at a time, each driving a real tool from the request to the finished result. An agent that has connected and holds a request needs to answer one question before anything else: is there a skill for this job, and which one? This page says how the pack is laid out, the three ways to find a skill, how a result is read, and what to do when nothing fits. The pack's words are English; the examples at the end are what the search returned on the day named.

## How the pack is laid out

- **An area is who does the work.** `marketing/`, `media/`, `design/`, `engineering/`, `product/` and `operations/` are the folders, one per kind of work, each with a manifest that says who its skills are for, a `README.md` that lists them, its skills under `skills/` and the documents its people read under `docs/`. The connection instructions list the areas with a line each, the jobs of the area first, and name the pack's manifest (`SKILLCDN.md`, the rules every skill runs under) and its README as what to read on demand; `browse_repo` on a folder names the folder's own manifest.
- **A skill's name is its tool family and its job.** `<area>/skills/<tool>-<job>/`: `higgsfield-shorts-ad` is the Higgsfield tools making a shorts ad, `html-card-news-from-brief` is HTML rendering a card news post from a brief, `skillcdn-document-research` is SkillCDN itself researching a pack of documents, `meta-ad-library-creative-research` is the Meta Ad Library website read for ad creatives. Read a name as "with this tool, this job"; the words are hyphenated one by one so that a search matches each of them.
- **A document set is not a skill.** `docs/<family>/` at the root and `<area>/docs/<family>/` hold what the skills of one tool family share (how a browser behaves, what the Higgsfield tools do, the shape of a card news brief); `docs/pack/`, this set, is about the pack itself. A search returns them as `document:` results beside the `skill:` results.
- **What each area holds today.** Marketing: a shorts ad from a reference and research in the Meta Ad Library for ad creatives. Media: an episode of a short drama. Design: slides added to a Figma deck in its own design, a first-draft deck as HTML and PDF, four looks for one design on a contact sheet, and card news (a reference's format measured into a spec, a format of the user's own varied from it, the carousel built from a sourced brief). Engineering: a skill written from work already done and a skill verified, documents turned into a searchable pack and a pack researched, a web app built and put live on Cloudflare, payments with Stripe, Meta ads connected and run, the operator's admin dashboard. Product: what is taking off in a market, read from where advertisers put new money in the Meta Ad Library, concept directions that get a reference's effect by other means, and a sourced topic brief of a story with its facts, its angle and its images; the planning skills are next. Operations: the minutes of a client meeting as one HTML file and an A4 PDF from the notes a person brings back, for sending the same day.

## Three ways to find a skill

1. **The jobs index, first.** [`jobs.md`](jobs.md) has one section per job, headed by the sentence a user says, with the skill's path. Search it with the job's words scoped to this set (`search_repo` with `path` set to `docs/pack`), or read it whole with `read_repo_file`; a section that matches names the skill, and the skill's path goes to `load_skill` as it is.
2. **Browse by area.** When the request says what kind of work it is, `browse_repo` on `<area>/skills` lists every skill of the area with its description, and the description's first lines say what the skill makes and when to use it. Two areas take two calls.
3. **Search the whole pack.** `search_repo` with two or three English nouns of the job, the way a user would name it ("card news post", "slides from notes", "payments on the site"), not a sentence of instructions. The pack's words are English: a request in Korean, Japanese or any other language is translated to the English words first (카드뉴스 is "card news", 발표자료 is "slides" or "deck", 광고 is "ad", 결제 is "payments", 핸드북 is "handbook"); the translations a skill carries are for people and are not searched. How the ranking works, so that the words are chosen well: a word that few entries hold decides the order and a word every entry repeats decides next to nothing, so the distinctive noun of the job matters most; a match in a skill's name counts twice a match in its body, a match in a heading of a document counts between the two, and a hyphenated name is matched by its parts as well as whole; a skill counts only a little above a document (its score 1.05 times a document's, SkillCDN 0.5.1), so a document that matches better can stand above it, and the jobs index, which names the skill, is often the second result: take the path it gives; where the deployment searches by meaning as well, a question asked in other words still finds the passage, and the result's last line says so (`Ranked by words and meaning.`). When that line says `by words alone this time`, ask once more with other words for the same job before concluding.

## Through a console

An agent that reads this pack through a SkillCDN Console's command, and not through a connection of its host, has the same four reads as commands, which `console skills` names when it lists the pack: `browse_repo` on a folder is `console skills <folder>`, `search_repo` is `console skills --search <words> [<folder>]`, `load_skill` is `console skill <path>`, and `read_repo_file` is `console skill --file <path>`. A path is the same either way, and everything on this page and in the skills holds as written.

## Reading a result

- A `skill:` result names the skill's path and its description: load the path with `load_skill` and follow it to the end before applying it. A `document:` result is a page with the sections that matched; it may name the skill (the jobs index does), and it is never run as one. A result marked as the overview of its folder is that folder's `README.md`, the map that says a little of everything in it: go on to the page it names rather than answering from the map.
- A description says what comes out from what, then when to use the skill in the user's own phrases ("Use when a user says ..."), and, where a neighbouring skill does a job that looks alike, which one to use instead. Read that last sentence before choosing between two.
- A skill result that says `described only` is served without its content under its license; its source link says where to read it.

## When no skill fits

Say so plainly: there is no skill in this pack for this job. Name the nearest skill and what it would not do, so that the user can decide whether a part of the job is still worth it; do not stretch a skill past what its description says, because its checkpoints and verdicts are written for its own job. Where the work has been done once by hand, in this session or another, `skillcdn-skill-authoring` (engineering) turns it into a skill in a fork of this pack or in this one. What the pack plans to add next is kept in its guide on the git host, which the mount does not serve.

## Examples

What `search_repo` returned for eleven requests, five said in English and five translated from Korean to English words first, and one for the newest skill, scoped to `docs/pack` and then unscoped, and what `browse_repo` showed for two areas, on the day named. Checked again when the search changes or a skill is renamed or added.

Checked 2026-11-15, on commit 4cf4176 under SkillCDN 0.5.1, with the deployment's meaning index complete and every result ranked by words and meaning. "Index" is the first section of the first result with `path` set to `docs/pack`, which was the jobs index every time; "whole pack" is the first result without a path.

| Request, as words | Index | Whole pack |
|---|---|---|
| "card news post" | the build (`html-card-news-from-brief`) | the study (`instagram-card-news-format-study`), the build second: a card news skill, not the one that makes the post |
| "slides from notes" | the deck (`html-deck-from-outline`) | the deck, the Figma skill second |
| "ad from a reference video" | the ad (`higgsfield-shorts-ad`) | the ad |
| "answer from the handbook" | the question (`skillcdn-document-answer`) | the question, the jobs index second, the research third |
| "four looks for this landing" | the looks (`html-design-variations`) | the looks |
| "analyze this account's card news format" (from 이 계정 카드뉴스 포맷 분석) | the study, found by its section's other phrasings | the study |
| "build an app and put it online" (from 앱 만들어서 올려줘) | the new app (`cloudflare-new-app`) | the new app, the deploy third |
| "take payments on the site" (from 결제 붙여줘) | the payments (`stripe-payments`) | the payments |
| "competitor ad research" (from 경쟁사 광고 조사) | the creative research (`meta-ad-library-creative-research`), found by its section's other phrasings | the creative research |
| "make documents searchable for agents" (from 문서를 에이전트가 검색하게) | the document pack (`skillcdn-document-pack`) | the document pack |
| "set up a new repository" | the setup (`git-repo-setup`) | the setup, the new app second |

Eleven of eleven requests found their skill as the first section of the index, and ten of eleven first in the whole pack; the one miss is a sibling skill of the same job sharing its words, not a reference file or a document, and the jobs index stood second in six of the whole-pack searches. That is why the index comes first and a whole-pack search is read to its third result where several skills share a job's words; the distinctive noun of the job still matters most, and a section's other phrasings find a request said another way. `browse_repo` on `marketing/skills` and `design/skills` listed every skill with the first lines of its description, enough to tell the ad from the ad research, and the study, the brief, the build, the deck and the looks apart.
