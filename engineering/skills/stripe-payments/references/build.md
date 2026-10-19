# The payments code

What the build phase writes into the project, file by file, so that a fresh agent produces the same shape: the price table, the ledger, the Stripe client, the checkout and return routes, the webhook, the entitlements and their hooks, the pages, the secrets' names and the tests. The structure follows the layout `cloudflare-new-app` leaves (`src/config/`, `src/lib/`, `src/app/`, `migrations/`); a project of another shape gets the same modules in its own places, and a piece this page leans on that the project lacks (a `Dict` type for locale-complete copy, a money formatter, an environment module, a guest cookie, a check script, legal pages) is added in its smallest form and named in the plan rather than skipped. The facts behind each piece are in [checkout.md](/engineering/docs/stripe/checkout.md).

## The price table

`src/config/pricing.ts`, the one place a price lives; its shape as data is [pricing.example.json](../assets/pricing.example.json):

- `PROJECT`: the Worker's `name` from the Wrangler configuration, the prefix of Stripe product ids (`<project>-<product id>`).
- `PRODUCTS`: one entry per thing sold, with `id` (lowercase, stable), `kind` (`once`, or `recurring` with `interval` `month` or `year`), `grant` (`{ type: 'unlock' }`, `{ type: 'credits', amount: 10 }`, `{ type: 'period' }`), `trialDays` when the plan asked for one, `prices` per currency as whole units (`{ USD: 10, JPY: 1000 }`), and `listPrices` per currency when a struck-through price is shown.
- `PRODUCT_COPY`: the name and description per locale, typed with the project's `Dict` so that a missing locale fails the typecheck; the name is what the buyer sees on Stripe's page.
- `lookupKey(productId, currency)`: `<productId>-<currency lowercase>-<once | month | year>`.
- `toMinorUnits(amount, currency)` and `fromMinorUnits`: whole units for the zero-decimal currencies on Stripe's list (`stripe docs currencies` prints it), hundredths otherwise; every amount that goes to or comes from Stripe passes through them.
- `currencyFor(locale)` from the project's locale table; the order's currency is fixed by the market the buyer is in, never by the browser.
- `MIN_CHARGE` per currency: Stripe's minimum charge amount in that currency, which a price must not go under; a discount is Stripe's (a coupon or a promotion code), never the app's.

## The ledger

A migration `migrations/<next>_payments.sql`:

```sql
CREATE TABLE orders (
  id TEXT PRIMARY KEY,                 -- ord_<random>, the Checkout's client_reference_id and metadata.order_id
  member_id TEXT,                      -- NULL for a guest
  device_id TEXT,                      -- the guest cookie's id, so that a guest's purchase is claimed on sign-in
  subject_id TEXT,                     -- what the order is about (an item, a document) when the grant is an unlock
  product_id TEXT NOT NULL,
  product_name TEXT NOT NULL,          -- the name shown at purchase, kept as it was
  amount INTEGER NOT NULL,             -- the price in whole units; the discount is kept apart
  currency TEXT NOT NULL,
  discount_amount INTEGER NOT NULL DEFAULT 0,   -- what Stripe's promotion code took off, written at settlement
  promotion_code TEXT,                          -- the code used, from the session, written at settlement
  status TEXT NOT NULL DEFAULT 'pending',       -- pending | paid | refunded | disputed | canceled
  payment_key TEXT,                    -- the PaymentIntent id (`free_<session id>` for an order Stripe completed with no payment)
  method TEXT,                         -- card, link, ... from the charge; 'code' for a free order
  buyer_email TEXT,                    -- from Checkout's customer_details for a guest
  refunded_amount INTEGER NOT NULL DEFAULT 0,
  dispute_status TEXT,
  attribution TEXT,                    -- JSON written at creation by an integration (the ads skill): click ids, the request's IP and agent
  livemode INTEGER NOT NULL,           -- 1 when the order was created under the live mode variable
  created_at TEXT NOT NULL,
  paid_at TEXT
);
CREATE INDEX idx_orders_status ON orders(status, paid_at);
CREATE INDEX idx_orders_payment_key ON orders(payment_key);
CREATE INDEX idx_orders_subject ON orders(subject_id);
CREATE INDEX idx_orders_member ON orders(member_id);

CREATE TABLE payment_events (          -- the idempotency keys and the audit of what Stripe told us
  id TEXT PRIMARY KEY,                 -- the Stripe event id, or a guard key such as notify:<order id>
  order_id TEXT,
  type TEXT NOT NULL,
  amount INTEGER NOT NULL DEFAULT 0,
  detail TEXT,
  created_at TEXT NOT NULL
);
CREATE INDEX idx_payment_events_order ON payment_events(order_id, created_at);

CREATE TABLE entitlements (            -- what a paid order granted, and to whom
  id TEXT PRIMARY KEY,
  order_id TEXT NOT NULL,
  product_id TEXT NOT NULL,
  member_id TEXT,                      -- the owner once known
  device_id TEXT,                      -- the guest owner until sign-in claims it
  subject_id TEXT,                     -- the thing unlocked, for an unlock grant
  kind TEXT NOT NULL,                  -- unlock | credits | period
  amount INTEGER NOT NULL DEFAULT 0,   -- credits granted (0 for an unlock)
  status TEXT NOT NULL DEFAULT 'active',   -- active | revoked
  created_at TEXT NOT NULL,
  revoked_at TEXT
);
CREATE INDEX idx_entitlements_subject ON entitlements(subject_id, status);
CREATE INDEX idx_entitlements_owner ON entitlements(member_id, device_id, status);
```

