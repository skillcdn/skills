# Where the site refuses the host

Read when the site's first page fails from the host, twice a few seconds apart, in the browser at hand, while a second site loads. That is the host's wall ([walls.md](/docs/browser/walls.md) "The host's wall"): nothing of the site is read from this host, by no proxy, mirror or disguised request. The order of the ways below, the go-ahead and the fall-through are that page's; this one says what each way is for this skill and what its spec lacks.

## The first message

Say that the site did not load from this host, measure nothing, and offer the ways in their order with what each leaves out of the spec and the recommendation; one word continues. On a go-ahead take the first way the host allows, said so; a way that fails gives way to the next, never to samples while a way above them is open.

| Way | What is read | What the spec lacks |
|---|---|---|
| 1. A browser of the user's own that the host drives (an extension in the user's browser, a browser pane the user opened). Recommended where the host has such a tool | The site's own pages, as phases 1 and 2 say | Nothing |
| 2. A local agent with a shell on a machine the site answers. Named as what to add: the run moves there | The same | Nothing |
| 3. The same posts where the account publishes them itself: its own site, or a portal's channel page of its own, as outlets, parties and organizations often do with every slide at full size, the date and the caption. Recommended where the host drives no browser of the user's and the account is such a publisher | Each slide from that page, as supplied slides (below) | `cadence`, the categories' shares, the posts visible; the page may carry only old posts, so each post's date is recorded |
| 4. Slides the user supplies as images | The user's screenshots or saved images of every slide of each post, as supplied slides | The same as way 3, and whatever the user did not send |
| 5. Samples found by a search | Three to five accounts of the reference's genre ("Samples from a search") | The reference itself: the spec is a format of the user's own in the genre, said to be so, never the reference's |

The page of way 3 is found by a web search for the account's name with "card news" in its language, never by a guessed address, which answers with an error or nothing. A reference that none of ways 1 to 4 reads becomes its genre, by way 5.

## With no reference named

The candidates ([genre.md](genre.md)) are then the accounts of the kind whose card news is readable outside the site, which the same web search names: an outlet's, a party's or an organization's own site or portal channel page, a forum's or a blog's repost with the account's mark. Each is listed with the page that carries its card news; the pick, or the recommendation on a go-ahead, is read from that page as supplied slides are, into a measured spec of that account. An account whose own channel carries a run of its card news at full size is a reference read this way and never a sample of its genre: read as samples, its values end up set by eye and nothing is measured. The genre's common form from samples is read only where no candidate's page carries a carousel or more than a cover.

## Supplied slides

For ways 3 and 4. From the user: every slide of each post, in order, one set per post with the post's date and its caption as text (a screenshot cuts a caption), a video post as three frames, and the name line and bio where they send them.

- Show each image in a page of the run's own in the browser at hand, driven or headless, one slide at a time at the canvas width, so that the screenshot, the zoom and the pixel rows are read as on a post page (reading-posts.md "Measuring sizes and colors"). On a phone screenshot the post's box is the region between the post's top and bottom edges, found once per post; the chrome around it is not the canvas. The pages and the crops stay in the run's folder under the host's scratch folder and go with its screenshots.
- `profile.md` holds what was read and from where, each post named as the page or the user names it; that name is its id in `seen_in` and `posts_read`.
- `cadence`, the categories' shares and the posts visible are left out of the spec and named in the delivery. `source.read` is `supplied`, for samples too, and `account` records it with the day.
- The platform's documented sizes are on the blocked site: the spec takes the value signed-out.md "The documented sizes" carries, with the day it was read there, marked illustrative, and the delivery says so.
- At the spec checkpoint, a kind seen once is confirmed by the user sending that kind's slides, since no older post can be opened.

## Samples from a search

For way 5, and for the genre's common form where no candidate's page carries more than a cover.

1. **Search**, in the market's language: a web search for the genre's words with "card news" and the platform's name (for a named reference, also its account's name with "card news"), which names the genre's accounts and the pages that carry card news with an account's name on them; and an image search engine's results page for the same words, opened in the browser at hand and never fetched by a plain request, which gets another, thinner page. The query leaves out the story's words: the genre's words with "card news" and the platform's name found dozens of samples on one results page, the genre's word with "card news" alone found unrelated pictures, and queries that carried the story's words found none (checked 2026-10).
2. **Take each result's page**, not its image: a results page lists each image with the address of the page it sits on, carried in the result's data beside the image's address (one engine, checked 2026-10), and a headless browser screenshots the results and reads those addresses from them. An engine whose results carry no page address is left for one that does.
3. **Open the page and read the image there**, never the thumbnail. The page shows the account (its name in the text, or its mark on the slides) and the image at full size, often the whole carousel with the post's date and caption; a community forum's or a blog's repost whose slides carry the account's mark, and a party's or an outlet's own page, are such pages and are most of what a results page lists. A page that shows no account, or only a thumbnail, is skipped and another found.
4. **Judge the sample's kind on its page**: a party's, an organization's or an outlet's card news is a sample of the genre whatever its subject, so a results page whose thumbnails are about other stories than the user's is not empty.
5. **Measure** each slide as a supplied slide: an `img` of the image's address inside a box of the canvas size, so that no file is written, screenshotted and read. An image narrower than about half the canvas gives its anatomy and its counts; its sizes and colors are marked as estimates from a small image. One carousel per account where the page carries one, else its cover and the body slides it shows; three to five accounts.

`slide-log.md` holds one row per sample slide, the page as the post's id; `profile.md` lists the search, each page, the account it shows and the day in place of a profile, and the genre's kinds are named from the samples' covers in plain words.

## The spec from samples

The spec holds what was measured: the cover as the samples share it and the body types two accounts showed, with the density counted on their legible slides; a type one sample showed is tentative. What no sample showed (a type, a density, the caption's register, the slide count, `cadence`, the shares) is left out and named in the style notes, never set here: the study designs nothing, and the variations design the rest ([format-spec.md](/docs/card-news/format-spec.md) "Where a spec comes from"). The samples are of the genre and not of one account, so `never` stays empty.

## Verdicts

| Result | Verdict |
|---|---|
| A sample that is a thumbnail, or whose page shows no account | Not measured: its page is opened and the image read there, else the sample is dropped and another found |
| No sample found for the genre | Say so; no spec is written, and the next way is named: the variations from the genre as the agent knows it, marked unseen, else the build's stand-in |
| Supplied slides or samples shown but not counted | Count them before the spec is written (characters per line, lines, sentences per slide, the edges of each block); a spec whose values were set by eye is not delivered as this skill's, and a field no count reached is left out and named for the variations |

## What the spec and the delivery say

`account` records how the posts reached the agent, the day, and what was not read; the checkpoint and the delivery say which way was taken and what the spec lacks because of it. A spec from samples is called a format of the user's own in the genre at every mention.
