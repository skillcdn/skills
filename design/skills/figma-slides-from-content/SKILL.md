---
name: figma-slides-from-content
description: Moves a document (a proposal, a report, any PDF) into an existing Figma Slides deck as new slides, one per page, built in the deck's own design system rather than a generic one. Use when a user says "put this PDF into this deck", "move this proposal into Figma as it is", "make slides from this document in the style of this deck", or asks for a deck's slides to be tidied to one scale and spacing. A deck from scratch with nothing to match is Figma's own slides guidance, not this skill. Reads the document's text with its sizes and positions and its images, measures the deck's existing slides for the type scale, colors, margins, bullet marks, cards and shadows, plans one slide per page with a layout type, builds them through the Figma MCP server, and checks every slide by numbers and zoomed renders so that alignments hold on the glyphs and every element of one role is identical across slides.
license: MIT
compatibility: Needs the Figma MCP server with use_figma, get_figma_skill and upload_assets, a Figma account that can write to the deck (writing through the server needs a paid Full seat), and a shell with Node.js and npm for reading the PDF and posting uploads. Works in any agent that can call MCP tools and run a shell.
metadata:
  author: skillcdn
  version: "1.0"
  tools: figma
skillcdn:
  include:
    - references/tool-notes.md
    - references/deck-spec.md
  translations:
    ko:
      title: 문서를 덱의 디자인 그대로 Figma 슬라이드로
      description: 제안서나 보고서 같은 PDF 문서를 기존 Figma Slides 덱에 페이지당 한 장씩 새 슬라이드로 옮깁니다. 임의의 디자인이 아니라 덱에 이미 있는 디자인 체계를 씁니다. 문서의 글자 크기와 위치, 이미지를 읽고, 덱의 기존 슬라이드에서 글자 크기 체계, 색, 여백, 불릿 표시, 카드, 그림자를 측정해 페이지마다 레이아웃 유형을 정한 슬라이드 계획을 세운 뒤 Figma MCP 서버로 만들고, 모든 슬라이드를 수치와 확대 렌더로 검사해 정렬이 글리프 기준으로 맞고 같은 역할의 요소가 전부 동일하게 합니다. "이 PDF 덱에 넣어줘", "제안서 피그마로 그대로 옮겨줘", "이 덱 스타일로 문서를 슬라이드로 만들어줘", 또는 덱의 슬라이드를 한 가지 크기와 간격으로 정리해 달라고 할 때 쓰세요. 맞출 기존 슬라이드가 없는 새 덱은 이 스킬이 아니라 Figma 자체 슬라이드 가이드의 몫입니다.
---
# Slides from a document, in the deck's own design

A document (a PDF) and a link to a Figma Slides deck go in; new slides come out, one per page of the document, in a row of their own, built from the deck's existing slides' measured specs: its type scale, colors, margins, title treatment, bullet marks, cards and shadows. The document's words, line breaks and images are kept as they are; only the design is the deck's. Every slide is checked before it is shown: content edges against the margins, one spec per element role, no text outside a card's padding, no word broken mid-way, and the alignment of glyphs, not boxes, on zoomed renders. Slides that existed before, and any slide the user edits during the run, are never rebuilt. Nothing is spent and nothing is deleted.

## How the user is involved

- **Questions:** only for the document and the deck link, and only when the request lacks one. Everything else is derived and stated at the plan checkpoint.
- **Checkpoints:** the slide plan (page to slide, layout type each, the type scale, the font substitution, the row) and the audit (a screenshot of every new slide with the element inventory). Each is one short message; "OK" continues.
- **Go-ahead:** when the user says to go ahead alone, both checkpoints are skipped; the delivery still shows every slide's screenshot.
- **Changes mid-run:** a correction ("the bars differ", "the base size should be 22") re-enters at the audit and is applied to every new slide, not only the one named; the run then re-audits all of them.

## Requirements

