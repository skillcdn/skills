# Access: the business, the app, the system users and their tokens

How an agent gets to read and change a business's ads and how a site gets to send its events: the pieces a business must have, the app and its access tier, the system user whose token the agent uses on the machine, the narrow tokens that go on Workers, how a call carries a token, where tokens are kept and when they are revoked, the API version and how fast it ages, and the read-only calls that prove access before anything is made. Menu names are the dashboard's of the month they were checked and are given to the user in the dashboard's language with the English in parentheses; the Marketing API documentation and the Business Help Center are the source of the current ones.

## The pieces

| Piece | What it is | Who makes it |
|---|---|---|
| Business portfolio | The container that owns ad accounts, Pages, datasets and the app; `business.facebook.com` | A person, once; most advertisers already have one |
| Ad account | Where campaigns live and are billed; has a currency and a time zone that cannot be changed after creation, and a payment method | A person in Business settings > Accounts > Ad accounts; the time zone is chosen to match the business day the dashboard reports in |
| Page | The Facebook Page the ads are shown from (`page_id` of every creative); an Instagram account can be linked to it | A person; the business must own or be assigned the Page |
| Dataset (pixel) | Receives the site's events; one per ad account can be created through the API, and a dataset is a business asset that several ad accounts can share | The agent ([measurement.md](measurement.md)) |
| App | A Meta app of type Business linked to the portfolio, with the Marketing API product added; needed only to mint system user tokens | A person at `developers.facebook.com/apps` > Create app > type Business > the portfolio, then Add product > Marketing API (checked 2026-10), once |
| System users | Server identities inside the business with their own long-lived tokens: one admin for the agent's setup and campaign work, one employee for a dashboard, whose tokens carry `ads_read` alone or, for a dashboard that steers campaigns, `ads_management` alone | A person in Business settings; the agent uses their tokens |

## Access tiers

An app with the Marketing API product has Limited Access by default (renamed from Standard Access; checked 2026-10): it may manage any number of the business's own ad accounts, with heavy rate limits per account, one system user and one admin system user, and it is meant for development and for a business operating its own accounts. Full Access (renamed from Advanced Access) needs App Review and is for apps that serve other advertisers at scale; a business running its own ads never needs it (authorization page, checked 2026-10). The rate limit matters only for bulk reads: an hourly sync of a few accounts stays far below it.

## Three tokens, three holders

| Token | Made by | Held by | May do |
|---|---|---|---|
| The admin system user's token (`.meta-token`) | The person, below | The agent, on the machine, while it sets up and runs campaigns; never a Worker secret | Create datasets, upload creatives, create and change campaigns, read insights |
| A dataset's own token (`META_CAPI_ACCESS_TOKEN`, one per market) | The person: Events Manager > the dataset > Settings > Conversions API > Generate access token (checked 2026-10) | The public site's Worker | Send events to that one dataset and nothing else |
| The employee system user's token (`META_ADS_ACCESS_TOKEN`) | The person, below, with `ads_read` only and View performance on the accounts | The operator's dashboard Worker, and the spend sync script on the machine until that dashboard exists | Read insights and campaign status; a dashboard that also pauses and re-budgets holds a separate `META_ADS_MANAGE_TOKEN`, generated on the same employee user (given Manage campaigns on the accounts) with `ads_management` alone, since Limited Access allows one employee system user and a token's permissions bound what it can do |

A site whose market has no dataset token sends nothing for that market; the admin token is never used as a fallback, because a compromised public site would then hold the business's ad accounts.

## The system users and their tokens

Business settings > Users > System users > Add: a name for the project and the role, Admin for the agent's user, Employee for the dashboard's (checked 2026-10 in the dashboard). Then Add assets: for the admin user every ad account the project uses (Manage campaigns), the Page (Create content) and the app (Develop app); for the employee user the ad accounts (View performance) and the app. Then Generate new token: choose the app, an expiry of 60 days for the admin user (generated again when the campaign work goes on longer; a token that never expires only on the user's explicit word), and the permissions `ads_management`, `ads_read` and `pages_manage_ads` for the admin user, with `business_management` only on the token that creates and shares the datasets (a token generated for the campaign months leaves it out), and `ads_read` alone for the employee user (checked 2026-10). The token is shown once.

Two things block the token wizard and are solved in the dashboard: "No permissions available" means the system user has not been assigned the app (Add assets > Apps); an app missing from the asset list means the app is not in the portfolio (create a new Business app from the portfolio, or claim the existing one under Business settings > Accounts > Apps).

## Where a token lives, how a call carries it

`.meta-token` in the project root holds the admin token, one line; the agent adds it to `.gitignore` and to the host's read-deny list (`.claude/settings.json` when the project has one) before asking for it, reads it into the environment for its own calls (`META_ACCESS_TOKEN` in scripts) and never prints it. The dataset tokens and the employee token reach the Workers through the deploy skill's secrets path. Every call sends the token in the `Authorization: Bearer <token>` header, never as the `access_token` query parameter, so that no log, trace or error message carries it in a URL; a script logs the path of a failed call and never its full URL or the raw error object. When the campaign work from this machine ends, the person revokes the admin token (the agent sends `DELETE /me/permissions` with the token, and a probe call must then answer error 190; when it still answers, the person removes the app from the system user's assets or removes the user in Business settings; generating a new token is not relied on to end the old one) and the file is deleted; the delivery says so.

## The API version

Requests name a version in the path (`https://graph.facebook.com/v26.0/...`). The Marketing API's versions live about a year while Graph API versions live two: v24.0 ended on 2026-10-06, v25.0 and v26.0 (released 2026-07-29) were current with end dates to be announced, and an automatic upgrade of Marketing API versions started on 2026-07-29 (changelog, checked 2026-10). Every response carries the version it ran on in the `facebook-api-version` header, and a call to a retired version answers an error naming the oldest version still served. The code keeps the version in one configuration value with a secret override, and the dashboard's status panel shows it next to the changelog's end date; a sync that answers "version deprecated" is the signal to raise it.

## Proving access, read-only

Before anything is created, a few calls prove the token and show the shape of what exists:

- `GET /me?fields=id,name`: the system user the token belongs to; `GET /me/permissions` lists what the token was granted, where the token type allows it, and otherwise the errors below name what is missing.
- `GET /me/adaccounts?fields=id,name,currency,timezone_name,account_status,amount_spent,min_daily_budget&limit=50`: the ad accounts the token sees, with `account_status` 1 active, 2 disabled, 3 unsettled, 7 to 9 in review or grace, 100 and 101 closed; `min_daily_budget` is the smallest daily budget the account accepts, in its currency's minor units; `timezone_name` decides how spend is bucketed ([monitoring.md](monitoring.md)). The account of a market is the one whose currency is the market's; when several match, the one whose name carries the market or the project, else the user chooses from the list.
- `GET /act_<id>/adspixels?fields=id,name,enable_automatic_matching,first_party_cookie_status,last_fired_time`: the dataset the campaign needs.
- `GET /me/accounts?fields=id,name,instagram_business_account`: the Pages; the Page of a project is the one named like the site, else the user chooses; `instagram_business_account.id` is the Instagram account linked to it, used as the creative's `instagram_user_id` when present.

A `(#100) Requires business_management permission` on a field such as the account's `business` names the permission to add; a `(#200)` names an asset the system user was not assigned; a `190` is an expired or revoked token. These answers are the diagnosis to give the person, with the dashboard path above.
