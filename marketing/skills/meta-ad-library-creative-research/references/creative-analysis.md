# Creative analysis

The method of phases 3 to 8: what to load, what to keep, what counts as proof, how a creative is read, and what the report holds. Thresholds are working defaults; state them in the report and change them when the user asks.

## Search plan

- **Terms.** Two to four, in the market's language, as buyers and sellers write them: the category word; a problem or benefit phrase; a named competitor when the user gave one (its advertiser view, or its domain as an exact phrase). For the user's own product, take the category words from its page. Where a language spells or spaces a word several ways, each variant is a different search: spend one load on a variant and keep it only when most of what it returns is not in the pool yet. A term whose first view is mostly off the subject is dropped, its other views unloaded.
- **Views per term**, one page load each: impressions order, all media (`q=<term>`); impressions order, video (`q=<term>&media=video`). Add impressions order for still images (`q=<term>&media=image_and_meme`) when the category sells with them or the user asked. When a term's first view fits on one page (`more` is false), its other views would repeat the same ads: skip them.
- **This week**, one load, for the main term only: most recent, all media (`q=<term>&sort=recent`). It returns ads a day or two old, which is the Fresh group and nothing for the shortlist.
- **Churn of the main term**, two loads: its counts by age (`q=<term>&before=7d`, `q=<term>&before=30d`; [ad-library.md](ad-library.md) "Counting by age") say what share of the active ads is new this week and what share has outlived a month.
- **Budget.** 40 page loads for the run: the views, the most-recent view, the two age counts, one advertiser view for each shortlisted seller and for the three sellers with the most entries in the cleaned pool, and a few spare. Note each view's count: together they are the landscape.

Work in one folder, `ad-research-<subject>-<YYYYMMDD>/`, the subject in lowercase ASCII words joined by hyphens (translated when it is not written in Latin script). Scripts, raw records and the load log go in `work/` inside it.

## Cleaning the pool

- **Relevance.** A keyword matches anywhere: in the text, in a Page name, in a link. Keep an ad only when its copy or its creative is about the subject. Judge by the text; when there is none, by the poster or the image. A neighboring product that competes for the same buyer stays, marked adjacent, and may enter the shortlist only as a benchmark.
- **Duplicates.** The same `group` in several views is one creative, even where the views show it under different IDs; keep its rank in each view. The same creative in several groups (the same opening line, the same poster) from one advertiser or its sister Pages is one entry: it takes the start date of its oldest copy, the best rank of any copy, the link of the best-ranked copy, and the number of copies as evidence.
- **Groups.** By advertiser (the Page), and by landing domain where the domain is the seller's own: several Pages often sell one store. A landing address that is a short link, a marketplace or an in-app page (`fb.com/canvas_doc`) says nothing about the seller; group those by advertiser.
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

An ad with no tier stays off the shortlist. A rank in the advertiser's own view is not Position; it is context for the breakdown. Say the counter-signals where they apply: a large brand runs awareness ads for months whatever they return; an active ad may be delivering nothing; a partnership ad may be a creator's post with a small budget behind it; an ad that ranks low in its own advertiser's view is not that advertiser's bet.

## Shortlist and checkpoint

Eight creatives by default. Tiers decide first (Rising, then Proven, then at most two Evergreen); among what qualifies, follow the format mix of the pool (about six videos and two stills where video dominates). At most two per seller, the Pages that lead to one store counting as one seller; at least four sellers when the pool allows; different hooks before near-duplicates. Load the advertiser view (`page=<page_id>`) of each shortlisted seller's main Page and of the three most present once: the count is its active ads, the first page shows where the creative ranks among its own, and an on-subject ad the keyword views missed may join the pool. A video's length comes from `ffprobe` on its address, or from the player in a driven browser. On the driven-browser route, take each shortlisted ad's full record here, while its advertiser view is open.

The checkpoint is one message in the user's language:

1. What was derived, in a line: the market, the terms, the tier rules.
2. The landscape: active ads per term, the share that is new this week, the share that is video (ads with several versions count in both the video and the image view, so shares may pass 100 percent), the advertisers most present with their active ad counts.
3. The shortlist as a table: advertiser, format and length, days running, proof in a few words, the hook in a few words, the link by Library ID.
4. That one word continues to the deep read, and that an ad can be dropped or added, or a term or the market changed.

## Deep read

One breakdown per shortlisted creative.

