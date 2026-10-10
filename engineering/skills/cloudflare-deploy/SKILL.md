---
name: cloudflare-deploy
description: Puts a web project live on Cloudflare Workers and makes it deploy itself from then on. Gets access with the user's API token (the exact steps of the day for creating it), creates the database, bucket and namespace the code binds, applies the schema, sets the secrets (signing keys it generates, provider keys the user supplies), deploys, attaches the domain (one the user owns and moves to Cloudflare, a new one bought through the Registrar API with the price confirmed, or a free workers.dev address), connects the repository so that every push to main deploys and every branch gets a preview, turns on logs and analytics, and writes DEPLOY.md into the project. Use when the user says to deploy, put live, host, go to production, connect a domain, set up Cloudflare, set the production keys or make deploys automatic for a project on Workers, including a Next.js app. Building the app itself is cloudflare-new-app, which hands over here at its launch phase.
license: MIT
compatibility: Needs a shell with Node.js, npm, git and curl in a checkout of the project, network access to the Cloudflare API and to the git host, and a Cloudflare API token the user creates (or a wrangler login). Works in any agent that can run a shell.
metadata:
  author: skillcdn
  version: "1.0"
  tools: cloudflare
skillcdn:
  include:
    - /engineering/docs/cloudflare/tokens.md
    - /engineering/docs/cloudflare/automation.md
  translations:
    ko:
      title: 프로젝트를 Cloudflare에 올리고 자동 배포까지
      description: 웹 프로젝트를 Cloudflare Workers에 올리고, 그 뒤로는 스스로 배포되게 만듭니다. 사용자의 API 토큰으로 접근을 얻고(오늘 기준 토큰 만드는 정확한 단계를 안내), 코드가 쓰는 데이터베이스·버킷·네임스페이스를 만들고 스키마를 적용하고, 시크릿을 넣고(서명 키는 직접 생성, 외부 서비스 키는 사용자에게 받음), 배포하고, 도메인을 붙이고(가진 도메인을 Cloudflare로 옮기거나, 가격을 확인받고 Registrar API로 새로 사거나, 무료 workers.dev 주소), 저장소를 연결해 main 푸시마다 배포되고 브랜치마다 미리보기가 생기게 하고, 로그와 분석을 켜고, 프로젝트에 DEPLOY.md를 남깁니다. 배포해 달라, 올려 달라, 도메인 연결해 달라, Cloudflare 세팅해 달라, 운영 키 넣어 달라, 자동 배포 만들어 달라고 할 때 쓰세요. 앱을 새로 만드는 일은 cloudflare-new-app이 하고, 그 스킬이 출시 단계에서 이 스킬로 넘깁니다.
---
# Put a project live on Cloudflare

What goes in: a project in a checkout, with a Wrangler configuration or a framework the platform page knows, a Cloudflare account the user can create a token for, the values of the secrets only they hold, and a decision about the domain. What comes out: the project serving at its address on Workers, its database, bucket and namespace created and bound, its schema applied, its secrets set, its domain attached with a certificate, its repository connected so that a push to `main` deploys and a branch gets a preview, logs and analytics on, and a `DEPLOY.md` in the project that says what exists and how to run it, every step shown as it happens and every spend confirmed before it is made.

## How the user is involved

- **Questions:** one message at the start, written under "Inputs": the token, the domain, the repository. The values only they hold (provider keys) are asked at the plan checkpoint, when the live address is known and the exact steps can be given. Everything else is derived and shown.
- **Checkpoints:** the deploy plan before anything is created; each purchase with its price (a domain, the Paid plan, the R2 subscription); the first production deploy, because the address becomes public; every push, which after the connection is also a deploy. One short message each, and one word continues.
- **Go-ahead:** when the user says to go ahead alone, the reports between phases need no answer. Purchases, the first deploy and pushes are confirmed in every mode.
- **Changes mid-run:** applied from that point. A resource already created is kept and recorded, never silently deleted.

