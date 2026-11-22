# The library: logos, icons and screens kept across issues

Where the marks and pictures of the companies and apps an issue shows are taken from, how they are named, and the index the deck relies on. Read before phase 4. The library belongs to the series, not to an issue: `library/` beside the issues' folders, so that the next issue finds what this one gathered.

## Folders

```
library/
  index.md     one row a file
  fonts/       the brand's font files
  logos/       company logos, as SVG where there is one
  icons/       app icons
  screens/     app screens and site captures
```

## Where a file comes from

In this order, stopping at the first that has the file:

1. **The company's own site**: its header and footer, its press or brand page. The logo as SVG where the site serves one (the `img` or the inline `svg` of the header, saved as it is; an inline one that lacks `xmlns="http://www.w3.org/2000/svg"` gains it, since without it the file does not open as an image).
2. **The app's store listing**, for an app's icon and its screens. The iTunes Search API answers without a key: `https://itunes.apple.com/search?term=<name>&entity=software&country=<cc>` gives `artworkUrl512`, `screenshotUrls` and `sellerName` for each match (checked 2026-11); pick the match by its seller, not by its rank.
3. **Simple Icons**, for the mark of a widely known brand whose site serves only a raster logo.

A file is saved as it was served, its size read from the file ([reading-pages.md](/docs/browser/reading-pages.md) "Downloading a file"). A screen or a photograph is taken as JPEG where the source offers one: a Chromium-family browser stores a WebP decoded in the PDF, which grows it.

## Names

`<brand>-<kind>[-<variant>].<ext>`, in lower case with hyphens: `acme-logo.svg`, `acme-icon.png`, `acme-screen-1.jpg`, `acme-logo-white.svg`.

- The kind is `logo`, `symbol`, `icon` or `screen`.
- A name is given once and not changed: the deck's paths are written from `index.md`, and a renamed file is a slide with a hole. Whoever fetches the files, a worker agent included, is told the names before it starts.

## A white variant

A logo drawn dark is unreadable on the issue's ground. Make the variant, keep the original: copy the SVG to `<brand>-logo-white.svg` and set its fills to white, leaving a part that carries the brand's own colour (a coloured symbol beside dark lettering) as it is. A raster logo with no light version is shown on a small light chip instead of being redrawn. Nothing else of a mark is changed: not its proportions, not its spacing, not its parts.

## The index

`library/index.md`, shaped as [`index.example.md`](../assets/index.example.md): one row a file with the brand, the kind, the pixel size or `vector`, the ground it is made for, the address it came from and the day it was fetched. The deck uses a file only through its row; a file the next issue no longer shows stays, for the issue after it.
