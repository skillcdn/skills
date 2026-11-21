# Images: where they come from, clips, frames, downloading, measuring, crediting

How the post's image set is made: where images and video are looked for and in what order, how each is found, downloaded and measured, which show on a slide and which do not, how a role is assigned, and how the credit line is written. The set's job is to show the story: the person, the place, the scene or the thing each beat names, legibly at phone size, with a credit the caption can print. A picture that shows none of that is not an image of the story.

## What the set must hold

One image per beat, and one spare per beat where photographs will be cropped: at least one legible image that works as a portrait cover (vertical, or horizontal with its subject central enough to crop; a clear frame where the spec's cover is itself a frame kept whole), the subject shots the facts need, and a mood shot. The spec's slide types say how the account treats its images. An account that keeps frames whole needs as many clear frames per beat as its type's `frames_per_slide`, each with a caption that states a fact of the table; a type that carries a page capture (a source card) needs the capture of each article a slide may cite. With no spec, photographs are taken as cropped full-bleed and frames one per beat, said at the brief checkpoint.

## Where images come from

Start from what each beat has to show, read from the facts: the subject, the scene of the event, the thing a fact names, the document or the post the story is about. Then look in this order, and stop when every beat has what the set must hold:

| Order | Source | Credit | When |
|---|---|---|---|
| 1 | A video of the story: the subject's own upload, footage of the event, a product's demonstration, as a short clip with its first frame as the poster | Whoever posted the original, with the seconds taken | First, unless the request or the policy says photos only; "A clip of the story's video" below |
| 2 | The articles' own photographs: their figure images with the printed captions | The agency or the photographer, and the outlet where it appeared | Always |
| 3 | The material the articles cite, where it is public: a broadcaster's clip of the report, the footage the story is about, the post or the video it quotes, a release's press images | The broadcaster, the footage's owner or the account, as the material itself credits them; the clip or the post as `url` | When 1 and 2 do not show what a beat names, or the account's format keeps such frames whole |
| 4 | The subject's own public pages the articles link or name: an official site, a press kit, a public account | The site or the account | When 1 to 3 give no image of the subject |
| 5 | A capture of a page the story is about or the articles cite (an advisory, a notice, a release, a post), or of the subject's own public page, taken by the run's browser at a width that reads at phone size and kept whole | The page's owner, with the address and the day | When 1 to 4 give no picture of what a beat names, as for a story about software or a document, or the spec has a type that carries a capture |
| 6 | An image search | The page the image was found on | Last, for a beat 1 to 5 left unshown; said at the brief checkpoint with what was looked for first |

A source the host cannot reach is skipped, not worked around: a site that fails from its first page while other sites load ([walls.md](/docs/browser/walls.md) "The host's wall") is named in the brief's `notes` as not reached, the next source in order is read, and the checkpoint and the delivery say so. A stock library or a generated image is used only when the user asks for it, and the credit says so. Which source each image came from goes in `source_kind` of its entry (`video-clip`, `article-figure`, `share-image`, `video-frame`, `subject-page`, `page-capture`, `image-search`, `user`).

## A clip of the story's video

Look for the story's own video before its photographs: what the subject posted, what was filmed of the event, the product shown working. The articles and the boards where the story is talked about name it; a re-upload, another outlet's edit with its captions and logo, or a video that is only about the same subject is not it. How a video is fetched, which range is worth cutting and how it is cut, with what that takes, is the pack's [video-clips.md](/docs/browser/video-clips.md), read before the first video is opened; nothing of it is repeated here. This skill adds one test: the range shows what a beat names, and shows it better than the photographs do. Each clip gives two entries: the clip itself (`source_kind` `video-clip`, the file `img/<name>.mp4`, the source's `url`, `from` and `to` in seconds of the source, `seconds`, `px`, `shows`, `credit`), and its first frame as a `video-frame` entry with `poster_of` naming the clip's file. `credits.md` says whose video it is and which seconds.

No video of the story, no way on this host to cut one, a video behind a login, or a clip that shows the thing worse than a photograph: the set is photographs alone. That is a normal result, said in one line at the checkpoint with what was looked for; a clip is never added to have one.

## Finding the images in an article

An article's photographs are its figure elements: an `img` inside a `figure`, with the caption and the credit in the text next to it (a byline of the agency, a photographer, a "provided by"). A page reader that returns the article's text usually returns the image URLs and the captions with it; where it returns no images, a driven browser reads the `img` elements with the script in [reading-pages.md](/docs/browser/reading-pages.md) "The images on a page".