## Requirements

| What | Used for |
|---|---|
| A shell with Node.js (the current LTS), npm, git and curl, in a checkout of the project | Wrangler through `npx`, the build, the API calls, the commit of the deploy record |
| The Cloudflare API token, or a `wrangler login` | Everything the first table of [automation.md](/engineering/docs/cloudflare/automation.md) lists |
| Network access to `api.cloudflare.com` and the git host | Resources, deploys, the repository connection |
| Optional: the `gh` CLI signed in | Creating the repository and pushing without the user's hands |
| The user, with a browser on any device | The few dashboard steps in automation.md's second table |

Check these before the first message. Without the token, give the steps of [tokens.md](/engineering/docs/cloudflare/tokens.md); when the user cannot create one, `npx wrangler login` (`--device` when the shell has no browser) covers phases 3 to 6 and the dashboard steps replace the Builds and analytics calls. Without network, stop and say so; without `gh`, the user creates the repository and gives its address.

What the Cloudflare skills share is the area's document set [`engineering/docs/cloudflare/`](/engineering/docs/cloudflare/README.md). [tokens.md](/engineering/docs/cloudflare/tokens.md) (access) and [automation.md](/engineering/docs/cloudflare/automation.md) (what the token does, what a person does once, the command for each), which every run reads, are included and arrive with this skill wherever SkillCDN serves it. [platform.md](/engineering/docs/cloudflare/platform.md) (the runtime, the configuration keys, the framework paths, the plans) is linked from phase 2 and read with `read_repo_file` through the repository or the engineering connection, or as a file under `docs/cloudflare/` of the engineering plugin, or at `engineering/docs/cloudflare/` of a checkout of this repository. A copy of this skill's directory lacks all three, and a mount of it alone lacks the linked one: say so in the first message, fetch what is missing from `engineering/docs/cloudflare/` of the repository this skill comes from (for this collection, `github.com/skillcdn/skills`) where the agent can, and otherwise run on this skill's own files, which carry its workflow and its rules. The procedures of each phase, with what to verify and what goes wrong, are in [resources.md](references/resources.md); what the tools did in runs is in [tool-notes.md](references/tool-notes.md).

## Inputs

| Input | Source |
|---|---|
| The project | The current directory, or the path the user names. Its `wrangler.jsonc` (or `.toml`), `package.json` scripts, `migrations/`, `.dev.vars.example` and `secrets.required` say what it needs; a project without a configuration gets one written from the framework guide, as platform.md says. |
| Access | The token, asked; its account id, derived with the accounts call. |
| The domain | Asked: one they own, one to buy, or none yet. |
| The repository | Asked: the GitHub address, or none yet; the owner, when `gh` creates it, is the one the user names, else the signed-in `gh` user. |
| Secret values | Generated for signing keys (a name with `_SECRET` or `_KEY` and no provider named, or marked as generated in the example file); asked at the plan checkpoint, by name and with where to get each, for provider keys. |
| Everything else | Derived and shown in the plan: the Worker's name (`name` in the configuration), its `workers.dev` address (the subdomain call), resource names (the configuration's, else `<name>-db`, `<name>-files`, `<name>-kv`), the plan (Free unless a feature needs Paid), the build and deploy commands (`package.json`, resources.md "Inventory"), the build variables (`NEXT_PUBLIC_*` names found in the code and the example files, `NODE_VERSION` from the project's version file or the machine's `node -v`). |

The questions, in one message at the start, each only when the answer is not already in the request, the project, or the handover from `cloudflare-new-app`:

- "To work on your Cloudflare account I need an API token. It takes a minute: [the steps of tokens.md, as the dashboard shows them today]. Save it in a file named `.cf-token` in the project folder and tell me; that keeps it out of this chat. If you paste it here instead, I move it into that file and never repeat it."
- "Do you already have a domain for this, should I find and buy one (I show the price before buying), or do we start on a free address (`<name>.<subdomain>.workers.dev`) and add a domain later?"
- "Where does the code live on GitHub? If nowhere yet, I can create a private repository for it, under your account or an organization you name."

