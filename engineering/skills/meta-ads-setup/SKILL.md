---
name: meta-ads-setup
description: Connects a web project to Meta ads and runs them end to end, with the agent doing every step a token allows. Wires the measurement first (a dataset per market, the pixel on public pages only, the Conversions API for leads, checkouts and purchases with deduplication, attribution from the first click to the order, privacy signals honored), creates the datasets and the domain's verification with the business's system user token, maps the ad accounts and syncs spend, builds campaigns from finished creatives in the shape a working account runs them, created paused and turned on only after the budget is confirmed, and writes the monitoring and optimization rules the operator panel applies. Use when the user says to connect Meta ads, add the pixel or the Conversions API, run a Facebook or Instagram campaign, put a creative on Meta, or set up ad tracking. Making the creative is higgsfield-shorts-ad; the screens that steer the campaigns are cloudflare-admin-dashboard.
license: MIT
compatibility: Needs a shell with Node.js, npm, git and curl in a checkout of the project, network access to graph.facebook.com, a Meta business portfolio with an ad account, a Page and the system user tokens the user creates, the project deployed with cloudflare-deploy (its address, its token file) for the live events and the domain, and finished creative files for the campaign phase. Works in any agent that can run a shell and write files.
metadata:
  author: skillcdn
  version: "1.1"
  tools: meta-marketing-api
skillcdn:
  include:
    - references/wiring.md
    - /engineering/docs/meta-marketing-api/access.md
    - /engineering/docs/meta-marketing-api/measurement.md
  translations:
    ko:
      title: Meta 광고 연동과 캠페인 운영
      description: 웹 프로젝트를 Meta 광고에 연결하고 광고를 돌립니다. 토큰으로 할 수 있는 일은 에이전트가 전부 합니다. 먼저 측정을 배선하고(시장별 데이터 세트, 공개 화면에만 도는 픽셀, 리드·결제 시작·구매를 보내는 전환 API와 중복 제거, 첫 클릭에서 주문까지 이어지는 어트리뷰션, 개인정보 신호 존중), 비즈니스의 시스템 사용자 토큰으로 데이터 세트와 도메인 인증을 준비하고, 광고 계정을 매핑해 광고비를 동기화한 뒤, 완성된 소재로 실제 운영 계정이 쓰는 방식대로 캠페인을 만들어 일시중지 상태로 두고 예산을 확인받은 뒤에만 켜며, 운영 패널이 적용할 모니터링·최적화 규칙을 적습니다. Meta 광고 연동해 달라, 픽셀이나 전환 API 붙여 달라, 페이스북·인스타그램 캠페인 돌려 달라, 소재를 Meta에 올려 달라, 광고 추적 세팅해 달라고 할 때 쓰세요. 소재 제작은 higgsfield-shorts-ad, 캠페인을 보고 조정하는 화면은 cloudflare-admin-dashboard가 맡습니다.
---
# Meta ads for a web project, from the pixel to running campaigns

What goes in: a project in a checkout with a live address, a Meta business portfolio with an ad account and a Page, the tokens the user creates, the markets the site sells in, the moments on the site that count as a lead and a sale, and, for the campaign phase, finished creatives and a daily budget. What comes out: the site measuring what the ads bring without sending anything private (a dataset per market, the pixel on public pages, the Conversions API for the rest, attribution from the first click to the order), the datasets, the domain's verification and the ad account mapping in place, the spend synced into the project's database, campaigns built from the creatives in the shape a working account runs them and turned on only after the user confirmed the budget, the rules by which they are watched and changed, and `docs/ads.md` saying what exists and what the operator panel shows. The user never needs to know Ads Manager: every setting is derived from their answers, shown with its reason, and changed when they ask.

## How the user is involved

