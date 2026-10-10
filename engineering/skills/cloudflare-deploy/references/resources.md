# The phases in detail: procedure, checks, failures

What each phase of the deploy runs, what it verifies before it reports, and what goes wrong with what to do. The commands are the ones [automation.md](/engineering/docs/cloudflare/automation.md) gives; this page says the order, the checks and the recovery. Every command runs from the project root with `CLOUDFLARE_API_TOKEN` (and `CLOUDFLARE_ACCOUNT_ID` when the token sees several accounts) in the environment: exported once, or read inline from `.cf-token` on each command when the shell forgets exports.

## Access

1. The token file: `.cf-token` in the project root, listed in `.gitignore` (add the line when it is missing, as a shown one-line change). A token the user pasted is written into that file by the agent and the paste is not quoted again. Export it: `export CLOUDFLARE_API_TOKEN=$(tr -d '\r\n ' < .cf-token)`.
2. Verify, list accounts, `npx wrangler whoami`, and the subdomain call; record the account id and name (several accounts: the one that holds the zone of the domain the user named, else the one they name, else ask), the token's kind from its prefix, and the subdomain (when the account has none, the plan names one, the account's name in lowercase letters, digits and hyphens, and the `PUT` runs after the plan's word).
3. Probe the permissions the plan will need with harmless reads, one per resource the configuration binds or the request names: `npx wrangler d1 list`, `npx wrangler r2 bucket list`, `npx wrangler kv namespace list`, `GET /accounts/<id>/workers/scripts` (Workers Scripts), `GET /accounts/<id>/builds/tokens` (Builds), `GET /zones` (zones, when a domain is wanted). Report any `Authentication error` or 403 with the row of tokens.md to add. Account Settings Edit cannot be probed without writing; the analytics call in phase 8 reports it when it is missing, and the dashboard path replaces it.

Failures: `Unable to authenticate request` on every call means the value was copied with a stray character or is a dashboard Global API Key, not a token; ask for a fresh copy into the file. `wrangler whoami` listing several accounts and later commands asking "which account" means `CLOUDFLARE_ACCOUNT_ID` is missing.

## Inventory and plan

