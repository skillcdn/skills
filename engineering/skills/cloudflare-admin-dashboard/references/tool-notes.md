# Tool notes: how the tools behaved in this skill's phases

By topic, in the order a run meets them. A fact that can go stale names where it was seen and the month; a fact about how the tools work carries no date and changes when a run finds it wrong. The platform-wide facts are in the Cloudflare pages of the pack; these are the edges of this skill's own phases.

## Access

- Every Access API call on an account without a Zero Trust organization answers `access.api.error.not_enabled` with the instruction to enable Access in the dashboard; the organization is created by a person, and the API token needs the Access rows before it can read the applications (seen 2026-10).
- The per-Worker setting (Workers & Pages > the Worker > Settings > Domains & Routes > Enable Cloudflare Access) covers every hostname of the Worker and creates a reusable policy named `<worker-name> - Production`; preview URLs share one policy across the account (Workers changelog, 2025-12; checked 2026-10).
- The token arrives in `Cf-Access-Jwt-Assertion`; the cookie is not guaranteed on every request, so the guard reads the header only.

## Workers and D1

- Two Workers bind the same D1 database by id; the admin's `database_name` and `database_id` are copied from the site's configuration, and `npx wrangler d1 migrations apply` with the admin's configuration keeps its own migrations folder and table apart from the site's.
- D1 refuses a `LIKE` or `GLOB` pattern longer than 50 bytes and fails the whole query; "contains" search uses `instr()` (seen 2026-09 on a list that answered 500 for long search terms).
- Local development never fires a cron; `curl "http://localhost:8788/cdn-cgi/local/scheduled?cron=*+*+*+*+*"` against the dev server runs the scheduled handler by hand, and an empty `crons` array in the configuration removes every trigger on deploy (cron triggers page, checked 2026-10).
- A scheduled handler has the Worker's CPU limit per invocation; a sync that reads many pages keeps its calls sequential per account and its writes in batches, and `waitUntil` after a response is good for about thirty seconds, which is too short for a long sync (seen 2026-09).
- A CLI secret change on a Worker that Workers Builds deploys can roll the live code back to the version active at that moment; the deploy status is checked after each change (seen 2026-09).

## Dashboards in production

- Figures bucketed by UTC in one place and by the business day in another made two tabs disagree by a day; one zone in one helper used everywhere was the fix (seen 2026-09).
- A chart cut by row count instead of by date hid the empty days and shifted the x axis; filling empty days and cutting by date fixed it.
- A revenue sync that wrote a partial page cap result zeroed the oldest days; the reader throws at the cap now (seen 2026-08).
- A `'use client'` dashboard component that imported a value from a server module threw in production and worked in development; the admin here renders on the server and ships no client component, which removes the class of bug (seen 2026-10).
- A link from the admin to a customer's own page is a bearer link and can have side effects (work started on the customer's behalf, a locale cookie changed); the admin renders a read-only view instead.
- A provider that refuses calls (an exhausted balance) can make an app serve fallback content silently, and usage rows at zero tokens and zero cost are the signal; the costs panel flags those rows and the digest counts them.
