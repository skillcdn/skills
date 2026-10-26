# Layout and rendering

What `scripts/render.py` does, written so that the HTML can be produced by hand when the helper cannot run, and so that a reviewer knows what a correct render looks like.

## Page

- One slide is one page of 13.333in by 7.5in (16:9, the size of a widescreen presentation). The CSS declares `@page { size: 13.333in 7.5in; margin: 0; }` and every `.slide` has that width and height, `overflow: hidden`, and `break-after: page`.
- Content lives inside a frame 0.55in from the left and right edges, 0.42in from the top and 0.45in from the bottom.
- The background is a light gradient (white to a pale tint, 155deg). The closing page is solid navy.
- Content slides carry a two-digit page number at the lower right (0.5in from the right, 0.26in from the bottom, 9.5pt, light gray).
- Text breaks at spaces, never inside a word (`word-break: keep-all` with `overflow-wrap: break-word` as the fallback for a string longer than its box).
- The HTML is one self-contained file: the stylesheet inline, the logos and marks as data URLs, the font loaded from the URL in `theme.font_css` with a system fallback. Nothing else is fetched.

## Theme defaults

| Token | Default | Used for |
|---|---|---|
| `navy` | `#22408E` | Titles, statements, number discs, bars, the closing background |
| `steel` | `#7089BF` | The accent bar beside the title, ticks, arrows, arrowheads, the statement lead |
| `ink` | `#2A3242` | Body text, fact values, profile names |
| `mute` | `#5A6478` | Subtitles, fact labels, descriptions, edge labels |
| `tint` | `#E7EDFA` | Diagram nodes, pale step labels, the first Gantt tone |
| `tint2` | `#D9E2F6` | Chips, the first cover stripe |
| `line` | `#E2E8F5` | Panel borders, list rules, Gantt month lines |
| `pale` | `#BFD0EC` | The loop ring, the diagram frame, timeline rails |
| `font` | `Pretendard`, falling back to the system's Korean-capable sans | All text |

Read the organization's own values from its brand file, website stylesheet or a previous deck; write them into `meta.theme`. Keep the roles: a theme is the colors, not a new layout.

## Marks

Logos and symbols are image files embedded as data URLs: PNG, JPG or SVG. A wordmark is 0.4in tall in a brand panel head and on the cover (the client's 0.4in, the presenter's 0.36in); a symbol is 0.46in tall beside a product name; a mark beside a fact is 0.32in square; a mark on a diagram node or at a loop's center is 0.34in to 0.4in tall. A mark is never recolored; a colored mark sits on white, so the node that carries marks is white with a navy border (`strong`), not navy.

## Type scale

| Element | Size | Weight | Color |
|---|---|---|---|
| Cover title | 50pt | bold | navy |
| Cover tagline | 16pt | regular | mute |
| Closing title | 44pt | bold | white |
| Slide title | 26pt | bold | navy |
| Slide subtitle | 14pt | regular | mute |
| Statement | 16pt to 22pt | bold | navy, the lead in steel |
| Statement body | 13.5pt | regular | ink |
| Fact label, fact value | 11.5pt, 14pt | regular, semibold | mute, ink |
| Inline fact label, value | 11.5pt, 12pt | regular, medium | mute, ink |
| Numbered title, description | 13.5pt, 11.5pt | bold, regular | ink, mute |
| Loop node title, sub; center caption | 12.5pt, 10pt; 10.5pt | bold, regular; regular | navy, mute; ink |
| Brand name, tagline, fact, items | 21pt, 12.5pt, 12pt, 12pt | bold, regular | ink |
| Row title, description | 13.5pt, 12pt | bold, regular | ink, mute |
| Gantt row label, month, bar text | 13pt, 11.5pt, 11pt | bold, bold, regular | ink, navy, white or navy |
| Process strip label | 11pt | bold | ink |
| Diagram node title, body | 13.5pt, 11pt (full width) | bold, regular | ink, white on an accent node |
| Profile name, title | 21pt, 10.5pt | bold, regular | ink, mute |
| Profile row label, lines | 13pt, 12.5pt | bold, regular | ink |
| Page number | 9.5pt | regular | light gray |

## Block markup

