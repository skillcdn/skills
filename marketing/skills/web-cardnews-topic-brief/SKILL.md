---
name: web-cardnews-topic-brief
description: Finds what is worth a card-news post this week in the categories an account covers, lets the user pick one, and turns the pick into a topic brief a post can be built from, with every fact traced to a sentence of an article read in full, the angle as a published interpretation quoted from its outlet, numbers cross-checked, unverified items listed, and the images that show the story collected from where the articles point (their photos, the clip or footage they cite as frames, the subject's public pages, a search last), each with its caption, credit, pixel size, legibility and licence terms. Reads the open web; nothing is paid or posted. Use when a user says "find some hot issues in these categories and I will pick one", "research this topic for a post with sources and images", or hands over a story to fact-check. The slides and the caption are then written from the brief by html-cardnews-from-brief, so a request for the whole post starts here; the account's format comes from instagram-cardnews-format-study.
license: MIT
compatibility: Needs a web search tool, a way to read a page's full text and its image elements (a fetch tool, a driven browser, or a shell with curl), and a shell with Node.js for downloading images and reading their pixel size; for frames of a clip the articles cite, a Chromium-family browser that playwright-core can launch. Works in any agent that can search the web and run a shell; without a shell, image URLs are listed instead of downloaded.
metadata:
  author: skillcdn
  version: "1.2"
  tools: web
skillcdn:
  include:
    - references/candidates.md
    - references/sourcing.md
    - references/images.md
    - references/tool-notes.md
    - assets/topic-brief.example.json
    - /marketing/docs/cardnews/topic-brief.md
    - /docs/browser/reading-pages.md
  translations:
    ko:
      title: 출처가 붙은 카드뉴스 소재 브리프
      description: 계정이 다루는 카테고리에서 이번 주에 카드뉴스로 만들 만한 이슈를 찾아 사용자가 고르게 하고, 고른 것을 게시물로 만들 수 있는 소재 브리프로 만듭니다. 모든 사실은 본문까지 읽은 기사의 문장에 대응시키고, 글의 각도는 보도된 해석을 매체와 함께 인용하며, 숫자는 기사끼리 교차 확인하고, 어느 기사도 확인해 주지 않은 것은 미확인으로 적습니다. 이미지는 이야기를 가장 잘 보여 주는 것을 기사가 가리키는 곳에서 찾습니다(기사 사진, 기사가 인용한 방송 클립이나 영상의 장면을 시각 표시와 함께, 당사자의 공개 페이지, 마지막으로 이미지 검색). 하나하나 캡션·출처·픽셀 크기·휴대폰 크기에서의 판독성·라이선스 조건과 함께 내려받습니다. 검색 도구와 페이지 읽기, 셸로 공개 웹을 읽을 뿐 비용도 게시도 없습니다. "이 카테고리에서 핫한 이슈 찾아줘, 내가 고를게", "이 주제로 게시물 만들게 출처랑 이미지까지 조사해줘", "스크립트·이미지·캡션 제안해줘", 또는 디자인 전에 사실 확인이 필요한 이야기를 넘길 때 쓰세요. 슬라이드는 html-cardnews-from-brief가 만들고, 계정의 포맷은 instagram-cardnews-format-study가 냅니다.
---
# A sourced topic brief for a card-news post

The categories an account covers go in, with who the post is for; a ranked list of this week's candidates comes out, the user picks one, and the pick becomes a topic brief: the angle as a published interpretation with its outlet and its sentence, every fact with the article sentence it rests on, numbers cross-checked, disagreements and unverified items listed, and the images that show the story on disk with captions, credits, pixel sizes, legibility and licence terms. The images come from where the articles point, in order: the articles' own photographs, the material the articles cite (a broadcaster's clip of the report, the footage or the post the story is about), the subject's own public pages, and an image search only for what those leave unshown; a photo that does not show the story is not an image of it, however well credited. The brief is what the build skill writes slides and the caption from, and it is the whole of what the slides may say and show: a reader who was burned once by a confident, invented thesis checks every sentence, so the brief makes that check possible before anything is designed. The first message says so: the facts, the angle, the images and the beats come from this skill; the script and the caption are written from them next, by the build skill.

## How the user is involved

- **Questions:** the audience, once, and only the half the request leaves open: "Which readers: which country or market?" when "domestic" names no country and neither the post's language nor the spec's account points to one market, and "In which language will the post be?" when neither the request nor the market's one language says. The categories, when neither the request nor a format spec gives them. Nothing else is asked.
- **Checkpoints:** the candidate list, where the user picks, with one card recommended (a stop that is not skipped: the pick is theirs); the brief, in plain words, before it is delivered. Picking a story also accepts that its images are collected into the brief folder (the articles' photos, frames of a clip they cite, the subject's public images, an image search where those leave a beat unshown), and the brief checkpoint lists each file with where it came from, what it shows, its size and its legibility. A story handed over in the request is the pick, and the list is not shown.
- **Go-ahead:** when the user says to go ahead alone after the pick, the brief checkpoint is skipped; the pick itself is never made by the skill.
- **Changes mid-run:** "domestic, not global" re-ranks the candidates; a fact the user doubts is re-read in its article, and the chat points to its id while the quoted sentence lives in the brief.

## Requirements

| What | Used for |
|---|---|
| A web search tool | The candidates of the week; the articles that carry a story. Recognize it by its action: a query in, titles and links out. |
| A way to read a page in full: a fetch tool that returns the article's text and its image elements, a browser the agent drives, or a shell with curl | The article bodies the facts come from; the figure images and their captions ([images.md](references/images.md) "Finding the images in an article"). Which tool reads what, and where a reading stops, is in [reading-pages.md](/docs/browser/reading-pages.md), included with this skill. |
| A shell with Node.js | Downloading images with the article as referer and reading their pixel size; writing the brief. Without a shell the brief lists image URLs and the delivery says they were not downloaded. |
| Optional: a Chromium-family browser playwright-core can launch, or a driven browser that saves a screenshot to a file | Frames of a public video clip the articles cite, saved with their time codes ([images.md](references/images.md) "Frames from a clip the articles cite"; the routes in [video-frames.md](/docs/browser/video-frames.md)). `playwright-core` is borrowed from a neighbouring project's install or installed into the brief folder, and a browser download is asked first, as [headless.md](/docs/browser/headless.md) says; check it with a `require` from the shell. Without either, the clip is listed as a source by its address, and the delivery says the frames were not taken. |

Check these before the first message. Without search, stop and say what to add; without a page reader, facts cannot be sourced and the run stops at the candidate list. No paywall is bypassed and no account is signed in to: an article that cannot be read in full is not a source. What the card-news skills share is in the area's document set [`marketing/docs/cardnews/`](/marketing/docs/cardnews/README.md); [topic-brief.md](/marketing/docs/cardnews/topic-brief.md), the fields of what this skill writes, is included and arrives with this skill wherever SkillCDN serves it, and so is [reading-pages.md](/docs/browser/reading-pages.md) from the repository's document set [`docs/browser/`](/docs/browser/README.md), whose [video-frames.md](/docs/browser/video-frames.md) and [headless.md](/docs/browser/headless.md) phase 3 reads when a clip is a source. A copy of this directory lacks the included pages, and a mount of one area or one skill cannot read the linked ones: say so, fetch them from `marketing/docs/cardnews/` and `docs/browser/` of the repository this skill comes from (for this pack, `github.com/skillcdn/skills`), and otherwise write the brief by the example in [topic-brief.example.json](assets/topic-brief.example.json), which is the shape. How the tools behaved in runs of this skill is in [tool-notes.md](references/tool-notes.md); read it before phase 1.

The area's rule that claims and assets come from the brand takes this form for a news post: the user is the brand, the claims are the articles', and the images are the outlets', agencies', broadcasters' and subjects' material, used as the account itself uses such material, with their credits. The skill records each image's source, credit and terms and leaves the use to the user, who is told so at every delivery; a user who prefers their own images supplies them, and the entries then carry the user's files.

## Inputs

| Input | Source |
|---|---|
| Categories | The format spec's `categories` when a study of the account exists (the user names the spec folder, or it sits beside the run); else the user's words, which then also define what fits. Asked only when neither gives them. |
| Audience | The market (a country or a region) and the post's language; asked only for the half the request leaves open. A domestic audience means the market's outlets first and a global story only where it is that market's reader's story too. The brief's language is the post's language. |
| Exclusions | Derived: what the account has already posted, from the spec's `posts_read`; with no spec, nothing is excluded and the list says so. |
| The pick | The user's: a number from the list at the candidate checkpoint, or a story named there or in the request, which goes through phases 2 to 4 like a pick. |
| Canvas and photo treatment | Derived: the spec's documented size when a spec exists, else the platform's documented portrait size looked up at run time (1080 by 1350 for 4:5 at the time of writing, illustrative); it decides what [images.md](references/images.md) "Choosing" says about each image's size. The spec's slide types say how the account treats its images (cropped full-bleed, or frames of a broadcast kept whole with their captions), which decides what the set must hold: an account that stacks frames needs the frames whose captions carry the facts. |
| Where the brief goes | Derived: the folder the user names, else `cardnews/<story>/` under the host's scratch or working folder, outside any git checkout, created after the pick and named after the story in a few words; `img/` inside it. The candidate list is written as `cardnews/candidates-<YYYY-MM-DD>.md` when the checkpoint is shown, so that a run cut off before the pick keeps it, and moved into the brief folder as `candidates.md` once the folder exists. Said in the message that creates it. |

## Workflow

Each phase produces a named artifact in the brief folder.

### Phase 1: Candidates

Produces the **candidate list** ([candidates.md](references/candidates.md)) and the first checkpoint.

1. Search each category for the last seven days, in the market's language and outlets first, as candidates.md "Searching" says; read enough of each result to know what the story is and whether it moved this week.
2. Keep five to eight in all, at most three per category, ranked by candidates.md "Ranking": fit to the categories and the audience, why it is timely now, whether it saves or shares, whether images of the story exist (photos in the articles, a clip or footage the articles cite). Drop what the account has already covered.
3. Write each as a candidate card: one line of what happened, one line of the angle a post could take, why now, two or more articles with their dates, and a note on what images exist, from the article pages opened for the card (their photos; a broadcast or footage they cite).

Checkpoint: the list, categories in the order of their best card and cards ranked inside, numbered across the whole list, with one card recommended and why; "pick a number, or name a story of your own; the pick also lets me collect its images". The pick is the user's; the run waits.

### Phase 2: Facts

Produces the **facts table** (`facts.md`, by [sourcing.md](references/sourcing.md); it becomes the `facts` field of the brief) and the **articles read** list.

1. Read three or more articles on the pick in full, from different outlets; a search summary or a snippet is not a source, and an article counts as read in full only when its end was reached, as sourcing.md "Reading" says. Record, per article, the outlet, the author where named, the date and time, the URL and its kind.
2. Extract every fact the post could use as its own sentence, with the article's sentence beside it, by sourcing.md "The facts table": numbers, dates, places, quotes with who said them, events, claims. Convert relative dates to absolute ones.
3. Cross-check every number and date across the articles; where two differ, record both and choose with the reason, in the precedence sourcing.md gives. A fact in one article only is marked single-source.
4. Find the angle: the interpretation the outlets share, quoted from the article that states it best, with its outlet and date. The agent's own reading of why the story matters is not an angle; sourcing.md "The angle" says what qualifies.
5. List as unverified what the post would want and no article gave: a handle for a mention, an official notice, a figure seen only in a summary.

### Phase 3: Images

Produces the **image set** in `img/` and the image entries ([images.md](references/images.md)).

1. List what the post has to show, from the facts, as a draft of the beats (five to eight, in story order, each naming its facts), written under the table in `facts.md`; phase 4 finishes them. The list names the subject, the scene of the event, the thing each fact names, the document or the post the story is about, and it is what the set is judged against; a well-credited photo that shows none of it is not an image of the story.
2. Look where the articles point, in the order images.md "Where images come from" gives, and stop when every beat has an image that shows it, except that the material the articles cite is read whenever the account's format keeps such frames whole: the articles' figure images with their printed captions and credits (images.md "Finding the images in an article"; the share image where it is the only one, credited to the outlet with `source_kind` `share-image`); the material the articles cite, where it is public (a broadcaster's clip of the report, the footage or the post the story is about), as frames with their time codes and their own on-screen captions (images.md "Frames from a clip the articles cite"); the subject's own public pages the articles link; and an image search last, for what is still unshown, said at the checkpoint with what was looked for first.
3. Download each with the page as referer and a browser user agent; read its pixel size with the size script ([image-size.example.mjs](scripts/image-size.example.mjs)) or a few lines like it, a frame's from the capture table; note any mark or logo and where it sits; note the licence terms the publisher states, and whether they allow modification. Judge each image's legibility at phone size (images.md "Legibility and what an image is"): a frame that is blur or mosaic alone, a scene too dark to show its subject, or a small picture that would upscale past about two times shows nothing on a slide. A re-enactment, an illustration or a generated image inside the material is not a photograph of the event and is marked so.
4. Keep what a post can use, two or three images per beat and a few spares where the account crops photographs: at least one legible image that works as a portrait cover (vertical, or horizontal with its subject central enough to crop; a clear frame where the spec's cover is itself a frame kept whole), the subject shots the facts need, and a mood shot. Where the account's format keeps frames whole, as many clear frames per beat as the spec's type stacks on one slide (its `frames_per_slide`), each with a caption that states a fact of the table. images.md "Choosing" gives, against the canvas, which sizes render clean and what to do below them. Downloads not kept go to `img-unused/` in the brief folder with one line each in `credits.md` on why (a duplicate, smaller, a large mark, no credit, unreadable), so that the user or the build can swap one in; a clip's unkept frames stay in their capture folder with one line for the clip.
5. Write the entries with `source_kind`, `shows`, `role`, `px`, `legibility`, `watermark`, `licence` and `credit`.

### Phase 4: Brief

Produces the **topic brief** (`topic-brief.json` by [topic-brief.md](/marketing/docs/cardnews/topic-brief.md); shape in [topic-brief.example.json](assets/topic-brief.example.json)), a **credits list** (`credits.md`: first one line per kept image in the spec's credit-line pattern, else as images.md "The credit line" says; then, under its own heading, the set-aside list), and the second checkpoint.

1. Assemble the fields; every fact keeps its source sentence, every image its credit.
2. Suggest five to eight beats in story order, each naming the fact ids it would carry and an image role; a working `headline` in the angle's words, or from the leading fact when the story has no angle. These are a starting point for the build skill, not the script.

Checkpoint, in plain words: the angle with its outlet; the facts in a short list with their outlets; the disagreements and how they were settled; the unverified items; the images with their files, where each came from, what it shows, its size, its legibility and any licence limit, and which beats needed a search; the suggested beats. "OK" delivers.

### Phase 5: Deliver

One message: the brief folder with `topic-brief.json`, `img/`, `img-unused/`, `credits.md`, `facts.md` and `candidates.md`; the angle in one line with its outlet; the number of articles read and of facts; the disagreements; the unverified list, repeated as what the user checks before publishing; the images with where each came from, their sizes, the ones that will upscale at the canvas, the soft ones, and any under a licence that forbids modification; that the images are the outlets', agencies', broadcasters' and subjects' material, used with credit at the user's discretion, and where a clip names the footage's origin, that origin; and that the script and the caption come next, from the build skill.

## Verdicts

| Result | Verdict |
|---|---|
| A fact with no article sentence beside it | Not in the brief; re-read the article or drop it |
| A number in one article only | Kept, marked single-source; the build says so if it uses it |
| Two articles disagree on a number | Both recorded; the one with the primary source (an official release, the outlet that first reported) used, the reason written |
| An interpretation the agent arrived at and no article states | Not the angle; the angle is the one the outlets share, or the brief says the story has none yet |
| A superlative or a comparison with no source ("the fastest", "the first") | Dropped |
| A superlative the outlets printed that an earlier article contradicts (a "first" that happened before) | Dropped, with both in `disagreements` |
| A page that is not an outlet's article: an influencer's post on a portal, a listing or aggregator site, a blog | Not a source; what only it says goes to `unverified` |
| An image that shows nothing the facts name (a stock scene, a logo, an unrelated file photo) | Not in the set, however well credited; the next source in order is read |
| A frame or a photo whose subject cannot be made out at phone size (blur or mosaic alone, a dark scene, motion blur) | `legibility` "unreadable": set aside, or kept only as a background under type, said so; a slide that has to be read takes only a clear one |
| A re-enactment, an illustration or a generated image inside the material | Not a photograph of the event: `role` "illustration" with `notes` saying what it is, or not kept |
| A frame whose printed caption states something no article body carries | Kept for what it shows, with `notes` saying its caption is uncarried; not a frame a slide reads from; the statement goes to `unverified` with the clip as where it was seen |
| An image found by image search | Kept only for what the articles, the cited material and the subject's pages left unshown, credited to the page it was found on with that page's credit, and said at the checkpoint |
| An image without a readable credit, other than a share image credited to its outlet or a frame credited to its broadcaster or channel | Not in the set |
| An image under terms that forbid modification | Kept with `modification_allowed` false and flagged; the build uses it whole or not at all |
| An image smaller than the canvas | Kept with its size and the upscale factor noted; below 700 pixels on its short side, marked as usable only darkened under type or in a collage half |
| An article behind a paywall or a login | Not a source; another outlet is read |

## Hard rules

1. Sources are article bodies read in full. A search summary, a snippet or the agent's memory is never a source, because a draft built from summaries put an unsourced superlative and a foreign figure on a slide and the user caught it.
2. Every fact carries the sentence it rests on. A sentence that cannot be traced is not written.
3. The angle is a published interpretation, quoted with its outlet. The skill does not invent why a story matters.
4. The pick is the user's, made at the candidate checkpoint or given in the request; the skill never picks, and the checkpoint is shown whenever the request names no story.
5. Images show the story and carry a credit. They come from where the articles point, in order (their own photographs, the clip or footage or post they cite, the subject's own public pages), and from an image search only for what those leave unshown, said at the checkpoint and credited to where it was found; none is generated or taken from a stock library unless the user asks for that and says so in the credit; all are collected only after the pick. A brief whose photos showed nothing of the story sent the build to the broadcaster's clip the articles cited, and that is where the images were. Terms that forbid modification are recorded and respected downstream; the use of such material is the user's decision, said at the delivery.
6. Every image is judged legible at phone size before it is kept for a slide that has to be read. Slides built on frames that were blur alone were sent back with "this cannot be seen"; the brief says which images are clear, which are soft and which show nothing.
7. No paywall, no login, no bypass; what cannot be read in full is not used.
8. Nothing is spent and nothing is posted.

## Terminology

| Term | Meaning |
|---|---|
| Candidate | A story of the week that fits the account's categories and audience, with its angle and the articles that carry it, before the user picks. |
| Market | The country or region the post's readers are in; with the language, the audience. |
| Pick | The candidate the user chose, or a story they named instead. |
| Fact | One sentence the post may use, with the article sentence it rests on. |
| Source sentence | The sentence of the article, quoted, that a fact rests on. |
| Angle | The interpretation the post runs on, as published by an outlet and quoted. |
| Single-source | A fact found in one article only. |
| Unverified | What the post would want to say and no article confirmed. |
| Image entry | One downloaded image with where it came from, what it shows, its caption, credit, size, legibility, marks and licence terms. |
| Cited material | What the articles name as their source or their subject and is public: a broadcaster's clip of the report, footage, a post, a release's images. |
| Frame | One still of a clip, saved with its time code; its caption is the text printed on it. |
| Legible | An image whose subject, and any text on it, can be made out at about a third of the canvas width, as a phone shows it. |
| Beat | One step of the story's order, naming the facts it carries; the build's starting point. |
