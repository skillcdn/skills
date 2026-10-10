# Search and AI readiness, share images, favicon, analytics

What every public page carries so that search engines index it per language and AI engines (answer engines, assistants with web search) read and cite it, how the share image and the favicon set are made from the brand without committing anything by hand, and how analytics is wired without cookies.

## The site URL

`config/site.ts` reads the public build variable `NEXT_PUBLIC_SITE_URL` with `http://localhost:<port>` as the default. Every absolute URL (canonical, hreflang, the share image, the sitemap, `llms.txt`, the sign-in callbacks) comes from it, so that before the launch everything resolves on the local address and after it the deploy skill sets the live address (the free one first, the domain when it comes) as a build variable and rebuilds. Nothing in the pages types a host by hand.

## Metadata on every public page

- Title (a template `%s | <site name>`), description, canonical URL for the page's locale, hreflang alternates with `x-default`, Open Graph (`type`, `locale`, `siteName`, `title`, `description`, `images` at 1200 by 630 with `alt`), Twitter card `summary_large_image`, icons (`favicon.ico`, `favicon.svg`, `icon-192.png`, `apple-touch-icon.png`), the manifest, `theme-color`, viewport with `viewportFit: cover`.
- From the framework's metadata API, built by one helper in `lib/seo.ts` that takes the locale and the path, so that no page writes a URL by hand.
- Private or transactional pages (an account page, a result only its owner sees, a checkout return, the admin) are `noindex` in the page and disallowed in `robots`.

## Sitemap and robots

- `sitemap.xml` from the framework's route: every public path for every locale, each with its alternates; `lastModified` from the content's real date; a public detail page listed when it should be found.
- `robots.txt`: allow the public paths, disallow the private ones, name the sitemap. AI crawlers (search bots of answer engines and the training crawlers) are allowed by default, because being read is the point of a public site; the user may opt out of training crawlers, and the decision is written in `docs/decisions.md`. Cloudflare's own bot settings must agree with the file: a crawler blocked at the edge never sees the allow.

## Structured data

JSON-LD in the page head, only for what is true: `WebSite` and `Organization` (name, URL, logo, the owner from the brief, the same names as the pages) on every page; `SoftwareApplication` or `Product` on the page that describes the offer, with real prices when there are any; `FAQPage` where a page answers questions; `Article` with dates and author on posts; `BreadcrumbList` on nested pages. No ratings, reviews or counts that are not real; search engines penalize invented ones and the user is embarrassed. An owner given "later" leaves the `Organization` out until it is known.

## For AI engines

- Server-rendered HTML with the content in the first response: the key text of a page is never only produced in the browser.
- Entity clarity: one sentence on the home page and the about page that says what the product is, who makes it, where and since when, with the same name everywhere (the title, the organization data, the manifest, the share image).
- Direct answers: a FAQ section with the questions people ask, each answered in the first sentence; pricing stated plainly; a changelog or a dated "what's new" when the product moves.
- `llms.txt` at the root: a Markdown page that says what the site is, lists its main pages with one line each, its pricing and contact, in the default locale (and `llms-full.txt` with the key pages' content when the site is large); served by a route that reads `config/site.ts`, so that it cannot drift from the site.
- Fast and stable: text first, images with dimensions, no layout shift; a Worker answers quickly, and the cache headers on static pages let the edge serve them.

## The share image and the favicon set

Source: the brand symbol as SVG in `public/brand/` with the wordmark, from the look. The script `scripts/brand/render.mjs` renders every raster the metadata names, so that a change of color or name is one command (`npm run brand`), and nothing is drawn by hand:

| Output | Size | From |
|---|---|---|
| `favicon.svg` | any | the symbol on its tile |
| `favicon.ico` | 16, 32, 48 | the PNG tiles, packed by a small ICO writer (a dev dependency such as `png-to-ico`, or a handful of lines) |
| `icon-192.png`, `icon-512.png`, `apple-touch-icon.png` (180) | square | the tile, with safe margins for the maskable variant |
| `og-image.png` and `og-image-<locale>.png` | 1200 by 630 | the symbol, the site's name and tagline in that locale, on the brand background |

Rendering: an SVG-to-PNG renderer that embeds fonts (`@resvg/resvg-js` as a dev dependency; it reads TTF and OTF files passed by path). The font files come from the family's own download (the download button of Google Fonts gives TTF; the Noto CJK subsets are release archives on the `notofonts` GitHub organization), saved in `.brand-tmp/fonts/` (gitignored) or a folder outside the repository that the script takes as an argument; the share image's text is set in each locale's font. The outputs are committed, because a scaffold without them is a page with no icon; the fonts are not. When the fonts cannot be fetched in the run's environment, render with the system fonts for the Latin outputs, leave the CJK share images as the symbol alone, and list them in `docs/status.md`. A per-page share image generated at request time (the framework's image response) comes later, when the adapter supports it (platform.md names where to check).

## Analytics

Cloudflare Web Analytics, created by the deploy skill (automation.md). For a domain on Cloudflare it is injected at the edge and the code needs nothing. For a `workers.dev` address the root layout renders the beacon script (`https://static.cloudflareinsights.com/beacon.min.js` with `data-cf-beacon='{"token": "<token>"}'`) only when the public build variable `NEXT_PUBLIC_CF_BEACON_TOKEN` is set; the layout carries that slot from the first commit and the deploy skill fills the variable. It sets no cookies, so no consent banner is needed for it. In the code, one `track(event, data)` in `lib/analytics.ts` that does nothing until a destination exists: ad pixels and product analytics fan out from there later, never from the pages. Honor the Global Privacy Control header and signal: when set, load no pixel at all.

## The check before delivery

Against the local address, for every locale: the home page's HTML contains the canonical and the hreflang links, the Open Graph image URL answers 200, the favicon files exist in `public/`, `/sitemap.xml` and `/robots.txt` answer, `/llms.txt` names the site, and the JSON-LD parses. One script in `tests/` or a shell loop; its output is in the delivery, and the deploy skill runs the same loop against the live address.
