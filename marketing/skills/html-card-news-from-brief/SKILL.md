---
name: html-card-news-from-brief
description: Builds an Instagram card news carousel (the slides of a post) from a sourced topic brief in a reference account's format, as HTML rendered to PNG. Use when a user says "make the card news and show it here", "build the finished post from this", "make this one the same way", or has a format spec and a brief and wants the slides. The brief comes from web-card-news-topic-brief and the format from instagram-card-news-format-study; with no spec, this skill says to run the study first. Every slide is one of the account's own slide types as the format spec measured them (anatomy, photo treatment, which text is the account's and which the material's), chosen by what it carries and sequenced as the account's build runs; the skill has no layouts of its own. Writes one thread from the published angle at the format's density and register, places the brief's images with their credits, previews, exports and reviews every slide at phone size, and delivers the PNGs, the caption and the credits with a pre-publish checklist.
license: MIT
compatibility: Needs a shell with Node.js and a Chromium-family browser that playwright-core can launch (an installed Chrome, Edge or Chromium, or playwright-core's own), a network for web fonts, and a way to show a local page to the user (the host's browser or preview pane) or to attach images. Works in any agent that can run a shell and attach files.
metadata:
  author: skillcdn
  version: "1.6"
  tools: browser
skillcdn:
  include:
    - references/script.md
    - references/layouts.md
    - references/tool-notes.md
    - assets/slide-plan.example.json
    - /marketing/docs/card-news/format-spec.md
    - /marketing/docs/card-news/topic-brief.md
    - /docs/browser/rendering-html.md
  translations:
    ko:
      title: 브리프로 만드는 카드뉴스 (HTML 조판, PNG 내보내기)
      description: 출처가 붙은 소재 브리프를 레퍼런스 계정의 포맷으로 인스타그램 카드뉴스로 만듭니다. HTML과 CSS로 조판하고 헤드리스 브라우저로 PNG를 뽑습니다. 모든 슬라이드는 포맷 스펙이 그 계정에서 잰 슬라이드 유형 중 하나로만 만듭니다(구조, 사진 처리, 어느 글이 계정의 것이고 어느 글이 자료의 것인지). 장마다 담는 내용으로 유형을 고르고 계정의 구성 순서를 따르며, 이 스킬 자체의 레이아웃은 없습니다. 보도된 각도 하나로 한 줄기의 스크립트를 포맷의 밀도와 어투로 쓰고, 브리프의 이미지를 출처와 함께 넣고, 호스트의 프리뷰에 띄우고, 장마다 내보낸 뒤 PNG를 휴대폰 크기로 하나씩 검토해(줄바꿈, 안 보이는 화면, 스펙과 다른 위치) PNG·캡션·크레딧과 게시 전 체크리스트로 냅니다. "카드뉴스 만들어서 여기 띄워줘", "이걸로 완성본 만들어", "이것도 똑같은 방식으로 만들어"라고 할 때 쓰세요. 브리프는 web-card-news-topic-brief가, 포맷은 instagram-card-news-format-study가 만듭니다. 스펙이 없으면 분석을 먼저 돌리라고 말합니다.
---
# Card news from a brief, in a reference format, rendered from code

A format spec and a topic brief go in; a carousel of PNG slides comes out, with its caption and its credits. Every slide is one of the reference account's own slide types, as the spec measured them on the account: its anatomy, how it treats its photo (cropped full-bleed, or a captured frame kept whole with its marks), which text is the account's own and which belongs to the material it shows. The type is chosen by what the slide carries and the sequence is the account's build; this skill has no layouts of its own, because the user holds the result against the account's posts and a type the account does not use is the first thing they see. The script is one thread from the brief's published angle, written at the format's counted density and in its register, on only the slides whose type carries text of the account's. Every image is the brief's, placed as its type treats it and credited in the caption. The page is HTML the agent can show and re-export in a minute, and every PNG is looked at at phone size before it is delivered. Nothing on a slide comes from anywhere but the brief; nothing is posted.

## How the user is involved

