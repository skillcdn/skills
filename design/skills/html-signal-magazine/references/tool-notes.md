# Tool notes: capturing a site, the driver, the PDF

What the tools did where an issue met them: the brand site's capture, the browser driver, a PDF that grows, the files' names. Read when a step meets one of these.

## A site with no language path

A brand site may serve its languages at one address and answer a language path (`/ko/`, `/en/`) with a 404. Capture the root address, with the reader's language in the request's `Accept-Language` where the site chooses by it, and say in `brand.md` which address was read.

## What a scroll reveals

A full-page capture of a site that fades its sections in as they scroll into view shows them blank. Request reduced motion for the page (`reducedMotion: "reduce"` in the browser context, the `prefers-reduced-motion` media feature) before the capture: most sites then show every section at once. Where one still hides a section, scroll to it and capture the viewport.

## The browser driver

The helper resolves `playwright-core` from its own folder unless `PLAYWRIGHT_FROM` names the `package.json` of a project that has it. A run folder has none of its own: point `PLAYWRIGHT_FROM` at a tools folder made once outside the series folder ([headless.md](/docs/browser/headless.md)), or at a project on the machine that already installed it. The helper's message "playwright-core not found" means this and nothing about the deck.

## A PDF that is too large

The helper prints the PDF's size and reports `heavy` over the deck's `pdf_max_mb`. What grew one, in the order to look:

- **A layer the browser paints as an image.** A repeated CSS gradient (dots from `radial-gradient` with a `background-size`), a blurred shape (`filter: blur`) and a blurred `box-shadow` go into the PDF as pictures, once for every slide they are on. Over a slide of text at 3 KB, one dot pattern across the slide cost about 50 KB, two such layers about 250 KB, a lit card's shadow about 50 KB and one blurred glow about 200 KB a slide; the slide's light as one plain gradient cost 2 KB (Chrome, six slides at 1920 by 1080, checked 2026-11). One issue's PDF went from 11.8 MB to 5.0 MB when a dot pattern was redrawn as a few SVG circles (illustrative).
- **How a pattern is drawn.** Where the pattern matters, a few hundred SVG shapes over the part of the slide that needs them. Not as thousands: a slide filled with 2,600 SVG circles weighed 480 KB, more than the gradient it replaced, and an SVG `pattern` fill weighed the same as the gradient.
- **Pictures.** A screen kept as PNG or WebP at several times the size it is shown at. Keep it at twice its shown size, as JPEG.
- **Finding which.** Hide one layer at a time (the pattern, the light, the pictures) with a line of CSS, render, and compare the sizes the helper prints; put back what did not matter.

## The files a reader receives

The HTML and the PDF are named for their readers, `<magazine>-<YYYY-MM>`, with no date of making in front: the name shows in a mail and in a download. The issue's own folder carries the period.
