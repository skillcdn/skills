# The format spec

The format spec is what a card-news account's posts look like, measured and written down so that a new post can be built in the same shape: the canvas, each slide type with its anatomy, the text density, the register, the caption conventions, what the account never does, and the nearest fonts and colors. The study skill writes it as a JSON file (`format-spec.json`) beside a short notes page (`style-notes.md`); the build skill reads both before it plans a single slide. The example JSON the study skill ships is the shape; this page says what each field means. Numbers in this page are illustrative; the spec carries the measured values, and marks as an estimate anything read by eye rather than counted.

## Fields

| Field | Holds | Obtained from |
|---|---|---|
| `account` | The handle studied, the day it was read, how many posts were visible without signing in and how many were read. | The profile. Stays in the user's spec; never in a skill's files. |
| `categories` | The kinds of story the account posts, each with its share of the visible posts and one example line (a caption's first line, quoted to identify the post). | The profile grid and the captions of the visible posts. |
| `cadence` | Posts per day or per week, counted from the visible posts' dates. | The post pages. |
| `canvas` | The ratio of a slide (4:5 portrait is common) measured on the post pages, the platform's documented pixel size for that ratio with the day it was looked up, and the slides per post as a range with a typical count. | The post pages for the ratio and the dot count; the platform's help pages for the size. |
| `cover` | The anatomy of the first slide: photo treatment (full-bleed, gradient at the bottom), the label (its kind of words, color, weight, italic or not, position), the headline (lines, characters per line, weight, color, style). The cover is described here and not in `slide_types`. | Two or more covers, side by side. |
| `slide_types` | One entry per slide type the account uses other than the cover, each with a name, the anatomy, the content it carries, the posts it was seen in, and `tentative` when seen in one post only. Expect a story slide (photo, one-line sub, three sentences), a note slide (photo only, a short serif line), a collage, a lead slide (two-line sub, small body, a source tag) and a poster slide (large type, a date or a list) when the account runs events or lists. | Every slide of the posts read, grouped by what repeats. |
| `density` | Per slide type: sub length in characters, sentences per slide, characters per sentence, lines per slide, one fact per sentence or not, where detail goes (the caption). Counts, with the most common value and the range. | Counted on the slides, in the account's script. |
| `register` | How the slides are written and how the caption is written, as patterns with what sounds wrong beside what sounds right: headline style, sub style, body endings, the caption's voice, the phrasings that would not appear. Named in the devices of the account's language. | The slides and the captions read side by side; described in English, the account's own sentences not copied. |
| `caption` | The order of the caption's parts (facts with a date and a source, context, a closing line, mentions, a photo credit line) and the credit line's exact pattern. | Three or more captions. |
| `variants_by_content` | Which slide type the account uses for which kind of content (a list, a date, a quote, a number, a mood), so that the build chooses by content rather than by habit. | Where each variant appeared and what it carried. |
| `never` | Statements of what the account does not do, each naming the kind of post it holds for and how many of that kind were read: a call to action on a story post, numbers as overlays, a box on a photo, text on every slide. Only from a kind read two or more times. | Absence across the posts read. |
| `fonts`, `colors` | The nearest free web fonts for the display and the serif faces, with where to load them and the observed weights, each marked `guess` when identified by letterforms; the label color, the text color, the gradient's darkness and the dim overlay as hex or rgba, each marked `estimate`. | The slides at zoom. |
| `posts_read` | The post ids read slide by slide with their kinds and slide counts, so that a later run does not re-read them and a research knows what the account has already covered. | The run. |

## How the build reads it

The build takes `canvas` and the typical slide count as its frame, `density` and `register` as the checks every sentence passes, `cover` and `slide_types` with `variants_by_content` as the catalogue it picks layouts from, `caption` as the template of its caption, and `fonts` and `colors` as its CSS tokens. A field missing from the spec is derived from the build skill's own defaults and said so at the plan checkpoint.

## Example

The study skill ships [`format-spec.example.json`](../../skills/instagram-cardnews-format-study/assets/format-spec.example.json) with placeholder values in this shape.