- **Questions:** only where the inputs are: the spec folder and the brief folder, when the request does not point at them and they are not beside the run. Nothing else is asked; the build, the slide count, the fonts and each slide's type are derived from the spec and shown.
- **Checkpoints:** the slide plan (the thesis, the thread, each slide's type from the spec, its text and its image), and the render review (every PNG attached, with what the review changed). Each is one short message; "OK" continues.
- **Go-ahead:** when the user says to go ahead alone, both checkpoints are skipped; the delivery still attaches every PNG.
- **Changes mid-run:** "too much text", "the tone is off", "this is not the account's format" re-enter at the plan and apply to every slide, not the one named: the last one means the spec was not followed, so the plan is held against the spec's types and build again, slide by slide, before anything is rendered. "This cannot be seen" re-enters at the plan's image step for every slide. A photo swap re-enters at the build.

## Requirements

| What | Used for |
|---|---|
| A shell with Node.js | The static server, the export script, the review script, image sizes. |
| A Chromium-family browser playwright-core can launch | Rendering each slide at its native size to PNG ([page-and-export.md](references/page-and-export.md) "Export"). `playwright-core` borrowed from a neighbouring project through `PLAYWRIGHT_FROM`, else installed once into the tools folder `card-news/tools/` beside the brief folders and never into `post/`, which is handed over; the browser found by channel; a browser download asked first, as [headless.md](/docs/browser/headless.md) says. |
| A way to show the page: the host's browser or preview pane pointed at a local server, or the PNGs attached to a message | The review checkpoint. A page opened as a file shows a static snapshot without its images in some hosts; serve it ([rendering-html.md](/docs/browser/rendering-html.md) "Serving the page"). |
| A network | Web fonts from a CDN, the spec's or the closest free ones it names. |

Check Node.js, the network (one request to the font path the spec names) and a Chromium-family browser (an installed Chrome or Edge, or playwright-core's own Chromium, proved by a launch and not by a look at the disk) before the first message, as [headless.md](/docs/browser/headless.md) "The check before the first message" says; without Node.js or a browser, stop and say what to install. `playwright-core` itself is borrowed or installed where phase 4 launches it, and a launch that still fails stops there with the install line. [page-and-export.md](references/page-and-export.md), the page and the review, is read when phase 2 comes. What the card-news skills share is in the area's document set [`marketing/docs/card-news/`](/marketing/docs/card-news/README.md); the two pages this skill reads from it, [format-spec.md](/marketing/docs/card-news/format-spec.md) and [topic-brief.md](/marketing/docs/card-news/topic-brief.md), are included and arrive with this skill wherever SkillCDN serves it, and so is [rendering-html.md](/docs/browser/rendering-html.md) from the repository's document set [`docs/browser/`](/docs/browser/README.md), which holds how any page the agent writes is served, exported and looked at; its headless.md is linked from the export. A copy of this directory lacks the included pages, and a mount of one area or one skill cannot read the linked one: say so, fetch them from `marketing/docs/card-news/` and `docs/browser/` of the repository this skill comes from (for this pack, `github.com/skillcdn/skills`), and otherwise read the spec and the brief as the files are. How the tools behaved in runs of this skill is in [tool-notes.md](references/tool-notes.md); read it before phase 1.

The area's rule that claims and assets come from the brand takes this form here: the user is the brand, the brief is what they supply, its facts are the articles' and its images come from where the articles point (their photographs, the clip or footage they cite, the subject's public pages), each with the credit the brief records, used as the account itself publishes such material. The canvas, the slide types and the caption's form come from the spec, which measured them on the account and looked up the platform's documented size.

## Inputs

| Input | Source |
|---|---|
| Format spec | `format-spec.json` and `style-notes.md` from a study of the account (in this pack, `instagram-card-news-format-study`), with the study's `slide-log.md` where it is beside them. Named in the request, or found beside the run. The JSON is what the build reads; the notes qualify it (the register's wrong-sounding counterparts, what was tentative), the log answers a measurement the JSON lacks, and the JSON wins where they differ. With none: the slides cannot be built in an account's format; say so, offer the study, and build only on the user's word, on the stand-in in [no-spec.md](references/no-spec.md), said to be one at every checkpoint. |
| Topic brief | `topic-brief.json` and `img/` from a research of the story (in this pack, `web-card-news-topic-brief`), with `credits.md` where the research wrote one; without it, the credit line is built from `images[].credit`. With none: say that the slides are written only from a brief and offer to run the research on the user's topic. A topic and a handful of links are not a brief. |
| Build | Derived, in this order: the kind of post the story is, read from the brief (a date to come or an event is an event post, a list of places or things a list, a story whose images are captioned frames of a broadcast a report, a person or an issue a story), said at the plan checkpoint; among that kind's builds, the one whose `text_on` matches what the brief's images carry (captioned frames of a clip carry the story themselves and take the build told by the material's captions; photographs with nothing written on them take a build of the account's sentences); where two still fit, the one whose slide range holds the brief's beats. Said at the plan checkpoint with the spec's `typical_order` for it. |
| Slide count | Derived: the spec's `canvas.slides_per_post.typical` where it lies in the build's `slides` range, else the middle of that range; fewer when the brief carries fewer beats, or fewer legible images than the build's slides need (a type that stacks two frames takes two; a frame left over goes on a one-frame type the spec has, else into the caption's sources); below the build's range, the plan goes to the checkpoint with the count it has and proposes extending the brief. |
| Series label | Only where the spec's cover carries a label: the user's own label when the request names one, else a word for the post's category in the label's measured style, said at the plan checkpoint. The reference account's label is its name and is never used. A cover the spec shows without a label gets none. |
| Fonts and colors | Derived: the spec's `fonts` and `colors`, loaded from the paths the spec names (a CDN stylesheet, or an `@font-face` for a file the spec points at); a family the spec names with no path is loaded from its distributor's documented CDN path, found by searching the family's name with "CDN", said at the checkpoint. |
| Where the post goes | Derived: the folder the user names, else `post/` inside the brief folder, with the page, `img/` copied from the brief, and `out/` for the PNGs; the previous posts of the same account are the other brief folders beside it whose `post/slide-plan.json` names the same spec in `spec`, written as the spec file's path relative to the plan file (`../../<handle>/format-spec.json`), so that two plans beside each other name it alike. Said in the first message. |

## Workflow

Each phase produces a named artifact in the post folder.

### Phase 1: Plan

Produces the **slide plan** (`slide-plan.json`, `caption.txt` and `credits.md`, by [script.md](references/script.md) and [layouts.md](references/layouts.md); shape in [slide-plan.example.json](assets/slide-plan.example.json)) and the first checkpoint.

1. The build and the thesis: the build in the spec's `kinds` that fits the post, its `typical_order` as the starting sequence; the thesis is the brief's `angle` as one sentence, or, when the story has no angle, the brief's `headline`, which the research wrote from the leading fact, and the post is then a report; the headline from it in the spec's cover headline style.
2. The thread: the brief's `beats` as the starting order, reshaped by script.md "The thread", one beat per slide, in the build's count; a beat the account's build carries as material alone (a captured frame whose own caption states it, a photo with nothing to add) is a beat too, with no text of the account's. Beats that outnumber the slides are merged where one slide's material or sentences state two, and the rest go to the caption, said at the checkpoint; a slide of a type that holds two frames carries the beats its two captions state.
3. Each slide's type by layouts.md "Choosing a type for a beat": the spec's `cover` for the first slide, in the variant whose `for` names the post's kind or build, else the plain cover; for every other slide, the one of the spec's `slide_types` whose `carries` names what the beat is, `variants_by_content` deciding where the account uses a particular type or element for that content, and the spec's `elements` riding on the slide where the spec places them. The spec's types are the only layouts: a beat the spec has no type for takes the nearest type the account has for content of that shape, said at the checkpoint, and never a type the account does not use. The spec's `never` limits every slide (a call to action on a story post, a number as an overlay); a type the spec maps to a content wins over a `never` for that content only. The sequence is the account's: where the spec's build repeats one type slide after slide, the plan repeats it; where the build's `order` varies between posts, read the `post/slide-plan.json` of the brief folders beside this one and differ from each in at least two slots, within the build's set of types and its count (layouts.md "Variation").
4. The text of every slide whose type carries text of the account's, by script.md "Density" and "Register": the sub, the sentences, each naming the fact ids it rests on; an element's lines, each naming the image caption or the quoted source sentence it comes from. An element's lines are text of the account's, and an element rides only on the types the spec's `rides_on` names. A sentence that no fact carries is not written: the beat is dropped or kept as material, and the plan goes on to the checkpoint, where the offer to extend the brief with the research skill is made; the run does not stop before it, and the skill does not add the fact itself. A type that carries no text of the account's gets none, whatever the beat; the material's own text (a frame's caption) is recorded in the plan as what the slide says, with the fact ids it states, and a frame whose caption states no fact of the brief goes on no slide that reads from it.
5. The image per slide from the brief's entries, treated as the spec's type treats its photo (layouts.md "Photo treatment"): cropped full-bleed around its marks where the type crops, with the entry's `watermark` and `notes` read before the crop is chosen; whole with its marks and the spec's margins where the type keeps frames whole; two images stacked or side by side where the type has two, and exactly that many. Match each image to its slide by the entry's `shows` and `caption`: a slide about a person carries that person, a slide whose beat is a frame's caption carries that frame. A slide that has to be read is one whose beat the reader takes from the image (a frame whose caption is the beat, a photo whose subject is the beat): it takes only an image the brief marks `clear`; a slide whose text of the account's carries the beat may take a `soft` one, said so at the checkpoint; an `unreadable` one is not placed. An image of other people, another production or another year goes on a slide only with a line that says what it shows, where the type allows one. Where the brief has no legible image of what the beat names, the beat moves to the caption and the checkpoint proposes extending the brief; the plan goes on without it until the user says. An image whose licence forbids modification is used whole or not at all; one whose terms are unknown is treated as the type treats its photos, with its credit, and the delivery says so.
6. The caption by script.md "The caption", in the spec's caption parts and register, with the credit line in the spec's pattern and mentions only from a fact that carries a handle with its source; and `credits.md` in the post folder, one line per image placed on a slide, rewritten from the brief's `credits.md` (or built from `images[].credit`) in the spec's pattern, which the caption's credit line merges.

