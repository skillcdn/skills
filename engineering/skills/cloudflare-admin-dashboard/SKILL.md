---
name: cloudflare-admin-dashboard
description: Builds the operator's dashboard as a separate Cloudflare Worker that only the operator can open, bound to the project's own database, protected by Cloudflare Access with a one-time email code and verified again inside the Worker so that it fails closed until protected, holding its own least-privilege keys apart from the public site, writing an audit log of every action, confirming anything that moves money or ads, and running a cron that syncs the ledgers and sends a daily digest. It shows today and the week, the funnel to the paid step, orders with refunds and disputes when stripe-payments ran, campaigns with spend, results and controls with the rules' recommendations when meta-ads-setup ran, costs, and the system's health. Use when the user asks for an admin, an operator dashboard, a back office, a place to see sales and ads, monitoring or alerts for a site, or to replace a password-protected admin page. Payments are stripe-payments, ads are meta-ads-setup, the public site is cloudflare-new-app.
license: MIT
compatibility: Needs a shell with Node.js, npm, git and curl in a checkout of a project that runs on Cloudflare Workers with a D1 database, the Cloudflare API token the deploy skill uses, network access to the Cloudflare API, and a person who can enable Cloudflare Access in the dashboard once. The read-only keys of the integrations the admin shows are created by that person; a chat bot token is optional, for alerts. Works in any agent that can run a shell and write files.
metadata:
  author: skillcdn
  version: "1.0"
  tools: cloudflare
skillcdn:
  include:
    - references/security.md
    - /engineering/docs/cloudflare/access.md
  translations:
    ko:
      title: 운영자만 여는 어드민 대시보드, 별도 워커로
      description: 웹 프로젝트의 운영 어드민을 운영자만 열 수 있는 별도 Cloudflare 워커로 만듭니다. 프로젝트의 데이터베이스를 같이 쓰고, Cloudflare Access(이메일 일회용 코드)로 보호하며 워커 안에서 토큰을 다시 검증해 보호되기 전에는 닫혀 있고, 공개 사이트와 분리된 최소 권한 키를 따로 갖고, 모든 액션을 감사 로그에 남기고, 돈이나 광고를 움직이는 일은 확인을 거치고, 크론으로 원장을 동기화하고 일일 요약을 보냅니다. 오늘과 이번 주의 개요, 결제까지의 퍼널, stripe-payments가 돌았으면 주문·환불·분쟁, meta-ads-setup이 돌았으면 광고비·성과·제어와 최적화 규칙의 추천, 비용, 시스템 상태를 보여 줍니다. 어드민, 운영 대시보드, 백오피스, 매출과 광고를 보는 화면, 모니터링이나 알림, 비밀번호로 막아 둔 어드민 교체를 요청할 때 쓰세요. 결제는 stripe-payments, 광고 연동은 meta-ads-setup, 공개 사이트 자체는 cloudflare-new-app이 맡습니다.
---
# The operator's dashboard, as a Worker only the operator can open

What goes in: a project in a checkout that runs on Cloudflare Workers with a D1 database, the operator's email addresses, the moments on the site that matter, the integrations the project already has (`docs/payments.md`, `docs/ads.md`) and the read-only keys for them. What comes out: a second Worker in the same repository under `admin/`, bound to the same database, serving the operator's screens over server-rendered pages, protected by Cloudflare Access with a one-time email code and checking Access's token and the operators' list on every request so that it serves nothing until protected, with its own secrets (a read-only payment key, a read-only ads token, a refund key and a management token only where the operator chose those controls), an audit log, confirmations, a cron that syncs the ledgers and sends a daily digest, `DEPLOY.md` and `docs/admin.md` saying what exists and how a later integration adds its panel. The design closes by construction the usual weaknesses of an admin built inside a public site: a shared password, a session on the public origin, a default signing key, no audit, pixels on admin pages, switches that unlock paid content.

## How the user is involved

