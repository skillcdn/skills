# The deck file

One JSON file holds the deck: `meta` and `slides`. The helper `scripts/render.py` reads exactly this; an HTML written by hand follows the same structure so that the next run can edit it in the same place.

## meta

| Key | Meaning |
|---|---|
| `client` | Who the deck is for, as shown on the cover ("<company> 귀중", "For <company>"). Omit for an internal deck. |
| `date` | The date as it appears on the cover, in the organization's own format. |
| `brand` | The presenting organization's name, shown on the cover footer. |
| `logo`, `logo_white` | Paths to a PNG wordmark for the cover (on light) and the closing (on dark). Embedded into the HTML as data URLs. Optional. |
| `external` | `true` when the deck goes outside the organization. Turns the style check on. |
| `style` | The house style: `forbidden` is a map of a character to its name (the check reports the name), `no_bracket_heads` bans a string that starts with `[...]`. Only checked when `external` is true. |
| `theme` | Colors and font: `navy` (titles, emphasis), `steel` (accent bar, ticks), `ink` (body), `mute` (secondary), `tint` and `tint2` (bands, chips), `line` (card borders), `pale` (rails), `font` (family name), `font_css` (a stylesheet URL for the font, optional). Any key left out takes the default in layout.md. |

Example:

```json
{
  "meta": {
    "client": "<client> 귀중",
    "date": "2026. 10. 28",
    "brand": "<brand>",
    "external": true,
    "style": { "forbidden": { "·": "middle dot", "—": "em dash", "–": "en dash", "①": "circled number" }, "no_bracket_heads": true },
    "theme": { "navy": "#22408E", "steel": "#7089BF", "font": "Pretendard" },
    "logo": "<path>/logo.png",
    "logo_white": "<path>/logo-white.png"
  },
  "slides": []
}
```

Keys whose values are paths or ids (`logo`, `logo_white`, `id`) are not style-checked.

## slides

A slide is `{"type": ..., ...}`. Three types.

### cover

`title_lines` (a list of lines, 40pt), `subtitle` (one sentence). The cover footer is `client`, `date`, `brand` from meta, and the logo.

### closing

`title` ("감사합니다", "Thank you") and `contact` (a list of lines: organization, person and email, address). Dark background, white logo.

### content

`title` (one line, 26pt), optional `subtitle` (one sentence, 15.5pt, the slide's message), optional `tag` (a chip at the top right, such as "기본" or "옵션"), and `blocks`, a list. At most two blocks plus one `note` per slide.

## Blocks

| kind | Fields | Shape |
|---|---|---|
| `cards` | `cols` (number of columns), `h` (card height in inches, optional), `items[]` of `title`, `body` | White cards in a row. Three or fewer parallel items. |
| `banner` | `lead` (bold label), `body` (one or two sentences), `h` (inches, optional) | A tinted band for the one sentence to remember. |
| `bullets` | `items[]` of `[head, body]`, `size` (pt), `gap` (pt) | Tick bullets: a bold head and its sentence. Up to six. |
| `rows` | `row_h` (inches), `items[]` of `no`, `title`, `desc`, optional `tag` | Numbered rows with a title column and a description. Four to six items. `tag` "옵션" turns the number steel. |
| `stack` | `row_h` (inches), `items[]` of `label`, `desc`, optional `aside` of `title`, `items[]` of `[head, body]` | A step stack: a label cell per step, darkening downward, and its description; an optional side card. Up to five steps. |
| `timeline` | `cols[]`, each a list of entries of `when`, `title`, `items[]`, optional `option` | One rail per column, entries top to bottom. Phases of a schedule. |
| `qa` | `items[]` of `q`, `a` | A question in navy and its answer. Up to three. |
| `shots` | `items[]` of `label`, `caption`, `h` | Framed placeholders for screenshots the outline asks for. |
| `split` | `left_w` (inches), `left` of `items[]` `[head, body]`, `size`, `gap`; `right` of `items[]` (shots) or `diagram` | Bullets on the left, a diagram or screenshot frames on the right. |
| `diagram` (inside `split.right`) | `nodes[]` of `id`, `title`, `body`, optional `accent`; `edges[]` of `[from, to, label]` | Five nodes: the source, the center (accent), the service above, the output, the update below; edges source→center, center→service, center→output, update→center. |
| `note` | `text` | One or two lines at the foot of the page, 10.5pt, for a caveat or a scope boundary. |

## Choosing a block

| The outline has | Block | Why |
|---|---|---|
| Two or three parallel things (what, when, how) | `cards` | Equal weight, read at a glance. |
| Four to six numbered things (scope items, requests, decisions) | `rows` | A number, a name and a sentence each; the number is what people refer to in the meeting. |
| A sequence of steps | `stack` | Order is the message; the darkening labels carry it. |
| A schedule by phase | `timeline` | One rail per phase, bullets under each. |
| A system of parts | `split` with `diagram` | The bullets say what each part does; the diagram shows how they connect. |
| One sentence everyone should remember | `banner` | Set apart from the lists. |
| A boundary, a caveat, a dependency | `note` | At the foot, out of the argument. |
| Questions the meeting must answer | `rows` with short `desc`, or `qa` when answers are proposed | Rows when the answers are to be collected; `qa` when the deck proposes them. |

## Writing the strings

- A `title` names; a `subtitle` is the slide's one-sentence message; `body` and `desc` are full sentences.
- One idea per card, row or step. Where the outline has more, split the slide.
- For an external deck, write within the house style from the first draft; the check is a net.
- No placeholder text. Where a fact is not yet known, say that it is to be confirmed, in the slide's own words.
