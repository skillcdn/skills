---
name: stripe-payments
description: Takes payments on a web project with Stripe, from a sandbox to live money, with the agent doing every setup step a key allows. Use when the user says to take payments, add checkout, sell something, charge for a feature, add a subscription, or connect Stripe to a site, on Cloudflare Workers by default. The screens that show the money and refund an order are cloudflare-admin-dashboard; the ads that bring the buyers are meta-ads-setup. Asks what is sold, at what price and who the seller of record is, builds the order ledger, the hosted Checkout, and the return and webhook that settle an order exactly once (refunds, disputes and subscriptions included), registers the products, prices and webhook endpoint through the API, proves the flow in a sandbox with the Stripe CLI and a test card, then switches to the live keys and endpoint, lists the dashboard-only settings a person must set, and writes docs/payments.md with the operator panel's spec.
license: MIT
compatibility: Needs a shell with Node.js, npm, git and curl in a checkout of the project with its dependencies installed, a Stripe account the user can create keys for, network access to api.stripe.com, and the Stripe CLI (installed with npm) for local webhook tests. The live phase needs the project deployed with cloudflare-deploy. A browser the agent drives is optional, for the test payments. Works in any agent that can run a shell and write files.
metadata:
  author: skillcdn
  version: "1.1"
  tools: stripe
skillcdn:
  include:
    - references/build.md
    - /engineering/docs/stripe/checkout.md
  translations:
    ko:
      title: Stripe 결제 연동, 샌드박스에서 라이브까지
      description: 웹 프로젝트에 Stripe 결제를 붙입니다. 샌드박스에서 시작해 실제 돈이 오가는 라이브까지, 키로 할 수 있는 세팅은 에이전트가 전부 합니다. 무엇을 얼마에 파는지와 판매자가 누구인지(본인 또는 Stripe)를 묻고, 주문 원장과 호스티드 Checkout, 주문을 정확히 한 번만 확정하는 복귀 확인과 웹훅(환불·분쟁·구독 포함)을 만들고, 상품·가격·웹훅 엔드포인트를 API로 등록하고, Stripe CLI와 테스트 카드로 샌드박스에서 흐름 전체를 증명한 뒤, 라이브 키·라이브 엔드포인트·사람만 할 수 있는 대시보드 설정으로 전환하고, 운영 패널 명세가 담긴 docs/payments.md를 남깁니다. 결제 받게 해 달라, 체크아웃 붙여 달라, 유료 기능 만들어 달라, 구독 넣어 달라, Stripe 연동해 달라고 할 때 쓰세요(기본은 Cloudflare Workers). 돈을 보고 환불하는 운영 화면은 cloudflare-admin-dashboard, 손님을 데려오는 광고는 meta-ads-setup이 맡습니다.
---
# Payments with Stripe, from a sandbox to live money

What goes in: a project in a checkout, what it sells and at what price in the user's words, a Stripe account the user can create keys for, and a decision about who sells. What comes out: an order ledger in the project's database, a buy flow that sends the buyer to Stripe's hosted Checkout and settles the order exactly once on return or by webhook, with refunds, disputes and subscriptions handled, the products, prices and webhook endpoint registered on Stripe's side by the agent, the whole path proven in a sandbox with the Stripe CLI and test cards, then, on a deployed project, the live keys and the live endpoint in place with a checklist of the few things only the account's owner can set, and `docs/payments.md` in the project saying what exists, how money is read, and what the operator panel shows. The user never needs to know Stripe: every choice is derived from their answers, shown with its reason, and changed when they ask.

## How the user is involved

- **Questions:** one message at the start, written under "Inputs": what is sold, who sells, and the sandbox key. The live keys are asked at the live phase, when the sandbox flow has passed. Everything else is derived and shown in the plan.
- **Checkpoints:** the plan, before any file is written or anything created on Stripe; the live switch, because from then on real cards are charged; every deploy and push, which follow the deploy skill's stops and the repository's agreement. One short message each, with a recommendation, and one word continues. The files build.md names land after the plan's word, each shown as a diff as it lands, in one batch per step rather than approved one by one; an edit the plan did not name waits for a word, as the area's rule says.
- **Go-ahead:** when the user says to go ahead alone, the reports between phases need no answer. The plan, the live switch, the deploys and the pushes hold in every mode.
- **Changes mid-run:** applied from that point. An object already created on Stripe is kept and recorded, never silently deleted; a price change creates a new price and archives the old.