- **Questions:** one message at the start, written under "Inputs": the token, the markets, the lead moment, the creatives at hand and the budget. The dataset tokens, the domain's tag and the test event code are asked when their phase comes, each with its steps. Everything else is derived and shown in the plan.
- **Checkpoints:** the plan, before any file is written or anything created on Meta; every activation, with the daily total and the first week's spend, because turning an ad on spends money; every budget increase; every deploy and push, which follow the deploy skill's stops and the repository's agreement. One short message each, with a recommendation, and one word continues. The files wiring.md names land after the plan's word, each shown as it lands; an edit the plan did not name waits for a word.
- **Go-ahead:** when the user says to go ahead alone, the reports between phases need no answer. Spend is confirmed in every mode: an activation, a budget increase, a new campaign; so are the deploys and pushes.
- **Changes mid-run:** applied from that point. An object already created on Meta is kept and recorded, never silently deleted; an ad set that must stop is paused.

## Requirements

| What | Used for |
|---|---|
| A shell with Node.js (the project's major), npm, git and curl, in a checkout with `node_modules` installed | The code, the setup and campaign scripts, the checks |
| The business's admin system user token ([access.md](/engineering/docs/meta-marketing-api/access.md)), saved in `.meta-token` in the project folder | Reading the accounts, creating the datasets, uploading creatives, creating and changing campaigns, reading insights; it never goes on a Worker |
| Network access to `graph.facebook.com` | All of it |
| The project deployed by `cloudflare-deploy`, with its `DEPLOY.md` and its `.cf-token` | The domain's verification tag and the dataset ids reach the live site through its deploys; the dataset tokens through the Worker's secrets; the migration through the remote database |
| An ad account with a payment method and a Page in the business, both assigned to the system user | A campaign's home and its sender; the person does these in Business settings |
| Finished creatives: vertical videos or images, with their primary text and headline, or none yet | The campaign phase; without one, the phase waits and the delivery names the skill that makes one |

Check these before the first message. Without a token, give the steps of access.md and wait; the measurement phases need only the project and run first. Without a deployed address, wire the code and stop before phase 4: the domain cannot be verified and events of a local server are not sent.

The Meta skills share the area's document set [`engineering/docs/meta-marketing-api/`](/engineering/docs/meta-marketing-api/README.md): [access.md](/engineering/docs/meta-marketing-api/access.md) (the business, the app, the system users and their tokens, the API version, the read-only probe) and [measurement.md](/engineering/docs/meta-marketing-api/measurement.md) (the dataset, the pixel's rules, the Conversions API, attribution, privacy signals, one dataset per market) are included and arrive with this skill wherever SkillCDN serves it; [campaigns.md](/engineering/docs/meta-marketing-api/campaigns.md) (the objects and the settings that run) is linked from phase 5 and [monitoring.md](/engineering/docs/meta-marketing-api/monitoring.md) (insights, the spend cache, the review method, the rules) from phase 6, and the Cloudflare page [automation.md](/engineering/docs/cloudflare/automation.md) (the Worker's secrets, the deploy status) from phase 4, all read with `read_repo_file` through the repository or engineering connection, from the engineering plugin's `docs/`, or from a checkout of this repository. A mount of this skill alone lacks the linked pages and a copy of its directory lacks the included ones too: say so in the first message, fetch them from `engineering/docs/` of the repository this skill comes from (`github.com/skillcdn/skills` for this pack) where the agent can, and otherwise run on this skill's own files, which carry the workflow and the rules. The code is [wiring.md](references/wiring.md), included; the campaign recipe is [campaign.md](references/campaign.md), the rules and the sync are [optimization.md](references/optimization.md), and what the tools did in runs is [tool-notes.md](references/tool-notes.md).

## Inputs

| Input | Source |
|---|---|
| The project | The current directory, or the path the user names: its locale table and currency per market, its public and private routes, the row that marks a visitor's first meaningful action, the payments module's hooks when `stripe-payments` ran (an order's creation and settlement are the checkout and purchase events), its deploy record, `docs/brief.md` |
| The token | Asked: the admin system user token in `.meta-token` (access.md), or the user's word that the business has none yet, in which case the measurement is wired with empty dataset ids and the rest waits |
| Markets | Derived from the project's locales and currencies, confirmed in the plan: one dataset and one ad account per market that will advertise; the account of a market is chosen as access.md "Proving access" says |
| The lead moment | Asked when the project does not make it obvious: the first thing a visitor does that shows intent (submits a form, starts an item, signs up), which becomes the `Lead` event and the first optimization target |
| Creatives | Asked: the files at hand (vertical video or image; a square or landscape video is accepted), each with its primary text and headline, and the landing page; or none yet |
| Budget | Asked for the campaign phase: the daily budget per ad set and the total the user is willing to spend in the first week, in the ad account's currency (an amount the user gives in another currency is converted at the day's rate and shown); the target cost per paid order, else derived as a third of the product's price |
| The business time zone | Derived from the project's configuration (the operator's zone, else the market's), confirmed in the plan: the day boundary of every figure |
| Everything else | Derived and shown in the plan: the dataset names, the public paths where the pixel runs, the consent mode per market (consent-first where the law requires prior consent, opt-out elsewhere), the events and their ids, the attribution fields and the URL tags, the account mapping with each account's currency and time zone, the Page and the Instagram account, the campaign's shape with its spend cap, the optimization event and how it is counted, the rules' thresholds, what the operator panel shows |

The questions, in one message at the start, each only when the request, the brief or the project does not answer it:

- "To work on your Meta ads I need a token from your business portfolio. It takes a few minutes: [the app step of access.md 'The pieces' when the business has no app, then 'The system users and their tokens' for the admin user, with the assets to assign]. Save it as one line in a file named `.meta-token` in the project folder and tell me; that keeps it out of this chat."
- "Which countries will you advertise in? I will set up one measurement set and one ad account per country. The site's languages suggest <markets>."
- "What is the first thing a visitor does on your site that shows real interest (fills in the form, starts an item, signs up)? That becomes the 'lead' the ads learn from until purchases are frequent."
- "Do you already have ad creatives (vertical videos or images) with their text? Send the files and the text for each, or say 'none yet' and I set up everything except the campaign; `higgsfield-shorts-ad` makes a creative from your product."
- "How much per day per creative should a test spend, and how much in total for the first week? I suggest <amount>; I check it against the account's minimum once I can read the account."

When their phase comes: "For each market, open Events Manager > the data set > Settings > Conversions API > Generate access token, and save it in `<the local secrets file>` as `META_CAPI_ACCESS_TOKEN<market suffix>`; tell me when done." "In Business settings > Brand safety and suitability > Domains, add <domain> with the Meta-tag method and send me the `content` value it shows; after my deploy, press Verify there." "Open Events Manager > the data set > Test events and send me the code it shows (it starts with TEST)."

## Workflow

Each phase produces a named artifact and ends with one line to the user. Nothing is turned on before phase 5's word.

### Phase 1: Access

Produces the **access record**: the token's owner and permissions, the ad accounts with their currency, time zone, status, spend so far and minimum daily budget, the Pages and their Instagram accounts, the datasets that exist, from the read-only probe of access.md; first, as shown changes, `.meta-token` joins `.gitignore` and the host's read-deny list. A missing asset or permission is reported now with the Business settings path, not at the step that fails. Without a token, record "none" and continue with phase 2 and 3; the account and campaign parts of the plan are shown again when the token arrives.

### Phase 2: Plan

Produces the **ads plan**, shown at the checkpoint: the markets and their datasets and accounts; the public paths where the pixel runs and the private ones where only the server speaks; the consent mode per market; the events (`PageView`, `ViewContent` from the browser; `Lead`, `InitiateCheckout`, `Purchase` from the server) with where each fires and what each carries; the attribution fields and the URL tags; what will be created on Meta (datasets, their settings) and what the person adds (the domain, the dataset tokens); the campaign's shape when creatives exist (campaign.md), with the daily total, the first week's spend, the spend cap and the optimization event; the rules and their thresholds (optimization.md); the time zone; what the operator panel will show. Then stop: "Here is the plan. **Markets:** <list>, one measurement set and one ad account each. **Measures:** page views on public pages, and leads, checkouts and purchases from the server, with nothing private. **I create on Meta:** <n> datasets; you add the domain and generate one token per set when I say (I give the clicks). **Campaign:** <n> creatives, each its own ad set at <budget> a day, optimizing for <event>, in <country>, aged 18 to 65; <daily total> a day, about <week total> in the first week, capped at <cap>, turned on only when you say. **Rules:** pause after <amount> with no sale, raise winners by 20 percent a day, never more than half the spend on new creatives once the first batch runs. **You will do:** the token (now), the Page and payment method if missing, the domain and the tokens (one click each), the deploys I ask for. OK?"

### Phase 3: Wire

Produces the **measurement code**, as [wiring.md](references/wiring.md) says, each file shown as it lands: the analytics configuration (dataset ids per market, public paths, the verification tag, the API version), the pixel loader in the public layout, the attribution module and its cookie, the server events module, the columns on the visitor's row, the hooks into the payments module, the lead event at the lead moment, the privacy switch, the privacy policy's paragraph, the test event script, the tests. `npm run check` passes, the phase ends with a commit, and the code reaches the live site through the project's deploy path (the migration applied to the remote database first, the push after the word, as `DEPLOY.md` says). With no dataset ids yet the code is complete and silent.

### Phase 4: Accounts

Produces the **account record** and the first `docs/ads.md`: per market the dataset created or found and set as measurement.md says (automatic matching off, first-party cookie on), the dataset ids written into the configuration (public values) and deployed; the domain added by the person with its tag value written into the configuration and deployed, then the person's Verify click (a `workers.dev` address skips this and the record says why); the dataset's own token per market, generated by the person, into the Worker's secrets as [automation.md](/engineering/docs/cloudflare/automation.md) "Secrets" says, with the deploy status checked after a CLI secret change; the account mapping (`<market>:act_<id>`) and the employee token into the local secrets file for the spend sync (and later the dashboard's), never on the public Worker; a test event per market with the person's test event code set as a secret for the test and deleted afterwards, answered with `events_received` 1 and seen in the dataset's `stats`.