1. `npm ci` (or `npm install` without a lockfile) when `node_modules` is missing, so that `npx wrangler` is the project's Wrangler. Find the configuration (`wrangler.jsonc`, `wrangler.json`, `wrangler.toml`). None: read the framework guide for the project's framework and write the file the platform page describes (name, main, assets, compatibility date of today, observability), as a shown new file, and say so in the plan.
2. List the bindings (`d1_databases`, `r2_buckets`, `kv_namespaces`, `send_email`) with their names and ids (a placeholder or missing id means "to create"), the secrets (`secrets.required`, else the names in `.dev.vars.example`, else `grep -r "env\." src` for names in capitals), the migrations folder, and the scripts (`build`, `deploy`, `preview`, `cf-typegen`).
3. The commands: the build command is the project's `build` script. The deploy command is the project's `deploy` script when that script is the framework's own deploy wrapper, run as automation.md's Deploy row says (on vinext: with the wrapper's skip-build flag, and through Wrangler with the configuration the build generated when the deploy carries secrets or is a preview), and `npx wrangler deploy` otherwise. Run the pair locally once in that order (with `--dry-run` where the wrapper offers it, else only the build) and check that what the deploy reads exists after the build (`dist/server/wrangler.json` and `dist/client` on vinext, `.open-next/worker.js` on OpenNext); when it exists only after the `deploy` script's own build step, move that step into `build` (a shown change) so that Builds and a local deploy do the same thing. Secrets and `secret list` address the Worker by its `name`, whichever configuration file the wrapper uses.
4. Build variables: every `NEXT_PUBLIC_*` name in the code and the example files (`grep -rho "NEXT_PUBLIC_[A-Z0-9_]*" src .dev.vars.example .env.example | sort -u`), with the site URL set to the address of this launch (the domain when one is attached in this run, else the `workers.dev` address), exported in the shell for the local build and set on the triggers; `NODE_VERSION` from `.node-version`, `.nvmrc` or `engines.node`, else the major of `node -v` on the machine where the check passed.
5. Derive names: the Worker is `name` in the configuration (the project's directory name when the file is new); the address `https://<name>.<subdomain>.workers.dev`; resources keep the configuration's names, and a binding with no entry gets `<name>-db`, `<name>-files`, `<name>-kv`.
6. Decide the plan: Free, unless the project uses Email Sending, Durable Objects beyond the free allowance, or the user names traffic above the Free numbers; then Paid, as a spend in the plan message.
7. For a domain to buy: run the search for the user's words, the check for the candidates, and put the top three with their registration and renewal prices in the plan; a `registrable: false` with a reason goes to the user.
8. The provider keys: for each secret with a provider in its name, the steps of automation.md's second table with this project's callback URLs: the callback path from the code (`grep -rn "callback" src/app/api/auth` or the auth module), the live address from step 5, `http://localhost:<port>` from the `dev` script; previews are not registered unless the user wants sign-in there.
9. Write the plan message of the skill's phase 2, with the code edits the launch needs (an analytics snippet in the root layout when the address is `workers.dev` and the layout has no slot for a beacon token; a `www` redirect when a domain comes) and stop.

## Resources

1. Which name wins: an entry with a name and a real id is kept and verified (`npx wrangler d1 info <database name>`); an entry with a name and a placeholder or missing id is created under that name (`npx wrangler d1 create <database name>` without `--update-config`, then the id written into the entry as a shown change); a binding the code uses with no entry is created with `--update-config` under the derived name. List first (`d1 list`, `r2 bucket list`, `kv namespace list`) and reuse a resource that already carries the name. The same for buckets and namespaces. A database is created with the location hint of automation.md's D1 row, chosen from the handover's audience, else the language of the request, and shown in the plan.
2. R2 answers with a subscription error until the user has added R2 in the dashboard: give the step, go on with the rest, and come back.
3. `npx wrangler d1 migrations apply <database name> --remote` (a non-interactive shell skips the confirmation and keeps the backup). A project with a single `schema.sql` instead of migrations: `npx wrangler d1 execute <database name> --remote --file=./db/schema.sql`; when the upload fails with `fetch failed`, send the statements with `--command` in small batches (seen 2026-09 on a Windows shell). A seed file the project or the handover names (`db/seed.sql`, sample content): `npx wrangler d1 execute <database name> --remote --file=./db/seed.sql` once, after the migrations and after the code that marks sample content is live (phase 5, or the build of a later push), and a count query afterwards to show the rows landed; the file is idempotent, so running it twice changes nothing.
4. `npx wrangler types` (or the project's `cf-typegen` script); `npx wrangler d1 migrations list <database name> --remote` must print no unapplied migration.
5. A public bucket: `dev-url enable` for a temporary address during the run, `domain add` with the zone id once the domain serves; record the public base URL for the app's configuration.

## Secrets

1. Split the required names: generated (a signing or session key with no provider in its name, or marked generated in the example file) and asked (everything with a provider: Google, LINE, Stripe, an email sender, an AI key). Generate straight into the secrets file, never through the terminal: `node -e "const c=require('crypto'),f=process.argv[1];require('fs').writeFileSync(f,JSON.stringify(Object.fromEntries(process.argv.slice(2).map(n=>[n,c.randomBytes(32).toString('base64url')])),null,2))" <secrets file> SESSION_SECRET ADMIN_SECRET`, the file in the user's temp directory.
2. Production gets fresh generated values. The local `.dev.vars` keeps the values it has (the new-app skill generated them) and gains only the names it lacks, so that the two carry the same names and never the same values; its content is never shown. A placeholder value in it (a provider's keys copied from the example file) is never sent: that secret is "later".
3. Complete the secrets file step 1 created, in the shape of [secrets.example.json](../assets/secrets.example.json), by adding every supplied value. It is sent in phase 5. A generated value the user must know (an admin password) also goes to a file of its own in the folder above the project (`<name>-admin-password.txt`), outside the checkout, named in the delivery and never written in a message.
4. A "later" value: ask once more at the plan checkpoint; still later: with `secrets.required` declared, show the change that drops the name from `required` (a comment says why), and confirm the code tolerates its absence (a provider check such as a function that answers false when the value is unset); when the code has no such check, add the one-line check as a shown change rather than ship a feature that throws. Note the name for the record.

## First deploy

1. Confirm (the message names the deploys that follow in this launch, such as the domain's). Then the project's build script with the `NEXT_PUBLIC_*` values of the inventory exported in the shell, and: a Worker that was never deployed: `npx wrangler deploy --secrets-file <secrets file>` (with the wrapper's generated configuration on vinext, automation.md's Deploy row; code and secrets in one version; `secrets.required` is satisfied in the same step); a Worker that exists: `npx wrangler secret bulk <secrets file>`, then `npx wrangler deploy`. Delete the secrets file. `npx wrangler secret list` must name every required secret.
2. The subdomain is known from phase 1, so the deploy does not prompt for one; a prompt that appears anyway means the account still has none: register it with the `PUT` and retry.
3. Verify: the public pages (the paths the sitemap lists, else `/` and the pages the plan named) with `curl -sIL https://<address><path>` answer 200 after redirects, and `curl -sL https://<address>/ | grep -o "<title>[^<]*"` shows the app's title; `npx wrangler deployments status` shows the new version active; `npx wrangler tail <name>` in the background for a minute while the pages are fetched shows no uncaught exception. A home page that redirects to a sign-in page counts when that page answers 200.
4. A 5xx: read the tail; a missing table means the migration was not applied (phase 3); a missing secret shows as the feature's own error; a 1042 is a same-zone fetch (platform.md).

## Domain

1. None yet: nothing to do; the record and the delivery say "to add a domain, run the deploy skill again with it", and the rest of this phase is skipped.
2. Owned domain: the zone is the registrable domain (`example.com` for `app.example.com`): `GET /zones?name=<that domain>` says whether it exists and its status. A hostname under a zone that exists needs no new zone and no nameserver change: take the zone id, check that no record exists for the hostname (`GET /zones/<zone id>/dns_records?name=<hostname>`; one that exists belongs to something else and attaching replaces it: stop and ask), skip to step 4 with that one hostname as the only custom domain, and add no `www`. Missing: `POST /zones` with the account id and `type: full`; give the two `name_servers` to the user with "set these at your registrar; it takes minutes to a day"; poll the zone's status while other phases run.
3. New domain: the Registrar API's check immediately before the register call, the price in the confirmation, then register; a `202` is polled; `action_required` stops and gives the user the reason; a domain bought this way is active on Cloudflare at once.
4. In the configuration, one shown edit: `routes` with the apex and `www` as custom domains (the one hostname alone when it is under an existing zone), `workers_dev: false`, and `preview_urls` untouched (platform.md's configuration table says why). Build again (on vinext the deploy reads the configuration the build generates, so every configuration change is followed by a build) and deploy; the certificate can take minutes, during which neither address answers. `curl -sIL https://<domain>/` and `https://www.<domain>/` both answer; the certificate can take a few minutes after the records appear.
5. `www` to apex: the app redirects when it sees the `www` host (one line in the request handler or the framework's proxy file, shown as a change), or a Single Redirect rule when the token has that permission; one of the two, not both. Update the site URL build variable to the domain.
6. A domain bought elsewhere and already on Cloudflare: nothing to move; take its zone id and continue at step 4.

## Deploys on push

1. Before any push: `.gitignore` lists `.dev.vars`, `.env*` (except the example), `.wrangler/`, `.cf-token` and the build output; the configuration with its ids, the generated types and the migrations are committed (a checkout with no commits gets its first commit here, shown as the list of files); the project's own check passes.
2. The repository, empty, before the connection: `gh repo create <owner>/<name> --private --source .` after the user's word (the owner they named, else `gh api user --jq .login`; the name is the Worker's), which adds the remote without pushing, or `git remote add origin <address>` with the address they gave. A shell where git hangs on credentials: tool-notes.md "Shell and token". A repository the user created on the site with a README or a license holds a commit the project lacks: `git pull --rebase --allow-unrelated-histories origin main`, the project's file kept on a conflict, then the push of step 5; a `main` is never force-pushed. `main` is the production branch.
3. The user installs the Cloudflare GitHub App (automation.md's second table); until that is done, the connection call answers with an error about the provider account. The installation must cover the repository: all repositories, or the new one added on GitHub's installations page. A user who followed the dashboard's prompts to the end has connected the repository and made the production trigger: list the Worker's triggers first, keep what exists, and add only the preview trigger and the variables.
4. Through the API, with the bodies automation.md gives: the GitHub ids, the repository connection, the Worker's tag, the build token (when the list is empty or holds only other projects' tokens, ask the user for one named for this project, the step of automation.md's second table, while the run goes on; when they decline, reuse one and record the dependency in `DEPLOY.md`), the production trigger, the preview trigger, the build variables from the inventory (`NODE_VERSION`, every `NEXT_PUBLIC_*`, with `is_secret: false` for public values).
5. Push `main` after the user's word (the confirmation covers the build it triggers): with the connection and the triggers in place, the push starts the first build; poll the builds list until its status is final; read the log on failure. Verify: that build's `commit_hash` equals `git rev-parse HEAD`, and the version it produced is the active one in `npx wrangler deployments status`. A build started through the API (a retry) carries no commit hash (automation.md's triggers row), so it is verified by its version alone.
6. The API path refused or unavailable: the dashboard: Workers & Pages > the Worker > Settings > Builds > Connect; branch `main`; build command the project's `build` script; deploy command the one the inventory derived; build variables as above; save, then push a commit.
7. Say to the user: from now on, a push to `main` deploys; a push to any other branch gets a preview address in the Worker's Previews section and on the pull request.

Failures: `The name in your Wrangler configuration file must match the name of your Worker` means the dashboard Worker and `name` differ; rename in the configuration. A build that times out at 20 minutes on a cold cache: retry once; then look for an install step fetching a large dependency. A build on the wrong Node.js major: pin `NODE_VERSION`.

## Observe and record

1. Analytics, with the call of automation.md's Analytics row. A zone is this site's alone when `GET /zones/<zone id>/dns_records` lists no hostname beyond the apex, `www` and mail: then the zone form of the call, and nothing to add to the code. Otherwise, and on a `workers.dev` address, the form by `host`, whose result carries the site's token: when the root layout reads a beacon token from a public build variable (the new-app skill leaves `NEXT_PUBLIC_CF_BEACON_TOKEN`), set it on the production trigger and rebuild; otherwise add the snippet before `</body>` of the root layout as a shown change. Without Account Settings Edit, give the dashboard path (Web Analytics > Add a site).
2. `observability.enabled` is true in the configuration; Workers Logs appear under the Worker's Logs tab after the next request. For a domain on Cloudflare, say to the user that the zone's bot settings (Security > Bots, the AI crawler blocking) must agree with the site's `robots.txt`, since a crawler blocked at the edge never reads it.
3. Write `DEPLOY.md` from the template below with only the rows that exist, commit it, and push on the user's word (which triggers a build).

### `DEPLOY.md` template

```markdown
# Deploy

Cloudflare account: <account name> (id in the Wrangler configuration or the environment). Worker: `<name>`.
Addresses: https://<name>.<subdomain>.workers.dev; https://<domain> (apex and www, or the one hostname) once attached, after which workers.dev is off.

| Resource | Name | Binding | Notes |
|---|---|---|---|
| D1 | <database name> | DB | migrations in `migrations/`, applied with `npx wrangler d1 migrations apply <database name> --remote` before pushing code that needs them; sample data in `db/seed.sql`; a read or a fix on the live data: `npx wrangler d1 execute <database name> --remote --command "<sql>"` |
| R2 | <bucket name> | BUCKET | public at https://files.<domain> |

## Secrets
Set with `npx wrangler secret bulk <file>` from a file outside the repository (the first deploy used `--secrets-file`), mirrored in `.dev.vars` (never committed).
Required: <NAME> (generated), <NAME> (from <provider>; steps: ...). Unset for now: <NAME>.
After a CLI secret change, check `npx wrangler deployments status`; rerun the build if the active version is older than the last build.

## Deploys
Push to `main` builds and deploys (Workers Builds; build `npm run build`, deploy `<the deploy command>`, Node <major>). Any other branch gets a preview. Build variables: <NAMES>.
Roll back: `npx wrangler rollback`, or the dashboard's Deployments tab.

## Observe
Logs: `npx wrangler tail <name>`, or the Worker's Logs tab. Analytics: Web Analytics in the dashboard.

## Token
The local Cloudflare token lives in `.cf-token` (gitignored) and is exported as `CLOUDFLARE_API_TOKEN`; its permissions are the "always" list in the skill's tokens page. Rotate it from My Profile > API Tokens when a machine is lost.
```
