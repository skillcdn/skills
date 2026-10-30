# Images: where they come from, finding, frames, downloading, measuring, crediting

How the post's image set is made: where images are looked for and in what order, how each is found, downloaded and measured, which show on a slide and which do not, what to note about marks and licences, how a role is assigned, and how the credit line is written. The set's job is to show the story: the person, the place, the scene or the thing each beat names, legibly at phone size, with a credit the user can print. A photograph that is well credited and shows none of that is not an image of the story.

## Where images come from

Start from what each beat has to show, read from the facts: the subject, the scene of the event, the thing a fact names, the document or the post the story is about. Then look in this order, and stop when every item has an image that shows it:

| Order | Source | Credit | When |
|---|---|---|---|
| 1 | The articles' own photographs: their figure images with the printed captions | The agency or the photographer, and the outlet where it appeared | Always first |
| 2 | The material the articles cite as their source or their subject, where it is public: a broadcaster's clip of the report, the footage the story is about, the post or the video it quotes, a release's press images | The broadcaster, the footage's owner or the account, as the material itself credits them; the clip or the post as `url` | When the articles' photographs do not show what a beat names, or the account's format keeps such frames whole |
| 3 | The subject's own public pages the articles link or name: an official site, a press kit, a public account | The site or the account | When 1 and 2 give no image of the subject |
| 4 | A capture of a page the story is about or the articles cite (an advisory, a notice, a release, a post), or of the subject's own public page, taken by the run's browser at a width that reads at phone size and kept whole with the page's marks | The page's owner, with the address and the day | When 1 to 3 give no photograph of what a beat names, as for a story about software or a document; `source_kind` `page-capture` |
| 5 | An image search | The page the image was found on, with the credit that page prints | Last, for a beat 1 to 4 left unshown; said at the brief checkpoint with what was looked for first |

A source the host cannot reach is skipped, not worked around: a site that fails from its first page while other sites load (a social network's pages from a chat assistant's sandbox, 2026-10; [reading-pages.md](/docs/browser/reading-pages.md) "Walls") is named in the brief's `notes` as not reached, the next source in order is read, and the checkpoint and the delivery say so; a page capture of it is not possible either. A stock library or a generated image is used only when the user asks for it, and the credit says so. Which source each image came from goes in `source_kind` of its entry (`article-figure`, `share-image`, `video-frame`, `subject-page`, `page-capture`, `image-search`, `user`). A run whose articles carried only file photos found the story's images in the broadcaster's clip every article cited, and the account's format itself stacked such frames; the order above is written from that.

## Finding the images in an article

An article's photographs are its figure elements: an `img` inside a `figure`, with the caption and the credit in the text next to it (a byline of the agency, a photographer, a "provided by"). A page reader that returns the article's text usually returns the image URLs and the captions with it; where it returns no images, a driven browser reads the `img` elements with the script in [reading-pages.md](/docs/browser/reading-pages.md) "The images on a page".

The share image in the page's metadata (`og:image`) is a fallback when the article has one photo only; its credit is then the outlet, with `source_kind` `share-image`. The article's logo, icons and advertisements are not images. An article that illustrates the story with an image it generated or a re-enactment says so in the caption or shows it in the picture; such an image is not a photograph of the event (below, "Legibility and what an image is").

A news photograph often appears in several outlets with the same agency credit; the largest copy is the one to download, and the credit names the agency, not the outlet, with the outlet noted as where it appeared.

## Frames from a clip the articles cite

