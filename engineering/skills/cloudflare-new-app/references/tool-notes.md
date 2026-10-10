# Tool notes: how the tools behaved in this skill's phases

By topic, in the order a run meets them. A fact that can go stale names where it was seen and the month; a fact about how the tools work carries no date and changes when a run finds it wrong. Platform-wide facts are in the shared pages.

## Scaffolding

- `npm create cloudflare@latest` is interactive; its prompts (a name, the framework, TypeScript, git, deploy now) are answered in the shell, and `--help` lists the flags that preset them for a non-interactive run. Answer "no" to deploying: the deploy skill does it with the user's word.
- The scaffold's `package.json` scripts are what Workers Builds and the deploy skill call; renaming them breaks the handover.
- The Next.js framework guide named vinext (beta) for a new app when checked (2026-10); its compatibility dashboard is the place to look when a feature misbehaves, and the OpenNext adapter is the proven fallback the reference projects ran on. A fresh run records which path it took in `docs/decisions.md`.
- Next.js 16 renamed the request interception file from `middleware` to `proxy` with a default export and removed `next lint` (release notes, checked 2026-10); the framework's own docs of the installed major say which file name and which lint setup apply.

## Local development

- The framework's dev server simulates the bindings through the adapter; a `.dev.vars` next to the configuration is loaded for secrets. A local D1 database lives under `.wrangler/` and is prepared with the migrations applied `--local`; the placeholder `database_id` in the configuration does not stop it.
- With `secrets.required` declared, local development loaded only the listed names from `.dev.vars` and the optional Google keys did not reach the app; the file was dropped and the names kept in `.dev.vars.example` (vinext scaffold, seen 2026-10).
- A long file written through a shell heredoc on Windows arrives truncated past a few thousand characters; write files with the editor's file tools and keep heredocs for short text (seen 2026-10).
- The vinext dev server listens on Vite's 5173 unless `server.port` is set in `vite.config.ts`; the example files and the callback URLs must name the port it really uses (seen 2026-10).
- `npm run preview` (the built Worker under `dist/server/`) has its own local D1 under `dist/server/.wrangler` with no tables, so every page answers 500 until the migrations are applied there (`wrangler d1 migrations apply <database name> --local --config dist/server/wrangler.json`); the vinext build also copies `.dev.vars` into `dist/server/` (seen 2026-10).
- Claude Code refuses its file tools on `.env*` files, `.env.example` included (seen 2026-10): write that file through the shell, and keep the public variables' names in `README.md` as well.
- vinext's route table at startup did not list the framework's `sitemap.ts` and `robots.ts` routes, yet it served `/sitemap.xml` and `/robots.txt`; check them with a request, not the table (vinext, seen 2026-10).
- Node.js 22.12 ran the scaffold, the dev server, the checks and the Worker preview; `--experimental-strip-types` is needed there for the tests and the brand script (seen 2026-10).
- OpenNext path only: the adapter's dev initializer must run only in development, not during the build, or the local runtime's lock collides with the build (seen 2026-09).
- A Windows checkout saves new files with CRLF unless `.gitattributes` says `eol=lf`; the formatter then flags every line of a new file (seen 2026-09).

## Rendering the brand files

- An SVG renderer needs the font files for every script embedded at render time; system fonts on the rendering machine are not enough for CJK on another machine. Keep the fonts out of the commit and pass their folder to the script (seen 2026-09).
- resvg renders a variable font (Noto Sans KR's variable TTF) at its default weight only; a bold title needs the static bold file (seen 2026-10).
- A renderer cannot write `.ico`; a small packer takes the PNG tiles. Browsers accept an SVG favicon, but `favicon.ico` is still requested at the root by default.

## Checks

- `node --test` runs `.test.ts` files directly on a current Node.js LTS; an older one needs `--experimental-strip-types`, and a `register` hook resolves `@/` path aliases in tests that import source modules (seen 2026-09).
- A server module that imports a function or value from a `'use client'` module throws at call time in production and works in development; the boundary test walks the imports and fails early (seen 2026-10).
- `npm run check` fails with `EBUSY` on `dist/client` while a local `wrangler dev` of the built output is still running; stop that server before the check (seen 2026-10). Stopping a backgrounded `npm run dev` or `npm run start` can leave child `node` and `workerd` processes holding the port and `dist/`; find them by port or name and end them by PID (seen 2026-10).
- Biome's `noDescendingSpecificity` rule flags a stylesheet ported from a mockup; turn the rule off for that file rather than reorder working CSS (seen 2026-10).
- On Windows, Git Bash rewrites an argument that starts with `/` into a Windows path (a `/path` label in a curl loop comes out mangled; `MSYS_NO_PATHCONV=1` or a leading `//` stops it), and Node's `fetch` to `localhost` resolves to `::1` while the local Worker listens on `127.0.0.1`: use the numeric address (seen 2026-10).
