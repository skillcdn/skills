# Tool notes: how the tools behaved

What runs of this skill met in a search tool, a page reader and a shell, by topic, with the day where a fact can go stale. What holds for any page reader, download or clip is in the repository's [reading-pages.md](/docs/browser/reading-pages.md), included with this skill, and [video-frames.md](/docs/browser/video-frames.md); this page holds what this skill's own phases met.

## Search

A search tool's own summary of its results is a lead and nothing more: a run that wrote a slide from a summary put a figure on it that no article body carried, and the user caught it. A thorough mode, where the tool offers one, found the week's domestic stories that the quick mode missed; use it for the first pass of each category (checked 2026-10). A photo query ("photos of <event>") returned little; the photographs came from reading the articles already found. A search for the platform's documented post size did not surface the platform's own help page (checked 2026-10); the size then comes from a guide that cites it, and the brief records which source gave it.

## Page readers

Which tool reads what, and what a fetch tool returned or refused, is in reading-pages.md "Which tool reads a page". Several articles on one story differ in small facts (a count given as three in one outlet and four in another, a figure present in one outlet only): read them all and cross-check, as [sourcing.md](sourcing.md) says.

## Downloading images

How a file is requested (one at a time, a browser user agent, the article as referer, a transform segment removed) and measured is in reading-pages.md "Downloading a file"; the size is read from the file, never assumed from the page. A sign-in or consent prompt on a news site is declined, never accepted, and a page that cannot be read without it is not a source (reading-pages.md "Walls").

## A video clip

The watch page rather than the embed, the `video` element pinned over the page, the stall at a raised rate and the reload at the next time code, the advertisements, the served quality and the relayout that the script pins against are in [video-frames.md](/docs/browser/video-frames.md) "A watch page in a headless browser", which is what [video-frames.example.mjs](../scripts/video-frames.example.mjs) does on its own; a six-minute clip was captured that way (checked 2026-10-26). The frame's recorded size is what was served, and it is the entry's `px`. A report's clip carried, after the event's footage, a re-enactment made with generated imagery, labelled as such on screen; its frames were set aside as illustrations.
