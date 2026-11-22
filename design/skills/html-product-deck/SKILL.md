---
name: html-product-deck
description: "Makes a product deck that sells a product or one of its features to buyers, as one HTML file and a PDF, every slide one message in a scene composed for it (a real screen, a scene drawn in the product's shapes, a chat, a customer's day) under a title that hooks in the buyer's words. Use when a user says \"make a product deck\", \"a product introduction for our customers\", \"a sales deck that hooks\", \"a brochure deck for our service\" or \"introduce this feature to customers as a deck\". A business plan, an investor plan, a kickoff or a report from notes is html-deck-from-outline, a market magazine issue is html-signal-magazine, and four looks for the cover come from html-design-variations. Reads what the product does from its own pages and documents, gathers its screens and brand tokens, storyboards one message a slide, writes each slide by hand, renders with a Chromium-family browser, checks the layout, the house style and the banned phrases, and looks at every slide before delivery. Nothing is spent."
license: MIT
compatibility: Needs a shell with Node.js, a Chromium-family browser (an installed Chrome or Edge, or Playwright's), a way to read the product's pages and documents, and a way to look at an image. Without the browser or the image reader the skill stops before the first message and says what to add.
metadata:
  author: skillcdn
  version: "1.2"
  tools: browser
skillcdn:
  include:
    - references/storyboard.md
  translations:
    ko:
      title: 제품을 파는 소개 덱을 HTML과 PDF로
      description: 제품이나 그 기능 하나를 구매자에게 파는 소개 덱을 HTML 파일 하나와 PDF로 만듭니다. 장마다 전할 말 하나를 그 장을 위해 새로 짠 장면(제품의 실제 화면, 제품 모양을 본떠 그린 장면, 메신저 대화, 고객의 하루)에 담고, 제목은 구매자의 말로 후킹합니다. "제품 소개서 만들어 줘", "고객에게 보여 줄 제품 소개 덱", "후킹되는 세일즈 덱", "서비스 브로슈어 PPT", "이 기능을 고객에게 소개하는 덱"이라고 할 때 쓰세요. 사업 기획안, 투자용 기획안, 착수회의 발표, 보고서는 html-deck-from-outline의 몫이고, 시장 매거진 한 호는 html-signal-magazine이, 표지의 네 가지 룩은 html-design-variations가 맡습니다. 제품이 하는 일은 제품의 페이지와 문서에서 읽고, 화면과 브랜드 토큰을 모으고, 장마다 한 문장으로 스토리보드를 짠 뒤, 장을 손으로 쓰고 크로미움 계열 브라우저로 렌더해 배치와 문안 규칙과 금지 문구를 검사하고, 모든 장을 직접 본 뒤 전달합니다. 비용은 들지 않습니다.
---
# A product deck that sells, in HTML and PDF

A product goes in (its site, its documents, its screens, or one feature named in a sentence) with who the deck is shown to; out come the deck's source (`deck.html`, one hand-written scene per slide), one self-contained HTML file, a PDF, an image of every slide and a contact sheet the agent has looked at, with a report that holds no finding. A product deck is not a document in slide form: each slide says one thing the buyer cares about and shows it in a scene composed for that slide. A deck assembled from shared blocks reads as a report however good its content, so this skill storyboards first and shares nothing between slides but the tokens.

## How the user is involved

- **Questions:** one first message, only for what the request and the material leave open: where the product can be read about and seen ("Where can I read about it and see it: a site, documents, a demo or a preview, brand files?"); the reader and the use ("Who will see this deck, and how: sent as a PDF, shown on a call, handed out?"); what stays out ("Is there anything that must not appear, such as internal screens, figures or how you work? And a feature still being built: left out, or shown?"); the reference ("Is there a deck or a page whose look ours should start from? Without one I start from the product's own site and brand."). A first message with nothing left to ask, or under a go-ahead, states what was derived and goes on.
- **Checkpoints:** the storyboard, before any slide is built: one line per slide (its message, its title, its scene), the look's routes with the recommendation, what stays out, the facts not found. Then the rendered deck: the contact sheet, the count of findings (none), which screens are captured and which drawn, what the scenes made up. One short message each; "OK" takes the recommendation.
- **Go-ahead:** the storyboard is stated and not waited on, with the recommended look; the sheet is still shown with the delivery.
- **Changes mid-run:** a note on the whole deck ("repetitive", "obvious", "too technical", "the hooks are weak") re-enters at the storyboard, for every slide; a note on one slide rewrites that slide's section; a note on a wording fixes it wherever it stands and adds it to the deck's `banned` list, so that a later render names it if it returns. Every round renders the whole deck, runs the checks and looks again.

## Requirements

| What | Used for |
|---|---|
| A shell with Node.js and `playwright-core` | The helper [`scripts/render.mjs`](scripts/render.mjs): the one-file HTML, the PDF, the page images, the sheet, the checks. The driver is borrowed through `PLAYWRIGHT_FROM` or installed once into a tools folder outside what is delivered ([headless.md](/docs/browser/headless.md)). |
| A Chromium-family browser | The render, and capturing the product's screens where a site, a demo or a preview can be opened. |
| A way to read the product's pages | A page reader, the browser, or the connection its documents are served through (a repository, a document pack with search and read tools). |
| A way to look at an image | Every slide is looked at before it is shown. |

Before the first message, run the helper on [`assets/deck-skeleton.html`](assets/deck-skeleton.html) into the host's scratch folder: two slides and no finding mean the driver, the browser and the helper work. Without a browser or a way to look at an image, stop and say what to add. Through SkillCDN the helper and the skeleton are read with `read_repo_file` at their paths and saved in the run folder.

Links that start with `/` are files of the pack this skill is from: a copy of this directory, a plugin or a mount below the root that lacks one reads it through the pack's connection (`https://skillcdn.ai/gh/skillcdn/skills`) or at `github.com/skillcdn/skills`.

## Inputs

| Input | Source |
|---|---|
| The product | The request: a name, a link, a folder, or one feature of a product named in a sentence. Asked where the request gives nothing to read. |
| What the product does | Its own pages and documents, read in full in phase 1: the site, the documentation, a README and release notes, a document pack the host is connected to. Never memory or a search summary. |
| Screens | In this order: files the user hands over; captures from a site, a demo or a preview the agent can open; scenes drawn from what the documents say a screen holds (building.md "Screens"). |
| The reader and the use | Asked; the request's implication is the default, a buyer who is not technical where nothing says. |
| What stays out, and features still being built | Asked. By default the organization's internal screens, figures and ways of working stay out, and so does a feature the documents do not describe as there, or describe and mark as not yet proven. |
| The reference | Asked: a deck or a page of the user's choice, else the product's own site and brand file. Where the user has none and the product has neither, three product pages of the kind are found and the user picks one. |
| House style | The usual set ([house-style.md](/docs/writing/house-style.md)) unless the request or the organization's records say otherwise; stated in the first message, written into the deck's `style` only where it differs. |
| The user's own facts | A career, a partner's name, a measured figure: used as given, never blurred into a vaguer word. |
| Where the run goes | The folder the user names, else `product-deck/<product>/` under the working folder: `brief.md`, `facts.md`, `storyboard.md`, `deck.html`, `assets/`, `out/`. |
| Everything else | Derived and shown at the storyboard: the story's order, ten to fifteen slides, each slide's scene, the tokens and the font, the cast, the banned list. |

## Workflow

### Phase 1: The brief and the facts

Produces `brief.md` and `facts.md`. Read the product's pages and documents in full, as [facts.md](/docs/writing/facts.md) of the writing set says; for one feature, the pages that introduce the product and the feature, and the pages those name for what it does; a further search result is read only where a claim needs it, and `facts.md` lists what was read and what was found and left unread. `brief.md` holds the reader and the use, what stays out, how a feature still being built is treated, the user's own facts, and three to five strengths to lead with, each as what the buyer gets. `facts.md` is a table of every claim the deck may make (what the product does, for whom, how a buyer starts, a figure), each with an id, the page or section it comes from and its sentence there, and the product's own word for a thing beside the buyer's word for it. What the documents do not say is not claimed: it goes under "not found", with where it was looked for, and is asked at the storyboard or dropped. The phase ends with the reader, the strengths and the gaps in a few lines.

### Phase 2: Materials

Produces `assets/`, by [building.md](references/building.md) "Materials" and "Screens": the product's marks, its colors and font, its screens (handed over, captured, or to be drawn), results it has made, the marks of the products it works with, each file's origin a line in `facts.md`. A screen that can be neither had nor captured is marked "drawn" for the storyboard, never replaced by a stock picture.

### Phase 3: The storyboard

Produces `storyboard.md`, by [storyboard.md](references/storyboard.md). Read first [readers.md](/docs/writing/readers.md), [sentences.md](/docs/writing/sentences.md), [outside-readers.md](/docs/writing/outside-readers.md) and house-style.md; this skill's own forms win. One row per slide: the message (one sentence the buyer could repeat to a colleague), the title, the scene's pattern, the material it uses (which screen, captured or drawn; which fact ids), and what the scene makes up. A job of the story that has no hook for this buyer is dropped, not shortened.

The look is decided here, from the reference, on the routes in this order:

| Route | What happens | Recommended when |
|---|---|---|
| Four looks from the reference | [html-design-variations](/design/skills/html-design-variations/SKILL.md) runs now on the cover and the slide with the strongest scene, with this storyboard's titles as the words, at its own stops; the pick's palette, type and shape become the deck's tokens. | The reference is another party's deck or page, so that ours is not a copy of it. |
| The reference as it is | Its colors, font, radius and surfaces are read into the tokens (building.md "Materials"); its pictures, words and layouts are not taken. | The reference is the product's own site and brand. |

Checkpoint, in plain words: the rows as a short list; the look's two routes with the recommendation; what stays out; the facts not found; "OK builds it, a number changes that slide, or name the other route".

### Phase 4: Build

Produces `deck.html`, from the skeleton, by building.md "The deck file": one `section.slide` per row of the storyboard, its `data-pattern` the row's pattern, every class of its scene under the slide's own prefix, every color and the font from the tokens. The deck's `banned` list starts with the wordings the user has rejected and, in the deck's language, the status tags and the disclaimers the hard rules exclude.

### Phase 5: Render, check and look

```
node render.mjs deck.html out --name <YYYY-MM-DD-product>-deck
```

The helper writes the one-file HTML, the PDF, `pages/NN.png`, `sheet.png` and `report.json` into `out/`, prints every finding with its slide, and exits 1 while there is one (building.md "The helper" has each finding's fix, and what its notes mean). Fix `deck.html` and run again until there is none; the HTML and the PDF are never edited by hand. Then look: the sheet for the deck as a whole (rhythm, a pattern that returns too soon, a slide that reads as a document page), then every page image at full size, as [rendering-html.md](/docs/browser/rendering-html.md) "Looking at a render" says, against the verdicts below. A slide that passes and still reads as a default is held against [not-ai.md](/docs/variation/not-ai.md).

Checkpoint: the sheet attached or by its path, the count of findings, which screens are captured and which drawn (said plainly where all are drawn), and what the scenes made up.

### Phase 6: Deliver

Deliver the HTML and the PDF by path, with the slide count and the report's verdict. Say where the tokens and the font came from, which fonts loaded and any face the text fell back to, which slides show captured screens and which drawn ones, what the scenes made up, what was left out on purpose, and what the user confirms before the deck goes out: a claim that rests on one source, a fact not found, a feature shown that the documents mark as unproven. `deck.html` and `assets/` stay as the source of the next change, the sheet and the report as the review's record.

## Verdicts

Read before the build and at the look.

| Result | Verdict |
|---|---|
| Every slide one message in its own scene, no pattern twice in a row, no finding, every page looked at at full size, every title in the buyer's words | Delivered |
| Slides that read as a document: stacked blocks, a table, bullets under a heading; or screens appended as pictures after the story | Back to the storyboard, for every slide |
| A slide with no hook, or a feature every product of the kind has | Dropped, or replaced by a scene the buyer would not expect; never shortened |
| A customer slide in which that customer cannot see their own day | Rebuilt as a day for each kind of customer |
| A finding that is meant (an enlargement running off the slide, a picture cut by its frame) | `data-bleed` or `data-clip` on that element, said in the delivery |
| The same note from the user a second time | The wording into `banned`, the point into `brief.md`, every slide checked for it |

## Hard rules

- **One message and one scene a slide; no pattern twice in a row.** Repetition is what makes a deck read as generated.
- **One title a slide, hooking in the buyer's words.** No subtitle row, author, date or document label; the cover carries the title and the marks.
- **Show the product at work.** A real screen, or a scene drawn in the product's shapes; a sentence about a feature is the last resort.
- **Nothing about the product is invented.** What it does, for whom and how well comes from `facts.md`; a scene's cast (its people, names, tasks, sample figures) is made up, plausible, and carries no "sample data" note.
- **The buyer's words, and effects over mechanisms.** An easy word that is not wrong beats an exact word that is hard; a number appears only when it is strong, a small count in words or not at all; a date only when the date is the message.
- **No disclaimers and no status tags.** "Coming soon" or "beta" only on the user's word; a wording the user rejected is in `banned` before the next render.
- **The organization's internal screens, figures and ways of working stay out**, whatever material was handed over, unless the user names them for the deck.
- **A deck with a finding, or a slide the agent has not looked at at full size, is not delivered.**

## Terminology

- **Pattern**: the kind of scene a slide is (storyboard.md "Scenes"), named in the storyboard and in the slide's `data-pattern`.
- **Cast**: the made-up people, names, tasks and sample figures inside the scenes, the same across slides.
- **Banned list**: the phrases in the deck's `deck-meta` that a render reports on any slide.
