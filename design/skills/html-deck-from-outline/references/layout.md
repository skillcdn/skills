# Layout and rendering

What `scripts/render.py` does, written so that the HTML can be produced by hand when the helper cannot run, so that a reviewer knows what a correct render looks like, and so that the measurements the helper reports can be made without it.

## Page

- One slide is one page of 13.333in by 7.5in (16:9, the size of a widescreen presentation). The CSS declares `@page { size: 13.333in 7.5in; margin: 0; }` and every `.slide` has that width and height, `overflow: hidden`, and `break-after: page`.
- Content lives inside a frame 0.55in from the left and right edges, 0.42in from the top and 0.45in from the bottom (0.55in in a report, above its footer).
- Proposal: the background is a light gradient (white to `tint`, 155deg); content slides carry a two-digit page number at the lower right (0.5in from the right, 0.26in from the bottom, 9.5pt, `faint`). Report: the background is white; a footer line sits 0.22in from the bottom with the brand, the document's name and the date at the left, separated by vertical bars, and the page number at the right, all 9pt `faint`. The closing page is solid navy in both.
- Text breaks at spaces, never inside a word (`word-break: keep-all` with `overflow-wrap: break-word` as the fallback for a string longer than its box).
- The HTML is one self-contained file: the stylesheet inline, the logos, marks and photographs as data URLs, the font loaded from the URL in `theme.font_css` with a system fallback. Nothing else is fetched.
- Every block's root element carries `data-path` with its path in the deck file (`$.slides[3].blocks[0]`), and every slide `data-slide` with its number: the layout report names findings by them.

## Theme

| Token | Default | Used for |
|---|---|---|
| `navy` | `#22408E` | Titles, statements, number discs, bars, a report's header rule and cover panel, the closing background |
| `accent` | the value of `steel` | The proposal's bar beside the title, a report's section label, ticks, arrows, arrowheads, the statement lead, the KPI bar, a timeline's `when` |
| `steel` | `#7089BF` | A mid tone of the navy hue: the stack's third tone, the fourth cover stripe, an option's disc |
| `ink` | `#2A3242` | Body text, fact values, profile names, table cells |
| `mute` | `#5A6478` | Subtitles, fact labels, descriptions, edge labels, captions |
| `tint` | `#E7EDFA` | Diagram nodes, pale step labels, the first Gantt tone, the table header, the KPI tag |
| `tint2` | `#D9E2F6` | Chips, the first cover stripe |
| `line` | `#E2E8F5` | Panel borders, list rules, Gantt month lines, table row rules |
| `pale` | `#BFD0EC` | The loop ring, the diagram frame, timeline rails, the cover's logo separator, the closing's contact lines, a report cover's labels |
| `rule` | `#C9D1E3` | The thin rules of definition lists, the contents and the Gantt header, the borders of loop nodes, profile row rules |
| `faint` | `#8A94A8` | Page numbers, the footer |
| `font` | `Pretendard`, falling back to the system's Korean-capable sans | All text |

Read the organization's own values from its brand file, website stylesheet or a previous deck; write them into `meta.theme`. Keep the roles: a theme is the colors, not a new layout.

### Deriving a theme from one color

With one brand color, the organization's primary, `navy` is that color, and the tinted tokens keep its hue and take these lightness and saturation values (HSL, rounded): `steel` 60% and 38%, `pale` 84% and 51%, `rule` 84% and 32%, `tint2` 91% and 62%, `line` 92% and 49%, `tint` 94% and 66%; these are the defaults' own values, so a brand whose primary is the default navy gets the defaults back. `ink`, `mute` and `faint` stay neutral unless the brand has its own grays. A second brand color, where the brand has one, is `accent` and nothing else: written into `steel` it enters the stack's tone sequence and a cover stripe and reads as emphasis where none is meant. Write the derived values into `meta.theme`, so that the deck file carries the theme and a later run edits it there. Text on a filled label is white or navy by the fill's luminance, never by its name.

## Marks