## Requirements

| What | Used for |
|---|---|
| A shell with Node.js (the project's major), npm, git and curl, in a checkout with `node_modules` installed | The code, the setup scripts, the checks, the commit |
| A Stripe account and the keys the user creates ([access.md](/engineering/docs/stripe/access.md)): the sandbox's secret key first, two restricted live keys at the live phase | Every call to Stripe: products, prices, the webhook endpoint, the test refund, reading a session back |
| The Stripe CLI, `npm install -D @stripe/cli` in the project with `XDG_CONFIG_HOME` pointed at a temporary folder (checked 2026-10), installed by the agent before the first message when it is missing | `stripe listen` for local webhooks, `stripe trigger` for event fixtures, `stripe docs` as the reference of the day |
| Network access to `api.stripe.com` | All of it; see [tool-notes.md](references/tool-notes.md) "Shell" for a shell whose curl cannot reach it |
| A running dev server for the sandbox phase | Where the listener forwards the webhook |
| For the live phase: the project deployed by `cloudflare-deploy`, with its `DEPLOY.md` and its `.cf-token` | The live address the endpoint points at, the Worker's secrets and variables, the deploy of the live code |
| Optional: a browser the agent drives | The test payments; without one the user makes them with the test cards on the local address and the agent watches the ledger |

Check these before the first message. Without the key, give the steps of access.md and wait. Without the CLI and with a machine that refuses to install it, the sandbox verification proves the return path locally and the webhook on the deployed address with a sandbox endpoint ([verification.md](references/verification.md) "Without the CLI"). Without a project, stop: this skill adds payments to a project that exists (`cloudflare-new-app` builds one). A project not deployed yet gets everything up to the live switch, and the delivery says that the switch is a later run of this skill after `cloudflare-deploy`.

The Stripe skills share the area's document set [`engineering/docs/stripe/`](/engineering/docs/stripe/README.md): [checkout.md](/engineering/docs/stripe/checkout.md) (the Checkout Session, confirmation, the webhook and its events, products and prices, promotion codes, subscriptions, refunds) is included and arrives with this skill wherever SkillCDN serves it; [access.md](/engineering/docs/stripe/access.md) (modes, keys, permissions, the CLI) is linked from phase 1 and [ledger.md](/engineering/docs/stripe/ledger.md) (settled revenue) from phase 6, and the Cloudflare pages [platform.md](/engineering/docs/cloudflare/platform.md) (where local secrets load from) and [automation.md](/engineering/docs/cloudflare/automation.md) (the Worker's secrets, the deploy status) from the phases that need them, all read with `read_repo_file` through the repository or engineering connection, from the engineering plugin's `docs/`, or from a checkout of this repository. A mount of this skill alone lacks the linked pages and a copy of its directory lacks the included one too: say so in the first message, fetch them from `engineering/docs/` of the repository this skill comes from (`github.com/skillcdn/skills` for this pack) where the agent can, and otherwise run on this skill's own files, which carry the workflow and the rules. The code this skill writes is [build.md](references/build.md), included; what is created on Stripe's side is [stripe-side.md](references/stripe-side.md), the checks are [verification.md](references/verification.md), and what the tools did in runs is [tool-notes.md](references/tool-notes.md).

## Inputs

