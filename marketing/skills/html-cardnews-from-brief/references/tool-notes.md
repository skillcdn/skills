# Tool notes: how the tools behaved

What runs of this skill met in the host's preview, in Node.js and in the headless browser, by topic, with the day where a fact can go stale.

## The host's preview

A page opened as a file in one host's browser pane rendered as a static snapshot: the layout showed, the relative images did not (checked 2026-10). A page with its images inlined as data URLs grew past four megabytes and did not open at all. Serving the folder with a small static server fixed both. The host's preview tool started the server from its launch configuration; in one run it passed the entry's port in the environment and in another it passed none, so the server takes the port as an argument from the entry (checked 2026-10). The same host allowed five preview servers at once and refused a sixth until one was stopped (checked 2026-10). A subagent in one host had no tool to attach files to its messages; it gave the `out/` path and the preview, and the session that started it attached the PNGs.

## Reading the PNGs

One host's image reader showed a PNG rewritten at the same path as it was before the rewrite (checked 2026-10); copying the PNG to a new file name before reading it showed the new render, and a change can also be confirmed on the browser pane or by measuring the pixels. Images copied from articles may carry their outlet's metadata, including a location; the exported PNGs are screenshots and carry none. A slide judged at native size passed and failed at phone size in one run: a frame shot at night from a vehicle's camera and frames of a face the broadcaster blurred read as shapes at a third of the width, and the user's first words were that the slides could not be seen (checked 2026-10); the review reads every PNG at both sizes.

## Node.js

A project whose `package.json` declares `"type": "module"` runs a `.js` file as an ES module, and a `require` in it fails with a reference error; the server and the export script are written as ES modules so that they run anywhere (checked 2026-10). A long file written through a shell heredoc on Windows can land truncated; write files with the editor's file tools.

## playwright-core

`playwright-core` was required from a neighbouring project's `node_modules` through `createRequire` of that project's `package.json`, which avoids an install; it launched the installed Chrome by channel (checked 2026-10). Waiting for `document.fonts.ready` after the network went idle was enough for CDN fonts to render; a short pause after it let the photos finish decoding. A screenshot clipped to the canvas at device scale 1 gives a PNG of exactly the canvas size.

## Fonts

A Korean sans with no italic for Hangul renders a synthetic slant where italic is asked for, which reads as a mistake; a label or a small heading the spec sets in italic was set upright in the spec's label color unless the face has a true italic, said at the checkpoint (checked 2026-10). A condensed width the spec measured was reached with `font-stretch` where the face supports it, else a horizontal `transform: scaleX()` on the text block. A display face the spec named was served by its distributor as a single `.woff` file and no stylesheet; an `@font-face` rule in the page's head with that URL loaded it, and the static server had to know the `.woff` type to serve a local copy (checked 2026-10). A heavy outline around display type, as some accounts set their covers, is `-webkit-text-stroke` with `paint-order: stroke fill`, so that the stroke sits behind the fill and does not thin the letters.

## Rendering

A body sentence of the spec's maximum characters fit one line at the spec's sizes in a column of the canvas width less the margins; sentences a few characters over wrapped, which the review caught on the PNG and not in the grid, where the scaled slide hides it (checked 2026-10). A source tag placed top-right collided with text inside a photo at the top-right; the tag moved to the bottom-right on that slide. An agency logo at the bottom-center of a collage half was cropped out with a scale transform of 1.3 and its origin at the top; a logo at a corner needed an origin a little away from the opposite corner, and the first guess cut the sign the slide was about, so the crop is checked on the PNG. On a format that stacks two 16:9 frames whole on a 4:5 canvas, each frame at the canvas width is 1080 by 607.5 and the two leave 67.5 pixels above and below; the spec's measured margins decided the rounding, and the frames' own logos and captions stayed as the account keeps them (checked 2026-10). A cover made from a picture inside a frame (a photograph shown on a broadcast) was cropped and scaled 1.8 times to fill the canvas and read soft but recognizable; the factor goes in the checklist.
