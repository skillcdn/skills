# Monitoring: reading results and deciding changes

How spend and results are read back, bucketed into the business day, cached and joined to the site's own ledger; how a day's numbers are reviewed; and the rules under which an ad set is paused, kept or scaled, with the thresholds the reference operation settled on as defaults. Meta's figures and the site's are two sources: Meta's drive its delivery and are read for the signal (click-through, frequency, learning); the site's (sessions, leads, orders by campaign id, settled revenue) are the money, and the decision is taken on them.

## The insights call

`GET /act_<id>/insights` (or `/<campaign id>/insights`, `/<ad set id>/insights`) with `level` (`campaign`, `adset`, `ad`), `fields`, a window (`date_preset` such as `last_7d` or `time_range={"since":"YYYY-MM-DD","until":"YYYY-MM-DD"}`), `time_increment=1` for one row per day, and `limit`; `paging.next` is followed until it is absent. Fields that monitoring reads: `spend`, `impressions`, `reach`, `frequency`, `inline_link_clicks`, `cpc`, `cpm`, `ctr`, `actions` and `cost_per_action_type` (lists of `{action_type, value}`; the pixel's conversions are `offsite_conversion.fb_pixel_purchase`, `offsite_conversion.fb_pixel_lead`, `offsite_conversion.fb_pixel_initiate_checkout`, and `landing_page_view`, `link_click` are delivery events), `purchase_roas`, `account_currency`, `campaign_id`, `campaign_name`, `adset_id`, `adset_name`, `ad_id`, `ad_name`. `action_attribution_windows` fixes the window (`7d_click`, `1d_view`) so that two reads compare like with like. One purchase action type is summed, never several (`purchase` and `offsite_conversion.fb_pixel_purchase` would double-count). `spend` is before taxes and credits and can differ a few percent from the invoice (checked 2026-10).

## Time zones

Insights days are the ad account's time zone. The business day the dashboard reports in is one zone for every source; when an account's zone has a different day boundary, the call adds `breakdowns=hourly_stats_aggregated_by_advertiser_time_zone`, asks one day wider on each side, and re-buckets each hour row into the business day; the totals equal the daily call's (checked 2026-10 in a run). An account whose zone matches, or whose offset is constant and equal, is read daily. The account's zone comes from `timezone_name` and is shown on the status panel; it cannot be changed after the account is created.

## The spend cache

A table of `day × channel × account × campaign` rows (`spend` in the account currency, the converted amount at the day's rate, `impressions`, `clicks`, the campaign name, the market), written by a sync that replaces the last 14 days per account (Meta corrects figures for a few days) and 120 days when the cache is empty; an account whose read failed keeps its rows and the sync's status says `partial`. A mapping `market:act_<id>[@YYYY-MM-DD]` in a secret names the accounts, their market and the day from which an account counts (its spend before that day is not the project's); without the mapping the sync lists the token's accounts and infers the market from their names, which is why the mapping is recommended. The last run, its window and each account's name, currency, time zone and status are stored for the status panel. The dashboard reads the cache only; the sync runs on the dashboard's cron and on its button.

## The second source

The site's rows carry `campaign_id`, `adset_id`, `ad_id` and the UTM fields from the ad's URL tags ([measurement.md](measurement.md)). Joined to the spend rows by campaign id and day, they give per campaign: sessions, leads (the first meaningful action), checkouts, paid orders, revenue at the order's currency converted at the day's rate, and from those cost per session, cost per lead, cost per paid order, and ROAS on the site's revenue. Opted-out visitors have no ids and are counted apart so that totals reconcile; zero-amount orders and their sessions are excluded. Settled revenue (the payment ledger) is the money across all campaigns and is not attributed per campaign; the panel shows both and says which is which.

## Reviewing a day

The method that finds a cause where it is when a day's revenue falls, in this order:

1. **By market first.** Which market lost: spend, sessions, conversion, revenue per market, against the same weekdays of the previous week (a Thursday to Sunday against the last Thursday to Sunday), not against the previous four days.
2. **Sessions or conversion.** Fewer sessions at the same conversion is a delivery or click problem; the same sessions at a lower conversion is a site or an audience problem.
3. **Creative mix and fatigue.** The share of the day's spend on creatives younger than two days; the click-through rate per ad against its own first days (a drop of a third with a rising frequency is fatigue); a decomposition of the market's click-through change into within-ad change and mix change, because a new creative taking half the budget looks like fatigue of the old ones.
4. **Hour of day.** The hourly breakdown shows whether a day fell everywhere or only in some hours.
5. **Change history.** Budget changes, ad sets turned on and off, new creatives, from the account's activity log (`GET /act_<id>/activities` with a date range lists them with their times), set against the hour the numbers moved.
6. **Not a cause until checked.** A site error, a payment failure or a platform outage is ruled in or out with the site's logs, the payment ledger and the platform's status page before the ads are blamed.

## The rules

Defaults the user changes in the plan; every rule names its evidence window and acts on the site's ledger with Meta's figures next to it. A rule proposes; a person or an explicit setting applies. The first batch of a market is exempt from the mix guard, since nothing else runs there yet; the guard holds from the second batch on.

| Rule | Condition | Action | Why |
|---|---|---|---|
| Kill | Over the last 3 full days an ad set spent at least the larger of 2 times the target cost per paid order and the plan's test spend floor, produced no paid order, and has either left learning or is older than 7 days | Pause the ad set | Spending without a sale past the learning window |
| Hold | A learning ad set, or one younger than 3 full days | Nothing | The numbers are not yet its numbers |
| Fatigue | Click-through rate down 30 percent or more from the ad's first 3 days while frequency rises above 2 | Ask for a new creative; pause when the kill rule also fires | A tired creative costs more per click every day |
| Scale | ROAS on the site's revenue at or above the target over the last 4 full days, spend at or near the budget, learning left | Raise the daily budget by at most 20 percent, once a day; move the creative into the winners' campaign when it holds for a week | More budget on what converts, in steps that do not reset learning |
| Mix guard | From the second batch on, creatives younger than 2 days would take more than half of a market's daily spend | Do not activate more; stagger | Too much of a day's spend on untested creatives can halve a market's conversions in a day |
| New market cap | A market with fewer than 50 paid orders in total | A campaign spend cap at twice the first week's total; weekly review | Meta's attributed ROAS alone misjudges a new market's profit |
| Change window | A budget or creative change | Judge the ad set by profit after the change, over at least 3 full days, not by click-through rate alone | A creative with a low click-through rate can still be the market's best seller |

Several changes to one market on one day are avoided; the review of the next day cannot otherwise tell which one worked. An automated rule, where the operator turns one on, may pause and lower, never raise, and never beyond a daily cap the operator set; every action it takes is written to the audit log with the figures that triggered it.

## Alerts

Daily, in the operator's chat tool: yesterday's spend, sessions, paid orders, revenue, ROAS and net profit per market, against the previous week's same weekday; the ad sets the rules flag; a sync that failed; an ad `WITH_ISSUES`. At once: an account whose status leaves 1 (disabled or unsettled), spend above the day's cap, a dataset that received no event for a day while ads run.