At the plan checkpoint, for each value the user holds: "`<NAME>`: [the steps of automation.md's second table for that provider, with the exact callback URLs of this project]. Paste it, save it in `.dev.vars`, or say 'later' and the feature stays off until it is set."

## Workflow

Each phase produces a named artifact and ends with one line to the user; the records are scratch notes that feed `DEPLOY.md` and are not committed as such. The procedure, the checks and the failures of each phase are in [resources.md](references/resources.md) under the phase's name.

### Phase 1: Access

Produces the **access record**: the token's kind, the account id and name, the `workers.dev` subdomain, what the token can do. Export the token from its file (never print it), run the verify call, the accounts call and the subdomain call, then `npx wrangler whoami`; when the token sees several accounts, set `CLOUDFLARE_ACCOUNT_ID`. Probe each permission the project's bindings and the request will need with the harmless reads resources.md lists, and report a missing one now, with the row of tokens.md to add, not at the step that fails.

### Phase 2: Inventory and plan

Produces the **deploy plan**, shown at the checkpoint. Read the project: the configuration's bindings and their ids, `secrets.required` and the example file, the migrations, the framework and its scripts ([platform.md](/engineering/docs/cloudflare/platform.md) for what each key means), the `NEXT_PUBLIC_*` names, the Node.js version. Derive the address, what will be created, what will be set, which code edits the launch needs (the analytics snippet when the address is not a zone of Cloudflare, a redirect for `www`), which dashboard steps the user owes and when, and what it costs: the plan's included usage from platform.md's table with its month, and the live price of a domain from the check call. Then stop: "I will create <resources>, set <n> secrets (<generated>; <asked>: here is where each comes from), deploy to <address>, <attach domain / buy domain at price / stay on workers.dev>, connect <repository> so that pushes deploy, and <edits>. On the Free plan this costs nothing; <the domain costs X per year>. You do once: <dashboard steps>. OK?"

### Phase 3: Resources

Produces the **resource record**: each database, bucket and namespace with its name and id, created under the configuration's names and written into it (resources.md "Resources" says which name wins when an entry exists), and the migrations applied to the remote database before any code that needs them is deployed. Regenerate the types. Verify with the list commands.

### Phase 4: Secrets

Produces the **secrets file**: the generated values written to the local `.dev.vars` (kept out of the commit) and, with the values the user gave, into one bulk file outside the repository, in the shape of [secrets.example.json](assets/secrets.example.json). Nothing is sent yet: a Worker that was never deployed cannot take secrets before its first version. A value the user said "later" to is handled as resources.md "Secrets" says and named in the delivery.

### Phase 5: First deploy

Produces the **live address**. Build with the project's script (resources.md "Inventory" says which pair of commands), confirm ("Deploying makes `<address>` public. OK?"), deploy with the secrets file on a first deploy (`--secrets-file`) or after a bulk call on a Worker that exists, delete the file, then verify: `secret list` names every required secret; the public pages answer 200 (following a redirect) with the app's title; a minute of `wrangler tail` while they are fetched; the deployment status. Report the address.

### Phase 6: Domain

Produces the **domain record**. None yet: the `workers.dev` address stays, the delivery says how to add a domain later (run this skill again with the domain), and the phase ends here. An owned domain: the zone exists or is created, the nameservers go to the user, the run continues with everything that does not wait on them, and the custom domains are attached once the zone is active. A new domain: search, check, show the price and the renewal, confirm, register, poll. For a domain: the apex and `www` as custom domains in the configuration, a deploy, and a check of DNS, certificate and the `www` redirect.

### Phase 7: Deploys on push

