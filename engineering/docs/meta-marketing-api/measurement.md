# Measurement: the dataset, the pixel, the Conversions API and attribution

How a site tells Meta what the ads brought, without telling it anything private: the dataset and its settings, the domain's verification, where the browser pixel may run and where only the server speaks, the Conversions API event and its deduplication, how a visit's origin is captured and carried to the purchase, the privacy signals that stop everything, and why each market has a dataset of its own. The rules hold for any site whose pages or links carry something a visitor would not want an ad platform to see: something made for them, an account, an order.

## The dataset

A dataset (the API still says pixel, `adspixels`) is created with `POST /act_<id>/adspixels` with `name`; an account holds one, and a second creation fails (error 6200 "A pixel already exists for this account", checked 2026-10). Settings set right after creation with `POST /<pixel_id>`: `enable_automatic_matching=false` (automatic advanced matching would read form fields such as a name or an email out of the page; the server sends the hashed email of a buyer instead), `first_party_cookie_status=FIRST_PARTY_COOKIE_ENABLED` (the `_fbp` cookie is set by the pixel on the site's own domain, which keeps attribution working without third-party cookies). A dataset is a business asset: `POST /<pixel_id>/shared_accounts` with `account_id` and `business` shares it with another ad account of the same business, which is how a second ad account (a new market's, another account of the same market) uses the same dataset, so that the dataset id in the code, the token and the event history stay (checked 2026-10). Assigning a system user to the dataset (`assigned_users`) is undocumented and may fail; the dashboard path is Business settings > System users > the user > Add assets > Datasets. The dataset id is a public value: it is in the page source of every site that runs the pixel, so it lives in the code's configuration, not in a secret. The dataset's `stats` edge (`GET /<pixel_id>/stats` with an aggregation by event, as the AdsPixel reference describes it) counts the events received by name over recent hours, which is how an agent confirms that a live event arrived without opening Events Manager.

## Domain verification

Business settings > Brand safety and suitability > Domains > Add > the site's domain, method Meta-tag: the person adds the domain and sends the `content` value of the `<meta name="facebook-domain-verification">` tag the screen shows; the value goes into the site's configuration (a public value) and is rendered in the head of every page; after the deploy, the person presses Verify on the same screen (checked 2026-10). The DNS TXT record and the HTML file are the alternatives when the agent can change DNS or the site's root. Verification needs a domain the business owns: a free `workers.dev` address is not the business's domain, so a site without a custom domain runs its ads unverified (Meta warns on the ads and the conversions still count for optimization) and verifies when the domain comes. Verification lets the business edit link previews of ads to its domain and is what Meta asks for conversion events of a domain to be used fully for optimization.

## The browser pixel

The pixel script (`fbevents.js`, `fbq('init', '<dataset id>')`, `fbq('track', 'PageView')`) runs only on public pages: the home, the product pages, the legal pages, the pages whose URL carries nothing private. It is rendered by the public pages' layout only, so that a private page's HTML (an item or an account page whose URL carries an id, a checkout page, the operator's screens) contains no pixel script at all, which a `curl` of the page proves; its automatic configuration (`fbq('set', 'autoConfig', false, '<dataset id>')`) and its automatic page view on history changes (`fbq.disablePushState = true`, set before `init`; Meta's single-page application page, checked 2026-10) are off, and private pages answer with `Referrer-Policy: no-referrer` (not `same-origin`, which still hands the full URL to the next page of the same site), because the pixel sends the current URL and the referrer with every event. The events it sends are `PageView` and `ViewContent` (the product page); everything that happens where the pixel does not run (`Lead`, `InitiateCheckout`, `Purchase`) is sent by the server alone. A browser event that the server also sends carries the same `eventID` so that Meta keeps one copy (`fbq('track', 'Purchase', {value, currency}, {eventID: '<order id>'})`). The pixel loader honors the privacy signals below before it loads anything. Site-wide ad pixels of other vendors follow the same rules.

## The Conversions API

`POST https://graph.facebook.com/<version>/<dataset id>/events` with the dataset's token in the `Authorization: Bearer` header, a JSON body `{"data":[<event>...]}` of up to 1,000 events, and `test_event_code` only while testing (checked 2026-10). An event:

