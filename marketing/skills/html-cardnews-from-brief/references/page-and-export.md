# The page, the preview, the export, the review

How the post is built as one HTML page, shown to the user, rendered to PNG, and checked.

## The page

One `index.html` in the post folder, with `img/` beside it (the brief's images copied in) and `out/` for the PNGs.

- **Slides at native size, a grid, a lightbox, an export mode.** Each slide is a box of the canvas size (`width: 1080px; height: 1350px`) scaled into its card, with a number badge on each card (`data-n`), a lightbox, and an export mode (`?slide=N`) that renders one slide at native size for the headless browser, as [rendering-html.md](/docs/browser/rendering-html.md) "Boxes at native size, and an export mode" says.
- **Below the grid**, the caption as preformatted text and the credits as a list, so that a reviewer sees them with the slides.
- **Tokens and classes.** The spec's colors as CSS variables; the fonts loaded in the head from the paths the spec names (a stylesheet link, or an `@font-face` for a font file); one class per slide type and element of the spec with the anatomy the spec measured (layouts.md "From the spec to classes"); a cropped photo as an `img` with `object-fit: cover` and its `object-position` set per slide, a crop by `transform: scale(<factor>)` with `transform-origin` placed away from the mark; a frame kept whole as an `img` at its own ratio inside a box at the spec's edges; gradient and dim overlays as positioned divs where the type has them; every text block positioned by the spec's top and bottom edges.
## Preview

Serve the post folder and show it as [rendering-html.md](/docs/browser/rendering-html.md) "Serving the page" says (a page opened as a file shows a static snapshot in some hosts; a free port; the host's preview tool and its launch configuration, with the port as the server's argument; the cap on servers): copy [server.example.mjs](../scripts/server.example.mjs) into the post folder and run it there. Reload the pane after each export.

## Export

Copy [export.example.mjs](../scripts/export.example.mjs) into the post folder and run it there; it renders every slide as rendering-html.md "PNG at the canvas size" says (the viewport at the canvas at device scale 1, the waits for the network and the fonts, a screenshot clipped to the canvas per slide, every slide every time), and launches the browser as [headless.md](/docs/browser/headless.md) "playwright-core from Node.js" says (`playwright-core` borrowed through `PLAYWRIGHT_FROM` or installed into the post folder; `chrome`, then `msedge`, then its own `chromium`; a browser download asked first). The environment names the served page (`BASE`), the slide count (`SLIDES`), the file prefix (`PREFIX`, the post's name) and the canvas (`WIDTH`, `HEIGHT`); set them the way the shell does (`$env:NAME = "value"` in PowerShell, `NAME=value` before the command in a POSIX shell). The PNGs land in `out/<post>-<NN>.png`.

## The review

### The line check

Before looking, count the lines the browser actually set, in the served page (not in export mode), with the script in [rendering-html.md](/docs/browser/rendering-html.md) "The line check": every text block carries `data-lines` with the count the plan placed and every card `data-n` with its slide number; an empty result means no line was broken by the renderer, and a line mixing type sizes (a date with a small arrow) can count one extra, read on the PNG.

### Looking

Open every PNG at its native size and once more at about a third of the canvas width, which is how a phone shows it, and read a file rewritten at the same path under a new name, as rendering-html.md "Looking at a render" says: what cannot be made out at phone size is what the user sees first. The verdicts in SKILL.md govern; this is the same list in the order a reviewer meets it:

| Look for | Fix |
|---|---|
| A slide beside the account's slide of its type looks like another account's: a type the spec lacks, a block the type does not have, a frame cropped where the account keeps it whole | Compose it again from the spec's type as measured |
| A sequence the account's build does not show | The spec's `typical_order` |
| An image that cannot be made out at phone size (mosaic or blur alone, a dark scene, motion blur, a small picture upscaled past about two times) | Another legible image of the beat from the brief; where there is none, the beat to the caption, or the brief extended |
| A line broken by the renderer | Shorten, or move the hand-placed break to a clause end; the type size does not shrink |
| A sub or a headline line wrapped | Rephrase |
| A mark the account crops away in the frame | A scale crop with the origin away from it, checked on the PNG; a "no modification" image is swapped for another of its role, or left whole with the mark in view and said so. A mark the account keeps stays |
| The account's text over the material's own text, or a note or a tag over a bright or busy area | The block moved where the type allows; a gradient where the type has one |
| A subject lost in a crop | Shift the object position; swap for an image of the same role that keeps it |
| An image of other people, another production or another year than the slide's text names | An image of what the text names from the brief; else a line that says what the image shows where the type allows one, or the beat without the image |
| A block off the spec's top or bottom edge by more than about a twentieth of the canvas, or an empty band the reference's slide does not have | Measure the block's edges on the PNG in pixel rows and place it by the spec's; with no vertical edges in the spec, read the account's slide's edges from the study's log, else set the block where its type leaves room, centered in that space |
| A photo visibly soft from upscaling | Swap for a larger image of the same role; else note the factor in the checklist, when it still reads |
| Type touching the margins the spec's type keeps | Fewer lines or rows, or the figures reduced by about a tenth, within the spec |

Fix in the page, export again, and look again, until nothing in the table applies. Write one line per slide per pass into `review.md`. Then attach every PNG to the checkpoint with one line each.

## Delivery files

`out/<post>-01.png` to `out/<post>-NN.png`; `index.html` with `img/`; `slide-plan.json` and `caption.txt` from the plan; `credits.md` (the brief's, rewritten in the spec's pattern); `review.md`.
