# Building the deck: materials, the deck file, the helper

How the materials of a product deck are gathered, how the deck's source file is written, and what the helper checks. Read before phase 2.

## Materials

Everything goes into `assets/` beside `deck.html`, under a name that says what it is, and its origin goes into `facts.md` (the page it came from, the day).

- **Marks.** The product's logo and symbol from its brand file or its site, as SVG where there is one, in the variant for the ground it sits on. The mark of another product the deck names is taken from the product's own pages where they show it, else from that product's brand page (search its name with "brand assets"), and used as published: a mark drawn in the current text colour (`fill="currentColor"`) is placed inline, so that it takes the slide's ground, and nothing else of a mark is changed. Where none is found, the name in type.
- **Tokens.** The product's colors, radius and surfaces are read from its site, not picked by eye: the CSS custom properties on the root element (`getComputedStyle(document.documentElement)` in a browser, or the stylesheet itself), and the brand file where it has one. They become the deck's `:root` tokens under the deck's own names; the storyboard names their source. A product whose site and whose app differ has two sets: a screen, captured or drawn, and the ground it sits on take the app's, the other ground the site's, and the storyboard says which ground took which. Where the look came from the four looks, the pick's handoff gives them instead.
- **Font.** The brand's font by its local name first, then its documented web file, downloaded into `assets/` so that the one-file HTML embeds it ([rendering-html.md](/docs/browser/rendering-html.md) "Fonts" has where a family documents its file); the stack ends in a system face with the language's letters. A second stack (a mono face for a command) names the deck's font after its own faces: a script the mono face lacks, Hangul inside a command, then falls to the deck's font and not to a system face.
- **Results the product made.** From the site's own showcase or the user's files: the original file, its size read from the file ([reading-pages.md](/docs/browser/reading-pages.md) "Downloading a file"). Photographs are kept as JPEG: Chromium stores a WebP in the PDF decoded, where a JPEG goes in as it is, and one deck's PDF came out at 9 MB against 5.3 MB with the same pictures as JPEG (illustrative; checked 2026-11).
- **A localized page.** A site with no language path in its addresses may still serve each language at the root address, by the request's `Accept-Language` (seen on one site, 2026-11): request the page with the reader's language in that header before taking a screen or a sentence from it.

## Screens

In the order of the Inputs: handed over, captured, drawn.

- **Captured.** Open the site, the demo or the preview in the browser at a fixed viewport and a device scale of 2, so that a crop still fills its place on the slide ([headless.md](/docs/browser/headless.md) "Screenshots"). The organization's own screens are not captured: where the only screens that open are its sign-in page or its live workspace, they stay out and the screens are drawn, and a local install is a demo only where it shows nothing of the organization's. An empty environment is filled first with the cast's data, plausible and in the reader's language. Crop to the part the slide talks about.
- **Pins.** A pin on a screen is placed in percent of the image's box (`left: 63%; top: 20%`), so that it holds when the image is resized.
- **Drawn.** Where no screen can be had, the scene is drawn in HTML and CSS from what the documents say the screen holds: its regions, its nouns, its states, in the deck's tokens and with the cast's data. Draw the few elements that carry the slide's message, large enough to read on the sheet; a drawn scene is a picture of the product at work, not a replica of a screen nobody saw. The storyboard marks it "drawn" and the delivery lists it.

## The deck file

`deck.html` starts as [`deck-skeleton.html`](../assets/deck-skeleton.html) and is one file: the meta, one stylesheet, one `section.slide` per slide.

- **The canvas.** Every slide is a box of 1920 by 1080 CSS pixels with `overflow: hidden`, and every direct child of a slide is placed in the slide's own pixels (`.slide > *` is `position: absolute`). Nothing is scaled by hand.
- **What is shared.** The tokens, the slide box, the two grounds, one title class and the page number. Everything else belongs to one slide.
- **A prefix per slide.** One stylesheet holds every slide, so a class written for one scene under a general name (`.card`, `.title`, `.step`) restyles another. Every class of a slide's scene carries that slide's prefix of a few letters (`c-` on the cover, `v-` on the voices), and a rule on a ground (`.dark`, `.light`) sets colors only, never positions or sizes.
- **`data-pattern`** on the section is the storyboard's pattern for the slide. The helper reports a slide without one, and two in a row with the same.
- **`data-bleed`** on an element marks it, and what is inside it, as meant to run past the slide's edge (a collage, an enlargement). **`data-clip`** marks an element whose content is meant to be cut by its box (a screen fragment in a tile). They go on the one element that is meant, never on the slide.
- **`deck-meta`**, the JSON script in the head: `canvas` (`[1920, 1080]`), `banned` (phrases a render reports on any slide), `external` (`false` turns the house-style check off; a product deck leaves it on), and `style` where the house style differs from the usual set, in the keys [house-style.md](/docs/writing/house-style.md) "How it is checked" gives (`usual`, `forbidden`, `no_bracket_heads`).
- **Text.** The `lang` of the `html` element is the deck's language. Breaks at spaces only (the skeleton sets it); a title's break is a `<br>` placed by hand. An image fills its box with `object-fit: cover`, its `object-position` chosen so that the subject stays in.
- **Assets** are referenced by relative path (`assets/<file>`); the helper embeds each into the one-file HTML and stops on a path that is not there.

## The helper

`node render.mjs <deck.html> <out folder> [--name <file name>]`, with `PLAYWRIGHT_FROM` set where `playwright-core` is borrowed. It loads the one-file HTML in the browser, waits for the network, the fonts and the images, measures, prints the PDF at the canvas size, takes every slide as a PNG, shooting each until two shots in a row are the same image, and tiles the sheet three to a row. It exits 0 with no finding, 1 with findings (every file is still written, for a look at a draft), 2 when it cannot run, with the reason.

| Finding | Means | Fix, in `deck.html` |
|---|---|---|
| `outside` | An element reaches past the slide. | Move or shrink it; `data-bleed` only where it is meant to run off. |
| `cut` | Text longer than its box. | Fewer words or a larger box; `data-clip` only on a fragment meant to be cut. |
| `lone` | A block wraps to two lines or more and its last line is one word. | Reword, or place the break by hand. |
| `repeat`, `pattern` | Two slides in a row declare the same pattern; a slide declares none. | Another scene for one of them, in the storyboard first. |
| `style` | A character or a bracketed head the house style bans. | Rewrite within the house style, as house-style.md "Writing within the house style" says. |
| `banned` | A phrase of the deck's banned list. | Rewrite the sentence; the phrase stays on the list. |
| `unstable` | A slide's image differed from one shot to the next and did not settle in five. | Take out what moves on that slide (an animation, a transition); a deck is still. |

- The first output line names the fonts that loaded. "None" means every slide rendered in the system fallback: check the font's address, and name the fallback in the delivery where it stays.
- The second line names the faces the browser rendered the text in, with their glyph counts. A `fallback` note names a run of text partly rendered in a face its own stack does not name: a script the stack's faces lack fell to a system face. A note is no finding and does not change the exit code; fix it as "Font" says, or name the face in the delivery where it stays.
- The checks measure boxes and words. They do not see two elements that overlap, a title under a picture, or a scene that says nothing: those are found by looking at every page at full size.
- The lone-word check reads a block's lines letter by letter, so a line of mixed type sizes is counted once.
