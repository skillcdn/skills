---
name: html-cardnews-from-brief
description: Builds an Instagram card-news carousel (a magazine-style post of portrait slides) from a sourced topic brief in the format of a reference account, as HTML rendered to PNG by a headless browser. Writes one thread from the published angle at the format's measured density and register, with text on only the slides that need it; lays out each slide by what it says (story, serif note, list poster, time poster, stat, collage, lead) instead of repeating one sequence; places the brief's photos with their credits; previews the page, exports and reviews every slide, and delivers the PNGs, the caption and the credits with a pre-publish checklist. Use when a user says "make the card news and show it here", "build the finished post from this", "make this one the same way", or has a format spec and a brief and wants the slides. The brief comes from web-cardnews-topic-brief and the format from instagram-cardnews-format-study; with neither, this skill says what to run first.
license: MIT
compatibility: Needs a shell with Node.js and a Chromium-family browser that playwright-core can launch (an installed Chrome, Edge or Chromium, or playwright-core's own), a network for web fonts, and a way to show a local page to the user (the host's browser or preview pane) or to attach images. Works in any agent that can run a shell and attach files.
metadata:
  author: skillcdn
  version: "1.0"
  tools: html
skillcdn:
  include:
    - references/script.md
    - references/layouts.md
    - references/page-and-export.md
    - references/tool-notes.md
    - assets/slide-plan.example.json
    - /marketing/docs/cardnews/format-spec.md
    - /marketing/docs/cardnews/topic-brief.md
  translations:
    ko:
      title: 브리프로 만드는 카드뉴스 (HTML 조판, PNG 내보내기)
      description: 출처가 붙은 소재 브리프를 레퍼런스 계정의 포맷으로 인스타그램 카드뉴스(1080×1350 캐러셀)로 만듭니다. HTML과 CSS로 조판하고 헤드리스 브라우저로 PNG를 뽑습니다. 보도된 각도 하나로 한 줄기의 스크립트를 쓰되 글이 필요한 장에만 글을 넣고, 포맷에서 잰 밀도와 어투를 지키며, 슬라이드마다 레이아웃을 내용에 따라 고릅니다(이야기 슬라이드, 사진에 세리프 한 마디, 번호 리스트 포스터, 날짜·시간 포스터, 숫자 슬라이드, 콜라주, 리드 슬라이드). 브리프의 사진을 출처와 함께 넣고, 호스트의 프리뷰에 띄우고, 장마다 내보낸 뒤 PNG를 하나씩 검토해(줄바꿈, 워터마크, 안 읽히는 글자) PNG·캡션·크레딧과 게시 전 체크리스트로 냅니다. "카드뉴스 만들어서 여기 띄워줘", "이걸로 완성본 만들어", "이것도 똑같은 방식으로 만들어"라고 할 때, 포맷 스펙과 브리프가 있어 슬라이드만 필요할 때 쓰세요. 브리프는 web-cardnews-topic-brief가, 포맷은 instagram-cardnews-format-study가 만듭니다. 둘 다 없으면 무엇을 먼저 돌릴지 말합니다.
---
# Card news from a brief, in a reference format, rendered from code

A format spec and a topic brief go in; a carousel of PNG slides comes out, with its caption and its credits. The script is one thread from the brief's published angle, written at the format's counted density and in its register; each slide's layout is chosen by what it says, so a list is a list, a time is a time and a mood is a photo with a line, and no two posts of the account repeat the same sequence; every photo is the brief's, placed and cropped around its marks, credited in the caption. The page is HTML the agent can show and re-export in a minute, and every PNG is looked at before it is delivered. Nothing on a slide comes from anywhere but the brief; nothing is posted.

## How the user is involved

