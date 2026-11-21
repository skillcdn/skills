# In an account's folder

What this skill does differently where the working folder is an account's, which it is when it holds `docs/policy.md` or `topics/covered.md`. The record's shape (the policy's headings, a post's `post.json` and its states, the ledger and what overlaps a row) is in the pack's [account.md](/docs/card-news/account.md); read it first. This page says only how the research reads and writes that record.

## The policy answers the questions

Read `docs/policy.md` before the first message. Each line is the user's standing answer and a rule for the candidates, also where it is narrower than this skill's defaults:

| Heading | Becomes |
|---|---|
| Readers | The brief's `audience`. |
| Stance and tone | The brief's `stance` and `tone`. |
| Lane | The categories, and what is left out: a story outside the lane is not a card, however timely. |
| Follow-ups | Whether a later turn of a story the ledger holds is a candidate. |
| Window | The days searched, in place of seven, and how far ahead a season counts. |
| Ranking | The criteria, their points and the bar, in place of the order in [candidates.md](candidates.md): each card then carries its score with its parts, only a card at the bar or over is recommended, and one under it is kept as a spare, named as such. |
| Sources | The outlets, official pages and boards searched first. |
| Pictures | Whether a video goes before a photo and what a cover must show, for phase 3. |

The first message says in a line what was taken from the policy and asks only what the page lacks. An answer or a correction that holds for the account (the user says "always" or "from now on", or answers yes to "Should that stand for the account?", asked once) is written under its heading in the same run, and the message says so; a word that changes a line changes the line.

## The ledger before the search

Read the rows of `topics/covered.md` and the last candidate lists in `topics/` before searching: a post that is booked or still being made is covered, and a story shown and passed over is not offered again unless it moved.

Check each candidate against the rows by the record page's three tests. Where a row is close (a shared topic key, the same protagonist), open that post's slide plan and caption and look for the passage itself: a check by titles missed a follow-up that an earlier post had already told on one of its slides, and a check by how stories work threw out candidates that overlapped nothing. Each card gets one more line, `Overlap: <the nearest row and why this is another story>`, and a protagonist the ledger already holds is said there.

## The candidate list

Written as `topics/<YYYY-MM-DD>.md`, the day of the search, in place of the `candidates-<day>.md` of a one-off run, and left there: first the stories a rule kept off the list with the rule that caught each, or "none"; then the cards; then `Picked`, filled after the pick. A story from the first section that the user tells the account to cover is made, and its ledger row records their words.

## A pick becomes a post

For each pick, before its brief is written:

1. Add the row to `topics/covered.md`: the slug, `idea` with the day, what happened in one line, two to four topic keys, the protagonist.
2. Create the post's folder `posts/<YYYY-MM-DD-slug>/`, the day being the one the post is meant for (the user's, else the day of the pick), with `post.json` at `idea`. Where the folder has a template for a new post or a command that makes one, use it: the folder's own agreement says.

That folder is the brief folder: `topic-brief.json`, `img/`, `credits.md` and `facts.md` go into it. At the delivery set `status` to `brief` and rewrite the row's state. Where the folder has a check of its own, run it after the row and after the brief.

Several picks at once each get their row and their folder first; the briefs are then written one pick at a time, or side by side by `html-card-news-batch`.

## A same-day story

Where the policy lets the day's story replace a booked post, the search is the same method with a window of one day, started from the other end: the three to five stories everyone is on that day, across the outlets' front pages and the boards' best-of pages, then which of them touch the lane. The link to the lane is a fact like any other, with its article sentence, never supplied. A story a rule catches goes to the first section, as above.
