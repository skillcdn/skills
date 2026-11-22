# The watch mode

Topics fixed earlier are counted again the same way, so that this run's numbers can stand beside the last run's and beside another country's. There is no sweep, no candidate and no ranking: the topics are the user's or the calling skill's already. Phases 1, 2 and 4 run as the skill says, with what this page changes; phases 3, 5 and 6 are replaced by it.

## Topics and their phrases

- A topic is an `id` (lowercase words joined by hyphens, the same in every country and every run, because entries are matched by it), a name, and one search phrase per country, in that country's language as its sellers write it. Every snapshot keeps the phrases of all the countries with the topic (`terms`), so that the pair is never rebuilt from memory.
- The topics come from the request or the calling skill's list; else from the latest watch snapshot of the same market and category, when the request is to count the same again; else from the entries of a sweep's snapshot the user points at, each taken over with its `key`, `query` and `search_type`.
- A topic that has an earlier snapshot takes over that snapshot's `query`, `search_type`, `sort` and `locale` exactly, even where a better phrase is in sight. A better phrase is a new topic beside the old one, or replaces it on the user's word: its first count is a new basis and is compared with nothing.
- A topic counted for the first time is searched as an exact phrase, and the first page of its first count is checked as [rising-signals.md](rising-signals.md) "Themes" says under "Check": two thirds on the topic, tightened once, else dropped and said so. For a second country the phrase is what that country's sellers write for the same thing, not a word-for-word translation, checked the same way. After its first run a phrase is not tightened again; strays become a flag.

## One run per country

Each country is a run of its own with its own 80 page loads, one country after the other and never side by side, in its own folder `rising-products-<category>-<market>-<YYYYMMDD>/`, with its own snapshot.

- **Baseline**, four loads: the earlier snapshot's baseline query; in a first run, the broadest word of the category in that country's language whose count is under the library's ceiling.
- **Topics**, four loads each (`A`, `older(7)`, `older(30)`, `older(90)`, by "Counts"), which is nineteen topics a run at most. With more, count in the order given and write the rest to `deferred`. The dated counts print the count alone (`lines=0`); the page of `A` is kept for the check and the flags.
- For each topic compute `new7`, `new30`, `life90`, and the class and the pace by "Classes". No profile is written, and `reported` is `true` for every topic counted.

## When the site slows the run down

At a sign of being slowed down ([ad-library.md](/docs/meta-ad-library/ad-library.md) "Manners and limits"; the one a long run meets is a count with no results under it) the run stops there. The load that showed the sign and any after it give no number. The topics not yet counted go to the snapshot's `deferred`, and the next run counts them first. The other country's run does not start in the same sitting unless the user says so.

## The comparison

Once the snapshot is written, run [compare-snapshots.example.mjs](../scripts/compare-snapshots.example.mjs) on the `snapshots/` folder, with the market and the category where the folder holds more than one series. Its table says for every entry of either run:

| Word in the table | Meaning | What the report says |
|---|---|---|
| `new basis` | The phrase, the search type, the sort or the locale is not the earlier run's. | No change is stated: this run is the first measurement on the new basis. |
| `new` | Counted now, absent from the earlier snapshot. | The first measurement. |
| `unranked` | Counted, and not shown in its run's ranking (`reported` is false). | Compared all the same. |
| `deferred` | In the earlier snapshot, and left for the next run by this one. | Carried over, never read as a fall. |
| `dropped out` | In the earlier snapshot, neither counted nor deferred now. | Not counted this time, with the reason. |
| `grew`, `fading` | `A` up or down by a quarter or more and by at least ten ads. | The measured change over the days between. A smaller move is the library's drift. |

Two countries are not compared count against count, since their libraries differ in size: compare a topic's `life90` in each, and its `A` as a multiple of that country's baseline `A`.

## What comes back

`report.md` in the run's folder, short, in the user's language: one row per topic (`A`, `new30`, `older(90)`, `life90` beside the baseline's, the class and the pace, the change since the last run or the table's word for it), the baseline's row, the topics deferred, what was dropped at its check and why, the date and the page loads. With two countries, one more table sets each topic's two rows under each other. The snapshot's path goes back to whoever asked, the user or the calling skill, and the profile the page dump left is removed as phase 7 says.
