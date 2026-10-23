# The page, the preview, the export, the review

How the post is built as one HTML page, shown to the user, rendered to PNG, and checked.

## The page

One `index.html` in the post folder, with `img/` beside it (the brief's images copied in) and `out/` for the PNGs.

- **Slides at native size.** Each slide is a box of the canvas size (`width: 1080px; height: 1350px`), absolutely positioned inside a card, with `transform-origin: top left`. A script scales every slide to its card's width (`scale(card.clientWidth / 1080)`) on load and on resize, so the grid shows the slides at any size while the CSS is written once in canvas pixels.
- **A grid and a lightbox.** The cards sit in a responsive grid; a click opens the slide in a lightbox at the largest size that fits.
- **Export mode.** With `?slide=N` in the URL, the script adds a class to the body that hides everything and sets `overflow: hidden` so that no scrollbar enters the clip, then clones slide N into a fixed stage at the top-left at native size with the clone's transform removed. The headless browser renders that.
- **Below the grid**, the caption as preformatted text and the credits as a list, so that a reviewer sees them with the slides.
- **Tokens and classes.** The spec's colors as CSS variables; the fonts loaded from their CDN in the head; one class per layout type with the anatomy the layout page gives; the photo as an `img` with `object-fit: cover` and its `object-position` set per slide; a crop by `transform: scale(<factor>)` with `transform-origin` placed away from the mark; gradient and dim overlays as positioned divs; the text blocks positioned from the bottom-left margins.
- **Numbering.** A small number badge on each card, so that the review and the user name slides the same way.

## Preview

A page opened from the file system shows, in some hosts' browser panes, a static snapshot without its relative images (checked 2026-10): serve it instead. Copy [server.example.mjs](../scripts/server.example.mjs) into the post folder; it serves its own folder on the port in `PORT` or 8787, with `Cache-Control: no-store` so that a re-export shows at once. Where the host has a preview tool that starts a server from a launch configuration and opens it in a pane, add an entry for `node <post folder>/server.example.mjs` there (the configuration file lives where the host reads it, which may be the working directory) and start it that way; a host that assigns a port passes it in `PORT`, and one that does not gets the same port in its entry and in the server's default. Reload the pane after each export.

The server and the export script are ES modules and run whatever the project's module type; a CommonJS file named `.js` fails under a `package.json` with `"type": "module"`.

## Export

Copy [export.example.mjs](../scripts/export.example.mjs) into the post folder and run it there; it renders every slide:

- `playwright-core` is required from where it is installed: a `node_modules` of a neighbouring project, named by `PLAYWRIGHT_FROM` as the path of that project's `package.json`, or installed into the post folder with `npm install playwright-core` (no browser download). It launches an installed browser by channel, `chrome` then `msedge`, and falls back to its own `chromium` where one is installed; a channel launch needs a playwright-core from the last year or so, and an older one is updated.
- The environment names the served page (`BASE`), the slide count (`SLIDES`), the file prefix (`PREFIX`, the post's name) and the canvas (`WIDTH`, `HEIGHT`); set them the way the shell does (`$env:NAME = "value"` in PowerShell, `NAME=value` before the command in a POSIX shell).
- A page with a viewport of the canvas size at device scale 1; for each slide, navigate to the served page with `?slide=N`, wait for the network to be idle and for `document.fonts.ready`, a short pause for the images, then a screenshot clipped to the canvas, saved as `out/<post>-<NN>.png`.
- The whole run takes seconds; export all slides every time rather than one, so that a fix to a shared class is seen on every slide.

## The review

Open every PNG at its native size (the host's image reader at full resolution, or the browser pane at 100%) and read it as the user will on a phone. The verdicts in SKILL.md govern; this is the same list in the order a reviewer meets it:

| Look for | Fix |
|---|---|
| A body sentence on two lines | Shorten the sentence to the spec's count; the type size does not shrink |
| A sub or a headline line wrapped | Rephrase |
| An agency mark, a logo, a watermark in the frame | A scale crop with the origin away from it, checked on the PNG; a "no modification" image is swapped for another of its role, or left whole with the mark in view and said so |
| A note or a tag over a bright or busy area | A top gradient under the note; the tag moved to the other corner |
| Text in the photo colliding with the slide's text | Reposition the image, or move the text block |
| A subject lost in a portrait crop | Shift the object position; swap for a vertical image of the same role |
| A photo visibly soft from upscaling | Swap for a larger image of the same role; else note the factor in the checklist |
| A poster's figures or list rows touching the margins | Fewer rows on the slide, or the figures reduced by about a tenth, within the spec |

Fix in the page, export again, and look again, until nothing in the table applies. Write one line per slide per pass into `review.md`. Then attach every PNG to the checkpoint with one line each.

## Delivery files

`out/<post>-01.png` to `out/<post>-NN.png`; `index.html` with `img/`; `slide-plan.json` and `caption.txt` from the plan; `credits.md` (the brief's, rewritten in the spec's pattern); `review.md`.
