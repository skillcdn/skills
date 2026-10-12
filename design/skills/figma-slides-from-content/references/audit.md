# The audit: numbers first, then zoomed renders

What is checked over every new slide before the second checkpoint, how, and what passes. Read in phase 6. The report is a text file in the scratch folder; its summary goes into the checkpoint message.

## Numeric checks

One read-only `use_figma` call over the new slides, found by the row's name, returning compact results.

| Check | How | Passes when |
|---|---|---|
| Margins | Minimum left and maximum right of each slide's children, background rectangles excluded; the top of the first content element below the title group | Nothing outside the spec's margins on any slide; on a slide whose layout spans the content width, the left edge equals the left margin and the right edge the right margin; the content top is the same on every slide that has a title group |
| Title group | The accent bar, the title and the subtitle by name: position and size on each slide | Identical coordinates and sizes on every slide that has them |
| Inventory | For each role name (`Bullet bar`, `Card`, `Number`, `Tile`, `Caption`, timeline `Dot` and `Line`): the set of distinct spec strings (size, fill, opacity, radius, shadow) and the count | One spec per role over all new slides; the count equals the expected count written in the slide plan |
| Mark gap | For each bullet mark, the nearest text to its right: the gap from the mark's right edge to the text's left, and the mark's top against the text's top | One gap value, the spec's; the offset within half a pixel of the spec's `mark.offset` |
| Text styles | Every `size/style/color/lineHeight` combination with the slides it appears on | Every combination is a role of the scale; no stray size |
| Collapsed boxes | Text nodes with auto-resize off and a height below the font size | None |
| Overflow and padding | For each text inside a card (the card found by containment): the text's ink (`absoluteRenderBounds`, or the box when the text is left-aligned at its natural width) against the card's edges minus the padding; a centered label's box spans its container on purpose and is not the measure | Nothing within the padding; nothing outside |
| Overlap and bounds | The batch validation from Figma's slides guidance: overlapping boxes, text clipping, nodes outside the slide. Two text boxes that overlap at coordinates taken from an existing slide pass when their ink does not touch, and the report says so | Clean, or noted |
| Protected slides | Child counts and names of the slides in the intake record's grid, against it now | Unchanged by the run; a slide the user changed is named in the report and left as it is |

Return each check's failures as short strings with the slide and the node name; an empty list is a pass.

## Visual checks

- A full screenshot of every new slide, inline from the same call (`await slide.screenshot()`), read for anything the numbers cannot see: a line broken mid-word, an image showing a background box, an oversized block, a card that looks empty.
- One zoomed render per element role at three to four times: a bullet row, a numbered row (circle, number, label, description), the title group, a timeline node, a caption pair, a tile label. Group the parts temporarily and render the group, as tool-notes.md "Zoomed renders" says. Read the glyphs against the mark as the existing slides show them: the digit's center in the circle, the mark against the first line's glyphs at the offset the deck uses, the bar's center on the title's glyphs, the dot's center on the heading's glyphs. A difference above one pixel at that zoom from what the existing slides show fails; the numbers are moved by the measured difference, and the numeric check is run again with the moved values.

## Fixing

A failure in a role is fixed on every instance of the role across the new slides in one call (the mark's size and fill set, the gap set, the text moved by the measured difference), and both parts of the audit run again. A fix that changes a layout (a taller card, a re-broken list) re-centers what the card holds. The loop ends when both parts pass; what was accepted with a change is written in the report and said at the checkpoint.

## The report

A text file with: the margins per slide; the inventory table (role, spec, count); the text style table against the scale; the fixes made, one line each; the renders read and their verdicts; anything left for the delivery's "not verified".
