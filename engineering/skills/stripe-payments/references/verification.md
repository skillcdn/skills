# Verification: the sandbox, then the live smoke

The checks that prove the flow before any live key exists, in the order they run, each with what it shows and what a failure means; the way without the CLI; then the one smoke test after the switch. A check that cannot run in the agent's environment is reported as not run with what the user can do instead; nothing is reported as passed that did not run. The payments the user makes without a browser are named in the plan, so that none surprises them.

## The listener

`stripe listen --print-secret` once, with the sandbox key in `STRIPE_API_KEY`, captures the signing secret into the local secrets file as `STRIPE_WEBHOOK_SECRET` through the shell (never shown), next to `STRIPE_MODE=sandbox`; the secret does not change between restarts. Then `stripe listen --forward-to http://127.0.0.1:<dev port>/api/webhooks/stripe` in the background with its output written to a file in the temp directory (the event ids are read from it; the first line repeats the secret, so the file is deleted at the end and never quoted), and the dev server restarted so that it reads the secret. Use the numeric loopback address: a hostname can resolve to IPv6 while the server listens on IPv4.

## The wiring

`stripe trigger checkout.session.completed`: the listener prints the forward and the handler answers 200 with `unknown order`, which proves the signature check, the parsing and the routing; a 400 means the secret in the local file is not the listener's, a 503 that the secret is unset. `stripe trigger charge.refunded` and `stripe trigger charge.dispute.created` do the same for those branches.

## The order path

With a browser the agent drives: open the buy surface on the dev server, press the button, pay on the hosted page with card `4242 4242 4242 4242`, any future expiry, any CVC and any postal code, and come back. Without one, ask the user: "Open <local address>/<buy page>, press the buy button, and on Stripe's page pay with card number 4242 4242 4242 4242, any future expiry date, any three digits, any postal code; tell me when you are back on the site." Then read the ledger: the order is `paid` once, with the PaymentIntent id and the method; the entitlement row exists (or the subscription row with `active` or `trialing`); `payment_events` holds the `checkout.session.completed` row from the webhook and the `notify:` guard when a notification hook exists; the success page shows the purchase. Then resend the event (`stripe events resend <event id>`, the id from the listener's file): the handler answers "duplicate event" and nothing changes.

## Refund and dispute

A sandbox refund of that order by the agent, with the sandbox key: `POST /v1/refunds` with `payment_intent=<the order's payment key>` and half the amount; the listener delivers `charge.refunded`; the order's `refunded_amount` is the half, credits are reduced by half, an unlock stays; a second refund of the rest marks the order `refunded` and revokes the entitlement. A dispute: a second test payment (by the agent with a browser, or by the user when they agreed in the plan) with card `4000 0000 0000 0259`, which is disputed as fraudulent and lost (testing page, checked 2026-10); `charge.dispute.created` arrives at once and the order is `disputed` and locked; the sandbox closes the dispute within minutes with the simulated outcome and `charge.dispute.closed` keeps it `disputed`; the agent waits up to ten minutes and reports the closing as pending when it has not come. A 3-D Secure card (`4000 0000 0000 3220`) proves the return path handles an authentication step; optional, named in the plan when the market needs it.

## The free code

The sandbox's test promotion code typed on the hosted page: the session completes with `payment_status` `no_payment_required` and a total of 0; the order is `paid` with `discount_amount` equal to the price, `promotion_code` set, `method` `code`, and the statistics queries (a count of paid orders and a revenue sum, run against the ledger) exclude it.

## Subscriptions

When something recurs: the first payment settles the order and creates the subscription row; `stripe trigger invoice.paid` proves the renewal branch's wiring; the cancel route sets `cancel_at_period_end` on Stripe and in the row; the portal route answers a `billing.stripe.com` URL. A test clock (`POST /v1/test_helpers/test_clocks` and a customer created on it) advances time through a renewal when the plan wants the renewal grant proven end to end; otherwise the renewal is reported as proven at the wiring only.

## The project's own check

The project's check (types, lint, tests, build; the script this skill added when there was none) is green, and the dev server's public pages still answer 200 in every locale; the buy surface and the success and failure pages answer in every locale.

## Without the CLI

The return path is proven locally as above without the listener. The webhook branch is proven on the deployed address: before the live switch the deployed Worker runs with the sandbox key and `STRIPE_MODE=sandbox`, so a sandbox webhook endpoint is registered at `https://<address>/api/webhooks/stripe` (stripe-side.md "The webhook endpoint") with its secret in the Worker's secrets, the migration applied to the remote database, and the same test payments made on the deployed site; `payment_events` of the remote database shows the rows. The window is bounded: the endpoint and the sandbox key leave the deployed Worker at the live switch or at the end of the run, whichever comes first (the endpoint deleted, `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` removed with `wrangler secret delete`, the deploy status checked), because a public site on a sandbox key lets anyone complete an order with a test card; and an entitlement counts only when its order's `livemode` matches the deployment's, so such orders unlock nothing once the site is live. A project not deployed yet reports the webhook branch as not run.

## Live

After the switch: `GET /v1/account` on the setup key shows `charges_enabled`; `GET /v1/webhook_endpoints` shows the live endpoint `enabled` and no sandbox one; the sync script in live mode printed the same lookup keys; the deployed Worker answers the buy route with a Checkout URL whose session is `livemode` true (`stripeConfigured()` would refuse a mismatched key or mode); the deployed site's buy surface opens a `checkout.stripe.com` page with the right amount and the business name, which the user closes without paying unless they choose to make and refund a real small purchase (their money, their word; a refund costs Stripe's fee). The Developers > Webhooks page shows the first delivery when a real order comes; `stripe trigger --live` is not used, because it creates live objects. The delivery says the live path was verified to the payment page and not through it.
