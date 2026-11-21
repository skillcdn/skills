# Candidates: finding and ranking this week's stories

How the candidate list is searched, ranked and written. The list is what the user picks from, so each card says enough to choose and no more. In an account's folder the policy changes the window, the ranking and what is left out ([account.md](account.md)); everything else here holds for every run.

## Searching

- **By category.** One search per category, in the market's language, for the window (the last seven days unless the request or the policy says more): the category's words plus the week or a dated event. Where the search tool has a thorough mode, use it for the first pass of each category; thin results get a second phrasing before the category is dropped. A category whose words can be read two ways (a place's name: its events this week, or everything about it) is read the broader way, and the first message says how it was read.
- **Where people talk.** Outlets alone bring stories that have already cooled. Look also at what the market's readers are talking about now in the categories: the best-of pages of its large community boards, the trending lists of its social platforms, a search engine's trends. Find them by a web search in the market's language where neither the request nor the policy names them. A board or a platform that answers with a check, a login or an error is not read from this host, with no sign-in and no request dressed up as a browser's; its talk is then found, in this order, by a search limited to the site, which gives titles and no counts, and by outlets' articles on what communities are talking about, whose quoted figures are the outlet's and are said so. [walls.md](/docs/browser/walls.md) has the whole order of ways around a site the host cannot reach. With neither, the card says "outlets only".
- **Seasons and dates.** Before the first search, list what the market's readers meet in the coming three weeks and met in the last one (an exam, a holiday, a sale season, an election, an awards night), and give each category one more search with those that could touch it.
- **A domestic audience:** the market's outlets and boards first; a global story only where the market's reader is part of it (a visit, a release there, a rule that changes there). **A global audience:** the international ones, and the market's angle noted where there is one.
- **The card's line comes from an article's body.** Open the one or two articles a card cites and write what happened from what the body says: a headline, a search summary and a community post each gave a line the body did not carry. Note there whether the story moved in the window (a release, a ruling, a number published, a date set) and what the pages show. The articles are read in full only after the pick.
- **A community post is a lead.** It says where to look and how loud the talk is; it is never a source, its author is not named anywhere, and a reaction goes on a card only as an outlet reports it.
- **Side by side, where the host can.** With a tool that starts agents side by side, the search may be split by region or by category, one agent each, given the categories, the audience, the window, the seasons, what is excluded and the card below; the first message says so. Their cards are leads: this run opens each card's article itself, checks the exclusions itself, and ranks. Without such a tool the same searches run one after another.

## What is left out

What the account has covered: the rows of its ledger in an account's folder (account.md), else the stories in the format spec's `posts_read`, matched by subject against each post's first line; with neither, nothing, and the list says so. A new development this week of a story the account posted is a candidate, said so on its card, unless the policy says follow-ups are not new stories. What a word of the user's or the policy's lane leaves out is left out too.

Nothing hot is dropped silently. Of the stories a rule kept off the list, the two or three most talked about go above the cards, each with what happened, where it is talked about and the rule that caught it; the user may pick one, and the rest are named in a line under the list.

## Ranking

| Criterion | What counts |
|---|---|
| Fit | The story belongs in one of the categories (as the account's own posts define them when a spec exists, as the user's words define them otherwise), and it is the audience's story. |
| Timeliness | It moved in the window; the newest movement is the hook. A date still to come ranks above one already past, and a story that touches a season or a date from the list above ranks higher while that date is ahead. For an exhibition or a performance that runs for months, the movement is its opening, its closing, an extension or a ticket release. |
| Talk | People are talking about it now: on several boards or platforms with large counts, on one, or in outlets only. |
| Save and share | A reader would save it (a rule that changes, a guide to a day, a list of places) or share it (a surprise, a number that reframes something). |
| Images | A video of the event or by the subject exists, the articles carry photographs of the subject, or they cite a public clip that shows it; a story with only logos or stock imagery costs a cover. Left out for a brief that takes no images. |
| Breadth | Two or more outlets carry it, so facts can be cross-checked; a story one outlet carries is not a card, and is named in one line under its category as a lead. |

The criteria are in order of weight: fit, timeliness, talk, save and share; images break ties, and breadth is the floor. Five to eight candidates in all, at most three per category, unless the request or the policy asks for more: a request for a batch of posts keeps its count and half again, so that there is something to pick from; a request that names one category keeps three, and the rest as leads under the list. A category with nothing timely is said so rather than filled, and a list is never padded to its number. A guide that gathers several events of the week (a list of places, a day's dates), each carried by two or more outlets, is one candidate, and its card says that the outlets may share no angle, which makes the post a report.

## The candidate card

```
<n>. <what happened, one line with the date>
   Angle: <the post a reader would want, one line>
   Why now: <the movement in the window; the season or date it touches>
   Talk: <where it is talked about and how much, as read or as an outlet reports it; or "outlets only">
   Articles: <outlet, date>; <outlet, date>; ...
   Images: <a video of the event or the subject's own, and whose; what the article pages show; or "none seen">
```

A card's articles are leads to read in phase 2, not yet sources. The angle on a card is a suggestion for the pick, not the brief's angle: the brief's angle is found in phase 2 among the articles' own interpretations, and may differ.

## Presenting

First the stories a rule kept off the list, where there are any. Then the categories in the order of their best card, the cards ranked inside each and numbered across the whole list. Recommend one card in a line, with the reason, and ask for a number or a story of the user's own; say that the pick also lets its images be collected. A user who answers with a correction of the audience gets the list again, re-ranked, before they pick.
