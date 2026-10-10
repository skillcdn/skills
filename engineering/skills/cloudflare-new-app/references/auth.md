# Sign-in

The default sign-in, how it is built so that it stays off until its keys exist, the session, the guest path that keeps the core action usable before sign-in, and when to reach for more.

## The guest path comes first

The brief's core action (saving, writing, booking) works on one device before anyone signs in: a random device id in a one-year cookie groups what a guest did on this device, and signing in claims it (`lib/db/claim.ts`: everything with this device id, or the same verified email, moves to the member). Sign-in is what makes the data follow the person across devices, not what unlocks the app; the plan says so in one line. The brief may name an action that needs an account (paying, publishing under a name), and only that action waits for sign-in. When the core action must be one per person and enforced (a vote, a ranking), browsing is the guest path and the action waits for sign-in, and the plan's line says so instead of "saving works before signing in"; an entry that only needs a name and a contact (a sign-up, a booking, a comment) takes them typed in on the guest path and is claimed on sign-in. This is also why an app ships before its sign-in keys exist.

## The default: Google, implemented directly

- OAuth 2.0 authorization code flow, no SDK: `lib/auth/google.ts` builds the authorization URL (`openid email profile`, `prompt=select_account`), exchanges the code at the token endpoint, and verifies the ID token with Google's JWKS through `jose` (issuer and audience checked). Three route handlers: `/api/auth/google/login`, `/api/auth/google/callback`, `/api/auth/logout`; `/api/me` returns the signed-in user for the client.
- `googleConfigured()` is true only when both `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` exist; the sign-in button renders only then, so that the app ships before the keys exist and turns the feature on when they arrive. Placeholder values in the local `.dev.vars` show the button for the layout; the round trip needs real keys. The keys come from Google Cloud Console (automation.md's second table has the clicks): an OAuth client of type Web application, with the authorized redirect URIs `https://<address>/api/auth/google/callback` for every live address and `http://localhost:<port>/api/auth/google/callback` for development; the deploy skill asks for them by name with these steps once the address is known.
- The `state` is a signed token (`jose`, HS256 with `SESSION_SECRET`, ten minutes) that carries the return path, the locale and a hash of the client IP, and is also set as a cookie. The callback accepts it when the cookie matches, and, when there is no cookie at all, when the signature, the expiry and the IP hash match: an in-app browser (a chat app, a social app) hands the callback to the system browser with none of the cookies, and without this fallback sign-in from those apps fails and loses the locale. A mismatch fails closed.
- Members live in D1 (`members`: id, email unique, name, picture, provider ids, created and last-sign-in times); the same email across providers is one member.

## The session

A signed JWT (`jose`, HS256, `SESSION_SECRET`) in an `HttpOnly`, `Secure`, `SameSite=Lax` cookie with a 30-day life, carrying the member id and the display fields the header needs; `lib/auth/session.ts` signs, reads and clears it; a missing or short secret in local development falls back to a fixed insecure key and logs a warning once. The admin, when the app has one, is a separate cookie signed with `ADMIN_SECRET`, opened with `ADMIN_PASSWORD`, on `/admin` routes that are `noindex` and outside locale handling; Cloudflare Access on `/admin` is the heavier alternative when a team signs in.

## Markets and providers

`localeFeatures(locale).login` says which providers a market shows: Google everywhere; a regional provider (LINE for Taiwan and Japan, Kakao for Korea) when the brief or the market asks, each with its own keys, its own callback and the same signed-state scheme. A provider that does not return an email gets a synthetic one (`<id>@<provider>.local`) that is never used as a claim key. Kakao Login (checked 2026-10): the two values are the REST API key and its client secret (on by default), the redirect URI is set under the app's platform keys for the REST API key, the consent items a new app gets without review are the nickname and the profile image, so there is no email and the synthetic id applies; the dashboard steps are in automation.md's second table.

## Email link sign-in

When the brief asks for email: a single-use token in D1 with a 15-minute expiry, sent by the app's email sender (platform.md names what the plan allows), verified by a route that creates the session; rate-limited per address. It needs a sending domain and the sender's key, so it waits for the launch.

## A test sign-in without a provider

When the user wants to try sign-in before any provider's keys exist: a nickname plus a code. The code is a secret (`TEST_LOGIN_CODE`) in letters and digits, because a password field under a Korean input method refuses Hangul (seen 2026-10), only a request that carries it creates or opens a member, those members carry `provider = 'test'` so that one statement deletes them with what they made, what they create is marked as test on the pages, and deleting the secret closes the door. Never the default; named in the delivery and in `DEPLOY.md`, and off before the site is announced. Sample accounts loaded from a seed (`provider = 'sample'`, ids outside the real sequence) never hold a session.

## When to use a library

Better Auth, with its Cloudflare integration for D1 and Workers, when the brief needs several providers, two-factor, organizations or passkeys (checked 2026-10); its schema replaces the `members` table and its routes replace the handlers above. Not for a single Google sign-in: the direct implementation is a few hundred lines with no dependency to keep up with.