Checkpoint, in plain words: the build and the thesis with the headline; the slides in a numbered list, each with its type from the spec, its own text or "material only" with the material's caption, its image with its treatment and legibility, and its fact ids; the caption; what was derived (the build, the count, the fonts, any nearest-type substitution); any beat dropped or moved for lack of a fact or of a legible image. "OK" builds.

### Phase 2: Build the page

Produces the **page** (`index.html` with `img/`), by [page-and-export.md](references/page-and-export.md) "The page": one file with the slides as native-size boxes scaled into a grid, a lightbox, an export mode that renders one slide at its native size, the caption and the credits below; the CSS tokens from the spec; one class per slide type and element of the spec, with the anatomy the spec measured (layouts.md "From the spec to classes"); each image placed as its type treats it; gradients and overlays as the type has them; the markup the review script reads (page-and-export.md "The page"). Copy into `img/` only the images the plan uses, and the three scripts into the post folder.

### Phase 3: Preview

Produces the **preview**: the page served by the static server ([server.example.mjs](scripts/server.example.mjs)) from the post folder and shown in the host's browser or preview pane, with the host's launch configuration where it has one (page-and-export.md "Preview"). Say in a line where it is and go on.

### Phase 4: Export

Produces the **PNGs** in `out/`, one per slide at the canvas size, by the export script ([export.example.mjs](scripts/export.example.mjs)) run from the post folder with its environment set (page-and-export.md "Export"): the page in export mode per slide, fonts awaited, the viewport clipped. A launch that finds no browser stops here with what to install.

