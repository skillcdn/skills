# Tool notes: how the tools behaved

What runs of this skill met in a search tool, a page reader and a shell, by topic, with the day where a fact can go stale.

## Search

A search tool's own summary of its results is a lead and nothing more: a run that wrote a slide from a summary put a figure on it that no article body carried, and the user caught it. A thorough mode, where the tool offers one, found the week's domestic stories that the quick mode missed; use it for the first pass of each category (checked 2026-10). A photo query ("photos of <event>") returned little; the photographs came from reading the articles already found. A search for the platform's documented post size did not surface the platform's own help page (checked 2026-10); the size then comes from a guide that cites it, and the brief records which source gave it.

## Page readers

A fetch tool that converts a page to text returned the figure images with their captions but not the page's metadata share image (checked 2026-10); where an article has one photo and the reader returns none, a driven browser reads the page's `img` elements. Several articles on one story differ in small facts (a count given as three in one outlet and four in another, a figure present in one outlet only): read them all and cross-check, as [sourcing.md](sourcing.md) says.

## Downloading images

Some image hosts refuse a request without a browser user agent or without the article as referer; send both. A CDN path with a format segment (an image transformed to a modern format on the fly) served the original when the segment was removed (checked 2026-10). Pixel sizes read from the files ranged from a few hundred to over three thousand pixels wide for the same story; the size is read from the file, never assumed from the page.

## A driven browser

Extracting image sources from an article with a script in the page (every `img` with a natural width above a few hundred pixels, with its figure's text) worked where the page reader returned no images. A sign-in or consent prompt on a news site is declined, never accepted, and a page that cannot be read without it is not a source.