Icons: the line icons a block's `icon` field may name are `file`, `layers`, `search`, `cpu`, `code`, `clipboard`, `check`, `refresh`, `users`, `calendar`, `lock`, `download`, `laptop`, `bolt`, `target`, `gear`, `edit`, `clock`, `flag`, `server`. Logos and symbols are image files embedded as data URLs: PNG, JPG or SVG. A wordmark is 0.4in tall in a brand panel head and on a proposal cover (the client's 0.4in, the presenter's 0.36in), 0.36in on a report cover; a symbol is 0.46in tall beside a product name; a mark beside a fact is 0.32in square; a mark on a diagram node or at a loop's center is 0.34in to 0.4in tall. A mark is never recolored; a colored mark sits on white, so the node that carries marks is white with a navy border (`strong`), not navy.

## Type scale

| Element | Size | Weight | Color |
|---|---|---|---|
| Cover title (proposal; report) | 50pt; 40pt | bold | navy; white |
| Cover tagline; report kind label | 16pt; 12pt | regular; bold, tracked | mute; pale |
| Closing title | 44pt | bold | white |
| Slide title (proposal; report) | 26pt; 24pt | bold | navy |
| Section label (report) | 10.5pt, tracked | bold | accent |
| Slide subtitle | 14pt | regular | mute |
| Statement | 16pt to 22pt | bold | navy, the lead in accent |
| Statement body | 13.5pt | regular | ink |
| Fact label, fact value | 11.5pt, 14pt | regular, semibold | mute, ink |
| Inline fact label, value | 11.5pt, 12pt | regular, medium | mute, ink |
| Numbered title, description | 13.5pt, 11.5pt | bold, regular | ink, mute |
| Contents number, title, line | 20pt, 14.5pt, 11.5pt | bold, bold, regular | accent, ink, mute |
| Table header, cell; note | 11.5pt, 11.5pt; 9.5pt | bold, regular | navy, ink; mute |
| KPI value, unit, label, tag | 30pt, 14pt, 12pt, 9.5pt | bold, semibold, regular, bold | navy (white on the navy tone), ink, mute |
| Loop node title, sub; center caption | 12.5pt, 10pt; 10.5pt | bold, regular; regular | navy, mute; ink |
| Brand name, tagline, fact, items | 21pt, 12.5pt, 12pt, 12pt | bold, regular | ink |
| Row title, description | 13.5pt, 12pt | bold, regular | ink, mute |
| Gantt row label, sub, month, bar text | 13pt, 10.5pt, 11.5pt, 11pt | bold, regular, bold, regular | ink, mute, navy, white or navy |
| Process strip label; detail tile step, when, title, sentence | 11pt; 9.5pt tracked, 10.5pt, 13.5pt, 10.5pt | bold; bold, regular, bold, regular | ink; accent, mute, navy, ink |
| Diagram node title, body | 13.5pt, 11pt (full width) | bold, regular | ink, white on an accent node |
| Profile name, title | 21pt, 10.5pt | bold, regular | ink, mute |
| Profile row label, lines | 13pt, 12.5pt | bold, regular | ink |
| Photo caption, credit | 11pt, 9pt | regular | mute, faint |
| Page number, footer | 9.5pt, 9pt | regular | faint |

## Block markup

