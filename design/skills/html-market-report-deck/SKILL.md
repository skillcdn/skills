---
name: html-market-report-deck
description: "Makes one issue of a market report a brand hands out, as a slide deck in one HTML file and a PDF, from market research already done: every slide one message carried by a chart or a picture composed for it, in the look of the brand's own site with a magazine-style cover and contents, every number kept in a ledger and checked against its source, and a closing view that says no more than the slides before it. Use when a user says \"make this month's market report\", \"turn the research into a deck we hand out\", \"a market trend report in our brand\", \"an industry report for founders\", \"this issue of our market magazine\" or \"the next issue\". The research comes from web-market-entry-signals and company figures from dart-company-figures; a deck that sells a product is html-product-deck, and an internal report or a proposal from notes is html-deck-from-outline. Reads the brand's site, gathers logos and app screens, writes each slide by hand and looks at every one before delivery. Nothing is spent."
license: MIT
compatibility: Needs a shell with Node.js, a Chromium-family browser (an installed Chrome or Edge, or Playwright's), a way to read web pages, and a way to look at an image. Without the browser or the image reader the skill stops before the first message and says what to add.
metadata:
  author: skillcdn
  version: "1.3"
  tools: browser
skillcdn:
  include:
    - /docs/market-research/evidence-grades.md
  translations:
    ko:
      title: 시장 리포트 한 호를 덱으로, HTML과 PDF
      description: 이미 해 둔 시장 조사로, 브랜드가 바깥에 내는 시장 리포트 한 호를 슬라이드 덱(HTML 파일 하나와 PDF)으로 만듭니다. 장마다 전할 말 하나를 그 장을 위해 짠 도표나 그림에 담고, 디자인은 브랜드 사이트를 따르되 표지와 차례는 매거진처럼 하며, 모든 숫자는 숫자 표에 적어 원문과 대조하고, 마지막 시각은 앞 장들이 말한 만큼만 말합니다. "이번 달 시장 리포트 만들어 줘", "조사 결과를 배포용 덱으로", "우리 브랜드로 시장 트렌드 리포트", "창업자에게 돌릴 산업 리포트", "시장 매거진 이번 호", "다음 호"라고 할 때 쓰세요. 조사는 web-market-entry-signals에서, 회사 숫자는 dart-company-figures에서 옵니다. 제품을 파는 덱은 html-product-deck, 노트로 만드는 내부 보고서나 제안서는 html-deck-from-outline의 몫입니다. 브랜드 사이트에서 토큰을 읽고, 로고와 앱 화면을 모으고, 장을 손으로 쓴 뒤 모든 장을 직접 보고 전달합니다. 비용은 들지 않습니다.
---
# One issue of a market report, as a deck in HTML and PDF

Research already done goes in (verdicts on markets, the numbers behind them, the companies in them) with the brand the report goes out under; out comes one issue: `deck.html` with one hand-written scene a slide, one self-contained HTML file and a PDF, the ledger of its numbers (`facts.md`), a library of logos, icons and screens the next issue uses again, and a note that hands the issue to a designer. Its readers did not ask for it, so an issue wins on data shown well and never on explanation: every slide is one sentence with its figure and one drawing composed for it. The series carries its corrections forward: the next issue starts from this one's folder.

## How the user is involved

- **Questions:** one first message, only for what the request and the series folder leave open: "Which brand does it go out under, and where is its site? I take the look from the site."; "What is the contact on the back cover?"; for a first issue, "What is the report called?"; "Which names and subjects stay out: your own companies and people, ideas you are still weighing, partners?"; and house-style.md's question, unless the last issue's `deck-meta` holds the answer. The readers and the questions the series answers are stated with their defaults (people and teams who want to start a business; which market to enter now, and how AI is put to work in it) and changed on the user's word.
- **Checkpoints:** the plan, before any slide: one line a slide (its sentence, its scene, its figures with their grades), how the closing view answers the series' questions, the companies proposed for cards with each figure's check, a recommended order and one alternative. Then the cover and the busiest slide, rendered in the brand's tokens. Then the whole issue: the sheet, no finding, and what the user confirms before it goes out (a figure that rests on one source, the companies named and their marks). Then the hand-off note, before anything is put on a designer's board.
- **Go-ahead:** the plan and the cover are stated and not waited on. The companies on cards are still the user's pick, the issue is still shown, and nothing goes to a designer or to readers without the user's word.
- **Changes mid-run:** a note on a wording fixes that slide, then every slide with a sentence of the same form, and the wording joins the `banned` list; a note on the order or the conclusion re-enters at the plan and runs phase 6 again; a note on the look ("off-brand", "too much emphasis") re-enters at phase 1's tokens, for every slide. Every round renders the whole deck and looks again.

## Requirements

| What | Used for |
|---|---|
| A shell with Node.js and `playwright-core` | The helper, [`render.mjs`](/design/skills/html-product-deck/scripts/render.mjs) of [html-product-deck](/design/skills/html-product-deck/SKILL.md), run as it is: the one-file HTML, the PDF, the page images, the sheet, the checks. The driver is borrowed through `PLAYWRIGHT_FROM` or installed once into a tools folder outside what is delivered ([headless.md](/docs/browser/headless.md)). |
| A Chromium-family browser | The render, and the captures of the brand's site. |
| A way to read web pages | The brand's site, and every source a number is checked against. |
| A way to look at an image | Every slide is looked at before it is shown. |

Before the first message, save the helper and [`assets/issue-skeleton.html`](assets/issue-skeleton.html) fresh in the host's scratch folder (through SkillCDN, `read_repo_file` at their paths), never beside what is delivered, and run the helper on the skeleton there: two slides and no finding mean the driver, the browser and the helper work.

Links that start with `/` are files of the pack this skill is from: a copy of this directory, a plugin or a mount below the root that lacks one reads it through the pack's connection (`https://skillcdn.ai/gh/skillcdn/skills`) or at `github.com/skillcdn/skills`.

## Inputs

| Input | Source |
|---|---|
| The research | What [web-market-entry-signals](/product/skills/web-market-entry-signals/SKILL.md) left in the market folder: the latest survey's gates table `report.md` and `notes/`, and `watch.json` with its observations. Taken first: what moved since the last issue. A verdict of `unknown` is shown as unknown; the watch list's statuses and the user's own plans are not shown. With no research, say that skill runs first. |
| Company figures | `figures.json` of [dart-company-figures](/product/skills/dart-company-figures/SKILL.md), run in phase 2, into the issue's folder, on the entrants and incumbents of the notes that could stand on a card. A figure goes on a slide where its `check` is `matches` or `sums-up`; `announced-only` goes on the user's list to confirm. A US company's are read again in its SEC filing; where that site refuses the host, the copy the survey saved in its `work/` is read, and `facts.md` says so. |
| An idea looked into | From `review.md` of [web-business-idea-deep-dive](/product/skills/web-business-idea-deep-dive/SKILL.md), only the numbers the user says may be public; never its verdict or its pilot plan. |
| The brand, the contact, the name, what stays out | Asked. The issue goes out as the brand: no person and no company name stands on it unless the user gives one for it. |
| The series folder | The folder the user names, else `market-report/` in the market folder: `brand.md`, `library/`, and one folder an issue, `<YYYY-MM>/` with `plan.md`, `facts.md`, `deck.html`, `handoff.md`, `out/`. A later issue starts as a copy of the last one's folder without `out/`. |
| The issue's name | Derived: its period ("JAN 2026"), the month its data stands at; issues are not numbered. |
| The banned list | The `banned` of the last issue's `deck.html`, the names and subjects the user keeps out, and every wording the user corrects. |
| Everything else | Derived and shown at the plan: the order, the slide count, each slide's scene, which companies and apps are shown. |

## Workflow

### Phase 1: The brand

Produces `brand.md`, by [design-system.md](references/design-system.md) "Reading the brand's site". A later issue reads `brand.md` and looks at the site again only for what changed. The look is offered on the root rule's routes with the site as it is recommended, since the issue goes out as the brand's; four looks from [html-design-variations](/design/skills/html-design-variations/SKILL.md) vary the cover and one body slide inside the site's tokens, at that skill's own stops. A magazine the user wants the issue to resemble is taken for its page composition only, where the user names one.

### Phase 2: The numbers

Produces `facts.md`, shaped as [`facts.example.md`](assets/facts.example.md): one row for every number the issue may show, with the sentence of its source, the address, its grade, its check and, where the watch list holds it, its metric id; its slide is filled in at the plan. Open every source again and find the number in the sentence: a number its source does not state, states of something narrower, or states of another period is corrected or dropped, and the row says which. A price is a band from the cheapest to the dearest of one billing period; a comparison sets side by side two values of the same year, definition and method (two countries' counts of themes named apart are not one); a profit is an amount.

### Phase 3: The plan

Produces `plan.md`. Read first [sentences.md](/docs/writing/sentences.md), [outside-readers.md](/docs/writing/outside-readers.md) and [house-style.md](/docs/writing/house-style.md); this skill's forms win. One row a slide: its sentence, its scene from [scenes.md](references/scenes.md), its rows of `facts.md`.

- The contents slide's title is the issue's one sentence, and the slides right after it are the ones that carry it.
- A slide's title is one sentence that holds its figure, the figure first: "<figure> came in within two years", not "Entry trends".
- No scene twice in a row, and several scenes an issue that the last issue did not use. A numbered list of three lines is a document page, not a scene.
- Under the question whether entrants earn, a card holds only a company that entered within the survey's window; an older one stands under its own head with the year it entered (a reader took an incumbent's profit there for the entrants'), as does an older company whose product entered in the window, its card saying the figures are the whole company's. A later period's filed figures that turn the year's (a profit after a loss) stand in a line under them.- The closing view answers the series' questions in their order and ends on a question the reader would put to the brand; each of its sentences names in `plan.md` the slides it rests on.

Checkpoint: the rows as a short list, the closing view's sentences, the look's routes, the companies proposed for cards (the name, what it sells, its founding year, whether it is listed, both figures with their `check`) for the user to pick, and "OK builds it, a number changes that slide".

### Phase 4: The library

Produces `library/` and its `index.md`, by [library.md](references/library.md): the logo, the icon and the screens of every company and app the plan shows, under names the deck can rely on.

### Phase 5: Build

Produces `deck.html`: the skeleton with the brand's tokens, then one `section.slide` a row of the plan, each started from its file under [`assets/scenes/`](assets/scenes/contents.html) and composed for its message, by design-system.md "The deck file" and scenes.md. The small figure beside a number on the cover and the contents is drawn by [sparks.md](references/sparks.md). Render the cover and the busiest slide first: the company cards where the plan has them, else the slide with the most drawn units.

Checkpoint: those two slides, by path or attached, and what was taken from the site.

### Phase 6: The closing view, checked

Take the closing view's sentences one by one against the slides they rest on. A sentence fails where its slide's verdict is `unknown`, where the slide tells a later turn the sentence leaves out (a leader overtaken, a loss), or where it says more than the slide shows ("new companies earn" over companies that are ten years old). A failed sentence is rewritten to what the slides show, or dropped, and `plan.md` records the pass.

### Phase 7: Render, check and look

```
node <scratch>/render.mjs <YYYY-MM>/deck.html <YYYY-MM>/out --name <report>-<YYYY-MM>
```

The helper writes the one-file HTML, the PDF, `pages/NN.png`, `sheet.png` and `report.json`, and exits 1 while it has a finding; design-system.md "The helper's findings" has each fix, and [tool-notes.md](references/tool-notes.md) what grows a PDF. Fix `deck.html` and run again until there is none. Then look: the sheet for the issue as a whole, then every page at full size, as [rendering-html.md](/docs/browser/rendering-html.md) "Looking at a render" says, for what no check sees: things that overlap or touch, a label off its tick, a drawing that says something other than its figure.

Checkpoint: the sheet, the count of findings, the PDF's size, and the list the user confirms before the issue goes out.

### Phase 8: Deliver and hand off

Deliver the HTML and the PDF by path with the slide count. Say which figures rest on one source, which scenes are new, and what was left out. A figure the series will show again and `watch.json` does not hold yet is added there as a metric, this reading its first observation (the filed figures of the companies on cards under gate 04, a new period of a count the issue drew; never a price band), with one line in `log.md`, in the shape [watch-record.md](/docs/market-research/watch-record.md) gives, and `facts.md` takes its id. Write `handoff.md` as [`handoff.example.md`](assets/handoff.example.md) at every delivery and show it; whether a designer takes the issue on, and putting the note and the files on a board, are the user's steps, confirmed each time.

## Verdicts

Read before the build and at the look.

| Result | Verdict |
|---|---|
| Every number in `facts.md` with its source's sentence, no finding, every page looked at, the closing view passed sentence by sentence | Delivered |
| A number its source does not state as shown | Corrected to the source's scope, or dropped |
| A slide that explains its method, points to another page, carries a baseline nobody needs or a title that only labels | Rewritten to its one sentence; the wording into `banned` |
| A scene the last issue used in the same place, or two alike in a row | Another scene, in the plan first |
| A company card with an adjective ("profitable") for a figure, or a figure whose `check` is below `sums-up` | The amount from the filing; else no card, and the company on the user's list |

## Hard rules

- **The look stays the brand's.** One ground with its light, the site's cards as the surfaces, one accent and about one accented figure a slide, the point colour for a dot, a fall drawn faint and never in a warning colour; the serif stands in the masthead and the foot mark alone. The series' own frame, in a magazine's manner, shows in the cover, the contents and the foot mark, nowhere else: an edition that left the site's look was sent back.
- **Sources and methods stay in `facts.md`.** No source line, no counting method and no note on how a chart was made stands on a slide: the sources are the brand's record and the method its know-how.
- **Every number is checked against its source's sentence before it is drawn**, and recorded: an issue whose numbers were all read again found several wrong or wider than their source.
- **A small figure is a different shape for every item**, drawn from real values: a straight line reads as made up.
- **Nothing that is not the message:** no intro that explains the method, no page pointer, no filler title, no promise of a next issue or its date, no credit to a tool, no headcount or target of the brand's. A corrected wording joins `banned` before the next render.
- **What the user keeps out stays out:** their companies and people, ideas under review and what was decided about them, partners and their products. All of it is in `banned`.
- **Logos, icons and screens come from the company's own pages or its store listing, at their own proportions,** to name the company. A mark a reader would not know by sight has the name beside it.
- **The closing view says no more than the slides before it** (phase 6).
- **An issue with a finding, or a slide not looked at at full size, is not shown.**

## Terminology

- **Scene**: the kind of drawing a slide is, named in `plan.md` and in the slide's `data-pattern`.
- **Banned list**: the phrases in the deck's `deck-meta` that a render reports on any slide.
- **Closing view**: the slide before the back cover, the brand's own reading of the issue.
