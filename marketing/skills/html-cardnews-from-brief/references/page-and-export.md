# The page, the preview, the export, the review

How the post is built as one HTML page, shown to the user, rendered to PNG, and checked.

## The page

One `index.html` in the post folder, with `img/` beside it (the brief's images copied in) and `out/` for the PNGs.

- **Slides at native size.** Each slide is a box of the canvas size (`width: 1080px; height: 1350px`), absolutely positioned inside a card, with `transform-origin: top left`. A script scales every slide to its card's width (`scale(card.clientWidth / 1080)`) on load and on resize, so the grid shows the slides at any size while the CSS is written once in canvas pixels.
- **A grid and a lightbox.** The cards sit in a responsive grid; a click opens the slide in a lightbox at the largest size that fits.
- **Export mode.** With `?slide=N` in the URL, the script adds a class to the body that hides everything and sets `overflow: hidden` so that no scrollbar enters the clip, then clones slide N into a fixed stage at the top-left at native size with the clone's transform removed. The headless browser renders that.
- **Below the grid**, the caption as preformatted text and the credits as a list, so that a reviewer sees them with the slides.
- **Tokens and classes.** The spec's colors as CSS variables; the fonts loaded in the head from the paths the spec names (a stylesheet link, or an `@font-face` for a font file); one class per slide type and element of the spec with the anatomy the spec measured (layouts.md "From the spec to classes"); a cropped photo as an `img` with `object-fit: cover` and its `object-position` set per slide, a crop by `transform: scale(<factor>)` with `transform-origin` placed away from the mark; a frame kept whole as an `img` at its own ratio inside a box at the spec's edges; gradient and dim overlays as positioned divs where the type has them; every text block positioned by the spec's top and bottom edges.
- **Numbering.** A small number badge on each card, so that the review and the user name slides the same way.

## Preview

A page opened from the file system shows, in some hosts' browser panes, a static snapshot without its relative images (checked 2026-10): serve it instead. Copy [server.example.mjs](../scripts/server.example.mjs) into the post folder; it serves its own folder on the port given as its first argument, else the one in `PORT`, else 8787, with `Cache-Control: no-store` so that a re-export shows at once. Pick a free port: one the server starts on without an address-in-use error. A host that caps the preview servers it runs at once refuses a new one; stop one this run started, never one of the user's. Where the host has a preview tool that starts a server from a launch configuration and opens it in a pane, add an entry that runs `node <post folder>/server.example.mjs <port>` with the same port as the entry's own (the configuration file lives where the host reads it, which may be the working directory) and start it that way. Reload the pane after each export.

The server and the export script are ES modules and run whatever the project's module type; a CommonJS file named `.js` fails under a `package.json` with `"type": "module"`.

## Export

Copy [export.example.mjs](../scripts/export.example.mjs) into the post folder and run it there; it renders every slide:

- `playwright-core` is required from where it is installed: a `node_modules` of a neighbouring project, named by `PLAYWRIGHT_FROM` as the path of that project's `package.json`, or installed into the post folder with `npm install playwright-core` (no browser download). It launches an installed browser by channel, `chrome` then `msedge`, and falls back to its own `chromium` where one is installed; a channel launch needs a playwright-core from the last year or so (its `package.json` `version`); a borrowed copy older than that is left as it is in its project, and playwright-core is installed into the post folder instead. Where no browser is installed at all, `npx playwright install chromium` downloads one, and the user agrees to the download first.
- The environment names the served page (`BASE`), the slide count (`SLIDES`), the file prefix (`PREFIX`, the post's name) and the canvas (`WIDTH`, `HEIGHT`); set them the way the shell does (`$env:NAME = "value"` in PowerShell, `NAME=value` before the command in a POSIX shell).
- A page with a viewport of the canvas size at device scale 1; for each slide, navigate to the served page with `?slide=N`, wait for the network to be idle and for `document.fonts.ready`, a short pause for the images, then a screenshot clipped to the canvas, saved as `out/<post>-<NN>.png`.
- The whole run takes seconds; export all slides every time rather than one, so that a fix to a shared class is seen on every slide.

## The review

### The line check

Before looking, count the lines the browser actually set, in the served page (not in export mode), with a script run in the page that compares each text block's rendered lines with the lines the plan placed:

```js
[...document.querySelectorAll(".slide [data-lines]")].map((el) => {
  const tops = new Set();
  const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  for (let node; (node = walk.nextNode()); ) {
    const r = document.createRange(); r.selectNodeContents(node);
    for (const box of r.getClientRects()) if (box.width) tops.add(Math.round(box.top));
  }
  return { slide: el.closest(".card")?.dataset.n, want: +el.dataset.lines, got: tops.size, text: el.innerText.slice(0, 30) };
}).filter((x) => x.got !== x.want);
```

Give every text block a `data-lines` attribute with the count the plan placed; an empty result means no line was broken by the renderer. The rectangles are taken from the text nodes alone: a range over the block's whole contents also returns the boxes of its child elements (one `p` per line), which counted every line twice (checked 2026-10). A line mixing type sizes (a date with a small arrow) can count one extra; read those on the PNG.

### Looking

Open every PNG at its native size (the host's image reader at full resolution, or the browser pane at 100%), then once more at about a third of the canvas width, which is how a phone shows it (a copy resized to about 360 pixels wide, or the page's grid card at that width): what cannot be made out at that size is what the user sees first. An image reader may show a cached copy of a file rewritten at the same path: copy the PNG to a new name outside `out/` before reading it, or confirm the fix in the browser pane or by measuring the pixels that changed. The verdicts in SKILL.md govern; this is the same list in the order a reviewer meets it:

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
