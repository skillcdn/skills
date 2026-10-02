# Rising signals

The method of phases 1 to 7: where candidates come from, what an item is, what is counted, how an item is classed, and what the report and the snapshot hold. Thresholds are working defaults; state them in the report and change them when the user asks.

## The assumption and its limits

Advertisers keep paying only for what returns, so an item whose ads multiply and stay up is probably selling. The library shows the paying, never the return. Read it this way:

- Many active ads show how much is being tested, not that it pays.
- Ads that survive show that someone chose to keep paying for them.
- A footprint that is already large with nothing old in it is a rise.
- Outside the EU and the UK only ads that still run are listed. "Nothing older than 90 days" means no such ad survives, not that the seller never advertised before.

## Seeds

- **Terms**, six to eight, in the market's language as its sellers write them, searched as `keyword_unordered`. For a sector: two or three category words, one or two problem or desire phrases, and two purchase cues joined to a category word. For a broad sweep: purchase cues alone. Purchase cues are the phrases of direct-response ads: free shipping, today only, selling out, special price, official store, back in stock. Use cues made of words: the search drops signs, so "1+1" finds nothing useful.
- **Views per term**, one page load each: most recent, and impressions order, both with all media. When a term's first view fits on one page (`more` is false), the second would repeat the same ads: skip it. A term that returns fewer than about twenty ads is replaced once.
- **Budget.** 80 page loads for the run: the sweep (two per term), the baseline (3), the counts (4 per candidate, 12 candidates at most), a few spare.

Work in one folder under the agent's working folder, `rising-products-<sector>-<YYYYMMDD>/`, the sector in lowercase ASCII words joined by hyphens (translated when it is not written in Latin script; `broad-sweep` when there is none). Scripts, raw records and the load log go in `work/` inside it. Earlier runs are the folders of the same name pattern beside it.

## Items