### Phase 5: Review

Produces the **review notes** (`review.md`, one line per slide per pass) and the second checkpoint. Run the review script ([review.example.mjs](scripts/review.example.mjs)) from the post folder: it counts the lines the browser set against the plan, measures every placed block's top and bottom edges against the spec's, and writes a phone-size copy of every PNG into `out/phone/` (page-and-export.md "The review"); then open every PNG at its native size (the host's image reader at full resolution, or the browser pane at 100%) and its phone-size copy, which is how a phone shows it, and judge it by the verdicts below; fix in the page and export again, all slides, until nothing fails. A color the spec marks as an estimate may be adjusted where the render shows text unreadable, and the checkpoint says by how much. Attach every PNG to the checkpoint message with one line each on what changed; where the host gives no way to attach files, give the `out/` path and the preview instead.

### Phase 6: Deliver

One message: the post folder with `out/`, `index.html`, `slide-plan.json`, `caption.txt`, `credits.md` and `review.md`; the PNGs attached; the caption as text; the credits as text; what was derived; what the review changed; and the pre-publish checklist: the brief's unverified items, the single-source facts the slides use, the images that upscaled and by how much (the larger of the placed box's width over the image's `px` width and its height over its `px` height, `px` being the size the brief recorded, which for a frame is the served resolution and never the capture file's size; the box is the canvas for a full-bleed crop and the frame's box for a frame kept whole, times any crop scale), any image under terms that forbid reproduction without authorization, forbid modification or allow only non-commercial use, how it was used and that it needs the rights holder's permission before publishing, any image whose terms are unknown and how it was used, the rights in the subjects of the photos (a character, an artwork) where the brief names them, and that the images are the outlets', agencies', broadcasters' and subjects' material, used with credit at the user's discretion. Publishing is the user's act.

## Verdicts

Read before every export. The review page's table ([page-and-export.md](references/page-and-export.md) "The review") is this list in the order a reviewer meets it.

| Result | Verdict |
|---|---|
| A slide of a type the spec does not have, or a type's anatomy changed beyond the spec's estimates (a text block added to a type that carries none, a frame cropped where the account keeps it whole, a gradient the type lacks) | Redo: the spec's type as measured. Two changes are said at the checkpoint and stand: a nearest-type substitution, with a block left empty where the beat has no text of the account's, and an image whose licence forbids modification placed whole where the type would crop it |
| A slide that does what the spec's `never` states for its kind of post | Redo: the sentence or the element removed, unless the spec maps a type to that content |
| A sequence the account's build does not show: where the build's `order` is `fixed`, any order other than its `typical_order`; where it `varies`, a type outside the build's set, or a stack of frames broken up | Redo: the sequence of the spec's build |
| The same sequence as a previous post of the account built by this skill, where the build's `order` varies between the account's own posts | Redo: at least two slots change type; slots are compared by position, and a slide past the shorter plan's count is a difference |
| An image that cannot be made out at phone size: a frame that is mosaic or blur alone, a scene too dark to show its subject, motion blur, a picture inside a frame upscaled past about two times | Redo: another legible image of the beat from the brief; where the brief has none, the beat moves to the caption or the brief is extended, said so |
| A line the renderer broke on its own (a wrap the plan did not place) | Redo: shorten, or place the break by hand at a clause end within the spec's characters per line; never a smaller type |
| A sub wraps, or a headline line exceeds the spec's characters per line | Redo: rephrase |
| More lines or sentences on a slide than the spec's range for its type or element | Redo: the surplus goes to the caption or to another beat |
| A note or an element shorter than the spec's range because its source holds no more | Accept: never padded beyond its source |
| A mark the account crops away (an agency mark, a logo, a credit mark on a full-bleed photo) visible on a slide | Redo: crop around it with the image's position or a scaled crop; where the licence forbids modification, another image of the same role, and where the brief has none, the image whole with the mark in view and said so. A mark the account keeps (a broadcaster's logo and labels on a frame kept whole) stays, as the spec's type has it |
| Text of the account's over the material's own text, or a tag or a note over a bright or busy region | Redo: the block moved where the type allows, or a gradient where the type has one |
| A subject lost in a crop | Redo: shift the object position, or swap for an image of the same role that keeps it |
| An image that shows other people, another production or another year than its slide's text names | Redo: an image of what the text names from the brief; where the brief has none, a line on the slide that says what the image shows where the type allows one, else the beat without the image |
| A text block or an image whose top or bottom edge, as the review script measures it, is off the spec's anatomy by more than about a twentieth of the canvas, or an empty band the reference's slide type does not have | Redo: place the block by the spec's edges; where the spec records no vertical edges, read them from the account's slide in the study's log, else set the block where the type leaves room for it, centered in that space |
| Type touching the margins the spec's type keeps | Redo: fewer lines or rows; on a type whose block is a number or a date set large (a poster, a stat), that figure's size reduced by about a tenth within the spec's estimate; body type never shrinks |
| An image upscaled more than two times at the canvas | Accept with a note in the checklist when it still reads; swap for a larger image of the same role when the brief has one |
| A sentence that names no fact id, or an element's line that names no caption or source sentence | Redo: traced or removed |
| An image used that is not in the brief | Redo: removed; the brief is the only source of images |

