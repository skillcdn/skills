# Meta Marketing API: what its skills share

The skills that connect a web project to Meta ads (`meta-ads-setup`) and the operator dashboard that shows and steers the campaigns share how an agent gets access to a business's ad accounts, how a site measures what the ads bring (the dataset, the browser pixel, the Conversions API, attribution), what a campaign, an ad set, a creative and an ad are made of in the shape working accounts run, and how spend and results are read back and judged. That lives here once, one file per topic; each skill includes or links the page from the phase that reads it and carries its own method itself. The Meta Ad Library, the public website the marketing skills read, is another tool and has its own set under `marketing/docs/`.

| Document | Holds | Read |
|---|---|---|
| [`access.md`](access.md) | Access: the business portfolio, the app and its access tier, the system user and its token, the dataset's own token, what each permission allows, the file the token lives in, the API version and its short life, the read-only probe that proves access. | Before the first call; included with the ads skill. |
| [`measurement.md`](measurement.md) | Measurement: the dataset (pixel) and its settings, domain verification, the browser pixel's rules on a site that sells something private, the Conversions API and its event shape, deduplication, attribution capture and the URL parameters, Global Privacy Control, one dataset per market. | When the site is wired; included with the ads skill. |
| [`campaigns.md`](campaigns.md) | Campaigns: the objects and the settings working accounts run with (the objective, budgets per ad set or per campaign, the optimization event, the audience, placements, attribution window, the creative and its enhancements, URL tags, naming), the upload of a video, the order of creation, activation, and what changes reset learning. | When a campaign is created or changed; linked from the ads skill's campaign phase and from the dashboard's ads panel. |
| [`monitoring.md`](monitoring.md) | Monitoring: the insights call and its fields, time zones, the spend cache and its sync rules, the site's own attribution as the second source, the review method, and the optimization rules with their default thresholds. | When results are read or a change is decided; linked from the ads skill's optimization phase and from the dashboard's ads panel. |

## Who reads this

[`meta-ads-setup`](../../skills/meta-ads-setup/SKILL.md) and [`cloudflare-admin-dashboard`](../../skills/cloudflare-admin-dashboard/SKILL.md), both in this area. The ads skill declares `access.md` and `measurement.md` in its `skillcdn.include`, so that they arrive with the skill wherever SkillCDN serves it, and links the other two from the phases that read them; the dashboard links `campaigns.md` and `monitoring.md` from its ads panel. A page is read with `read_repo_file` at `engineering/docs/meta-marketing-api/<topic>.md` through the repository or the engineering connection, or as a file at `docs/meta-marketing-api/` of the engineering plugin. A skill mounted alone cannot read a linked page there, and a copy taken into another agent has none: its Requirements say so and name this directory. A change to an included page changes the served digest of the skill that includes it: edit deliberately.

## What every Meta skill does the same way

- **The token is the business's and never printed.** It is read from its file into the environment, never echoed, never committed, never put in a URL that is logged; the Worker's copy is a secret.
- **Money is a stop.** Creating ads is free; turning them on spends. Every campaign is created paused, its daily total is estimated in front of the user, and it is activated only after their word. A budget increase is a spend too.
- **Nothing private goes to Meta.** No name, nothing typed into a form, no content the visitor made or received, no page URL that carries a bearer key; what goes is the hashed email of a buyer, the IP and user agent, the click and browser ids, the product id and the amount. Zero-amount orders and opted-out visitors send nothing.
- **One dataset per market, never a fallback.** An event for a market without a dataset is dropped, not sent to another market's dataset, so that one market's learning is not fed another's visitors.
- **Two sources, read side by side.** Meta's attributed results drive its learning; the site's own ledger (sessions, leads, orders by campaign id, and settled revenue) decides where money goes. A decision is taken on the ledger with Meta's numbers next to it, never on Meta's numbers alone.
- **Discovery over memory.** The API version of the day, an account's currency and time zone, the minimum daily budget, an enum's current values: read from the API at run time and written down with the month when they must stand.

## How these pages are written

By topic, stating what holds now. A fact that can go stale (a version's end date, a dashboard path, a default the API changed, a limit) names the source and the month; a fact about how the API works carries no date and changes when a run finds it wrong. No run narrative, no account, no campaign and no product is named: the shapes observed in the reference accounts are written as shapes.

## Adding what a run taught

The API or the dashboard behaved differently from a sentence here: the sentence changes, with the source and the month. What one skill's method learned goes to its own `references/tool-notes.md`. An agent without the repository at hand reports the finding in its delivery.
