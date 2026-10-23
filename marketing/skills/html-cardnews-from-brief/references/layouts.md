# Layouts: the catalogue, choosing by content, the defaults

The layout types a card-news post is composed from, what each carries, how one is chosen for a beat, and the CSS values that stand in when the spec gives none. The catalogue's names are the classes of the page; the spec's `cover` and `slide_types` anatomy override the defaults of the class they map to (a spec's `poster` is list, time or stat by what the beat carries). The defaults are illustrative, measured once on one account's format (checked 2026-10), and a build on them says so at the plan checkpoint.

## The catalogue

| Type | Carries | Anatomy |
|---|---|---|
| Cover | The headline | Full-bleed photo; gradient over the lower 60% to about 80% black; the series label above the headline in the spec's color, weight and italic; two lines of display type, bottom-left, inside the margins. |
| Story | One beat in sentences | Full-bleed photo with the bottom gradient; a one-line sub in heavy type; three to four sentences in regular type below it, bottom-left. |
| Note | A mood, a quote, a scene | Full-bleed photo; a serif note of two to four lines, top-right and right-aligned, or top-left when the photo's right side is busy; a top gradient when the photo is bright there. The lines come from an image caption or a quoted source sentence in the brief, shortened to the spec's line length, never from the agent's head. |
| Lead | One item with its source | Full-bleed photo with the bottom gradient; a two-line sub in larger heavy type, one or two short sentences in smaller regular type, a small source tag in the corner away from the photo's text. |
| List poster | A list of places, items or names | Full-bleed photo under a dim overlay; a kicker, a heading, a numbered list in two columns with a hairline under each row and a small tag at the row's end (a district, a category); a footer line for the rest of the list and one sentence of context. |
| Time poster | A date, a time span, a route | Dim photo; a kicker, the date line, the time span in very large figures with an arrow between, the route line, two or three notes in smaller type. |
| Stat | Two to four numbers | Dim photo; a kicker and a heading; one row per number with the figure in very large type and its unit, a label and a one-line detail beside it, hairlines between rows; a footer sentence. |
| Collage | Two related images and one beat | Two photos stacked (both landscape) or side by side (both portrait); the sub and sentences as the story type over the bottom gradient. |

A photo-only slide with no note is a note type with the note empty, and it is allowed where the thread has a beat that is the photo.

## Choosing a layout

| The beat carries | Type | Why |
|---|---|---|
| One fact or a cluster of related facts in sentences | Story | The format's default; the sentences are the content |
| A short list of two or three items with one source | Lead | The sub carries the items, the tag the source |
| A list of five or more places, names or items | List poster | Sentences cannot carry a list a reader scans; the type can |
| A date and a time span, a route, a deadline | Time poster | The figures are what a reader saves; type, not a sentence |
| Two to four numbers that make the point | Stat | A number in a sentence is read once; a number in display type is remembered |
| A quote, a mood, a scene with no fact | Note | The photo is the content; a line sets its tone |
| Two images that belong together | Collage | One beat, two views |

The spec's `variants_by_content` overrides this table where the account does something else for that content. A beat that fits two types takes the one the account uses for that content; failing that, the one that has not appeared in this post.

Variation: a story slide may follow a story slide; no other type repeats consecutively; a post that carries a list, a time or numbers gives each its own type rather than a story slide; and no two posts of one account built by this skill share a sequence of types, which the plan checks against the `post/slide-plan.json` of the brief folders beside this one.

## Photos under each type

- The crop is the image's object position; a mark, a logo or a credit at an edge is cropped out by a scale transform with its origin away from the mark, by only as much as the mark needs, and the result is checked on the PNG.
- A dim overlay (list, time, stat) sits between the photo and the type; the gradient (cover, story, lead, collage) covers the lower part; a note gets a top gradient when its region is bright.
- An image whose licence forbids modification takes no crop, overlay or gradient: it is placed whole at its own ratio, centered on the spec's dark color (the default's dim black), on a note slide with the note in the band above or below it, or not used. An image whose terms are unknown is cropped and dimmed as the layout needs, with its credit.
- A source tag sits in the corner away from any text in the photo.

## Defaults when the spec gives none

Canvas 1080 by 1350, or the platform's documented portrait size looked up at run time. Margins 72 on the sides, 150 from the bottom for text blocks; posters and stats run from 120 to 120 from the top and the bottom with 84 at the sides; a note starts 140 from the top at a width of up to 640. Gap between a sub and its body 34; between a kicker and its heading 14; between stat rows 30 above and 34 below the hairline.

Fonts: a free sans that covers the post's script with weights 400 and 800, loaded from its distributor's documented CDN path (found by searching the family's name with "CDN"); a free serif in the same script at weight 500 for notes; the plan checkpoint names the families chosen.

Sizes: label 30 italic 800; headline 72 at line height 1.28, weight 800; sub 46 weight 800; body 31 weight 400 at line height 1.62; note 34 serif at 1.7; lead sub 54, lead body 28; poster and stat kicker 30 italic, heading 60 weight 800 at 1.2; list rows 34 weight 600 with 28 numbers and 24 tags, the footer 27 at 1.6; time date line 54 weight 800, figures 150 weight 800 with the arrow at 60, route line 40 weight 600, notes 28 at 1.65; stat figures 112 weight 800 with 44 units, label 34 weight 700, detail 30 at 1.5, footer 28 at 1.6; tags 24.

Colors: text white; a label in a saturated accent that reads on a dark photo (the account's accent when the spec names one, else a warm yellow); hairlines white at 22% to 28% opacity; secondary text white at 65% to 85%; bottom gradient from transparent to rgba(0,0,0,.8); top gradient to rgba(0,0,0,.62); dim rgba(0,0,0,.62). These are one account's measurements and they are only a stand-in: a build on them is said to be one at the plan checkpoint.