- **Questions:** one message after the inventory, written under "Inputs": who the operators are, the moments that matter, the controls they want, the chat for alerts, and the keys with the steps to create them. Everything else is derived and shown in the plan.
- **Checkpoints:** the plan, before any file is written; the first deploy of the admin Worker, because it creates a public address (serving only a "not configured" page until protected); the one dashboard step the person takes to enable Access, which the run waits for; every push. One short message each, and one word continues. The files build.md names land after the plan's word, each shown as it lands; an edit the plan did not name waits for a word.
- **Go-ahead:** when the user says to go ahead alone, the reports between phases need no answer; the deploys and pushes hold, as the deploy skill's rules say.
- **Changes mid-run:** applied from that point; a panel added or removed, an operator added, a rule's threshold changed.

## Requirements

| What | Used for |
|---|---|
| A shell with Node.js (the project's major), npm, git and curl, in a checkout with `node_modules` installed | Building, testing and deploying the Worker |
| The project on Cloudflare Workers with a D1 database (`cloudflare-deploy` put it there): its Wrangler configuration with the database id, its `DEPLOY.md` | The binding the admin shares, the account, the names |
| The Cloudflare API token of the deploy skill (`.cf-token`); with Access: Apps and Policies Read added ([tokens.md](/engineering/docs/cloudflare/tokens.md)) the agent reads the AUD tag itself, else the person pastes it | Deploying the Worker, its secrets, the build connection; reading the Access application |
| A person with the dashboard | Enabling Access on the Worker once, and the Zero Trust organization the first time ([access.md](/engineering/docs/cloudflare/access.md)); creating the read-only keys |
| Optional: `docs/payments.md` from `stripe-payments`, `docs/ads.md` from `meta-ads-setup` | The payments and ads panels; without them those panels wait |
| Optional: a chat bot token and chat id (a Telegram bot from BotFather, or another tool with a send-message call) | The daily digest and the alerts; without one they go to the system panel only |

Check these before the first message. Without a Workers project with a database, stop: the admin reads the project's own tables and has nothing to show. Without the token, give the deploy skill's steps and wait.

The Cloudflare skills share the area's document set [`engineering/docs/cloudflare/`](/engineering/docs/cloudflare/README.md): [access.md](/engineering/docs/cloudflare/access.md) (Access, the one-time setup, protecting a Worker, verifying the token, service tokens, the token permissions) is included and arrives with this skill wherever SkillCDN serves it; [tokens.md](/engineering/docs/cloudflare/tokens.md), [automation.md](/engineering/docs/cloudflare/automation.md) and [platform.md](/engineering/docs/cloudflare/platform.md) are linked from phases 4 and 5 for the secrets, the build connection and the plan's limits. The payments panel reads [access.md](/engineering/docs/stripe/access.md) and [ledger.md](/engineering/docs/stripe/ledger.md) of the Stripe set (the read key's rows, the revenue ledger) and the ads panel [access.md](/engineering/docs/meta-marketing-api/access.md), [monitoring.md](/engineering/docs/meta-marketing-api/monitoring.md) and [campaigns.md](/engineering/docs/meta-marketing-api/campaigns.md) of the Meta set (the employee token, the spend cache and the rules, the objects), all read with `read_repo_file` through the repository or engineering connection, from the engineering plugin's `docs/`, or from a checkout of this repository. A mount of this skill alone lacks the linked pages and a copy of its directory lacks the included one too: say so in the first message, fetch them from `engineering/docs/` of the repository this skill comes from (`github.com/skillcdn/skills` for this pack) where the agent can, and otherwise run on this skill's own files, which carry the workflow, the security design and the rules. The design is [security.md](references/security.md), included; the screens are [panels.md](references/panels.md), the code and the deploy are [build.md](references/build.md), and what the tools did in runs is [tool-notes.md](references/tool-notes.md).

## Inputs

| Input | Source |
|---|---|
| The project | The current directory, or the path the user names: its Wrangler configuration (the Worker's name, the database binding and id), `migrations/` (the tables the panels read), `DEPLOY.md` (the account, the addresses, who holds which secret), `docs/brief.md`, `docs/payments.md` (its mode, its tables, its panel spec) and `docs/ads.md` (its tables, the account mapping, its panel spec) when they exist, the local secrets example file |
| The operators | Asked: the email addresses that may open the admin; one at least; the same list goes into the Access policy and into the Worker's allowlist |
| The moments | Asked when the project does not make them obvious: the three to five steps from a first visit to the paid step, which become the funnel's columns, mapped to the tables and columns the inventory found |
| The controls | Asked: whether the admin may refund orders (when payments exist), with a daily refund cap (default three times the highest price); whether it may pause, resume and re-budget ads (when ads exist); each control brings its own key |
| The keys | Asked with their steps, once the controls are known: a Stripe read key, and a refund key when refunds were chosen, created by the person as [access.md](/engineering/docs/stripe/access.md) "The live keys and their permissions" says, in the project's mode (`docs/payments.md` says sandbox or live); the Meta employee token and the account mapping from the project's local secrets file where `meta-ads-setup` left them, else created as the Meta [access.md](/engineering/docs/meta-marketing-api/access.md) says, and a management token when controls were chosen; all saved in `admin/.dev.vars` |
| Alerts | Asked: a chat to receive the daily digest and the alerts (a Telegram bot token and chat id, saved in `admin/.dev.vars`), or none |
| The business time zone | Derived from the project's configuration (the operator's zone from the brief), confirmed in the plan; every day in the dashboard is a day in that zone |
| Everything else | Derived and shown in the plan: the Worker's name (`<project>-admin`), its address, the panels that apply, the cache tables reused from the project and the ones the admin adds, the syncs and their hours (the digest at 08:00 business time), the alert rules, the audit log, the local development switch |

The questions, in one message after the inventory, each only when the request or the project does not answer it:

- "Who may open the admin? Give the email addresses; each person signs in with a code sent to that address, nothing to remember."
- "Which moments matter on your site, from a first visit to the paid step? For example visit, started, reached the key page, paid. I will show the funnel in that order."
- With payments: "Should the admin be able to refund an order, with a confirmation each time and a daily cap of <default>? If yes, create a Stripe key for refunds besides the read key: [the two keys' rows and the dashboard steps of the Stripe access page, in the project's mode], and save them in `admin/.dev.vars` as `STRIPE_READ_KEY` and `STRIPE_REFUND_KEY`." Without the control, the read key alone.
- With ads: "Should the admin be able to pause, resume and change the budget of your ads, with a confirmation each time, or only show them? Showing needs the read-only token `meta-ads-setup` already saved; controls need a management token: [the steps of the Meta access page]." Saved in `admin/.dev.vars`.
- "Do you want a daily summary and alerts in a chat? For Telegram: create a bot with BotFather, send it any message, save the bot token in `admin/.dev.vars` as the line `TELEGRAM_BOT_TOKEN=<token>` and tell me; I read your chat id with the bot's `getUpdates` call from that file and save it as `TELEGRAM_CHAT_ID`. Or say no."

## Workflow

Each phase produces a named artifact and ends with one line to the user. The Worker serves nothing until Access protects it, and the secrets that unlock it are set only after the protection is on.

### Phase 1: Inventory

Produces the **inventory**: the Worker's name and account from the project's configuration and `DEPLOY.md`; the database id; the tables and columns the funnel's moments map to, the orders, events and entitlements tables when payments exist, the spend and attribution tables when ads exist, the usage table when the project logs model calls; the cache tables the project already has (named in `docs/payments.md` and `docs/ads.md`) and the ones the admin will add; which secrets each Worker holds and the ones the admin needs instead; whether `admin/.dev.vars` is ignored (`git check-ignore -q admin/.dev.vars`), else the `.gitignore` line is added first, as a shown change; the time zone; any switch found in the public code that unlocks paid content or bypasses a payment, any admin key in the public Worker's secrets and any password page, reported as findings; and the panels that apply by [panels.md](references/panels.md) "Which panels apply". The questions of "Inputs" go out after it, in one message.

### Phase 2: Plan

Produces the **admin plan**, shown at the checkpoint: the panels and what each shows, the funnel's columns, the controls and their confirmations and caps, the keys the Worker will hold and with which permissions, the syncs and their cron, the alert rules, the operators, the address, the local development switch, and the two steps the person takes. Then stop: "Here is the plan. **Admin at** `<name>-admin.<subdomain>.workers.dev`, open only to <emails>, by a code sent to the email. **Shows:** <panels>. **Can do:** <refund an order up to <cap> a day / pause, resume and re-budget ads / nothing that changes anything>, each confirmed and logged. **Keys it holds:** <list>, none of them the public site's. **Syncs:** revenue and ad spend hourly, a digest at <hour>. **Costs:** nothing on the Free plans ([platform.md](/engineering/docs/cloudflare/platform.md) "Plans"; the syncs stay small per run). **You will do:** create the keys, and enable Access on the Worker once it is deployed; I walk you through both. OK?"

### Phase 3: Build

Produces the **admin Worker** under `admin/`, as [build.md](references/build.md) says, each file shown as it lands: the Wrangler configuration bound to the same database with its own migrations table, a cron and the production flag, the guard that verifies Access's token and the list and fails closed, the audit log and the nonce table, the confirmation and origin checks, the pages and the panels of the plan with their queries, the charts, the syncs, the alerts, the local development switch, the tests, and the project's check extended to the admin. `npm run check` passes before the phase ends.

### Phase 4: Protect and deploy

Produces the **live admin**. In this order: the admin's migrations applied to the remote database (the plan named the tables); checkpoint: "Deploying creates `<address>`; until you enable Access it shows only 'not configured'. OK?"; the first deploy without the Access secrets; the person's step from access.md "Protecting a Worker" (Workers & Pages > the admin Worker > Settings > Domains & Routes > Enable Cloudflare Access on workers.dev, a policy with the operators' emails, the one-time PIN login if the organization is new), given as the exact clicks of the day in one message in the user's language with the English in parentheses, covering both the case with and without an existing Zero Trust organization; then the team domain, read from the `Location` header of an unauthenticated request to the address (`curl -sI`), which Access now redirects to `https://<team>.cloudflareaccess.com/...`; the AUD tag read through the API when the token has Access: Apps and Policies Read, else pasted by the person from Zero Trust > Access controls > Applications > the Worker's application > Overview; the secrets set in one bulk file (`ACCESS_TEAM_DOMAIN`, `ACCESS_AUD`, `ADMIN_OPERATORS`, the generated `ADMIN_CONFIRM_SECRET`, the keys and the chat token from `admin/.dev.vars`) through the deploy skill's secrets path ([automation.md](/engineering/docs/cloudflare/automation.md) "Secrets"), a redeploy, and the checks: an unauthenticated request is redirected to the Access login page and never reaches a panel; the operator signs in ("Open <address>, enter your email, type the code you receive, and tell me what you see"); the sign-in appears in the audit log; the guard's refusals (a wrong audience, an email outside the list, no secrets) are covered by the unit tests, since the edge intercepts such requests live; the active deployment is the latest build. Then the build connection for `admin/` as build.md "Deploys on push" says, or the manual deploy command recorded; `DEPLOY.md` gains its admin section and `docs/admin.md` is written from build.md's template.

### Phase 5: Data and alerts

Produces the **first sync and the first digest**: the cron handler run locally through the scheduled test route, then live either at the next hourly tick or by the operator's button, with `sync_state` read from the remote database (`npx wrangler d1 execute <db> --remote --command`) to confirm it; the ledgers filled for their default windows, the panels showing figures, the digest sent to the chat (or shown on the system panel), the alert rules armed. What has no data yet (no orders, no spend) is shown as empty with the date it started counting, never as zero revenue.

### Phase 6: Delivery

One message: the address and how to sign in, the panels and what each shows, what the admin can change and how it asks, the keys it holds and what they cannot do, the syncs and the digest's hour, what was verified and what was not, the findings of the inventory (a bypass switch, a key in the wrong Worker, a password page), and how a later integration adds its panel (`docs/admin.md`).

### Verdicts

| Result | Verdict |
|---|---|
| Unauthenticated requests reach the login page and never a panel; the tests prove 503 without secrets even from loopback in a production configuration, 403 for a bad token and for an email outside the list; the operator sees the panels; every action writes an audit row with the actor; the syncs fill their tables; `npm run check` passes | Accepted |
| The Worker is deployed and locked but Access waits on the person, a key was not created yet, or a chat was not given | Accepted with the gap named in `DEPLOY.md` and the delivery |
| A panel answers without a verified token and a listed email, a secret or a bearer link appears on a page, in a message or in the repository, an action runs without a confirmation and an audit row, a panel reads an external API on view | Redone before anything is committed |

## Hard rules

1. The admin serves nothing until Access protects it and the Worker's own check passes: the Access secrets unset or the operators' list empty means 503 and no page, every request is verified and its email checked against the list, and the only exception is the development switch of `admin/.dev.vars`, which the production configuration cannot carry.
2. The admin is its own Worker with its own secrets: the public site never holds the admin's keys, the admin never holds the public site's signing secrets, runtime key or dataset tokens, and a key the admin holds is read-only unless the user chose a control that needs more.
3. Every action that changes something (a refund, a pause, a budget, a setting) is confirmed with its exact effect, bounded by the caps of the plan, and written to the audit log and the Worker's logs with the operator's email, the figures and the result; a read is never a write.
4. Pages read the project's tables and the admin's own caches only; external APIs are called by the syncs and the actions, never on view, and a sync that fails or reads a partial window leaves the cache as it was and says `partial`.
5. No third-party script, no analytics, no pixel runs on the admin; no raw HTML from data; no message to a chat and no page carries a link that opens a customer's content or a key.
6. Figures that carry a date are in the business time zone, windows are cut by date and filled with empty days, every label says its window, and zero-amount orders and opted-out visitors are excluded and counted apart, because dashboards misread each of these when they do not.
7. Deploying the admin and pushing follow the deploy skill's stops; a CLI secret change on a Worker that builds deploy is followed by a check of the active deployment.

## Terminology

| Term | Meaning |
|---|---|
| Operator | A person allowed to open the admin, by email, through Access and the Worker's list. |
| Access, AUD tag, team domain | Cloudflare's identity layer in front of the Worker, the application's audience id, and the `https://<team>.cloudflareaccess.com` issuer the Worker checks. |
| Guard | The middleware that verifies Access's token and the operators' list on every request and fails closed. |
| Development switch | `ENVIRONMENT=development` and `ADMIN_DEV_BYPASS=1` in `admin/.dev.vars`, which only `wrangler dev` reads. |
| Panel | One screen of the admin with its queries, charts and controls. |
| Moment | A step of the funnel, mapped to a table and a column. |
| Audit log | The table every action writes to, with the actor, the figures and the result, mirrored to the Worker's logs. |
| Confirmation | The step that shows an action's exact effect and asks before it runs, with a single-use token. |
| Sync | A cron job that reads an external ledger into the admin's cache tables. |
| Digest | The daily message with yesterday's figures against the same weekday last week. |
| Cache | The tables (revenue by day, spend by day, rates) that pages read instead of calling an API; the project's where they exist, the admin's where they do not. |
| Finding | Something the inventory saw in the public site that weakens it; reported, fixed on the user's word. |
