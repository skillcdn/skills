# The watch record: a market measured again

The file a market survey leaves so that the same markets are measured again by the same yardstick: `watch.json`, with its sources, themes, metrics and observations, the statuses a theme moves through and who moves them, what may be compared with what, and where the files of a market folder are. [`web-market-entry-signals`](/product/skills/web-market-entry-signals/SKILL.md) writes it in a survey and adds to it in every round, and carries its schema, an example and the two scripts that print and check it; the deep dive adds or corrects one theme line; the market report reads figures by metric id and returns the ones it will use again as observations.

## The market folder

`market/` in the working directory, or the unit's folder in a studio. Derived, never asked.

| Path | Holds | Written by |
|---|---|---|
| `watch.json` | The watch list. One file, added to, never started over. | The survey, every round |
| `log.md` | One dated line a survey, a round or a deep dive: what was read, what moved, what was put off. The course of events lives here, not in a note field. | The survey, every round, the deep dive |
| `snapshots/<YYYY-MM-DD>-meta-<market>-<category>.json` | The ad counts of one market and category on one day. | `meta-ad-library-rising-products` |
| `<YYYY-MM-DD>-entry-signals/report.md`, `notes/<branch>.md` | A survey's gates table and its branch notes. The latest dated folder is the current survey. | The survey |
| `<YYYY-MM-DD>-<idea>/review.md`, `notes/` | The review of one business idea and its branch notes. | [`web-business-idea-deep-dive`](/product/skills/web-business-idea-deep-dive/SKILL.md) |

## The file

```json
{
  "schema": "market-watch/1",
  "updated": "2026-01-05",
  "thresholds": { "01": "<spend or users a year>", "02": "<growth over a year>", "03": "<entrants in two years>", "04": "<entrants with a filed profit>" },
  "sources": [
    { "id": "kr-online-shopping", "name": "<the release's name>", "url": "https://example.org/release", "cadence": "monthly", "free": true, "how": "<where the number stands on the page>" }
  ],
  "themes": [
    { "id": "example-theme-a", "name": "<theme in a few words>", "kind": "rising", "status": "watch",
      "ai_role": "<what AI does in the product or the operation>", "added": "2026-01-05", "next_check": "2026-01-19",
      "doc": "2026-01-05-entry-signals/notes/kr-consumer.md", "note": "<one plain line>",
      "gates": { "kr": { "01": "pass", "02": "partial", "03": "pass", "04": "unknown", "memo": "<do entrants earn; which year of the inflow>", "judged": "2026-01-05" } } }
  ],
  "metrics": [
    { "id": "kr-example-a-online-sales", "theme": "example-theme-a", "name": "<what is counted>", "unit": "KRW bn a month",
      "source": "kr-online-shopping", "gate": "02", "country": "kr",
      "observations": [
        { "read": "2026-01-05", "period": "2025-11", "value": 100.0, "grade": "official", "url": "https://example.org/release/2025-11", "note": "" }
      ] }
  ]
}
```

- **A source** is read again on its `cadence`: `weekly`, `monthly`, `quarterly`, `yearly` or `irregular`. A metric's `source` is a source id, or an address where the source is read once.
- **A theme** is `big` (money already moves there) or `rising`. Its `gates` hold, per country code, the verdict on each of the four questions in the vocabulary of [evidence-grades.md](evidence-grades.md), the memo and the day it was judged. `doc` is the note or the review that says more.
- **A metric** belongs to one theme and one country and is evidence for one gate. A figure for the whole world is a metric of the country whose gate it bears on, its note beginning `worldwide`: it is a proxy there. Its `id` is what a market report's ledger and a round's report point to, so it is never reused for another definition.
- **Two runs** may hold the file at once (a market report's delivery, a deep dive's, a round): read it just before writing, and change only the lines of the theme and the metrics this run adds.
- **An id** is lower-case words joined by hyphens, unique in its list, and never renamed.

## An observation

One line a reading: `read` (the day it was read), `period` (what the number is about: `2025`, `2025-Q4`, `2025-11`, `2025-11-17`), `value`, `grade`, `url`, `note`.

- A reading of a new period is a new line. A revision of a period already read is a second line with the same `period`; the later `read` is that period's value.
- A change is measured against the latest observation of an earlier period, never against a revision of the same one.
- A source that could not be read leaves a line with `value` null and the note `not published` or `not reached`; only the theme's `next_check` moves.
- `note` is one plain line of at most 200 characters, no Markdown. News changes the value or the note; what happened on which day goes to `log.md`.

## Statuses

| Status | Means | Who moves a theme here |
|---|---|---|
| `watch` | Measured every round. | The survey, when it adds the theme; the deep dive, when its idea is not on the list yet. |
| `candidate` | Worth the user's look: the rise was measured, not inferred. | A round, by its rule. |
| `testing` | The user is trying it. | The user only. |
| `cooling` | The measure it was raised on is falling. | A round, by its rule. |
| `dropped` | Set aside, with the reason in `note`. Still measured; never recommended again. | The user only, and only the user reopens it. A survey writes it for what the user ruled out at its start. |

The deep dive corrects the line of a theme that is on the list (its name, `ai_role`, `doc`, `note`, its metrics) and writes a dated line to `log.md`; it moves no status.

## What may be compared

Only values measured the same way: the same source, the same query, the same definition, the same unit. An ad count is compared only with a snapshot of the same market and category taken with the same terms, sort and locale. Where the way of measuring changed, the old metric ends and a new one begins under a new id.
