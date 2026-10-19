# Meta Marketing API skills

How the skills that connect a site to Meta ads and run them (`meta-ads-setup`, and the ads panel of `cloudflare-admin-dashboard`) are written and kept in step, for authors. What they share at run time is the document set [`engineering/docs/meta-marketing-api/`](../../engineering/docs/meta-marketing-api/README.md), which agents read; this page says what goes there, what stays in a skill, and how the family is tested. The Meta Ad Library, the public website the marketing skills read, is another family with its own set and its own page.

## The tool is the Graph API and the business's dashboards

The skills drive the Marketing API through `fetch` in Node scripts and in the Worker, with a system user's token the user creates in Business settings; the few steps the API does not offer (the business, the app, the system user, the Page, the payment method, the domain's Verify click, the dataset's own token) are the person's, given as the dashboard paths of the day. Endpoints, fields and enum values are named exactly; menu names, defaults that changed (Advantage+ audience required on creation), version end dates and limits carry the month they were checked, because the API's versions live about a year and the dashboards move faster. Budgets, minimums, currencies and time zones are never written as facts: the account answers them at run time.

## What is shared and what stays in the skill

| In `engineering/docs/meta-marketing-api/` | In the skill |
|---|---|
| `access.md`: the pieces, the access tiers, the system user and the token, the dataset's token, the version, the probe | What the skill asks the user for and when |
| `measurement.md`: the dataset, the domain, the pixel's rules, the Conversions API, attribution, privacy signals, one dataset per market | The code the skill writes (`references/wiring.md`) and its tests |
| `campaigns.md`: the objects and the settings a working account runs, uploads, creation order, activation, what resets learning | The campaign recipe (`references/campaign.md`): the spec, the script, the estimate, the stop |
| `monitoring.md`: the insights call, time zones, the spend cache, the second source, the review method, the rules and their reasons | The parameters, the sync and review scripts, the panel spec (`references/optimization.md`) |

The test for a sentence: would it be true for the next skill of the family (a marketing-only skill that runs a campaign on an account already wired, a skill that reads a weekly report)? Then it belongs in the set. A sentence about one skill's phase stays in that skill; how the API behaved in that phase goes in its `references/tool-notes.md`.

The set sits in the area's `docs/` because every skill of the family is an engineering skill today; when a marketing skill joins the family, the set moves to the root `docs/` as the Higgsfield set did, with the root-relative links unchanged in meaning. The ads skill includes `access.md` and `measurement.md`; the admin skill links `campaigns.md` and `monitoring.md`. A change to an included page changes the served digest of the ads skill: edit deliberately.

## The seams

`meta-ads-setup` attaches to the hooks of `stripe-payments` for the checkout and purchase events and the attribution metadata, and says what to do when the payments module is absent; it takes a finished creative from `higgsfield-shorts-ad` or any file the user gives, and says what a creative must be when there is none. It writes `docs/ads.md` with the panel's spec, which the admin skill reads. A change to the rules' defaults is made in `monitoring.md` (the reasons) and `references/optimization.md` (the parameters) together.

## Examples name no one

Accounts, datasets, Pages, campaigns and creatives are placeholders (`act_<id>`, `<dataset id>`, `hook-a`); what the reference accounts' structure taught is written as shapes and ranges ("daily budgets per ad set at two to twenty times the account's minimum"), never as names, products or amounts spent; what their operators' analyses taught is written as rules with their reasons.

## Testing

The ads skill is exercised by a fresh agent wiring a stand-in project (phases 1 to 3 cost nothing and need no account), then, with a business the user lends, creating the datasets and sending a test event (no spend), then building a campaign from a stand-in creative to the activation checkpoint, left unanswered, so that nothing is spent; a run that activates is a spend the user confirms with its daily total. The admin's ads panel is exercised against the same account's insights. A change to either skill is dry-read before it is pushed; a run is read against the files as `skillcdn-skill-verification` says.