A report's clip on the broadcaster's public video channel, or the footage the story is about on the channel the articles name, is captured from its public watch page with [video-frames.example.mjs](../scripts/video-frames.example.mjs) (a shell with Node.js and a Chromium-family browser, [headless.md](/docs/browser/headless.md)); how the watch page behaves, and the other routes to a clip's frames, are in [video-frames.md](/docs/browser/video-frames.md). The script is written against the watch page of the largest video platform, where broadcasters publish their reports: a clip the articles link on the broadcaster's own player is looked for on the broadcaster's channel there first. Where the script cannot run and the driven browser can save a screenshot to a file, the clip is stepped by hand (play, pause, save, note the time); where the browser only shows screenshots to the agent, the clip is listed as a source by its address and the delivery says the frames were not taken. The script plays the page at normal speed, with one reload on a stall, and saves a frame every few seconds of video, named by its time code in tenths of a second (`t00120.jpg` is 12.0 seconds, so `&t=12s` in the entry's `url`), with `frames.tsv` beside them (seconds, served width by height, file), appended on every run, so a rerun gets an empty folder. A clip of several minutes runs for minutes; run it in the background.

Capture the whole clip once into a capture folder of its own in the brief folder (`frames/<clip>/`, never `img/`), then choose from the frames: the ones whose own captions or graphics state a fact of the table (a subtitle, a name card, a graphic), the ones that show the subject clearly, and one frame per scene the beats name, or as many per beat as the spec's type stacks on one slide. A kept frame is copied into `img/` as `<clip>_<its time code name>.jpg`; the rest stay in the capture folder, set aside with one line in `credits.md` for the clip. Each kept frame's `caption` is the text printed on it, as printed; its `url` is the clip's address with the time; its `credit` is the broadcaster and the program as the clip shows them, with the clip's publication date as `date`, and where the clip names the footage's origin (a viewer's camera, the subject's own channel, a public body), that origin goes in `notes` and in the delivery. A frame whose caption states something no article body carries is kept for what it shows, never for what it says: `notes` says so and the statement goes to `unverified`. A frame of a re-enactment, an illustration or a generated image inside the material is not a photograph of the event: `role` "illustration" with `notes` saying what it is, or not kept. Faces the broadcaster blurred stay blurred, and a frame that is blur or mosaic alone shows nothing (below, "Legibility and what an image is").

## Finding by search

For a beat 1 to 3 left unshown, an image search of the subject's name with the event: open the page each result sits on and take the image only from a page that prints a credit or is itself the rights holder (the subject's own account, an official site); the credit is that page's. Say at the checkpoint which beats needed a search and what was looked for first. A search is never the first source, because the articles' and the material's images are what the account would show and what a reader recognizes. Where the host's search tool returns text results only, an image search engine's results page opened in the browser at hand, driven or headless, lists the images with the page each sits on (checked 2026-10); the image is still taken from its page, never from the thumbnail.

## Downloading

- One file per image, named for its source and subject (`<outlet>_<subject>.jpg`; a frame as the script names it, by its time code), into `img/` of the brief folder, after the pick and never before.
- Request each as [reading-pages.md](/docs/browser/reading-pages.md) "Downloading a file" says: one at a time, through the browser that read the article where there is one, else by a plain request; the transform segment removed where the host serves the original to a plain request; a host that answers with an error is not downloaded from.
- Read the pixel size from the file with [image-size.example.mjs](../scripts/image-size.example.mjs) (JPEG, PNG and WebP) or a few lines like it. The size goes in the entry, not an estimate. A frame's `px` is the resolution the clip was served at, read from the capture table, not the capture file's size, which is always the box's; the 700-pixel rule and the upscale factor are judged on the served size.

## Choosing

The canvas is the spec's documented size when a spec exists, else the platform's documented portrait size (about 1080 by 1350 pixels for 4:5 at the time of writing, illustrative; looked up at run time). An image rendered full-bleed at that size is judged by its own size; a frame the account keeps whole at the canvas width is judged against that width:

| Image | At the canvas |
|---|---|
| Vertical, as wide as the canvas or more | Clean as a cover or a full slide |
| Horizontal, as tall as the canvas or more | Clean, cropped to portrait; a subject at the edge is lost, and the entry says so |
| Horizontal, as wide as the canvas or more | Clean as a frame kept whole at the canvas width; as a full slide, cropped with the loss said |
| Smaller, down to 700 pixels on its short side | Upscaled up to two times; acceptable on a phone, soft on a tablet; the entry says the factor (the larger of canvas width over image width and canvas height over image height) |
| Under 700 pixels on its short side | Usable only darkened under type, in a collage half, or not at all; the entry says so |

