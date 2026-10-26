# The deck file

One JSON file holds the deck: `meta` and `slides`. The helper `scripts/render.py` reads exactly this; an HTML written by hand follows the same structure so that the next run can edit it in the same place.

## meta

| Key | Meaning |
|---|---|
| `client` | Who the deck is for ("<company> 귀중", "For <company>"). Shown on the cover only when the cover sets `footer: true`. Used in the file names. |
| `date` | The date in the organization's own format. Shown on the cover only with `footer: true`. |
| `brand` | The presenting organization's name. Shown on the cover only with `footer: true`. |
| `logo`, `logo_white` | Paths to the presenter's wordmark for the cover (on light) and the closing (on dark), relative to the deck file. PNG, JPG or SVG, embedded into the HTML as data URLs; a path that does not exist is reported and draws nothing. Optional; without `logo_white` the closing shows `brand` in white type. |
| `client_logo` | Path to the client's logo for the cover. It is placed first, a thin rule, then the presenter's logo. Optional; only from an asset the organization already holds. |
| `external` | `true` when the deck goes outside the organization. Turns the style check on. |
| `style` | The house style: `forbidden` is a map of a character to its name (the check reports the name), `no_bracket_heads` bans a string that starts with `[...]`. Only checked when `external` is true. |
| `theme` | Colors and font: `navy` (titles, emphasis), `steel` (accent bar, ticks, arrows), `ink` (body), `mute` (secondary), `tint` and `tint2` (bands, chips, the page gradient), `line` (card borders), `pale` (rails, the diagram frame, the loop ring, the closing's contact lines), `rule` (the thin rules of lists and the borders of nodes), `faint` (page numbers), `font` (family name), `font_css` (a stylesheet URL for the font, optional). Any key left out takes the default in layout.md; with one brand color, the rest are derived as layout.md "Deriving a theme from one color" says. |
| `page_numbers` | `false` turns the page number at the lower right of content slides off. Default on. |

Example:

```json
{
  "meta": {
    "client": "<client> 귀중",
    "date": "<the date, in the organization's own format>",
    "brand": "<brand>",
    "external": true,
    "style": { "forbidden": { "·": "middle dot", "—": "em dash", "–": "en dash", "①": "circled number" }, "no_bracket_heads": true },
    "theme": { "navy": "#22408E", "steel": "#7089BF", "font": "Pretendard" },
    "logo": "<path>/logo.png",
    "logo_white": "<path>/logo-white.png",
    "client_logo": "<path>/client.png"
  },
  "slides": []
}
```

Keys whose values are paths, ids or icon names (`logo`, `logo_white`, `client_logo`, `logos`, `symbol`, `center_logos`, `id`, `icon`, `font_css`) are not style-checked.

## Marks and icons

A named product, registry, host, editor or agent is shown by its mark: an image path (PNG or SVG) in `logo`, `symbol`, `logos` or `center_logos`, from the product's brand assets or a brand-icon set. A line icon (`icon`, one of `file`, `layers`, `search`, `cpu`, `code`, `clipboard`, `check`, `refresh`, `users`, `calendar`, `lock`, `download`, `laptop`, `bolt`, `target`, `gear`, `edit`, `clock`, `flag`, `server`) exists for the rare item whose meaning a word does not carry; it is never one per item and never a stand-in for a named product.

## slides

A slide is `{"type": ..., ...}`. Three types.

### cover

`title_lines` (one or two lines, 50pt), `tagline` (one short line that names the technical substance of the work; omit it rather than write a sentence; `subtitle` is accepted as another name for it), optional `footer: true` to print the client, date and brand line under the logos. The cover carries the logos (`meta.client_logo` first when present, then `meta.logo`) and the decorative stripes; nothing else.

### closing

`title` ("감사합니다", "Thank you") and `contact` (a list of lines: the person and email, the address). Dark background, white logo, everything centered.

### content

`title` (one line, 26pt), optional `subtitle` (one sentence, 14pt regular, only where the slide needs its one-sentence message), optional `logo` (a path; the image sits at the header's right; rarely right, a brand panel is the usual place for a mark), optional `tag` (a chip at the top right), optional `valign: "center"` (the blocks sit in the middle of the page instead of under the title; for a slide with one or two short blocks), and `blocks`, a list. One to three blocks per slide; three only when each is short. A `note` block is allowed but not used by default (see the composition rules in SKILL.md).

## Blocks

| kind | Fields | Shape |
|---|---|---|
| `columns` | `widths` (a grid-template-columns string such as "1fr 5.4in"), `gap` (inches), `stretch` (true to make the columns equal height), `blocks[]` (one block per column) | Side-by-side blocks: a statement beside facts, a loop beside a numbered list, two brand panels. |
| `statement` | `text` (one or two sentences), `size` (pt, 16 to 22), optional `lead` (a word or two in steel, inline before the text), optional `body` (a paragraph under it) | The slide's message in large bold type. The overview's goal; a quality bar with its lead inline. |
| `facts` | `items[]` of `[label, value]` (value a string or a list of lines), `label_w` (inches), `inline` (true for a row of label-above-value facts under another block) | A definition list with thin rules: the figures and facts of the overview; inline, the durations under a method. |
| `numbered` | `items[]` of `title`, `desc`, optional `no`; `cols` | A numbered list with thin rules: the steps of a method beside its loop. Up to six. |
| `loop` | `nodes[]` of four `title`, `sub` (top, right, bottom, left, clockwise); `center[]` (lines), `center_logos[]` (image paths); `width`, `height`, `r` (ring radius) in inches, `node_w`, `center_w` | A ring with arrowheads through four nodes, the tools' marks and a caption at the center: a method that repeats. |
| `brand` | `logo` (a wordmark path) or `symbol` (a mark path) with `name`; `tagline` (one line on what it is); `facts[]` of `logo`, `text` (the marks of where it lives with a fact each); `items[]` (what it does in this work) | A panel for a product or platform the work stands on. Two side by side in `columns` with `stretch`. |
| `rows` | `row_h` (inches), `items[]` of `title`, `desc`, optional `no`, `tag`, `icon`; block-level `basic_tag`, the tag value that reads as the default option and gets the filled chip (none unless set) | Numbered rows with a title column and a description. Four to six items (scope items, requests). |
| `steps` | `items[]` of strings (pills in one line) or of `label`, `icon`; `style: "tiles"` for tiles (number above the label); items with an icon render as tiles too | A process strip, up to six steps, above a `diagram`. |
| `diagram` | `nodes[]`, exactly five, in this order: the source, the center, the service, the output, the update; each of `id`, `title`, `body`, optional `logos[]` (image paths drawn above the title), `chips[]` (step numbers), `icon` (a line icon before the title, rarely), `strong` (white with a navy border, for the node that holds the tools) or `accent` (navy); `edges[]` of `[from, to, label]`, read for the labels of source to center, center to service, center to output and update to center; optional `frame`, `frame_note`, `mid_w` (inches, the width of the service and update nodes) | Five nodes at page width: the source (left), the center, the service above the center, the output (right), the update below. The first three rows sit inside a dashed frame; the update node sits below the frame with its arrow crossing the line. |
| `gantt` | `months[]`, `rows[]` of `label` and any of `start`, `end` (month indexes from 0, `end` exclusive, so that 0 to 2 covers the first two months; fractions allowed) with `tone` ("tint", "pale", "steel", "navy") and `text`; `milestone` (a month index from 0, fractions allowed; the diamond sits at that point) with `mtext` (or `text` when the row has no bar) | One row per phase, a bar in the months it covers, a diamond for a deadline. |
| `profiles` | `cols`, `items[]` of `name`, `initial`, `title`, `rows[]` of `[label, [lines...]]` | One card per person: a ring with the initial, the name, the title, then labeled rows. |
| `timeline` | `cols[]`, each a list of entries of `when`, `title`, `items[]`, optional `option` | One rail per column, entries top to bottom. Phases of equal weight. |
| `stack` | `row_h`, optional `cols` (a grid-template-columns string), `items[]` of `label`, `desc`; optional block-level `aside` of `title` and `items[]`, a side card that spans every row | A step stack with darkening labels; an optional side card. |
| `cards` | `cols`, `h` (inches), `icon_pos` (`"inline"` sets the icon beside the title, else above it), `items[]` of `title`, `body` or `items[]`, optional `icon` | White cards in a grid. The last resort, never the page structure; never one icon per card. |
| `banner` | `lead`, `body`, `h`, optional `icon` | A tinted band. A `statement` usually serves better. |
| `stats` | `caption`, `cols`, `items[]` of `icon`, `value`, `label` | Big-number tiles. Only when the figures are the slide; the design floor flags them as a default. |
| `bullets` | `items[]` of `[head, body]` or strings, `size`, `gap` | Tick bullets. Up to six. |
| `qa` | `items[]` of `q`, `a` | A question and its answer. Up to three. |
| `shots` | `items[]` of `label`, `caption`, optional `label_above` (a second label over the frame) | Framed placeholders for screenshots the outline asks for. |
| `split` | `left_w`, `left` of `items[]`, `right` of `items[]` (shots) or `diagram` (compact) | Bullets beside screenshot frames or a compact diagram. |
| `note` | `text` | Foot note. Not used by default. |

## Choosing a block

| The outline has | Block | Why |
|---|---|---|
| The goal and the facts of the work (volume, outputs, period, deadline) | `columns` of `statement` + `facts` | The goal in large type, the facts in a list with rules; nothing boxed. |
| Four to six numbered things (scope items, requests) | `rows` | A number, a name and a sentence each; the number is what people refer to in the meeting. |
| A quality bar or one sentence to remember | `statement` with `lead` | One bold sentence with its lead inline; not a banner, not a note. |
| A method that repeats, with its steps and durations | `columns` of `loop` + `numbered`, then `facts` inline | The loop shows the cycle and the tools at its center; the numbers carry the order; the durations sit under both. |
| The tools the work stands on | `columns` of two `brand` panels | Each tool by its real mark, where it lives, what it does here; two products easily confused told apart. |
| A system of parts and where the work happens | `steps` + `diagram` with node `logos` | The strip names the procedure; the chips say where each step runs; the tools' marks sit on the node that holds them. |
| A schedule with phases of different lengths | `gantt` | Bars for the phases, a diamond for the deadline. |
| A schedule by phase, equal weight, bullets per phase | `timeline` | One rail per phase. |
| The people doing the work | `profiles` | One card per person in the organization's own card format. |
| Questions the meeting must answer | `rows` with short `desc`, or `qa` | Only when the outline asks for such a slide. |
| Next steps or asks, each with an owner or a date | `rows`, or `numbered` where the items have no description | The number is what the room refers to; the owner or the date goes in the description. |
| A method that runs once, in order | `numbered` for up to six steps with a sentence each; `stack` when each step has a short label and the steps build toward a result; `timeline` when the steps have dates | One block per method; a method that repeats is the loop above. |
| Scope and goals on one slide | `columns` of `statement` + `facts` when there is one goal and its facts; `rows` when the scope is a list of items; two slides when both are long | The statement wins where the goal is one sentence. |
| Three items, or seven or more | `rows` or `numbered` for three, never `cards`; seven or more split across two slides or grouped into fewer rows | A slide holds four to six things at most. |

## Writing the strings

- A `title` names; a `subtitle` is the slide's one-sentence message; a `statement` is the message in full; `desc` is a full sentence; a fact value, a loop node's sub line or a profile line is a phrase.
- One idea per row, step, node or fact. Where the outline has more, split the slide.
- A quality bar is written as a floor with the ceiling open: what is always delivered, and what the iterations raise, in two sentences; nothing about who signs off.
- Durations that are alternatives per item are written as alternatives, with the rule that decides the total; durations that follow one another are written in sequence.
- Where two products are easily confused (a tool and the service it runs on, an agent and a model), say which the work uses and what it talks to.
- For an external deck, write within the house style from the first draft; the check is a net.
- No placeholder text. Where a fact is not yet known, say that it is to be confirmed, in the slide's own words.
