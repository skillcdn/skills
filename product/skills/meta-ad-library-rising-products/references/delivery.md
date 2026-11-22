# Profiles, report and snapshot

What phases 6 and 7 write: one profile per reported entry, the report, and the snapshot the next run is compared with. The counts, the classes and the order are in [rising-signals.md](rising-signals.md).

## Profiles

For each reported item, from the pages already loaded:

- **What it is**, and the price and offer as the ads state them, quoted.
- **Who sells it**: the store, the number of Pages that advertise it, creators named as partners.
- **The ads that carry it**: two or three links by Library ID: the oldest survivor, the most reused (`uses`), the newest burst. The share of video.
- **The numbers**: `A`, `new7`, `new30`, `older(30)`, `older(90)`, `life90` beside the baseline's, the class and the pace with the reason in a line, the first day when known, the change since the snapshot when there is one.
- **Competition**: how many other sites in the pool sell the same kind of item. Several sellers with fresh creatives confirm demand; the same creative on dozens of stores is saturation.
- **Flags**, stated as observations about the ads and not as verdicts on the seller: cure or miracle claims; income or savings promised as a figure; a health, finance or other regulated category; a general store; borrowed brand names or likely counterfeits; a seasonal push; a whole footprint launched on one day; almost every ad marked low impression; a Page that runs the same ads in many countries, whose count is not this market's alone.

A theme's profile reads across its sellers: what its ads promise, as two or three lines quoted from different sellers; who sells it (how many sellers, the most present named, and what they sell: the thing itself, or courses about it); the ads as above; the numbers; and as flags the strays its phrase matches and the spelling it misses.

With a driven browser, the advertiser's `About` tab adds the day its Page was created. A web-reading tool may read the landing page for the price. Neither is required.

## The report

The run's folder holds `report.md` in the user's language and `work/`. The template's headings are written in the report's language; a class or a pace keeps its English word beside the translation, so that the report and the snapshot agree. Where the agent cannot write files, the report goes into the client's document surface and the snapshot is given as a code block to save.

```markdown
# Rising products: <sector> (<market>, <date>)

## Scope
<Sector, what counts as an item in it, market, terms, date read, route, page loads. What the classes, the pace and the lifespan share mean. What the library cannot show: spend, sales, stopped ads outside the EU and the UK. Whether an earlier snapshot was compared.>

## Ranking
| # | Item or theme | Seller | Active ads | New 7d | New 30d | Older 30d | Older 90d | Lifespan share | Class, pace | Since last run | Ads |
<A theme's seller is "<n> sellers".>

## Items and themes
### 1. <item or theme>
<The profile: what it is, who sells it, the ads that carry it, the numbers, competition, flags.>

## Benchmarks
<The largest Proven ones that are not faster, a line each.>

## Sector baseline
<The four counts of the baseline term, its shares and its lifespan share.>

## <What the user asked, in their words>
<Only when the request asked more than a ranking: what to build, stock, offer or write about. Each answer names the entries of the ranking it rests on, and says what the library cannot tell about it.>

## Method and limits
<Class and pace rules as used. Counted but not reported, with numbers. Themes dropped at their check. What was left out, and what a signed-out reader cannot see (age-restricted ads). That the next run measures real growth against this snapshot.>
```

## The snapshot

One file per run in `snapshots/` beside the run folders, named `<YYYY-MM-DD>-meta-<market>-<category>.json` ([rising-signals.md](rising-signals.md) "Seeds"), shaped like [snapshot.example.json](../assets/snapshot.example.json); a run of the watch mode writes the shape of [snapshot.watch.example.json](../assets/snapshot.watch.example.json). The field names and these values are fixed English words, and everything else is free text in the user's language:

| Field | Values and meaning |
|---|---|
| `mode` | `sweep` (the run chose its candidates) or `watch` (the topics were given). |
| `market`, `category` | The country code, and the sector as the file's name has it. `sector` beside them is the user's words. |
| `route` | `page dump`, `driven browser`, `hand-carried`. |
| `locale`, `sort` | What every address of the run carried: `en_US`, and the order of the count pages (`total_impressions` unless the run set another). A later run that counts the same again takes both over. |
| `terms` | In a sweep, the seed terms. On an entry of the watch mode, the topic's search phrase per country code. |
| `search_type` | The URL parameter's value: `keyword_exact_phrase`, `keyword_unordered`, `page`. |
| `scope` | What the counts cover: `store` (a site or a Page that sells the one thing, counted whole), `item` (one product inside a general store), `theme` (a phrase across its sellers). |
| `class`, `pace` | `breakout`, `new push`, `proven`, `thin`; `faster`, `level`, `slower`. |
| `pages`, `week_share`, `life90` | The Pages seen advertising it, which for a theme is its sellers; `new7 / new30`; `older90 / active`, to two decimals, `null` where `active` is 0. |
| `since_last_run` | The change in `A` since the earlier snapshot, `null` without one. |
| `reported` | `true` for what the ranking or the benchmarks show; a counted entry that is not shown stays in the file with `false`, so that the next run still compares it. |
| `deferred` | The keys the run was to count and did not, because it stopped at a sign of being slowed down. The next run counts them first. |