Produces the **build connection**. First the commit of everything the launch changed (the configuration with its ids, the types, the migrations), with the ignore list checked; then the repository on the git host (created with `gh` and pushed after the user's word, or the address the user gave). The user installs the GitHub App once; the agent makes the connection, the production and preview triggers, the build variables and the Node.js version through the API, runs one build (covered by the confirmation of the push that carried the code), reads its log, and verifies that the active deployment is that build and that build is `HEAD`. When the API refuses, the dashboard steps replace it, as resources.md gives them. From here on, a push to `main` is a deploy and a push to a branch is a preview; say so.

### Phase 8: Observe and record

Produces **`DEPLOY.md`** in the project (the template in resources.md) and the delivery. Create the Web Analytics site (injected at the edge for a domain on Cloudflare; a beacon token set as a build variable, or a shown edit of the root layout, for a `workers.dev` address); confirm logs are on. Commit `DEPLOY.md` and push on the user's word. Deliver in one message: the addresses, what was created and set, what the user still owes (a nameserver change, a "later" secret), what was verified and how, and how the next deploy happens.

### Verdicts

| Result | Verdict |
|---|---|
| The public pages answer 200 over HTTPS with the app's title, the deployment status shows the build of `HEAD`, every required secret is listed, no migration is unapplied | Accepted |
| The site serves but a secret is "later", or the domain waits on nameservers | Accepted with the gap named in `DEPLOY.md` and the delivery |
| A build fails, a page answers 5xx, the certificate is pending after an hour | Redone from the phase that failed, with resources.md's failure notes; the user is told what was tried |

## Hard rules

1. The token and every secret stay out of the repository, the logs and the agent's own words: a value is read from its file into the environment, written to the Worker and to the local secrets file, never echoed, never put as a literal on a command line, and the bulk file is deleted. A leak means a rotation, which the user is told at once.
2. Nothing is bought or upgraded without the price in front of the user and their word: a domain (non-refundable), the Paid plan, the R2 subscription. A go-ahead never covers these.
3. The first production deploy and every push are confirmed. After the repository is connected, a push is a deploy, which the user chose at the plan checkpoint; a change they want kept off production goes to a branch, which previews.
4. The agent never asks the user to do what the token can do, and gives every dashboard step as the exact clicks of the day in one message, so that the user can do them while the run goes on.
5. A schema change reaches the remote database before the code that needs it is deployed, because a connected repository deploys on push and a page that meets a missing table answers 500.
6. After a secret is changed from the CLI on a Worker that builds deploy, the active deployment is checked against the latest build and the build is rerun when they differ; a sister project once found its live code reverted by that path.
7. Names and ids go into the configuration and `DEPLOY.md`; a value a secret scanner would flag (a key, a token) never does. Every edit to the project's files is shown as a diff before it lands, including the ignore list and `secrets.required`.

## Terminology

| Term | Meaning |
|---|---|
| Token | The Cloudflare API token the user created; the agent's access, read from `.cf-token`. |
| Account id | The 32-character id of the Cloudflare account the resources go in. |
| Subdomain | The account's `workers.dev` name; a Worker's free address is `<name>.<subdomain>.workers.dev`. |
| Zone | A domain managed by Cloudflare DNS; a custom domain for a Worker lives in one. |
| Binding | The name the code uses for a resource (`DB`, `BUCKET`, `KV`, `EMAIL`), declared in the Wrangler configuration. |
| Secret | A value the Worker reads at run time and nobody can read back; set with Wrangler, mirrored in the local `.dev.vars`. |
| Secrets file | The JSON file outside the repository that carries every secret to the Worker in one call, deleted afterwards. |
| Custom domain | A hostname attached to the Worker with its DNS record and certificate made by Cloudflare. |
| Builds, trigger | Workers Builds, the service that builds and deploys the repository on push; a trigger is its rule for one branch set. |
| Preview | The address a build of a non-production branch gets. |
| Deploy record | `DEPLOY.md`: what exists, under which names, how secrets are set, how to roll back. |
| Later | A secret the user did not supply; the feature it serves stays off and the delivery names it. |
