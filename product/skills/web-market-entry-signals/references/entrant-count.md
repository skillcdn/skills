# Counting entrants so that the count can be made again

Gate 03 asks whether new competitors are coming in. This page says which counts answer it, how each is made, and what each misses. Read by the branch that counts, and before the verdicts.

## Names are a floor, not a count

The companies a note happens to name are the ones the articles named. Counted, they give a floor far under the real number: a recount of one theme from first release dates in an app store found several times as many entrants in each year as the names in the notes. So a count of names is never written as a number, in a note, a verdict or a memo. Write "at least the three named here" in words, and count by one of the three ways below.

## App store first release dates

For a theme sold as an app. The App Store search answers without a key ([sources.md](/docs/market-research/sources.md)); [appstore-entrants.example.mjs](../scripts/appstore-entrants.example.mjs) reads it, keeps the apps that pass the tests, counts them by the year of first release and writes every kept app to a CSV.

1. **Terms.** About twenty, in the country's language: the words a buyer types for this kind of app, not brand names. At most 200 apps come back for a term, so several narrow terms find more than one broad one.
2. **The core test.** The words that make an app one of this theme's business, looked for in the name and the start of the description. Too few words lose apps; a word that also names another business brings strangers.
3. **The AI test**, when the theme is the AI form of an older business: an AI mark in the name, or an AI word close to a core word in one sentence of the description. Leave it out when any entrant counts.
4. **Exclusions.** Words of neighbouring businesses that the core test lets in, and of services the user has a stake in.
5. Read twenty rows of the CSV from different years before the count is used: strangers that remain mean a tighter test and a second run.

What it misses, said with the count: only apps in the store today are counted, so those that left are gone; a web service or a messenger channel has no app; a first release can be older than the app's present business. The count is `measured`, and the note keeps the country, the terms, the tests and the day.

## Official registrations and formations

For a theme sold by registered businesses: new online sellers by category from the filings file, registered businesses of an everyday type, new businesses by industry, business applications by sector. [sources.md](/docs/market-research/sources.md) says where each is and when it comes out. The category that holds the theme is wider than the theme: say which category was read and that it is an upper bound on the theme's own entrants. The count is `official` where the release states it and `computed` where it is counted from a downloaded file.

## Ads against a baseline

For any theme that advertises: the number of different sellers on the pages read for the theme's phrase, and the theme's active ads against the baseline term's, from `meta-ad-library-rising-products` in its watch mode. It counts sellers who advertise now on one platform, not all who entered. `measured`.

## Which to use

| The theme is sold as | First count | Second, to bound it |
|---|---|---|
| An app | App store first release dates | Ads against a baseline |
| A web service, a channel in a messenger, a shop | Official registrations in its category | Ads against a baseline |
| A service to businesses | Official formations in its sector | Named entrants, in words |

Two counts that disagree are both written, with what each misses. A theme with one count says so in the memo; a theme with none is `unknown` on gate 03.
