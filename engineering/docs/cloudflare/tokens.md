# Access: the API token

How an agent gets to act on a Cloudflare account: which kind of token to ask for, where the user creates it, the permissions a full setup needs and what each one is for, how to verify it, where it is kept, and what to do when there is none yet. Dashboard paths and permission names change; every one here carries the month it was checked, and the permissions reference at `developers.cloudflare.com/fundamentals/api/reference/permissions/` is the source of the current names.

## Which token

| Kind | Prefix | Created at | Choose it when |
|---|---|---|---|
| User API token | `cfut_` | My Profile > API Tokens (`dash.cloudflare.com/profile/api-tokens`) | One person's machine or agent. It can do everything below. Default. |
| Account API token | `cfat_` | Manage Account > Account API Tokens | A team's CI or an integration that must outlive its creator. It cannot buy domains (Registrar), create Turnstile widgets or call the Workers Builds API; the compatibility matrix on the account-tokens page says what else (checked 2026-10). Needs Super Administrator or token-provisioning rights to create. |

Convenience is the priority for a developer's own account: one user token with the "always" rows below, for all accounts and all zones, no IP filter, no expiry or a year. Say why to the user in one line: the token can change DNS and code on every zone and Worker of the account, so it lives in one gitignored file on one machine and is rotated when that machine is lost.

## The steps the user takes

1. Open the token page for the kind chosen above and select **Create Token**.
2. Start from the **Edit Cloudflare Workers** template (Workers Routes, Workers Scripts, Workers KV Storage, Workers Tail, Workers R2 Storage, Workers Builds Configuration, Account Settings, User Details, Memberships; checked 2026-10 in the dashboard), then add the rows below that the template lacks (D1, DNS, Zone, and the ones the plan needs) with **+ Add more**, and raise Account Settings to Edit. Each row is scope, resource, level.
3. Account Resources: **Include > All accounts** (or the one account). Zone Resources: **Include > All zones**: a new domain gets a new zone, and "all zones" covers it without editing the token.
4. Client IP filtering: none. TTL: none, or one year.
5. Continue to summary, create, copy the secret once. Save it in a file named `.cf-token` in the project's root folder (the folder that holds the Wrangler configuration; for a project not created yet, the folder it will be created in, from where the agent moves it) and tell the agent; this keeps it out of any chat log. A token pasted into the chat instead is moved into that file by the agent at once and never repeated.

## Permissions

The dashboard shows levels as Read and Edit; the API's permission-group list names the same groups with Write (checked 2026-10).

Always, whatever the project:

| Scope | Permission | Level | For |
|---|---|---|---|
| Account | Workers Scripts | Edit | Deploy, secrets, versions, the `workers.dev` subdomain, custom domains from the Worker's side |
| Account | Workers KV Storage | Edit | KV namespaces |
| Account | Workers R2 Storage | Edit | R2 buckets, their public URLs and domains |
| Account | D1 | Edit | Databases, migrations, queries |
| Account | Workers Tail | Read | `wrangler tail` |
| Account | Workers Builds Configuration | Edit | Connecting a repository, triggers, build variables, running builds through the API; in the template, and the permissions reference lists it as Workers CI (checked 2026-10) |
| Account | Account Settings | Edit | Listing accounts; creating the Web Analytics site through the API needs Edit (checked 2026-10); Read is enough without analytics |
| Zone | Workers Routes | Edit | Routes and custom domains |
| Zone | DNS | Edit | Records for email, verification, redirects |
| Zone | Zone | Edit | Creating a zone for a domain the user already owns (Zone Edit or DNS Edit on all zones; checked 2026-10), reading zone ids |
| User | User Details, Memberships | Read | `wrangler whoami`, account lookup |

When the plan needs it:

| Scope | Permission | Level | For |
|---|---|---|---|
| Account | Registrar | Edit | Buying domains with the Registrar API; the reference page did not list the group when checked (2026-10), so take the name from the dashboard's Account list or from the permission-groups endpoint |
| Account | Email Routing Addresses | Edit | Email Service sending or routing mail for the app |
| Account | Cloudflare Images | Edit | Images transformed or stored with Images |
| Account | Queues, Workers AI, Turnstile | Edit | When the app uses them; Turnstile is user-token only |
| Zone | Zone Settings | Edit | SSL mode, always-HTTPS |
| Zone | Single Redirect | Edit | A www-to-apex redirect rule instead of a redirect in code |
| Zone | Email Routing Rules | Edit | Inbound mail routing |

To see the current groups with their ids: `GET https://api.cloudflare.com/client/v4/user/tokens/permission_groups` with any valid token.

## Verify and use

```sh
export CLOUDFLARE_API_TOKEN=$(tr -d '\r\n ' < .cf-token)
curl -s https://api.cloudflare.com/client/v4/user/tokens/verify -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
curl -s https://api.cloudflare.com/client/v4/accounts -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
npx wrangler whoami
```

The verify call answers `"status": "active"`; the accounts call lists the account ids and names the token can see; `wrangler whoami` prints the same through Wrangler, which reads `CLOUDFLARE_API_TOKEN` from the environment. When the token sees several accounts, Wrangler asks which one: set `CLOUDFLARE_ACCOUNT_ID` in the environment or `account_id` in the Wrangler configuration. An account token is verified at `/accounts/<account id>/tokens/verify` instead. The file carries a carriage return on Windows; the `tr` strips it.

The token lives in `.cf-token` in the project root, listed in `.gitignore`, and reaches commands as an environment variable: exported once in a shell that keeps exports, or read inline on each command (`CLOUDFLARE_API_TOKEN=$(tr -d '\r\n ' < .cf-token) npx wrangler ...`) in a shell that does not. Never as a literal on a command line, never in the Wrangler configuration, never in `.dev.vars` (that file holds the app's own secrets), never in a commit, a log or a message the agent writes.

## When there is no token yet

`npx wrangler login` signs Wrangler in with OAuth, all scopes by default, through the browser of the machine the shell runs on; `--device` prints a code and a URL the user opens on any device when the shell has no browser (checked 2026-10). Every Wrangler command then works without a token, which covers resources, secrets, deploys and custom domains. For the REST calls (zones, DNS, the subdomain, Builds, Registrar, Web Analytics), `npx wrangler auth token` prints the OAuth bearer token for scripts, limited to the scopes granted at login; whether the Builds API accepts it was not checked (2026-10), and the dashboard steps replace it when it does not. Prefer the token: it does not expire mid-run and it carries exactly the permissions above.
