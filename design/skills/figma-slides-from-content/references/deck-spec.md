# The deck spec: measuring the existing slides and building from them

How the design system of an existing deck is read into a spec that every build call uses, and how text and marks are created so that the audit passes. Read in phase 3 and again before phase 5. The JSON shape is [deck-spec.example.json](../assets/deck-spec.example.json).

## Which slides to measure

The content slides: every existing slide that carries running text below a title. The cover and the closing slide are read for their own roles only (the logo's place, the closing treatment). A deck with no content slide has nothing to match, and the skill says so at the plan checkpoint instead of inventing.

## What to measure

One read-only `use_figma` call per group of slides, returning compact strings; the return payload is capped (tool-notes.md "Return payload"), so aggregate and never return whole node trees.

| Role | Measure |
|---|---|
| Slide | Width and height of a slide node. |
| Margins | Minimum left and maximum right of every child (background rectangles excluded, recognized by covering the slide) over the content slides; the top of the first content element below the title group; the bottom of the lowest. |
| Title group | The accent bar (size, position, color), the title (family, style, size, line height, color, position), the subtitle or lead (the same), on each content slide; they repeat at the same coordinates. |
| Body | The text style combination (size, style, color, line height) that running text uses, see "The body size". |
| Bullet mark | The small rectangle or ellipse beside list items: width, height, fill, opacity, its vertical offset from the first line's top, the gap from its right edge to the text's left. |
| Card | White or tinted rectangles that hold text: fill, corner radius, the drop shadow's color, opacity, offset and blur; the padding from the card's edge to its first text. |
| Tile, accent shape | Filled rectangles that carry a label: fill, radius, the label's style and alignment. |
| Timeline | A dot's diameter and fill, a line's width and fill (a gradient's stops), the heading's size, the offset between the dot's center and the heading's glyph center. |
| Page number | Style, size, color, position, alignment. |
| Text styles | Every combination `size/style/color/lineHeight` with the slides it appears on. The deck's roles are the combinations that repeat across slides. |

A measurement script collects, for each node: type, size (to a tenth for anything under 12 px), position, the first fill as hex or its type, the first stroke, the corner radius, the effects; for text, the family, style, size, line height unit and value, the first fill, and the first characters. Group the strings by role and return them with the slide they came from.

## The body size

The body size is the most frequent text size on the content slides among text nodes below the title group and above the page number, by character count. The deck's scale is then the sorted set of sizes that repeat on two or more slides (on the one slide, when the deck has a single content slide), each with its role from where it sits (above everything: title; below the title: lead; the first text in a card or a column: heading; a bold size between the heading and the body that opens a group inside a card: sub-heading; smaller than the body: caption). A role the deck lacks takes a step from the base using the deck's ratio between the two roles nearest to it, rounded to a whole number. When the user names a base ("make the base 22"), the roles keep their ratios to it. A title group whose coordinates differ between slides takes the most common ones.

## Fonts

List the families on the content slides from the text nodes' `fontName` (mixed nodes through `getStyledTextSegments`). For each family, `figma.listAvailableFontsAsync()` says which styles load through the server; a family that is installed only on the user's machine returns no styles and `loadFontAsync` throws for it (tool-notes.md "Fonts"). Choose the substitute as the family that loads and covers the document's script with the styles the scale needs (a bold, a regular, a medium where the lead uses one). The font list says nothing about coverage: start from a family whose name carries the script (KR, JP, SC, TC, CJK, or a known vendor of that script), then prove it in one read-only call that creates a text node in that family with one line of the document, renders it with `node.screenshot()` and removes the node; fallback boxes or a changed shape in the render mean the family lacks the glyphs. Say at the plan checkpoint which family stands in for which.

## The spec object

The spec is written once, as JSON in the scratch folder, and pasted into every build call as a constant: colors as hex strings converted by one helper, sizes and line heights per role, the margins, the title group's coordinates, the bullet mark, the card, the list gap (the vertical space between items), the card padding. Nothing in a slide's build code carries a number that is not read from the object; a value that must differ for one slide (a taller card for a two-line row) is computed from the object's values.

## The preamble

Every build call starts with the same text, verbatim:

1. Font loading for every style the scale uses, awaited together.
2. The hex helper and the spec object.
3. `rect(parent, x, y, w, h, fill, radius, opacity)`: create, `appendChild`, resize, fill, radius, then `x`/`y`. The slides guidance explains why position comes after `appendChild`.
4. `card(parent, x, y, w, h)`: a rect with the spec's fill, radius and shadow, named `Card`.
5. `text(parent, style, size, color, characters, x, y, lineHeight, options)`: see "Text". `options` carries a fixed `width` (natural width when absent), the horizontal `align`, an `opacity`, and a `name` (the first line of the characters when absent).
6. `body`, `heading`, `subhead`, `caption`: `text` with the role's size, style, color and line height from the spec.
7. `rich(parent, label, body, x, y)`: one body text with the label range in the heading's style and color (`setRangeFontName`, `setRangeFills`), for "label: value" items.
8. `list(parent, x, y, items)`: for each item, a body text at `x + mark.width + mark.gap` and a mark rect at `x`, the mark's top at `textTop + mark.offset`, where `mark.offset` is the measured distance from the first line's top on the existing slides and, when the deck centers its marks, equals `(lineHeightPx - mark.height) / 2` with `lineHeightPx = size * lineHeight / 100`; items `listGap` apart; returns the bottom of the last item. The audit checks the same offset, and the zoomed render confirms that the glyphs sit on the mark as they do on the existing slides.
9. `header(slide, title, subtitle)`: the title group at the spec's coordinates.
10. `grid()`: `figma.getSlideGrid()` read now, not from an earlier call, and the row found by name.

## Text

Create the node, `appendChild` it, set `fontName`, `fontSize`, `characters` (with the document's breaks as `\n`), `fills`, `lineHeight`. A line of the document that is wider than its region at the deck's size (measure with a natural-width node, or estimate from the character count times the size) is re-broken by the agent at a space, into the fewest lines that fit; the region's width and the card padding are fixed, the break is not. Then the size, in this order:

- A fixed width: `resize(width, 10)` first, then `textAutoResize = 'HEIGHT'`. The node grows to its lines.
- A natural width: `textAutoResize = 'WIDTH_AND_HEIGHT'`.

A `resize` after `textAutoResize = 'HEIGHT'` collapses the node to the height given and turns auto-resize off (tool-notes.md "Text sizing"), and every vertical center computed from its height is then wrong. Read `height` only after the auto-resize is set. Horizontal alignment (`textAlignHorizontal`) is set before the position; a centered label gets the full width of what it is centered in and `x` at its left edge.

Vertical centering of a text in a shape: `y = shapeTop + (shapeHeight - text.height) / 2`, then checked on a zoomed render, because a font's ascent sits the ink above the box's center by a pixel or two; the audit moves the text by the measured difference. Where the API returns `absoluteRenderBounds` for a text node, the difference between that box and the node's box is the offset to correct by before the render check.

## Layouts

A page's layout type maps to the spec's parts:

| Layout type | Built from |
|---|---|
| Cover | The deck's own cover, measured for its parts (the logo's place and size, the title's size and position, the date or subtitle); built new with the document's words and logo. A deck whose cover the user keeps gets no new cover, said at the plan |
| Headings and paragraphs | The title group, then the blocks down the content width in one column with the spec's list gap between them, no cards; two equal columns when the blocks exceed half the content height |
| Lead and cards | The title group; two or three cards across the content width with equal gaps, each a heading and a body or a list |
| Tiles with descriptions | A column of tiles with centered labels, a column of cards with vertically centered descriptions, a side card with sub-headings and lists; the three columns share one bottom |
| Numbered rows | Full-width cards of one height (taller for a two-line description), a numbered circle, a bold label, a description, each vertically centered on the row |
| Device mockups | Equal images across the content width, a bold caption and a muted description under each |
| Timeline | Two columns, each a vertical line with a dot and a heading per phase and a list under it, the dot centered on the heading's glyphs |
| Two columns | Two cards of one height, each a heading and a list with explicit breaks |
| Closing | The deck's own closing slide, measured as the cover is: its fill, the logo's place, the line's style |

A layout taken from an existing slide is re-created with the preamble's helpers at that slide's coordinates and sizes; the existing slide is never cloned, because its nodes carry no role names and it is protected. When the page holds more items than that slide did, the type goes one step down and the spacing is refitted before the build, and the checkpoint says so.