## Hard rules

1. The slides say only what the brief carries. Every sentence names its fact ids, every note line its caption or source sentence; the thesis is the brief's published angle. A fact the post needs goes back to the research, never onto a slide from memory: a deck built without this put two invented claims on slides, and the user caught them.
2. Density is the spec's counts: the sub's characters, the lines and sentences per slide, the characters per line. A draft that put five facts and a paragraph on each slide read as an explainer; the detail goes to the caption.
3. One thesis, one thread, and text of the account's on only the slides whose type carries it. A deck that distributes facts across slides without a line through them reads as nothing; a deck that wrote over material the account shows as it is was not the format.
4. The register is the spec's patterns, checked sentence by sentence by script.md "Register": the headline style, the sub style, the slides' own voice and endings, no explanatory closers. The user's word for what this prevents is "sounds like AI".
5. Every slide is one of the spec's own slide types at its measured anatomy, in the sequence of the spec's build; this skill has no layouts of its own and adds none. A deck composed from a catalogue of the skill's own, with the spec only adjusting it, was sent back twice as "not the format", and a deck that reused the previous deck's order where the account varies was sent back too.
6. Images are the brief's, each credited in the caption; none is generated, found or stocked here. They are the outlets', agencies', broadcasters' and subjects' material, used with credit at the user's discretion, and the delivery says so and names the images that need the rights holder's permission before publishing. An image whose licence forbids modification is used whole or not at all. An image that cannot be made out at phone size does not go on a slide that has to be read: a deck delivered on blurred frames was sent back with "this cannot be seen".
7. Every PNG is looked at before it is delivered, at its native size and at phone size, against the verdicts.
8. Nothing is posted and nothing is spent.

## Terminology

| Term | Meaning |
|---|---|
| Thesis | The one sentence the post says: the brief's angle, or its headline when the story has no angle. |
| Thread | The order of beats that carries the thesis from the first slide to the last. |
| Beat | What one slide does in the thread; a photo-only slide is a beat. |
| Slide type | One of the spec's `cover` or `slide_types`, its anatomy measured on the account; the only layouts a post is composed from, chosen by what each slide carries. |
| Material | What a slide shows that is not the account's own: a photograph, a captured frame with its own captions and marks. A type may carry material alone, with no text of the account's. |
| Legible | An image whose subject, and any text on it, can be made out at about a third of the canvas width, as a phone shows it. |
| A slide that has to be read | A slide whose beat the reader takes from the image: a frame whose caption is the beat, a photo whose subject is the beat. It takes only a clear image. |
| Density | The spec's counts of text per slide type. |
| Register | The spec's writing patterns, applied sentence by sentence. |
| Export mode | The page rendered one slide at native size, by a query parameter, for the headless browser. |
| Review | The pass over every PNG against the verdicts, before the checkpoint and before the delivery. |
| Pre-publish checklist | The unverified items, the upscales and the licence flags, repeated at the delivery for the user. |
