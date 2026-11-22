# Creative analysis

The method up to the checkpoint, phases 1 to 4: what to load, what to keep, what counts as proof, and the shortlist. How a creative is read and what the report holds is [deep-read.md](deep-read.md), read once the checkpoint has passed. Thresholds are working defaults; state them in the report and change them when the user asks.

## Search plan

Views are written here as the page-dump script's specs ([page-dump.md](/docs/meta-ad-library/page-dump.md) "The script"). On another route each key maps to a parameter of [ad-library.md](/docs/meta-ad-library/ad-library.md) "URLs": `media` to `media_type`, `sort=recent` to the most-recent sort, `before` and `after` to the date bounds, `page` to the advertiser view, `exact=1` to the exact phrase; `lines` only shortens what the script prints.

- **Terms.** Two to four, in the market's language, as buyers and sellers write them: the user's own keyword as given, which is the main term; the category word; a problem or benefit phrase; a named competitor when the user gave one (its advertiser view, or its domain as an exact phrase). A term of several words is searched in any order, the default, and as an exact phrase only when the user quoted it. For the user's own product, take the category words from its page. Where a language spells or spaces a word several ways, each variant is a different search: spend one load on a variant and keep it only when most of what it returns is not in the pool yet. A term whose first view is mostly off the subject is dropped, its other views unloaded.
- **Views per term**, one page load each: impressions order, all media (`q=<term>`); impressions order, video (`q=<term>&media=video`). Add impressions order for still images (`q=<term>&media=image_and_meme`) when the category sells with them or the user asked. When a term's first view fits on one page (`more` is false), its other views would repeat the same ads: skip them.
- **This week**, one load, for the main term only: most recent, all media (`q=<term>&sort=recent`). It returns ads a day or two old, which is the Fresh group and nothing for the shortlist.
- **Churn of the main term**, two loads: its counts by age (`q=<term>&before=7d`, `q=<term>&before=30d`; [ad-library.md](/docs/meta-ad-library/ad-library.md) "Counting by age") say what share of the active ads is new this week and what share has outlived a month.
- **Budget.** 40 page loads for the run: the views, the most-recent view, the two age counts, one advertiser view for each shortlisted seller and for the three sellers with the most entries in the cleaned pool, and a few spare. Note each view's count: together they are the landscape. A full research with frames for six videos has taken 15 to 24 page loads and 11 to 28 minutes; a shortlist of videos with their sheets, as the reference for an ad, 15 or 16 loads and four minutes.

Work in one folder, `ad-research-<subject>-<YYYYMMDD>/`, the subject in lowercase ASCII words joined by hyphens (translated when it is not written in Latin script), under the folder the user named for the run's outputs, else in the working directory when it is not a code repository, else in a folder outside it named at the checkpoint. Scripts, raw records and the load log go in `work/` inside it.

## Cleaning the pool

- **Relevance.** A keyword matches anywhere: in the text, in a Page name, in a link. Keep an ad only when its copy or its creative is about the subject. Judge by the text; when there is none, by the poster or the image. A neighboring product that competes for the same buyer stays, marked adjacent, and may enter the shortlist only as a benchmark.
- **Duplicates.** The same `group` in several views is one creative, even where the views show it under different IDs; keep its rank in each view. The same creative in several groups (the same opening line, the same poster) from one advertiser or its sister Pages is one entry: it takes the start date of its oldest copy, the best rank of any copy, the link of the best-ranked copy, and the number of copies as evidence.
- **Groups.** By advertiser (the Page), and by landing domain where the domain is the seller's own: several Pages often sell one store. A landing address that is a short link, a marketplace, an app store page or an in-app page (`fb.com/canvas_doc`) says nothing about the seller; group those by advertiser, and an app's several Pages by the app they install.
- **Drop.** Ads marked low impression. Catalog ads (`DPA`), which are feed templates and not creative decisions, unless the user asked about them. Ads whose landing page is off the subject. Keep the dropped ads and the reason in the data file.

## Proof

| Signal | Read from | Why it counts |
|---|---|---|
| Position | Rank 10 or better, as the page gives it, in an impressions-ordered view of a subject term that runs past one page | Meta puts the most-shown ads first. In a view that fits on one page the rank says little: lean on the other signals. |
| Survival | `days` of 30 or more while active | Advertisers stop what does not pay, and outside the EU and the UK the library keeps only what still runs. |
| Reuse | `uses` of 2 or more, or the same text and media found in two or more ads or Pages | The advertiser put it into more ad sets or accounts: it is being scaled. |
| Iteration | Siblings: separate ads that keep the hook and visibly change the edit or the text, started on a later day than the first. Versions inside one ad, and variants launched together on one day, are a test and not a sign. | The advertiser came back to the idea and built on it. |
| Tested account | The advertiser has 20 or more active ads (the count of its advertiser view, or of its landing domain as an exact phrase) | Where ads are launched constantly an old ad survived a cull; where there are three ads it may only be forgotten. |
| Reach | The ad details, in the EU and the UK only | The one number the library gives. |

| Tier | Rule | Place in the shortlist |
|---|---|---|
| Rising | Running 7 to 29 days, with Position, Reuse of 3 or more, or siblings | First: what is winning now. |
| Proven | Running 30 to 89 days, with Position or Reuse; stronger in a tested account | The core. |
| Evergreen | Running 90 days or more, still with Position or in a tested account | At most two, as benchmarks. |
| Fresh | Running under 7 days | Never on the shortlist, and no evidence about itself. Reported as a group: what advertisers are testing this week. |

An ad with no tier stays off the shortlist. The tested-account test needs the advertiser's count, which phase 4 loads for the shortlisted sellers and the three most present: give the tiers first from Position, Reuse and siblings, then read them again once those counts are in, and tier an ad that joined the pool from an advertiser view with the rest. A rank in the advertiser's own view is not Position; it is context for the breakdown. Say the counter-signals where they apply: a large brand runs awareness ads for months whatever they return; an active ad may be delivering nothing; a partnership ad may be a creator's post with a small budget behind it; an ad that ranks low in its own advertiser's view is not that advertiser's bet.

## Shortlist and checkpoint

Eight creatives by default. Tiers decide first (Rising, then Proven, then at most two Evergreen); among what qualifies, follow the format mix of the pool (about six videos and two stills where video dominates). At most two per seller, the Pages that lead to one site or one app counting as one seller; at least four sellers when the pool allows; different hooks before near-duplicates. Load the advertiser view (`page=<page_id>`) of each shortlisted seller's main Page and of the three most present once: the count is its active ads, the first page shows where the creative ranks among its own, and an on-subject ad the keyword views missed may join the pool. A video's length comes from `ffprobe` on its address, or from the player in a driven browser; with neither, the length column says unknown. On the driven-browser route, take each shortlisted ad's full record here, while its advertiser view is open.

The checkpoint is one message in the user's language:

1. What was derived, in a line: the market, the terms, the tier rules.
2. The landscape: active ads per term, the share that is new this week, the share that is video (ads with several versions count in both the video and the image view, so shares may pass 100 percent), the advertisers most present with their active ad counts.
3. The shortlist as a table: advertiser, format and length, days running, proof in a few words, the hook in a few words, the link by Library ID.
4. That one word continues to the deep read, and that an ad can be dropped or added, or a term or the market changed.
