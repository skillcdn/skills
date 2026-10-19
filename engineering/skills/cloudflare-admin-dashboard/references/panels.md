# The panels

Which panels an admin gets, what each shows and from where, the charts' rules, the controls, and the contract by which a later integration adds its panel. The queries read the project's tables and the admin's caches; the money's truth is the payment ledger ([ledger.md](/engineering/docs/stripe/ledger.md)), the ads' figures are the spend cache and the site's rows ([monitoring.md](/engineering/docs/meta-marketing-api/monitoring.md)).

## Which panels apply

| Panel | Built when | Reads |
|---|---|---|
| Overview | Always | The funnel's tables, the orders and revenue caches when they exist, the spend cache when it exists |
| Funnel | Always | The tables the moments map to |
| Payments | `docs/payments.md` exists (the orders and events tables) | Orders, payment events, the revenue cache, Stripe's refund call for the control |
| Ads | `docs/ads.md` exists (the spend and attribution tables) | The spend cache, the site's attributed rows, the rules' parameters, Meta's status and controls |
| Costs | An AI usage table exists, or the user records costs | The usage table, the manual costs table, the rates cache |
| System | Always | The sync state, the secrets' presence, the webhook events, the audit log, the Worker's own health |

The plan names the set; a panel the project cannot feed is not built and `docs/admin.md` says what would feed it.

## Overview

Today so far, yesterday, the last 7 days and the last 30, each against the same window a week earlier: visits (the first moment; a project with no visits table gets a daily counter by page group, written in the background by the public site's request handler with no cookie and bots excluded, as a shown addition of the plan), the paid step's count, conversion between the first and the last moment, paid orders and their revenue (orders table, excluding zero-amount orders), settled net revenue (the ledger cache), ad spend and net profit (revenue net minus spend minus costs) when the caches exist, ROAS on the site's revenue. A line of what needs attention from the alert rules. "Today" is the business day in the operator's zone; a figure with no data yet shows a dash and the date counting started.

## Funnel

The moments in order, as columns, per day for the last 30 days and summed for 7, 30 and all time, with the rate between consecutive steps; a cohort view where each day's visitors are followed to their own later steps (a 24-hour maturity before a day's conversion is shown as final); a split by locale or market when the project has several. Zero-amount orders' visitors are excluded from the paid step and counted apart; opted-out visitors are counted in visits and never attributed. A list of recent visitors' rows with the moments reached, the source when attributed, and a detail page with the row's fields, its orders and, when the project logs model calls, those calls' cost and latency; no customer content is rendered beyond what the operator needs to support the person.

## Payments

Revenue by day and market from the ledger cache (gross, fees, refunds, net), the sync's last run and a button; product by currency for 7, 30 and all time from the orders table, net of partial refunds; the orders list (search by email or order id as a `POST`, status filter, pagination), each with amount, currency, promotion code, status, refunds, dispute state, and its PaymentIntent id linked to Stripe's dashboard payment page, which opens only for a signed-in Stripe user (no receipt links, which are bearer links); subscriptions when they exist, with status, period, cancellation, and the counts the plan asks for (active, new this month, cancelled this month, past due). Webhook health: the last events in `payment_events` and the time since the last one, and the endpoint's status from Stripe read with the read key. The refund control, when the plan has it: from an order's row, the confirmation with the amount (full or partial, in the currency's minor units, within the order's unrefunded amount and the day's cap), the call (`POST /v1/refunds` with `payment_intent`, `amount`, `reason` and an `Idempotency-Key` equal to the confirmation's nonce), the result; the webhook does the bookkeeping, and the row shows it when the event lands.

## Ads

Per market and period (7, 14, 30 days, custom): the campaign table at campaign, ad set and ad level with spend (native and converted), impressions, clicks, CTR, CPC, frequency, the learning status, Meta's purchases and ROAS, and beside them the site's sessions, leads, orders, revenue, cost per order and ROAS from the attribution join; the recommendations of the rules with their evidence and, when the plan has controls, an apply button each (pause, resume, a budget change within the step and the cap), confirmed and audited; the attribution funnel by campaign; the integration status (datasets per market from the project's analytics configuration and their last event from the dataset's stats, accounts with currency, time zone and status from the sync, the API version with its end date when known, which of the admin's own secrets are set); the spend sync's last run and a button. The test event is sent from the shell with the project's script, since the admin holds no dataset token. The rules' parameters shown with a form to change them, confirmed and audited.

## Costs

AI usage when the project logs model calls: calls, tokens and cost by day and by model, average and p90 latency, calls with no tokens and no cost (the sign of a silent fallback), stuck rows (a step started and not finished within its usual time); manual costs: a form (day, market, type, amount, currency) that converts at the day's rate when entered and stores the rate, a list with delete behind a confirmation; both feed net profit and never ROAS.

## System

The sync state of every cache (last run, window, status, detail), the cron's last tick, the admin's secrets' names with set or unset, the time since the public site's last webhook event, the admin's audit log (newest first, filters), the Worker's version from its version metadata binding, the operators from the allowlist secret, and the inventory's findings until they are fixed.

## Charts

Inline SVG rendered by the Worker: a bar or a line per series, days on the x axis filled with empty days so that a gap is a gap, the window cut by date, the label naming the window and the zone, at most four series, colors that differ in lightness so that they read without color, numbers formatted by the operator's locale, money with its currency. No chart library, no client rendering, no animation.

## The panel contract

`docs/admin.md` in the project says how a later integration adds its panel, so that `stripe-payments` or `meta-ads-setup` run after the admin can add theirs without reading this skill:

- A panel is a folder `admin/src/panels/<name>/` with `index.ts` exporting `{ key, title, routes, nav }`, its queries in `queries.ts` against the shared database, its views in `views.tsx`, and its actions under `routes` as `POST` handlers that use the confirmation helper and the audit helper.
- It is listed in `admin/src/panels/index.ts`, in the order of the navigation.
- Its migrations (cache tables) go in `admin/migrations/` and are applied to the shared database before the deploy that reads them; a cache table the project already has (named in `docs/payments.md` or `docs/ads.md`) is reused, never duplicated, and a table the admin adds carries the `admin_` prefix.
- Its secrets are named in `admin/.dev.vars.example` with comments and set on the admin Worker, never on the public site.
- Its syncs register with the cron scheduler in `admin/src/jobs/index.ts` with an hour and a name, and write the sync state.
- Its alerts register with `admin/src/alerts/index.ts` as functions that return a list of lines for the digest and immediate alerts.
