# Finding a skill: how it works and how it is kept working

For whoever maintains this repository or a fork of it. How an agent that has just connected finds the skill for a request, what bounds that as the pack grows, and how it is checked. The pages the agent reads are [`docs/pack/finding-a-skill.md`](../docs/pack/finding-a-skill.md) and [`docs/pack/jobs.md`](../docs/pack/jobs.md); this page is for the people who keep them true, and no page an agent reads sends it here.

## What an agent does

A fresh agent with a request and the pack's connection reads, in this order: the connection instructions, which say `Start here, before a task: read_repo_file docs/pack/finding-a-skill.md.` because the root manifest names that page as its `start` (SkillCDN 0.6.0); that page, whole; the jobs index, searched with `search_repo` scoped to `docs/pack` in English words for the request; the matching section by its offset, or the area's skills with `browse_repo`; then `load_skill` on the path the section names. That is three to five reads of the pack before the skill. A request that no skill does ends with the agent saying so after one more search of the whole pack. An area's line in the connection instructions was a hint at most: every session went on to the page the root names before it chose (11 fresh sessions, one request each, Opus 5.5 at high effort, SkillCDN 0.5.2, 2026-11).

A request whose material sits in another connection is where a session passed the pack by. Asked to find three answers "in the SkillCDN documents" with SkillCDN's documentation connected beside this pack, a fresh session searched that pack, answered without reading its quotes again, and took `skillcdn-document-answer` only on a line of direction; the root description then named the page without saying to read it first. Since it says "Before a job, find its skill", the same request read `finding-a-skill.md` and the jobs index and loaded the skill unprompted. The sentence costs a one-line request little: a sentence to translate was answered once after three reads of the pack and a remark that no skill fits, and once, after the page said such a request takes no search, with no read at all (5 fresh sessions, Opus 5.5 at high effort, SkillCDN 0.5.3, 2026-11).

The rounds above ran when the root description itself ended on that sentence ("Before a job, find its skill"); since the manifest names the page as its `start`, the connection says it in the place of the README line and the description carries the jobs alone. So the `start` line is the one sentence the whole finding hangs on, and `finding-a-skill.md` is the one page every session reads whole. Under reading rules 22 with `start`, eight fresh sessions, one request each (the seven requests the market chain, the studio and the product deck added to the table below, and the winter camping post), all read `finding-a-skill.md` first from the `start` line and all found their skill, with three to five reads of the pack before `load_skill` and every page of the skill read; the scoped search of `docs/pack` missed the right section in five of the eight while the deployment's meaning index held 107 of its 230 documents, and each of those sessions went on to read the jobs index or to search the whole pack, and found it there (commit 8925ee8, SkillCDN 0.6.1, Opus 5.5 at high effort, 2026-11).

## What bounds it as the pack grows

- **The connection instructions hold 2,000 characters.** The head (the root's name, its description cut to 240 characters, the counts), the manifest and overview lines and the closing lines on the tools always stand; the folders share what is left, one line each in path order, and every folder keeps its line while its path fits. Where the lines do not fit whole, the descriptions are cut to one length for all of them, the greatest that fits, a short one staying whole; below 24 characters they are left out, then the names are cut the same way and left out below 16; a folder is left out, and counted in a line of its own, only when the paths and counts alone do not fit (`fitInstructions` in SkillCDN's `@skillcdn/core`, 0.5.3; through 0.5.2 the folder that did not fit and every one after it were left out without a word). With seven areas and `docs/`, the instructions took 1,996 of the 2,000 characters `npx @skillcdn/cli@latest check` counts, every folder's description cut to 84 characters, and the check said that the folder lines say less, to fit (2026-11); `npx @skillcdn/cli@latest check` prints the length today, beside what a client is told; `writing/` took its line with its first skill, and six areas stood at the full cut of 100 before it. The next folder with a line cuts them all further, and thirteen folders to about 40. The check says beside the length when the folder lines say less or how many are left out; say in the change that adds an area what it then prints. The root description is in the head and is not cut for the folders; the line that sends an agent to the page that finds a skill comes from the manifest's `start`, not from the description.
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
| "SkillCDN 문서에서 찾아서 알려줘." and three questions on the connection instructions, a name joined by capitals and a price (find it in the SkillCDN documents), asked without the test sentence, with SkillCDN's documentation connected beside the pack | `skillcdn-document-answer`, loaded unprompted |
| "이 문장 영어로 자연스럽게 바꿔줘: 내일 회의는 오후 3시로 미뤄졌습니다." (put this sentence into natural English), asked without the test sentence | none, and no search of the pack |
| "다음 달 신제품 출시 보도자료 써줘." (write the press release for next month's launch) | none: the agent says so, and names `docs/writing/` as what it would write by |
| "뉴스 앵커 리포트 써줘." (write a news anchor report), asked without the test sentence | `web-news-anchor-report-script` |
| "어느 시장에 들어갈지 실제 통계로 찾아 줘, 한국이랑 미국." (find which market to enter from real statistics, Korea and the US) | `web-market-entry-signals` |
| "지켜보는 시장들 이번 주 다시 재 줘." (measure the markets we watch again this week) | `web-market-entry-signals`, its round |
| "이 회사 작년 영업이익 공시로 확인해 줘." (check this company's operating profit last year in its filings) | `dart-company-figures` |
| "이 사업 아이템 법이랑 경쟁자까지 깊게 조사해 줘." (look into this business idea in depth, the law and the competitors too) | `web-item-deep-dive` |
| "이번 조사로 시장 매거진 이번 호 만들어 줘." (make this issue of the market magazine from the research) | `html-signal-magazine` |
| "우리 팀이 광고 소재를 계속 만들고 최적화하는 저장소를 세팅해 줘." (set up a repository where our team keeps making and tuning ad creatives) | `git-studio-setup` |
| "우리 제품 소개 덱 만들어줘." (make our product introduction deck) | `html-product-deck` |

All eleven found what they must under SkillCDN 0.5.2 (2026-11-16), on commit 00e0d5d and again on commit cd13d10, before and after `finding-a-skill.md` lost its list of what each area holds and its table of examples to this page, with three to five reads of the pack before the skill both times; the session with no skill to find read the jobs index's section on jobs with no skill before it said so. The twelfth request joined the round with the writing set and was run alone, as a subagent with the pack's four read tools and nothing else, on commit 76aad81 under SkillCDN 0.5.3 (2026-11-21): it read the finding page, searched the jobs index and read it whole, searched the whole pack once and read the writing set's index, five reads of the pack, then said that no skill writes a press release, named the three nearest skills with what each does not do, and offered to write by the set's pages. The thirteenth joined with the writing area's first skill and was run as that skill's own fresh run, on commit 9b7e736 under SkillCDN 0.5.3 (2026-11-21), minutes after the push: the session read the finding page, searched the jobs index, which returned the card news sections and not yet the new one while the mount's meaning index was still embedding the commit, browsed `writing/skills` and loaded the skill, three reads of the pack; the same search returned the new section first once the embedding was complete. The round as a whole was not run again for the area's changed description and the page's list of folders.

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
