# Tool notes: how the tools behaved

What runs of this skill met in the host's preview, in Node.js and in the headless browser, by topic, with the day where a fact can go stale.

## The host's preview

A page opened as a file in one host's browser pane rendered as a static snapshot: the layout showed, the relative images did not (checked 2026-10). A page with its images inlined as data URLs grew past four megabytes and did not open at all. Serving the folder with a small static server fixed both; the host's preview tool started the server from its launch configuration and assigned a port of its own, which the server reads from the environment.

## Node.js

A project whose `package.json` declares `"type": "module"` runs a `.js` file as an ES module, and a `require` in it fails with a reference error; the server and the export script are written as ES modules so that they run anywhere (checked 2026-10). A long file written through a shell heredoc on Windows can land truncated; write files with the editor's file tools.

## playwright-core

`playwright-core` was required from a neighbouring project's `node_modules` through `createRequire` of that project's `package.json`, which avoids an install; it launched the installed Chrome by channel (checked 2026-10). Waiting for `document.fonts.ready` after the network went idle was enough for CDN fonts to render; a short pause after it let the photos finish decoding. A screenshot clipped to the canvas at device scale 1 gives a PNG of exactly the canvas size.

## Rendering

A body sentence of the spec's maximum characters fit one line at the default sizes in a column of the canvas width less the margins; sentences a few characters over wrapped, which the review caught on the PNG and not in the grid, where the scaled slide hides it (checked 2026-10). A source tag placed top-right collided with text inside a photo at the top-right; the tag moved to the bottom-right on that slide. An agency logo at the bottom-center of a collage half was cropped out with a scale transform of 1.3 and its origin at the top; a logo at a corner needed an origin a little away from the opposite corner, and the first guess cut the sign the slide was about, so the crop is checked on the PNG.
