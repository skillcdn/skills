# Public sources read again

The public sources a market survey reads and a round reads again, by country: what each counts, which gate it is evidence for, when it comes out and how its number is found. All are free and need no sign-in. A source is a row of `sources` in the watch list ([watch-record.md](watch-record.md)) once a metric is read from it; this page says how to read it the first time and what to expect of it later. An address was last opened in the month it carries; where a site has moved, search for the release by its name on the publisher's site and correct the row.

## How a source is read

- Read the release or the table itself, never a summary of it, and keep the address of the page that holds the number, not of the site.
- Write the `period` the number is about, which is not the day it came out: a monthly release is about a month one or two months back.
- A table revised later keeps its period: the new value is a second observation of the same period.
- An index (search interest, a ranking) is relative: compare it only within one query and one date range, never across queries.
- Where the publisher has a release calendar, the next date comes from it; a round whose source has not come out notes `not published` and moves on.

## Korea

| Source | Counts | Gate | Comes out | Where (checked 2026-11) |
|---|---|---|---|---|
| Online shopping survey of the national statistics office | Online sales by product group, a month | 01, 02 | Monthly, about five weeks after the month | `kosis.kr`, the table by product group; the release on the statistics office's site (`kostat.go.kr` now answers at `mods.go.kr`) |
| Population trends of the same office | Births, deaths, marriages, divorces, a month | 01, 02 for a market that follows them | Monthly, about two months after the month | `kosis.kr` |
| National Tax Service, 100 everyday business types | Registered businesses by type, a month | 03 | Monthly | `tasis.nts.go.kr`, the tax statistics portal |
| Fair Trade Commission, mail-order business filings | Every filed online seller with its filing date and what it sells: new filings a month are counted from the file | 03 | Kept current; downloaded | `ftc.go.kr`, the business information download page |
| Ministry of SMEs and Startups, new business trends | New businesses by industry, a month | 03 | Monthly, around the middle of the month | The ministry's release at `mss.go.kr`; the tables on `kosis.kr` |
| Korea Tourism Data Lab | Visitors and their spending by region and origin, a month | 01, 02 for travel themes | Monthly | `datalab.visitkorea.or.kr` |
| App analytics vendors' releases | Users and spending of named apps | 01, 02, graded `estimate` | Irregular | The vendor's own release, not the article that quotes it |
| DART, the disclosure system | A company's revenue and operating profit | 04 | Yearly for an audit report, quarterly for a listed company | Read with `dart-company-figures` |

## The United States

| Source | Counts | Gate | Comes out | Where (checked 2026-11) |
|---|---|---|---|---|
| Census Bureau, Business Formation Statistics | Business applications a month, by NAICS sector | 03 | Monthly, around the middle of the next month | `census.gov/econ/bfs/`; the monthly file is `csv/bfs_monthly.csv` under it, one row a sector and series (`BA_BA` all applications, `BA_HBA` those likely to hire), `sa` `A` adjusted or `U` not, a column a month |
| App Store search | Apps for a search term with each one's first release date | 03 | Live | `itunes.apple.com/search?term=<words>&country=<code>&entity=software&limit=200`: no key, at most 200 apps a term, `releaseDate`, `trackName`, `description`, `sellerName` in each result |
| App Store charts | The top free and top paid apps of a country today | 01 as a sign only | Live | `rss.marketingtools.apple.com/api/v2/<code>/apps/top-free/<n>/apps.json` (the older host `rss.applemarketingtools.com` redirects to it) |
| App analytics vendors' posts | Downloads and spending of categories and named apps | 01, 02, graded `estimate` | Irregular | The vendor's own post |
| SEC EDGAR | A listed company's revenue and operating income, and what it says of competitors entering | 04 | Quarterly and yearly | `sec.gov/edgar/search/`, the company's 10-K and 10-Q; a script that reads it names itself in its user agent, as the site asks |

The App Store search and charts answer for any country code, Korea included.

## Any country

| Source | Counts | Gate | Where |
|---|---|---|---|
| Meta Ad Library | Active ads for a phrase, how many outlived 90 days, how many sellers | 03, graded `measured` | Read with `meta-ad-library-rising-products` in its watch mode, which keeps the terms, the sort and the locale in the snapshot |
| Search interest: Google Trends, Naver DataLab for Korea | A relative index of searches over time | The fad rule; never a size | `trends.google.com`, `datalab.naver.com`. Neither answers a plain fetch (Trends answered scripted requests with 429, DataLab asks for its form, checked 2026-11): read them in a driven browser, else the report says the fad rule was not read |

## When a round reads which

A round every two weeks does not read every source. A monthly source is read in the first round after it comes out; the entry statistics that come out around the middle of the month are read in the round of the third week; a quarterly source in the first round of the quarter; a yearly one in the round after its release. Ads and a live source are read every round. A metric whose `cadence` is not due is left alone, and its theme's `next_check` still moves.
