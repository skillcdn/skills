# Campaigns: the objects and the settings that run

What a campaign is made of in the Marketing API and the settings the reference accounts run with, written as shapes: the objective and the budget level, the ad set's optimization and audience, the creative and its enhancements, the ad, the URL tags that make the site's attribution work, naming, the order of creation, activation, and the changes that send an ad set back into learning. Enum values and limits are the API's as checked in 2026-10; `GET` on an existing object shows the current shape, and the ad set and ad creative references are the source.

## The objects

```
campaign (objective, budget when CBO, status)
  ad set (budget when ABO, optimization event, audience, placements, attribution window, schedule, status)
    ad (creative, status)
      creative (page, video or image, texts, call to action, link, URL tags, enhancements)
```

Every object is created with `status=PAUSED` and the whole tree is activated at once after the user's word; an object created `ACTIVE` would start spending as soon as its parents are active.

## Campaign

`POST /act_<id>/campaigns` with `name`, `objective=OUTCOME_SALES` (a site that sells; `OUTCOME_LEADS` when the goal is a sign-up and nothing is sold yet), `special_ad_categories=[]` (required, empty for ordinary goods; `HOUSING`, `EMPLOYMENT`, `CREDIT`, `FINANCIAL_PRODUCTS_SERVICES` and the others when the law applies), `buying_type=AUCTION` (the default), `status=PAUSED`. The budget sits at one level:

| Level | Shape | Used for |
|---|---|---|
| Ad set budgets (ABO) | No budget on the campaign; `daily_budget` on each ad set | Testing creatives: one ad set per creative, each with the same small budget, so that every creative gets its own spend and a clean read |
| Campaign budget (CBO) | `daily_budget` and `bid_strategy=LOWEST_COST_WITHOUT_CAP` on the campaign, none on the ad sets | Running proven creatives together and letting delivery shift budget to what converts |

