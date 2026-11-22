# The four gates: what makes a market worth entering

How a theme is judged, per country, on four questions, with the thresholds the plan shows, what counts as evidence for each, how ads and prices are read, and when a rise is a fad. Read before the plan is shown and again before the verdicts.

## The four questions

| Gate | Question | Evidence that answers it | Default threshold |
|---|---|---|---|
| 01 | Are many people already paying? | Yearly spend from an official statistic or filings; failing that, users from a vendor's estimate | Spend of KRW 100 bn a year in Korea, USD 100 m in the US; or 1 million monthly users |
| 02 | Is it growing? | The same measure a year apart, from the same source | 10 percent or more over the last year |
| 03 | Are new competitors coming in? | A count that can be made again: [entrant-count.md](entrant-count.md) | Three or more entrants within two years, or an official count of operators that rises |
| 04 | Are the ones who came in earning? | The revenue and operating profit of named entrants, from filings | At least one entrant of the last three years files an operating profit |

The thresholds are working values, not findings: the plan shows them, the user changes any of them in a word, and the head of the gates table and `thresholds` in the watch list say which were used. For a country other than these two, scale 01 by the size of its economy and say so.

A verdict is one of `pass`, `partial`, `fail`, `unknown` ([evidence-grades.md](/docs/market-research/evidence-grades.md)). A cell with no address behind it is `unknown`. A cell met through a proxy (customers in place of spend, the spend of a neighbouring market) is `partial`, and the memo names the proxy.

## Why 03 never decides alone

New entrants show almost everywhere in a year when a technology gets cheap: new apps in a category can double while downloads barely move. An inflow says a market is easy to enter, not that entering pays. So 04 is read with it, and the memo of every row says two things: whether those who entered earn, in amounts, and which year of the inflow this is, counted from the year the first entrants appeared. In a market where the leader's earnings became known first and the crowd followed, prices can reach their floor within a few years: a late year of the inflow is a weaker `pass` than an early one, and the memo says so in words.

## A benchmark first

When the user names a market "like this one", judge it before any other theme and put its row at the top. If the gates do not pass the benchmark, the thresholds are wrong for this user: say so with the cells that failed, and ask whether to change them, before the other verdicts are written.

## Reading ads for gate 03

The counts come from `meta-ad-library-rising-products` in its watch mode, per country, with a baseline term.

- The share of ads that started within 30 days does not separate themes: it is high for any broad term (most of the active ads for a broad baseline term, an illustration, checked 2026-11).
- Three things do: the theme's active ads against the baseline term's; how many different sellers stand on the pages read; and `life90`, the part of the active ads older than 90 days, against the baseline's (a small part for a broad baseline term, an illustration). A theme well above the baseline's `life90` has sellers who keep paying; one far below it is new money that has not yet stayed.
- An ad count is `measured` and says nothing of sales. It supports 03, never 01 or 04.

## A price is a band

A market's price is written as a band for each kind of product, from the cheapest offer found to the most expensive, with what is sold at each end and the grade of each source. One value is not a market price, and one value divided by another is not a comparison: where a note holds a multiple ("ten times cheaper"), go back for the band on both sides.

## A fad

A theme whose search interest fell to half within 30 days of its peak is marked `fad` in the memo and is not raised on that rise. The 30 days are a working value: where the run has the budget, measure how long a few past fads of the same market took to halve and say what was found. Search interest is an index: it places a peak in time and says nothing of size.

## What the user set aside

A theme the user's own circumstances rule out (an area they already work in, a form that failed them before) and an idea they dropped earlier are judged like any other and stay in the table, marked as set aside. The report states what their signals are and recommends none of them. The reasons are the user's and are written nowhere but the note they gave.
