# The deck file

One JSON file holds the deck: `meta` and `slides`. The helper `scripts/render.py` reads exactly this; an HTML written by hand follows the same structure so that the next run can edit it in the same place. Which blocks a slide takes is decided by the register ([registers.md](registers.md)); this page says what each block is.

## meta

| Key | Meaning |
|---|---|
| `register` | `proposal` or `report` (registers.md). Decides the page frame, the cover variant and the footer. Default `proposal`. |
| `client`, `date`, `brand` | Who the deck is for, the date in the organization's format, the presenting organization. Shown on a proposal cover only with `footer: true`; `brand` and `date` in a report's footer. |
| `doc_name`, `footer` | A report's document name for its footer (default: the cover's first title line); `footer: false` turns the footer line off. |
| `logo`, `logo_white`, `client_logo` | Paths relative to the deck file (PNG, JPG or SVG, embedded): the presenter's wordmark on light, the white one for the closing and a report's cover, the client's for a proposal cover, first before the presenter's. |
| `external`, `style` | `external: true` turns the style check on: `forbidden` maps a character, or a string of characters checked one by one, to its name; `no_bracket_heads` bans a string that starts with `[...]`. |
| `labels` | The helper's fixed words, in the deck's language: `step` ("STEP") before the number of a detail tile, `q` ("Q.") before a question. |
| `theme` | Colors and font (`navy`, `accent` for a second brand color, `steel`, the grays and tints, `font`, `font_css`): roles, defaults and the derivation from one color in layout.md "Theme". |
| `page_numbers` | `false` turns the page number off. Default on. |

```json
{ "meta": { "register": "report", "date": "<date>", "brand": "<brand>", "doc_name": "<title> business plan", "external": false,
    "style": { "forbidden": { "·": "middle dot", "—": "em dash", "–": "en dash", "①②③④⑤⑥⑦⑧⑨⑩": "circled number" }, "no_bracket_heads": true },
    "theme": { "navy": "#22408E", "accent": "#7089BF", "font": "Pretendard" }, "logo": "<path>/logo.png", "logo_white": "<path>/logo-white.png" },
  "slides": [] }
```

Keys whose values are paths, ids or icon names (`logo`, `logo_white`, `client_logo`, `logos`, `symbol`, `center_logos`, `photo`, `src`, `id`, `icon`, `font_css`) are not style-checked.

## Marks, icons and photographs

A named product is shown by its mark: an image path in `logo`, `symbol`, `logos` or `center_logos`, from its brand assets. A line icon (`icon`, one of the names in layout.md "Icons") is for the rare item whose meaning a word does not carry, never one per item and never a stand-in for a named product. A photograph (`photo` on a cover, `src` in a `photo` block) is a file the organization or the user supplied; nothing is generated.

## slides

A slide is `{"type": ..., ...}`. Three types.

