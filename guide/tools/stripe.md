# Stripe skills

How the skills that take payments with Stripe and read its ledger (`stripe-payments`, and the payments panel of `cloudflare-admin-dashboard`) are written and kept in step, for authors. What they share at run time is the document set [`engineering/docs/stripe/`](../../engineering/docs/stripe/README.md), which agents read; this page says what goes there, what stays in a skill, and how the family is tested.

## The tool is the API, the CLI and the sandbox

The skills drive the REST API through `fetch` in Node scripts and in the Worker (not the SDK: the Workers bundle stays small and the REST shapes are what the CLI's `stripe docs` prints), the Stripe CLI for local webhooks and fixtures, and the user's dashboard for the account's own settings, which the API refuses on the account that owns the key. They name endpoints and parameters exactly, because those are the stable surface, and they name dashboard paths, defaults that moved (Managed Payments on new accounts), limits and CLI flags with the month they were checked, because those move. A fee, a payment method's availability by country and the account's API version are never written as facts to rely on: the skill says where to read them (the pricing page, the payment method configuration, Workbench).

## What is shared and what stays in the skill

| In `engineering/docs/stripe/` | In the skill |
|---|---|
| `access.md`: modes, key types, the permissions of a restricted key for the app and for a reader, where the key is kept, the CLI | What the skill asks the user for and when (the sandbox key at intake, the live key at the switch) |
| `checkout.md`: the Checkout Session, confirmation, the webhook and its events, idempotency, products and prices, promotion codes, subscriptions, refunds | The code the skill writes (`references/build.md`), the order of the phases, the checks (`references/verification.md`) and the stops |
| `ledger.md`: the balance ledger, the fold into days, the cache rules | How the payments panel shows it |

The test for a sentence: would it be true for the next skill of the family (a skill that sells through Payment Links, one that adds invoicing, one that reads the ledger for a report)? Then it belongs in the set. A sentence about one skill's phase stays in that skill's reference; how a tool behaved in that phase goes in its `references/tool-notes.md`.

The set sits in the area's `docs/` because every skill of the family is an engineering skill. The payments skill includes `checkout.md`; the admin skill links `ledger.md` from its payments panel. A change to `checkout.md` changes the served digest of the payments skill: edit deliberately.

## The seams

`stripe-payments` leaves hooks (`src/lib/payments/hooks.ts`: metadata providers, paid, refunded and disputed callbacks) that `meta-ads-setup` attaches to for the purchase event and the attribution metadata; the payments skill knows nothing of ads beyond the hook. It writes `docs/payments.md` with the panel's spec, which the admin skill reads; the admin skill knows nothing of Stripe beyond the ledger page and that spec. A change to what the panel shows is made in the payments skill's template; a change to how a panel is added, in the admin skill's contract.

## Examples name no one

Products, prices, account ids and domains in the set and the skills are placeholders (`item-unlock`, `10 USD`, `acct_<id>`); what running payment code taught is written as behavior ("a cap reached mid-window loses the oldest days"), never as their names, and no amount a customer paid appears anywhere.

## Testing

The payments skill is exercised by a fresh agent adding payments to a stand-in project with a sandbox key the user supplies, through the plan, the build, the Stripe-side setup and the sandbox verification (the CLI's listener, a triggered event, a test card payment made by the agent with a browser it drives or by the user), stopping before the live switch, which costs the user's attention and, after it, real money; a run to the live switch is confirmed as such. The admin's payments panel is exercised with the same sandbox's ledger. A change to either skill is dry-read before it is pushed; a run is read against the files as `skillcdn-skill-verification` says; what the API or the CLI did differently goes into the sentence of the set it bears on.
