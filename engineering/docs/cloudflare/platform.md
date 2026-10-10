# The platform: what Workers means for an app

What the Cloudflare Workers runtime can and cannot do, the configuration an app on it needs, how code reaches bindings and secrets locally and live, which path a Next.js app takes, and what each plan includes. Read when an app is scaffolded, configured or deployed. Facts that move (a flag, a default, a plan's numbers, a beta) carry the month they were checked; the Workers documentation is the source.

## The runtime

- A Worker runs on V8 isolates at the edge, not in a Node.js process. Node.js built-ins (`node:crypto`, `node:buffer`, `node:fs`, `node:http`, and the rest the runtime supports) are available by default for a compatibility date of 2026-08-04 or later; an earlier date needs `nodejs_compat` in `compatibility_flags` (checked 2026-10).
- No raw TCP mail: email goes through an HTTP API, Cloudflare Email Service (the `send_email` binding or its REST endpoint, Workers Paid, beta, checked 2026-10) or a third-party REST sender.
- The clock is UTC. A "today" that depends on where the user lives is computed with that locale's offset or time zone, never from the Worker's local time.
- CPU time, not wall time, is limited per invocation: 10 ms on the Free plan, 30 s default on Paid (checked 2026-10). A long AI call waiting on the network costs little CPU; heavy rendering or hashing does.
- A `fetch` from one Worker to another on the same zone by route or `workers.dev` fails (error 1042) unless the target runs on a Custom Domain or is called through a service binding. A cron that must call the app calls its custom domain.
- Image optimization of a framework (such as `next/image`) is not a built-in: the framework guide says whether its path supports it, through Cloudflare Images or not; a plain `<img>` with width and height is always safe.
- Static assets (the framework's build output under `assets.directory`) are served before the Worker runs and cached at the edge; the Worker handles the rest.

## The configuration file

`wrangler.jsonc` at the project root (TOML works too); `"$schema": "./node_modules/wrangler/config-schema.json"` gives editor help. What an app needs:

| Key | Holds | Note |
|---|---|---|
| `name` | The Worker's name | Must equal the Worker's name in the dashboard: Workers Builds refuses a mismatch |
| `main`, `assets` | Entry file and the static assets directory with its `binding` (`ASSETS`) | Set by the framework's scaffold |
| `compatibility_date` | The day the project was created | Moving it forward is a deliberate change: read the compatibility flags page for what it switches on |
| `observability.enabled` | `true` | Workers Logs in the dashboard, kept after the request |
| `d1_databases`, `r2_buckets`, `kv_namespaces` | Each with a `binding` name and the resource's name and id | `wrangler <resource> create --update-config` writes the entry |
| `secrets.required` | The names of the secrets the Worker cannot run without | Only when every listed secret must exist before any deploy: `wrangler deploy` fails when one is missing, and local development then loads only the listed names from `.dev.vars` (checked 2026-10). An app that ships before an optional provider's keys exist leaves the key out of the file, and lists every secret's name in `.dev.vars.example` instead, which the deploy skill reads |
| `vars` | Non-secret configuration | Never a key or a token |
| `routes` | `{ "pattern": "<domain>", "custom_domain": true }` per hostname | Deploying creates the DNS record and the certificate |
| `workers_dev`, `preview_urls` | `false` once the custom domain serves | Avoids a duplicate public address |
| `triggers.crons` | Cron expressions | Only in a Worker that has a `scheduled` handler |
| `send_email` | `[{ "name": "EMAIL" }]` | Email Service sending binding |

`npx wrangler types` writes the `Env` interface for the bindings and secrets; commit the generated file and regenerate it when the configuration changes.

## Bindings and secrets in code

- Plain Workers and vinext: `import { env } from "cloudflare:workers"` anywhere on the server, or the `env` argument of the handler. The OpenNext adapter: `getCloudflareContext().env` from `@opennextjs/cloudflare`. Wrap the access in one module (`lib/cf.ts`, `lib/env.ts`) so the rest of the code does not know which adapter runs.
- A secret is read the same way as a binding (`env.SESSION_SECRET`); with Node.js compatibility `process.env` also sees secrets and `vars`, never bindings.
- Local development: `.dev.vars` (or `.env`, not both) next to the configuration holds the secrets as `KEY=value`; both files are gitignored, with a committed `.dev.vars.example` of names and comments only. `wrangler dev` and the framework's dev server simulate D1, R2 and KV locally under `.wrangler/`; `wrangler d1 migrations apply <db> --local` prepares the local database.
- Deployed: per-Worker secrets through Wrangler (`secret put`, `secret bulk <file>`, `deploy --secrets-file <file>`), each of which creates a new version and deploys it. Secrets Store, account-level secrets shared by Workers, is in open beta (checked 2026-10) and is not needed for one app.

## Next.js and other frameworks

- Read the framework guide for Next.js on Cloudflare's site before scaffolding; it names the path for a new app. When checked (2026-10) that path was vinext, a Vite-based implementation of the Next.js API surface, in beta: `npm create cloudflare@latest -- <name> --framework=next` scaffolds a Workers-ready app on it, `npx vinext check` then `npx vinext init` add it to an existing Next.js 16 app, bindings come from `cloudflare:workers`, and its compatibility dashboard at `vinext.dev/compatibility` lists what fails (partial prerendering and Babel-based transforms, when checked). The OpenNext adapter (`@opennextjs/cloudflare`) stays documented for an app with a gap vinext does not cover and is what the reference projects of this repository ran on; it needs `nodejs_compat`, `.open-next/worker.js` as `main`, `.open-next/assets` as assets, and `open-next.config.ts`.
- The scaffold's `package.json` scripts (`dev`, `build`, `preview`, `deploy`, `cf-typegen`) are the ones Workers Builds and the deploy skill call; keep their names.
- `NEXT_PUBLIC_*` values are inlined at build time: they belong in the build's variables (Workers Builds build variables, or the shell that runs `npm run build`), not in the Worker's secrets. vinext replaces only the literal `process.env.NEXT_PUBLIC_X` form (a Vite define); `process.env?.X` and `import.meta.env` are left as they are (checked 2026-10).
- The vinext scaffold declares an `images` binding for the framework's image optimization through Cloudflare Images (checked 2026-10): keep it only when the app uses `next/image`, with the Images row of tokens.md on the token; remove it when the app serves plain `<img>`. Whether a deploy with the binding needs the permission or costs anything was not checked.
- Astro, React Router, SvelteKit, TanStack Start, Vue, Hono and plain Vite apps are first-class through the Cloudflare Vite plugin, with the same configuration file and bindings; `npm create cloudflare@latest -- <name> --framework=<name>` scaffolds each (checked 2026-10).

## Plans and what they include

Illustrative, checked 2026-10 on the pricing pages, which are the source for a cost estimate:

| | Workers Free | Workers Paid (USD 5 per month) |
|---|---|---|
| Requests | 100,000 per day | 10 million per month included |
| CPU time | 10 ms per invocation | 30 million CPU ms per month included |
| D1 | 5 million rows read and 100,000 written per day, 5 GB | 25 billion read and 50 million written per month, 5 GB |
| R2 (own free tier, needs the R2 subscription added once) | 10 GB, 1 million class A and 10 million class B operations per month | the same free tier, then usage |
| Workers Builds | 3,000 build minutes per month, 1 at a time | 6,000 minutes, 6 at a time |
| Email Sending (beta) | not available | available |

A small app with a database, a bucket, a custom domain, logs and analytics runs on the Free plan; the move to Paid is for traffic, CPU-heavy work or Email Sending, and it is a spend the user confirms.
