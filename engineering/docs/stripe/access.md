# Access: sandboxes, keys and the CLI

How an agent gets to act on a Stripe account: the two modes and their keys, which keys to ask for and with which permissions, where the user creates them and where they are kept, how to verify one, and the Stripe CLI, which is both a test tool and the reference of the day. Dashboard paths and defaults change; a sentence that states one names the month it was checked, and `stripe docs <topic>` or the API reference at `docs.stripe.com/api` (every page is also served as Markdown at its URL with `.md` appended) is the source of the current names.

## Modes

Every request runs in a sandbox or in live mode, and objects of one are invisible to the other: a product, a price, a webhook endpoint and a coupon exist per mode and are created twice, with the same lookup keys and ids where the API allows one, so that the code does not change at the switch. A sandbox is an isolated test environment with its own keys; an account can have several, and a new integration gets a sandbox of its own so that its settings and data stay apart from live mode (sandboxes page, checked 2026-10). In a sandbox the card networks process nothing: test cards complete a Checkout, and Stripe's test numbers cover declines, 3-D Secure and disputes. Live mode needs an activated account (the business details, a bank account, identity checks the dashboard asks for), which only the account owner can do. Every object and event carries `livemode`, and the code checks it against the mode its deployment is meant for, so that a sandbox key on a live site, or a sandbox event at a live endpoint, settles nothing.

## Keys

| Kind | Prefix | For |
|---|---|---|
| Secret key | `sk_test_`, `sk_live_` | Unrestricted. The sandbox's key: a sandbox holds no money and the skills' own checks create charges, refunds and disputes there, which a narrow key cannot. Never the live key of a Worker. |
| Restricted key | `rk_test_`, `rk_live_` | The live keys: permissions chosen per resource, so that a leaked key can do only what its holder does. Stripe recommends them over secret keys for every new integration (keys page, checked 2026-10). Live mode gets two: a setup key the agent uses once and that is rolled afterwards, and a runtime key the Worker holds. |
| Publishable key | `pk_test_`, `pk_live_` | Only for client-side Stripe.js. A hosted Checkout integration needs none. |
| Webhook signing secret | `whsec_` | Not an API key: one per webhook endpoint, returned once when the endpoint is created (or shown in the dashboard under the endpoint), verified by the webhook handler. |

A key created in live mode is shown once and cannot be revealed again; in a sandbox, keys stay visible in the dashboard (keys page, checked 2026-10). A restricted key can be tagged at creation as belonging to an autonomous agent ("Authorizing agent access to your account"), which puts refunds, payouts and account changes made with it under the account's approval rules (checked 2026-10): offer it for the setup key when the user wants a human in the loop.

### The live keys and their permissions

The dashboard groups permissions by resource with None, Read and Write (checked 2026-10). Three keys, each held by one party:

