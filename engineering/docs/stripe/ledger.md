# Settled revenue: the balance ledger

What the business earned is read from Stripe's balance transactions, not from the app's orders table: fees, refunds, disputes and the real exchange rate are already in it, in the account's settlement currency. This page says how the ledger is read, folded into days and markets, cached and shown, and where it differs from the orders table. The orders table stays the funnel's truth (what was ordered, by whom, in which currency); the ledger is the money's.

## Reading the ledger

`GET /v1/balance_transactions` with `created[gte]` and `created[lt]` as Unix seconds, `limit=100`, `expand[]=data.source` and `starting_after` for the next page. Each row has `type` and `reporting_category` (the category is the stable grouping: `charge`, `refund`, `dispute`, `dispute_reversal`, `fee`, `payout`, `transfer`, ...), `amount` (the gross movement), `fee`, `net`, `currency` (the settlement currency) and `created`; the expanded `source` is the charge, refund or dispute, and its own `currency` is what the customer was charged in, which is the key to the market (a run confirmed that a restricted key with Balance Transactions Read and Charges Read can expand it, checked 2026-10). The key needs no more than those two read permissions.

## Folding into days

One row per day and market: `gross` (charges' `amount`), `fee` (every row's `fee`, plus standalone negative adjustments that are not refunds), `net` (every row's `net`), `refund` (refunds, disputes, dispute reversals and failures, as positive amounts that reduce revenue; a reversal is negative and so reduces the refund figure), `charges` (the count of charge rows). The day is the business day in the operator's time zone, computed from `created` with that zone's offset, never the Worker's UTC. The market is the presentment currency's market (the site's locale table maps currency to market); a currency not in the table is `other`. Rows whose settlement currency is not the account's are counted and skipped, because mixing settlement currencies breaks the sum. Payouts, transfers, top-ups and their reversals are balance movements, not profit or loss, and are excluded.

## The cache and the sync

The dashboard never calls Stripe on view: a sync writes the folded rows into a table (`revenue_daily` or the name the project chose) and the panels read the table. Because refunds and disputes land on later days against earlier charges, the sync re-reads a whole window (the last 14 days by default; 120 days when the cache is empty or covers only the last week, in windows of 30 days) and replaces each window in one batch. Two rules protect the cache:

- **A partial read never overwrites.** The list is newest first and `starting_after` walks back in time, so when the page cap is reached the oldest days of the window are the ones missing; writing what came back would zero those days. The reader throws when `has_more` is still true at the cap (40 pages of 100 by default), the sync records the failure, and the cache keeps the earlier figures. A wide backfill is split into shorter windows instead of raising the cap.
- **One failing source never wipes another.** Revenue, ad spend and exchange rates are synced independently; a failure in one leaves the others' rows untouched and the sync's status says `partial`.

The sync is a scheduled job (a cron trigger of the dashboard's Worker, hourly) and a button on the panel that the operator presses; it records its last run, its window and its result where the panel shows them. A page never starts a sync by itself.

## What the figures mean

- Net profit for a day is the ledger's `net` minus ad spend minus other costs the operator records; ROAS is gross divided by ad spend. The ledger's net already excludes Stripe's fees and refunds, so it matches the dashboard's "net volume" in Stripe.
- The orders table's revenue (paid orders at their currency, converted at the day's exchange rate) differs from the ledger by fees, by refund timing, by the exchange rate Stripe used and by orders paid outside Stripe; the panels show one as money and the other as the funnel's outcome, never as the same number.
- Zero-amount orders (a 100 percent promotion code) appear in neither: they are excluded from revenue, conversion and funnel statistics, and kept in the orders list with a mark.
- In a sandbox the ledger holds test movements with the same shape, which is how the fold is verified before live mode.

## Exchange rates

Only costs in other currencies need converting (ad spend billed in a local currency); revenue is already settled. Daily reference rates from the European Central Bank through the free `api.frankfurter.dev` (historical, no key), with `open.er-api.com` as the same-day fallback for currencies the ECB does not publish (checked 2026-10), carried forward over weekends, cached per day and currency, converted at the spend day's rate and never the latest one; a row without a rate keeps its local amount and a null converted amount, which the panel counts and shows rather than recording a zero.
