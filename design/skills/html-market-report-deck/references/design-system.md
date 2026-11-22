# The look of an issue: the brand's tokens, the frame, the deck file

How the look is read from the brand's site, what the series' frame adds to it, how the deck's one file is written, and what the helper reports. Read before phase 1, and again at the build.

## Reading the brand's site

Phase 1 writes `brand.md` in the series folder from the site itself, never by eye from memory.

- **Capture.** The first screen and each main section, at a fixed viewport and with reduced motion requested, so that what a scroll would reveal is in the picture ([headless.md](/docs/browser/headless.md) "Screenshots"; [tool-notes.md](tool-notes.md) has two things a capture met). The captures stay in the scratch folder: they are what the look is checked against, not material for a slide.
- **Tokens.** Read from the root element's custom properties and the computed styles of a section, a card and a heading: the ground's colours (most sites have two, the ground and a lifted tone), the text colour and its muted tone, the accent, a second accent where the site has one, the one colour it keeps for a small point, the radius, the card (its fill, its border), and where the ground is lit.
- **Fonts.** The site's family by its local name first, then its documented web file saved under `library/fonts/` ([rendering-html.md](/docs/browser/rendering-html.md) "Fonts"). A serif for the masthead is one the brand already uses, else one plain system serif.
- **`brand.md`** names each token with its value and where on the site it was read, the fonts with their files, and in a line each: how the site builds a card, how it lights its ground, how it writes a section head. The skeleton's `:root` takes these values under its own names.

## What the series' frame adds

The site gives the ground, the surfaces, the colours and the type. The series adds a frame in a magazine's manner, four things and no more: the masthead (the name in the serif, the issue's period beside it), the cover's lines, the contents slide, and the foot mark on every slide (the name in the serif, the period in the mono). A slide between them looks like a page of the brand's site that happens to hold a chart.

## Colour and emphasis

- One ground with its light, on every slide but the plates. A plate, the light ground, carries one or two slides an issue where a chart reads better dark on light.
- The surfaces are the site's cards. One card a slide may be lit (`.hero`): the one the title speaks of.
- One accent. About one figure a slide takes it, the one the title names; everything else is the text colour or its muted tone.
- The point colour marks a dot or a single small mark, never a block.
- A fall, a loss or a "no" is drawn in the muted tone, not in red or amber: a warning colour turns a page of data into a dashboard.

## Type

- The brand's font everywhere. The serif stands in the masthead and the foot mark alone.
- The mono face is for page numbers, the period and figures on a scale. Text in a script the mono face lacks (Hangul, for one) is never set in it: it falls to a system face at the mono's wide spacing.
- A title is two lines, broken by hand where a person would pause. Blocks of a few lines are balanced (`text-wrap: balance`, which the skeleton sets on the title and the captions): in a Chromium-family browser it left no one-word last line in English or in Korean set to break at spaces, where `text-wrap: pretty` left most Korean blocks as they were (Chrome, checked 2026-11).

## The frame of a slide

Every slide between the covers has the same four fixed things, which the skeleton holds: the header at the top left (the section, in a few words), the title under it, the foot mark at the bottom left, the page number at the bottom right. The scene takes the field between: from 340 to 960 pixels down, 96 pixels in from each side. A scene whose figure is the title (`giant-figure`) puts its sentence where it reads best and has no second title.

The cover has the masthead and the period on one line with a rule under them, the cover story as the largest type of the issue, three cover lines (a figure, its small figure, a line of words), and the screens of the apps the issue shows as a collage that runs off the right edge. The back cover is centred: the masthead, the question the issue leaves, the contact.

## The deck file

`deck.html` starts as [`issue-skeleton.html`](../assets/issue-skeleton.html), or as the last issue's `deck.html`, and is one file: the meta, one stylesheet, one `section.slide` a slide.

- **The canvas.** A slide is 1920 by 1080 CSS pixels with `overflow: hidden`, and every direct child of a slide is placed in the slide's own pixels (`.slide > *` is `position: absolute`).
- **What is shared.** The tokens, the slide box, the plate, the header, the title, the foot mark, the page number, the card, the lit card, the figure face and the caption. Everything else belongs to one slide.
- **A prefix a slide.** One stylesheet holds every slide, so every class of a scene carries that slide's prefix of a letter or two (`c-` on the cover, `m-` on the map). Two slides built from one scene file take two prefixes.
- **`data-pattern`** on the section is the scene's name from the plan. **`data-bleed`** marks an element meant to run past the slide's edge, **`data-clip`** one whose content is meant to be cut by its box, **`data-count="N"`** a drawing of counted units, which must hold N element children.
- **`deck-meta`**, the JSON script in the head: `canvas`; `banned`, the phrases a render reports on any slide; `pdf_max_mb`, 10 unless the user sends the file somewhere with a lower limit; `style` only where the house style differs from the usual set, in the keys [house-style.md](/docs/writing/house-style.md) "How it is checked" gives.
- **Assets** are referenced by a relative path into the library (`../library/logos/<file>`); the helper embeds each in the one-file HTML and stops on a path that is not there.
- **Backgrounds.** The slide's light is one plain gradient, never a blurred shape. A pattern that repeats (dots, a grid) is a few SVG shapes where the slide needs them, never a repeated CSS gradient across every slide ([tool-notes.md](tool-notes.md) "A PDF that is too large").

## The helper's findings

`node render.mjs <deck.html> <out folder> --name <file name>`, with `PLAYWRIGHT_FROM` set where `playwright-core` is borrowed. It exits 0 with no finding, 1 with findings (every file is still written, for a look at a draft), 2 when it cannot run, with the reason. Its first line names the PDF's size and the fonts that loaded; "none" means every slide fell to a system face.

| Finding | Means | Fix, in `deck.html` |
|---|---|---|
| `outside` | An element reaches past the slide. | Move or shrink it; `data-bleed` only where it is meant. |
| `cut` | Text longer than its box. | Fewer words or a larger box; `data-clip` only on a screen in its frame. |
| `lone` | A block's last line is one word. | Reword, break by hand, or balance the block. |
| `repeat`, `pattern` | Two slides in a row declare one scene; a slide declares none. | Another scene for one of them, in the plan first. |
| `count` | A `data-count` drawing does not hold its count. | Draw the count the figure says. |
| `style` | A character the house style bans. | Rewrite within the house style. |
| `banned` | A phrase of the banned list. | Rewrite the sentence; the phrase stays listed. |
| `heavy` | The PDF is over `pdf_max_mb`. | tool-notes.md "A PDF that is too large". |
| `unstable` | A slide's image did not settle. | Take out what moves; an issue is still. |

A `fallback` note names text partly rendered in a face its stack does not name; it is no finding. The checks measure boxes, words and counts: they do not see two labels that overlap, an axis title off its arrow, or a chart that says something other than its figure.
