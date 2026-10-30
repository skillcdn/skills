# The minutes file

One JSON file holds the minutes. The helper `scripts/render.py` reads exactly this; an HTML written by hand follows the same structure ("Markup and style" below), so that the next run can edit it in the same place.

## Top-level keys

| Key | Meaning |
|---|---|
| `file` | The output name without an extension: `<file>.html`, `<file>.pdf`, `<file>-preview.png`. |
| `lang` | The language tag of the minutes (`ko`, `en`), written into the HTML. |
| `kind` | The document kind shown at the top right ("Minutes", 회의록). |
| `title` | The title: the project and the meeting ("<project> kickoff meeting minutes"). |
| `logos` | A list of `{"src", "alt"}`, the client's logo first, then the organization's wordmark: paths relative to the minutes file, embedded as data URLs (PNG, JPG or SVG). A path that does not exist is reported and draws nothing. Optional; without it, `org` is shown in type. |
| `org` | The organization's name, shown in type where there are no logos. |
| `external` | `true` by default: the house-style check runs. `false` only for minutes that stay inside the organization. |
| `style` | The house style, left out when it is the usual set (below), which the helper then applies whole. Written only when the organization's set differs: `usual: true` starts from the usual set, `forbidden` is a map of a character to its name (the check reports the name) added to it, or the whole set when `usual` is absent, and `no_bracket_heads` bans a string that starts with `[` (on with `usual`, off otherwise unless set). `{"usual": true, "forbidden": {"~": "tilde"}}` is the usual set and one more; `{"forbidden": {}}` is a style that bans nothing. The same keys as the deck skill's `meta.style`. |
| `theme` | `font`, the family name, and `font_css`, a stylesheet URL for it (optional). The stack ends in the system's sans with the script's letters; the default is that stack alone. No colors: the minutes are grayscale. |
| `meta` | The header table, a list of `[label, value]` pairs, four of them: date and time, place, attendees, author. A `\n` in a value breaks the line. |
| `sections` | The sections, in order (below). |
| `footer` | One line under a thin rule at the end. Not used unless the organization's own minutes carry one. |

The usual set: middle dots in every form (`·`, `•`, `‧`, `∙`, `ㆍ`), the em dash, the en dash, the horizontal bar (`―`), circled numbers (`①` to `⑳`), and bracketed heads. Keys whose values are paths, codes or the style itself (`file`, `lang`, `logos`, `theme`, `style`, `external`) are not checked.

## Sections

A section is `{"heading", "type", ...}` with an optional `note` (one short line under it, in small gray type). The number is part of the heading ("2. Decisions"); a reference table is unnumbered ("Reference. Delivery formats").

| type | Fields | Shape |
|---|---|---|
| `text` | `paragraphs[]` | Paragraphs. The overview. |
| `list` | `items[]` of strings or of `{"title", "body"}` | Numbered items, `1)`, each a bold title and one sentence. Decisions, questions and answers, items to confirm. |
| `table` | `columns[]`, `widths[]` (CSS widths, optional), `rows[][]` | A grid with a gray header row, repeated on a new page. The actions (item, owner, planned); figures given in the room. |
| `kv` | `rows[]` of `[label, value]` | A two-column table like the header. The next meeting (date and time, place, agenda). |

The order of a set of minutes: overview (`text`), decisions (`list`), questions and answers (`list`), a reference table where the room was given figures (`table`), items to confirm (`list`), actions (`table`), next meeting (`kv`). A section with nothing in it is left out, and the numbers close up.

Example: [minutes.example.json](../assets/minutes.example.json), a fictional meeting with placeholder values.

## Terms

The headings, the header labels and the columns are in the minutes' language, in the terms the organization's earlier minutes use. With none, in English: Date and time, Place, Attendees, Author; Overview, Decisions, Questions and answers, Reference., Items to confirm, Actions, Next meeting; Item, Owner, Planned; "and others". In Korean: 일시, 장소, 참석, 작성; 회의 개요, 결정사항, 질의와 답변, 참고., 확인사항, 조치사항, 다음 회의; 항목, 담당, 예정; 외. Another language takes the plainest words of its business writing for the same things.

## Markup and style

What the helper renders, so that the HTML can be written by hand when the helper cannot run, and so that a reviewer knows what a correct render looks like.

- **Page.** A4 with margins of 18 mm at the top and 16 mm at the sides and the bottom (`@page { size: A4; margin: 18mm 16mm 16mm; }`). The page number sits in the foot, centered, as `1 / 3`, printed by the browser's footer template; the template draws in the margin the print call sets, so the call passes the same margins as the CSS. The HTML is one self-contained file: the stylesheet inline, the logos as data URLs, the font from `theme.font_css` where given, with the system fallback.
- **Type.** Body text 10.5 pt at a line height of 1.55; the title 18 pt bold; a section heading 12 pt bold with a 0.6 px gray rule under it; table text 9.8 pt; a note 9 pt gray. `word-break: keep-all` with `overflow-wrap: break-word`, so that text breaks at spaces and never inside a word. Every color of the document's own is a gray: `#1b1b1b` text, `#222` the top rule, `#999` section rules, `#c8c8c8` table borders, `#f2f2f2` header cells, `#555` the kind and the notes; the logos keep their own colors.
- **Top.** One row: the logos at the left, each 4.5 mm tall with a 0.6 px gray hairline between them (or `org` in 9.5 pt gray type), the kind at the right in 9.5 pt gray; a 1.2 px rule under the row. Then the title, then the header table (`table.meta`: a 22 mm label column with a light gray cell and 0.6 px borders).
- **Sections.** `h2` for the heading, with `break-after: avoid` so that it never ends a page alone. A list is an `ol` with `1)` counters, the title in bold followed by the sentence, `break-inside: avoid` on each item. A table has a gray header row (`thead`, repeated when the table continues on a new page) and 0.6 px borders, `break-inside: avoid` on each row. A note is a `div.note`.
- **Print.** Backgrounds on (`print-color-adjust: exact`), A4 preferred from the CSS; a page that overflows breaks between items and rows, never through one.