| What | Used for |
|---|---|
| `use_figma` of the Figma MCP server | Every read and write in the deck, as Plugin API JavaScript: inspection, the build, the audit, inline screenshots with `node.screenshot()`. |
| `get_figma_skill` | Figma's own guidance, read before the first write: the index at `skill://index.json`, then the `figma-use` and `figma-use-slides` skills and the slides references the index and the skill link (gotchas, lifecycle, grid, content). This skill does not restate them. |
| `upload_assets` | Image fills for the document's images: one upload URL per image, posted from the shell. |
| A shell with Node.js and npm | Reading the PDF (a PDF library and a canvas package installed in the scratch folder), cropping images, posting uploads. |
| Write access to the deck | Writing through the server needs a paid Full seat (Figma MCP server, checked 2026-10). It shows at the first write, in phase 5: a write that fails with a permission error stops the run with that message, and nothing is probed before. |

Check the tools before the first message. Without the Figma server, stop and ask the user to connect it; without a shell, stop and say that the document cannot be read. `get_metadata` does not work on Slides files: read the deck with `use_figma` only. Optional: `get_screenshot` for a slide the user wants to see at a chosen size; inline screenshots inside `use_figma` cover the run. How these tools behaved in this skill's own phases is in [tool-notes.md](references/tool-notes.md); read it before phase 3.

## Inputs

| Input | Source |
|---|---|
| Document | A PDF: a path, or a file the user attaches. Another format is exported to PDF by the user first. Asked only when missing. |
| Deck | A Figma Slides link; the file key is the segment after `/slides/` or `/deck/`. Asked only when missing. |
| Protected slides | Derived, never asked: every slide that existed before the run, and any slide the user edits during the run (they say so, or its children no longer match what the run wrote). |
| Base body size | Derived: the body size measured on the deck's content slides ([deck-spec.md](references/deck-spec.md) "The body size"). The user may set one ("make the base 22"); then the scale is rebuilt from it. |
| Type scale | Derived from the base: title, lead, heading, sub-heading, body, caption; the deck's own sizes for the roles it has, steps from the base for the rest. |
| Fonts | Derived: the deck's families and styles when the font list says they load; else the closest family that loads, said at the plan checkpoint. |
| Where the slides go | Derived: a new row after the last existing row, named after the document. |
| Line breaks | Derived: the document's own, written as explicit breaks. A line that does not fit its box at the deck's size is re-broken by the agent at a space, as deck-spec.md "Text" says; the margins and the card padding win over a kept break. |

## Workflow

Each phase produces a named artifact, written in a scratch folder outside any repository; the delivery says where. Phases stop only at the two checkpoints.

### Phase 1: Intake

Produces the **intake record**: the document, the file key, the scratch folder, the tools found, and the deck's slide grid as it is now.

1. Both inputs in the request: say in a line what happens next and go on. One missing: ask for it and stop. "Which document and which deck? A PDF path and the deck's link."
2. Load Figma's guidance with `get_figma_skill`: the index, `figma-use`, `figma-use-slides`, and that skill's references for gotchas and the slide lifecycle. Pass the skill names in `use_figma`'s `skillNames` as the guidance says.
3. Install the PDF reader in the scratch folder, and run every script from that folder as the working directory ([document-reading.md](references/document-reading.md) "Setup").
4. List the slide grid with a read-only `use_figma` script: rows with their names, slides with id, name and child count. Every slide in that listing is protected; the audit compares against it.

### Phase 2: Read the document

