# Rendering an HTML page the agent wrote

How a page the agent lays out in HTML and CSS (a carousel of slides, a deck, a share image, an app's pages) is shown to the user, rendered to PNG or printed to PDF with a headless browser ([headless.md](headless.md)), and looked at before it is delivered. The page's design (its slide types, its blocks, its tokens) is the skill's; this page holds how any such page is built to render, served, exported and reviewed.

## Boxes at native size, and an export mode

- Every unit (a slide, a page, a card) is a box of its native size in CSS pixels (`width: 1080px; height: 1350px`, or a page of `13.333in` by `7.5in`), with `overflow: hidden`, so that the CSS is written once in the unit's own pixels and nothing has to be scaled by hand.
- A preview grid scales each box into its card with `transform: scale(card.clientWidth / width)` and `transform-origin: top left`, on load and on resize; a lightbox shows one unit at the largest size that fits. A small number badge on each card, so that the review and the user name units the same way.
- An export mode renders one unit for the headless browser: with `?slide=N` in the URL, a script hides everything else, sets `overflow: hidden` on the body so that no scrollbar enters the clip, and places a clone of unit N at the top left at native size with its transform removed.
- Text breaks at spaces and never inside a word: `word-break: keep-all` with `overflow-wrap: break-word` as the fallback for a string longer than its box, for Korean and every language that breaks at spaces.
- A page meant to be the deliverable itself (a deck) is self-contained: the stylesheet inline, the marks as data URLs, the font from one URL with a system fallback; it opens anywhere and needs no server.

## Serving the page

- A page opened from the file system shows, in some hosts' browser panes, a static snapshot without its relative images, and a page with its images inlined as data URLs grew past a few megabytes and did not open at all (checked 2026-10). Serve the folder with a small static server that sends `Cache-Control: no-store`, so that a re-export shows at once, on a free port: one the server starts on without an address-in-use error. The card-news build skill carries one as [`server.example.mjs`](/marketing/skills/html-cardnews-from-brief/scripts/server.example.mjs); it takes the port as its argument and knows the `.woff` type.
- Where the host has a preview tool that starts a server from a launch configuration and opens it in a pane, add an entry that runs the server with the entry's own port as its argument, because the port arrived in the environment in one run and not in another (checked 2026-10), and start it that way. A host that caps the preview servers it runs at once refuses a new one: stop one this run started, never one of the user's. Reload the pane after each export.
- A subagent in one host had no tool to attach files to its messages (checked 2026-10): it gives the output folder and the served address, and the session that started it attaches the files.

## PNG at the canvas size

For each unit: a page with the viewport at the canvas size and `deviceScaleFactor: 1`, navigate to the served page in export mode, wait for the network to be idle and for `document.fonts.ready`, pause about 300 milliseconds for the images, then a screenshot clipped to the canvas, saved as `out/<name>-<NN>.png`. The clip at scale 1 gives a file of exactly the canvas size. Export every unit every time rather than one, so that a fix to a shared class is seen on every unit; the whole run takes seconds. The card-news build skill carries this as [`export.example.mjs`](/marketing/skills/html-cardnews-from-brief/scripts/export.example.mjs), driven by `BASE`, `SLIDES`, `PREFIX`, `WIDTH` and `HEIGHT` in the environment.

## PDF at a declared page size

The CSS declares `@page { size: <w> <h>; margin: 0 }` and gives every page element that size with `break-after: page`; the browser prints at that size with background graphics on and the CSS page size preferred, after the waits above (headless.md "PDF"). A page that overflows prints a cut, and the fix is in the content (fewer words, fewer items, a split page), never in the CSS. Without a browser the agent can run, deliver the HTML and say that the PDF is printed from the browser's print dialog at the page size with background graphics on. The deck skill's helper, [`render.py`](/design/skills/html-deck-from-outline/scripts/render.py), prints this way with Playwright from Python.

## Fonts

- Load a web font in the head from the family's documented path: for a family on Google Fonts its `css2` URL with the weights, checked to return `@font-face` rules; otherwise the path in the family's own README. A face served as a single `.woff` file takes an `@font-face` rule, and a static server that serves a local copy must know the `.woff` type (checked 2026-10). Every stack ends in a system fallback that has the script's letters (a Korean-capable sans for Korean).
- `document.fonts.ready` after the network went idle was enough for CDN fonts to render (checked 2026-10).
- A Korean sans with no italic renders a synthetic slant where italic is asked for, which reads as a mistake: set the text upright unless the face has a true italic (checked 2026-10). A condensed width is `font-stretch` where the face supports it, else `transform: scaleX()` on the block. A heavy outline around display type is `-webkit-text-stroke` with `paint-order: stroke fill`, so that the stroke sits behind the fill and does not thin the letters.

## The line check

Before looking, count the lines the browser set, in the served page and not in export mode, with a script in the page that compares each text block's rendered lines with the lines the plan placed. The markup it needs: every text block carries `data-lines` with the count the plan placed, and each unit's card carries `data-n` with its number.

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

An empty result means no line was broken by the renderer. The rectangles are taken from the text nodes alone: a range over the block's whole contents also returns the boxes of its child elements (one `p` per line), which counted every line twice (checked 2026-10). A line that mixes type sizes (a date with a small arrow) can count one extra: read those on the PNG.

## Looking at a render

- Open every PNG at its native size (the host's image reader at full resolution, or the browser pane at 100%), then at the size its reader will see it: a phone shows a post at about a third of the canvas width (a copy resized to about 360 pixels wide, or the grid card at that width); a deck page is read as it projects. What cannot be made out at that size is what the user sees first: a render judged at native size alone passed, and failed at phone size.
- An image reader may show a cached copy of a file rewritten at the same path (checked 2026-10): copy the PNG to a new name outside the output folder before reading it, confirm the fix in the browser pane, or measure the pixels that changed.
- A render that was made and not looked at was not reviewed: the review says which file it read.
- Every change is made in the page or in the source file and exported again; a PNG or a PDF is never edited by hand.

## A contact sheet of many pages

For a deck or a run of many units, rasterize every page small (about 55 dpi: a PDF rasterizer such as PyMuPDF renders pages to PNG, or a browser screenshot of each page does) and tile them three or four per row into one image; look for cut text, a line broken inside a word, a lone word on a second line, a value that wraps, elements that touch, and the defaults the skill's own design floor names; then open any suspect page at about 85 dpi or at full size. The sheet is the review's record: the delivery names it.