When something recurs:

```sql
CREATE TABLE subscriptions (
  id TEXT PRIMARY KEY,                 -- sub_<random>
  member_id TEXT NOT NULL,             -- a subscription needs an account to follow the person
  product_id TEXT NOT NULL,
  stripe_subscription_id TEXT NOT NULL UNIQUE,
  stripe_customer_id TEXT,
  status TEXT NOT NULL,                -- Stripe's: active | trialing | past_due | canceled | ...
  cancel_at_period_end INTEGER NOT NULL DEFAULT 0,
  current_period_start TEXT,
  current_period_end TEXT,
  currency TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

A credits grant is the sum of active `credits` entitlements minus what the project's own spend table consumed (the project keeps a `credit_uses` ledger when none exists). An unlock is an active `unlock` entitlement for the subject whose order's `livemode` equals the deployment's mode; the same filter applies to credits and periods, so that sandbox test orders grant nothing once the site runs live. A guest is identified by the project's guest cookie; a project without one gets `<app>_device`, a random id in a one-year `HttpOnly` cookie set by the orders route, and sign-in claims the entitlements of that device id as the new-app skill's guest path does. The migration is applied locally in this phase and to the remote database before the code that needs it is pushed, as the deploy skill's rule says.

## The Stripe client

`src/lib/payments/stripe.ts`: a `stripeFetch(path, { method, form, key?, idempotencyKey? })` over `fetch` with the key as a bearer header and `application/x-www-form-urlencoded` bodies (nested fields as `line_items[0][price]`), which throws an error carrying Stripe's `error.code`; no SDK, because the Workers bundle stays small and the REST shapes are what `stripe docs` prints. On top of it: `createCheckoutSession(order, options)`, `retrieveCheckoutSession(id)` with `expand[]=payment_intent.latest_charge` and `expand[]=total_details.breakdown`, `findPrice(lookupKey)` (`GET /v1/prices?lookup_keys[]=<key>&active=true`, cached for the request), `verifyWebhookSignature(rawBody, header, secret)` (HMAC-SHA256 over `<t>.<body>` with Web Crypto, five-minute tolerance, constant-time compare), and for subscriptions `getSubscription`, `cancelAtPeriodEnd`, `cancelNow`, `createPortalSession`. The key comes from `STRIPE_SECRET_KEY` and the mode from `STRIPE_MODE` (`sandbox` or `live`, a var of the deployment and a line of the local secrets file) through the project's environment module; `stripeConfigured()` is false when either is unset or when the key's prefix disagrees with the mode (`_live_` under `sandbox`, `_test_` under `live`), and then paid orders answer 503 "payments not ready" while free orders still work. `expectedLivemode()` is true under `live`; every settlement compares it with the object's `livemode`.

`createCheckoutSession` builds the form of checkout.md "Hosted Checkout": the price by lookup key, else `price_data` with the product's name in the buyer's language; `mode` by the product's kind; `success_url` and `cancel_url` with the locale parameter the project uses; the order id in `client_reference_id`, `metadata` and `payment_intent_data` (or `subscription_data` for a recurring product); `customer_email` for a member; `allow_promotion_codes=true`; `locale` from the buyer's locale when Stripe lists it; `managed_payments[enabled]` as the plan decided; `subscription_data[trial_period_days]` when the plan has a trial; `automatic_tax[enabled]=true` only when the plan says Stripe Tax is active. The metadata carries the order id and nothing else about the buyer.

## The routes

- `POST /api/orders`: body `{ productId, subjectId?, locale? }`. Validates the product, finds the buyer (member session, else the guest cookie, set here when missing), fixes the currency from the market, runs the attribution providers (below) and stores their result in `attribution`, creates the order row as `pending` at the full price with the deployment's `livemode`, and creates the Checkout Session with the parameters of checkout.md's table (`adaptive_pricing[enabled]=false` among them) and answers `{ ok, orderId, url }`; the client navigates to `url`. Rate limit: no more than six pending orders per subject or device in ten minutes. A partner link's code, when the project has them, is passed to Stripe as checkout.md says of promotion codes; an order Stripe completes with no payment (a 100 percent code) is settled by the same confirmation and webhook path, never by the app alone.
- `POST /api/payments/confirm`: body `{ sessionId }` from the success page. Retrieves the session, finds the order by `metadata.order_id` or `client_reference_id`, and settles as checkout.md "Confirming a payment" says: the session's `livemode` equals the deployment's; the currency equals the order's; `amount_subtotal` equals the order's amount in minor units; `amount_total` is the subtotal minus the discount Stripe reports, which is written to `discount_amount` with the code from the breakdown; `payment_status` is `paid`, or `no_payment_required` with a total of 0 for a free code. Answers `{ ok }` to anyone with the session id and the order's product, grant and where to go next only when the caller's member session or guest cookie matches the order. An already paid order answers success without granting again; a refunded or disputed one answers 409, and the success page shows its own message for that case rather than "nothing was charged".
- `POST /api/webhooks/stripe`: raw body, signature check (503 when the secret is unset, 400 on a bad signature), an event whose `livemode` disagrees with the deployment's answered 200 ignored, then by event type as checkout.md "The webhook endpoint" lists; every handler inserts its `payment_events` row first (a duplicate id means "already processed"), deletes it and answers 500 when it throws, and answers 200 with a one-word result otherwise. Unknown types answer 200 ignored. The checkout handler applies the same amount rule as the confirmation; a refund or dispute handler that meets an order still `pending` settles it from its session first, as checkout.md says.
- Subscriptions: `POST /api/subscription/cancel` (period end), `POST /api/subscription/portal` (a portal session URL), both for the signed-in member.

## Settlement and entitlements

`src/lib/payments/settle.ts`: `settleOrder(order, session)` marks the row paid with the payment key, method, buyer's email, discount and code, inserts the entitlement row (or upserts the subscription from Stripe's object for a period grant), and calls the hooks. `revokeOrder(order, { amount, reason })` reverses the grant in proportion to the refunded amount (an unlock is revoked when the refund is full; credits are revoked by the refunded share, floored at zero) and calls the hooks. `src/lib/payments/entitlements.ts` is what pages ask: `isUnlocked(subjectId)`, `creditsOf(person)`, `hasActivePlan(memberId)` (status active or trialing, and the period end plus a 72-hour grace in the future).

`src/lib/payments/hooks.ts`: `onPaid`, `onRefunded`, `onDisputed` as arrays of async functions `(order, context)` that never throw into the caller (each wrapped, failures logged), and `attributionProviders` as functions `(request, draftOrder) => Record<string, string>` whose results are merged into the order's `attribution` JSON at creation, so that the webhook, which is not the buyer's request, finds there what the browser knew. Both settlement paths, the return confirmation and the webhook, call the same hooks, and only the path that moves the order to `paid` runs them: a path that finds the order already paid returns without them, so a hook that needs a retry retries itself; a hook that must run once per order guards itself with a row in `payment_events` (`notify:<order id>`, `capi:<order id>`) written after its work succeeded. The hooks are where other integrations attach: the ads integration adds an attribution provider and a paid hook that sends the purchase event; a notification (an operator's chat message, a receipt email) is a guarded paid hook.

## The pages

- The buy surface where the plan put it: the product's name, price in the buyer's currency formatted by the project's money formatter, the list price struck through when there is one, a note on the payment page's provider, and the button that posts to `/api/orders` and navigates to the URL. Whether content is paid is decided by a configuration var, `PAYMENTS_ENABLED` (`false` while the user wants the content free before the live switch, `true` from the switch), never by whether a key is set: with the var on and the key or the mode missing, the paid part stays locked and the button says payments are unavailable (the orders route answers 503), so that a lost secret never gives paid content away.
- `/pay/success`: reads `session_id`, posts to confirm, shows what was bought and a link to it; `noindex`, out of the sitemap. `/pay/fail`: a plain message and the way back; `noindex`. Receipts are Stripe's emails, not a page of the site.
- The refund page per locale with the policy the user chose, linked from the buy surface and the footer; the terms page names the seller of record; the privacy page's payments paragraph says that Stripe processes the card and what the site keeps (an email, an amount, never a card number). A project without legal pages gets them here, in their smallest honest form, because the payment page links them.
- An account page section, when members exist: the orders, the subscription's status and period, the cancel and portal buttons.

## Secrets and configuration

The project's local secrets example file gains the names with comments: `STRIPE_SECRET_KEY` (the sandbox's key locally, the restricted runtime key on the Worker), `STRIPE_WEBHOOK_SECRET` (the CLI listener's locally, the endpoint's on the Worker), `STRIPE_MODE` (`sandbox` locally; on the Worker a var in the Wrangler configuration, `sandbox` until the live switch sets `live`). When the Wrangler configuration declares `secrets.required`, the two secret names are added there, since local development loads only the listed names. `DEPLOY.md`'s secrets section and `docs/payments.md` list them. No key goes into `wrangler.jsonc`'s `vars`.

## The sync script

`scripts/stripe/sync.mjs` imports `src/config/pricing.ts` directly (Node strips types on the current LTS; `--experimental-strip-types` on an older one) and syncs products and prices as [stripe-side.md](stripe-side.md) says, with the key in `STRIPE_API_KEY`.

## Tests

`tests/payments.test.ts`, run by the project's test script: the minor-unit conversion in both directions for a zero-decimal and a decimal currency; the lookup key format; the signature check accepts a correct signature and rejects a wrong one and an old timestamp; the amount rule accepts a session whose total is the subtotal minus a discount and refuses one whose subtotal differs from the order; a session or an event whose `livemode` disagrees with the mode variable settles nothing; a key of the other mode makes `stripeConfigured()` false; the webhook's idempotency (the same event twice settles once) against an in-memory database; the refund arithmetic (partial and full) and the grant reversal; the Checkout form for a one-time and a recurring product carries the order id in every place, the promotion code switch and the Managed Payments field, and no buyer data in metadata; the confirmation reveals the grant only to the matching cookie; the dictionary of product copy has every locale.

## `docs/payments.md` template

```markdown
# Payments