### Phase 5: Campaign

Produces the **campaign record**, as [campaign.md](references/campaign.md) and [campaigns.md](/engineering/docs/meta-marketing-api/campaigns.md) say: the creatives uploaded and ready, the campaign with its spend cap, one ad set per creative, one creative and one ad each, all paused, named by date, market and creative, with the URL tags and the enhancements the plan chose; then the checkpoint with the exact objects and the estimate: "Created paused: <campaign> with <n> ad sets at <budget> a day each, <daily total> a day, about <week total> this week, capped at <cap>, optimizing for <event> in <country>. Turn them on?" On the word, activate in order and record the ids, the budgets and the time in `docs/ads.md`. Without creatives, the phase ends with what a creative must be (vertical video or image, the texts, the landing) and the skill that makes one.

### Phase 6: Monitor and optimize

Produces the rest of **`docs/ads.md`** and the **sync and review code**, as [optimization.md](references/optimization.md) and [monitoring.md](/engineering/docs/meta-marketing-api/monitoring.md) say: the spend table and its sync script, the join to the site's rows, the rules' parameters with the thresholds the plan fixed, the review module and its script, the actions with their log, the panel spec, the alert list, and the first review date (three full days after activation). When the project has an operator dashboard (`admin/` from `cloudflare-admin-dashboard`), add the ads panel as that project's `docs/admin.md` says and connect the sync to its cron; otherwise the delivery says the dashboard skill will build it from `docs/ads.md`, and the sync script runs by hand until then. Commit as the repository's agreement says.

