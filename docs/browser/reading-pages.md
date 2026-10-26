# Reading a page in full

How an article, a help page or a site page is read for its text and its images: with which tool, what counts as read, where the reading stops, how an image is taken from the page, and how a file is downloaded. What one site shows and where stays with the skill or the family that reads it; this page holds what holds for any page.

## Which tool reads a page

| Tool | Reads | Does not |
|---|---|---|
| A fetch tool that converts a page to text | An article's text and, usually, its figure images with their captions | The share image in the page's metadata, on one tool (checked 2026-10); a page that renders by script (a help site returned nothing); a page behind a browser check; some outlets' pages, which answer a plain fetch with an error page while a browser reads the article as any visitor's does (checked 2026-10) |
| A browser the agent drives ([driven-browser.md](driven-browser.md)) | Everything a person sees, the image elements by a script in the page, pages that render by script, pages that answer only a browser engine | A page behind a wall (below) |
| A shell with `curl` | A page's HTML as the host serves it to a plain request; a media file the host serves to a plain request | A page that answers only a browser engine (an HTTP 403 with a check script): the check is not replayed, and the request is not dressed up as a browser's |

A search tool's own summary of a page is a lead and never a source: a figure read from a summary and not from the page has been wrong. Where one tool returns nothing or an error page, the next in the table is tried, because a fetch tool cannot render what a browser can; a page that needs a sign-in, a subscription, a consent or a check that does not pass by itself is read by none of them ("Walls" below), a browser is never dressed up as something else, and a page none can read is not a source, which the delivery says.

## Read to the end

A page counts as read in full when its end was reached: the last paragraph, the comments, the footer. A reader that returns a cut page (a length limit, a "read more" fold, a tab the content sits under) has not read it: read on with the browser, by scrolling or by opening the fold, and say where a page could not be finished. The visible text of a long caption or a list may be cut by the page itself; the data embedded in the page holds it whole (driven-browser.md "Data embedded in a page").

## Walls

A page that needs a login, a paid subscription, a consent the content cannot be read without, or a browser check that does not pass on its own is not read: no sign-in, no account, no form filled, no replay of a check, no disguised browser. A prompt that only covers the page is closed by its own control and the page read; a prompt that gates the content ends the reading, and another source is read. A page that shows nothing but a request to log in after pages that read fine is the site asking for a pause: stop, say so, and do not go on without the user.

## Pages that render by script

A help site, a settings page, a profile: the text arrives by script after the load. A fetch tool returns nothing, a shell gets the empty shell of the page; the driven browser reads it, and a headless browser's dump of the DOM ([headless.md](headless.md) "The bare browser with --dump-dom") carries what the scripts built. Where neither is at hand, the delivery says that the fact (a documented size, a limit) could not be read on the day and where it was read instead.

## The images on a page

- An article's photographs are its figure elements: an `img` inside a `figure`, with the caption and the credit in the text beside it. A page reader that returns the text usually returns the image addresses and the captions; where it returns no images, a driven browser runs this in the page:

```js
[...document.querySelectorAll("img")]
  .filter((i) => (i.naturalWidth || 0) > 300)
  .map((i) => ({ src: i.currentSrc || i.src, w: i.naturalWidth, h: i.naturalHeight, caption: (i.closest("figure")?.innerText || i.alt || "").slice(0, 200) }))
```

- The share image (`og:image` in the page's metadata) is a fallback where the page has one photograph; a fetch tool may not return it (checked 2026-10).
- Logos, icons, advertisements and tracking pixels are not images of the page; the width filter above drops most of them.
- The same photograph appears on several pages: the largest copy is the one to take, and the credit is the agency's or the photographer's, with the page noted as where it appeared.

## Downloading a file

- One request at a time, as with pages. Where a browser read the page, download the image through it: the driven browser's save, or a headless browser that opens the image's address and saves the response body, as the browser's own request; from a shell with no browser, a plain request, and a host that answers it with an error is not downloaded from (checked 2026-10). A request is never dressed up as a browser's.
- An address that transforms the image on the way carries a segment or a parameter for it (`/cdn-cgi/image/<options>/`, `/resize/<w>x<h>/`, `w_1200`, `format=webp`): the address without it is the original where the host serves one to a plain request, and the larger file is kept; an address the host does not answer is left alone (checked 2026-10).
- Read the pixel size from the file, never from the page or the address: the copies of one story's photographs ranged from a few hundred to over three thousand pixels wide. A few lines that read the JPEG, PNG and WebP headers do it; the card-news research skill carries them as [`image-size.example.mjs`](/marketing/skills/web-cardnews-topic-brief/scripts/image-size.example.mjs).
- A file copied from a page may carry the page's metadata, a location included; a screenshot carries none.
- Some sites sign their media addresses, and the signature expires within days: read the media in the run that found it, and cite the page.

## Site facts are dated

What a site shows without signing in, where a control sits, what a label says and which key its JSON uses change without notice. A statement about one site carries the day it was checked and the way to find the value again (the address bar after a filter is set by hand, one card's text, the keys in the page's JSON), and lives with the family or the skill that reads that site; a statement about a tool's behavior on any page carries the month it was seen and lives here.
