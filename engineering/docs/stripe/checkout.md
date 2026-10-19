# The payment flow: Checkout, confirmation, webhooks

How a hosted Checkout is created and confirmed, how the webhook is registered and verified, which events matter and how they stay idempotent, how products and prices are kept per mode, and what subscriptions, refunds and disputes do to an order. Facts that move (a parameter that appeared, a default that changed, a limit) carry the month they were checked; `stripe docs checkout_sessions` and the API reference are the source.

## Hosted Checkout

A Checkout Session is created server-side with `POST /v1/checkout/sessions` and the customer is redirected to its `url`; the default `ui_mode` is `hosted_page` and nothing of Stripe.js runs on the site (checked 2026-10). The parameters an order needs:

| Parameter | Value | Why |
|---|---|---|
| `mode` | `payment` for a one-time order, `subscription` when a line item recurs | Required |
| `line_items[0][price]` | The price id found by lookup key for this product, currency and interval | Prices are per mode; the lookup key is the same in both |
| `line_items[0][price_data]` | Inline `currency`, `unit_amount`, `product` or `product_data[name]`, `recurring[interval]` | The fallback when a price is missing, so that a sale never fails on a sync gap; the name shown is the buyer's language |
| `success_url` | `<origin>/pay/success?session_id={CHECKOUT_SESSION_ID}` plus the locale parameter | Stripe replaces the placeholder literally |
| `cancel_url` | `<origin>/pay/fail` plus the locale and what the buyer was doing | Shows a back button on Checkout |
| `client_reference_id`, `metadata[order_id]` | The order id, twice | `metadata` is read on return and in `checkout.session.completed`; `client_reference_id` is the fallback |
| `payment_intent_data[metadata][order_id]` | The order id on the PaymentIntent too | A refund or a dispute event carries the charge and its intent, not the session |
| `subscription_data[metadata][...]` | The order id and the member on the subscription | Renewal events carry the subscription, not the session; `payment_intent_data` is not allowed in subscription mode |
| `customer_email` | The signed-in member's email | Prefills and locks the field; a guest types one, which comes back in `customer_details.email` |
| `allow_promotion_codes` | `true` | Stripe validates the code and shows the discount; no coupon system in the app |
| `locale` | The buyer's language tag from Stripe's list, else `auto` | The page's language |
| `managed_payments[enabled]` | `false` unless the user chose Stripe as the merchant of record | Some accounts created from late July 2026 have Managed Payments on by default for every session, and the dashboard offers no account toggle, so the integration states its choice on every session (third-party report and a run, checked 2026-10) |
| `automatic_tax[enabled]` | `true` only when Stripe Tax is active on the account | Needs the head office and registrations set in the dashboard |

The metadata carries ids and nothing personal: what the site knew about the buyer's visit (an IP address, a user agent, a click id) stays in the order row of the site's own database, where the webhook reads it, because metadata lives on Stripe's objects for as long as they do. Amounts are in the currency's smallest unit: whole units for zero-decimal currencies (the list is in `stripe docs currencies`), hundredths otherwise. One function converts, and the same function converts back when an event is read. A session expires after 24 hours by default (`expires_at` sets 30 minutes to 24 hours).

### Managed Payments

Stripe's merchant-of-record product for digital goods: Stripe is the seller, handles sales tax, VAT and GST in more than 80 countries, fraud, disputes and transaction-level support, for a fee, through Checkout and Payment Links only; it does not support Connect or Elements (Managed Payments pages, checked 2026-10; eligibility at `docs.stripe.com/payments/managed-payments/eligibility.md`). It is a business decision the user makes once: it changes who the buyer contracts with, the receipts, the refund policy page and the fee. The default of the payments skill is the user as seller with `managed_payments[enabled]=false`; when the user chooses Stripe, the sessions set it to `true`, the eligibility page is read for the countries and products allowed, and the legal pages say who sells.

## Confirming a payment

On return, the success page sends only `session_id` to the server; the server retrieves the session (`GET /v1/checkout/sessions/<id>?expand[]=payment_intent.latest_charge&expand[]=total_details.breakdown`) and settles the order only when all of these hold: the session's `livemode` equals the mode the deployment is meant for; the session's `currency` equals the order's; `amount_subtotal` equals the order's price in minor units; `amount_total` equals the subtotal minus `total_details.amount_discount` (a promotion code Stripe applied, recorded on the order with its code from the breakdown); and `payment_status` is `paid`, or `no_payment_required` with a total of 0. A subtotal that differs from the order is logged and refused: the price is the app's, the discount is Stripe's. The order record keeps the PaymentIntent id as its payment key, the charge's `payment_method_details.type` and the buyer's email from `customer_details`; the receipt URL stays with Stripe, where the dashboard's payment page shows it. An order that is already paid answers success without granting twice; an order that is refunded or disputed is never revived by a revisit of the success URL; and the answer reveals the grant's destination only to the browser whose member or guest cookie matches the order, since the session id is in a URL anyone could hold.

## The webhook endpoint

