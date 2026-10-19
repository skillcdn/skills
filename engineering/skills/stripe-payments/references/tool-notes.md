# Tool notes: how the tools behaved in this skill's phases

By topic, in the order a run meets them. A fact that can go stale names where it was seen and the month; a fact about how the tools work carries no date and changes when a run finds it wrong. What every Stripe skill shares is in the pack's Stripe pages; these are the edges of this skill's own phases.

## Shell

- On a Windows machine, Git Bash's `curl` crashed on `api.stripe.com` (exit code 139) while Node's `fetch` worked; the setup script and every ad hoc call run as a Node script that reads the key from its file by path (seen 2026-09).
- A key saved on Windows carries a carriage return; the reader trims it, or every call answers 401 with a key that looks right.
- The CLI reads `STRIPE_API_KEY` from the environment and needs no `stripe login`; a shell that forgets exports between commands gets the variable on each command line, read from the file, never typed.
- Git Bash turns an argument such as `/v1/prices` into a Windows path; a Node script, or `MSYS_NO_PATHCONV=1` on the command, keeps it (seen 2026-10).
- `@stripe/cli` as a dev dependency of the project with `XDG_CONFIG_HOME` pointed at a temporary folder kept the CLI and its configuration inside the project; nothing global changed (seen 2026-10).
- A project on Cloudflare's typed configuration (`cloudflare.config.ts`) hands the dev server only the secrets the configuration declares; `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` are declared for the dev server before the first local test (seen 2026-10).

## Account and keys

- `POST /v1/account` on the account that owns the key answers 403: the call is for connected accounts, so the business profile, the statement descriptor and the branding are the person's dashboard items (seen 2026-08).
- A restricted key with Balance Transactions Read and Charges Read expands `data.source` on balance transactions, which is what the revenue sync needs; a key without Charges Read gets the id and no currency (seen 2026-09).
- A sandbox's account profile name carries "sandbox" and its own account id; the live account's id differs, which is how a run tells the two apart without reading the key (seen 2026-10).
- The `Stripe-Version` response header of any call names the API version it ran on; with no request header that is the account's default, and it is what the webhook endpoint is pinned to.
- On API version 2026-08-26 a promotion code is created with `promotion[type]=coupon` and `promotion[coupon]=<id>`; `coupon` alone is refused and the error names the parameter (seen 2026-10).

## Checkout

- Accounts created from mid-2026 can have Managed Payments on by default for every session, with no account-level toggle; `managed_payments[enabled]=false` on each session keeps the business as the seller (third-party report, and a run, checked 2026-10).
- `payment_intent` on a retrieved session is a string unless `expand[]=payment_intent.latest_charge` is passed; the reader handles both shapes.
- A promotion code lowers `amount_total` below the order's price while `amount_subtotal` keeps the price; a check that compared the total with the order refused every discounted order until it compared the subtotal and recorded the discount.
- The product's name shown on the hosted page is the inline `product_data[name]` when the buyer's locale differs from the registered product's language; the registered product is used for the default locale only, which is why both paths exist.
- Stripe's Checkout `locale` list has `zh`, `zh-HK` and `zh-TW` but no regional variants of most other languages; an unlisted tag is sent as `auto`.
- Adaptive Pricing showed a buyer with a Korean address a USD price converted to won; the session completed in won and the amount check refused it, which `adaptive_pricing[enabled]=false` on every session prevents (seen 2026-10).
- `expand` goes at most four levels deep; a promotion code expanded through the breakdown failed both the return and the webhook until the code was read separately by its id (seen 2026-10).

## Webhooks

- `stripe trigger` builds its own fixtures: the event reaches the handler with an order id the ledger does not know, so it proves the wiring, not the order path; the order path needs a session the app created and a payment on the hosted page.
- Events arrive out of order and more than once; a `payment_events` row inserted before any work is what made a resent event a no-op in every run.
- A dispute event arrived before the session's completion event in a test and was dropped as an unknown order until the handler settled the order from its session by `payment_intent` first (seen 2026-10).
- On a Worker that Workers Builds deploys, setting the webhook secret from the CLI created a version from the code that was active at that moment, which once was older than the last build; the deploy status is checked after every CLI secret change and the build rerun when they differ (seen 2026-09 on a connected Worker).

## Subscriptions

- `current_period_start` and `current_period_end` moved from the subscription's top level to its items on newer API versions; the reader looks in both places (seen 2026-09).
- A subscription Checkout creates a new Customer per session, so an email change for receipts is per subscription (`POST /v1/customers/<id>` with `email`).

## Ledger

- `GET /v1/balance_transactions` lists newest first; a page cap reached mid-window loses the oldest days, and a sync that wrote the partial result zeroed them; the reader throws at the cap instead (seen 2026-08).