The share image in the page's metadata (`og:image`) is a fallback when the article has one photo only; its credit is then the outlet, with `source_kind` `share-image`. The article's logo, icons and advertisements are not images. A news photograph often appears in several outlets with the same agency credit; the largest copy is the one to download, and the credit names the agency, with the outlet noted as where it appeared.

## Frames from a clip the articles cite

A report's clip on the broadcaster's public video channel, or the footage the story is about on the channel the articles name, is captured from its public watch page with [video-frames.example.mjs](../scripts/video-frames.example.mjs) (a shell with Node.js and a Chromium-family browser; `playwright-core` is borrowed from a neighbouring project's install through `PLAYWRIGHT_FROM`, else installed once into the tools folder `card-news/tools/` beside the brief folders and never into a brief folder, which is handed over, the install said in a line and a browser download asked first, as [headless.md](/docs/browser/headless.md) says); how the watch page behaves, and the other routes to a clip's frames, are in [video-frames.md](/docs/browser/video-frames.md). The script is written against the watch page of the largest video platform, where broadcasters publish their reports: a clip the articles link on the broadcaster's own player is looked for on the broadcaster's channel there first. Where the script cannot run and the driven browser can save a screenshot to a file, the clip is stepped by hand (play, pause, save, note the time); where the browser only shows screenshots to the agent, the clip is listed as a source by its address and the delivery says the frames were not taken. The script saves a frame every few seconds of video, named by its time code in tenths of a second (`t00120.jpg` is 12.0 seconds, so `&t=12s` in the entry's `url`), with `frames.tsv` beside them (seconds, served width by height, file), appended on every run, so a rerun gets an empty folder. A clip of several minutes runs for minutes; run it in the background.

Capture the whole clip once into a capture folder of its own in the brief folder (`frames/<clip>/`, never `img/`), then choose: the frames whose own captions or graphics state a fact of the table (a subtitle, a name card, a graphic), the ones that show the subject clearly, and one frame per scene the beats name, or as many per beat as the spec's type stacks on one slide. A kept frame is copied into `img/` as `<clip>_<its time code name>.jpg`; the rest stay in the capture folder, with one line in `credits.md` for the clip. Each kept frame's `caption` is the text printed on it, as printed; its `url` is the clip's address with the time; its `credit` is the broadcaster and the program as the clip shows them, with the clip's publication date, and where the clip names the footage's origin (a viewer's camera, the subject's own channel, a public body), that origin goes in `notes` and in the delivery. Faces the broadcaster blurred stay blurred.

## Finding by search

For a beat the sources above left unshown, an image search of the subject's name with the event: open the page each result sits on and take the image from that page, never from the thumbnail, credited to that page with the credit it prints. A search is never the first source, because the articles' and the material's images are what the account would show and what a reader recognizes. Where the host's search tool returns text results only, an image search engine's results page opened in the browser at hand, driven or headless, lists the images with the page each sits on (checked 2026-10).

## Downloading and measuring

- One file per image, named for its source and subject (`<outlet>_<subject>.jpg`; a frame as the script names it, by its time code), into `img/` of the brief folder, after the pick and never before.
- Request each as [reading-pages.md](/docs/browser/reading-pages.md) "Downloading a file" says: one at a time, through the browser that read the article where there is one, else by a plain request; the transform segment removed where the host serves the original to a plain request; a host that answers with an error is not downloaded from.
- Read the pixel size from the file with [image-size.example.mjs](../scripts/image-size.example.mjs) (JPEG, PNG and WebP) or a few lines like it. The size goes in the entry, not an estimate. A frame's `px` is the resolution the clip was served at, read from the capture table, not the capture file's size, which is always the box's.
- Note where a logo, a watermark or a credit mark sits (a corner, the lower edge), because the build crops around it where the account crops and keeps it where the account keeps it.
- Downloads not kept go to `img-unused/` with one line each in `credits.md` on why (a duplicate, smaller, a large mark, unreadable), so that the user or the build can swap one in.

## Choosing

The canvas is the spec's documented size when a spec exists, else the platform's documented portrait size (about 1080 by 1350 pixels for 4:5 at the time of writing, illustrative; looked up at run time). An image rendered full-bleed at that size is judged by its own size; a frame the account keeps whole at the canvas width is judged against that width:

| Image | At the canvas |
|---|---|
| Vertical, as wide as the canvas or more | Clean as a cover or a full slide |
| Horizontal, as tall as the canvas or more | Clean, cropped to portrait; a subject at the edge is lost, and the entry says so |
| Horizontal, as wide as the canvas or more | Clean as a frame kept whole at the canvas width; as a full slide, cropped with the loss said |
| Smaller, down to 700 pixels on its short side | Upscaled up to two times; acceptable on a phone, soft on a tablet; the entry says the factor (the larger of canvas width over image width and canvas height over image height) |
| Under 700 pixels on its short side | Usable only darkened under type, in a collage half, or not at all; the entry says so |

Where no image of a beat reaches the canvas, look for the same photograph's larger copy in other outlets' articles, which its agency credit names, before accepting an upscale above two: a set of small copies alone was upscaled two to four times, and the slides read soft.

### Legibility and what an image is

Every image is judged as a phone reader will see it, at about a third of the canvas width (the file shown in the driven browser or the host's browser pane at that width; or, with `playwright-core` at hand, a headless page that shows the file at that width, screenshotted, as the pack's [rendering-html.md](/docs/browser/rendering-html.md) "Looking at a render" says, since Node.js has no image resize of its own): the subject must be made out and any text on it read. `legibility` in the entry is `clear`, `soft` (usable, with the factor or the reason in `notes`) or `unreadable`. Slides delivered on unreadable frames were sent back with "this cannot be seen"; the judgement is made here, image by image, so that the build never has to make it.

`shows` says in the post's language what the image shows (the person by name as the articles give it, the scene, the thing), so that the build matches each slide's text to an image that shows what it names; a frame's `shows` includes what its caption states.

| Image | Verdict |
|---|---|
| Shows nothing the facts name (a stock scene, a logo alone, an unrelated file photo) | Not in the set; the next source in order is read |
| Its subject cannot be made out at phone size (blur or mosaic alone, a dark scene, motion blur, a small picture that would upscale past about two times) | `unreadable`: set aside, or kept only as a background under type, said so; a slide that has to be read takes only a clear one |
| A re-enactment, an illustration or a generated image inside the material | Not a photograph of the event: `role` `illustration` with `notes` saying what it is, or not kept |
| A frame whose printed caption states something no article body carries | Kept for what it shows, with `notes` saying its caption is uncarried; the statement goes to `unverified` with the clip as where it was seen |
| Found by image search | Kept only for what the earlier sources left unshown, and said at the checkpoint |
| Smaller than the canvas | Kept with its size and the upscale factor noted, as the table above says |

## Roles

`cover` for the image that reads at portrait with the subject central; `subject` for what the facts are about; `scene` for the event's place or moment; `mood` for a scene without a subject, which takes a note or a dim overlay; `detail` for a close view that illustrates one beat; `illustration` for a re-enactment, a drawing or a generated image inside the material, never shown as a photograph of the event.

## The entry

```json
{
  "file": "img/example-clip_t00120.jpg",
  "source_kind": "video-frame",
  "shows": "<what the image shows, in the post's language; a frame's caption's statement>",
  "caption": "<the caption as printed, or the text printed on the frame>",
  "credit": { "agency": "<broadcaster and program, or agency>", "photographer": "", "outlet": "<where it appeared, or the channel>", "date": "0000-00-00" },
  "url": "https://example-video.example/watch?v=<id>&t=12s",
  "px": { "w": 1920, "h": 1080 },
  "legibility": "clear",
  "watermark": "broadcaster's logo, top right; the program's label, top left",
  "role": "subject",
  "notes": "<the footage's origin as the clip credits it, or what the build must know about this image>"
}
```

A clip's two entries are in [topic-brief.example.json](../assets/topic-brief.example.json).

## credits.md and the credit line

`credits.md` beside the brief has two parts. First, one line per kept image or clip, in the order of the entries: the file name, a separator (` | `), then the credit as the entry gives it (the agency or the broadcaster and program, the photographer where named, the outlet or channel, the date; for a clip, whose video and which seconds), written in the spec's `caption.credit_line_pattern` where a spec exists. Then, under a heading of its own, the set-aside list: one line per file in `img-unused/` with the reason, and one per capture folder. The caption's credit line is the build's to write from the first part, for the images it placed: in the spec's pattern, or, with no spec, the word for "photo" in the post's language, a separator, then the agencies, photographers, broadcasters and accounts in the order of the slides, each once, the outlet where it is the credit.