Produces the **content map** and the **assets folder** ([document-reading.md](references/document-reading.md); the map's shape in [content-map.example.json](assets/content-map.example.json)).

1. Extract every text run with its font size, position and end-of-line flag, page by page; group runs into lines and lines into blocks; rank the sizes on each page and across the document into hierarchy levels (title, lead, heading, sub-heading, body, caption, page furniture) by document-reading.md "Hierarchy levels"; a bold run at the body size is a label inside its body block, not a level. Keep the document's line breaks in each block's text.
2. Render each page to an image and read it: assign each page a **layout type** from the catalogue in document-reading.md (cover, lead and cards, tiles with descriptions, numbered rows, device mockups with captions, timeline, two columns, closing), and note which blocks go into which region.
3. Extract the images (logos, mockups, photos): embedded images where the PDF has them, crops of a high-resolution page render otherwise; make page-colored margins transparent so that a crop does not show as a box on a colored slide.

### Phase 3: Read the deck

Produces the **deck spec** ([deck-spec.md](references/deck-spec.md); the JSON shape in [deck-spec.example.json](assets/deck-spec.example.json)).

1. From the intake record's grid, take the content slides: every slide with running text below a title (deck-spec.md "Which slides to measure").
2. Measure them as deck-spec.md says: slide size, content margins, the title group (bar, title, subtitle, each with position and size), the body size, line height and color, the bullet mark (size, color, opacity, gap to text, offset from the first line's top), cards (fill, radius, shadow), tiles and accent shapes, the page-number treatment, and each text style combination with the slides it appears on.
3. List the fonts in use and check which load (deck-spec.md "Fonts"); record the substitution for any that do not.
4. Screenshot two representative content slides inline, to see what the numbers describe.

### Phase 4: Slide plan

Produces the **slide plan** and the first checkpoint.

1. One slide per page, in the document's order: the page's layout type, the deck's layout that carries it (an existing slide's layout re-created at its coordinates where one matches the type, else the spec's parts composed as deck-spec.md "Layouts" says; a protected slide is never cloned), the blocks it holds and their hierarchy levels, the images it places, and the expected count of each element role (marks, cards, numbers, captions) that the audit will check.
2. The type scale from the base: the deck's sizes for the roles the deck has; a step down the deck's own ratios for the rest; line heights from the spec. A layout taken from a slide that holds fewer items than the page does gets its type one step down and its spacing refitted, before it is built.
3. The fit of each slide, estimated from line counts: each block's lines times its line height in pixels, plus the spec's gaps and paddings, against the content height. A page that does not fit at the scale is split into two slides that carry the same title, at a block boundary, and the plan says so; the type is not shrunk below the scale for it.
4. The **preamble** for the build: the spec as a constants object, the font loading, the helpers of deck-spec.md "The preamble", every spec value read from the object and none typed into a slide.

Checkpoint, in plain words: the page-to-slide list with each layout type and any split; the scale (base, and each role's size); the font substitution if any; the row the slides go in; that existing slides stay. "OK" builds.

### Phase 5: Build

Produces the **slides**.

1. Create the row and the slides with the lifecycle guidance, re-reading the grid at the start of every call; move a slide that landed in another row with the row's `appendChild` (tool-notes.md "Slide rows").
2. Build three to five slides per `use_figma` call, each call starting with the preamble verbatim. Every node gets a name that says its role (`Title bar`, `Card`, `Bullet bar`, `Number`, `Caption`): the audit counts by name, and a later call addresses nodes by name, never by a size or font filter (tool-notes.md "Addressing nodes"). A slide itself keeps no name (Figma numbers slides), so a slide is found by its row and its index in it.
3. Text is created as deck-spec.md "Text" says: the characters with the document's breaks, the width set first and the auto-resize set to height after it, the vertical position computed from the box's height only after that order.
4. Upload the images with `upload_assets`, one node per image, and post the files one after another (tool-notes.md "Uploads").
5. Return the created node ids and each slide's child count from every call; screenshot the first batch's slides inline before the next batch.

### Phase 6: Audit

Produces the **audit report** and the second checkpoint ([audit.md](references/audit.md)).

1. Numeric, over every new slide: content edges within the deck's margins; the inventory of each element role by node name with one spec each and its count; the table of text style combinations against the scale; the overflow and overlap check from Figma's guidance; every text box's height against its font size (a collapsed box is repaired, tool-notes.md "Text sizing").
2. Visual: a full screenshot of every new slide, and a zoomed render of one instance of each element role (a bullet row, a numbered row, a title group, a timeline node, a caption) at three to four times, read for the glyphs against the mark or the shape they align with.
3. Fix what fails by the verdicts below and run both parts again, until nothing fails. A fix to one element role is applied to every instance on every new slide.

Checkpoint: every new slide's screenshot, saved from the inline render into the scratch folder and attached to the message (or its `get_screenshot` link where the host shows no files), the inventory (roles, specs, counts), the margins, and anything the verdicts accepted with a change. "OK" delivers. A correction from the user is applied to every new slide and the audit runs again.

### Phase 7: Deliver

In one message: the deck link and the row; the slides, one line each; the scale and the spacing used (base, each role's size, margins, card padding, list gap, the mark's size and gap); the font substitution; the slides left untouched; what was not verified (a page whose layout type was a guess, an image that was cropped by hand). The content map, the deck spec and the audit report stay in the scratch folder.

## Verdicts

Read before every build and every fix.

| Result | Verdict |
|---|---|
| A word of a script without spaces (Korean, Japanese, Chinese) wrapped mid-word | Redo: the document's break as an explicit break; when that line does not fit its box at the deck's size, the box widened up to its region's width, then the line re-broken at a space by the agent |
| Text closer to a card's edge than the card padding, or outside it | Redo: re-break the text at a space, or make the card taller; padding holds on all four sides and wins over a kept break |
| A page's content does not fit one slide at the scale, with the spec's gaps and paddings | Accept with a change: two slides with the same title, split at a block boundary, said at the plan checkpoint; the scale is not shrunk for it |
| An element role with more than one spec in the inventory | Redo: every instance to the spec, and the count checked again |
| A glyph more than one pixel off the center of its mark or shape at three to four times zoom | Redo: measure the glyph box, move the text or the mark |
| A text box whose height is below its font size with auto-resize off | Repair: width first, auto-resize to height after it, position recomputed |
| A layout copied from an existing slide holds more items and reads oversized | Accept with a change: the type one step down, the spacing refitted, said at the checkpoint |
| A content edge outside the deck's margins, a page number included | Redo |
| A slide the user edited during the run | Accept: left as it is, named in the delivery |

## Hard rules

1. Every spec comes measured from the deck's existing slides. A size, a color, a radius, a gap or a shadow that the deck does not have is derived from the deck's own ratios, never from a generic preference: a foreign element is the first thing the user sees.
2. One spec per element role across every new slide, proven by the inventory count before the checkpoint. Marks, lines and gaps drift between batches unless they are counted.
3. Alignment is judged on rendered glyphs at zoom, never on box coordinates alone. A collapsed or padded text box centers wrong while its numbers look right.
4. A slide that existed before the run, or that the user edited during it, is not rebuilt, moved or deleted. A rebuild touches only what this run made.
5. Every break is explicit: the document's where it fits, the agent's at a space where it does not. A wrap of a script without spaces is never left to the renderer, which breaks mid-word; the margins and the padding win over a kept break.
6. Nothing is spent and nothing is deleted. The server's writes cost no credits; the seat is the user's.

## Terminology

| Term | Meaning |
|---|---|
| Content map | The document read into pages, blocks with hierarchy levels and breaks, images, and a layout type per page. |
| Layout type | The spatial shape of a page, from a fixed catalogue; the handle the plan uses. |
| Deck spec | The measured design system of the existing slides, as a JSON object the preamble reads. |
| Element role | What a node is for (title bar, card, bullet bar, number, caption), carried in its name. |
| Preamble | The constants, font loading and helpers pasted at the top of every build call. |
| Base body size | The size of running text; every other size is a step from it. |
| Protected slide | A slide that existed before the run, or that the user edited during it. |
| Inventory | The count of specs per element role over the new slides; passes at one spec each. |
| Glyph box | The ink of a text node as rendered, against which alignment is judged. |
| Collapsed box | A text node resized after its auto-resize was set, left a few pixels tall with auto-resize off. |