Stripe account <id, country, settlement currency>; API version <from the probe>. Mode: <sandbox only | sandbox and live>. Seller of record: <the business | Stripe (Managed Payments)>. Refund policy: <the policy>.

## What is sold
| Product | Kind | Grants | Prices | Lookup keys |
|---|---|---|---|---|

## Stripe objects
Sandbox: products <ids>, prices <ids>, promotion code <code> (test, free); webhook: the CLI listener locally, endpoint <id> at <url> while the deployed site ran on the sandbox key.
Live: products <ids>, prices <ids>, webhook endpoint <id> at <url>. Keys: the runtime key on the Worker; the setup key rolled on <day>.
Sync: `node scripts/stripe/sync.mjs` with the mode's key in `STRIPE_API_KEY` (creates or updates by id and lookup key).

## Flow
Buy button on <page> -> POST /api/orders -> Stripe Checkout -> /pay/success -> POST /api/payments/confirm; backup and refunds through POST /api/webhooks/stripe (events: ...). The deployment's mode is STRIPE_MODE; nothing of the other mode settles.

## Money
Orders table: the funnel. Settled revenue: Stripe's balance transactions (see the ledger page of the pack); the operator panel syncs them. Zero-amount orders are excluded from the numbers.

## Operator panel (spec)
Orders list (search by email or id, status, amounts, discount, refund and dispute state, the PaymentIntent id linked to Stripe's dashboard page); a refund action that calls POST /v1/refunds with the order's payment key, confirmed and audited; revenue by day and market from the ledger; webhook health (last events, the endpoint's status); subscriptions with status and period. A key with Balance Transactions Read, Charges Read, PaymentIntents Read and Webhook Endpoints Read for the figures; a key with Refunds Write and PaymentIntents Read only where the panel refunds.

## Done by a person
<the dashboard checklist with the menu paths of the day, ticked as GET /v1/account shows them set>
```
