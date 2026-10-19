# Monitoring and optimization: the sync, the join, the rules, the record

What phase 6 writes and sets so that the campaigns are watched on the site's own numbers and changed by rules the user fixed in the plan: the spend table and its sync, the join to the site's rows, the rules' parameters, the actions and their log, the alerts, and the `docs/ads.md` template with the operator panel's spec. The insights call, the time zones, the review method and the rules' reasons are in [monitoring.md](/engineering/docs/meta-marketing-api/monitoring.md); this page is what goes into the project.

## The spend table

A migration adds `ad_spend` (`day`, `channel` `meta`, `account_id`, `campaign_id`, `campaign_name`, `adset_id`, `adset_name`, `ad_id`, `ad_name`, `market`, `currency`, `amount`, `amount_converted`, `impressions`, `reach`, `clicks`, `purchases_meta`, `leads_meta`, `updated_at`, primary key `(day, channel, account_id, ad_id)`), `fx_rates` (`day`, `currency`, `per_unit`, `source`) and a `sync_state` key in the project's settings table (last run, window, status, detail, the accounts' info). The business day is the operator's time zone from the project's configuration.

## The sync

`scripts/meta/sync-spend.mjs [--days 14] [--remote]`, and the same module exported for the dashboard's cron: with the employee token (`META_ADS_ACCESS_TOKEN`) and the mapping (`META_AD_ACCOUNT_IDS`) read from the local secrets file, for each account of the mapping, the insights call at `level=ad` with `time_increment=1` over the window (one day wider on each side with the hourly breakdown when the account's day boundary differs, re-bucketed), the rows replaced per account for the window, exchange rates fetched for the account currencies and the order currencies over the window (ECB rates through `api.frankfurter.dev`, `open.er-api.com` for currencies it lacks; checked 2026-10) and cached, the converted amount at the day's rate (null when missing, never zero), `sync_state` written with `ok`, `partial` or `error` and the accounts' name, currency, time zone and status. A failed account keeps its rows. The default window is 14 days, 120 when the table is empty. From the shell the script writes the local database; with `--remote` it writes the same statements to the remote database through `npx wrangler d1 execute <db> --remote --file` in batches, which is how the cache is filled until the dashboard's cron exists.

## The join

A view or a query module `src/lib/ads/attribution-stats.ts`: per day, market and campaign (and down to the ad), the site's sessions, leads, checkouts, paid orders and revenue (orders' amounts converted at the day's rate, zero-amount orders and their sessions excluded, opted-out sessions counted apart), joined to `ad_spend` by `campaign_id`, `adset_id` and `ad_id`; derived: cost per session, cost per lead, cost per paid order, ROAS on the site's revenue, alongside Meta's `purchases_meta` and its own ROAS. Settled revenue from the payments ledger is the money across campaigns and is shown apart. Meta's automatic parameters (`utm_campaign` numeric, `utm_term`, `utm_content`) stand in for the ids when the explicit ids are absent.

## The rules' parameters

`src/config/ads.ts`, the one place, filled from the plan: `targetCostPerOrder` per market (the user's, else a third of the product's price), `targetRoas` (default 1.5), `testSpendFloor` (the kill rule's minimum spend, default three times the daily budget), `killDays` 3, `scaleDays` 4, `budgetStepPercent` 20, `newCreativeShareMax` 0.5, `newMarketOrderThreshold` 50, `fatigueCtrDrop` 0.3, `fatigueFrequency` 2, `reviewAfterDays` 3, `dailySpendCap` per market (the plan's weekly total divided by 7, rounded up), and `autoRules` off by default. The dashboard's panel reads these, shows them, and lets the operator change them with a confirmation.

## The review and the actions

Written in phase 6 together with the sync, because the first review comes three days after activation and the panel needs the same module. `src/lib/ads/review.ts`: `reviewAds(day)` computes, per ad set over the rule windows, the figures and the rule that fires (kill, hold, fatigue, scale, mix guard, new market cap, change window), and returns recommendations with their evidence. `applyAction(action, actor)`: pause or resume an ad set (`POST /<adset id>` with `status`), set a daily budget (`POST /<adset id>` with `daily_budget`, refused when the step exceeds `budgetStepPercent` or the new budget exceeds the cap), each written to the audit log with the actor and the figures; from the shell it uses the admin token of `.meta-token`, from the dashboard the management token the operator chose to give it. The script `scripts/meta/review.mjs` prints the review for the shell; the dashboard runs it on its cron and shows it on the ads panel with an apply button per recommendation. When `autoRules` is on, the cron applies only pauses and decreases, never above the cap, and writes each to the audit log and the daily alert.

## Alerts

The daily digest and the immediate alerts of monitoring.md "Alerts", sent through the project's notification hook (the operator's chat tool when `stripe-payments` or the dashboard set one up; else nothing, noted in the record).

## `docs/ads.md` template

```markdown
# Meta ads

Markets: <market: locale, currency, time zone of the account>.

## Measurement
Datasets: <market: dataset id (public)>. Domain verification: <tag set, verified on <day> | waiting on the click>. Events: PageView, ViewContent (browser, public pages: <paths>); Lead at <moment>, InitiateCheckout at order creation, Purchase at settlement (server). Tokens: <market: dataset token generated on <day> | not yet, events off>. Test: `node scripts/meta/test-event.mjs <market> Lead <code>`.

## Accounts
| Market | Account | Currency | Time zone | Status | Counts from | Page |

## Campaigns
| Campaign | Market | Ad set | Creative | Daily budget | Optimizes | Activated | Paused | Why |

Specs: `scripts/meta/campaigns/*.json`. Create: `node scripts/meta/campaign.mjs <spec> --apply`; activate after the word with `--activate`.

## Rules
<the parameters of src/config/ads.ts in plain words, and the review date>. Review: `node scripts/meta/review.mjs`. Sync: `node scripts/meta/sync-spend.mjs --remote` (the dashboard's cron runs it hourly once it exists); the employee token and the account mapping live in the local secrets file and on the dashboard Worker, never on the public site.

## Operator panel (spec)
Campaign table (spend, impressions, clicks, CTR, CPC, frequency, learning status, site sessions, leads, orders, revenue, cost per order, ROAS on site revenue, Meta's purchases and ROAS beside them), per day and per market; the recommendations with their evidence and an apply button (pause, resume, budget within the step and the cap), confirmed and audited; the attribution funnel by campaign; the integration status (datasets and their last event from the dataset's stats, accounts with currency, time zone and status, the API version with its end date, the day each dataset token was generated as this file records it); the sync's last run and a sync button. The test event is sent from the shell with the script above, not from the panel, which holds no dataset token. A read-only token for the figures; the management token only where the panel changes campaigns.

## Done by a person
<Page and payment method, the domain's Verify click, the dataset tokens, revoking the admin token when the campaign work from this machine ends, with the Business settings paths of the day>
```
