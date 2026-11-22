# Deep read, patterns and the report

The method after the checkpoint, phases 5 to 8: how each shortlisted creative is read, the words the report names things with, the patterns, the directions and the report's shape. Read before phase 5.

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
- The hook sheet is the first three seconds, six frames half a second apart, read left to right and top to bottom, large enough to read the words on screen: 480 pixels wide from the large video; 240 from the small one cannot be read for small print.
- The overview sheet is the whole ad. `N` is the duration divided by 24 and rounded up, at least 1: one frame every N seconds. `ROWS` is the number of frames (the duration divided by N, rounded up) divided by 6 and rounded up; the tile filter needs both dimensions.
- The last command takes one frame at second `T` at full size, for small print the sheets do not show.

Look at the images: a sheet that was made and not looked at was not read, and each breakdown says which sheets it comes from. Where a speech-to-text tool is installed, extract the audio (`-vn -ac 1 -ar 16000`) and transcribe it; where none is, the burned-in captions on the frames carry the script, and the report says the audio was not transcribed. A speech-to-text model mishears product names that the burned-in captions show: for names, the frames are the ground truth.

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

**Still image.** Look at it (the `image` address downloaded into `work/` and opened with the file reader, where there is a shell; the card, in a driven browser): the headline inside the image, the layout (product hero, before and after, review screenshot, comparison, meme, a note that looks native), how much text.

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

The report names each kind with these words.

- **Hook types.** Question. Bold claim. Problem callout. Curiosity gap. Number or social proof. Before and after. Demonstration. Contrarian or myth. Offer first. Story or confession. Native disguise (looks like a post, a review, a message). Authority. Comparison. Trend or meme.
- **Angles.** Pain relief. Aspiration. Proof by others. Price or deal. Novelty. Scarcity. Identity ("for people like you"). Ease.
- **Formats.** Creator talking to camera. Testimonial mashup. Hands-only demo. Studio demo. Before and after. Founder story. Street interview. Reaction or green screen. Skit. Screen recording. Listicle. Unboxing. Product hero still. Review screenshot. Comparison chart. Meme. Carousel.
- **Offers.** None stated. Percent or amount off. Bundle or multi-buy. Free shipping or gift. Trial or guarantee. Deadline or limited stock.

## Patterns

Count across the shortlist, and across the cleaned pool where the text allows: hook types, formats, video lengths, offers, buttons, landing page kinds, words and claims that recur. Then three readings: what the Rising tier does that the Evergreen tier does not (the trend), what many advertisers do alike (crowded), and what nobody in the pool does (open).

## Recommendations

Three directions for the user's subject, written new. Each has: the mechanism and the library ads it is taken from (links); why it fits this subject; one hook line in the market's language, with a bracketed blank wherever a fact about the user's product is needed and not known; the structure in beats with seconds; format, length, on-screen text style; the call to action; what to avoid. One direction follows the proven pattern, one bets on an open angle, and one takes a form the pool lacks (a kind of proof, a format).

## Report

The run's folder holds `report.md` in the user's language, headings included, `ads.json` shaped like [research-data.example.json](../assets/research-data.example.json) (field names and fixed values in English, free text in the user's language, quoted ad text as written; it reshapes the record: `advertiser` is the record's `page`, `landing_domain` the host of its `landing`, `copies` the Library IDs merged into the entry as [creative-analysis.md](creative-analysis.md) "Cleaning the pool" says, the group's own first, `ranks` its `rank` per view), `frames/` when a shell made frames, and `work/`. Where the agent cannot write files, the same report goes into the client's document surface. Frames are working files for the user's own study; the report links ads by Library ID and embeds no one's creative.

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
