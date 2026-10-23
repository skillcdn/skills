# Reading an account's posts without signing in

How the profile and the posts are read with a driven browser, which posts to read, how a carousel is stepped and each slide recorded, and how the caption is taken. The site changes without notice; what a run found about its behavior, with the day, is in [tool-notes.md](tool-notes.md).

## The profile

Open the profile at `https://www.instagram.com/<handle>/`. A sign-in prompt covers the page a moment after it loads; close it by its close control (tool-notes.md "The sign-in prompt"). The grid shows the posts visible without an account, a dozen or so at the time of writing; each tile links to a post page at `/<handle>/p/<id>/` (a video at `/<handle>/reel/<id>/`). The grid shows neither dates nor captions: open each visible post's page in turn, one at a time with a few seconds between loads, and read there its date, the first line of its caption and whether it is a carousel, a single image or a video (the grid's badges and the post page's dots say which). Write them into `profile.md` as a table. The bio, the name line and the link in bio say what the account calls itself and who runs it; record them as the account's own words.

## Which posts to read

The spec needs every slide type the account uses, and a type is only known from the slides. Read, slide by slide, at least one post of each kind the account has among the visible posts:

| Kind | How to recognize it | What it teaches |
|---|---|---|
| A story about a person or an issue | A photo of someone or something on the cover, a two-line headline, several slides of text | The story slide's anatomy and density, the note and collage variants, whether the last slide carries a call to action |
| An information or visit post | A place, a product or an event; prices, dates or a location somewhere | Boxed captions, tags, an information slide at the end |
| A list or weekly post | A number in the headline, a series label | The lead slide: a two-line sub, a small body, a source tag |
| An event or sponsored post | A sponsor's name as the label, a date range | The poster slide: large type, a date, little else |
| A single image | No dots under the post | What the account does when there is one slide |
| A video | A play badge | Whether video slides mix into carousels |

Three kinds at least, and two posts of the kind the user's own post will be (the account's most common kind when the request names none), because what the account never does on a kind is only said of a kind read twice. A post the user names is read whatever its kind.

## Stepping and reading

Open the post page and close the prompt. The carousel's next control sits at the right edge of the post's image box, vertically centered, and shows on hover: hover there, take a screenshot to see it, then click it with a real pointer click at its coordinates, because a click dispatched from a script does not advance the carousel (tool-notes.md "Stepping a carousel"). After each step the page's URL, as the browser reports it, carries the slide index, which confirms the step; where the host does not report the URL, the dots under the post do. On every slide, zoom into the post's image region to read the type; the region's coordinates come from the screenshot and stay the same for every slide of the post. A video post's control sits a little differently, and a click on the middle of the box toggles playback instead of stepping; find the control again on that post.

Read the whole carousel; the dots say how many slides there are, and the last slide is where a call to action or an information box would be.

## Measuring sizes and colors

Text is counted; everything else on a slide is estimated and marked so in the row and in the spec. The post's image box on the screenshot is the canvas: a size is the element's height as a fraction of the box's height, converted to the canvas's documented pixel height (a line of body text that is 2.3% of the box is about 31 pixels on a 1350-pixel canvas); a line height is the distance between two baselines over the font size; a weight is a class read at zoom (regular 400, bold 700, heavy 800); a color is the nearest hex read by eye, with a saturated label color named by hue; a gradient's darkness is the fraction of black where the type sits. The example JSON carries `estimate` beside these fields. A font is named by its letterforms as the closest free equivalent, with `guess` true.

## What to record

One row per slide, before stepping on:

| Column | What goes in |
|---|---|
| `post`, `kind`, `slide`, `of` | The post id, its kind, the slide's number and the slide count. |
| `photo` | Full-bleed photo, two photos stacked or side by side, video, flat color; the gradient (bottom, top, none) and how dark; a dim overlay. |
| `label` | The small label above the headline or sub: its words' kind (a series name, a sponsor), color, weight, italic, position. |
| `headline`, `sub` | Lines, characters per line, size (estimate), weight, color, position; whether it is a news title, a question, a fragment, a noun phrase, a quote. |
| `body` | Sentences, characters per sentence, lines, size and line height (estimates), weight, color, position; the ending of each sentence (declarative, a sentence-final noun phrase, a quote); one fact per sentence or not. |
| `note` | A short serif or script line on a photo-only slide: lines, characters, size (estimate), position, face. |
| `tags`, `boxes` | A source tag in a corner; a boxed caption with its colors; a price or location tag. |
| `other` | Anything this slide does that the others do not. |

Count characters in the account's own script, spaces included, from the zoomed image; a count is the row. A slide with no text is a row with `photo` and `note` empty or not, and that absence is a measurement too. The rows go into `slide-log.md` as one table.

## The caption

Read the caption whole: from the page's text where the host shows it entire; else run a short script in the page that returns the document's HTML, search it for the caption's first words as shown on the page, and take the whole text from there to its closing quote, with the HTML entities decoded (a shell with Node.js decodes them; the browser is the only thing that touched the site). Record its parts in order (facts with a date and an outlet, context, a closing line, mentions, a credit line), its endings against the slides' endings, the exact pattern of its credit line, and any phrase the voice repeats across captions. The caption's words are data about the account's register, described in the spec as patterns; a first line may be quoted in `profile.md` and in `categories` to identify the post, and nothing of the caption is copied beyond that.
