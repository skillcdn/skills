# The reference stack and structure

A proposal, not a requirement: the stack the reference projects of this collection run on and the structure they converged on, with the reason for each choice, so that a new app starts from something proven and changes what the brief needs. Versions are never written here: `npm view <package> version` and the framework guide of the day say what is current.

## The stack

| Piece | Choice | Why, and the alternative |
|---|---|---|
| Language, runtime | TypeScript, strict; Node.js current LTS; npm with its lockfile | Every reference project; Workers Builds detects the package manager from the lockfile. pnpm is fine when the team prefers it |
| Framework | Next.js (App Router) on the path Cloudflare's framework guide names today: `developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/` (platform.md) | Server rendering for search engines, one codebase for pages and API routes, the reference projects. Astro for a content site with little interactivity; React Router or TanStack Start when the team is Vite-native |
| Styling | Tailwind (current major) with the design tokens declared in the stylesheet's theme block; `clsx` and `tailwind-merge` for class composition | Tokens in one place, utilities everywhere; no component library by default, headless primitives (Base UI, Radix) only when forms and dialogs multiply |
| Data | D1 with plain SQL migrations under `migrations/` and a thin typed module per entity under `lib/db/` | Zero dependency, the reference projects' shape; an ORM (Drizzle, with `migrations_pattern` in the configuration) when the model grows past a dozen tables |
| Files | R2 through its binding, public files behind a custom domain | Only when the brief keeps files |
| Sign-in | Google OAuth implemented directly with `jose` for tokens and sessions (auth.md) | Small, no vendor; Better Auth with its Cloudflare integration when many providers, 2FA or organizations are needed |
| Email | Cloudflare Email Service when the plan is Paid and the beta suits; a REST sender otherwise | Workers cannot do SMTP (platform.md) |
| Lint and format | The scaffold's ESLint and Prettier when it brings them; Biome when it brings nothing | One fast tool; keep what the framework's template configured |
| Tests | `node --test "tests/**/*.test.ts"` (Node.js strips types on a current LTS; `--experimental-strip-types` on an older one) | No framework to install; tests that hold a rule, not coverage |
| Analytics | Cloudflare Web Analytics (seo-geo.md) | Free, no cookies, no banner; a `track()` fan-out for pixels later |
| Design input | A design skill of the host when installed; otherwise "The look" below | A reviewed look beats a default one |

## Scaffold prompts

`npm create cloudflare@latest -- <slug> --framework=next` in the parent folder (its `--help` lists the flags that preset answers for a non-interactive shell). The Cloudflare prompts: TypeScript yes, git yes, deploy no. The framework's own creator then asks its questions: TypeScript yes, ESLint yes (keep what it brings), Tailwind yes, `src/` directory yes, App Router yes, import alias `@/*`, the default bundler. A commit the scaffold makes is kept; the skill's first commit goes on top.

## Files at the root

| File | Holds |
|---|---|
| `wrangler.jsonc` | platform.md "The configuration file"; the D1 entry carries `database_name` `<slug>-db` and a placeholder `database_id` (`00000000-0000-0000-0000-000000000000`) until the deploy skill creates the database and writes the real id; local development does not check it |
| `package.json` scripts | `dev`, `build`, `preview`, `deploy`, `cf-typegen` from the scaffold; add `typecheck` (`tsc --noEmit`), `lint`, `test`, `check` (typecheck, lint, test, build in that order), `db:migrate:local`, `db:migrate:remote`, `brand` (renders the icon and share images) |
| `.gitignore` | `node_modules`, the framework's output (`.next`, `.open-next`, `dist`), `.wrangler`, `.dev.vars`, `.env*` except `.env.example`, `.cf-token`, `*.tsbuildinfo`, `.brand-tmp/` (the brand render's scratch folder) |
| `.gitattributes` | `* text=auto eol=lf`, so that a Windows checkout does not trip the formatter with CRLF |
| `.editorconfig`, `.node-version` | Two-space indent, LF, UTF-8; the Node.js major the build pins |
| `.dev.vars.example` | Every secret's name with a comment on where it comes from and whether it is generated; no values |
| `.env.example` | The public build variables: `NEXT_PUBLIC_SITE_URL` (localhost in development; the deploy skill sets the live one), `NEXT_PUBLIC_CF_BEACON_TOKEN` (empty until the deploy skill creates the analytics site) |
| `.claude/settings.json` | Denies reads of secret files, allows the check commands and read-only git commands (working-agreement.md) |
| `CLAUDE.md`, `AGENTS.md`, `README.md`, `docs/` | working-agreement.md |

## The structure

```
src/
  app/              routes, layouts, route handlers (the framework's convention)
  components/       ui/ primitives, then one folder per feature; a dictionary next to the component it serves
  config/           single sources: i18n.ts (locales, formats), site.ts (name, URL from NEXT_PUBLIC_SITE_URL, copy per locale, owner), features.ts (switches per locale), pricing.ts when money exists
  lib/              pure logic: db/ (one module per entity, a client.ts), auth/, i18n.ts (locale from the request, URLs per locale), seo.ts (metadata helpers), cf.ts (bindings and secrets behind one function), analytics.ts
  styles/           globals.css with the tokens
migrations/         0001_init.sql, numbered, never edited after they are applied live
public/             favicon set, share images, brand/ (the SVG symbol and wordmark), site.webmanifest
scripts/brand/      render.mjs: the SVG to every PNG the metadata names
tests/              *.test.ts: dictionaries, boundaries, the rules
docs/               brief.md, brand.md, status.md, decisions.md
DEPLOY.md           written by the deploy skill at the launch
```

Rules the structure keeps: a fact lives in one `config/` file and is imported, never retyped (the locale list, the site URL, a price); money and dates are formatted by a function that takes the locale; the platform is reached only through `lib/cf.ts`, so that the adapter can change (`cloudflare:workers` on vinext, the adapter's context on OpenNext); a server module never imports a value from a client module.

The boundary test (`tests/boundaries.test.ts`): walk `src/`, find the modules whose first statement is `'use client'`, and fail when a module without that directive imports anything from one of them that is not a component (a PascalCase export) or a type; the reason is that such a value throws when called on the server in production and works in development.

## Mobile first

- Layout at 360 px wide first, then widen; no horizontal scrolling at any width; type at 16 px or larger in inputs so that phones do not zoom.
- Touch targets 44 px or more; the primary action within thumb reach at the bottom on phones; a bottom bar when there are more than three sections.
- `viewport-fit=cover` with safe-area insets; the theme color set; images with width and height to avoid layout shift.
- One column by default; a second column only when the viewport allows it, never by hiding content.
- Without a browser the agent can drive, these are checked by the user on a phone-width window and reported as not run.

## The look

Without a design skill, derive the look from the brief and write it to `docs/brand.md`:

- **Palette:** one background, one surface, one ink, one accent; tinted neutrals, never pure black or gray; contrast of 4.5:1 for text; a dark mode only when the audience expects it.
- **Type:** a family with the glyphs of every script the locales use (localization.md "Fonts"); headings and body from the same family unless the mood asks for a serif; sizes on a small scale (five steps).
- **Shape and motion:** one radius for everything (or none, as a statement); motion that settles once, no loops; no gradients, no nested cards, no icon tiles above headings.
- **Tone:** two or three words (calm, direct, warm), and what the copy never does (exclamation marks, jargon, false urgency).
- **Symbol:** one simple shape in the accent on the background, drawn as SVG, legible at 16 px; it becomes the favicon and the share image's mark.

Record each decision in `docs/brand.md` with its reason, so that a designer can change it on purpose.