### Phase 7: Delivery

One message: what the site now measures and how to see it (Events Manager, the test event), the datasets and accounts, the campaign and its budget and when its first review is, the rules in plain words, what the person still owes (the domain click, a token, the Page or payment method, revoking the admin token when the campaign work from this machine ends), what was verified and what was not, and how the operator sees and steers the campaigns.

### Verdicts

| Result | Verdict |
|---|---|
| A test event per market is received; a real lead, checkout and purchase count in the dataset's stats as server events with no private field; a private page's HTML carries no pixel script; an opted-out visitor sends nothing; `npm run check` passes; the campaign's objects exist paused with the plan's settings and are active only after the word | Accepted |
| Measurement works but the domain waits on the person or on a custom domain, a market's dataset token is not yet generated, or there are no creatives yet | Accepted with the gap named in `docs/ads.md` and the delivery |
| A private value reaches Meta, an event goes to another market's dataset, the admin token is set on a Worker, an ad is active without the word, a zero-amount order is sent as a purchase | Redone before anything is committed or left running |

## Hard rules

1. The admin token stays on the machine and out of the repository, the logs and the agent's own words: read from its file into the environment, sent in a header and never in a URL, never set on a Worker, revoked by the user when the campaign work from this machine ends. A leak means revoking it in Business settings, which the user is told at once.
2. Nothing is turned on without the budget in front of the user and their word: a campaign is created paused with a spend cap, an activation and a budget increase are confirmed in every mode, and an automated rule may pause and lower but never raise.
3. Nothing private goes to Meta: no name, nothing typed into a form, no content the visitor made or received, no page URL with a bearer key and no field that carries one (an event id is never the key of a private page); a zero-amount order and an opted-out visitor send nothing, and in a consent-first market nothing is sent before the visitor opts in; what is sent is listed in the privacy policy.
4. One dataset per market, one token per dataset, and no fallback: an event for a market without its dataset and its own token is dropped, because a market's learning must not be fed another's visitors and a public site must never hold the business's admin token.
5. The site's own numbers decide money: cost per paid order and ROAS are computed on the site's orders and settled revenue, with Meta's attributed figures beside them, never instead of them.
6. A budget moves by at most 20 percent a day and one thing of an ad set changes per day, because larger or combined changes send the ad set back into learning and blur the next day's reading.
7. Once a market has running ad sets, new creatives take at most half of its daily spend, because too much of a day's spend on untested creatives can halve a market's conversions in a day; the first batch is exempt and is the plan's small test budget.
8. Every change made to a campaign is written down with its figures (in `docs/ads.md` by this skill, in the audit log by the panel), so that the next review knows what changed and when.

