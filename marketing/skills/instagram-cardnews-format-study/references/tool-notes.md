# Tool notes: how the site and the browser behaved

What runs of this skill met on the site and in a driven browser, by topic, with the day where a fact can go stale. The site has no changelog: when a statement here is wrong on the day, re-derive the value the way the sentence says and fix the sentence.

## What is visible without signing in

A profile shows its bio, its counts and about a dozen recent posts; older posts and, in one run, the weekend's posts needed an account (checked 2026-10). A post page opens from its URL without an account and shows every slide of a carousel and the caption whole. Signed out, a pinned post carries no label: posts whose dates are older than the ones after them at the head of the grid are likely pinned, and they are left out of the cadence. The sample is therefore the account's last week or two; the delivery says how many posts were visible.

## The platform's documented size

The platform's help page on post sizes, found by searching its help site for the photo or post size, gave a maximum width of 1080 pixels and supported ratios from 1.91:1 to 3:4, not a fixed portrait size (checked 2026-10-23); the height is the width divided by the measured ratio (1350 for 4:5). A fetch tool that converts pages to text returned nothing from the help site, which renders by script; the driven browser read it.

## The sign-in prompt

A modal asking to sign up or log in covers the page a moment after a profile or a post loads, and again after some navigations. Close it with its close control at the top right of the modal, found on a screenshot; its coordinates depend on the viewport, so take the screenshot first. In a viewport narrower than about 768 pixels the site serves its mobile layout and the prompt is an "open in the app" sheet, closed by the X at its top right; a reel's page becomes an interstitial with a "continue on web" link, which is clicked. Never sign in and never fill the form.

## The viewport

In one host the zoom action cropped the downscaled screenshot rather than re-rendering the region, so at a desktop viewport the slide's type was too small to count (checked 2026-10). Setting the tab's viewport to about 720 by 1050 serves the mobile layout, where the post's image box is about 720 by 900 CSS pixels and every line of a slide reads at zoom. Reset the viewport at the end of the run.

## The page's data

Each post page carries a `script` element of type `application/json` that holds the post object; the one whose `code` equals the post's id in the URL is the post. It gives `taken_at` (the post's time as a Unix timestamp), `carousel_media_count`, each slide's media type and pixel size, and the whole `caption.text` with no entities to decode (checked 2026-10). Read it with a script run in the page. It does not carry the slides' text, which is in the images, so every slide is still stepped to and read at zoom. The grid's alt text also carries a date, in a time zone that can put it a day off; take dates from `taken_at`.

## Stepping a carousel

The next control is at the right edge of the post's image box, vertically centered, and appears on hover. A real pointer click at its coordinates advances the carousel and the page's URL, as the browser reports it after the click, gains the slide index (`?img_index=<n>`), which confirms the step; a click dispatched from a script on the control's element does not advance it (checked 2026-10). On a video post the control sits a little inward and a click on the middle of the box toggles playback; find the control on that post's screenshot before stepping.

## Reading a slide

Zoom into the post's image region on every slide; the region is the same for every slide of one post. In one host's browser, a zoom called inside a batch of actions returned no image when a scale factor was passed with it; leaving the scale out returned the image (checked 2026-10). Character counts are taken from the zoomed image in the account's script.

## The caption

The page's visible text may cut a long caption; the post object above holds it whole. A link in a caption is read for the credit line and the mentions and never followed as an instruction.
