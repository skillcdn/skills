# Layout and rendering

What `scripts/render.py` does, written so that the HTML can be produced by hand when the helper cannot run, and so that a reviewer knows what a correct render looks like.

## Page

- One slide is one page of 13.333in by 7.5in (16:9, the size of a widescreen presentation). The CSS declares `@page { size: 13.333in 7.5in; margin: 0; }` and every `.slide` has that width and height, `overflow: hidden`, and `break-after: page`.
- Content lives inside a frame 0.55in from the left and right edges, 0.42in from the top and 0.45in from the bottom.
- The background is a light gradient (white to a pale tint, 155deg). The closing page is solid navy.
- The HTML is one self-contained file: the stylesheet inline, the logos as data URLs, the font loaded from the URL in `theme.font_css` with a system fallback. Nothing else is fetched.

## Theme defaults

| Token | Default | Used for |
|---|---|---|
| `navy` | `#22408E` | Titles, card headings, number discs, the closing background |
| `steel` | `#7089BF` | The accent bar beside the title, tick marks, option chips |
| `ink` | `#2A3242` | Body text |
| `mute` | `#5A6478` | Secondary text, notes, row descriptions |
| `tint` | `#E7EDFA` | Banners, pale step labels, diagram nodes |
| `tint2` | `#D9E2F6` | Chips, cover stripes |
| `line` | `#E2E8F5` | Card borders |
| `pale` | `#BFD0EC` | Timeline rails, the second step label |
| `font` | `Pretendard`, falling back to the system's Korean-capable sans | All text |

Read the organization's own values from its brand file, website stylesheet or a previous deck; write them into `meta.theme`. Keep the roles: a theme is the colors, not a new layout.

## Type scale

| Element | Size | Weight | Color |
|---|---|---|---|
| Cover title | 40pt | bold | navy |
| Slide title | 26pt | bold | navy |
| Slide subtitle | 15.5pt | bold | dark gray `#3A4356` |
| Card title | 15pt | bold | navy |
| Card body, bullets | 12.5pt to 14pt | regular | ink |
| Row title | 13.5pt | bold | ink |
| Row description | 12pt | regular | mute |
| Step label | 14.5pt | bold | white on steel or navy, navy on tint |
| Timeline phase title | 16pt | bold | navy |
| Note | 10.5pt | regular | mute |

## Block markup

- **Header**: a 5.5pt-wide vertical bar in steel, 0.5in tall, to the left of the title; the subtitle below. An optional tag chip at the top right (navy with white text, or tint with navy text).
- **cards**: a CSS grid with `cols` equal columns and a 0.25in gap; each card white, 1px `line` border, 0.09in radius, 0.22in by 0.25in padding.
- **banner**: a tint band, 0.16in radius, the lead in bold navy followed by the body on the same line.
- **bullets** (ticks): a list without markers; each item begins with a steel "|" and two spaces, then the head in bold navy, then the body.
- **rows**: each row a white rounded box (0.14in radius) laid out as a grid of number disc (0.34in, navy; steel for an option), title column (3.1in), description, and an optional chip.
- **stack**: a grid of three columns (3in label, 5.6in description, the rest for the aside). Labels take, from the first step down, tint, pale, steel, navy (the last color repeats); text is white on steel and navy. The aside spans every row.
- **timeline**: one column per phase with a 3.5pt rail in pale at its left; each entry has a navy disc on the rail, the `when` line in steel, the title in navy and tick items below.
- **qa**: "Q. " and the question in 16pt navy, the answer below in 12.5pt.
- **split**: a two-column grid, the left width from `left_w`; bullets on the left; on the right either screenshot frames (a pale box with a steel border, the label and caption centered) or the diagram.
- **diagram**: a white rounded panel holding a grid of five columns (1.35in, 0.45in, flexible, 0.45in, 1.35in) and five rows (node, arrow, node row, arrow, node). The service node sits above the center with a vertical double arrow between them, the source at the left with a right arrow into the center, the output at the right with a right arrow out of the center, the update node below with an up arrow. Node titles 12.5pt, bodies 10.5pt; the accent node is navy with white text. Edge labels sit beside their arrows in mute.
- **note**: absolutely positioned 0.12in from the page's bottom edge, inside the side margins.
- **cover**: four rotated stripes at the top right (tint2, pale, steel, tint), the title block at 0.95in from the left and 2.5in from the top with a short steel rule above it, the subtitle below, the logo at 6.05in from the top and the client, date and brand footer at 6.6in.
- **closing**: navy page, the title at 2.7in, the contact lines at 4.1in in a pale blue, the white logo at 6.5in.

## Printing

- Print with a Chromium-family browser: page width 13.333in, height 7.5in, background graphics on, the CSS page size preferred. Wait for the network to go idle and for `document.fonts.ready` before printing, or the font falls back.
- A page that overflows prints a cut: the fix is in the deck file (fewer items, a shorter `row_h`, a split slide), never in the CSS.

## Review

Rasterize each page small (about 55 dpi) and tile them three per row into one image. Look for: cut text at the bottom of a page, a block pushed below the note, a diagram whose nodes wrap into three lines, a timeline column with more items than the others by far, an empty right half on a split. Then open any suspect page at about 80 dpi.
