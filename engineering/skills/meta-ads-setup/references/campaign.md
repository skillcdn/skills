# The campaign recipe

How finished creatives become running ads, in the shape a working account runs them: the spec the agent writes from the plan, the script that creates the objects paused, the estimate, the activation, the record, and what a creative must be when the user has none. The objects and their settings are in [campaigns.md](/engineering/docs/meta-marketing-api/campaigns.md); this page is the order and the choices. Every call carries the admin token from `.meta-token` in the `Authorization` header, read by path, never on a Worker.

## The spec

`scripts/meta/campaigns/<YYMMDD>-<market>-<batch>.json`, in the shape of [campaign.example.json](../assets/campaign.example.json): the market and its ad account, dataset and Page (and the Instagram account linked to the Page, when there is one); the landing URL with the locale parameter the site uses; the objective (`OUTCOME_SALES` when the site sells, `OUTCOME_LEADS` before); the optimization event, chosen by what the site's own ledger counts over the last seven days (`PURCHASE` from about fifty paid orders a week; `INITIATED_CHECKOUT` from about fifty checkouts a week while paid orders are under ten; `LEAD` until then; the counts come from the orders table by `status` and `created_at`, excluding zero-amount orders, and the plan says which it chose and why); the daily budget per ad set in the account's currency; the campaign's spend cap (twice the first week's total, in minor units); the audience (country, `age_min` 18 unless the product requires more, `age_max` 65, Advantage+ audience on); the attribution window (7-day click); the enhancements (standard enhancements and the video's native subtitles on, everything else at the account's default, which is off); the creatives, each with its file path or URL, thumbnail, name, primary text (a few sentences in the market's language), headline, call to action (`LEARN_MORE` by default, which fits a paid digital service; `SIGN_UP` for a lead site; `SHOP_NOW` for goods), and `textVariants` when several primary texts test one video. The spec is committed; it is the record of what was created.

## The script

`scripts/meta/campaign.mjs <spec> [--apply] [--activate]`, run with the token from `.meta-token` read by path:

1. Probe: the account's currency, time zone, status and `min_daily_budget`; refuse a budget below the minimum; the dataset and the Page exist and are assigned.
2. Validate: every body with `execution_options=["validate_only"]` first; a validation error names the field and stops the run before anything is created.
3. Upload: each video with `POST /act_<id>/advideos` (`file_url` when the site serves the file publicly, else `source` from the file; a file over about 100 MB in the chunked phases), then read each video back until its status says it is ready (`status.video_status` `ready`), retrying a creative that answers "still processing" a minute later; each thumbnail with `POST /act_<id>/adimages` (a still the user gave, else the video's own `picture` URL as `image_url`); a creative that already has a video id in the spec skips the upload.
4. Create, all `PAUSED`: the campaign (ABO: no budget on it, `spend_cap` from the spec; the winners' campaign: `daily_budget` and `bid_strategy`), one ad set per creative with the budget, the optimization, the audience and the window, one creative per ad set with `object_story_spec`, `url_tags` and `degrees_of_freedom_spec`, one ad per ad set. Names `<YYMMDD>-<market>-<creative name>`.
5. Print the plan: the objects with their ids, the daily total (`ad sets × daily budget`), the first week's spend (`daily total × 7`), the cap, the optimization event and the audience; write them into the spec's `created` block and into `docs/ads.md` "Campaigns".
6. `--activate`, only after the user's word: `status=ACTIVE` on the ads, then the ad sets, then the campaign; record the time.

Without `--apply` the script stops after validation and prints what it would create, which is what the plan checkpoint shows when the user wants to see the exact objects first.

## The estimate and the stop

The checkpoint message names the exact numbers from the spec and the account: "Created paused: <campaign> with <n> ad sets at <budget> <currency> a day each, <daily total> a day, about <week total> this week, capped at <cap>, optimizing for <event> in <country>, 18 to 65, automatic placements. Turn them on?" Delivery starts within hours of activation and the first day spends a fraction of the budget; the first review is three full days later, and the plan's weekly total is what the operator watches on the panel against the cap.

## Winners

An ad set that meets the scale rule of [monitoring.md](/engineering/docs/meta-marketing-api/monitoring.md) for a week is duplicated into the market's winners' campaign (a CBO campaign with `daily_budget` at the sum of the winners' budgets, `bid_strategy=LOWEST_COST_WITHOUT_CAP`, created once per market) by creating a new ad set and ad there from the same creative id, and the test ad set is paused a day later when the copy delivers. The winners' campaign is raised by at most 20 percent a day, with the user's word each time.

## Refreshing creatives

A new creative enters as a new ad set in the current test campaign (a new spec file with one creative, the same budget), never by swapping the creative of a running ad set, which would reset its learning and lose its history. The mix guard holds from the second batch on: when the new ad sets would take more than half of the market's daily spend, they are staggered over days.

## When there is no creative

Phase 5 ends with the brief for one: a vertical video (9:16, up to 60 seconds, MP4, with burned-in captions since most feeds play muted; a square or landscape video is accepted and fits fewer placements) or a square or vertical image, a primary text of two to four sentences in the market's language that says what the visitor gets and asks them to try it, a headline of a few words, and a landing page that loads in under three seconds on a phone and shows the lead moment above the fold. `higgsfield-shorts-ad` makes such a video from the product's link and a reference ad; the delivery names it and says to run this skill again with the files, which starts at phase 5.

## What the record holds

`docs/ads.md` "Campaigns": one row per ad set with the campaign, the market, the creative name, the daily budget, the optimization event, the day activated, the day paused and why, and the ids; the spec files are the detail. The panel reads the same table and adds the live figures.