| Key | Held by | Permissions | For |
|---|---|---|---|
| Setup key (`.stripe-live-setup-key`) | The agent, on the machine, for the live phase only; rolled or deleted in the dashboard when the phase ends | Products Write, Prices Write, Coupons Write, Promotion Codes Write, Webhook Endpoints Write, Billing Portal Write, Tax Settings Read, Payment Method Configurations Read | Registering products, prices, the endpoint, the portal configuration; reading the account's settings |
| Runtime key (`STRIPE_SECRET_KEY` on the public Worker) | The public site | Checkout Sessions Write, Prices Read, PaymentIntents Read, Charges Read; Customers Write, Subscriptions Write and Billing Portal Write when something recurs | Creating and reading back a Checkout, resolving a price by lookup key, reading a charge's method, the member's subscription actions |
| Read key (`STRIPE_READ_KEY` on the operator's Worker) | The dashboard `cloudflare-admin-dashboard` builds | Balance Transactions Read, Charges Read, PaymentIntents Read, Webhook Endpoints Read | The settled revenue ledger (ledger.md), the order's payment page link, the endpoint's status |
| Refund key (`STRIPE_REFUND_KEY` on the operator's Worker, only when it refunds) | The dashboard | Refunds Write, PaymentIntents Read | Issuing a refund from the operator panel |

A public site that is compromised can then create and read Checkouts and payments and, when something recurs, act on customers and subscriptions; it cannot redirect the webhook, change a price, mint a code or refund. The webhook handler needs no key beyond the signing secret.

## Where a key is created and kept

1. Dashboard > Developers > API keys (`dashboard.stripe.com/apikeys`), with the sandbox or live toggle set to the mode wanted (checked 2026-10). For the sandbox: the secret key shown there. For live mode: **Create restricted key**, named after the project and its role, with the rows above, created, copied once.
2. The user saves it where the skill says: the sandbox's key as the line `STRIPE_SECRET_KEY=<key>` in the project's local secrets file (`.dev.vars`, or `.env` when the project chose it; gitignored), which the dev server reads and the agent reads for setup calls; the live setup key in `.stripe-live-setup-key` and the live runtime key in `.stripe-live-runtime-key` in the project folder (both listed in `.gitignore` and in the host's read-deny list before the user is asked), from which the agent runs the live setup and sets the Worker's secret, and which it deletes at the end of that phase, telling the user to roll the setup key in the dashboard. A key pasted into the chat is moved there by the agent at once; a live key that reached the chat is treated as leaked, because the transcript is a log, and the user rolls it in the dashboard when its phase ends.
3. The agent reads a key into the environment for its own calls (`STRIPE_API_KEY` is what the CLI reads; a script reads the file by path) and never prints it, not even its prefix beyond `sk_test_`.

## Verify

`GET /v1/account` with the key as a bearer token answers the account's id, country and default currency, whether charges are enabled, and the business profile; the id tells sandbox from live, and the account's profile name of a sandbox carries "sandbox" in accounts seen 2026-10. The response header `Stripe-Version` names the API version the request ran on, which is the account's default when the request named none; that is the version to pin a webhook endpoint to. A 401 means the key is wrong or expired; a `permission_error` names the missing permission, which is the row to add. The settlement currency is the account's `default_currency`; the ledger (ledger.md) is in that currency whatever the customer paid in.

## The Stripe CLI

Install with `npm install -g @stripe/cli` (also scoop, Homebrew and direct downloads; checked 2026-10). It needs no login when `STRIPE_API_KEY` is set in the environment or `--api-key` is passed; `stripe login` pairs a browser session instead. What the skills use it for:

- `stripe docs <query>` prints the reference pages in the terminal, which is the way to read a parameter's current definition without leaving the shell (CLI 1.43 or newer, checked 2026-10).
- `stripe listen --forward-to http://127.0.0.1:<port>/api/webhooks/stripe` receives the sandbox's events and forwards them to the local app, printing a signing secret (`whsec_`) that does not change between restarts and goes into the local secrets file as `STRIPE_WEBHOOK_SECRET` for development; `--events` filters, `--print-secret` prints only the secret, `--latest` uses the latest API version (checked 2026-10).
- `stripe trigger <event>` creates the objects that produce an event (`checkout.session.completed`, `charge.refunded`, `charge.dispute.created`, `customer.subscription.updated`, `invoice.paid` are supported; `stripe trigger --help` lists them) and sends it to the listener; `--override` and `--add` set fields of the fixture such as metadata (checked 2026-10). `stripe events resend <id>` delivers an event again.
- `stripe agent setup` installs Stripe's own agent skills and MCP server into the host it detects (checked 2026-10); optional, and never a substitute for this skill's rules.

## API version

Requests run on the account's default API version unless a `Stripe-Version` request header pins one, every response carries the version it ran on in its `Stripe-Version` header, and webhook events are shaped by the account's version unless the endpoint pins `api_version`. Since the `2024-09-30.acacia` release, monthly versions inside a named release carry no breaking changes, and a new named release with breaking changes comes twice a year (events page, checked 2026-10). The skills read the account's version from the response header of their first call (Workbench shows the same in the dashboard) and pin the endpoint to it, so that a dashboard upgrade does not change the events under the code.
