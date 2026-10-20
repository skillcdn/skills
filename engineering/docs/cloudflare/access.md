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
| Per-Worker Access | Workers & Pages > the Worker > the **Access** tab > "Protect this Worker with Access". The dialog asks which traffic ("Preview only", the default, which leaves the production address public; "All traffic", which an operator's Worker needs), who may open it (a policy list; "Cloudflare account" members are allowed by default, "Add policy" adds emails) and the session duration. The tab then shows the Worker's policies, how policies match (hostname policies first, then Worker policies, then account policies) and the Application values, the AUD tag and the JWKS URL, each with a copy button (dashboard, seen 2026-10) | Every hostname the Worker serves: workers.dev, custom domains, routes, previews; the preview-only scope is the account-wide policy named "Cloudflare Workers Preview URLs" | The screens are a Worker of their own (the operator dashboard the skills build), which makes the whole Worker private without a domain |
| Self-hosted application | Zero Trust > Access controls > Applications > Create new application > Self-hosted and private > Add public hostname, with a path such as `/admin`; or `POST /accounts/<id>/access/apps` with `type` `self_hosted`, `domain` `<host>/admin`, `policies` | The hostname and path named, which must be in an active zone of the account | The screens live inside the public site on a custom domain |

A protected Worker that is reached before Access is enabled is public: the Worker's own token check below is what closes that window, so the check ships before the first deploy and the protection is enabled right after it.

The policy: the default "Cloudflare account" entry allows the members of the Cloudflare account, who sign in with their Cloudflare login, which suits a one-person operator and needs no login method set up; an operator without a Cloudflare account gets an added policy with Include "Emails" (or "Emails ending in" for a company domain) and the one-time PIN login. Session duration a day or shorter. Policies are Include (any match), Require (all) and Exclude (none); an application is deny by default (Access policies page, checked 2026-10). "Manage Access" on the Worker's Access tab edits the scope and the policies, and the application also appears under Zero Trust > Access controls > Applications. The AUD tag and the JWKS URL (`https://<team>.cloudflareaccess.com/cdn-cgi/access/certs`, whose host is the team domain) are on the Worker's Access tab under Application values, so the person copies them from there; an account with no Zero Trust organization got one when Access was enabled, its team name taken from the account's workers.dev subdomain (seen 2026-10).

## Verifying the token at the origin

Access attaches the application token to every authenticated request as the header `Cf-Access-Jwt-Assertion` (and as the cookie `CF_Authorization` on browser requests, which is not guaranteed to be passed). The Worker verifies it on every request, with `jose`:

- Keys from `https://<team>.cloudflareaccess.com/cdn-cgi/access/certs` (a JWKS; Access rotates keys about every six weeks and the previous keys stay valid for seven days, so the keys are fetched, cached briefly and never hard-coded), algorithm RS256.
- Claims: `iss` equals `https://<team>.cloudflareaccess.com`; `aud` contains the application's AUD tag; `exp` in the future (the library checks it). A user token carries `email`, `sub`, `country` and `identity_nonce`; a service-token token carries `common_name` (the token's client id) and an empty `sub`, and no `email` (application token page, checked 2026-10).
- The team domain and the AUD tag are secrets of the Worker (`ACCESS_TEAM_DOMAIN`, `ACCESS_AUD`); when either is unset the Worker answers 503 with a one-line "not configured" page and serves nothing else. The only exception is an explicit development switch read from the local secrets file, which a deploy never carries. A token that fails verification answers 403, and so does a verified `email` that is not on the Worker's own list of operators, which the Access policy mirrors with the "Emails" selector. The verified `email` is the actor written in the audit log.

The team domain is read from the `Location` header of an unauthenticated request to the protected address once Access is on (`curl -sI https://<address>/` answers a redirect to `https://<team>.cloudflareaccess.com/cdn-cgi/access/login/...`), or from the JWKS URL on the Worker's Access tab, whose host it is, or from Zero Trust > Settings > Custom Pages. The AUD tag is read from the application: `GET /accounts/<id>/access/apps` answers each application with its `aud` field (Access: Apps and Policies Read; checked 2026-10), or the person copies it from the application's Overview page.

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
