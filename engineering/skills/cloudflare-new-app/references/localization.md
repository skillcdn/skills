# Localization: every language from the first commit

How the app speaks every locale the brief names, so that adding one later touches the configuration and the dictionaries and nothing else. Translation is the smallest part: a locale also decides currency, dates, fonts, legal pages, sign-in providers and which features exist.

## The locale list

`config/i18n.ts` is the one place:

- `LOCALES` as a readonly tuple of tags (`ko`, `en`, `zh-TW`, `ja`), the default first; `type Locale`; `DEFAULT_LOCALE`.
- `type Dict<T> = Record<Locale, T>`: every dictionary in the app is typed with it, so that a missing locale fails the typecheck.
- Per locale, in the same file: the `html lang` value, the Open Graph locale (`ko_KR`), the hreflang tag, the time zone (the Worker runs in UTC), the currency and number format, the font family for its script, the URL prefix or parameter.
- `localeFeatures(locale)`: the switches that differ by market (a disclaimer line, a sign-in provider, an analytics pixel allowed or not), kept in `config/features.ts` next to it and read from there and nowhere else; a `locale === 'x'` scattered through pages is the thing to avoid.

## Dictionaries

- A dictionary lives next to the piece it serves (`components/<feature>/copy.ts`) as a typed object `Dict<{...}>`; strings with variables are functions, so that word order can differ by language.
- Written in the language, not translated word by word: honorifics and tone per language (Japanese and Korean politeness levels, Chinese variants), no exclamation marks when the tone forbids them, the product's name spelled as each language spells it.
- The dictionary test (`tests/dictionaries.test.ts`): walks every dictionary and fails on an empty string and on a script that does not belong to the locale (the script of one locale in another's dictionary, Latin-only text in the dictionary of a language with its own script); the typecheck catches a missing key, this catches a wrong one. A string that is a URL, a bracketed placeholder (`[owner]`) or a name from a short allowlist of brands and product names in the test passes the script check, so that a brand name in Latin letters is not a failure in the dictionary of another script.
- AI prompts, when the app uses a model, are a dictionary too: one pack per locale written in that language only, with a test that no other script leaks in.

## Routing and detection

| Scheme | URLs | Choose when |
|---|---|---|
| Path prefix (default) | `/` for the default locale, `/ja/...` for the others | Search engines index each language at its own address; links are readable; the framework's routing handles it |
| Single URL with a parameter and a cookie | `/page`, `/page?hl=ja`, the choice remembered in a cookie | Links must stay identical across languages (ads, sharing, a product whose URL is the brand); every page then sends `Vary` and the parameter variants are the hreflang alternates |

In both: the URL decides which locale a page shows. A cookie remembers an explicit choice (the switcher, a prefix, a parameter) for two uses only: links that come back (payment returns, share links, emails) land in that locale, and the suggestion is silenced. The first visit to the root with no choice shows the default locale, and a one-line suggestion to switch appears when the browser's language is another locale the app speaks; no automatic redirect by browser language, because it hides the other versions from crawlers and annoys travelers.

On Next.js the path-prefix scheme is: every page and the root layout under an `app/[locale]/` segment; the request interceptor (`proxy.ts` on the current major, with a named `proxy` export or a default export, both accepted by vinext when checked 2026-10) rewrites an unprefixed path to the default locale's segment and redirects an explicit default prefix (`/ko/...`) to the bare path with 307, so that each page has one URL per locale; a catch-all route under the segment answers not found for an unknown locale. Route handlers under `app/api/` stay outside the segment.

## Metadata per locale

Every public page: `html lang`, the canonical URL of its own locale, hreflang alternates for every locale and `x-default` for the default, the Open Graph locale, title and description from the locale's dictionary, the share image of the locale (seo-geo.md). The sitemap lists every locale's URL with its alternates.

## Formatting and time

- Money: a price table per currency in `config/pricing.ts`, formatted with `Intl.NumberFormat(locale, { style: 'currency', currency })`; never a number with a symbol typed into copy.
- Dates and times: `Intl.DateTimeFormat` with the locale and the locale's time zone; "today" for a user is computed in their zone, since the Worker's clock is UTC. A locale with a region takes the region's zone; a locale without one (`ko`, `en`) takes the operator's zone, from the brief's owner (question 1 asks where they are based), else the zone of the default locale's main country; a thing that happens at a place (a meeting, a show) shows that place's time in every locale; UTC only for a worldwide audience the brief names.
- Plurals and lists: `Intl.PluralRules` and `Intl.ListFormat`; counts never hardcode "s".
- Input: names without a required family-name split, addresses as free lines, phone numbers with a country code; validation by shape, not by one country's rule.

## Fonts

One family per script that has the glyphs: a Latin family alone drops to a fallback for CJK and looks broken. The pages load the family from Google Fonts by `<link>` per locale (only the family the page needs, with `preconnect` and `display=swap`), or self-host it under `public/fonts/` when a market blocks the host or the brand asks; a blocked market gets the system stack. Korean text uses `word-break: keep-all` and `overflow-wrap: anywhere`; Japanese and Chinese wrap by character; German and Finnish need a third more width in buttons and navigation than English, so labels are tested in the longest language, not the default one.

## Legal and market pages

Terms, privacy and refund pages exist per locale, with one legal original (the operator's language) and summaries in the others, and a line that says which governs. A market that requires a disclaimer, a business registration line or a specific sign-in provider gets it through `localeFeatures`, so that the requirement is visible in one file.

## Adding a language later

Add the tag to `LOCALES` and its row of formats; the typecheck lists every dictionary that misses it; write them; run the dictionary test; add the share image; the sitemap, the switcher, hreflang and the routing follow from the list.
