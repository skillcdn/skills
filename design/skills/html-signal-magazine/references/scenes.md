# Scenes: what a slide of an issue can be

The scenes an issue is planned from, each with the file it starts from under `assets/scenes/` and how its drawing is computed from the figures. Read at the plan (phase 3) and at the build. A file holds placeholder values, a `<style>` block of its own classes and one `section.slide`: its rules go into the deck's stylesheet, its section into the body, its values and words are replaced, and the drawing is recomposed for what the slide says.

## Choosing a scene

- The sentence comes first. The scene is the drawing in which a reader sees that sentence before reading it: a size as an area, a count as units, a spread as a band, a place among others as a map.
- No scene twice in a row, and none in the same place as in the last issue. An issue tries several scenes the last one did not have; a drawing that is none of these takes a name of its own, and its section is kept as a file for the next issue.
- A slide of stacked text (a numbered list, three lines under a heading) is not a scene. What it says becomes a drawing or leaves the issue.
- A figure appears once at its full size. What stands beside it gives it scale: another value of the same year, never a value decades old and never a ratio of two single prices.

## The frame scenes

| Scene | Starts from | Holds |
|---|---|---|
| `cover` | the skeleton | The masthead, the period, the cover story, three cover lines with a small figure each, the apps' screens as a collage off the edge. |
| `contents` | `contents.html` | The issue's one sentence as the title, a row an item with its figure and a small figure, the apps shown as a row of icons. No heading that only labels the icons. |
| `view-card` | `view-card.html` | The closing view in a lit card, and a card for each of the series' questions. |
| `back-cover` | the skeleton | Centred: the masthead, the question the issue leaves, the contact. |

## Scenes for one figure or one comparison

| Scene | Starts from | The drawing |
|---|---|---|
| `giant-figure` | `giant-figure.html` | One figure across the slide over its sentence, with one value of the same year beside it. |
| `split-bars` | `split-bars.html` | Two measures of the same things, growing left and right from the names. A bar's width is its value in percent of the largest on its side. |
| `dot-plot` | `dot-plot.html` | One value a row as a dot on a common scale; the scale's two ends are named and nothing else. |
| `band-plate` | `band-plate.html` | Prices as bands on a log scale, on the plate. The file's head gives the arithmetic. |
| `unit-columns` | `unit-columns.html` | Columns of unit blocks, a block a fixed amount named once. Each stack carries `data-count`. |
| `circles` | `circles.html` | Sizes by area: a diameter is the largest one's times the square root of the value's share of the largest. |
| `country-columns` | `country-columns.html` | The same measures in two countries, a pair a measure. A pair compares the countries, never one measure with another. |

## Scenes for many things at once

| Scene | Starts from | The drawing |
|---|---|---|
| `sieve` | `sieve.html` | The questions as cards, and how many candidates were left after each, as counted dots. |
| `verdict-map` | `verdict-map.html` | The themes on two axes, the cell the title speaks of lit, beside each theme the mark of its gate 04 verdict (pass, partial, fail, unknown). |
| `company-cards` | `company-cards.html` | A card a company: the logo, the name, what it sells in a line, two figures as amounts. |
| `screen-tiles` | `screen-tiles.html` | The products as their own screens in a row, a name under each and, where the plan's sentence needs it, one line of what the product does. |
| `icon-timeline` | `icon-timeline.html` | When each came in, as its icon over the year on one line. |
| `logo-columns` | `logo-columns.html` | Three groups of companies by their logos, a count and a head a group. |

## Rules of the drawings

- **Counted units are counted.** A drawing of dots, blocks or people holds exactly the number its figure says and declares it in `data-count`; count them again at the look. One issue drew half as many dots again as its figure said, and no layout check saw it.
- **An axis is an arrow, and its title stands at the arrow's end:** at the top for the upward one, at the right for the rightward one.
- **No line that is not data.** A baseline, a grid or a target line stays out unless the sentence is about it.
- **A verdict is a signal mark,** the same three everywhere and named once in a key: three bars where those who came in earned, two where only the large ones did, one dashed bar where it is not known yet.
- **A company card** holds the logo, the name, one line and two figures. No founding year, no adjective in place of an amount.
- **Labels keep clear:** of each other, of the next column, of the title. A label that does not fit is shortened in the words, not in the type size.
- **The row the title speaks of is the accented one** (`.on` in the files), and it is one row.
