# Tool notes: how the tools behaved in this skill's phases

By topic, in the order a run meets them. A fact that can go stale names where it was seen and the month; a fact about how the API works carries no date and changes when a run finds it wrong. What every Meta skill shares is in the pack's Meta Marketing API pages; these are the edges of this skill's own phases.

## Token and access

- A token with `ads_read` alone reads campaigns, ad sets, ads, creatives and insights, but a request for the account's `business` field answers `(#100) Requires business_management permission`; the probe asks for that field only with the admin token (seen 2026-10).
- The token wizard shows no permissions until the system user has the app assigned as an asset, and the app appears in the asset list only when it belongs to the business portfolio; both are dashboard steps the person takes (seen 2026-09).
- A system user that created a dataset can send events to it without a further grant, which is how a setup script proves a dataset before the person generated its own token; the Worker still gets only the dataset's token (seen 2026-09).
- A Graph call accepts the token in the `Authorization: Bearer` header as well as in the query; the header form keeps it out of logged URLs and error messages.

## Datasets and the domain

- `POST /act_<id>/adspixels` on an account that has one answers error 6200; the existing one is read and renamed instead. Setting `enable_automatic_matching=false` and the first-party cookie on through `POST /<pixel id>` worked; `POST /<pixel id>/assigned_users` is undocumented and may fail, and the dashboard path is given then (seen 2026-09).
- A `workers.dev` address cannot be verified as the business's domain; the ads run with Meta's warning until a custom domain is attached and verified.
- `POST /<pixel id>/shared_accounts` with `account_id` and `business` shares a dataset with another ad account of the same business, keeping the dataset id, the token and the event history; a mapping entry with an `@<day>` start counts that account's spend from that day only.
- The domain verification tag is published in the head and the person clicks Verify; a deploy that goes out before the click is fine, since the tag is harmless until verified.

## Events

- Events sent with a `test_event_code` appear only in Events Manager's test tab within a minute and are not used for delivery; a code left in the Worker's secrets after verification routes every live event there, which the operator panel flags in red (seen 2026-09).
- `events_received: 1` is the whole success answer; a 400 with `(#100) Invalid parameter` named a `user_data` value that was not hashed, and a 190 an expired or revoked token.
- Meta's automatic URL parameters, when an ad's tracking field is left empty, arrive as `utm_source=fb|ig|msg|an`, `utm_medium=paid`, `utm_campaign=<campaign id>`, `utm_term=<ad set id>`, `utm_content=<ad id>`; the attribution module recognizes numeric ids in those fields (seen 2026-10).

## Campaigns

- Ad sets created without `targeting_automation.advantage_audience` set explicitly fail on v23.0 and later; the recipe always sends `1` or `0` (changelog, checked 2026-10).
- `special_ad_categories` is required on campaign creation even as an empty list.
- Every account surveyed ran `billing_event=IMPRESSIONS`, `optimization_goal=OFFSITE_CONVERSIONS`, `bid_strategy=LOWEST_COST_WITHOUT_CAP` and a 7-day click attribution on every ad set; daily budgets per ad set in a test batch sat at two to twenty times the account's minimum, and the winners' campaigns carried a campaign budget of five to twenty times a test ad set's (observed 2026-10).
- A video creative needs a thumbnail: the reference creatives carried an `image_hash`; without one the creation answered an error naming the image (seen 2026-09).
- `SEE_DETAILS` is the call to action on the surveyed ads; the enum the reference lists for the sales objective includes `LEARN_MORE`, `SHOP_NOW`, `SIGN_UP` and `GET_OFFER`, and an unsupported type for the objective answers an error naming the allowed set.
- The first day after activation spent a few percent of the daily budget; delivery ramped over the next days (seen 2026-10).

## Insights and sync

- The hourly breakdown's totals equal the daily call's for the same window, which is what makes re-bucketing into the business day safe (checked 2026-10).
- An account whose `account_status` is not 1 still answers insights for its past days, so it stays in the mapping until its spend correction window has passed.
- The `spend` field is before taxes and credits; the invoice differs by a few percent.
- The ad account's `activities` edge lists budget and status changes with their times, which is how a day's change history is read (seen 2026-09).
