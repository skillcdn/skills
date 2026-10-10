# Cloudflare: what its skills share

The skills that build for and deploy to Cloudflare (`cloudflare-…`) share how an agent gets access to an account, what the Workers platform means for an app and its configuration, and what an agent can do with a token against what only a person can do in the dashboard. That lives here once, one file per topic, kept current in one place; each skill includes or links the page from the phase that reads it and carries its own method (what it asks, where it stops, what it accepts, its rules) itself.

| Document | Holds | Read |
|---|---|---|
| [`tokens.md`](tokens.md) | Access: the two kinds of API token and which to choose, where each is created, the permissions a full setup needs and what each is for, how to verify a token and where to keep it, the sign-in fallback when there is no token. | Before the first call to the account; included with the deploy skill, linked from the new-app skill's intake. |
| [`platform.md`](platform.md) | The platform: what the Workers runtime can and cannot do, the Wrangler configuration an app needs, bindings and secrets in code and in local development, the paths for Next.js and other frameworks, the plans and their included usage. | When an app is scaffolded or configured; included with the new-app skill, linked from the deploy skill. |
| [`automation.md`](automation.md) | Automation: what an agent does with the token (resources, secrets, deploys, domains, builds, analytics) and what a person does once in the dashboard, with the command or call for each. | When resources are created or a deploy is automated; included with the deploy skill, linked from the new-app skill's launch phase. |

## Who reads this

[`cloudflare-new-app`](../../skills/cloudflare-new-app/SKILL.md) and [`cloudflare-deploy`](../../skills/cloudflare-deploy/SKILL.md), both in this area. Each declares the page every one of its runs reads in its `skillcdn.include` by its root-relative path, so that it arrives with the skill wherever SkillCDN serves it, and reads the other pages with `read_repo_file` at `engineering/docs/cloudflare/<topic>.md` through the repository or the engineering connection, or as a file at `docs/cloudflare/` of the engineering plugin, two levels above its own folder. A skill mounted alone cannot read a linked page there, and a copy taken into another agent has none of the pages: its Requirements say so and name this directory in the repository, which is where to fetch them. What a skill cannot work without (its workflow, its checkpoints, its verdicts, its hard rules) stays in the skill. A change to an included page changes the served digest of the skill that includes it, as a change to a manifest does: edit it deliberately.

## What every Cloudflare skill does the same way

- **The token is the user's.** The agent asks for it with the exact steps of the day, reads it only to put it in the environment, never prints it, never writes it into the repository, and uses it for everything it can do before asking the user to do anything by hand.
- **Money and live addresses are stops.** Buying a domain, moving to a paid plan, the first production deploy and every push are confirmed one at a time with what they cost and what they change; a go-ahead never covers them.
- **Discovery over memory.** The adapter the framework guide recommends, a permission's name, a plan's included usage, a command's flags: read from the documentation or the tool at run time, and written down with the month when they must stand.
- **Live before code.** A schema the code needs is applied to the remote database before the code is deployed, because a connected repository deploys on push.
- **The project carries its own deploy record.** What was created, under which names, where secrets live and how to roll back is written into the project (`DEPLOY.md`), never only in chat.

## How these pages are written

Each page is organized by topic and says what holds now. A fact that can go stale (a dashboard path, a permission's name, a plan's included usage, a product's beta status, a command's flag) names its source and the month it was checked at the end of the sentence; a fact about how the platform works carries no date, and changes when a run finds it wrong. There is no chronological log and no run narrative.

## Adding what a run taught

The platform, the dashboard or a command that behaved differently from a sentence here: that sentence changes, with the source and the month. Something one skill's method learned: that skill's own `references/tool-notes.md`. Examples name no account, no zone and no project: placeholders for ids, domains and names. An agent running a skill without the repository at hand reports the finding in its delivery, for whoever maintains the skill.
