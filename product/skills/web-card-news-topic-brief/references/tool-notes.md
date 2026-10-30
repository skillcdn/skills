# Tool notes: how the tools behaved

What runs of this skill met in a search tool, a page reader and a shell, by topic, with the day where a fact can go stale. What holds for any page reader, download or clip is in the repository's [reading-pages.md](/docs/browser/reading-pages.md), included with this skill, and [video-frames.md](/docs/browser/video-frames.md); this page holds what this skill's own phases met.

## Search

A search tool's own summary of its results is a lead and nothing more: a run that wrote a slide from a summary put a figure on it that no article body carried, and the user caught it. A thorough mode, where the tool offers one, found the week's domestic stories that the quick mode missed; use it for the first pass of each category (checked 2026-10). A run on a Korean domestic category found few of the week's stories through the search tool even in its thorough mode, and the week came instead from a portal's news search page, filtered to the past seven days and sorted by date, read with a plain request page by page (Daum's, checked 2026-10), while another portal's search page refused the fetch tool (Naver's, checked 2026-10); the portal's own article pages read fine with the fetch tool. A photo query ("photos of <event>") returned little; the photographs came from reading the articles already found. A search for the platform's documented post size did not surface the platform's own help page (checked 2026-10); the size then comes from a guide that cites it, and the brief records which source gave it.

## Page readers

Which tool reads what, and what a fetch tool returned or refused, is in reading-pages.md "Which tool reads a page". A fetch tool of one host returned a summary of the article rather than its text (checked 2026-10): a lead and not a reading, so the article was read from its HTML by a plain request, as that page says. Several articles on one story differ in small facts (a count given as three in one outlet and four in another, a figure present in one outlet only): read them all and cross-check, as [sourcing.md](sourcing.md) says.

## Downloading images

How a file is requested (one at a time, through the browser that read the page where there is one, a transform segment removed where the host serves the original) and measured is in reading-pages.md "Downloading a file"; the size is read from the file, never assumed from the page. A sign-in or consent prompt on a news site is declined, never accepted, and a page that cannot be read without it is not a source (reading-pages.md "Walls").

## A video clip

The watch page rather than the embed, the `video` element pinned over the page, the one reload on a stall, the advertisements, the served quality and the relayout that the script pins against are in [video-frames.md](/docs/browser/video-frames.md) "A watch page in a headless browser", which is what [video-frames.example.mjs](../scripts/video-frames.example.mjs) does on its own; a clip of several minutes was captured with the pinned element and reloads at a raised rate (checked 2026-10), and the present setting, normal speed with one reload on a stall, is untried. The frame's recorded size is what was served, and it is the entry's `px`. A clip may carry, after the footage, a re-enactment made with generated imagery and labelled as such on screen: its frames are set aside as illustrations.
