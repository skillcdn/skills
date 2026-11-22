---
name: html-design-variations
description: Shows four looks for one design (a page's first screen, a deck's cover, a card news format) as HTML rendered in a browser and tiled on one contact sheet, from a reference, a concept or the thing as it is. Use when a user says "show me four looks for this", "give me design directions for this page", "variations of this cover", "how else could this deck look", "like this account's card news but different", "a card news format of our own", or wants looks before a page, a deck or a post is built. Reads the reference's aesthetics for what the look must say, places candidates on the design axes a still can show (palette, type, composition, imagery, shape), near or far as the request asks, renders each, judges each for the AI feel (icon card grids, gradients, mockups, kickers) before anything is shown, compares them with a recommendation and a runner-up, and hands the pick to the skill that produces (for card news, as a format spec). The concept behind a look is web-concept-variations. Nothing is spent.
license: MIT
compatibility: Needs a shell with Python or Node.js and a Chromium-family browser a headless driver can launch, or a browser the agent drives that can screenshot a local page; a way to look at an image (the host's image reader or a browser pane); a file tool. Without a browser or a way to look at a screen the skill stops before the first message and says what to add.
metadata:
  author: skillcdn
  version: "1.9"
  tools: browser
skillcdn:
  include:
    - /docs/variation/effect-brief.md
    - /docs/variation/axes.md
    - /docs/variation/not-ai.md
  translations:
    ko:
      title: 디자인 하나의 룩 네 가지, HTML로 조판한 콘택트 시트
      description: 디자인 하나(랜딩 페이지 첫 화면, 덱의 표지와 본문 한 장, 게시물 커버, 카드뉴스 포맷의 표지와 본문 한 장, 프레임)의 룩을 네 가지로 만들어 HTML로 조판하고 브라우저로 렌더해 콘택트 시트 한 장에 모아 보여 줍니다. 레퍼런스나 기획, 또는 지금의 디자인에서 출발해 그 미감이 무엇을 말해야 하는지 읽고, 정지 화면이 보여 줄 수 있는 디자인 축(팔레트, 서체, 구성, 이미지, 형태)에 후보를 요청이 말하는 만큼 가깝게 또는 멀리 놓고, 각 후보를 데스크톱과 휴대폰 크기의 대표 화면 하나로 렌더하고, 보여 주기 전에 "AI 느낌"(아이콘 카드 격자, 그라디언트, 목업, 키커)을 판정하고, 추천과 차석과 함께 비교한 뒤 고른 룩의 토큰을 제작 스킬에 넘깁니다(카드뉴스는 빌드가 따르는 포맷 스펙으로). "이거 네 가지 룩으로 보여줘", "이 페이지 디자인 방향 뽑아줘", "이 커버 배리에이션", "이 덱 다르게 보이게", "우리만의 카드뉴스 포맷 만들어줘", "이 계정 카드뉴스처럼 하되 조금 다르게"라고 할 때, 페이지, 덱, 게시물을 만들기 전에 룩이 필요할 때 쓰세요. 룩 뒤의 기획은 web-concept-variations가, 생성 도구로 만들어야 하는 스틸은 그 도구 가족의 스킬이 맡습니다. 비용이 들지 않습니다.
---
# Four looks for one design, rendered and compared

A design to vary goes in (a page's first screen, a deck's cover and one body slide, a post's cover, a card news format's cover and one body slide, a frame), with a reference, a concept from the concept skill, or the thing as it is; a contact sheet of four looks comes out, each a position on the design axes, rendered as one representative screen the way the medium's cheapest means renders it (HTML in a browser), judged for the AI feel before it is shown, compared with a recommendation and a runner-up, and the user's pick written as a handoff of tokens for the skill that builds the thing. The reference is read for what its look says before what it is, so that the looks say the same thing by other means; nothing is spent, and a look that only a generative tool could render is shown as its position in words and handed to that tool's family.

## How the user is involved

- **Questions:** in one message, only what nothing at hand answers: the design to vary, when the request does not say which unit (the first screen, the cover, which slide); the words that must be on it, when neither the request nor a concept handoff gives them; the existing page or piece, when the request says one exists and gives neither its address nor a screenshot ("is there a page already: its address, or a screenshot?"); the brand's own tokens, when the subject has a brand file and the request did not say whether the looks may leave it. A first message with no question states what was derived and goes on.
- **Checkpoint:** the contact sheet, once, with the sheet's table: the looks with their positions, the recommendation and the runner-up. The user picks one, merges two, asks for more on one axis, or disputes a reading; the pick is theirs and the run waits.
- **Go-ahead:** when the user says to go ahead alone, the sheet is still shown and the recommendation is taken as the pick, said so. A run with no one to answer (a subagent, a showcase made unattended) takes the recommendation as a go-ahead would, marks the handoff as the skill's own pick, and leaves the sheet for whoever reads the result.
- **Changes mid-run:** a merge or "more on this axis" re-enters at the candidates, is rendered and judged again before it is shown; a disputed reading re-opens the brief.

## Requirements

| What | Used for |
|---|---|
| A shell with Python or Node.js and a Chromium-family browser a headless driver can launch, or a browser the agent drives that screenshots a local page | Rendering each look at a desktop width and a phone width and tiling the contact sheet; the same browser looks at the pages of the kind the brief reads for the crowd. A browser download is asked first. |
| A way to look at an image: the host's image reader, or a browser pane | The verdict, which is made on the screens; without it nothing can be judged. |
| A file tool | The looks as HTML files, the brief, the sheet and the handoff, in a run folder. |
| Optional: a web search tool, or a page reader | Finding the pages of the kind the brief reads for the crowd, and reading the reference's page or the subject's brand file where there are any; without search, the crowd is read from pages the user names or from what the agent knows of the genre, marked as unseen. |

Check the shell, the browser and the image reader before the first message: the browser by a launch and not a look at the disk (the render script on the skeleton, one look, is the launch); without a browser or a way to look at a screen, stop and say what to add, because a look nobody looked at is not shown. The skeleton of a look, with the rule that makes it read at phone width, is [look.example.html](assets/look.example.html); [shoot.example.py](scripts/shoot.example.py) renders the looks and tiles the sheet where the shell has Python with a headless driver, and where it has Node.js with `playwright-core` instead, the same steps are a short script of the run's own, launched as [headless.md](/docs/browser/headless.md) says.

Links that start with `/` are files of the pack this skill is from: a copy of this directory, a plugin or a mount below the root that lacks one reads it through the pack's connection (`https://skillcdn.ai/gh/skillcdn/skills`) or at `github.com/skillcdn/skills`.

## Inputs

| Input | Source |
|---|---|
| The design to vary | From the request: which unit (a page's first screen, a deck's cover and a body slide, a post's cover, a card news format's cover and one body slide, a frame) and for what. Asked when the request names only a thing. |
| The start | A reference (a link, a file, a screenshot), a concept handoff from [web-concept-variations](/product/skills/web-concept-variations/SKILL.md) (its effect brief, mechanism line and sample lines), or the design as it is (its address or a screenshot); from the request. With none of the three, the design as the user describes it, and the brief is written from their words and the crowd. The start's positions are the first row of the candidates, which "holds" refers to; with no start, that row is the crowd's positions where the request wants the genre, else the skeleton's own tokens and layout, said so. |
| The distance | Derived from the request, as axes.md "The near and the far candidate" says: a slight change keeps the looks within one or two axes of the start; something new moves each two or three axes from it, holding the mechanism line; otherwise one near, one far and two between. Said in the first message. |
| The words on it | From the concept handoff or the request: the headline, the one line, the ask, the subject's name where the request gives one, and a navigation of the subject's own sections where it has any; asked when neither gives them. The words are the same on every look, so that the sheet compares looks; the material a look shows (a document, a transcript, a diagram) carries its own words, the same across the looks that show it. |
| The brand's tokens | Read from the subject's brand file, site or previous piece where there is one; the request says whether the looks may leave them. Without any, the looks set their own and say so. |
| The medium's size | Derived: a page at a desktop width and a phone width; a slide at its page size; a post at its canvas, and since a post has no narrow screen of its own, judged on a copy at the feed's width (about a third of the canvas) with no type under about a thirtieth of the canvas's width; a frame at its aspect. Said in the first message. |
| Where the run goes | Derived: the folder the user names, else `variations/<the subject in a few words>/looks/` under the working folder, under the host's scratch folder when the working folder is a git checkout, and beside the working folder when there is no scratch folder, so that the handoff lasts for the producing skill's later run; said in the first message. The run's files never enter a repository. |
| A card news format | Where the unit is a card news format, read [card-news-format.md](references/card-news-format.md) before the first message: it says what the rows above and each phase take for that unit. |

## Workflow

Each phase produces a named artifact in the run folder.

### Phase 1: The brief, for the look

Produces the **effect brief** (`effect-brief.md`), by effect-brief.md, read for the look: the aesthetics reading above all (what each choice of the reference signals), with intent and expected effect where the reference or the concept handoff gives them and "none" where not, each one entry; the line the look must say ("the maker knows the craft", "this is for people like you", "there is nothing to hide here"), which is the look's mechanism line and what every look keeps; and the crowd, the positions the genre's pages share (a dark hero with a gradient, a device mockup, three icon cards), from three to five pages of the kind found by the category, looked at in the browser and cited by where they were seen (a page the host cannot reach is passed over for the next of the kind, and the brief says from how many pages the crowd was read), or, where none can be found or seen, written from what the agent knows of the genre and marked as unseen. A concept handoff's other references are read for their look as well. With no reference, the aesthetics reading is of the words' register and of the crowd, and the brief says so. The phase ends with the readings and the crowd in a few lines to the user.

### Phase 2: Candidates on the design axes

Produces the **candidates** (`candidates.md`), by axes.md: the start's positions as the first row, then four looks, each a position on two or three of the axes a still can show (palette, type, composition, imagery, shape and surface) with the rest held at the start's; rhythm and the tone of the copy are held, because the words are the same and a still shows no motion; written before any file is made. One near (one axis moved, the control, the one exception to two or three), one far (two or three of the crowd's positions left, which may touch more axes, the other exception), two between on different sets of axes. The request's distance changes this set as axes.md "The near and the far candidate" says. The start itself is never one of the four; where the user asks to see the design as it is beside them, it goes on the sheet as the start, labeled so.

Read the producing skill's row in [handoff.md](/docs/variation/handoff.md) "By producing skill" now: a position that skill cannot take (a block the deck's floor rejects) is not a position, and each position is written in that skill's vocabulary where it has one (the deck's theme tokens and blocks; for a page, the builder's brand file, whose sections are palette, type, shape and motion, tone and symbol, with composition and imagery described as the first screen beside it). A face is named by its class (a humanist sans, a transitional serif, a monospace); the family is the producing skill's to choose. The phase ends with the positions as a table to the user, names and axes only.

### Phase 3: Render

Produces the **looks** and the **screens**. Read [rendering-html.md](/docs/browser/rendering-html.md) before this phase.

- **The looks** (`look-<n>-<name>.html`): one self-contained fluid page each, from the skeleton, numbered 1 to 4 with the near look 1 and the far look 4, a replacement taking the number of the look it replaces. Every line of interface text (a search field's placeholder included) is set not to wrap at the phone width, and the page breaks words at spaces only.
- **The screens** (`out/`): each look opened from its file in the headless browser at the medium's size and, for a page, at a phone width too, and screenshotted (rendering-html.md "Looking at a render"; a look is a fluid page, not a page of many units with an export mode). The render script does the launch, the two widths and the tiling, and `sheet.html` is its working file.
- **Words the run writes itself** (the interface text, the words of the material a look shows) are written after reading [readers.md](/docs/writing/readers.md) and [facts.md](/docs/writing/facts.md) of the pack's writing set.
- **Fonts:** a web font the brand names is loaded from its documented path (rendering-html.md "Fonts"), the one thing fetched; otherwise system faces, which are the host's, so that a screen shows the host's face for the class named.
- A look that needs a still only a generative tool can make carries the position as a note where the still would be, marked as a note, and the sheet says so.

The phase ends with a line that the screens exist; none is shown yet.

### Phase 4: The verdict

Produces the **verdict** (`verdict.md`), by not-ai.md "Signals in a look", the bundles and the positive tests, on the screens and not on the files, each screen looked at (a re-rendered file read under a new name, or its pixels compared, as rendering-html.md says) and named in the verdict with the render it was: the thumb test as the first second on the first screen; take the product away on the look with its words; the followers test where a reference exists; one is not like the others on the set as a whole. A look is judged at the size its reader meets first, the phone width for a page and the feed-width copy for a post (each copy opened, not the sheet's tiles), and a look that reads at one width only is fixed (the narrow-width rule of the skeleton) and rendered again; a look that cannot be fixed on its axes is dropped, its file removed, and replaced under its number; the script is run again after the fixes, so that the sheet tiles what passed. A signal kept on purpose is named with its reason, which the sheet's verdict column carries. The phase ends with one line per look on what was fixed.

### Phase 5: The contact sheet

Produces the **sheet** (`sheet.md` and `out/sheet.png`). Read [comparison.md](/docs/variation/comparison.md) before this phase. The four desktop screens are tiled at the same size on one image with the name under each, the near one first and the far one last, the reference not on it, the phone screens beside it one per look (for a post, the sheet's own tiles are its feed-width copies); the table has comparison.md's columns, with what the look says in the brief's terms as its mechanism, keeps and changes against the start's row, to produce in the producing skill's units where its handoff row gives them, and the screens' names; then the recommendation argued in the brief's readings, the runner-up with what it would give instead, and why the far one is there.

Checkpoint, in plain words: the sheet and the phone screens attached (for a post, the sheet alone), or their paths where the host attaches no files, with the table; the recommendation and why; the runner-up; "pick a number, merge two, ask for more on an axis, or say which reading is wrong"; "ok" takes the recommendation. The pick is the user's; the run waits. A merge, or more on an axis, is placed on the axes, rendered, judged and shown once more within six, the weakest kept ones dropped and their files removed; `candidates.md`, `verdict.md` and `sheet.md` are rewritten, the earlier sheet kept as `sheet-1.md`.

### Phase 6: The handoff

Produces the **handoff** (`handoff.md`), by handoff.md of the variation set: the brief with the line the look must say, the pick's row, what must stay (the narrow-width rule among it), the screens, the fixes, the assumptions the run rests on (the start, the crowd seen or unseen, the medium) and what was left out, and the pick's tokens in the producing skill's own vocabulary (a deck's `meta.theme` and its blocks; a page's brand file with palette, type, shape and motion, tone and symbol with the reason for each, the first screen's composition and imagery described beside it); a token no look decided (a symbol, a motion) is left open and said so. The delivery: the run folder's path, the pick in one line, the look files, the producing skill to start next and what it will ask that the pick does not answer (its handoff row says), and that nothing was built here.

## Verdicts

| Result | Verdict |
|---|---|
| A look that moves on every axis, or on none | Redo: two or three axes, the rest held at the start's row; the near look's one axis and the far look's crowd are the exceptions |
| Two looks that differ in a color only, where the request did not name color alone | Redo: one of them on another set of axes |
| A look that carries a bundle of signals, or a signal with no reason the sheet can state | Fix on its axes and render again; drop and replace when the fix lands on another look's axes |
| A look that reads at the desktop width and not at the phone width (one word per line, a column that cannot be read, a cut) | Fix the narrow-width rule and render again; never shown as it was |
| A look whose words differ from the others' | Redo: the same words on all |
| A screen made and not looked at | Not reviewed: look, then judge; without a way to look, the run stopped before rendering |
| A look shown before the verdict | Not done: positions and a line end phases 2 and 3; the screens appear at the sheet |
| A position the producing skill cannot take | Redo: a position in that skill's vocabulary |
| A sheet without the near or the far look its distance asks for (axes.md), or more than six | Redo |
| A look that needs a generated still | Shown as its position in words where the still would be, said so; the still is that family's skill's |

## Hard rules

1. The look is read for what it says before what it is: no candidate before the aesthetics reading and the line the look must say.
2. The same words on every look. A sheet whose looks differ in their words compares copy, not looks.
3. Every look is rendered and looked at, at the size its reader meets first, before it is shown; a look that fails the phone width is fixed, never shown with a caveat. The user's word for what the verdict prevents is "it looks like AI".
4. Nothing is downloaded, generated or spent: system faces, the brand's own web font, or the web font a card news look names, HTML in a browser, no still from a generative tool; where a look needs one, the position is shown in words and the tool's family decides what it costs. Opening a public page in the browser to look at it is not a download.
5. The pick is the user's, at the sheet; the skill recommends and never chooses. A go-ahead takes the recommendation and says so.
6. The handoff is tokens in the producing skill's own vocabulary, for a card news format a designed spec; that skill is started by the user, or goes on where it asked for the looks, and keeps its own floor.
7. For a card news format, posts are read only by `instagram-card-news-format-study`, and a reference's photos, words and name never enter a look.

## Terminology

| Term | Meaning |
|---|---|
| Look | One position on the design axes, rendered as one representative screen. |
| Representative screen | The unit the reader meets first: a page's first screen, a cover, a frame; rendered at the medium's size and, for a page, at a phone width. |
| Start | The positions every look holds unless it moves: the reference's, the existing design's, or, with neither, the crowd's or the skeleton's, as the first row of the candidates. |
| Crowd | The positions the genre's pages share, recorded in the brief; what the far look leaves. |
| Axis | A dimension a look moves on: palette, type, composition, imagery, shape and surface, rhythm, tone of the copy. |
| Near, far | The look that moves on one axis (the control); the one that leaves the positions the genre crowds on. |
| Verdict | The pass of every look against the AI-feel signals and the positive tests, on the screens, before the sheet. |
| Contact sheet | The four screens tiled at the same size on one image, the names under them, the reference not on it. |
| Handoff | The pick's tokens in the producing skill's own vocabulary, for the user to start that skill with. |