- **Header** (proposal): a 5.5pt-wide vertical bar in the accent, 0.5in tall, to the left of the title; the subtitle below in regular muted type; an optional tag chip or logo at the top right; 0.3in of space below. **Header** (report): the section label above the title, the title, the subtitle, then a 1.5pt navy rule across the frame's width, 0.28in of space below.
- **Body**: a column of blocks with 0.26in between them, under the header. With `valign: "center"` the column is centered in the remaining height.
- **columns**: a CSS grid with the declared `widths` and gap; each column holds one block; `stretch` makes the columns equal height.
- **statement**: the lead in bold accent, then the text in bold navy at the declared size with a line height of 1.42 and slightly tight tracking; an optional paragraph under it at 13.5pt with a line height of 1.6.
- **facts**: a definition list; each row a grid of label column (`label_w`) and value, 0.13in of padding, a 1px rule above each row and below the last. Inline: the rows side by side, label above value, one rule above the whole row.
- **numbered**: each item a grid of a 0.3in navy disc with the number and a text column (title bold, description muted), 0.1in of padding, a 1px rule above each item and below the last.
- **toc**: a grid of `cols` columns filled column by column, 0.6in apart; each entry a grid of a 0.75in number column and the text, 0.14in of padding, a rule under each entry and above the first of a column.
- **table**: full width, collapsed borders; the header row on tint with navy bold text, 0.1in by 0.14in of padding; every cell the same padding with a 1px rule below; the first column bold when `first_col` says; the note under the table at 9.5pt muted.
- **kpi**: a grid of `cols` white panels (0.12in radius, 0.26in by 0.3in padding) each a column of the value with its unit (the unit small, semibold), the label sentence, the tag as a tint chip at the left, and, when `bar` is set, a 0.09in track in `line` with the ratio filled in the accent; the navy tone fills the panel navy with white type and translucent white for the chip and the track.
- **photo**: a frame with 0.12in radius and the image covering it (or contained, per `fit`) at the declared height, the caption under it at 11pt muted and the credit at 9pt faint.
- **loop**: a box of `width` by `height` holding an SVG ring (radius `r`, 3 units in pale) with four accent arrowheads at the diagonals pointing clockwise; four white nodes (1px border, 0.1in radius) centered on the ring at the top, right, bottom and left, `node_w` wide; the center caption `center_w` wide with the marks in a row (0.4in tall) above the caption lines. With `width` 4.6in, `height` 4.0in, `r` 1.45in, `node_w` 1.3in and `center_w` 1.45in the nodes and the caption do not touch.
- **brand**: a white panel (0.12in radius, 0.32in by 0.38in padding) with a head row 0.52in tall (the wordmark 0.4in tall, or the symbol 0.46in tall beside the name at 21pt), one line at 12.5pt, a fact list between two rules (each fact a 0.32in mark and its text at 12pt), then tick lines at 12pt.
- **rows**: each row a white rounded box (0.14in radius) laid out as a grid of number disc (0.34in, navy; steel for an option; a 0.08in accent dot when `numbered` is false), title column (3.1in), description, and an optional chip.
- **steps**: a flex row with an accent arrow between items; all items share the width equally. Pills: white with full radius and a 1px border, a 0.3in navy disc with the number, the label. Tiles: white rounded boxes (0.14in radius) with the number disc on the first line and the label centered below. Detail tiles: left-aligned boxes with "STEP n" tracked in the accent, the when in mute, the label bold in navy, the sentence at 10.5pt; the block's `facts` under the strip as an inline definition list.
- **diagram** (full width): a dashed frame (1.5pt, pale, 0.16in radius) with its label as a tint chip overlapping the top left edge and an optional note chip at the top right. Inside, a grid of five columns (2.6in, 0.75in, flexible, 0.75in, 2.6in) and three rows (service node, 0.5in arrow row, main row). The service node is centered above the center node at `mid_w` wide with a vertical double arrow; the source is at the left with a right arrow into the center; the output at the right with a right arrow out of the center. Below the frame a second grid with the same columns holds an up arrow (0.45in row) and the update node, `mid_w` wide, centered under the center node. A node's marks sit in a row above its title (0.34in tall); step chips are 0.24in navy discs above them; a `strong` node is white with a 2pt navy border, an `accent` node navy with white text. Edge labels sit beside their arrows in mute.
- **gantt**: a two-column grid, 2.9in for the labels and the rest for the tracks. The header row holds the month labels in navy over a 1px rule; every track is 0.6in tall with a 1px line at each month boundary. The label column holds the label and, under it, the sub line. A bar is 0.36in tall with full round ends, positioned by percentage of the track; its tone is tint, pale, steel or navy. A milestone is a navy 0.22in square rotated 45 degrees on the date, with its text in bold navy at its left; where the row's bar ends at the date or spans it, the text sits at the diamond's right instead, so that it never crosses the bar's text.
- **profiles**: a grid of `cols` white cards (0.14in radius, 0.36in by 0.45in padding). The head is a 0.8in ring (2pt ink) with the initial at 22pt, then the name at 21pt and the title in small muted type with letter spacing. Each row is a 0.85in label column and a lines column; every line has a 1.5pt light rule at its left and 0.16in of padding.
- **timeline**: one column per phase with a 3.5pt rail in pale at its left; each entry has a navy disc on the rail, the `when` line in the accent, the title in navy and plain tick lines below.
- **stack**: a grid of three columns (3in label, 5.6in description, the rest for the aside, or the block's own `cols`). Labels take, from the first step down, tint, pale, steel, navy, one hue; the text on each is white or navy by the fill's luminance. The aside spans every row.
- **cards**: a grid of white cards (0.1in radius, 0.26in by 0.3in padding); with `numbered` a 0.42in navy disc with the number above the title and no icon; else an optional icon disc above or beside the title. **banner**, **stats**, **bullets** (ticks), **qa**, **split**, **shots**, **note**: as deck-spec.md "Blocks" defines them. These are the blocks the design floor limits.
- **cover** (proposal): four rounded stripes rotated 40 degrees at the upper right (centers, widths and lengths in inches: 5.3/0.85 0.9×2.4 tint2, 9.3/2.1 0.85×6.1 line, 8.7/4.2 1.05×6.2 tint, 9.9/4.7 0.75×3.1 steel), the title block 0.75in from the left and 2.05in from the top (50pt, two lines), the tagline 0.35in below it, the logos in a row 0.75in from the left and 5.5in from the top (the client's logo 0.4in tall, a 1px rule, the presenter's logo 0.36in tall, 0.3in apart), and, with `footer`, the client, date and brand line (or the given line) at 6.2in. **cover** (report): a navy panel 7.4in wide over the page's full height with 0.75in of padding, the white mark at its top left (0.36in tall; the brand in white type without one), the kind label tracked in pale, the title in white at 40pt, the tagline in pale, and the meta rows as a two-column list (1.2in labels in pale, values in white) at the panel's foot; the photograph covers the rest of the page, or the stripes sit there without one.
- **closing**: navy page; the title centered at 2.75in from the top; the white logo centered at 5.15in, 0.3in tall; the contact lines centered at 5.65in in a pale blue, 12pt.

## Printing, the layout report and the contact sheet

- Print with a Chromium-family browser at 13.333in by 7.5in, background graphics on, the CSS page size preferred, after the network went idle, `document.fonts.ready` and about 300 milliseconds for images, as [rendering-html.md](/docs/browser/rendering-html.md) "PDF at a declared page size" and [headless.md](/docs/browser/headless.md) "PDF" say; without the wait the font falls back. The helper takes the first route the host has: Playwright from Python; Node.js with `playwright-core`, borrowed through `PLAYWRIGHT_FROM` (the `package.json` of a project that has it) or installed once into a tools folder in the user's cache (`DECK_TOOLS`, else `html-deck-tools` under the local application data folder on Windows or `~/.cache` elsewhere); the installed browser's own `--print-to-pdf`. It prints which it took.
- A page that overflows prints a cut: the fix is in the deck file (fewer words, fewer items, a split slide), never in the CSS.
- **The layout report** (`--report <json>`) measures the rendered page in the browser before the PDF is printed, and names each finding by the block's `data-path`: a block or a header beyond the page or below the content frame, text cut inside a box, two text elements whose boxes overlap, a title or a list item whose last line is one word alone, a fact value, a row title, a KPI value, a Gantt bar text or a stack label that wraps, and a content slide whose blocks use less than the fill threshold of the body's height (0.5 by default, `--fill` sets it; a lower half left empty is what the floor rejects; the contents slide is exempt). It needs a driver (Playwright from Python or Node); with the bare browser alone it is skipped with a message, and the review says so. By hand, the same measurements come from `getBoundingClientRect` on every `[data-path]` element and on the text leaves of a slide, and from `Range.getClientRects` for the line boxes.
- **The contact sheet** (`--sheet <png>`) tiles the pages three per row at a small size: from the PDF with PyMuPDF where it is installed; else from the HTML, which the helper lays out three per row with `zoom` into a sheet page beside the PNG and screenshots with the browser route it has. **The look sheet** (`--look <png>`) is the same for the cover and one body slide in each register, two per row with the register as the label, and skips the style check. **One page at full size** (`--page <n> <png>`) is the screenshot of that slide alone, for a closer look.

## Review

Read the layout report first: every finding is fixed in the deck file and rendered again until the report is empty. Then look at the sheet for what the report does not measure: a line broken inside a word, a loop whose center touches its nodes, a diagram whose nodes wrap into three lines, a brand panel whose marks are recolored or on a dark ground, a profile card whose rows run past the card, a photograph cropped into its subject, a section label that is not the contents' entry, a figure without its source or tag, and the design-floor defaults (icon card grids, number tiles, kickers). Then open any suspect page at full size with `--page`.
