# Reading an account's posts without signing in

How the profile and the posts are read with a driven browser, which posts to read, how a carousel is stepped and each slide recorded, and how the caption is taken. The site changes without notice; what a run found about its behavior, with the day, is in [tool-notes.md](tool-notes.md).

## The profile

Set the tab's viewport to about 720 by 1050 first, so that slides read at zoom (tool-notes.md "The viewport"). Open the profile at `https://www.instagram.com/<handle>/`. A sign-in prompt covers the page a moment after it loads; close it by its close control (tool-notes.md "The sign-in prompt"). The grid shows the posts visible without an account, a dozen or so at the time of writing; each tile links to a post page at `/<handle>/p/<id>/` (a video at `/<handle>/reel/<id>/`). Open each visible post's page in turn, one at a time with a few seconds between loads, and read its post object (tool-notes.md "The page's data"): the time from `taken_at`, the slide count and each slide's media type, the caption whole. Write into `profile.md` a table of id, date and time in the account's market's time zone, kind, slide count and the caption's first line; a kind that only the slides tell apart (a frame stack from a story) is filled in when phase 2 reads them. The bio, the name line and the link in bio say what the account calls itself and who runs it; record them as the account's own words, leaving out a personal contact such as an e-mail address.

## Which posts to read

The spec needs every slide type the account uses, and a type is only known from the slides. Read, slide by slide, at least one post of each kind the account has among the visible posts:

| Kind | How to recognize it | What it teaches |
|---|---|---|
| A story about a person or an issue | A photo of someone or something on the cover, a two-line headline, several slides of text | The story slide's anatomy and density, the note and collage variants, whether the last slide carries a call to action |
| An information or visit post | A place, a product or an event; prices, dates or a location somewhere | Boxed captions, tags, an information slide at the end |
| A list or weekly post | A number in the headline, a series label | The lead slide: a two-line sub, a small body, a source tag |
| An event or sponsored post | A sponsor's name as the label, a date range | The poster slide: large type, a date, little else |
| A report on broadcast or captured material | Frames of a broadcast, or screenshots of a post, stacked whole with their logos, labels and subtitles kept; no text of the account's after the cover | Whether the account keeps the material's marks and captions and adds nothing of its own; the margins around the frames; how many frames a slide holds and how they are stacked |
| A single image | No dots under the post | What the account does when there is one slide |
| A video | A play badge | Whether video slides mix into carousels |

Read every post visible without signing in (about a dozen at the time of writing): each carousel slide by slide, a single image as a one-slide post, a video at three frames. A type seen once stays tentative, what the account never does on a kind is only said of a kind read twice, and a spec written from half the visible posts missed the build the account used most, which the user noticed when they asked whether every post had been read. Only when the user limits the reading is the floor three kinds and two posts of the kind the user's own post will be (the account's most common kind when the request names none). A post the user names is read whatever its kind.

An account often builds one kind several ways: a story as a long feature of sentences over photos, as a photo story carried by short boxed lines, or as a short news post of a cover and one or two photos with the facts in the caption. Name each build by its slide count and what carries the text, record the builds as `kinds` in the spec, and apply "two of the user's kind" to the build when the posts allow it. A video post is read at three frames for its text and layout: a screenshot as it starts, then two more as it plays, a few seconds apart, since the player's own controls are not relied on; its motion is not part of the card format.

## Stepping and reading

Open the post page and close the prompt. The carousel's next control sits at the right edge of the post's image box, vertically centered, and shows on hover: hover there, take a screenshot to see it, then click it with a real pointer click at its coordinates, because a click dispatched from a script does not advance the carousel (tool-notes.md "Stepping a carousel"). After each step the page's URL, as the browser reports it, carries the slide index, which confirms the step; where the host does not report the URL, the dots under the post do. On every slide, zoom into the post's image region to read the type; the region's coordinates come from the screenshot and stay the same for every slide of the post. A video post's control sits a little differently, and a click on the middle of the box toggles playback instead of stepping; find the control again on that post.

