# Sourcing: the facts table, the cross-check, the angle

How facts are taken from articles so that every sentence of a post can be traced, how numbers are checked across outlets, what qualifies as the post's angle, and what goes on the unverified list.

## Reading

Three or more articles from different outlets, each read in full: the body, the captions, the dates. Where a page reader returns the article as text, read all of it; where only a driven browser reaches it, read it there. An article is read in full when its end was reached: the last paragraph followed by what closes an article on that site (a byline or date line, the reporter's e-mail, the tags, a copyright line, the related-articles block); a text that ends mid-sentence or without that closing was cut by the reader and is read again in the driven browser. A text extraction that strips the page's footer hides the copyright line: look for the closing in the raw HTML, and where the footer is loaded by script, the reporter's e-mail or the tags are the close. An article that stops at a paywall, a login or a consent wall that cannot be declined is not a source; find the story in another outlet. Where the outlets refuse this host itself and fewer than two that carry the pick can be read in full, the run stops, as [tool-notes.md](tool-notes.md) "A site this host cannot read" says.

An outlet's article is a news organization's report, analysis or interview under a byline or a desk. An influencer's post hosted on a portal, a post on a community board or a social platform, a listing or aggregator site, a blog and a wiki are not articles: they are leads, and a detail only they carry (an exact address, a last-entry time, how people reacted) goes to the unverified list. An article that reprints an organizer's release (the release's wording before the event, the photos credited to the organizer) counts as the official release for the cross-check, and the fact's `note` says `organizer's release reprinted`. An organizer's, a venue's, an institution's or the subject's own page or notice (a release, an advisory), or a document the articles cite as their source, is a source for a schedule, a price, an address, an opening, or an identifier, a version or a date of its own matter, and for nothing else: the fact's `source.kind` is `official` and `single_source` is true, and the story itself still needs an outlet's article.

Record per article, in the brief's `articles_read`: outlet, author where named, date and time of publication, URL, and whether it is a report, an analysis or an interview.

## The facts table

One row per fact the post could use:

| Column | What goes in |
|---|---|
| `id` | `f1`, `f2`, ... in the order of the story; an id never changes once a checkpoint has shown it. |
| `text` | The fact as one sentence in the post's language, with absolute dates and the unit. |
| `kind` | number, date, place, quote, event, claim. |
| `source` | Outlet, date, URL, the article's own sentence, quoted exactly, and `kind`: `article`, or `official` for an organizer's, a venue's, an institution's or the subject's own page or notice, or a document the articles cite as their source. |
| `also_in` | Other articles read that carry the same fact, as outlet and date. |
| `single_source` | True when no other article read carries it. |
| `note` | Optional: a caveat the build must keep (a market figure an outlet quotes from a third party, which needs that party named if used). |

## The cross-check

Every number and date is looked for in every article read. Where two agree, both go in `also_in`. Where two differ:

- Record both values with their sources in `disagreements`.
- Prefer, in this order: the value that quotes an official release or document; the outlet that reported first; the article that explains how the number is made up. Write the reason.
- Where the sum of parts does not match a total in the same article, say so; the total is the suspect value.

## The angle

The angle is what the post says the story means, and it must already have been said in print: the sentence of an article that interprets the story, quoted with its outlet and date, and shared in substance by at least one other article. An expert quoted in an article gives an angle; a reporter's framing in the lead gives an angle; an organizer's quoted words support one but are not one alone; the agent's own sense of why the story matters does not. Where the articles carry no interpretation, the brief says the story has no angle yet and the post stays a report. Where the outlets printed more than one reading that qualifies, the one that speaks to the brief's readers is the angle and the others go in `angle.alternatives` with their own sources, offered at the checkpoint; where none speaks to those readers, the shared reading stands and the facts and the beats are chosen for what they need to know and do. Where the stance is a side's case, the angle is that side's published reading or its spokespeople's as an outlet printed it, the other side's reading goes to `alternatives` and its reply among the facts, and the facts and quotes most unfavourable to the other side are gathered first, each attributed. A thesis that sounded right was challenged by the user and held only because two outlets had printed it: quote the sentence in the brief so that the next reader need not take the agent's word, and in chat point to the fact's id and the outlet.

## The unverified list

What the post would like and no article confirmed, each with what was looked for and where:

- An account handle for a mention (the subject's official account, the organization's): found on the subject's own site or not; never guessed from a name.
- An official notice (a schedule, a re-issue, a change) mentioned in one article without a document behind it.
- A figure from a secondary source (a wiki, an aggregator) that no outlet's body repeats.
- A comparison or a superlative the agent would like to make: dropped from the facts, listed here if the user may want to source it.
