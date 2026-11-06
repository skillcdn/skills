# The platform: what Workers means for an app

What the Cloudflare Workers runtime can and cannot do, the configuration an app on it needs, how code reaches bindings and secrets locally and live, which path a Next.js app takes, and what each plan includes. Read when an app is scaffolded, configured or deployed. Facts that move (a flag, a default, a plan's numbers, a beta) carry the month they were checked; the Workers documentation is the source.

## The runtime

- A Worker runs on V8 isolates at the edge, not in a Node.js process. Node.js built-ins (`node:crypto`, `node:buffer`, `node:fs`, `node:http`, and the rest the runtime supports) are available by default for a compatibility date of 2026-08-04 or later; an earlier date needs `nodejs_compat` among the compatibility flags (`compatibility_flags`, or `compatibilityFlags` in the typed file; checked 2026-10).
- No raw TCP mail: email goes through an HTTP API, Cloudflare Email Service (the `send_email` binding or its REST endpoint, Workers Paid, beta, checked 2026-10) or a third-party REST sender.
- The clock is UTC. A "today" that depends on where the user lives is computed with that locale's offset or time zone, never from the Worker's local time.
- CPU time, not wall time, is limited per invocation: 10 ms on the Free plan, 30 s default on Paid (checked 2026-10). A long AI call waiting on the network costs little CPU; heavy rendering or hashing does.
- A `fetch` from one Worker to another on the same zone by route or `workers.dev` fails (error 1042) unless the target runs on a Custom Domain or is called through a service binding. A cron that must call the app calls its custom domain. A framework's entry (vinext's fetch handler, checked 2026-10) exposes no `scheduled` handler: a change due at a time happens on the first request after it, or a small separate Worker with a cron calls the app's custom domain.
- Image optimization of a framework (such as `next/image`) is not a built-in: the framework guide says whether its path supports it, through Cloudflare Images or not; a plain `<img>` with width and height is always safe.
- Static assets (a Wrangler file's `assets.directory`; a typed project's Build Output) are served before the Worker runs and cached at the edge; the Worker handles the rest.

## The configuration file, and the CLI it chooses

A project carries one of two configuration generations, and the file decides the CLI (checked 2026-11):

