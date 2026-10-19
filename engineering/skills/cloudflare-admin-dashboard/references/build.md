# The admin Worker

What the build phase writes under `admin/`, how it is run locally, tested and deployed, and the templates of `DEPLOY.md`'s section and `docs/admin.md`. The security design is [security.md](security.md), the screens are [panels.md](panels.md); this page is the code and the deploy.

## Stack

A plain Worker, no framework adapter: Hono for routing and server-rendered pages with its JSX (`hono/jsx`) or its `html` template tag (`hono/html`, which escapes values the same way and needs no JSX build for the tests), `jose` for the Access token, D1 through the binding, Wrangler's bundler straight from TypeScript (no build step of its own). The packages are added to the project's root `package.json` (one lockfile, one install) at the version the registry resolves (`npm view hono version`), pinned; `tsx` as a dev dependency runs the tests. No client framework: a few hundred lines of the admin's own script for confirmations and tabs, one stylesheet, inline SVG charts. The reason: the admin is a dozen server-rendered screens that read a database; a framework would add a build, a client bundle and an update treadmill for nothing the operator sees.

## Files

```
admin/
  wrangler.jsonc        name <project>-admin, main src/index.ts, compatibility_date today, observability on,
                        d1_databases [{ binding DB, database_name <the project's>, database_id <the same id>,
                                        migrations_dir "migrations", migrations_table "d1_migrations_admin" }],
                        version_metadata { binding VERSION },
                        triggers.crons ["17 * * * *", "<the digest's minute and hour in UTC>"],
                        workers_dev true, preview_urls false,
                        vars { ENVIRONMENT "production", ADMIN_TIMEZONE, PUBLIC_SITE_URL }
  .dev.vars.example     ENVIRONMENT=development, ADMIN_DEV_BYPASS=1, then the secrets' names with comments:
                        ACCESS_TEAM_DOMAIN, ACCESS_AUD, ADMIN_OPERATORS, ADMIN_CONFIRM_SECRET, STRIPE_READ_KEY, STRIPE_REFUND_KEY,
                        META_ADS_ACCESS_TOKEN, META_AD_ACCOUNT_IDS, META_ADS_MANAGE_TOKEN, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
  migrations/           0001_admin.sql: admin_audit, admin_nonces, admin_settings (key, value, updated_at), the sync state and
                        the cache tables the project does not have yet (panels.md "The panel contract"); later ones per panel
  src/index.ts          the Hono app: headers middleware, guard, routes of every panel, the scheduled handler
  src/guard.ts          verifyAccess(request, env): the JWKS cache, jwtVerify, the allowlist, the fail-closed answers, the bypass
  src/audit.ts          audit(env, actor, action, target, params, result, ok): the row and the JSON log line
  src/confirm.ts        the confirmation token (HMAC with ADMIN_CONFIRM_SECRET, a nonce consumed by INSERT), the origin check,
                        the confirmation page
  src/db.ts             the D1 helpers: query, one, run, batch; the business-day helpers for the zone
  src/layout.tsx        the shell: header with the panels, the actor's email, the logout link; the stylesheet
  src/charts.tsx        bars and lines as SVG from day series
  src/panels/<name>/    index.ts, queries.ts, views.tsx, actions.ts per panel (panels.md "The panel contract")
  src/panels/index.ts   the ordered list
  src/jobs/             revenue.ts (ledger sync), spend.ts (the ads sync, importing the project's scripts/meta module when
                        it exports one, else the same logic), fx.ts, digest.ts, index.ts (which job runs on which cron)
  src/alerts/           rules.ts, send.ts (the chat tool, never logging its URL), index.ts
  src/integrations/     stripe.ts (balance transactions, the endpoint's status, refunds with an idempotency key),
                        meta.ts (insights, status, controls, the token in a header), telegram.ts
  tests/                guard, confirm, charts, queries against an in-memory D1 (getPlatformProxy), the rules, the log filter
```

The project's root scripts gain `dev:admin` (`wrangler dev --config admin/wrangler.jsonc --port 8788`), `deploy:admin` (`wrangler deploy --config admin/wrangler.jsonc`), `db:migrate:admin:local` and `db:migrate:admin:remote` (`wrangler d1 migrations apply <db> --config admin/wrangler.jsonc ...`), `test:admin` (`node --import tsx --test admin/tests/*.test.ts`), and `check` runs the admin's typecheck (a `tsconfig.json` under `admin/` with `jsxImportSource` `hono/jsx`) and tests after the site's.

## The guard

