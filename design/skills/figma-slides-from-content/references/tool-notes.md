# Tool notes: the Figma MCP server in this skill's phases

What the server and the Plugin API did in runs of this skill, by topic, as it holds now. Figma's own guidance (`figma-use`, `figma-use-slides` and its references) is the base; these notes add what the guidance did not say or said differently when met. A fact that can change names the month it was checked.

## Return payload

`use_figma` returns only the script's `return` value, capped at 20 KiB; a larger return fails the whole call and none of its edits land (Figma MCP server, checked 2026-10). Inspection scripts aggregate (counts, sets of style strings, first characters) and never return node trees; a build returns ids and child counts.

## Slide rows

- `figma.getSlideGrid()` returns arrays of slides per row and leaves out an empty row, so a row created in the same call is not at the index its position suggests; `figma.createSlide(row, index)` then puts the slide in another row (checked 2026-10). Find rows as nodes: the `SLIDE_GRID` child of the current page, its `SLIDE_ROW` children by name, and move a slide with `row.appendChild(slide)`.
- `figma.setSlideGrid()` throws "must contain all the children in the current grid" when the array passed leaves any slide out; moving with `appendChild` avoids it.
- The grid, the row indices and the slide ids change under the run when the user adds, removes or reorders slides between calls. Every call reads the grid again and finds the row by name and the slides by their index in it; an id or a row index from an earlier call is not reused.
- `SLIDE_ROW.name` is settable; the arrays `getSlideGrid()` returns are not rows, and a name set on them does nothing.
- A slide's own `name` does not persist: Figma Slides names every slide by its ordinal in the deck, and a name set at build time reads back as a number in the next call (checked 2026-10). Find a new slide by its row (by name) and its index in that row, and carry role names on the nodes inside the slide, never on the slide.

## Text sizing

A text node given `resize(w, h)` after `textAutoResize = 'HEIGHT'` ends with that height and `textAutoResize = 'NONE'` (checked 2026-10). The order that works is width first, then `HEIGHT`. The signature in an audit: a text node with `textAutoResize === 'NONE'` and `height < fontSize`. Repair: set `WIDTH_AND_HEIGHT`, read the natural width, then `resize(width, height)` and `HEIGHT` again when it needs a fixed width or a non-left alignment, and recompute its `y`.

## Fonts

- `figma.listAvailableFontsAsync()` lists what loads through the server. A family installed only on the user's machine (a local font the deck shows in the editor) lists no styles and `loadFontAsync` throws "could not be loaded"; the deck's text keeps showing it, but new text cannot use it (checked 2026-10).
- A family that loads offers only the styles it lists; the scale's bold, regular and medium are chosen from those names exactly.
- Mixed-style text: `fontName === figma.mixed`; read the segments with `getStyledTextSegments(['fontName'])` and load each before writing characters.

## Uploads

- `upload_assets` with `count` and `nodeIds` returns one single-use URL per image; the file is posted as multipart (`curl -F "file=@<path>"` worked; checked 2026-10) and the server sets it as the node's fill with `scaleMode` (`FIT` keeps the image whole). In a Windows PowerShell, `curl` is an alias of another command and refuses `-F`; use `curl.exe` or a POSIX shell.
- URLs posted in parallel from background shells landed only one image; posting them one after another in one foreground command landed all (checked 2026-10). A node whose fill stayed `SOLID` after the round was not uploaded; request new URLs for those nodes only.
- A raster crop with the page's background in its margins shows as a box on a colored slide. Flood-fill the margins from the border to transparent before the upload (document-reading.md "Images"; the example script's `--transparent` mode does it).

## Addressing nodes

A selector by a property (every rectangle narrower than 600, every text of size 16) catches the wrong node on another slide (a page number, a side card). Give every node a role name at creation and select by `name`; `findAllWithCriteria({ types: ['TEXT'] })` for all text, then filter by name.

## Zoomed renders

`await node.screenshot()` inside `use_figma` returns an image with the call; `node.screenshot({ scale })` renders at a multiple, but a text node alone renders without its mark. For a glyph check, group the mark and its text temporarily (`figma.group([...], parent)`), screenshot the group at three to four times, then `figma.ungroup(group)`; or shorten a long body text to its first line, render, and restore its characters. `absoluteRenderBounds` on a text node gives the ink box without a render, where it is returned.

## Scripts without spaces

Figma wraps Korean, Japanese and Chinese text at any character, so a fixed-width box breaks a word where the width runs out. Explicit `\n` at the document's own line ends, with the box wide enough for the longest line, is the only reliable break; `textAutoResize = 'WIDTH_AND_HEIGHT'` with explicit breaks never wraps.

## Validation

`get_metadata` is refused on Slides files; every check is a read-only `use_figma` script. `console.log` output is not returned. An error inside the script discards every edit of that call, so a long build is split into batches of three to five slides.
