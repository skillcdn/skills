# The page, the preview, the export, the review

How the post is built as one HTML page, shown to the user, rendered to PNG, and checked. What holds for any page the agent writes and renders is the repository's [rendering-html.md](/docs/browser/rendering-html.md), read with this page; a video slide adds what [video.md](video.md) says to each section.

## The page

One `index.html` in the post folder, with `img/` beside it (the brief's images copied in, or the brief's own `img/` in an account's folder) and `out/` for the PNGs.

- **Slides at native size, a grid, a lightbox, an export mode.** Each slide is a box of the canvas size (`width: 1080px; height: 1350px`) scaled into its card, with a number badge on each card (`data-n`), a lightbox, and an export mode (`?slide=N`) that renders one slide at native size for the headless browser, as rendering-html.md "Boxes at native size, and an export mode" says.
- **Below the grid**, the caption as preformatted text and the credits as a list, so that a reviewer sees them with the slides.
- **Tokens and classes.** The spec's colors as CSS variables; the fonts loaded in the head from the paths the spec names (a stylesheet link, or an `@font-face` for a font file); one class per slide type and element of the spec with the anatomy the spec measured (layouts.md "From the spec to classes"); a cropped photo as an `img` with `object-fit: cover` and its `object-position` set per slide, a crop by `transform: scale(<factor>)` with `transform-origin` placed away from the mark; a frame kept whole as an `img` at its own ratio inside a box at the spec's edges; gradient and dim overlays as positioned divs where the type has them; every text block positioned by the spec's top and bottom edges.
- **Markup for the review.** Every card carries `data-n` with its slide number, the export mode's stage element has the class `stage`, every block the spec places carries `data-block` with the spec's block name (`headline`, `sub`, `body`, `note`, `tag`, `frame`, `label`), and every text block carries `data-lines` with the count the plan placed, so that the review script counts lines and measures edges.

## Preview

Serve the post folder and show it as rendering-html.md "Serving the page" says (a page opened as a file shows a static snapshot in some hosts; a free port; the host's preview tool and its launch configuration, with the port as the server's argument; the cap on servers): copy [server.example.mjs](../scripts/server.example.mjs) into the post folder and run it there. Reload the pane after each export.

## Export

Copy [export.example.mjs](../scripts/export.example.mjs) into the post folder and run it there; it renders every slide as rendering-html.md "PNG at the canvas size" says (the viewport at the canvas at device scale 1, the waits for the network and the fonts, a screenshot clipped to the canvas per slide, every slide every time), and launches the browser as [headless.md](/docs/browser/headless.md) "playwright-core from Node.js" says (`playwright-core` borrowed through `PLAYWRIGHT_FROM`, else installed once into the tools folder with `PLAYWRIGHT_FROM` pointing at its `package.json`: `card-news/tools/` beside the brief folders, in an account's folder its scratch folder, never the post folder; `chrome`, then `msedge`, then its own `chromium`; a browser download asked first). The environment names the served page (`BASE`), the slide count (`SLIDES`), the file prefix (`PREFIX`: the plan's `post`, which in an account's folder is the post folder's name) and the canvas (`WIDTH`, `HEIGHT`); set them the way the shell does (`$env:NAME = "value"` in PowerShell, `NAME=value` before the command in a POSIX shell). The PNGs land in `out/<post>-<NN>.png`.

## The review

### The review script

Before looking, run [review.example.mjs](../scripts/review.example.mjs) from the post folder with the same environment as the export. It counts the lines the browser set against `data-lines` in the served page (the script of rendering-html.md "The line check"; an empty list means no line was broken by the renderer, and a line mixing type sizes, a date with a small arrow, can count one extra, read on the PNG), prints every `data-block` element's top and bottom edges per slide in export mode as percentages of the canvas, to hold against the spec's anatomy, and writes a phone-size copy of every PNG into `out/phone/`.

### Looking

Open every PNG at its native size and its copy in `out/phone/`, which is how a phone shows it, and read a file rewritten at the same path under a new name, as rendering-html.md "Looking at a render" says: what cannot be made out at phone size is what the user sees first. Judge by the verdicts in SKILL.md, in the order a reviewer meets them: the slide beside the account's slide of its type and the sequence first, then what cannot be made out, then the lines, then marks, crops and what an image shows, then the edges the script measured and the margins. What any medium's reader calls the AI feel, beyond the spec's register and types, is listed in the repository's [not-ai.md](/docs/variation/not-ai.md), read when a slide passes every verdict and still reads wrong.

Fix in the page, export again, run the review script again, and look again, until no verdict applies. Write one line per slide per pass into `review.md`, as `pass <n>, slide <NN>: <what was looked at>; <ok, or the fix made>`. Then attach every PNG to the checkpoint with one line each.

## Delivery files

`out/<post>-01.png` to `out/<post>-NN.png`, with `out/phone/` beside them; `index.html` with `img/`; `slide-plan.json` and `caption.txt` from the plan; `credits.md` (the brief's, rewritten in the spec's pattern); `review.md`.