- **Questions:** only where the inputs are: the spec folder and the brief folder, when the request does not point at them and they are not beside the run. Nothing else is asked; the slide count, the fonts and the layouts are derived and shown.
- **Checkpoints:** the slide plan (the thesis, the thread, each slide's layout, text and image), and the render review (every PNG attached, with what the review changed). Each is one short message; "OK" continues.
- **Go-ahead:** when the user says to go ahead alone, both checkpoints are skipped; the delivery still attaches every PNG.
- **Changes mid-run:** "too much text", "the tone is off", "the layouts all look the same" re-enter at the plan and apply to every slide, not the one named; a photo swap re-enters at the build.

## Requirements

| What | Used for |
|---|---|
| A shell with Node.js | The static server, the export script, image sizes. |
| A Chromium-family browser playwright-core can launch | Rendering each slide at its native size to PNG ([page-and-export.md](references/page-and-export.md) "Export"). `playwright-core` from a local install, borrowed from a neighbouring project or installed into the scratch folder; it finds an installed Chrome or Edge by channel, else its own Chromium. |
| A way to show the page: the host's browser or preview pane pointed at a local server, or the PNGs attached to a message | The review checkpoint. A page opened as a file shows a static snapshot without its images in some hosts; serve it (page-and-export.md "Preview"). |
| A network | Web fonts from a CDN, the spec's or the closest free ones. |

Check Node.js and the network before the first message; without Node.js, stop and say what to install. The browser is checked where it is launched, in phase 4: a launch that finds no browser stops there with the install line of the export script, and nothing before it depends on the browser. What the card-news skills share is in the area's document set [`marketing/docs/cardnews/`](/marketing/docs/cardnews/README.md); the two pages this skill reads from it, [format-spec.md](/marketing/docs/cardnews/format-spec.md) and [topic-brief.md](/marketing/docs/cardnews/topic-brief.md), are included and arrive with this skill wherever SkillCDN serves it. A copy of this directory lacks them: say so, fetch them from `marketing/docs/cardnews/` of the repository this skill comes from (for this collection, `github.com/skillcdn/skills`), and otherwise read the spec and the brief as the files are. How the tools behaved in runs of this skill is in [tool-notes.md](references/tool-notes.md); read it before phase 1.

The area's rule that claims and assets come from the brand takes this form here: the user is the brand, the brief is what they supply, and its facts and photographs are the articles' and the agencies', used as the account itself publishes news, with their credits. The canvas and the caption's form come from the spec, which measured them on the account and looked up the platform's documented size; with no spec, the platform's documented portrait size is looked up at run time.

## Inputs

| Input | Source |
|---|---|
| Format spec | `format-spec.json` and `style-notes.md` from a study of the account (in this collection, `instagram-cardnews-format-study`). Named in the request, or found beside the run. The JSON is what the build reads; the notes qualify it (the register's wrong-sounding counterparts, what was tentative) and the JSON wins where they differ. With none: build on the defaults in [layouts.md](references/layouts.md), say so in the first message and at the plan checkpoint, and offer the study at the delivery. |
| Topic brief | `topic-brief.json` and `img/` from a research of the story (in this collection, `web-cardnews-topic-brief`), with `credits.md` where the research wrote one; without it, the credit line is built from `images[].credit`. With none: say that the slides are written only from a brief and offer to run the research on the user's topic. A topic and a handful of links are not a brief. |
| Slide count | Derived: the spec's typical count; fewer when the brief carries fewer beats. |
| Fonts and colors | Derived: the spec's `fonts` and `colors`, loaded from their CDN; the defaults in layouts.md "Defaults" when the spec has none. |
| Where the post goes | Derived: the folder the user names, else `post/` inside the brief folder, with the page, `img/` copied from the brief, and `out/` for the PNGs; the previous posts of the same account are the other brief folders beside it, each with its own `post/slide-plan.json`. Said in the first message. |

## Workflow

Each phase produces a named artifact in the post folder.

### Phase 1: Plan

Produces the **slide plan** (`slide-plan.json` and `caption.txt`, by [script.md](references/script.md) and [layouts.md](references/layouts.md); shape in [slide-plan.example.json](assets/slide-plan.example.json)) and the first checkpoint.

1. The thesis: the brief's `angle` as one sentence, or its `headline` when the story has no angle; the headline from it in the spec's headline style.
2. The thread: the brief's `beats` as the starting order, reshaped by script.md "The thread", one beat per slide, with text on only the slides that need it; a photo-only slide is a beat too.
3. Each slide's layout by script.md and layouts.md "Choosing a layout": what the beat carries (a fact in sentences, a list, a date and a time, numbers, a quote or a mood, two related images) decides the type; the spec's `variants_by_content` wins where it says. The catalogue's names are the classes; the spec's `poster` is one of list, time or stat by what the beat carries, and the spec's anatomy overrides the defaults of that class. Read the `post/slide-plan.json` of the brief folders beside this one and keep this plan's sequence of types different from each of theirs in at least two slides.
4. The text of every text slide by script.md "Density" and "Register": the sub, the sentences, each naming the fact ids it rests on; the note lines, each naming the image caption or the quoted source sentence it comes from; the poster's parts. A sentence that no fact carries is not written: the beat is dropped or kept as a photo, said at the checkpoint with the offer to extend the brief with the research skill; the skill does not add the fact itself.
5. The image per slide by role from the brief's entries: a cover that reads at portrait, a subject under a story or a lead, a mood under a note, a dim photo under a poster or a stat; two images of one beat as a collage, stacked when both are landscape and side by side when both are portrait; the crop that avoids each image's marks. An image whose licence forbids modification is used whole, letterboxed on the spec's dark color on a note slide with the note clear of it, or not at all; one whose terms are unknown is used as the account uses news photographs, cropped and dimmed as the layout needs, with its credit.
6. The caption by script.md "The caption", in the spec's caption parts and register, with the credit line from `credits.md` (or built from `images[].credit`) in the spec's pattern, and mentions only from a fact that carries a handle with its source.

Checkpoint, in plain words: the thesis and the headline; the slides in a numbered list, each with its layout type, its text or "photo only", its image and its fact ids; the caption; what was derived (count, fonts, defaults used); any beat dropped for lack of a fact. "OK" builds.

### Phase 2: Build the page

Produces the **page** (`index.html` with `img/`), by [page-and-export.md](references/page-and-export.md) "The page": one file with the slides as native-size boxes scaled into a grid, a lightbox, an export mode that renders one slide at its native size, the caption and the credits below; the CSS tokens from the spec; one class per layout type of the catalogue; each image placed with its crop; gradients and overlays as the layout says. Copy the two scripts into the post folder with it.

### Phase 3: Preview

Produces the **preview**: the page served by the static server ([server.example.mjs](scripts/server.example.mjs)) from the post folder and shown in the host's browser or preview pane, with the host's launch configuration where it has one (page-and-export.md "Preview"). Say in a line where it is and go on.

### Phase 4: Export

Produces the **PNGs** in `out/`, one per slide at the canvas size, by the export script ([export.example.mjs](scripts/export.example.mjs)) run from the post folder with its environment set (page-and-export.md "Export"): the page in export mode per slide, fonts awaited, the viewport clipped. A launch that finds no browser stops here with what to install.

### Phase 5: Review

Produces the **review notes** (`review.md`, one line per slide per pass) and the second checkpoint. Open every PNG at its native size (the host's image reader at full resolution, or the browser pane at 100%) and judge it by the verdicts below; fix in the page and export again, all slides, until nothing fails. Attach every PNG to the checkpoint message with one line each on what changed. A correction from the user is applied to every slide it concerns and the review runs again.

### Phase 6: Deliver

One message: the post folder with `out/`, `index.html`, `slide-plan.json`, `caption.txt`, `credits.md` and `review.md`; the PNGs attached; the caption as text; the credits as text; what was derived; what the review changed; and the pre-publish checklist: the brief's unverified items, the images that upscaled and by how much (the larger of canvas width over image width and canvas height over image height, times any crop scale), any image under a licence that forbids modification and how it was used, and that the images are the outlets' and agencies' material, used with credit at the user's discretion. Publishing is the user's act.

## Verdicts

Read before every export. The review page's table ([page-and-export.md](references/page-and-export.md) "The review") is this list in the order a reviewer meets it.

| Result | Verdict |
|---|---|
| A body sentence wraps to a second line | Redo: shorten the sentence to the spec's characters per sentence; never a smaller type |
| A sub wraps, or a headline line exceeds the spec's characters per line | Redo: rephrase |
| More sentences on a slide than the spec's range | Redo: the surplus goes to the caption or to another beat |
| Two consecutive slides of one layout type other than the story type, or three story slides in a row in a post that carries a list, a time or numbers | Redo: the beat that is a list, a time or a number takes its own layout |
| The same sequence of layout types as a previous post of the account built by this skill | Redo: at least two slides change type |
| An agency mark, a logo or a credit mark visible on a slide | Redo: crop around it with the image's position or a scaled crop; where the licence forbids modification, another image of the same role, and where the brief has none, the image whole with the mark in view and said so |
| A source tag or a note over a bright or busy region, or colliding with text inside the photo | Redo: a top gradient under the note, or the tag moved to the other corner |
| A subject lost in the portrait crop | Redo: shift the object position, or swap for a vertical image of the same role |
| A poster's figures or list rows touching the margins | Redo: fewer rows on the slide, or the figures reduced by about a tenth, within the spec |
| A serif note of more than the spec's lines | Redo: cut to the range |
| An image upscaled more than two times at the canvas | Accept with a note in the checklist; swap for a larger image of the same role when the brief has one |
| A sentence that names no fact id, or a note line that names no caption or source sentence | Redo: traced or removed |
| An image used that is not in the brief | Redo: removed; the brief is the only source of images |

## Hard rules

1. The slides say only what the brief carries. Every sentence names its fact ids, every note line its caption or source sentence; the thesis is the brief's published angle. A fact the post needs goes back to the research, never onto a slide from memory: a deck built without this put two invented claims on slides, and the user caught them.
2. Density is the spec's counts: the sub's characters, the sentences per slide, the characters per sentence. A draft that put five facts and a paragraph on each slide read as an explainer; the detail goes to the caption.
3. One thesis, one thread, and text on only the slides that need it. A deck that distributes facts across slides without a line through them reads as nothing.
4. The register is the spec's patterns, checked sentence by sentence by script.md "Register": a news-title headline, noun-phrase subs, the slides' own voice with sentence-final noun phrases mixed in, no explanatory closers. The user's word for what this prevents is "sounds like AI".
5. A slide's layout follows what it says, by the catalogue and the spec's variants, and no two posts repeat a sequence. A deck that reused the previous deck's sequence slide for slide was sent back.
6. Images are the brief's, each credited in the caption; none is generated, found or stocked here. An image whose licence forbids modification is used whole or not at all.
7. Every PNG is looked at before it is delivered, at its native size, against the verdicts.
8. Nothing is posted and nothing is spent.

## Terminology

| Term | Meaning |
|---|---|
| Thesis | The one sentence the post says, taken from the brief's angle. |
| Thread | The order of beats that carries the thesis from the first slide to the last. |
| Beat | What one slide does in the thread; a photo-only slide is a beat. |
| Layout type | One of the catalogue's arrangements (cover, story, note, lead, list poster, time poster, stat, collage), chosen by content. |
| Density | The spec's counts of text per slide type. |
| Register | The spec's writing patterns, applied sentence by sentence. |
| Export mode | The page rendered one slide at native size, by a query parameter, for the headless browser. |
| Review | The pass over every PNG against the verdicts, before the checkpoint and before the delivery. |
| Pre-publish checklist | The unverified items, the upscales and the licence flags, repeated at the delivery for the user. |
