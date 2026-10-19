# Stripe-side setup: what the agent creates, what a person sets

Everything on Stripe's side that a key can do is done by the agent, per mode, with a script that stays in the project and can be run again; what the API refuses on an account's own settings is given to the person as a checklist with the dashboard paths of the day. The calls are the ones [checkout.md](/engineering/docs/stripe/checkout.md) gives; this page says the order, the idempotency and the checks. In the sandbox the sandbox's secret key does all of it; in live mode the setup key does the creating and is rolled afterwards, and the runtime key is what the Worker gets ([access.md](/engineering/docs/stripe/access.md) "The live keys and their permissions").

## The sync script

`scripts/stripe/sync.mjs` in the project, run with the mode's key in `STRIPE_API_KEY` (read from the local secrets file or the live setup key file by the agent, never typed): it imports `src/config/pricing.ts` directly (Node strips types on the current LTS; `--experimental-strip-types` on an older one), takes `PROJECT` from it, then for each product `POST /v1/products` with `id=<project>-<product id>`, `name`, `description` (the default locale's copy) and `metadata[product_id]`; on `resource_already_exists` it `POST /v1/products/<id>` to update name and description. For each price of the product: `GET /v1/prices?lookup_keys[]=<key>&active=true`; none: `POST /v1/prices` with `product`, `currency`, `unit_amount` in minor units, `recurring[interval]` for a recurring product, `lookup_key`, `nickname`, `metadata[product_id]`; one with the same amount: nothing; one with another amount: create the new price with `transfer_lookup_key=true` and archive the old with `active=false`. It prints a table of ids and lookup keys, which goes into `docs/payments.md`. Products and prices are separate per mode, so the script runs once per mode, and the ids match across modes because they are chosen.

## The webhook endpoint

Local development uses the CLI's listener, no endpoint. A deployed address gets one per mode: `GET /v1/webhook_endpoints` first, reuse the one whose `url` matches (and update `enabled_events` with `POST /v1/webhook_endpoints/<id>` when the list changed), else `POST /v1/webhook_endpoints` with `url=https://<address>/api/webhooks/stripe`, `enabled_events[]` as checkout.md lists (`checkout.session.completed`, `charge.refunded`, `charge.dispute.created`, `charge.dispute.closed`, and `invoice.paid`, `customer.subscription.updated`, `customer.subscription.deleted` when something recurs), `api_version` pinned to the version the probe's response header named, and `description` naming the project and the mode. The `secret` of the answer is written straight into the Worker's secrets (`npx wrangler secret put STRIPE_WEBHOOK_SECRET` fed from the script's output through a pipe or a file in the temp directory that is deleted, never shown) and into the record as "set"; on a Worker that Workers Builds deploys, the active deployment is checked afterwards (`npx wrangler deployments status`, and a rebuild when the active version is older than the last build), because a CLI secret change can roll the code back to the version that was active ([automation.md](/engineering/docs/cloudflare/automation.md) "Secrets" and "Deploy"). A sandbox endpoint is made on the deployed address while it runs on the sandbox key (verification.md "Without the CLI"), and deleted at the live switch or at the end of the run, together with the sandbox key on the Worker; the live one at the live phase.

## Payment methods

`GET /v1/payment_method_configurations` shows the default configuration and which methods are on (`<method>.display_preference.value`); Checkout shows the eligible ones automatically. The plan lists what is on and leaves it unless the user asks: turning a method off is `POST /v1/payment_method_configurations/<id>` with `<method>[display_preference][preference]=off` (checked 2026-10). Wallets and local methods appear by the buyer's country and currency; a market whose popular method is off is what the user would notice first, so the plan names the methods that matter for each market it sells in.

## Promotion codes

A coupon and a promotion code per mode for the operator's use, created by the agent only when the plan asks for one; always one test code in the sandbox: `POST /v1/coupons` with `percent_off=100`, `duration=once`, `name=Test`, then `POST /v1/promotion_codes` with `code=TEST<random>`, `max_redemptions=50` and the coupon in the shape the account's API version takes (checkout.md on promotion codes); the code goes into `docs/payments.md` and the delivery, and the live account gets no such code unless the user asks, because a guessable full discount in live mode is a loss.

## Customer portal

When something recurs: `GET /v1/billing_portal/configurations`; none active: `POST /v1/billing_portal/configurations` with `business_profile[headline]`, `features[subscription_cancel][enabled]=true` (`mode` `at_period_end`), `features[payment_method_update][enabled]=true`, `features[invoice_history][enabled]=true`, `default_return_url=<address>/account`; the id is read at run time by the portal session route (the default configuration is used when none is passed). Receipts and renewal reminders are the dashboard's customer emails (below), not the app's.

## Tax

`GET /v1/tax/settings`: `status` `active` means Stripe Tax is set up (a head office address and registrations the person entered); then the plan sets `automatic_tax[enabled]=true` and prices carry `tax_behavior`. `pending` means the person has not activated it, and the sessions do not ask for tax until they do; the delivery says where (Dashboard > Tax). Under Managed Payments none of this applies: Stripe is the seller and handles tax.

## Managed Payments

When the user chose Stripe as the seller, eligibility (products, countries, integration) is read before the plan from `docs.stripe.com/payments/managed-payments/eligibility.md` and the setup page next to it; the sessions then set `managed_payments[enabled]=true`, the terms page says Stripe is the seller, and refunds and disputes are Stripe's. Otherwise every session sends `false`, since accounts created from mid-2026 may have it on by default with no account toggle (checked 2026-10); there is nothing to set on the account either way.

## The mode of a deployment

The Worker carries `STRIPE_MODE` (`sandbox` or `live`) as a var in its configuration (a build variable on the deploy, `sandbox` in the local secrets file), and the code refuses to start a Checkout with a key of the other mode and settles nothing whose `livemode` disagrees with it ([checkout.md](/engineering/docs/stripe/checkout.md) "Confirming a payment"). The live switch is the deploy that changes the var to `live` together with the runtime key.

## What a person sets in the dashboard

The account's own profile cannot be changed through the API: `POST /v1/account` on the account that owns the key answers 403, because the call is for connected accounts (seen 2026-08 in a run). Give these as one list with the paths of the day (checked 2026-10), with what to enter, and tick in `docs/payments.md` what `GET /v1/account` already shows as set:

| Item | Where | What to enter |
|---|---|---|
| Activate the account | Dashboard home > Activate payments (the business details, the owner's identity, the bank account) | Only the owner can; live charges fail until done |
| Public business name and statement descriptor | Settings > Business > Public details | The name buyers see on their card statement, 5 to 22 characters, letters and digits; the support email and phone the receipt shows |
| Branding | Settings > Business > Branding | The icon and colors of the hosted page and receipts, from the project's brand files |
| Customer emails | Settings > Business > Customer emails | Successful payments and refunds on; for subscriptions also the renewal reminders |
| Payment methods | Settings > Payments > Payment methods | Review what Stripe turned on; the plan's list per market |
| Radar | Radar > Rules | The defaults block the obvious; a rule for a market's risk later |
| Webhook endpoints | Developers > Webhooks | Created by the agent; the person sees the deliveries and failures here |
| Tax | Tax > Get started | Only when the plan has Stripe Tax |
| Roll the setup key | Developers > API keys > the setup key > Roll or Expire | After the live phase; the agent deleted its file |

The item is done when `GET /v1/account` shows `business_profile.name`, `business_profile.support_email`, `settings.payments.statement_descriptor` and `settings.branding.icon`, and `charges_enabled` is true for the live account; the agent checks and reports which are still open.