## Terminology

| Term | Meaning |
|---|---|
| Business portfolio | The Meta business that owns the ad accounts, Pages, datasets and the app. |
| Admin token, dataset token, employee token | The agent's system user token on the machine; the token a dataset issues for the site's events; the read-only token for the dashboard and the spend sync. |
| Dataset | What receives the site's events (the API says pixel); one per market, shared across accounts when one is replaced. |
| Pixel | The browser script that sends `PageView` and `ViewContent` from public pages. |
| Conversions API | The server call that sends `Lead`, `InitiateCheckout` and `Purchase` with an event id. |
| Attribution | The click and campaign ids a visit carried, stored on the visitor's row and the order, and the join of the site's rows to spend by campaign. |
| Market | A country the site advertises in, with its locale, currency, dataset and ad account. |
| Lead moment | The first action on the site that shows intent; the `Lead` event and the first optimization target. |
| ABO, CBO | Budget per ad set (the test batch) or per campaign (the winners). |
| Spend cap | The campaign's hard ceiling, twice the first week's total for a new market. |
| Learning | The phase after an ad set starts or changes, before Meta's delivery has enough conversions to be judged. |
| Test event code | A code from Events Manager that routes server events to its test tab; set while verifying, removed after. |
| Operator panel | The ads screen of the dashboard `cloudflare-admin-dashboard` builds from `docs/ads.md`. |