| Generation | File | CLI | Written by |
|---|---|---|---|
| Typed (open beta) | `cloudflare.config.ts` at the project root: a TypeScript module built with `defineConfig`, `defineWorker`, `bindings` and `triggers` from `cf/config` | `cf`, a dev dependency of the project (`npx cf`; a global `npm install -g cf` hands each command to the project's copy) | `npm create cloudflare@latest -- <name> --framework=next` (through `create-vinext-app`), `cf init` for a new or an existing project, `cf migrate` on a Wrangler project |
| Wrangler | `wrangler.jsonc` (TOML works too), with `"$schema": "./node_modules/wrangler/config-schema.json"` for editor help | Wrangler, `npx wrangler` | `npm create cloudflare@latest` for a plain Worker (`--type=hello-world`), the framework scaffolds before 2026-11 (the 2026-10 vinext scaffold among them), the OpenNext adapter |

What follows from the file:

- `cf dev`, `cf build` and `cf deploy` read only the typed file. On a project that has only a Wrangler file they write a new configuration that ignores it (an automatic configuration, applied without asking where there is no terminal): never run them there; `cf migrate` converts a Wrangler project (`--dry-run` first), and `cf` resource and account commands (`cf d1 list`, `cf zones list`) work in any directory. Wrangler reads only its own file; on a typed project it runs only the commands `cf` lacks (live logs, a single secret), with the Worker's name passed to it.
- Loading `cloudflare.config.ts` needs Node.js 22.18 or later (`npm view cf engines` names the minors the installed `cf` accepts), and every `cf` command run inside the project loads it, so below that floor none runs: `cloudflare.config.ts loading requires Node.js v22.18.0 or higher`. `package.json` must carry `"type": "module"` (`cf init` and `cf migrate` set it; without it Node.js warns on every load, and with `commonjs` the load fails).
- A typed project's build writes the Build Output to `.cloudflare/output/v0/` (`config.json` with the mode, `workers/<name>/` with the bundle and the assets); `cf deploy --prebuilt` deploys it, `cf deploy --dry-run` builds and validates it without credentials. `cf build`, and `cf deploy` without `--prebuilt`, run the framework's own build command (`vite build`), not the `build` script of `package.json`; a project whose `build` script has extra steps keeps them by writing the script as those steps followed by `cf build` (`tsc -b && cf build`), while the deploy skill builds with the script and deploys with `--prebuilt`. Types: `npx cf workers types` writes `.cloudflare/types/index.d.ts` (the scaffold's `cf-typegen` script; the dev server and the build regenerate it), `tsconfig.json` includes `.cloudflare/types`, and the whole `.cloudflare/` is ignored by git.
- Local development of a typed project keeps its state (D1, KV, R2, the cache) under the project's `.cloudflare/state/v3/`, which `vite dev` and `vite preview` share; a `cf ... --local` command writes to the user's configuration directory instead (`%APPDATA%\xdg.config\cloudflare\state` on Windows) unless `--persist-to .cloudflare/state` points it at the project's (seen 2026-11).

What an app needs, in both generations:

| Need | Wrangler file | `cloudflare.config.ts` | Note |
|---|---|---|---|
| The Worker's name | `name` | `worker.name` | Must equal the Worker's name in the dashboard: Workers Builds refuses a mismatch |
| Entry and assets | `main`, `assets` with its `binding` (`ASSETS`) | `worker.entrypoint`, `worker.assets` (`htmlHandling`, `notFoundHandling`, `runWorkerFirst`), `ASSETS: bindings.assets()` in `worker.env` | Set by the framework's scaffold; the typed file names no assets directory, the build provides it |
| Compatibility | `compatibility_date`, `compatibility_flags` | `worker.compatibilityDate`, `worker.compatibilityFlags` | The day the project was created; moving it forward is a deliberate change: read the compatibility flags page for what it switches on |
| Logs | `observability.enabled: true` | `worker.observability: { enabled: true }` | Workers Logs in the dashboard, kept after the request |
| Resources | `d1_databases`, `r2_buckets`, `kv_namespaces`, each with a `binding` name and the resource's name and id | in `worker.env`: `DB: bindings.d1({ name, id })`, `BUCKET: bindings.r2({ name })`, `KV: bindings.kv({ id })` | `wrangler <resource> create --update-config` writes its entry; in the typed file the agent writes the id the create command returned |
| Secrets | `secrets.required`: the names the Worker cannot run without; `wrangler deploy` fails when one is missing, and local development then loads only the listed names from `.dev.vars` (checked 2026-10) | `NAME: bindings.secret()` in `worker.env` for every secret the code reads: the dev server passes only declared names from `.dev.vars`, and `cf deploy` refuses a version while a declared secret has no value on the Worker (`The following required secrets have not been set`), so the declaration is the required list; a secret once set stays for later versions (seen 2026-11) | An app that ships before an optional provider's keys exist leaves the name out of a Wrangler file and lists it in `.dev.vars.example`, which the deploy skill reads; in the typed file the name stays declared and the deploy sets it to an empty value, which the code treats as unset, until the key exists |
| Non-secret configuration | `vars` | `NAME: bindings.text("...")`, `bindings.json({...})` | Never a key or a token |
| The account | `account_id` | `accountId`, at the top level beside `worker` | Or `CLOUDFLARE_ACCOUNT_ID` in the environment, which both CLIs read first; needed only when the token sees several accounts |
| Custom domains | `routes: [{ "pattern": "<domain>", "custom_domain": true }]` per hostname | `worker.domains: ["<domain>", "www.<domain>"]` | Deploying creates the DNS record and the certificate |
| The free address | `workers_dev: false` once the custom domain serves; `preview_urls` stays `true` while branch previews are wanted | No key: the Worker's `workers.dev` address goes off through the subdomain call of automation.md, previews kept | Avoids a duplicate public address without losing the previews |
| Cron | `triggers.crons` | `worker.triggers: [triggers.scheduled({ schedule: "<cron>" })]` | Only in a Worker that has a `scheduled` handler |
| Email sending | `send_email: [{ "name": "EMAIL" }]` | `EMAIL: bindings.sendEmail()` | Email Service sending binding |

`npx wrangler types` or `npx cf workers types` writes the `Env` types for the bindings and secrets; a Wrangler project commits the generated file and regenerates it when the configuration changes, a typed project regenerates it under the ignored `.cloudflare/types`.

## Bindings and secrets in code

- Plain Workers and vinext: `import { env } from "cloudflare:workers"` anywhere on the server, or the `env` argument of the handler. The OpenNext adapter: `getCloudflareContext().env` from `@opennextjs/cloudflare`. Wrap the access in one module (`lib/cf.ts`, `lib/env.ts`) so the rest of the code does not know which adapter runs.
- A secret is read the same way as a binding (`env.SESSION_SECRET`); with Node.js compatibility `process.env` also sees secrets and `vars`, never bindings.
- Local development: `.dev.vars` (or `.env`, not both) next to the configuration holds the secrets as `KEY=value`; both files are gitignored, with a committed `.dev.vars.example` of names and comments only; a framework's public build variables are set in the shell or the build's variables, never in a local `.env` (Wrangler reads one as secrets; what the typed scaffold's dev server does with a local `.env` was not seen, 2026-11). The dev server simulates D1, R2 and KV locally: under `.wrangler/` on a Wrangler project, where `wrangler d1 migrations apply <db> --local` prepares the local database; under `.cloudflare/state/` on a typed project, where `npx cf d1 migrations apply <database id> --local --persist-to .cloudflare/state --dir ./migrations` prepares it, with the id the binding carries (a valid UUID placeholder until the deploy writes the real one: `cf` refuses a name, a binding name and the all-zero id).
- Deployed: per-Worker secrets through the project's CLI (Wrangler: `secret put`, `secret bulk <file>`, `deploy --secrets-file <file>`; `cf`: `deploy --prebuilt --secrets-file <file>`, `workers secrets bulk`), each of which creates a new version and deploys it. Secrets Store, account-level secrets shared by Workers, is in open beta (checked 2026-10) and is not needed for one app.

## Next.js and other frameworks

- Read the framework guide for Next.js on Cloudflare's site before scaffolding; it names the path for a new app. When checked (2026-11) that path was vinext, a Vite-based implementation of the Next.js API surface, in beta: the guide puts `create-vinext-app` first for a new app and `npx vinext check` then `npx vinext init` for an existing Next.js app, and `npm create cloudflare@latest -- <name> --framework=next` scaffolds the same app through `create-vinext-app` with the Cloudflare steps added (the compatibility date, the ignore list, the first commit). That scaffold is a typed project: `cloudflare.config.ts` with `entrypoint: "vinext/server/fetch-handler"`, `nodejs_compat`, `runWorkerFirst` for every path but `/_next/static/*`, and `ASSETS` and `IMAGES` bindings, with `cf` and the Cloudflare Vite plugin as dev dependencies (the 2026-10 scaffold wrote a Wrangler file and built to `dist/`, and a project of that generation stays a Wrangler project). Bindings come from `cloudflare:workers`, and the compatibility dashboard at `vinext.dev/compatibility` lists what fails. The OpenNext adapter (`@opennextjs/cloudflare`) stays documented for an app with a gap vinext does not cover and is what the reference projects of this repository ran on; it needs `nodejs_compat`, `.open-next/worker.js` as `main`, `.open-next/assets` as assets, and `open-next.config.ts`. The vinext dev server listens on Vite's port 5173, and `vite preview` of the built Worker (the scaffold's `start` script) on 4173; `server.port` in `vite.config.ts` moves the first, so that one port appears in the example files and the callback URLs (checked 2026-11).
- The scaffold's `package.json` scripts (`dev`, `build`, `start`, `preview`, `deploy`, `cf-typegen`) are the ones Workers Builds and the deploy skill call; keep their names. `deploy` is `vinext-cloudflare deploy`, which builds with Vite and deploys through `cf` on a typed project and through Wrangler on a Wrangler one, takes `--skip-build` and `--dry-run`, and has no secrets flag (checked 2026-11).
- `NEXT_PUBLIC_*` values are inlined at build time: they belong in the build's variables (Workers Builds build variables, or the shell that runs `npm run build`), not in the Worker's secrets. vinext replaces only the literal `process.env.NEXT_PUBLIC_X` form (a Vite define); `process.env?.X` and `import.meta.env` are left as they are (checked 2026-10).
- The vinext scaffold declares an images binding (`IMAGES: bindings.images()`, checked 2026-11) for the framework's image optimization through Cloudflare Images: keep it only when the app uses `next/image`, with the Images row of tokens.md on the token; remove it, with the `imagesOptimizer()` line of `vite.config.ts` that goes with it, when the app serves plain `<img>`. Whether a deploy with the binding needs the permission or costs anything was not checked.
- Astro, React Router, SvelteKit, TanStack Start, Vue, Hono and plain Vite apps are first-class through the Cloudflare Vite plugin, with the same bindings; `npm create cloudflare@latest -- <name> --framework=<name>` scaffolds each (checked 2026-10), and which configuration generation it wrote is read from the result.

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
