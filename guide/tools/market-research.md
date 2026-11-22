# Market research skills

How the skills that find a market to enter, measure it again, look into one business idea, read a company's filings and put the result out as a market report issue are written and kept in step, for authors. What they share at run time is the document set [`docs/market-research/`](../../docs/market-research/README.md), which agents read; this page says what goes there, what stays in a skill, and how the chain is tested.

## The tools are public sources, and the chain is the job

Four skills of two areas, and one mode of a fifth: `web-market-entry-signals` (the survey and its later rounds), `web-business-idea-deep-dive` and `dart-company-figures` in `product/`, `html-market-report-deck` in `design/`, and the watch mode of `meta-ad-library-rising-products`. They read official statistics, filings, app stores and the public ad library with a search tool, a page reader or a driven browser, and a shell for their scripts; there is no account to connect. A skill's Requirements name those capabilities and how to recognize each, never a product's tool names.

The measuring again is not a skill of its own. A round reads what is due on the watch list, by the same gates, into the same file as the survey that wrote it, so it is a second entry into `web-market-entry-signals` (`references/round.md`), read only when a watch list exists and a round is asked or due. A repository that keeps running rounds is a studio, set up by `git-studio-setup`, which keeps the record, the log and the next date; the round's method stays in the skill.

The seams are written in the skill that needs the other's result, with a link to the other's `SKILL.md`: the survey says how it calls the ad count and the company figures, the deep dive where its idea comes from, the market report where its research and its company cards come from. `dart-company-figures` and `meta-ad-library-rising-products` stay general: their descriptions name their callers, and their bodies depend on none.

## What is shared and what stays in the skill

| In `docs/market-research/` | In the skill |
|---|---|
| `evidence-grades.md`: the four vocabularies (the grade of a number, the check of a number against its source, the check of a company's announced figure against its filing, the verdict of a gate), one table each | Which grade a skill accepts for which use: the survey's verdict cells, the market report's company cards |
| `watch-record.md`: the watch list's shape, the observation line, the statuses and who moves which, what may be compared, the files of a market folder | The gates and their thresholds (`references/gates.md`), how entrants are counted (`references/entrant-count.md`), the branch brief and note, the round, the schema, the example and the two scripts, all in `web-market-entry-signals` |
| `sources.md`: the public sources read again, by country, with when each comes out and how its number is found | What a skill searches beyond them, and its budget of searches |
| `README.md`: who hands what to whom, and what every skill of the set does the same way | The handover itself, in the receiver's Inputs |

The test for a sentence: would it be true in the next skill of the set? Then it belongs in the set; else in the skill. The set sits at the root because skills of two areas include `evidence-grades.md`, and the format serves an include to two areas only from there. That page is included by all four skills, so an edit to it reaches each on its next load and changes each one's served digest: keep it to tables. The other pages are read at the step that names them, and the indexer's check prints what each skill includes.

## One change, several files

- **A vocabulary changes in one change**: `evidence-grades.md`, the lists in `scripts/check-watch.mjs` (`GRADES`, `VERDICTS`, `STATUSES`, `CADENCES`), `assets/watch.schema.json`, and the `check` values `dart-company-figures` writes.
- **The watch list's schema is versioned** (`market-watch/1`). A field added is a new schema string, a line in `watch-record.md`, the schema file, the example and the checker together; `watch.mjs` must still print an older file.
- **The file names between the skills are fixed**: `watch.json`, `log.md`, `snapshots/<YYYY-MM-DD>-meta-<market>-<category>.json`, `<YYYY-MM-DD>-entry-signals/report.md` with `notes/<branch>.md`, `<YYYY-MM-DD>-<item>/review.md`, `figures.json`. A rename is a change to every skill of the set and to `watch-record.md`, "The market folder".
- **The snapshot is the ad library skill's.** Its schema, its file name and its compare script live in `meta-ad-library-rising-products`; the survey and the round call that skill's watch mode and run its script, and carry no copy.
- **The renderer is the product deck's.** `html-market-report-deck` runs `scripts/render.mjs` of `html-product-deck`, linked as that skill's file: a check the market report needs is added there in a way the product deck is not changed by.

## Facts are dated, thresholds are defaults

A row of `sources.md` carries the month its address was opened; a round that finds one moved changes the row, with the new month. A route into DART's site carries the month it was checked and the way to find it again, in the company figures skill. The thresholds of the gates are working defaults, shown at the plan and changed on the user's word; a share or a threshold taken from the first run is marked as an illustration and is not a finding.

## Examples name no one

No theme, market, company, verdict or reason of any real survey enters the files: examples are `example-theme-a` and `<placeholders>`, a company is `<company>`, a figure is a placeholder value. The market report's scene templates hold placeholder text and no logo. The subject of a fresh run is a public one that has nothing to do with the organization.

## Testing

- **The survey**: one fresh run on a public subject in two countries. Look for the budget per branch said at the plan, entrants counted by a source that can be counted again, an address in every verdict cell, a "Not seen" at the end of each note, and `check-watch.mjs` passing.
- **The round**: a placeholder watch list (three themes, six metrics, a made-up first observation) and one fresh round. Look for the targets chosen, the line written for a source that could not be read, the snapshot comparison, the check, and a report of three lists only. The round is designed and has met no real round: its status rules are the first thing to revisit when one is folded in.
- **The company figures**: three public companies, one listed (a consolidated business report), one unlisted and audited (a separate audit report), one subsidiary of a listed parent (the announced figure consolidated, the sum matched in the parent's report).
- **The deep dive**: two fresh runs on public ideas, in two countries and two kinds of customer.
- **The market report**: a short issue of six to eight slides from placeholder research and one public brand site: the tokens taken from the site, an address and a check on every line of the ledger, small figures that all differ, the closing view checked against its slides, the render's findings at zero.
- **The chain**: one request that needs it whole, the survey, two entrants through the company figures, then a short issue. A seam is tested only by a request that crosses it.

A change to a skill of the set is dry-read before it is pushed, and a run is read against the files as `skillcdn-skill-verification` says; what a source did differently goes into the sentence of the set it bears on.