| Input | Source |
|---|---|
| The project | The current directory, or the path the user names: its framework and adapter, the single-source configuration folder, the locale list and the currency per market, the database and its migrations, the member or guest model, where local secrets load from (`.dev.vars` or `.env`, and `secrets.required`), its check script, and `docs/brief.md` when the new-app skill wrote it, which often already says what is sold |
| What is sold | Asked: the things, their prices, the currency per market, whether anything recurs, a free trial; the default currency is the market's, from the project's locale table |
| What a purchase grants | Derived from the things sold and shown in the plan: an unlock of one item, a balance of credits, a period of access; the user corrects it |
| The seller of record | Asked once: the user's business (default), or Stripe through Managed Payments; when the user chooses Stripe, phase 2 reads the eligibility page before the plan ([checkout.md](/engineering/docs/stripe/checkout.md) "Managed Payments") |
| The refund policy | Asked with a default: refunds on request within 14 days, issued by the operator; the legal page says it; not asked when Stripe sells |
| The keys | The sandbox's secret key in the local secrets file; at the live phase, a setup key and a runtime key, restricted as access.md lists, each in its own file that the agent reads and deletes at the end of that phase |
| Everything else | Derived and shown in the plan: product ids and lookup keys, the Checkout parameters, the tables and routes, the webhook events, promotion codes instead of a coupon system, the success and failure pages, the legal pages, the API version pin (from the `Stripe-Version` header of the probe's answer), the deployment's mode variable, what the operator panel will show, and which pieces build.md leans on that the project lacks and this skill adds in their smallest form |

The questions, in one message at the start, each only when the request, the brief or the project does not answer it:

- "What do you sell, and at what price? For example a one-time unlock at 10 dollars, a pack of 10 credits at 5, or a monthly plan at 8 with a 7-day free trial. If prices differ by country, give each."
- "Who should the buyer pay: your business, which is the usual choice, or Stripe as the seller of record (Managed Payments), which then handles sales tax, VAT, refund support and disputes for a higher fee? I recommend your business unless you sell digital goods in many countries and want tax handled for you."
- "Refunds: on request within 14 days, handled by you from the dashboard? Say otherwise if you want a different window or no refunds for used content."
- "To set things up I need the secret key of a Stripe sandbox made for this project (it moves no real money; a sandbox borrowed from another project shows that project's name on the test payment page): [Sandboxes > Create when the account has none for this project, then the steps of access.md 'Where a key is created and kept' for the sandbox]. Save it as the line `STRIPE_SECRET_KEY=<key>` in the file `<the project's local secrets file>` in the project folder and tell me; that keeps it out of this chat. If you paste it here instead, I move it there and never repeat it."

In the plan: "You will make a few test payments on the local page with Stripe's test cards when I ask: one ordinary, one with a code that makes the order free, and, if you want the refund and dispute paths proven, one more each."

At the live phase: "Create two live keys as the dashboard shows them today: a setup key with [the setup rows of access.md], saved in a file named `.stripe-live-setup-key` in the project folder, and a runtime key with [the runtime rows], saved as `.stripe-live-runtime-key`. Tell me when both are there. I register the live products and endpoint with the first, put the second into the live site's secrets, delete both files at the end of this step, and ask you to roll the setup key in the dashboard."

## Workflow

Each phase produces a named artifact and ends with one line to the user. Nothing of the sandbox is reused in live mode: products, prices, the endpoint and the keys are created again there, under the same ids and lookup keys, so that the code does not change.

### Phase 1: Access

Produces the **access record**, kept at the head of `docs/payments.md` from phase 4 and shown in the plan: the account's id, country and settlement currency, whether charges are enabled, the key's mode, the default payment method configuration's methods that are on, and the account's default API version from the `Stripe-Version` header of the answer. First, as shown changes, the key files' names (`.stripe-live-setup-key`, `.stripe-live-runtime-key`) and the local secrets file join `.gitignore` when missing and the host's read-deny list (`.claude/settings.json` when the project has one), so that no later step can commit or read them. Then read the key from the local secrets file into the environment (never printed), call `GET /v1/account` and `GET /v1/payment_method_configurations` as [access.md](/engineering/docs/stripe/access.md) "Verify" says. A `permission_error` names the row the user must add; say so now. Confirm `stripe --version`. Find where the project loads local secrets (`.dev.vars` or `.env`, [platform.md](/engineering/docs/cloudflare/platform.md) "Bindings and secrets in code") and whether its Wrangler configuration declares `secrets.required`, which would hide a name not listed there.

### Phase 2: Plan

Produces the **payments plan**, shown at the checkpoint. From the answers and the project: the product table (`src/config/pricing.ts`), each product with its id, kind (one-time or recurring), what it grants, its price per currency and the lookup key per price; the buy flow (where the buy button sits, the hosted Checkout, the return page, the failure page); the entitlement model and where it is checked (build.md "The ledger"); the tables and routes build.md names; the webhook events; the legal pages that change (terms, privacy, a refund page); what will be created on Stripe's side in the sandbox; the seller of record (when Stripe, the eligibility page read first) and what it means for the pages; the tests; the pieces build.md leans on that the project lacks and this skill adds (a check script, a money formatter, legal pages); and the cost: Stripe's fees per transaction from the pricing page of the account's country (`stripe.com/pricing`, fetched), nothing up front. Then stop: "Here is the plan. **Sells:** <products with prices>. **Grants:** <what a purchase unlocks>. **Flow:** a buy button on <page>, Stripe's own payment page, back to <page>. **Seller:** <you / Stripe>. **Refunds:** <policy>. **I create on Stripe:** <n> products and <m> prices, the webhook endpoint, a promotion code for testing. **Costs:** Stripe's fee per payment, <rate from the pricing page>; nothing else. **You will do:** two to four test payments on the local page with test cards when I ask; the live keys when we switch; <the dashboard items> once. OK?"

### Phase 3: Build

Produces the **payments code**, as [build.md](references/build.md) says, each file shown as it lands: the price table, the migration with the orders, events, entitlements and (when something recurs) subscriptions tables, the Stripe client over `fetch` with the mode check, the checkout route, the return confirmation, the webhook with its signature check and idempotency, the entitlement module with its hooks, the pages, the local secrets names and the mode variable, and the tests. The project's check passes (or the check script this skill added) before the phase ends, and the phase ends with a commit as the repository's agreement says.

### Phase 4: Stripe-side setup

Produces the **Stripe record** for the sandbox, written into `docs/payments.md` as [stripe-side.md](references/stripe-side.md) says: the products and prices synced by the project's own script (idempotent, by product id and lookup key), the local webhook through `stripe listen` with its secret in the local secrets file, a customer portal configuration when something recurs, a test promotion code that makes an order free, and the review of payment methods and tax settings. Every id goes into `docs/payments.md`, never into the code.

### Phase 5: Verify

Produces the **verification report**, as [verification.md](references/verification.md) says: a triggered `checkout.session.completed` reaches the handler; a test payment with the test card through the site's own button settles the order once, grants what the plan says, and a resent event changes nothing; a sandbox refund made by the agent and a disputed test card do their bookkeeping; the free promotion code completes with no payment and no revenue; the check is green. What could not run (no browser, no CLI, a payment the user did not make) is reported as not run, with what the user can do instead.

### Phase 6: Live

Produces the **live record**. The project must be deployed (`DEPLOY.md` from `cloudflare-deploy`); when it is not, the phase ends here, `docs/payments.md` says "sandbox only", and the delivery says to run the deploy skill and then this skill again for the switch. Checkpoint: "The sandbox passed <what>. Switching to live needs your two live keys and creates the products, prices and webhook endpoint on the live account; from then on real cards are charged. OK?" Then, in this order: the sync script in live mode with the setup key read from its file; the live endpoint at `https://<address>/api/webhooks/stripe` registered with the setup key, its secret into the Worker's secrets as [automation.md](/engineering/docs/cloudflare/automation.md) "Secrets" says (`npx wrangler secret put` fed from a file, never a literal); the runtime key from its file into the Worker's `STRIPE_SECRET_KEY` the same way; the sandbox endpoint on that address deleted; the deployment's mode variable set to `live` (stripe-side.md "The mode of a deployment") and a deploy through the project's own path (a push on a connected repository, after the word; `npx wrangler deployments status` afterwards, and a rebuild when the active version is older than the last build, as automation.md says); the smoke test of verification.md "Live"; then both key files deleted and the user told to roll the setup key. Read [ledger.md](/engineering/docs/stripe/ledger.md) and complete `docs/payments.md` from build.md's template: what exists under which ids, how to read the money, the operator panel's spec, and the dashboard checklist for the person with what `GET /v1/account` shows as already set. When the project has an operator dashboard (`admin/` from `cloudflare-admin-dashboard`), add the payments panel as that project's `docs/admin.md` says; otherwise the delivery says that the dashboard skill will build it from `docs/payments.md`. Commit as the repository's agreement says.

### Phase 7: Delivery

One message: where the buy flow is, what a purchase grants, what was created on Stripe in each mode, what was verified and what was not, the dashboard items the person still owes with the menu paths of the day, how a refund is issued, and how the operator sees the money.

### Verdicts

| Result | Verdict |
|---|---|
| A test payment settles the order once, grants what the plan says, a resent event changes nothing, a refund and a dispute do their bookkeeping, the free code costs nothing and counts as nothing, an event of the other mode is ignored, the check passes | Accepted |
| The flow passes but the project is not deployed yet, the live switch waits on the user's activation or keys (the sandbox key and endpoint then leave the deployed Worker until the switch, as verification.md says), or a test payment could not be made | Accepted with the gap named in `docs/payments.md` and the delivery |
| An order is settled twice, a client-reported amount is trusted, a webhook with a bad signature or of the other mode is processed, a secret appears in a file or a message, paid content shows free because a key is missing | Redone before anything is committed |

## Hard rules

1. The keys and the signing secrets stay out of the repository, the logs and the agent's own words: read from their file into the environment or the Worker's secrets, never echoed, never a literal on a command line (a command substitution that reads the file is not a literal); the live key files are deleted at the end of the live phase and the setup key is rolled by the user. A leak means a rotation, which the user is told at once.
2. The sandbox passes end to end before anything is created in live mode, and the live switch is confirmed in every mode, because from then on real cards are charged.
3. An order is settled only when Stripe says the session is paid, its `livemode` matches the deployment's mode, its currency and its subtotal equal the order's own, and its total is lower only by a discount Stripe itself applied, which is recorded; the client never reports an amount, because a client is anyone.
4. Settlement is idempotent: the event id or the order's own status decides, a failed webhook handler answers 500 so that Stripe retries, and the return path and the webhook may both run with one result.
5. Prices live in one file and reach Stripe from it: the lookup key resolves the registered price, the inline price is the fallback, and a price change is a new price, never an edit.
6. Every Checkout Session states the Managed Payments choice, because a new account may have it on by default and the choice changes who the buyer pays.
7. A zero-amount order is a paid order for the buyer and nothing for the numbers: excluded from revenue, conversion and funnel statistics, marked in the ledger.
8. The public site holds a key that can create Checkouts and read them back, and nothing that can refund, change a price or move the webhook; those keys live with the agent for one phase or with the operator's dashboard. This skill charges no real card and issues no live refund: in the sandbox it refunds its own test payments to prove the bookkeeping.

## Terminology

| Term | Meaning |
|---|---|
| Sandbox, live | Stripe's two modes, with separate keys and objects; everything is built in the sandbox and recreated in live mode at the switch. |
| Mode variable | `STRIPE_MODE` on the deployment, `sandbox` or `live`; the code settles only what matches it. |
| Setup key, runtime key | The two restricted live keys: the agent's, for one phase, then rolled; the Worker's, for Checkouts only. |
| Checkout | Stripe's hosted payment page, created server-side as a Checkout Session and opened by redirect. |
| Order | A row of the project's ledger: what was bought, for how much, in which currency, by whom, and its status (`pending`, `paid`, `refunded`, `disputed`). |
| Settle | Marking an order paid and granting what it buys, once, by the return path or the webhook. |
| Grant, entitlement | What a paid order gives: an unlock, credits, a period of access; the row that records it; and the check the app runs before showing it. |
| Lookup key | The stable name of a price (`<product>-<currency>-<interval>`) that the code resolves to Stripe's price id in either mode. |
| Webhook | Stripe's call to the project with an event, verified by its signature, keyed by its event id. |
| Promotion code | A code the buyer types on the hosted page; Stripe validates it, and a 100 percent code makes a free order. |
| Seller of record | Who the buyer contracts with: the user's business, or Stripe under Managed Payments. |
| Ledger | Settled revenue read from Stripe's balance transactions, apart from the orders table. |
