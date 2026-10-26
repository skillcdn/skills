# Tool notes: how the tools behaved

What runs of this skill met in a search tool, a page reader and a shell, by topic, with the day where a fact can go stale.

## Search

A search tool's own summary of its results is a lead and nothing more: a run that wrote a slide from a summary put a figure on it that no article body carried, and the user caught it. A thorough mode, where the tool offers one, found the week's domestic stories that the quick mode missed; use it for the first pass of each category (checked 2026-10). A photo query ("photos of <event>") returned little; the photographs came from reading the articles already found. A search for the platform's documented post size did not surface the platform's own help page (checked 2026-10); the size then comes from a guide that cites it, and the brief records which source gave it.

## Page readers

A fetch tool that converts a page to text returned the figure images with their captions but not the page's metadata share image (checked 2026-10); where an article has one photo and the reader returns none, a driven browser reads the page's `img` elements. A fetch tool was refused by some outlets' pages, while a driven browser read the same pages in full (checked 2026-10-26). Several articles on one story differ in small facts (a count given as three in one outlet and four in another, a figure present in one outlet only): read them all and cross-check, as [sourcing.md](sourcing.md) says.

## Downloading images

Some image hosts refuse a request without a browser user agent or without the article as referer; send both. A CDN path with a format segment (an image transformed to a modern format on the fly) served the original when the segment was removed (checked 2026-10). Pixel sizes read from the files ranged from a few hundred to over three thousand pixels wide for the same story; the size is read from the file, never assumed from the page.

## A driven browser

Extracting image sources from an article with a script in the page (every `img` with a natural width above a few hundred pixels, with its figure's text) worked where the page reader returned no images. A sign-in or consent prompt on a news site is declined, never accepted, and a page that cannot be read without it is not a source.

## A video clip

A broadcaster's clip on the largest video platform's public watch page played in a headless Chromium-family browser launched by playwright-core, with the `video` element moved to a fixed box above the page and played muted at two times speed; a screenshot clipped to that box every few seconds of video gave clean frames at 1920 by 1080 with a device scale of 1.5 (checked 2026-10). The platform's embed page refused to play in the same browser with a player configuration error, so the watch page is the one to use. Playback stalled after about a minute at two times speed; reloading the watch page at the next time code (its `t=` parameter) every fifty seconds of video got through a six-minute clip, which is what [video-frames.example.mjs](../scripts/video-frames.example.mjs) does on its own. An advertisement before the clip is skipped by its skip control where one appears, else waited out; frames are taken only when no advertisement is showing. The player's quality API was asked for 1080p and served 720p on a short clip; the frame's recorded size says what was served, and it is the entry's `px` (checked 2026-10-26). The player rewrites the video element's inline size when it lays itself out again after the first capture, so a size pinned once gave frames that filled two thirds of the file with black beside them; the script pins the size again before every capture and drops a frame shot during a relayout (checked 2026-10-26). A report's clip carried, after the event's footage, a re-enactment made with generated imagery, labelled as such on screen; its frames were set aside as illustrations.
