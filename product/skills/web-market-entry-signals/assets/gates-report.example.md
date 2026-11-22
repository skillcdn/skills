# Market entry signals: <what was looked for>

Data read on <YYYY-MM-DD>. Countries: <kr, us>. Branches: <kr-consumer, kr-business, us-consumer, us-business, ads kr, ads us>; the notes are in `notes/`.

Thresholds used: 01 <spend or users a year, per country>; 02 <growth over a year>; 03 <entrants within two years>; 04 <an entrant that files a profit>.

## In short

- Pass all four: <theme (country)>, <theme (country)>.
- Pass 01 to 03, 04 open: <theme (country)>.
- Set aside by you, signals only: <theme>: <which gate turned, since when>.
- Not seen: <categories the budget did not reach; sources that could not be read>.

## The gates

| id | Theme | Country | 01 paying | 02 growing | 03 entering | 04 earning | Memo: do entrants earn, which year of the inflow | Grades | Note |
|---|---|---|---|---|---|---|---|---|---|
| example-theme-a | <theme> | us | pass | pass | pass | partial | <one entrant files a profit, two a loss; third year> | official, filing, measured | `notes/us-consumer.md` |
| example-theme-a | <theme> | kr | pass | partial | pass | unknown | <no entrant with a filing yet; second year. 02 by a proxy: users, not spend> | official, estimate, measured | `notes/kr-consumer.md` |
| example-theme-c | <theme you set aside> | kr | partial | unknown | pass | fail | <entrants file losses; first year> | estimate, measured | `notes/kr-business.md` |

A benchmark the request named stands in the first row. A theme marked `fad` in its memo rose on search interest that halved within the fad rule's days.

## Evidence by theme

### <theme> (us)

- 01: <number, unit, period> (official, <url>)
- 02: <the same measure a year apart> (official, <url>)
- 03: <the count, how it was made, what it misses> (measured, <file or url>)
- 04: <company: revenue and operating profit, year, basis> (filing, <url>); first entrants in <year>
- Prices: <kind of product>: <cheapest> to <most expensive> (<grade>, <url> each end)
- What AI does: <the part of the product or the operation>

## Seen by ads alone

A theme no note of a country holds, counted there with the others: no verdict.

| Theme | Country | Phrase | Active ads | `life90` (baseline) | Class, pace |
|---|---|---|---|---|---|
| <theme> | kr | <phrase> | <n> | <share> (<share>) | <class>, <pace> |

## Measured again

`watch.json` holds <n> themes and <m> metrics from this survey. The first round that compares is due on <YYYY-MM-DD>.
