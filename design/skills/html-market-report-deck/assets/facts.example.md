# The ledger of an issue: every number, its source and its check

The shape of `facts.md` in an issue's folder, with placeholder values. One row for every number the issue may show. It is the only place a source, a counting method or a doubt is written: none of them stands on a slide. The grade and the two checks take their values from the set's [evidence-grades.md](/docs/market-research/evidence-grades.md).

| Slide | Figure as shown | The source's sentence | Address | Grade | Check | Metric id | Note |
|---|---|---|---|---|---|---|---|
| 3 | 00% of sellers came in within two years | "Of the 000 sellers registered, 00 registered in or after 0000." | `<url>` | official | confirmed | `m-entrants-kr` | Counted from the register's table; the method is in the notes of the research. |
| 6 | 0 to 000, the price band of kind two | "Plans start at 0 a month" and "the enterprise plan is 000". | `<url>`, `<url>` | announced | confirmed | | Two sources, one for each end of the band. |
| 10 | Company one: revenue 000, operating profit 00 | The income statement of the audit report for fiscal 0000. | `<url>` | filing | matches | | From `figures.json`; basis separate. |
| 10 | Company two: revenue 000 | A press release of the company. | `<url>` | announced | announced-only | | Not on a card until the user confirms it. |
| 12 | 0 of 0 apps first released in 0000 or later | The first release date of each listing. | `<url>` | measured | confirmed | `m-app-entrants-us` | |
| - | 00% growth in one year | "grew strongly over the year" | `<url>` | press | differs | | Dropped: the source gives no figure. |

## What was corrected or dropped

- Slide 3: the source speaks of first registrations only; the slide's sentence was narrowed to say so.
- The growth figure of the last row: dropped, since its source states no number.

## To measure again

- `m-entrants-kr`, `m-app-entrants-us`: on the watch list. The price band of kind two is not: added as a metric at delivery if the series will show it again.
