# Stripe: what its skills share

The skills that take payments with Stripe and read its ledger (`stripe-payments`, and the operator dashboard that shows revenue) share how an agent gets access to an account, how a hosted checkout is created and confirmed, how the webhook is received and kept idempotent, and how settled revenue is read from the balance ledger. That lives here once, one file per topic, kept current in one place; each skill includes or links the page from the phase that reads it and carries its own method (what it asks, where it stops, what it accepts, its rules) itself.

| Document | Holds | Read |
|---|---|---|
| [`access.md`](access.md) | Access: sandboxes and live mode, the key types and which to ask for, where a key is created and kept, the permissions a restricted key needs for the app and for a read-only dashboard, verification, the Stripe CLI as the reference of the day. | Before the first call to the account; linked from the payments skill's intake and the dashboard's data phase. |
| [`checkout.md`](checkout.md) | The payment flow: a Checkout Session and its parameters, confirming a payment on return, the webhook endpoint and its signature, the events that matter and how to stay idempotent, products and prices by lookup key, promotion codes, subscriptions, refunds and disputes. | When the payment code is written or changed; included with the payments skill. |
| [`ledger.md`](ledger.md) | Settled revenue: the balance transactions ledger, how it is folded into days and markets, what is excluded, why a partial read must never overwrite a cache, and how the figures differ from the orders table. | When revenue is shown or synced; linked from the payments skill's live phase and from the dashboard's payments panel. |

## Who reads this

[`stripe-payments`](../../skills/stripe-payments/SKILL.md) and [`cloudflare-admin-dashboard`](../../skills/cloudflare-admin-dashboard/SKILL.md), both in this area. The payments skill declares `checkout.md` in its `skillcdn.include`, so that it arrives with the skill wherever SkillCDN serves it, and links the other two from the phases that read them; the dashboard links `ledger.md` from its data phase. A page is read with `read_repo_file` at `engineering/docs/stripe/<topic>.md` through the repository or the engineering connection, or as a file at `docs/stripe/` of the engineering plugin. A skill mounted alone cannot read a linked page there, and a copy taken into another agent has none of the pages: its Requirements say so and name this directory in the repository. What a skill cannot work without (its workflow, its checkpoints, its verdicts, its hard rules) stays in the skill. A change to an included page changes the served digest of the skill that includes it, as a change to a manifest does: edit it deliberately.

## What every Stripe skill does the same way

- **The key is the user's and never printed.** A key is read from the file the user saved it in, or from the local secrets file, into the environment or the Worker's secrets; it is never echoed, never put on a command line as a literal, never committed. A key that was pasted into a chat is moved into its file and the chat copy is not repeated; a live key that reached the chat is treated as leaked, because the transcript is a log, and the user rolls it when its phase ends. A live key reaches only the live Worker.
- **Sandbox first, live last.** Everything is built and verified against a sandbox with test cards; the live keys, the live webhook and the live products are the last phase, after the user's word, because from then on real money moves.
- **Amounts are verified server-side.** A payment counts only when the retrieved session says `paid` and its amount and currency equal the order's; the client never reports an amount.
- **Two paths confirm a payment, one wins.** The return to the site and the webhook both try to settle an order; an idempotency row decides, and a failed webhook handler answers 500 so that Stripe retries.
- **Revenue truth is the balance ledger.** What the business earned is read from Stripe's balance transactions, which already carry fees, refunds, disputes and the real exchange rate; the orders table is the funnel's truth, not the money's.
- **Discovery over memory.** A parameter's name, an event's shape, a payment method's availability, a fee: read from the API reference or the Stripe CLI at run time (`stripe docs` prints the reference pages in the terminal), and written down with the month when they must stand.

## How these pages are written

Each page is organized by topic and says what holds now. A fact that can go stale (a dashboard path, a default that changed for new accounts, a limit, a CLI flag) names its source and the month it was checked at the end of the sentence; a fact about how the API works carries no date, and changes when a run finds it wrong. There is no chronological log and no run narrative, and no example names an account, a product or a person.

## Adding what a run taught

The API, the dashboard or the CLI behaved differently from a sentence here: that sentence changes, with the source and the month. Something one skill's method learned: that skill's own `references/tool-notes.md`. An agent running a skill without the repository at hand reports the finding in its delivery, for whoever maintains the skill.
