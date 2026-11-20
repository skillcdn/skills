# Finding a skill: how it works and how it is kept working

For whoever maintains this repository or a fork of it. How an agent that has just connected finds the skill for a request, what bounds that as the pack grows, and how it is checked. The pages the agent reads are [`docs/pack/finding-a-skill.md`](../docs/pack/finding-a-skill.md) and [`docs/pack/jobs.md`](../docs/pack/jobs.md); this page is for the people who keep them true, and no page an agent reads sends it here.

## What an agent does

A fresh agent with a request and the pack's connection reads, in this order: the connection instructions, where the root description's last sentence names `docs/pack/finding-a-skill.md`; that page, whole; the jobs index, searched with `search_repo` scoped to `docs/pack` in English words for the request; the matching section by its offset, or the area's skills with `browse_repo`; then `load_skill` on the path the section names. That is three to five reads of the pack before the skill. A request that no skill does ends with the agent saying so after one more search of the whole pack. An area's line in the connection instructions was a hint at most: every session went on to the page the root names before it chose (11 fresh sessions, one request each, Opus 5.5 at high effort, SkillCDN 0.5.2, 2026-11).

So the root description's last sentence is the one sentence the whole finding hangs on, and `finding-a-skill.md` is the one page every session reads whole.

## What bounds it as the pack grows

- **The connection instructions hold 2,000 characters.** The head (the root's name, its description cut to 240 characters, the counts), the manifest and overview lines and the closing lines on the tools always stand; the folders share what is left, one line each in path order, and every folder keeps its line while its path fits. Where the lines do not fit whole, the descriptions are cut to one length for all of them, the greatest that fits, a short one staying whole; below 24 characters they are left out, then the names are cut the same way and left out below 16; a folder is left out, and counted in a line of its own, only when the paths and counts alone do not fit (`fitInstructions` in SkillCDN's `@skillcdn/core`, 0.5.3; through 0.5.2 the folder that did not fit and every one after it were left out without a word). With six areas and `docs/`, the instructions take 1,989 of the 2,000 characters `npx @skillcdn/cli check` counts, every folder's description at its cut of 100 characters (2026-11): the next area cuts them all to about 88, and thirteen folders to about 40. The check says beside the length when the folder lines say less or how many are left out; say in the change that adds an area what it then prints. The root description, which ends on the page that finds a skill, is in the head and is not cut for the folders: keep that sentence last.
- **An area's line quotes at most 99 characters of its description and an ellipsis, fewer once the folders must share the room.** Put the area's kinds of work first, in a user's words, the most asked before the fortieth character; for an area of many skills, name the kinds rather than the skills, so that none is hidden past the cut.
- **`finding-a-skill.md` is read whole by every session, before anything else.** It holds the method only: the layout, the ways to find a skill, reading a result, what to do when nothing fits. What the pack holds is the jobs index's, the catalogs' and the connection's; the evidence that the method works is this page's. A line that names every skill, or a table of results, grows with the pack and is paid for by every session.
- **`jobs.md` grows with every skill and is never read whole on the way.** It is searched and read a section at a time, so its size costs nothing until a search misses; its headings are the sentences users say, because a search ranks a heading above a body.

## How it is checked

- `node scripts/check.mjs` fails a skill with no section in `jobs.md`.
- **The search examples** below are run with `search_repo` against the deployment, scoped to `docs/pack` and then unscoped, when the search changes (a release of SkillCDN that changes ranking) or a skill is renamed or added.
- **The fresh-agent round** is run when `finding-a-skill.md`, the root description or an area's description changes, or an area is added: one headless session per request, each in an empty folder of its own, Opus at high effort, with only the pack's read tools allowed, and the request followed by one sentence in its language: "This is a test: pick the skill you will use, go only as far as the skill's first question to me, its first spend or its first file written, then stop and say which skill you chose (or that none fits) and how you found it." The transcripts under `~/.claude/projects/<slug of the folder>/` say which reads each session made; a session that chose the wrong skill, or took more than five reads of the pack to find it, is a finding about the page it read last.

