---
name: web-card-news-topic-brief
description: Finds what is worth a card news post now in the categories an account covers, in the outlets and where people are talking, lets the user pick, and turns the pick into a sourced topic brief a post can be built from, with every fact traced to a sentence of an article read in full, the angle quoted from its outlet, numbers cross-checked, unverified items listed, and the story's video clips and images collected with credits, sizes and legibility. Use when a user says "find some hot issues in these categories and I will pick one", "find the next topics for our account", "research this topic for a post with sources and images", or hands over a story to fact-check. In an account's folder it follows the account's policy and leaves out what its ledger holds. The slides and the caption are then written by html-card-news-from-brief, where a request for the whole post starts; the format comes from instagram-card-news-format-study or html-design-variations. Reads the open web; nothing is paid or posted.
license: MIT
compatibility: Needs a web search tool, a way to read a page's full text and its image elements (a fetch tool, a driven browser, or a shell with curl), and a shell with Node.js for downloading images and reading their pixel size. Optional, for the story's video, the tools docs/browser/video-clips.md names for a clip and a Chromium-family browser that playwright-core can launch for frames. Without a shell, image URLs are listed instead of downloaded.
metadata:
  author: skillcdn
  version: "1.14"
  tools: web
skillcdn:
  translations:
    ko:
      title: 출처가 붙은 카드뉴스 소재 브리프
      description: 계정이 다루는 카테고리에서 지금 카드뉴스로 만들 만한 이슈를 언론과 커뮤니티에서 찾아 사용자가 고르게 하고, 고른 것을 게시물로 만들 수 있는 소재 브리프로 만듭니다. 모든 사실은 본문까지 읽은 기사의 문장에 대응시키고, 글의 각도는 보도된 해석을 매체와 함께 인용하며, 숫자는 기사끼리 교차 확인하고, 어느 기사도 확인해 주지 않은 것은 미확인으로 적습니다. 그림은 이야기의 영상부터 찾아 쓸 만한 구간을 클립으로 남기고, 이어서 기사 사진, 기사가 인용한 영상의 장면, 당사자의 공개 페이지, 마지막으로 이미지 검색에서 찾아 캡션, 출처, 픽셀 크기, 휴대폰 크기에서의 판독성과 함께 내려받습니다. 계정의 작업 폴더에서는 계정 방침이 독자와 소재의 결을 정하고, 다룬 소재 장부에 있는 이야기는 다시 내지 않습니다. 검색 도구와 페이지 읽기, 셸로 공개 웹을 읽을 뿐 비용도 게시도 없습니다. "이 카테고리에서 핫한 이슈 찾아줘, 내가 고를게", "다음 소재 찾아와", "이 주제로 게시물 만들게 출처랑 이미지까지 조사해줘"라고 하거나 디자인 전에 사실 확인이 필요한 이야기를 넘길 때 쓰세요. 슬라이드는 html-card-news-from-brief가 만들고, 게시물 전체를 만드는 요청은 그 스킬에서 시작합니다. 포맷은 instagram-card-news-format-study가 재거나 html-design-variations가 바꿔 만듭니다.
---
# A sourced topic brief for a card-news post

The categories an account covers go in, with who the post is for; a ranked list of candidates comes out, found in the outlets and where people are talking, the user picks, and the pick becomes a topic brief: the angle as a published interpretation with its outlet and its sentence, every fact with the article sentence it rests on, numbers cross-checked, disagreements and unverified items listed, and the story's video and images on disk with captions, credits, sizes and legibility. The brief is the whole of what the slides may say and show: a reader who has met a confident, invented thesis once checks every sentence, so the brief makes that check possible before anything is designed. The first message says that the facts, the angle, the images and the beats come from this skill, and the script and the caption next, from [html-card-news-from-brief](/design/skills/html-card-news-from-brief/SKILL.md), the build skill.

## How the user is involved