Read the whole carousel; the dots say how many slides there are, and the last slide is where a call to action or an information box would be.

## Measuring sizes and colors

Text is counted; everything else on a slide is estimated and marked so in the row and in the spec. The post's image box on the screenshot is the canvas: a size is the element's height as a fraction of the box's height, converted to the canvas's documented pixel height (a line of body text that is 2.3% of the box is about 31 pixels on a 1350-pixel canvas); a line height is the distance between two baselines over the font size; a weight is a class read at zoom (regular 400, bold 700, heavy 800); a color is the nearest hex read by eye, with a saturated label color named by hue; a gradient's darkness is the fraction of black where the type sits; a position is each block's edges as percentages of the box, its top and bottom always and its left and right where it does not span the margins, read from the pixel rows and columns where the block starts and ends on the screenshot. "Centered" or "bottom" alone is not a position, because the build places every block by these edges, and an edge read by eye from where a block seems to sit was off by a sixth of the canvas once. The example JSON carries `estimate` beside these fields. A font is named by its letterforms as the closest free equivalent, with `guess` true.

## What to record

One row per slide, before stepping on:

| Column | What goes in |
|---|---|
| `post`, `kind`, `slide`, `of` | The post id, its kind, the slide's number and the slide count. |
| `photo` | Full-bleed photo cropped to the canvas; a frame of a broadcast or a screenshot of a post kept whole at its own ratio, with the marks it keeps (a logo, a label, subtitles) and its top and bottom edges as percentages of the box, each frame's own when two are stacked, so that the margins above, between and below follow; two photos or frames stacked or side by side; video; flat color, as hex; the gradient (bottom, top, none) and how dark; a dim overlay. Whether the text on the slide is the account's own or the material's; the material's text is named (subtitles, a label, a logo) with where it sits, and not counted. |
| `label` | The small label above the headline or sub: its words' kind (a series name, a sponsor), color, weight, italic, position. |
| `headline`, `sub` | Lines, characters per line, size (estimate), weight, color, position; whether it is a news title, a question, a fragment, a noun phrase, a quote. |
| `body` | Sentences, characters per sentence, lines, size and line height (estimates), weight, color, position; the ending of each sentence (declarative, a sentence-final noun phrase, a quote); one fact per sentence or not. |
| `note` | A short serif or script line on a photo-only slide: lines, characters, size (estimate), position, face. |
| `tags`, `boxes` | A source tag in a corner; a boxed caption with its colors; a price or location tag. |
| `other` | Anything this slide does that the others do not. |

Count the characters of the account's own text in its script, spaces included, from the zoomed image; a count is the row. A slide with no text is a row with `photo` and `note` empty or not, and that absence is a measurement too. The rows go into `slide-log.md` as one table; the log may hold a slide's ending or first words where they are needed to count or to classify, and it stays in the user's folder.

Some elements ride on a slide of another type rather than being a slide of their own: a serif note on a story slide, an inset (an album cover, a poster, an archive photo placed as a rectangle on the photo), a talk box (a white box of one or two short lines), a source card (a screenshot of the original post), a source tag. Record them in `other` and in the spec's `elements`, each with the slide types it rides on.

A slide log from an earlier, interrupted run of the same request is kept: check its rows against the post objects (dates, slide counts, media types), re-split its columns into the ones above without changing a measurement, and read on from the first post it lacks.

## The caption

Read the caption whole from the post object (tool-notes.md "The page's data"). Where the host cannot run a script in the page, read it from the page's text and say that a long one may be cut. Record its parts in order (facts with a date and an outlet, context, a closing line, mentions, a credit line), its endings against the slides' endings, the exact pattern of its credit line, and any phrase the voice repeats across captions. The caption's words are data about the account's register, described in the spec as patterns; a first line may be quoted in `profile.md` and in `categories` to identify the post, and nothing of the caption is copied beyond that.