The reference accounts run both at once: ABO campaigns named for a market and a test batch, and one or two CBO campaigns per market that hold the winners (observed 2026-10). `spend_cap` on a campaign is the hard ceiling for a new market's first weeks: the plan sets it at twice the first week's total (Meta's minimum is about 100 USD in the account currency; checked 2026-10). `daily_budget` is in the account currency's minor units (whole units for a zero-decimal currency, hundredths otherwise); the account's `min_daily_budget` is the floor.

## Ad set

`POST /act_<id>/adsets` with `campaign_id`, `name`, `status=PAUSED`, `daily_budget` (ABO only), `billing_event=IMPRESSIONS`, `optimization_goal=OFFSITE_CONVERSIONS`, `bid_strategy=LOWEST_COST_WITHOUT_CAP` (no cap: the account's history shows nothing else), `destination_type=WEBSITE`, `promoted_object={"pixel_id":"<dataset id>","custom_event_type":"PURCHASE"}` (`LEAD` until purchases exist, then `PURCHASE` once the site records about fifty a week, which is the volume delivery needs to learn on), `attribution_spec=[{"event_type":"CLICK_THROUGH","window_days":7}]` (the account default; a view-through day is sometimes added), `start_time` now, no `end_time` with a daily budget, and the targeting:

```json
{"geo_locations":{"countries":["<ISO code>"],"location_types":["home","recent"]},
 "age_min":18,"age_max":65,
 "targeting_automation":{"advantage_audience":1}}
```

Broad: the country, the legal age floor, and Advantage+ audience on, which must be stated explicitly on creation since v23.0 (changelog, checked 2026-10); no interests, no custom audiences in the test batch. Placements are automatic when `publisher_platforms` is omitted. `age_min` of 18 to 25 and `age_max` 65 are what the Advantage+ audience accepts as limits it keeps (reference, checked 2026-10). The reference accounts run every ad set on this shape, with a narrower age band only in a few deliberate tests.

Readable fields for monitoring: `effective_status` (`ACTIVE`, `PAUSED`, `CAMPAIGN_PAUSED`, `ADSET_PAUSED`, `WITH_ISSUES`, `IN_PROCESS`), `learning_stage_info` (`status` `LEARNING`, `SUCCESS` or `FAIL`, and `conversions` since the last significant edit; only for active ad sets; checked 2026-10), `daily_budget`, `budget_remaining`.

## Uploading a video and a thumbnail

`POST /act_<id>/advideos` with `file_url` (a public URL of the finished video) or `source` (the file as form data; a large file goes through the chunked phases `start`, `transfer`, `finish` with `upload_session_id`), and `name`; the answer is the video id. Processing takes a minute or more: read the video back (`GET /<video id>?fields=status`) until its status says it is ready (`status.video_status` `ready`); when the field is not returned, a creative created too early answers that the video is still processing, and the creation is retried a minute later. A thumbnail: `POST /act_<id>/adimages` with the still (`bytes` as base64 or `filename`), whose `hash` is the creative's `image_hash`; or `image_url` of a frame the site serves. The video's own `picture` field is a generated thumbnail when nothing better exists.

## Creative

`POST /act_<id>/adcreatives` with `name`, `object_story_spec` and the two extras:

```json
{"page_id":"<page id>","instagram_user_id":"<optional>",
 "video_data":{"video_id":"<video id>","image_hash":"<thumbnail hash>",
   "message":"<primary text>","title":"<headline>",
   "call_to_action":{"type":"LEARN_MORE","value":{"link":"https://<site>/<landing>?<locale parameter>"}}}}
```

An image ad uses `link_data` with `image_hash`, `link`, `message`, `name` (the headline) and the same `call_to_action`. The call-to-action type is one of the API's enum (`LEARN_MORE`, `SIGN_UP`, `SHOP_NOW`, `GET_OFFER`, `SEE_DETAILS` is what the reference ads carry); the allowed set depends on the objective. `url_tags` on the creative adds the attribution parameters to every link click without putting them in the link:

```
utm_source=meta&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&campaign_id={{campaign.id}}&adset_id={{adset.id}}&ad_id={{ad.id}}
```

Meta fills the braces at delivery; the site's attribution reads the ids ([measurement.md](measurement.md)). `degrees_of_freedom_spec` chooses the automatic enhancements, feature by feature: `{"creative_features_spec":{"standard_enhancements":{"enroll_status":"OPT_IN"},"<feature>":{"enroll_status":"OPT_OUT"}}}`. The running accounts opt into `standard_enhancements` and the video's native subtitles (`ig_video_native_subtitle`) and out of everything that rewrites text, crops or regenerates media; the feature keys of the day are the ones a `GET /<creative id>?fields=degrees_of_freedom_spec` on any creative of the account returns, or the ad creative reference lists, and a key omitted from the spec takes the account's default, so a spec that names only `standard_enhancements` and the subtitles is complete (observed 2026-10). A creative whose texts come in several variants is one creative with `asset_feed_spec` (several `bodies`, one `titles`, `optimization_type` `DEGREES_OF_FREEDOM`), which the reference uses for a text test on one video.

## Ad

`POST /act_<id>/ads` with `name`, `adset_id`, `creative={"creative_id":"<id>"}`, `status=PAUSED`. Tracking specs for the dataset are added by Meta from the ad set's promoted object. The ad's `effective_status` and the campaign's `WITH_ISSUES` are where a rejected creative shows; `GET /<ad id>?fields=effective_status,issues_info` names the policy reason.

## Names

`<YYMMDD>-<market>-<creative or angle>` for ad sets and ads (the ad set and its single ad share the name), `<YYMMDD>-<market>-<batch> ABO` or `<market> winners CBO` for campaigns: the date says when it started, the market says which dataset and ledger it belongs to, the creative name joins it to the creative's file. A copy carries the original name and a suffix. The dashboard reads the market from the name's second token when the account mapping has none.

## Order and activation

1. Prove access and read the account's currency, time zone and minimum daily budget; read the dataset id, the Page id and the Instagram account linked to the Page.
2. Upload the videos, wait for `ready`; upload the thumbnails.
3. Campaign, then one ad set per creative, then one creative and one ad per ad set, all paused; `execution_options=["validate_only"]` on a first try validates a body without creating it.
4. Show the plan with the daily total (`ad sets × daily budget`), the first week's spend, the spend cap and the exact objects created; on the word, set `status=ACTIVE` on the ads, then the ad sets, then the campaign. Delivery starts within hours; the first day spends a fraction of the budget.

## What resets learning

An ad set learns on its first conversions and exits learning after about fifty optimization events in a week; a change to targeting, to the optimization event, to the creative, to the bid, or a budget change larger than about 20 percent sends it back into learning and discards what it learned (Meta's guidance as read in the dashboard and in a run's change history, checked 2026-10). A budget is lowered only to at least 10 percent above what was already spent that day (ad set reference, checked 2026-10). The rule the operators keep: raise a budget by at most 20 percent at a time, once a day, and never edit several things of one ad set on the same day.
