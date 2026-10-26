# Images: finding, downloading, measuring, crediting

How the articles' own photographs become the post's image set: where they are on a page, how they are downloaded with their captions and credits, what their pixel size means for the canvas, what to note about marks and licences, how a role is assigned, and how the credit line is written.

## Finding the images

An article's photographs are its figure elements: an `img` inside a `figure`, with the caption and the credit in the text next to it (a byline of the agency, a photographer, a "provided by"). A page reader that returns the article's text usually returns the image URLs and the captions with it; where it returns no images, a driven browser reads them with a script run in the page, in the shape of:

```js
[...document.querySelectorAll("img")]
  .filter((i) => (i.naturalWidth || 0) > 300)
  .map((i) => ({ src: i.currentSrc || i.src, w: i.naturalWidth, h: i.naturalHeight, caption: (i.closest("figure")?.innerText || i.alt || "").slice(0, 200) }))
```

The share image in the page's metadata (`og:image`) is a fallback when the article has one photo only; its credit is then the outlet, marked `share_image` in `notes`. The article's logo, icons and advertisements are not images.

A news photograph often appears in several outlets with the same agency credit; the largest copy is the one to download, and the credit names the agency, not the outlet, with the outlet noted as where it appeared.

## Downloading

- One file per image, named for its source and subject (`<outlet>_<subject>.jpg`), into `img/` of the brief folder, after the pick and never before.
- Send a browser user agent and the article's URL as referer; some image hosts refuse a bare request.
- A CDN path that transforms the image carries a segment for it (`/cdn-cgi/image/<options>/`, `/resize/<w>x<h>/`, a `w_1200` or `format=webp` parameter): remove the segment or the parameter to reach the original where the host allows it, and keep the larger file.
- Read the pixel size from the file with [image-size.example.mjs](../scripts/image-size.example.mjs) (JPEG, PNG and WebP) or a few lines like it. The size goes in the entry, not an estimate.

## Choosing

The canvas is the spec's documented size when a spec exists, else the platform's documented portrait size (about 1080 by 1350 pixels for 4:5 at the time of writing, illustrative; looked up at run time). An image is rendered full-bleed at that size, so its own size decides whether it renders clean:

| Image | At the canvas |
|---|---|
| Vertical, as wide as the canvas or more | Clean as a cover or a full slide |
| Horizontal, as tall as the canvas or more | Clean, cropped to portrait; a subject at the edge is lost, and the entry says so |
| Smaller, down to 700 pixels on its short side | Upscaled up to two times; acceptable on a phone, soft on a tablet; the entry says the factor (the larger of canvas width over image width and canvas height over image height) |
| Under 700 pixels on its short side | Usable only darkened under type, in a collage half, or not at all; the entry says so |

Keep at least one image that works as a cover, the subject shots the facts need, and a mood shot. Note where a logo, a watermark or a credit mark sits (a corner, the lower edge), because the build crops around it where the licence allows.

## Licence terms

Most news photographs carry no terms of their own. An outlet's footer often states site-wide terms (no unauthorized reproduction or redistribution, no use for AI training, non-commercial use with credit): record that line verbatim in `licence.terms` with `modification_allowed` "unknown", since such a line forbids reuse in general and modification in particular only where it says so. Where nothing is stated, `licence.terms` is "none stated". A rights line burned into the photo (an organizer's press image carrying the rights holders of a character or a work) is a mark: note it in `watermark` and prefer another image of the role. A photo whose subject is someone else's work (a character, an artwork, a product design) carries that work's rights as well, and the delivery names it. The delivery says that the images are the outlets' and agencies' material, used with credit at the user's discretion. A public institution's photograph often states a public licence with a type that allows or forbids modification and commercial use; record the type as the page states it, and set `modification_allowed` false where modification is forbidden: that image is then used whole, not cropped, dimmed or overlaid, or not at all.

## Roles

`cover` for the image that reads at portrait with the subject central; `subject` for what the facts are about; `mood` for a scene without a subject, which takes a note or a dim overlay; `detail` for a close view that illustrates one beat.

## The entry

```json
{
  "file": "img/example-outlet_subject.jpg",
  "caption": "<the caption as printed>",
  "credit": { "agency": "<agency>", "photographer": "<name or empty>", "outlet": "<where it appeared>", "date": "0000-00-00" },
  "url": "https://example-outlet.example/path/to/image.jpg",
  "px": { "w": 1200, "h": 800 },
  "watermark": "outlet logo, bottom right",
  "licence": { "terms": "none stated", "modification_allowed": "unknown" },
  "role": "subject",
  "notes": "horizontal; the subject sits left of center, a portrait crop keeps it"
}
```

## The credit line

`credits.md` beside the brief lists one line per image in the credit-line pattern the format spec gives (`caption.credit_line_pattern`), so that the build pastes it. With no spec, the line is the word for "photo" in the post's language, a separator, then the agencies and photographers in the order of the images, each once, the outlet where it is the credit; the build replaces it with the spec's pattern when a spec arrives later.