**Copy.** The primary text and above all its first line, which is the hook in text (about the first 125 characters show before "See more"). The headline, the description, the button. The landing page by kind: product page, collection, article or listicle, quiz, lead form or message, in-app page, marketplace store, app store.

**Video, with a shell and `ffmpeg`.** `ffmpeg` reads the video's address directly, so no copy of the video is kept: only two small contact sheets per ad, as working files. One request at a time, as with pages.

```sh
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$URL")
ffmpeg -v error -y -t 3 -i "$URL_HD" -vf "fps=2,scale=480:-2,tile=3x2" -frames:v 1 "frames/hook-$ID.jpg"
ffmpeg -v error -y -i "$URL" -vf "fps=1/$N,scale=200:-2,tile=6x$ROWS" -frames:v 1 "frames/sheet-$ID.jpg"
ffmpeg -v error -y -ss "$T" -i "$URL_HD" -frames:v 1 "frames/frame-$ID-$T.jpg"
```

- `URL` is the record's `video`; `URL_HD` is its `video_hd`, or `video` when there is none.
- The hook sheet is the first three seconds, six frames half a second apart, read left to right and top to bottom, large enough to read the words on screen.
- The overview sheet is the whole ad. `N` is the duration divided by 24 and rounded up, at least 1: one frame every N seconds. `ROWS` is the number of frames (the duration divided by N, rounded up) divided by 6 and rounded up; the tile filter needs both dimensions.
- The last command takes one frame at second `T` at full size, for small print the sheets do not show.

Look at the images: a sheet that was made and not looked at was not read, and each breakdown says which sheets it comes from. Where a speech-to-text tool is installed, extract the audio (`-vn -ac 1 -ar 16000`) and transcribe it; where none is, the burned-in captions on the frames carry the script, and the report says the audio was not transcribed.

**Video, with a driven browser only.** Open the video's own address (`video_hd`, else `video`) in a tab, run this in the page and take one screenshot. It draws the frames side by side over the page, as large as the viewport allows, so a video costs two screenshots: once with `show` as `"hook"` and once as `"overview"`. For small print, give `show` a second and `part` a third of the frame, and take another. Frames are not kept on this route; say so in the report. Where no script can run, pause the player and take a screenshot at 0, 1, 2 and 3 seconds and at a few later moments.

```js
(async () => {
  const show = "hook";  // "hook": the first three seconds; "overview": twelve frames across the video; a number: the frame at that second
  const part = null;    // with a number: null for the whole frame, or "top", "middle", "bottom" to enlarge that third
  const v = document.querySelector("video");
  if (!v) return { ok: false };
  v.pause(); v.muted = true;
  document.querySelectorAll("canvas").forEach((x) => x.remove());
  const times = show === "hook" ? [0, 0.5, 1, 1.5, 2, 2.5] : show === "overview" ? Array.from({ length: 12 }, (_, i) => (v.duration * i) / 12) : [show];
  const band = ["top", "middle", "bottom"].indexOf(part), sh = band < 0 ? v.videoHeight : v.videoHeight / 3, sy = band < 0 ? 0 : band * sh;
  const W = innerWidth * devicePixelRatio, H = innerHeight * devicePixelRatio, n = times.length;
  let cols = 1, w = 0;  // the grid that shows the frames largest in this viewport
  for (let c = 1; c <= n; c++) { const fit = Math.min(W / c, (H / Math.ceil(n / c)) * (v.videoWidth / sh)); if (fit > w) { w = fit; cols = c; } }
  const h = (w * sh) / v.videoWidth;
  const c = document.createElement("canvas");
  c.width = W; c.height = H;
  c.style.cssText = "position:fixed;left:0;top:0;width:100vw;height:100vh;z-index:99999;background:#000";
  document.body.appendChild(c);
  const g = c.getContext("2d");
  for (let i = 0; i < n; i++) {
    await new Promise((r) => { v.addEventListener("seeked", r, { once: true }); v.currentTime = Math.min(times[i], v.duration - 0.1); setTimeout(r, 15000); });
    await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
    g.drawImage(v, 0, sy, v.videoWidth, sh, (i % cols) * w, Math.floor(i / cols) * h, w, h);
  }
  return { ok: true, seconds: Math.round(v.duration), frames: n, at: times.map((t) => +t.toFixed(1)), grid: [cols, Math.ceil(n / cols)] };
})()
```

**Video, with neither.** The poster and the copy only. Mark the breakdown "poster only".