- **Questions:** one message, only for what neither the request, a starting skill nor an account's policy answers. The readers, always: "Who are the readers: what do they know of the subject, and what of theirs does the story touch?", with what the request implies offered as the default so that one word continues, because a post written for a reader nobody named reads as nobody's. With them the stance and the tone, the request's implication as the default: "A neutral report, commentary, or a case for one side? Calm or aggressive?" The market or the language where the request leaves one open: "Which country or market?", "In which language will the post be?" The categories, when neither the request nor a format spec gives them.
- **Checkpoints:** the candidate list, where the user picks, with one card recommended. Then the brief, in plain words, before it is delivered. A story handed over in the request is the pick, and no list is shown.
- **Go-ahead:** skips the brief checkpoint. The pick is never made by the skill.
- **Changes mid-run:** "domestic, not global" re-ranks the candidates. A word on what the list should hold ("something hotter", "funnier", "nothing we already did") re-enters at the search as a rule for the list, and in an account's folder the skill asks whether it stands for the account. A fact the user doubts is re-read in its article; the chat points to its id while the quoted sentence lives in the brief.

## Requirements

| What | Used for |
|---|---|
| A web search tool | The candidates; the articles that carry a story. Recognize it by its action: a query in, titles and links out. |
| A way to read a page in full: a fetch tool that returns the article's text and its image elements, a browser the agent drives, or a shell with curl | The article bodies the facts come from; the figure images and their captions. Which tool reads what, and where a reading stops, is in [reading-pages.md](/docs/browser/reading-pages.md), read before the first article. |
| A shell with Node.js | Downloading images and reading their pixel size; writing the brief. Without a shell the brief lists image URLs and the delivery says they were not downloaded. |
| Optional: what [video-clips.md](/docs/browser/video-clips.md) names for fetching and cutting a clip | A clip of the story's own video. |
| Optional: a Chromium-family browser playwright-core can launch, or a driven browser that saves a screenshot to a file | Frames of a public clip the articles cite; images.md says where `playwright-core` comes from. Without either, the clip is listed as a source by its address. |
| Optional: a tool that starts agents side by side | The search split by region or by category. Without it, one search after another. |

Check the first three before the first message: without search, stop and say what to add; without a page reader, facts cannot be sourced and the run stops at the candidate list. The optional ones are checked after the pick, when a video makes them wanted, and a missing one is said in a line, the run going on with frames or photographs. Where the request or an account's policy asks for video, the clip tools are checked before the first message, by video-clips.md "What it takes", and it names what is missing and what adding it gives.

[tool-notes.md](references/tool-notes.md), how the tools behaved in runs, is read before phase 1. Links that start with `/` are files of the pack this skill is from: a copy of this directory, a plugin or a mount below the root that lacks one reads it through the pack's connection (`https://skillcdn.ai/gh/skillcdn/skills`) or at `github.com/skillcdn/skills`.

The area's rules that evidence stays apart from inference and that assumptions are written down take this form for a news post: a fact is an article's sentence, the angle is an outlet's published reading and never the agent's, and what no article confirmed is listed as unverified.

## Inputs

| Input | Source |
|---|---|
| What the brief is for | A card news post, unless the request or the skill that started this run says it is for a text that takes no images of its own (a news script, an article). Then phase 3, `canvas` and the beats are left out, `images` is an empty list, the cards and the ranking leave images out, and each message says that no images are collected and names the skill that writes that text as what comes next. What a starting skill gives (the readers, the stance, the tone, the categories, where the files go) answers this skill's questions. |
| An account's folder | Derived: the working folder holds `docs/policy.md` or `topics/covered.md`. Then read [account.md](references/account.md) before the first message: the policy answers the questions and rules the list, the ledger says what is covered, and a pick becomes a post's folder with its record. The rows below are the defaults a policy may change. |
| Categories | The format spec's `categories` when a study of the account exists (the user names the spec folder, or it sits in `card-news/` beside the brief folders); else the user's words, which then also define what fits. The spec's fields this skill reads (`categories`, `posts_read`, a type's `frames_per_slide`, `caption.credit_line_pattern`) are as [format-spec.md](/docs/card-news/format-spec.md) defines them. |
| Audience | The market, the post's language and the readers, kept in `audience` in the user's words; the angle, the facts and the beats are chosen for them. A request written in one market's language that names no market is for that market, in that language, said in the first message. |
| Stance and tone | `stance` (`report`, `commentary`, or `advocacy` with the side) and `tone` (`calm` or `aggressive`). The stance places the other side's reply among the facts for a report and after the case for advocacy, never dropped; the tone sets how far the headline goes within the facts and the attributed quotes. Neither moves the floor: a user who wants a rumor on a slide is told it stays in `unverified`. |
| Window and exclusions | Derived: the last seven days, whatever the weekday, and what the account has covered ([candidates.md](references/candidates.md) "What is left out"), unless the request or the policy says otherwise. |
| The pick | The user's: a number from the list, or a story named there or in the request (where the name matches more than one event, the most reported of the window, the others named at the brief checkpoint). A named story older than the window is researched as it is, the newest articles first; a guide rather than news (how to keep something through a season) is researched without the window, and its reason for now is the season. |
| Canvas | Derived: the spec's documented size, else the documented portrait size of Instagram, the platform the neighbouring skills build for, unless the request names another, looked up at run time (1080 by 1350 for 4:5 at the time of writing, illustrative) and written into `canvas` with its source and the day. |
| Where the brief goes | Derived: the folder the user or a starting skill names; in an account's folder, the post's folder; else `card-news/<story>/` under the working folder (under the host's scratch folder when the working folder is a git checkout, under the user's home without one; a working folder named `card-news` is that folder), created after the pick, with `img/` inside. The candidate list is written as `card-news/candidates-<YYYY-MM-DD>.md` when its checkpoint is shown, so that a run cut off before the pick keeps it, and moved into the brief folder as `candidates.md`. Said in the message that creates it. |