Keep at least one legible image that works as a cover, the subject shots the facts need, a mood shot, and, where the account's format keeps frames whole, the frames whose captions state the facts, one per beat. Where no image of a beat reaches the canvas, look for the same photograph's larger copy in other outlets' articles, which its agency credit names, before accepting an upscale above two: a set of small copies alone was upscaled two to four times, and the slides read soft (2026-10). Note where a logo, a watermark or a credit mark sits (a corner, the lower edge), because the build crops around it where the account crops and the licence allows, and keeps it where the account keeps it.

### Legibility and what an image is

Every image is judged as a phone reader will see it, at about a third of the canvas width (the file shown in the driven browser or the host's browser pane at that width; or, with `playwright-core` at hand, a headless page that shows the file at that width, screenshotted, as the repository's [rendering-html.md](/docs/browser/rendering-html.md) "Looking at a render" says, since Node.js has no image resize of its own): the subject must be made out and any text on it read. Not legible: a frame that is mosaic or blur alone, a scene so dark its subject is a shape, motion blur, a small picture inside a frame that would need more than about two times upscale to fill a slide. `legibility` in the entry is `clear`, `soft` (usable, with the factor or the reason in `notes`) or `unreadable` (kept only as a background under type, said so, or set aside to `img-unused/`). A slide the build has to read from the image, such as a frame whose caption is the beat, takes only a clear one. Slides delivered on unreadable frames were sent back with "this cannot be seen"; the judgement is made here, image by image, so that the build never has to make it.

`shows` says in the post's language what the image shows (the person by name as the articles give it, the scene, the thing), so that the build matches each slide's text to an image that shows what it names; a frame's `shows` includes what its caption states.

## Licence terms

Most news photographs carry no terms of their own. An outlet's footer often states site-wide terms (no unauthorized reproduction or redistribution, no use for AI training, non-commercial use with credit): record that line verbatim in `licence.terms` with `modification_allowed` "unknown", since such a line speaks of modification only where it says so, and say at the checkpoint and at the delivery that an image under a line that forbids reproduction without authorization needs the rights holder's permission before the post is published; the user decides, and nothing is published by these skills. Where nothing is stated, `licence.terms` is "none stated". A broadcaster's clip and an account's footage state no terms of their own as a rule; the platform's or the channel's terms, where read, go in `terms` verbatim, and the material is the broadcaster's or the owner's, used with credit as the account itself uses such frames, at the user's discretion. A rights line burned into the photo (an organizer's press image carrying the rights holders of a character or a work) is a mark: note it in `watermark` and prefer another image of the role. A photo whose subject is someone else's work (a character, an artwork, a product design) carries that work's rights as well, and the delivery names it. The delivery says that the images are the outlets', agencies', broadcasters' and subjects' material, used with credit at the user's discretion. A public institution's photograph often states a public licence with a type that allows or forbids modification and commercial use; record the type as the page states it, and set `modification_allowed` false where modification is forbidden: that image is then used whole, not cropped, dimmed or overlaid, or not at all.

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
  "licence": { "terms": "none stated", "modification_allowed": "unknown" },
  "role": "subject",
  "notes": "<the footage's origin as the clip credits it, or what the build must know about this image>"
}
```

## credits.md and the credit line

`credits.md` beside the brief has two parts. First, one line per kept image, in the order of the entries: the file name, a separator (` | `), then the credit as the entry gives it (the agency or the broadcaster and program, the photographer where named, the outlet or channel, the date), written in the spec's `caption.credit_line_pattern` where a spec exists. Then, under a heading of its own, the set-aside list: one line per file in `img-unused/` with the reason, and one per capture folder. The caption's credit line is the build's to write from the first part, for the images it placed: in the spec's pattern, or, with no spec, the word for "photo" in the post's language, a separator, then the agencies, photographers, broadcasters and accounts in the order of the slides, each once, the outlet where it is the credit; a frame's credit names the broadcaster and the program.