**What to read from the frames.** The first frame: what stops the scroll (a face, the product, a line of text, a motion, something odd). Every word on screen in the first three seconds, verbatim. Who is on screen and as what: a creator, a customer, an expert, a founder, nobody. Then the beats with their seconds: where the problem, the product, the proof, the offer and the call to action appear. The caption style (burned-in subtitles, stickers, a look copied from native posts), the length, the aspect.

**Still image.** Look at it (the `image` address, or the card in the browser): the headline inside the image, the layout (product hero, before and after, review screenshot, comparison, meme, a note that looks native), how much text.

**Several versions** (`DCO`, `CAROUSEL`). Read the record's `cards`: what varies between versions (the headline, the image, the offer) is what the advertiser is testing; versions that differ only in shape are placements, not tests.

| Breakdown field | Content |
|---|---|
| Hook | The first frame and the first line, verbatim, and its type from the list below. |
| Angle | The reason to buy it leans on. |
| Format and length | From the list below; seconds; aspect. |
| Structure | The beats in order with their seconds. |
| Proof used | Reviews, numbers, authority, demonstration, guarantee. |
| Offer and call to action | Price, discount, bundle, deadline, button, landing page kind. |
| Why it is on the list | Its tier and signals in a line, and any counter-signal. |
| What transfers | The mechanism another product could use, in a sentence. Never its lines, footage, people or brand. |

## Vocabulary

Use one word for one thing across the report, and add a word when none fits.

- **Hook types.** Question. Bold claim. Problem callout. Curiosity gap. Number or social proof. Before and after. Demonstration. Contrarian or myth. Offer first. Story or confession. Native disguise (looks like a post, a review, a message). Authority. Comparison. Trend or meme.
- **Angles.** Pain relief. Aspiration. Proof by others. Price or deal. Novelty. Scarcity. Identity ("for people like you"). Ease.
- **Formats.** Creator talking to camera. Testimonial mashup. Hands-only demo. Studio demo. Before and after. Founder story. Street interview. Reaction or green screen. Skit. Screen recording. Listicle. Unboxing. Product hero still. Review screenshot. Comparison chart. Meme. Carousel.
- **Offers.** None stated. Percent or amount off. Bundle or multi-buy. Free shipping or gift. Trial or guarantee. Deadline or limited stock.

## Patterns

Count, do not characterize: "5 of 8", not "most". Across the shortlist, and across the cleaned pool where the text allows: hook types, formats, video lengths, offers, buttons, landing page kinds, words and claims that recur. Then three readings: what the Rising tier does that the Evergreen tier does not (the trend), what many advertisers do alike (crowded), and what nobody in the pool does (open).

## Recommendations

Three directions for the user's subject, written new. Each has: the mechanism and the library ads it is taken from (links); why it fits this subject; one hook line in the market's language, with a bracketed blank wherever a fact about the user's product is needed and not known; the structure in beats with seconds; format, length, on-screen text style; the call to action; what to avoid. One direction follows the proven pattern, one bets on an open angle. Statements about the user's product come only from its page or from the user.

## Report

The run's folder holds `report.md` in the user's language, headings included, `ads.json` shaped like [research-data.example.json](../assets/research-data.example.json) (field names and fixed values in English, free text in the user's language), `frames/` when a shell made frames, and `work/`. Where the agent cannot write files, the same report goes into the client's document surface. Frames are working files for the user's own study; the report links ads by Library ID and embeds no one's creative.

```markdown
# Ad creative research: <subject> (<market>, <date>)

## Scope
<Subject, market, terms, date read, route used, page loads, how many ads read and kept. What "proof" means here and what the library does not show.>

## Landscape
<Active ads per term. The share that is new this week. Video share. Advertisers most present, with active ad counts. What is being tested this week (the Fresh group).>

## Shortlist
| # | Advertiser | Format, length | Running | Proof | Hook | Read from | Link |
<"Read from" is what was looked at, not what was made: both sheets, the overview sheet, the poster, the image.>

## Breakdowns
### 1. <advertiser>: <hook in a few words>
<The breakdown fields. "Poster only" or "audio not transcribed" where that is the case.>

## Patterns
<Counts, then: the trend, the crowded, the open.>

## Recommendations
### Direction 1: <name>
<Mechanism and source ads, fit, hook line, structure, format, call to action, avoid.>

## Method and limits
<Tier rules as used. What was not read and why, the hook sheets that were made and not looked at among it. Links expire: the Library ID links last, the media addresses do not.>
```