| Field | Value |
|---|---|
| `event_name` | `Lead`, `InitiateCheckout`, `Purchase` (the standard names; a custom name clutters the dataset and is not used for optimization) |
| `event_time` | Unix seconds, within the last seven days |
| `event_id` | The order id for checkout and purchase events, `lead_<row id>` for the lead (the id of the visitor's own row); the same id on a resend, so that a retry is deduplicated |
| `action_source` | `website` |
| `event_source_url` | The public URL of the screen with every id and query removed: `/item/<id>?x=y` becomes `/item`; a page that is not public is reduced to its first path segment |
| `user_data` | `client_ip_address` and `client_user_agent` as they are; `fbp` and `fbc` as they are; `em` as the SHA-256 of the trimmed lower-cased email, for a purchase only; never a name, a phone number, an address or a date of birth, even hashed |
| `custom_data` | `value` and `currency` for checkout and purchase, `content_ids` with the product id and `content_type` `product` |
| `data_processing_options` | `["LDU"]` with `data_processing_options_country` 0 and `data_processing_options_state` 0 for a market that includes the United States, so that Meta applies Limited Data Use to the visitors it geolocates to California; `[]` elsewhere |

The response's `events_received` is 1 when the event was accepted; `fbtrace_id` is what Meta's support asks for. A failure is logged and never blocks the order; the send runs after the response (`waitUntil` on Workers) with a five-second timeout. From a development server (a loopback host) nothing is sent unless a test event code is set, so that a developer's clicks do not train the live dataset; on the deployed site during verification the test event code is set as a secret for the hour it takes and deleted afterwards.

### What is never sent

An order whose amount is zero (a full promotion code); an event of a visitor who opted out (below); any event of a market that has no dataset or no token, which is dropped rather than sent to another market's dataset; the content the visitor made or received, their name, anything typed into a form. The privacy policy's section on ad measurement lists what is sent and is rendered only while a dataset exists.

## Attribution

What a visit knew about its ad is captured at the first page and carried to the order inside the site's own database, because the webhook that settles a payment is not the buyer's request and Stripe's objects are not the place for a visitor's IP address:

1. The landing URL's `fbclid`, `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`, and the ids `campaign_id`, `adset_id`, `ad_id` (the URL tags of [campaigns.md](campaigns.md)) are read from an allowlist, trimmed to fixed lengths, and kept in a first-party cookie for 90 days with the time they were seen; the external referrer is kept as its origin only. A later tagged visit replaces the stored one; an untagged internal navigation keeps it.
2. `_fbp` (the browser id the pixel sets) and `_fbc` (the click id cookie) are read when present; without `_fbc`, one is built from `fbclid` as `fb.1.<time seen in ms>.<fbclid>`.
3. When the visitor starts something (a session, an item), the server stores the attribution fields on that row, re-validated from the request's cookies and referer; when an order is created, the fields that Meta needs (`fbp`, `fbc`, the request's IP address and user agent, the sanitized source URL) are written into the order row's attribution JSON by the payments module's attribution hook, so that the webhook reads from the order what the browser knew. Stripe's metadata carries the order id and nothing about the person.
4. Meta's automatic URL parameters (set when the ad's tracking field is empty: `utm_source=fb|ig|msg|an`, `utm_medium=paid`, `utm_campaign=<campaign id>`, `utm_term=<ad set id>`, `utm_content=<ad id>`) are recognized as the ids when the explicit ids are absent (seen 2026-10), so that attribution survives an ad made by hand.

The ids join the site's rows to the spend rows of the same campaign ([monitoring.md](monitoring.md)); that join is the second source every decision is read against.

## Privacy signals

The `Sec-GPC: 1` request header (Global Privacy Control) and a first-party opt-out cookie the site sets when the browser signals it: no pixel loads, no event is sent, no attribution is stored, the measurement cookies the pixel set earlier are expired, and the row is marked as opted out so that the dashboard can count it without attributing it. Where the site offers a consent choice, the same switch stops everything. In a market whose law requires prior consent (the EEA, the UK, Switzerland), the pixel, its cookies, the attribution cookie and the server events stay off until the visitor opts in through the site's consent banner, which the plan names; elsewhere the signals above opt a visitor out.

## One dataset per market

A site that sells in several markets with separate ad accounts keeps a dataset per market and chooses it by the visitor's locale in the browser and by the order's currency on the server; an event of a market without a dataset or without its own token is dropped. The dataset ids live in one configuration map keyed by locale with a public build variable override per market; the dataset tokens live in secrets keyed by a market suffix, with no shared fallback. A market that is turned off for ads (a region where Meta does not deliver) is an explicit `false` in the features table, not a missing id.