- **Key.** The landing site: the domain without `www.` or `m.`. On a host that many sellers share (a marketplace, a store builder's shared domain) the key is the host with the seller's path segment. Where the landing address says nothing about the seller (a short link, an in-app page such as `fb.com/canvas_doc`, a lead form, a message, a social profile) the key is the advertiser's Page.
- **What counts.** A product an independent seller sells, physical or digital, and inside the sector: a keyword matches anywhere, so most of a pool is strays. Leave out app installs, lead forms and services (clinics, courses, finance, lodging), live animals, charities and events, marketplaces and very large brands advertising a catalog, news and politics, and ads in a language the market does not read. When in doubt keep the item and say why at the checkpoint.
- **A general store** that sells unrelated products under one domain is a seller, not an item: name the item from the ad titles, keep the store as its seller, and count the item as "Counts" says, not the store.
- **Tally** per item across every view, after removing duplicates by creative group (`group`, not `id`: one group shows under different IDs in different views): creative groups, Pages, the largest `uses`, the youngest and the oldest `days`, how many groups are marked low impression.

## Candidates and checkpoint

An item qualifies with two or more creative groups in the pool, or one group with `uses` of 3 or more, provided not all of it is marked low impression. Take twelve at most:

- **Nine for signs of a rise**, the items showing the most of these first, more groups in the pool breaking ties: five or more ads started on one day within the last 30 days; an ad 60 days old or younger among the first ten of an impressions view; three or more Pages advertising one site; a group with `uses` of 3 or more.
- **Three for scale**: the qualifying items with the most groups in the pool, whatever their age. They become the benchmarks.

The checkpoint is one message in the user's language: the sector, the market and the terms in a line; the candidates as a table (item, what it sells, groups seen, youngest and oldest, why it was picked); what was left out as a kind; that one word continues to the counting, and that candidates can be struck or added and the sector changed.

## Counts

Four counts per candidate, by [ad-library.md](ad-library.md) "Counting by age". The query is the item's key as an exact phrase, or the advertiser view when the key is a Page.

| Count | Spec adds | Gives |
|---|---|---|
| `A` | nothing | Active ads now. |
| `older(7)` | `before=7d` | `new7 = A − older(7)`: started this week and still running. |
| `older(30)` | `before=30d` | `new30 = A − older(30)`; `older(30)` itself is the ads that outlived a month. |
| `older(90)` | `before=90d` | The ads that outlived a quarter. Zero means no surviving ad is older than 90 days. |

Each of these loads also lists the most-shown ads of that age group with their start dates: keep them for the profile. When the `older(30)` page fits on one page, its oldest start date is the first day of the item's surviving ads; when it does not, two more counts at 45 and 60 days place that day within a fortnight, for a Breakout only and inside the budget.

**An item inside a general store.** The store's counts are not the item's. Count the item itself: a product phrase that only its ads use, as an exact phrase, after checking on the first page that no other product comes back; failing that, the sum of `uses` over the item's creative groups, read on the unfiltered page and again under each date bound, where `uses` shrinks to the copies that had started by then. When neither isolates the item, report the store's numbers labeled as the store's, and do not class the item.

**Baseline.** The category word with the highest count among the seeds, with the same three date bounds (its `A` is already known from the sweep). Its shares say what is ordinary. As an illustration only: on 2026-10-02, for four broad terms in one market, 33 to 46 percent of the active ads had started within seven days, 64 to 77 percent within thirty, and 7 to 13 percent were older than ninety; `new7 / new30` lay between 0.53 and 0.59. A third of the ads being new is the normal churn of the library, not a rise.

## Classes

A class by age, applied in this order, then a pace.

| Class | Rule | Reading |
|---|---|---|
| Thin | `A` under 10 | Too few ads to read. Left out. |
| Proven | `older(90)` of 1 or more | It has paid for ads for more than a quarter. A benchmark, and news only when its pace is faster. |
| New push | `older(30)` is 0, or `A` under 20 | Launched within the month, or still small: volume without survival. A bet to watch, not proof. |
| Breakout | `older(90)` is 0, `older(30)` of 1 or more, `A` of 20 or more | No surviving ad is older than a quarter, the footprint is sizeable, and some of it has outlived a month. This is the rise the skill looks for. |

| Pace | Rule | Reading |
|---|---|---|
| Faster | `new7 / new30` at least 0.15 above the baseline's (0.57 becomes 0.72) | Launching more this week than its sector does. |
| Slower | at least 0.15 below | The push was earlier in the month; it may be over. |
| Level | otherwise, and whenever `new30` is under 10 | |

Order of the report: Breakout, faster or level, by `A`; Proven, faster, by `new7`; Breakout, slower, said to be slowing; New push by `A`. The three largest Proven items that are not faster go under "Benchmarks", not in the ranking; anything else counted goes in "Method and limits" with its numbers.

- **With an earlier snapshot** of the same market: for every item in both, the change in `A` over the days between. Growth of a quarter or more and at least ten ads is stated as measured growth and puts the item at the top of its class; a fall of a quarter marks it fading. Items that disappeared are listed. This is the only true trend outside the EU and the UK, so say when it is missing.
- **In the EU and the UK** the library keeps stopped ads for a year. For the five strongest items, count the ads that delivered in each of the last four weeks and in one week two months back (`status=all` with `after` and `before`): a rising series is a rise, whatever the class.

## Profiles

For each reported item, from the pages already loaded:

- **What it is**, in plain words, and the price and offer as the ads state them, quoted.
- **Who sells it**: the store, the number of Pages that advertise it, creators named as partners.
- **The ads that carry it**: two or three links by Library ID: the oldest survivor, the most reused (`uses`), the newest burst. The share of video.
- **The numbers**: `A`, `new7`, `new30`, `older(30)`, `older(90)`, the class and the pace with the reason in a line, the first day when known, the change since the snapshot when there is one.
- **Competition**: how many other sites in the pool sell the same kind of item. Several sellers with fresh creatives confirm demand; the same creative on dozens of stores is saturation.
- **Flags**, stated as observations about the ads and not as verdicts on the seller: cure or miracle claims; a health, finance or other regulated category; a general store; borrowed brand names or likely counterfeits; a seasonal push; a whole footprint launched on one day; almost every ad marked low impression.

With a driven browser, the advertiser's `About` tab adds the day its Page was created. A web-reading tool may read the landing page for the price. Neither is required.

## Report and snapshot

The run's folder holds `report.md` in the user's language, `snapshot.json` shaped like [snapshot.example.json](../assets/snapshot.example.json), which the next run compares against, and `work/`. In the snapshot the field names and the values of `class`, `pace` and `scope` are fixed English words; everything else is free text in the user's language. Where the agent cannot write files, the report goes into the client's document surface and the snapshot is given as a code block to save.

```markdown
# Rising products: <sector> (<market>, <date>)

## Scope
<Sector, market, terms, date read, route, page loads. What the classes and the pace mean. What the library cannot show: spend, sales, stopped ads outside the EU and the UK. Whether an earlier snapshot was compared.>

## Ranking
| # | Item | Seller | Active ads | New 7d | New 30d | Older 30d | Older 90d | Class, pace | Since last run | Ads |

## Items
### 1. <item>
<The profile: what it is, who sells it, the ads that carry it, the numbers, competition, flags.>

## Benchmarks
<The largest Proven items that are not faster, a line each.>

## Sector baseline
<The four counts of the baseline term and its shares.>

## Method and limits
<Class and pace rules as used. Counted but not reported, with numbers. What was left out. That the next run measures real growth against this snapshot.>
```