- **Header**: a 5.5pt-wide vertical bar in steel, 0.5in tall, to the left of the title; the subtitle below in regular muted type. An optional tag chip or an optional logo image at the top right. 0.3in of space below the header.
- **Body**: a column of blocks with 0.26in between them, under the header. With `valign: "center"` the column is centered in the remaining height.
- **columns**: a CSS grid with the declared `widths` and gap; each column holds one block; `stretch` makes the columns equal height (for brand panels).
- **statement**: the lead in bold steel, then the text in bold navy at the declared size with a line height of 1.42 and slightly tight tracking; an optional paragraph under it at 13.5pt with a line height of 1.6.
- **facts**: a definition list; each row a grid of label column (`label_w`) and value, 0.13in of padding, a 1px rule above each row and below the last. Inline: the rows side by side, label above value, one rule above the whole row.
- **numbered**: each item a grid of a 0.3in navy disc with the number and a text column (title bold, description muted), 0.1in of padding, a 1px rule above each item and below the last.
- **loop**: a box of `width` by `height` holding an SVG ring (radius `r`, 3 units in pale) with four steel arrowheads at the diagonals pointing clockwise; four white nodes (1px border, 0.1in radius) centered on the ring at the top, right, bottom and left, `node_w` wide; the center caption `center_w` wide with the marks in a row (0.4in tall) above the caption lines. Geometry: with `width` 4.6in, `height` 4.0in, `r` 1.45in, `node_w` 1.3in and `center_w` 1.45in the nodes and the caption do not touch.
- **brand**: a white panel (0.12in radius, 0.32in by 0.38in padding) with a head row 0.52in tall (the wordmark 0.4in tall, or the symbol 0.46in tall beside the name at 21pt), one line at 12.5pt, a fact list between two rules (each fact a 0.32in mark and its text at 12pt), then tick lines at 12pt.
- **rows**: each row a white rounded box (0.14in radius) laid out as a grid of number disc (0.34in, navy; steel for an option), title column (3.1in), description, and an optional chip.
- **steps**: a flex row with a steel arrow between items; all items share the width equally. Pills: white with full radius and a 1px border, a 0.3in navy disc with the number, the label. Tiles: white rounded boxes (0.14in radius) with the number disc on the first line and the label centered below.
- **diagram** (full width): a dashed frame (1.5pt, pale, 0.16in radius) with its label as a tint chip overlapping the top left edge and an optional note chip at the top right. Inside, a grid of five columns (2.6in, 0.75in, flexible, 0.75in, 2.6in) and three rows (service node, 0.5in arrow row, main row). The service node is centered above the center node at `mid_w` wide with a vertical double arrow; the source is at the left with a right arrow into the center; the output at the right with a right arrow out of the center. Below the frame a second grid with the same columns holds an up arrow (0.45in row) and the update node, `mid_w` wide, centered under the center node. A node's marks sit in a row above its title (0.34in tall); step chips are 0.24in navy discs above them; a `strong` node is white with a 2pt navy border, an `accent` node navy with white text. Edge labels sit beside their arrows in mute.
- **gantt**: a two-column grid, 2.9in for the labels and the rest for the tracks. The header row holds the month labels in navy over a 1px rule; every track is 0.6in tall with a 1px line at each month boundary (a repeating background image sized to one month). A bar is 0.36in tall with full round ends, positioned by percentage of the track; its tone is tint, pale, steel or navy. A milestone is a navy 0.22in square rotated 45 degrees on the date, with its text in bold navy to its left; a row may hold a bar and a milestone.
- **profiles**: a grid of `cols` white cards (0.14in radius, 0.36in by 0.45in padding). The head is a 0.8in ring (2pt ink) with the initial at 22pt, then the name at 21pt and the title in small muted type with letter spacing. Each row is a 0.85in label column and a lines column; every line has a 1.5pt light rule at its left and 0.16in of padding.
- **timeline**: one column per phase with a 3.5pt rail in pale at its left; each entry has a navy disc on the rail, the `when` line in steel, the title in navy and plain tick lines below.
- **stack**: a grid of three columns (3in label, 5.6in description, the rest for the aside, or the block's own `cols`). Labels take, from the first step down, tint, pale, steel, navy; text is white on steel and navy. The aside spans every row.
- **cards**, **banner**, **stats**, **bullets** (ticks), **qa**, **split**, **shots**, **note**: as in 1.0; a card may carry an icon disc above or beside its title, a banner an icon disc at its left, a stat tile an icon disc, a value and a label. These are the blocks the design floor limits.
- **cover**: four rounded stripes rotated 40 degrees at the upper right (centers, widths and lengths in inches: 5.3/0.85 0.9×2.4 tint2, 9.3/2.1 0.85×6.1 line, 8.7/4.2 1.05×6.2 tint, 9.9/4.7 0.75×3.1 steel), the title block 0.75in from the left and 2.05in from the top (50pt, two lines), the tagline 0.35in below it, the logos in a row 0.75in from the left and 5.5in from the top (the client's logo 0.4in tall, a 1px rule, the presenter's logo 0.36in tall, 0.3in apart), and, only with `footer: true`, the client, date and brand line at 6.2in.
- **closing**: navy page; the title centered at 2.75in from the top; the white logo centered at 5.15in, 0.3in tall; the contact lines centered at 5.65in in a pale blue, 12pt.

## Printing

- Print with a Chromium-family browser: page width 13.333in, height 7.5in, background graphics on, the CSS page size preferred. Wait for the network to go idle and for `document.fonts.ready` before printing, or the font falls back.
- A page that overflows prints a cut: the fix is in the deck file (fewer words, fewer items, a split slide), never in the CSS.

## Review

Rasterize each page small (about 55 dpi) and tile them three per row into one image. Look for: cut text at the bottom of a page, a line broken inside a word, a lone word on a second line, a fact value that wraps, a loop whose center touches its nodes, a diagram whose nodes wrap into three lines, a Gantt bar whose text overflows its ends, a brand panel whose marks are recolored or on a dark ground, a profile card whose rows run past the card, and the design-floor defaults (icon card grids, number tiles, kickers). Then open any suspect page at about 85 dpi.
