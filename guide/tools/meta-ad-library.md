# Meta Ad Library skills

How the skills that read the Meta Ad Library (`meta-ad-library-…`) are written and kept in step, for authors. What the skills share at run time is the document set [`marketing/docs/meta-ad-library/`](../../marketing/docs/meta-ad-library/README.md), which agents read; this page says what goes there, what stays in a skill, how the site's facts are kept true, and how the family is tested.

## The tool is a website

There is no MCP server and no account to connect. A skill's "Requirements" name capabilities and how to recognize them (a shell with a Chromium-family browser on the same machine, a browser the agent drives), never one product's tool names: every assistant names its browsing tools differently and replaces them within months. A named product is a dated illustration at most.

## What is shared and what stays in the skill

| In `marketing/docs/meta-ad-library/` | In the skill |
|---|---|
| `ad-library.md`: what the library is evidence of, the routes, the URL parameters, what a result carries, counting by age, what needs a click, manners and limits, when no route works | What to search (the terms and the views), the page-load budget, the cleaning, what counts as proof or as an item, the classes, the checkpoint, the report and its data file |
| `record.md`: the record every route yields, where each field comes from, how long media addresses last | The fields the skill adds to its own data file (`assets/*.example.json`) |
| `page-dump.md`: the shell route and `adlib.py` | |
| `driven-browser.md`: what a driven browser does on the site, the in-page readers, the reach script | The frame script of the creative research skill |

The set sits in the area's `docs/` rather than the repository's because both skills are marketing skills: it travels with the marketing mount and the marketing plugin, and only a skill mounted alone or copied lacks it, which its Requirements say. The test for a sentence: would it be true in the next skill that reads the library? Then it belongs in the set. A page of the set is linked with a root-relative path and, until the spec's shared pages are served, not included; each skill includes its own method page instead, so that the method arrives with the skill and the shared pages cost one `read_repo_file` each when their phase comes. Once they are served, `ad-library.md`, which every run reads before its first page load, goes into each skill's `skillcdn.include` by its root-relative path.

## Facts are dated, and rediscoverable

The site has no changelog. A statement about a parameter, a label or a field carries the day it was last checked, and next to it the way to find the value again: the address bar after a filter is set by hand, one card's text for a label, the keys of the JSON in the page. When a run finds a statement wrong, fix both the statement and the way to rediscover it, in the sentence it bears on; the pages keep no log of runs ([skill-authoring.md](../skill-authoring.md) "Knowledge pages").

The readers hold on to the JSON keys in the page and to the visible English labels (`locale=en_US`). Class names on the site are generated; never write a selector that depends on one.

## Check before changing

Five page loads show whether the set still describes the site: a keyword search (a count and Library IDs), the same with the most-recent sort, an advertiser view, a search with a date upper bound, and one ad by `id`. The script in `page-dump.md` prints what each page gave:

```sh
python adlib.py check.jsonl US "q=<word>" "q=<word>&sort=recent" "page=<page id>" "q=<word>&before=30d" "id=<library id>"
```

The in-page readers of `driven-browser.md` and the frame script of the creative research skill are checked the same way in a driven browser: paste, run, compare with the page.

## Manners are part of the skill

Page-load budgets, two seconds between loads, one page at a time, no sign-in, and no way around a browser check, a login wall or a block. Meta's terms restrict automated collection; these skills stay at the scale of one person's research and say so in their rules. Do not add bulk collection, scheduled crawling, or anything that disguises the browser.

## Examples name no one

Reference files, the set and the assets use placeholders (`example-store.com`, `000000000000001`). Numbers quoted from real runs are aggregates. No real advertiser, Page or ad is named in the repository.

## Testing

Exercise both machine routes: the page dump from an agent with a shell, the driven browser from an assistant that has one. Media addresses expire within days, so a test collects and reads in one run. What a fresh agent had to guess goes back into the files; what the site did differently goes into the sentence of the set that it bears on, with the day it was seen.

A skill that makes ads may start from this research when the user has no reference. The choice among the shortlist is that skill's, and the research stays general. One request that needs both ("make an ad for this product", with no reference) exercises the seam; run it at least to the producing skill's cost checkpoint, and read what the agent chose and why before reading what it made.