`verifyAccess`: with `env.ENVIRONMENT !== 'production'`, `env.ADMIN_DEV_BYPASS === '1'` and the request URL's hostname `localhost` or `127.0.0.1`, the actor is the development actor; otherwise `ACCESS_TEAM_DOMAIN`, `ACCESS_AUD` or a non-empty `ADMIN_OPERATORS` missing means 503; the header `Cf-Access-Jwt-Assertion` missing means 403; `jwtVerify(token, createRemoteJWKSet(new URL(teamDomain + '/cdn-cgi/access/certs')), { issuer: teamDomain, audience: aud })` with the key set cached in the isolate; `payload.email` missing or not in the list means 403 with an audit row; the actor is the email. Every route goes through it, including the static stylesheet and the health route.

## The scheduled handler

`scheduled(event, env, ctx)`: the scheduler matches `event.cron` to the jobs; each job writes `sync_state` with its start, result and detail, catches its own errors, and writes an audit row as `cron`. The digest job reads yesterday's figures in the business zone and sends them; its cron is the plan's hour (08:00 business time by default) converted to UTC. Jobs stay small per tick to fit the plan's CPU limit ([platform.md](/engineering/docs/cloudflare/platform.md) "Plans"): one account or one window per run, a backfill spread over ticks. Locally, `wrangler dev` does not fire crons; a request to `/cdn-cgi/local/scheduled?cron=<expression>` (spaces as `+`) runs the handler by hand (cron triggers page, checked 2026-10), which phase 5 uses before the live run.

## Local development

`npm run dev:admin` with `admin/.dev.vars` holding `ENVIRONMENT=development`, `ADMIN_DEV_BYPASS=1` and only the keys the developer has (none is required: a panel whose key is missing says so; the Access secrets are not mirrored locally, the bypass stands in); the database is the project's local D1 (the same `--persist-to` as the site's dev server, so that the admin reads what the site wrote), with the admin's migrations applied locally. The site's `.claude/settings.json`, when it exists, denies reading `admin/.dev.vars` like the others. Before any key is saved in `admin/.dev.vars`, `git check-ignore -q admin/.dev.vars` passes, else the line is added to `.gitignore` as a shown change.

## Deploys on push

Workers Builds deploys one Worker per connection: the admin gets its own on the same repository, root directory `/`, build command `npm ci`, deploy command `npx wrangler deploy --config admin/wrangler.jsonc`, production branch `main`, no preview trigger, `path_includes` `["admin/**", "package.json", "package-lock.json"]`, and the site's trigger gains `path_excludes` `["admin/**"]`, so that a push to one does not rebuild the other; made with the deploy skill's calls ([automation.md](/engineering/docs/cloudflare/automation.md) "Deploys on push") after the first manual deploy created the Worker, with the build token the project already has. When the Builds API refuses, the dashboard path is given, and until then `npm run deploy:admin` is the deploy, recorded in `DEPLOY.md`. The admin's migrations reach the remote database before the deploy that reads them, as the deploy skill's rule says.

## Tests

`admin/tests/*.test.ts`: the guard answers 503 with the secrets unset in a production configuration even for a loopback request, 403 for a missing or bad token and for an email outside the list, and admits a token signed by a test key whose JWKS the test serves; the bypass admits only with the three development conditions; the confirmation token is single use, bound to its parameters and expires, and two concurrent posts pass once; the origin check refuses a foreign origin and a request with neither header; the chart fills empty days and cuts by date; each panel's queries run against an in-memory database seeded with a few rows and exclude zero-amount orders; the rules fire on the thresholds and not below; no log line and no rendered page contains a key's prefix; every view escapes a value that contains markup.

## `DEPLOY.md` section template

```markdown
## Admin
Worker `<project>-admin` at https://<name>-admin.<subdomain>.workers.dev, bound to the same D1. Protected by Cloudflare Access (per-Worker setting; policy `<project>-admin - Production`, the operators' emails, kept out of this file); the Worker verifies the token (secrets ACCESS_TEAM_DOMAIN, ACCESS_AUD, ADMIN_OPERATORS) and serves nothing without them.
Secrets (set with `npx wrangler secret bulk <file> --config admin/wrangler.jsonc`, mirrored in `admin/.dev.vars` except the Access pair): <names, generated or from where>.
Migrations: `admin/migrations/`, applied with `npm run db:migrate:admin:remote` before deploying code that needs them.
Deploys: <Workers Builds connection for admin/ | `npm run deploy:admin`>. Cron: hourly syncs, digest at <hour> <zone>.
Operators: the Access policy (Workers & Pages > the Worker > Settings > Domains & Routes > Manage Cloudflare Access) and the secret `ADMIN_OPERATORS` on the admin Worker, kept the same; the addresses are not written in the repository.
```

## `docs/admin.md` template

```markdown
# Admin
What it is, who opens it and how (Access, a code by email), the panels and what each shows, what it can change and how it asks, the keys it holds and their permissions, the syncs and the digest, the time zone.

## Adding a panel
<panels.md "The panel contract", as the project's own words>

## Findings
<the inventory's findings about the public site, with what was done about each>
```