## Workflow

Each phase produces a named artifact in the brief folder, by the reference it names, which is read first.

### Phase 1: Candidates

Produces the **candidate list**, by [candidates.md](references/candidates.md).

1. List the seasons and dates ahead of the readers, then search each category in the window, in the outlets and where the market's readers talk.
2. Open the one or two articles each story cites and write its card from the body, in the card's shape there.
3. Leave out what the account has covered and what the user's words or the lane leave out, and keep the most talked about of those for the top of the list, each with the rule that caught it. Rank the rest, keep five to eight and never pad the list.

Checkpoint: the stories a rule kept off the list, then the cards, numbered, with one recommended and why; "pick a number, or name a story of your own; the pick also lets me collect its video and images". The run waits.

### Phase 2: Facts

Produces the **facts table** (`facts.md`; it becomes the brief's `facts`) and the **articles read** list, by [sourcing.md](references/sourcing.md). Read with it [readers.md](/docs/writing/readers.md) and [facts.md](/docs/writing/facts.md) of the pack's writing set; sourcing.md is this brief's sharper form of them and wins where they differ.

1. Read three or more articles on the pick in full, from different outlets, and record each.
2. Extract every fact the post could use as its own sentence, with the article's sentence beside it; look for the facts that show the story in the readers' own case before general figures.
3. Cross-check every number and date across the articles; where two differ, record both and choose with the reason. A fact in one article only is marked single-source.
4. Find the angle: the interpretation the outlets share, quoted from the article that states it best, chosen among several readings for the brief's readers and, where the stance is a side's case, from that side (sourcing.md "The angle"). A statement an outlet printed with its speaker is not left out for its strength; what the agent leaves out of the brief it names at the checkpoint, where the user decides.
5. List as unverified what the post would want and no article gave: a handle for a mention, an official notice, a figure seen only in a summary.

### Phase 3: Images

Produces the **image set** in `img/` and its entries, by [images.md](references/images.md). Left out for a brief that takes no images.

1. Draft the beats under the table in `facts.md`: five to eight, in story order, each naming its facts, one of them the readers' own case where the facts hold it. What each beat has to show is what the set is judged against.
2. Look in the order images.md gives, the story's own video first, as a clip, and stop when every beat has what the set must hold. No clip worth taking is a normal result: photographs alone, said in a line.
3. Download and measure each, judge it at phone size, and set aside what is not kept with its reason.
4. Write the entries and `credits.md`.

### Phase 4: Brief

Produces the **topic brief** (`topic-brief.json`, its fields by [topic-brief.md](/docs/card-news/topic-brief.md), its shape in [topic-brief.example.json](assets/topic-brief.example.json)) and the second checkpoint.

1. Assemble the fields; every fact keeps its source sentence, every image and clip its credit.
2. Finish the beats, each naming its fact ids and an image role, and write a working `headline` in the angle's words, or from the leading fact when the story has no angle. They are the build's starting point, not the script.

Checkpoint, in plain words: the stance and the tone; the angle with its outlet; the facts in a short list with their outlets; the disagreements and how they were settled; the unverified items; the clips and the images with where each came from, what it shows, its size and its legibility, which beats needed a search, and where no clip was taken, why; the suggested beats. "OK" delivers.

### Phase 5: Deliver

One message: the brief folder and its files; the angle in a line with its outlet; the number of articles read and of facts; the disagreements; the unverified list, as what the user checks before publishing; the clips and the images with where each came from, the ones that will upscale at the canvas and the soft ones; for a story still moving (an investigation, a ruling awaited), that the newest reports are read again before it is published; and that the script and the caption come next, from the build skill, after the design variations where the build is making a format of the user's own.

## Verdicts

| Result | Verdict |
|---|---|
| A card's line that the article's body does not carry | Rewritten from the body, or the card dropped |
| A story a rule keeps off the list while people talk about little else | Shown above the cards with the rule; never dropped silently |
| A fact with no article sentence beside it | Not in the brief; re-read the article or drop it |
| A number in one article only | Kept, marked single-source; the build says so if it uses it |
| Two articles disagree on a number | Both recorded; the one with the primary source (an official release, the outlet that first reported) used, the reason written |
| A superlative or a comparison with no source, or one an earlier article contradicts | Dropped; the contradicted one with both in `disagreements` |
| A page that is not an outlet's article: a post on a community board or a social platform, an influencer's post on a portal, a listing or aggregator site, a blog | A lead, not a source; what only it says goes to `unverified` |
| An organizer's, a venue's, an institution's or the subject's own page or notice, for a schedule, a price, an address or another fact of its own matter | A source for that fact only (`source.kind` `official`, `single_source` true); the story itself still needs an outlet's article |
| An image or a clip | By the table in images.md "Legibility and what an image is": it shows a thing the facts name, reads at phone size, and is a picture of the event or is marked as not |

## Hard rules

1. Sources are article bodies read in full. A search summary, a headline, a community post or the agent's memory is never a source, for a fact or for a card's line: a draft built from summaries put an unsourced superlative and a foreign figure on a slide, and the user caught it.
2. Every fact carries the sentence it rests on. A sentence that cannot be traced is not written.
3. The angle is a published interpretation, quoted with its outlet, whichever side the user's stance takes; a story whose outlets share none has no angle yet, and the brief says so. The skill does not invent why a story matters, and a rumor is an unverified item, never a fact, whatever the tone.
4. The pick is the user's, made at the candidate checkpoint or given in the request, and a rule that excludes a story is a reason to show it with the rule, not to hide it: the week's most talked-about story, kept off a list by three rules and noted in one line, was the next day's biggest news.
5. Images show the story. They come from where the story's own video and the articles point, in the order images.md gives, and from an image search only for what those leave unshown; none is generated or taken from a stock library unless the user asks for that; all are collected only after the pick. A brief whose photos showed nothing of the story sent the build to the clip the articles cited, and that is where the images were.
6. Every image is judged legible at phone size, at about a third of the canvas width, before it is kept for a slide that has to be read. Slides built on frames that were blur alone were sent back with "this cannot be seen".
7. No paywall, no login, no bypass: what cannot be read in full is not used. A site that refuses this host is not read from it: one source among several gives way to the next, and the run stops only where the pick's own articles cannot be read ([tool-notes.md](references/tool-notes.md) "A site this host cannot read").
8. Nothing is spent and nothing is posted.

## Terminology

| Term | Meaning |
|---|---|
| Candidate | A story that fits the categories and the audience, with the articles that carry it, before the user picks. |
| Lead | What points to a story and is not a source: a search result, a headline, a community post. |
| Pick | The candidate the user chose, or a story they named instead. |
| Fact | One sentence the post may use, with the source sentence, quoted from the article, that it rests on. |
| Angle | The interpretation the post runs on, as published by an outlet and quoted. |
| Single-source | A fact found in one article only. |
| Unverified | What the post would want to say and no article confirmed. |
| Clip, frame | A few seconds cut from the story's own video, with its first frame as its poster; one still of a video, saved with its time code, whose caption is the text printed on it. |
| Beat | One step of the story's order, naming the facts it carries; the build's starting point. |