- **cover**: `title_lines` (one or two), `tagline` (one short line naming the substance of the work). Proposal: optional `footer` (`true` for the client, date and brand line, or a string for one line of the organization's own). Report: `kind` (the document's kind, as a label), `meta_rows` (`[label, value]` pairs: author, date, classification), optional `photo` (a path).
- **closing**: `title` ("감사합니다", "Thank you") and `contact` (lines). Dark page, white logo, centered.
- **content**: `title`, optional `section` (a report's section label, "01 Summary", the same on every slide of the section), optional `toc_sub` (the contents' one line for the section, on its first slide), optional `subtitle` (one sentence, only where the slide needs it), optional `logo` (at the header's right; rarely right), `tag` (a chip), `valign: "center"` (one or two short blocks centered), and `blocks`: one to three, three only when each is short.

## Blocks

| kind | Fields | Shape |
|---|---|---|
| `columns` | `widths` (a grid-template-columns string, "1fr 5.4in"), `gap` (inches), `stretch` (equal heights), `blocks[]` (one per column) | Side-by-side blocks. |
| `statement` | `text` (one or two sentences), `size` (pt, 16 to 22), optional `lead` (a word or two in the accent before the text), `body` (a paragraph under it) | The slide's message in large bold type. |
| `facts` | `items[]` of `[label, value]` (a string or a list of lines), `label_w` (inches), `inline` (label-above-value facts in a row under another block) | A definition list with thin rules. |
| `numbered` | `items[]` of `title`, `desc`, optional `no`; `cols` | A numbered list with thin rules. Up to six. |
| `toc` | `items[]` of `[no, title, sub]`, or `auto: true` (built from the slides' `section` and `toc_sub`); `cols` (2) | The contents: the number large in the accent, the title bold, one line under it. Report. |
| `table` | `columns[]`, optional `widths[]`, `rows[][]`, optional `first_col: "bold"`, `size` (pt, 10.5 to 12.5), `note` (one line under it: the sources) | A header row on tint, thin rules. Four to eight rows; a wider table splits across slides. |
| `kpi` | `cols`, `items[]` of `value`, optional `unit`, `label` (one sentence), `tag` (the source, or "to be confirmed"), `bar` (0 to 1), `tone: "navy"` (the ask); optional `note` | One to three panels per deck: the value, the sentence, the tag as a chip, an optional bar. Report; a proposal puts figures in `facts`. |
| `photo` | `src` (a supplied image), optional `caption`, `credit`, `h` (inches), `fit` (`"cover"` or `"contain"`) | A photograph in a rounded frame with its caption and credit, in `columns` beside facts or a list. |
| `loop` | `nodes[]` of four `title`, `sub` (clockwise from the top); `center[]` (lines), `center_logos[]`; `width`, `height`, `r`, `node_w`, `center_w` (inches) | A ring through four nodes, the tools' marks and a caption at the center: a method that repeats. |
| `brand` | `logo` (a wordmark) or `symbol` with `name`; `tagline`; `facts[]` of `logo`, `text`; `items[]` | A panel for a product the work stands on; two side by side in `columns` with `stretch`. |
| `rows` | `row_h` (inches), `items[]` of `title`, `desc`, optional `no`, `tag`, `icon`; `basic_tag` (the tag that gets the filled chip), `numbered: false` (a dot, for items with no order) | Rows with a title column and a description. Four to six. |
| `steps` | `items[]` of strings (pills), of `label`, `icon` (tiles), or of `label`, `when`, `desc` (detail tiles); `style: "tiles"`; optional `facts[]` of `[label, value]` under the strip | A process strip, up to six steps, above a `diagram` or on its own as a plan in stages. |
| `diagram` | `nodes[]`, five in this order: the source, the center, the service, the output, the update; each `id`, `title`, `body`, optional `logos[]`, `chips[]`, `icon`, `strong` or `accent`; `edges[]` of `[from, to, label]`; optional `frame`, `frame_note`, `mid_w` | Five nodes at page width inside a dashed frame, the update below it with its arrow crossing the line. |
| `gantt` | `months[]`, `rows[]` of `label`, optional `sub`, `start` and `end` (month indexes from 0, `end` exclusive, fractions allowed) with `tone` ("tint", "pale", "steel", "navy") and `text`, `milestone` (a month index) with `mtext` | One row per phase, a bar and a diamond; the milestone's text on the side the bar leaves free. |
| `profiles` | `cols`, `items[]` of `name`, `initial`, `title`, `rows[]` of `[label, [lines]]` | One card per person: a ring with the initial, the name, the title, labeled rows. |
| `timeline` | `cols[]`, each a list of `when`, `title`, `items[]`, optional `option` | One rail per column, entries top to bottom. |
| `stack` | `row_h`, optional `cols`, `items[]` of `label`, `desc`; optional `aside` of `title`, `items[]` | A step stack with darkening labels in one hue; an optional side card. |
| `cards` | `cols`, `h` (inches), `numbered: true` (a number disc, no icons) or `icon_pos`, `items[]` of `title`, `body` or `items[]`, optional `icon` | White cards in a grid: a proposal's last resort; a report's problem defined, two by two at most. |
| `bullets`, `qa` | `items[]` of `[head, body]` or strings, `size`, `gap`; `items[]` of `q`, `a` | Tick bullets, up to six; a question and its answer, up to three. |
| `banner`, `stats`, `shots`, `split`, `note` | `lead`, `body`, `h`; `caption`, `cols`, `items[]` of `value`, `label`; `items[]` of `label`, `caption`; `left_w`, `left`, `right`; `text` | A tinted band (a `statement` serves better); big-number tiles (the design floor flags them); screenshot frames the outline asks for; bullets beside frames or a compact diagram; a foot note, not used by default. |

## Writing the strings

- A `title` names; a `subtitle` is the slide's one-sentence message; a `statement` is the message in full; `desc` is a full sentence; a fact value, a node's sub line, a table cell or a profile line is a phrase or a number; a `kpi` label is one sentence and its `tag` names the source or says "to be confirmed" in the deck's language ("확인 필요" in Korean).
- One idea per row, step, node, cell or fact; where the outline has more, split the slide. A quality bar is a floor with the ceiling open, two sentences. For an external deck, write within the house style from the first draft; the check is a net.
- No placeholder text: where a fact is not yet known, say it is to be confirmed in the slide's own words, or tag the figure.
