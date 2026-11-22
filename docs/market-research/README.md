# Market research: what its skills share

The skills that find a market to enter, look into one item, read a company's figures and put the result out as a magazine issue share three things: the words a number and a verdict are tagged with, the file a watched market is measured again in, and the public sources read again. They live here once, one file per topic; each skill carries its own method (what it searches, what it counts, what it accepts) itself.

| Document | Holds | Read |
|---|---|---|
| [`evidence-grades.md`](evidence-grades.md) | The grade of a number, the check of a number against its source, the check of a company's announced figure against its filing, the verdict of a gate. One table each. | Included with each of the four skills below. |
| [`watch-record.md`](watch-record.md) | The watch list file `watch.json`: sources, themes with their status and their verdicts per country, metrics, the observation line, who moves a status, what may be compared, where the files of a market folder are. | Before the watch list is written or read. |
| [`sources.md`](sources.md) | The public sources read again, by country: what each counts, when it comes out, how its number is found. | From the step that reads a source. |

## Who hands what to whom

| From | To | What | How the receiver chooses |
|---|---|---|---|
| [`web-market-entry-signals`](/product/skills/web-market-entry-signals/SKILL.md), the survey | its own later round | `watch.json` | The file in the market folder. Without one, the survey runs first. |
| the survey | [`web-item-deep-dive`](/product/skills/web-item-deep-dive/SKILL.md) | One row of the gates table in `report.md` | The user picks; the survey never does. |
| [`meta-ad-library-rising-products`](/product/skills/meta-ad-library-rising-products/SKILL.md), watch mode | the survey and the round | `snapshots/<YYYY-MM-DD>-meta-<market>-<category>.json` | The two latest of the same market and category. |
| [`dart-company-figures`](/product/skills/dart-company-figures/SKILL.md) | the survey, the deep dive, the magazine | `figures.json`, one row a company | Rows whose `check` is `matches` or `sums-up` go into anything shown; `announced-only` goes on the list the user confirms. |
| the deep dive | the watch list | One theme line, changed | The same theme id. |
| the survey, the round, the deep dive | [`html-signal-magazine`](/design/skills/html-signal-magazine/SKILL.md) | Verdicts, observations, what changed, the figures the user says may be public | What differs from the last issue first. Verdicts on the user's own plans are not handed on. |
| the magazine | the watch list | A figure of the issue that will be used again | An observation under the metric's id. |

## What every skill of the set does the same way

- **A number carries its grade and its address.** A number is used in a verdict only after the sentence that holds it was read in its source.
- **A count can be counted again.** An entrant count, an ad count and a metric name the source, the query and the day; names met in passing are a floor and are not written as a number.
- **A price is a band**, from the cheap end to the expensive one for each kind of product. One value divided by another is not a comparison.
- **Like is compared with like**: the same source, the same query, the same definition. A changed definition is a new metric.
- **The user's own plans stay out of what is shown**: which markets they dropped and why, what they will try. A skill reports the signal and the user decides.

Each skill states these in its hard rules, in the form its workflow gives them, so that they hold where these pages do not travel.

## How these pages are written

By topic, saying what holds now. A fact about a site carries the month it was checked and the way to find the value again; a threshold or a share that illustrates a shape is marked as an illustration. Examples carry placeholder values and name no company and no market anyone chose.