`POST /v1/webhook_endpoints` with `url` and `enabled_events[]` creates the endpoint and returns `secret` once (checked 2026-10); the agent writes it into the Worker's secrets (and the local file, for a local endpoint created with the CLI) and never prints it. An account holds at most 16 event destinations per mode; the dashboard's Workbench also shows them, and the newer "event destinations" API (`/v2/core/event_destinations`, thin or snapshot events) coexists with the v1 endpoints, which keep working and are what the skills register (events page, checked 2026-10). The endpoint is registered per mode: the sandbox one with the CLI's `listen` for local work and a sandbox endpoint on the deployed address while it runs on the sandbox key, the live one at the live phase.

The events the handler subscribes to and what each does:

| Event | Does |
|---|---|
| `checkout.session.completed` | Settles the order when the return never happened (the buyer closed the tab); the same checks as the return path, including `livemode` |
| `charge.refunded` | `amount_refunded` is cumulative: the new refund is the difference from what the order already recorded; revoke the granted part in proportion, lock the entitlement when fully refunded |
| `charge.dispute.created` | Record the dispute with its reason, revoke what is left of the grant, lock |
| `charge.dispute.closed` | `status` `won` restores what the dispute revoked; any other status keeps the order disputed |
| `invoice.paid` | Subscription mode: `billing_reason` `subscription_cycle` is a renewal (grant the period's allowance); `subscription_create` is the first payment, already handled by the session |
| `customer.subscription.updated`, `customer.subscription.deleted` | Mirror `status`, `cancel_at_period_end` and the period into the subscriptions table |

Verification: the `Stripe-Signature` header carries `t=<unix>` and one or more `v1=<hex>`; the expected signature is HMAC-SHA256 of `<t>.<raw body>` with the signing secret, compared in constant time, and a timestamp older than five minutes is rejected. The raw body is read as text before any parsing. An event whose `livemode` does not match the deployment's mode is answered 200 and ignored. Stripe retries a failed delivery for up to three days in live mode with back-off and three times over a few hours in a sandbox, and events are not ordered, so the handler keys its work on the event id: a `payment_events` row inserted first makes a duplicate a no-op, and a handler that throws deletes its row and answers 500 so that the retry runs again (events page, checked 2026-10). IP allowlisting is Stripe's second recommendation; on Workers the signature is the check.

## Products and prices

Products and prices are created per mode with `POST /v1/products` and `POST /v1/prices`, the price with a `lookup_key` such as `<product>-<currency>-<interval or once>` that the code resolves at checkout time (`GET /v1/prices?lookup_keys[]=...&active=true`). A price is immutable: a price change creates a new price with `transfer_lookup_key=true`, which moves the key atomically, and archives the old one with `active=false` (prices reference, checked 2026-10). The product's `id` can be chosen on creation (`<project>-<product>`), which makes the sync idempotent across runs: create, or on `resource_already_exists` update the name and description. A product's metadata carries the app's product id so that a dashboard reader can map back.

## Promotion codes

`allow_promotion_codes=true` lets the buyer enter a code on the hosted page; the operator creates coupons (`POST /v1/coupons` with `percent_off` or `amount_off` and `currency`, `duration`) and promotion codes (`POST /v1/promotion_codes` with `coupon`, `code`, `max_redemptions`, `expires_at`, `restrictions[first_time_transaction]`) per mode. A 100 percent coupon makes a session that completes with no payment (`payment_status` `no_payment_required`, `amount_total` 0); the handler treats it as paid with the whole price as discount and keeps such orders out of revenue and conversion statistics. Partner links that carry a code (`?code=`) are an app concern: a cookie remembers the code and the checkout passes it as `discounts[0][promotion_code]` instead of letting the buyer type it.

## Subscriptions

`mode=subscription` with a recurring price creates a Customer and a Subscription; the subscriptions table mirrors Stripe (status, `cancel_at_period_end`, current period start and end, which newer API versions put on the subscription's items rather than the top level, so the reader checks both; checked 2026-10). Cancellation at period end is `POST /v1/subscriptions/<id>` with `cancel_at_period_end=true`; an immediate cancellation is `DELETE /v1/subscriptions/<id>`, used when a refund or a dispute ends the relationship. A customer portal configuration (`POST /v1/billing_portal/configurations`, then `POST /v1/billing_portal/sessions` per visit) gives the member a Stripe-hosted page to update the card or cancel, which replaces building those screens. Entitlement checks allow a grace of a few days past `current_period_end` so that a late renewal webhook does not lock a paying member out.

## Refunds from the operator's side

`POST /v1/refunds` with `payment_intent` and an optional `amount` in minor units and `reason`, with an `Idempotency-Key` header so that a repeated submission refunds once; the `charge.refunded` event then does the bookkeeping in the app, so a refund issued in the dashboard and one issued by an operator screen end in the same state. A refund is money leaving the account: an operator screen confirms the amount and the order before calling it and writes who did it.

## Local development

The dev server reads the sandbox key, `STRIPE_MODE=sandbox` and the CLI's signing secret from the local secrets file; `stripe listen --forward-to` delivers the sandbox's events; `stripe trigger checkout.session.completed` proves the handler's wiring, and a test payment with card `4242 4242 4242 4242`, any future expiry and any CVC proves the whole path from the site's own button through the hosted page and back (testing page, checked 2026-10). The event the trigger makes carries Stripe's fixture, not the app's order, so the handler's "unknown order" branch is what it exercises; the real order path needs a session the app created.
