# Card-news skills

How the skills that make card news for a magazine-style social account (`instagram-cardnews-format-study`, `web-cardnews-topic-brief`, `html-cardnews-from-brief`) are written and kept in step, for authors. They drive three tool families (a website read with a driven browser, the open web, HTML rendered by a headless browser), so what they share is not a tool but two artifacts: the document set [`marketing/docs/cardnews/`](../../marketing/docs/cardnews/README.md) holds the shape of each, and this page says what goes there, what stays in a skill, and how the three are tested together.

## Three skills, two seams

The run these skills come from was one job in the user's words ("make a card-news post the way that account does it") and three jobs in the evidence: a study of the account, a research of the story, a build of the slides. Each is written as a skill that is complete alone and useful alone (a study of an account's format, a sourced brief for any post, a build from any brief), and the seams are written in the skill that needs the other's result: the build says where its spec and its brief come from and what it does with neither; the study and the research stay general.

| In `marketing/docs/cardnews/` | In the skill |
|---|---|
| `format-spec.md`: the fields of the spec, how each is measured and how the build reads it | How posts are read on the site, which posts, the slide log, the verdicts of the study |
| `topic-brief.md`: the fields of the brief, how each is obtained and how the build reads it | How candidates are searched and ranked, the facts table, the angle test, image sourcing |
| | The script's checks, the layout catalogue, the page, the server and export scripts, the review |

The test for a sentence: would the next skill that writes or reads a spec or a brief need it? Then it belongs in the set. Everything about one skill's method stays in that skill, because each may be mounted alone or copied.

## What the user corrected, and where it went

The run was sent back five times, and each correction is a rule in the skill whose phase it bears on, with the reason beside it: the density of a slide (counts, not impressions; the study measures them, the build keeps them), the thread (one thesis, text only where needed), the sourcing (every sentence to an article sentence; the angle published and quoted), the register (patterns with wrong-sounding counterparts, checked sentence by sentence), and the layouts (chosen by content, never a sequence repeated). A future run that meets a correction of the same kind sharpens that sentence rather than adding a note.

## Facts are dated, and instance material stays out

The site a study reads has no changelog: a statement about what is visible without signing in, how a carousel is stepped, or how a host's browser behaves carries the day it was checked and the way to find it again (`instagram-cardnews-format-study/references/tool-notes.md`). The layout defaults in the build skill are one account's measurements, marked illustrative; the spec wins over them. No account, outlet, story, person or photo from a run is named anywhere in these skills or in the set: examples use placeholders, numbers quoted from runs are shapes.

## Testing

Each skill is tried alone from a fresh session, and the three together with one request that needs all of them ("make a card-news post about <a stand-in topic> the way <a stand-in account> does it") at least to the build's plan checkpoint. What a fresh agent had to guess goes back into the files; a site that behaved differently changes the sentence in the study's tool notes, with the day; a finding about a field of the spec or the brief changes the shared page and the skill that writes it in the same change.