The requests of the round, with the skill each must find:

| Request | Skill |
|---|---|
| "우리 사내 핸드북에서 재택근무 규정이 어떻게 되어 있는지 찾아서 알려줘." (what our handbook says on remote work) | `skillcdn-document-answer` |
| "오늘 고객사 미팅 메모 줄 테니까 바로 보낼 수 있게 회의록 만들어줘." (minutes to send today from my client meeting notes) | `html-meeting-minutes-from-notes` |
| "내 데스크 세팅해줘." (set up my desk) | `git-desk-setup` |
| "겨울 캠핑 주제로 인스타 카드뉴스 만들어줘." (an Instagram card news post on winter camping) | `html-card-news-from-brief` |
| "경쟁사들이 요즘 어떤 광고를 돌리는지 보고 우리 광고 방향 잡아줘." (see what ads competitors run and set our direction) | `meta-ad-library-creative-research` |
| "요즘 미국에서 광고비를 늘리면서 뜨는 앱이나 서비스가 뭔지 알려줘." (which apps or services are rising on growing ad spend in the US) | `meta-ad-library-rising-products` |
| "이 PDF 제안서를 우리 피그마 발표자료에 슬라이드로 옮겨줘." (move this PDF proposal into our Figma deck as slides) | `figma-slides-from-content` |
| "앱스토어 리뷰들에 답글 좀 달아줘." (reply to our App Store reviews) | none: the agent says so |
| "Give me a few different directions for our landing page hero before we build it." | `html-design-variations` |
| "우리 사이트 매출이랑 광고 성과를 한눈에 보는 관리자 페이지 만들어줘." (an admin page with our site's sales and ad results at a glance) | `cloudflare-admin-dashboard` |
| "회사 정책 문서들이 PDF로 잔뜩 있는데, 에이전트가 검색해서 쓸 수 있게 만들어줘." (make our policy PDFs searchable for agents) | `skillcdn-document-pack` |

All eleven found what they must under SkillCDN 0.5.2 (2026-11-16), on commit 00e0d5d and again on commit cd13d10, before and after `finding-a-skill.md` lost its list of what each area holds and its table of examples to this page, with three to five reads of the pack before the skill both times; the session with no skill to find read the jobs index's section on jobs with no skill before it said so.

## Search examples

What `search_repo` returned for twelve requests, five said in English, five translated from Korean to English words first, and one for each of the two newest skills, scoped to `docs/pack` and then unscoped, and what `browse_repo` showed for two areas, on the day named.

Checked 2026-11-21, on commit 6739fa8 under SkillCDN 0.5.3 (reading rules version 19, which reads a name joined by capitals by its words too), with the deployment's meaning index complete and every result ranked by words and meaning. "Index" is the first section of the first result with `path` set to `docs/pack`, which was the jobs index every time; "whole pack" is the first result without a path.

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
| "set up my desk" | the desk (`git-desk-setup`) | the desk, the repository setup second |

Twelve of twelve requests found their skill as the first section of the index, and eleven of twelve first in the whole pack; the one miss is a sibling skill of the same job sharing its words, not a reference file or a document, and the jobs index stood second in six of the whole-pack searches. The same twelve on commit cd13d10 under SkillCDN 0.5.2 (2026-11-16) returned the same, as eleven of them did on commit 4cf4176 under SkillCDN 0.5.1 (2026-11-15), while `finding-a-skill.md` still held this table. That is why the index comes first and a whole-pack search is read to its third result where several skills share a job's words; the distinctive noun of the job still matters most, and a section's other phrasings find a request said another way. `browse_repo` on `marketing/skills` and `design/skills` (2026-11-16) listed every skill with the first lines of its description, enough to tell the ad from the ad research, and the study, the brief, the build, the deck and the looks apart.
