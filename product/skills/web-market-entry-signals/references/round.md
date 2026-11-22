# A round: the watched markets measured again

The second entry into this skill. A watch list exists, and the request is to measure again or the date of the next round has come: every metric that is due is read once more, one observation is added to each, the ads are counted the same way as last time and compared, statuses move by fixed rules, and the report holds only what changed. Read this page and [watch-record.md](/docs/market-research/watch-record.md) first; a round runs in place of the survey's phases and stops once, at its report.

## 1. Targets

`node scripts/watch.mjs --due` lists the themes whose `next_check` has come, with each metric's cadence and the last period read. Dropped themes are on the list: their signals are read like any other. From it take the metrics to read now by [sources.md](/docs/market-research/sources.md) "When a round reads which": a metric whose source has nothing new since the last period is left alone. Take today's date from the system.

A metric or a source the user adds in the request is written into the file first, with its first observation, and the round goes on. A request to measure again before any `next_check` has come reads only what has a new period since its last reading, the deferred ad topics first; a metric read the same day is left alone, said in one line.

## 2. Reading again

For each metric due, open its source as its `how` says and add one observation: `read`, `period`, `value`, `grade`, `url`, `note`.

- The number is about a period: write the period the source gives, not today.
- A period already in the file that the source has revised gets a second line with the same `period`.
- A source that has not come out, or could not be reached, gets a line with `value` null and the note `not published` or `not reached`. Nothing is estimated in its place.
- A number written in an issue of the market report that came back as worth reading again is already a metric: read it like the rest.

## 3. The ads

`node scripts/watch.mjs --ads` lists the latest snapshots of each market and category. For each, run [meta-ad-library-rising-products](/product/skills/meta-ad-library-rising-products/SKILL.md) in its watch mode on the topics of the last snapshot, a run a country: it takes the phrases, the sort and the locale from that file, counts each topic and the baseline, writes `snapshots/<YYYY-MM-DD>-meta-<market>-<category>.json` and sets it beside the last one with its compare script, which shows every topic, the ones the new run did not count among them.

- A snapshot taken with other terms, another sort or another locale is not compared: it becomes the new base, and the report says the series starts over.
- At a sign of being slowed down that skill stops. What it counted before the sign stands; the topics left are `deferred` in the snapshot and go first in the next round; the report names them.
- Each topic's active ads and `life90` go into the watch list as observations of that theme's ad metrics, with the day as the period and the snapshot's path as the note; a theme with no such metric in that country gains `<country>-<theme>-ads-life90` (source the ad library, gate 03). Counts of a country where the theme has no gates yet write no verdict there, and the report says so.

## 4. Statuses and gates

`node scripts/watch.mjs --id <theme>` prints a theme's observations with the change from the period before.

| From | To | When |
|---|---|---|
| `watch` | `candidate` | The same metric rose in two periods running, each read from its source, and gates 01 to 03 are `pass` in one country |
| `watch`, `candidate` | `cooling` | The metric the theme was raised or added on fell in two periods running, or the theme meets the fad rule of [gates.md](gates.md) |
| `cooling` | `watch` | That metric rose again in a period |
| any | `testing`, `dropped`, or back from `dropped` | Never by the round: the user's word only. The round says what it would suggest and why |

One rise is not a rise: the theme stays `watch`, and the report may say "one more reading would raise it". A rise in a proxy raises nothing. Where a reading changes the evidence for a gate, write the new verdict and the day into the theme's `gates` for that country, by gates.md, and say it in the memo. Then set `next_check` of every theme read to the date of the next round, and `updated` to today.

## 5. The check

`node scripts/check-watch.mjs` until it prints `ok`. A round is not reported before it passes.

## 6. The report and the log

One message, three lists and no more:

1. Themes raised to `candidate`, each with the metric, its two rises and the addresses.
2. Themes now `cooling`, the same way.
3. Dropped themes where a gate turned to `pass` since the last round: the fact and its address, and no suggestion.

Under them, in one line each: how many metrics were read, how many were not published or not reached, which ad topics were deferred, what only the user can decide (a move to `testing`, reopening a dropped theme), and the date of the next round, two weeks on unless the user keeps another rhythm. An empty list is said to be empty.

Append one line to `log.md`: the date, what was read, what moved, what was put off. Where the market folder is a unit of a studio, the round ends as the studio's agreement says a unit is recorded.

## Verdicts

| Result | Verdict |
|---|---|
| A value with its source's address and its period | Recorded |
| The source put its release off | A null line noted `not published`; the theme's next check moves |
| A "new" reading whose period is already in the file | Recorded as a revision of that period, never as a new period |
| One measured rise | The theme stays; the report says one more reading would raise it |
| A rise in a proxy, or between values measured in different ways | No move; a changed way of measuring starts a new metric |
| Ad counts read after the sign of being slowed down | Discarded; the topics are deferred |
