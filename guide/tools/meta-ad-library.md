# Meta Ad Library skills

Conventions shared by the skills that read the Meta Ad Library (`meta-ad-library-…`). For authors: a skill still carries what it cannot work without in its own `references/`, because it may be mounted alone and this page is not discoverable.

## The tool is a website

There is no MCP server and no account to connect. A skill's "Requirements" name capabilities and how to recognize them (a shell with a Chromium-family browser on the same machine, a browser the agent drives), never one product's tool names: every assistant names its browsing tools differently and replaces them within months. A named product is a dated illustration at most.

## Two shared references, kept identical

| File | Holds |
|---|---|
| `references/ad-library.md` | What the library is evidence of, the routes, the URL parameters, the fields of a result, counting by age, what needs a click, manners and limits, what to do when no route works. Included with the skill. |
| `references/collectors.md` | The record, the page-dump script, the in-page readers, the script that reads reach, notes from real runs. Linked, and read before the first page is loaded. |

Both are the same file in every skill of the family. Change every copy in one commit, scoped to the area, and compare them before committing:

```sh
diff marketing/skills/meta-ad-library-creative-research/references/ad-library.md marketing/skills/meta-ad-library-rising-products/references/ad-library.md
diff marketing/skills/meta-ad-library-creative-research/references/collectors.md marketing/skills/meta-ad-library-rising-products/references/collectors.md
```

What belongs to one skill (how a creative is read, how an item is classed) lives in that skill's own reference.

## Facts are dated, and rediscoverable

The site has no changelog. A statement about a parameter, a label or a field carries the date it was last checked, and next to it the way to find the value again: the address bar after a filter is set by hand, one card's text for a label, the keys of the JSON in the page. When a run finds a statement wrong, fix both the statement and the way to rediscover it.

The readers hold on to the JSON keys in the page and to the visible English labels (`locale=en_US`). Class names on the site are generated; never write a selector that depends on one.

## Check before changing

Five page loads show whether the references still describe the site: a keyword search (a count and Library IDs), the same with the most-recent sort, an advertiser view, a search with a date upper bound, and one ad by `id`. The script in `collectors.md` prints what each page gave:

```sh
python adlib.py check.jsonl US "q=<word>" "q=<word>&sort=recent" "page=<page id>" "q=<word>&before=30d" "id=<library id>"
```

The in-page readers of `collectors.md` and the frame script of the creative research skill are checked the same way in a driven browser: paste, run, compare with the page.

## Manners are part of the skill

Page-load budgets, two seconds between loads, one page at a time, no sign-in, and no way around a browser check, a login wall or a block. Meta's terms restrict automated collection; these skills stay at the scale of one person's research and say so in their rules. Do not add bulk collection, scheduled crawling, or anything that disguises the browser.

## Examples name no one

Reference files and assets use placeholders (`example-store.com`, `000000000000001`). Numbers quoted from real runs are aggregates. No real advertiser, Page or ad is named in the repository.

## Testing

Exercise both machine routes: the page dump from an agent with a shell, the driven browser from an assistant that has one. Media addresses expire within days, so a test collects and reads in one run. What a fresh agent had to guess goes back into the files, and what the site did differently goes into "Notes from real runs" with its date.

A skill that makes ads may start from this research when the user has no reference. The choice among the shortlist is that skill's, and the research stays general. One request that needs both ("make an ad for this product", with no reference) exercises the seam; run it at least to the producing skill's cost checkpoint, and read what the agent chose and why before reading what it made.
