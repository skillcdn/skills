# Access: protecting an operator's screens with Cloudflare Access

How a Worker that only the operator may open is put behind Cloudflare Access: what Access does, the one-time setup of a Zero Trust organization, the two ways to protect a Worker (the per-Worker setting that covers every hostname, or a self-hosted application on a path of a domain), the login method for a small team, how the Worker verifies the token Access attaches so that it fails closed when the protection is missing, service tokens for machines, and what the API token needs. Dashboard paths and plan limits move; each carries the month it was checked, and the Cloudflare One documentation is the source.

## What Access is

Access is Cloudflare's identity layer in front of a hostname: a request to a protected address is sent to a login page first, the person signs in with an identity provider or a one-time code sent to their email, and only a request that carries Access's own signed token reaches the origin. The origin never sees a password, holds no session store and runs no login code; it checks the token. The Zero Trust Free plan covers a small team at no cost (Cloudflare's pages say up to 50 users; checked 2026-10 on the Access product page, where the exact wording should be re-read before relying on the edge). Authentication events are logged by Cloudflare per user and per application.

## The one-time setup

Access lives in a Zero Trust organization with a team name (`<team>.cloudflareaccess.com`). Until one exists, every Access API call answers `access.api.error.not_enabled` and tells the caller to visit the dashboard and select Enable Access (seen 2026-10 on an account without one). A person creates it once: Cloudflare dashboard > Zero Trust, choose a team name, choose the Free plan (the onboarding asks for a plan and a payment method only for paid plans; checked 2026-10). Then the login method: Zero Trust > Integrations > Identity providers > Add new identity provider > One-time PIN (dashboard, checked 2026-10), or `POST /accounts/<id>/access/identity_providers` with `{"type":"onetimepin","config":{}}` when the token has the permission below. With the one-time PIN a person types their email on the login page, receives a code that lasts ten minutes, and is let in only when a policy allows that email; an address no policy allows gets no email.

## Protecting a Worker

Two forms; the first needs no domain.

| Form | Where | Covers | Choose when |
|---|---|---|---|
| Per-Worker Access | Workers & Pages > the Worker > Settings > Domains & Routes > Enable Cloudflare Access on the workers.dev row (and on Preview URLs) | Every hostname the Worker serves: workers.dev, custom domains, routes, previews; the policy is a reusable one named `<worker-name> - Production`, previews share one account-wide policy named "Cloudflare Workers Preview URLs" (Workers changelog, 2025-12; blog, 2026-08; checked 2026-10) | The screens are a Worker of their own (the operator dashboard the skills build), which makes the whole Worker private without a domain |
| Self-hosted application | Zero Trust > Access controls > Applications > Create new application > Self-hosted and private > Add public hostname, with a path such as `/admin`; or `POST /accounts/<id>/access/apps` with `type` `self_hosted`, `domain` `<host>/admin`, `policies` | The hostname and path named, which must be in an active zone of the account | The screens live inside the public site on a custom domain |

A protected Worker that is reached before Access is enabled is public: the Worker's own token check below is what closes that window, so the check ships before the first deploy and the protection is enabled right after it.

The policy: Allow, Include "Emails" with the operator's addresses (or "Emails ending in" for a company domain), Session Duration a day or shorter. Policies are Include (any match), Require (all) and Exclude (none); an application is deny by default (Access policies page, checked 2026-10). The dashboard's Manage Cloudflare Access on the Worker edits the policy, and the Access application it created appears under Zero Trust > Access controls > Applications with its Application Audience (AUD) tag under Overview.

## Verifying the token at the origin

Access attaches the application token to every authenticated request as the header `Cf-Access-Jwt-Assertion` (and as the cookie `CF_Authorization` on browser requests, which is not guaranteed to be passed). The Worker verifies it on every request, with `jose`:

- Keys from `https://<team>.cloudflareaccess.com/cdn-cgi/access/certs` (a JWKS; Access rotates keys about every six weeks and the previous keys stay valid for seven days, so the keys are fetched, cached briefly and never hard-coded), algorithm RS256.
- Claims: `iss` equals `https://<team>.cloudflareaccess.com`; `aud` contains the application's AUD tag; `exp` in the future (the library checks it). A user token carries `email`, `sub`, `country` and `identity_nonce`; a service-token token carries `common_name` (the token's client id) and an empty `sub`, and no `email` (application token page, checked 2026-10).
- The team domain and the AUD tag are secrets of the Worker (`ACCESS_TEAM_DOMAIN`, `ACCESS_AUD`); when either is unset the Worker answers 503 with a one-line "not configured" page and serves nothing else. The only exception is an explicit development switch read from the local secrets file, which a deploy never carries. A token that fails verification answers 403, and so does a verified `email` that is not on the Worker's own list of operators, which the Access policy mirrors with the "Emails" selector. The verified `email` is the actor written in the audit log.

The team domain is read from the `Location` header of an unauthenticated request to the protected address once Access is on (`curl -sI https://<address>/` answers a redirect to `https://<team>.cloudflareaccess.com/cdn-cgi/access/login/...`), or from Zero Trust > Settings > Custom Pages, where the dashboard shows it. The AUD tag is read from the application: `GET /accounts/<id>/access/apps` answers each application with its `aud` field (Access: Apps and Policies Read; checked 2026-10), or the person copies it from the application's Overview page.

## Service tokens

For a machine that must call the protected Worker (another Worker, a job on a server): Zero Trust > Access controls > Service credentials > Service Tokens > Create Service Token, or `POST /accounts/<id>/access/service_tokens`; the client sends `CF-Access-Client-Id` and `CF-Access-Client-Secret`, the policy for it has the action Service Auth with the selector Service Token, and the secret (`cfast_` prefix) is shown once (service tokens page, checked 2026-10). A dashboard Worker that runs its own cron needs none: the scheduled handler runs inside the Worker.

## What the API token needs

The Cloudflare API token of [tokens.md](tokens.md) gets these rows when Access is driven through the API; without them the person does the dashboard steps above and pastes the AUD tag.

| Scope | Permission | For |
|---|---|---|
| Account | Access: Apps and Policies | Read to read the AUD tag, which is all the admin skill needs; Edit only when the agent creates applications and policies itself |
| Account | Access: Organizations, Identity Providers, and Groups | Edit only for adding the one-time PIN login method through the API, removed afterwards; the team domain is read without it |
| Account | Access: Service Tokens | Edit only when a machine must call the Worker |

The API's permission list names them "Access: Apps and Policies Write" and the like; the dashboard shows Read and Edit (checked 2026-10).
