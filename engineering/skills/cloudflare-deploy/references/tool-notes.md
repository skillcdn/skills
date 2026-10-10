# Tool notes: how the tools behaved in this skill's phases

By topic, in the order a run meets them. A fact that can go stale names where it was seen and the month; a fact about how the tools work carries no date and changes when a run finds it wrong. The platform-wide facts are in the shared pages; these are the edges this skill's own phases met.

## Shell and token

- A token saved to a file on Windows carries a carriage return; strip it before exporting (`tr -d '\r\n '`), or every call fails authentication with a value that looks right.
- Wrangler reads `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` from the environment and never from the configuration file; a shell that does not keep exported variables between commands (some agent harnesses) needs them read from the file on each command line, never typed as literals.
- A token without zone permissions makes `wrangler deploy` fail at the routes step when the configuration declares a custom domain, because Wrangler reads the zone's routes first; the workaround that stood in a run (attaching the domain through the account's `workers/domains` API and keeping `routes` out of the file) is unnecessary when the token carries Workers Routes and DNS on all zones (seen 2026-09).

- Git Credential Manager hangs on a fetch or a push from a non-interactive shell; `git -c credential.helper= -c 'credential.https://github.com.helper=!gh auth git-credential' ...` lets the signed-in `gh` answer (seen 2026-10).

## D1

- `wrangler d1 execute --file` uploaded a large SQL file and failed with `fetch failed` on one Windows machine; the same statements sent with `--command` in a few batches went through (seen 2026-09).
- A `LIKE` or `GLOB` pattern longer than 50 bytes fails the whole query on D1; a "contains" search uses `instr` (seen 2026-09 on a list page that answered 500 for long search terms).
- Applying migrations in a non-interactive shell skips the confirmation prompt and still takes the backup, so the remote apply runs unattended.
- `--update-config` appends a new entry to the configuration; on a binding that already has an entry (a placeholder id from the scaffold), create without it and write the id into the existing entry, or the Worker ends up with two bindings of one name.

## Secrets and versions

- `wrangler secret put` and `secret bulk` each create and deploy a new version, and fail on a Worker that has never been deployed; the first deploy carries the secrets with `--secrets-file` instead (Wrangler reference, checked 2026-10).
- On a Worker that Workers Builds deploys, a sister project once found the live code reverted to an older version after a CLI secret change; the deploy status showed it and a rebuild fixed it (seen 2026-09). Check `wrangler deployments status` after every CLI secret change on a connected Worker.
- A secret change makes a version that `wrangler versions view <id>` labels `Source: Secret Change`, built from the code of the version active at that moment, not from the last build: when those differ, the Worker goes live on the older code, which is what the check above catches; the next push-triggered build became the active version again (seen 2026-10).

## Deploy and domains

- The first `wrangler deploy` of an account asks for a `workers.dev` subdomain in an interactive shell; the subdomain call of automation.md reads or registers it beforehand, so a non-interactive shell never meets the prompt.
- A custom domain's certificate appears a few minutes after the DNS record; `curl` answers a TLS error until then, which is not a failure.
- Both the apex and `www` attached as custom domains, with the app redirecting `www` to the apex, held in production for two sites (seen 2026-09); the redirect-rule path of the custom domains page is the alternative when a redirect in code is not wanted.
- A cron Worker that calls the app must call the custom domain, not a `workers.dev` address of the same account: the same-zone call fails with error 1042 (seen 2026-09).

## Workers Builds

- The Builds API takes a user token; an account token answers "Invalid token" (API reference, checked 2026-10).
- The repository connection call fails until the Cloudflare GitHub App is installed for the GitHub account that owns the repository; it is the one dashboard step the connection cannot skip (checked 2026-10).
- The build image's default Node.js moves with the LTS releases and is announced; pinning `NODE_VERSION` to the project's major keeps a build from changing under the project (build image page, checked 2026-10).
- A build started through the API shows no `commit_hash` in the builds list; the build a push triggers does (seen 2026-10).
- The account's build tokens carry the names of the projects they were made for, and the API cannot create one; the dashboard does (checked 2026-10).
- `GET /accounts/<id>/rum/site_info/list` answered an authentication error with a token that had just created a site with the `POST` (seen 2026-10).
- `NEXT_PUBLIC_*` values missing from the build variables build fine and ship empty strings; the symptom is a wrong site URL in canonical links and share images, not a failed build.
