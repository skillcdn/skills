# Tool notes: how the tools behaved in this skill's phases

By topic, in the order a run meets them. A fact that can go stale names where it was seen and the month; a fact about how the tools work carries no date and changes when a run finds it wrong. Platform-wide facts are in the shared pages.

## Scaffolding

- `npm create cloudflare@latest` is interactive; its prompts (a name, the framework, TypeScript, git, deploy now) are answered in the shell, and `--help` lists the flags that preset them for a non-interactive run. Answer "no" to deploying: the deploy skill does it with the user's word.
- The scaffold's `package.json` scripts are what Workers Builds and the deploy skill call; renaming them breaks the handover.
- The Next.js framework guide named vinext (beta) for a new app when checked (2026-10); its compatibility dashboard is the place to look when a feature misbehaves, and the OpenNext adapter is the proven fallback the reference projects ran on. A fresh run records which path it took in `docs/decisions.md`.
- Next.js 16 renamed the request interception file from `middleware` to `proxy` with a default export and removed `next lint` (release notes, checked 2026-10); the framework's own docs of the installed major say which file name and which lint setup apply.

## Local development

- The framework's dev server simulates the bindings through the adapter; a `.dev.vars` next to the configuration is loaded for secrets. A local D1 database lives under `.wrangler/` and is prepared with the migrations applied `--local`; the placeholder `database_id` in the configuration does not stop it.
- OpenNext path only: the adapter's dev initializer must run only in development, not during the build, or the local runtime's lock collides with the build (seen 2026-09).
- A Windows checkout saves new files with CRLF unless `.gitattributes` says `eol=lf`; the formatter then flags every line of a new file (seen 2026-09).

## Rendering the brand files

- An SVG renderer needs the font files for every script embedded at render time; system fonts on the rendering machine are not enough for CJK on another machine. Keep the fonts out of the commit and pass their folder to the script (seen 2026-09).
- A renderer cannot write `.ico`; a small packer takes the PNG tiles. Browsers accept an SVG favicon, but `favicon.ico` is still requested at the root by default.

## Checks

- `node --test` runs `.test.ts` files directly on a current Node.js LTS; an older one needs `--experimental-strip-types`, and a `register` hook resolves `@/` path aliases in tests that import source modules (seen 2026-09).
- A server module that imports a function or value from a `'use client'` module throws at call time in production and works in development; the boundary test walks the imports and fails early (seen 2026-10).
