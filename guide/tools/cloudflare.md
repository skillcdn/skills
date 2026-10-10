# Cloudflare skills

How the skills that build for and deploy to Cloudflare (`cloudflare-…`) are written and kept in step, for authors. What they share at run time is the document set [`engineering/docs/cloudflare/`](../../engineering/docs/cloudflare/README.md), which agents read; this page says what goes there, what stays in a skill, and how the family is tested.

## The tool is the account, the CLI and the documentation

The skills drive a shell with Wrangler through `npx`, the Cloudflare REST API through `curl`, the git host, and the user's browser for the few steps only a signed-in person can take. They name Wrangler commands and API routes exactly, because those are the family's stable surface, and they name the dashboard's paths and permission labels with the month they were checked, because those move. A framework adapter, a package version, a plan's numbers and a beta's status are never written as facts to rely on: the skill says where to read them today (the framework guide, the registry, the pricing pages) and gives a dated number only to show the shape.

## What is shared and what stays in the skill

| In `engineering/docs/cloudflare/` | In the skill |
|---|---|
| `tokens.md`: the two token kinds, the dashboard steps, the permission list with what each is for, verification, storage, the sign-in fallback | What the skill asks the user for at intake, and when |
| `platform.md`: the runtime's limits, the configuration keys, bindings and secrets in code, the framework paths, the plans | The structure a new app gets, the pieces the build adds, the agreement it writes |
| `automation.md`: what the token does with the command for each, what a person does once in the dashboard | The order of the phases, what each verifies, what fails and what to do (`references/resources.md`), and the stops |

The test for a sentence: would it be true for the next skill of the family (a skill that moves a site to Cloudflare, one that adds a cron Worker, one that sets up email)? Then it belongs in the set. A sentence that holds for one skill's phase stays in that skill's reference; how a tool behaved in that phase goes in its `references/tool-notes.md`.

The set sits in the area's `docs/` because both skills are engineering skills: it travels with the engineering mount and plugin; a skill mounted alone cannot read its linked pages, and a copy lacks all of them, which each skill's Requirements say. The deploy skill includes `tokens.md` and `automation.md`; the new-app skill includes `platform.md`; the rest is linked from the phase that reads it. A change to an included page changes the served digest of the skill that includes it: edit deliberately.

## The seam between the two skills

The new-app skill hands over at its launch phase with the project path, the token, the domain answer, the secrets by name (generated or held by the user, with the steps for each) and the repository answer; the deploy skill stays general and takes any project with a Wrangler configuration or a framework the platform page names. A change to what the deploy skill asks at intake is mirrored in the new-app skill's intake, so that the user is asked once; a change to the agreement's deploy section (`DEPLOY.md`) is made in the deploy skill, which writes it.

## Facts are dated

A dashboard path, a permission label, a plan's included usage, a product's beta status, an adapter's name, a command's flag: each sentence that states one names its source and the month at the end, and changes when a run finds it wrong. The permissions reference and the pricing pages are quoted by their path on `developers.cloudflare.com`; a page's Markdown is at its URL with `index.md` appended, which is how the pages were read when this family was written (2026-10).

## Examples name no one

Account ids, zone ids, domains, Worker names and resource names in the set and the skills are placeholders (`<account id>`, `<domain>`, `<name>-db`). No run's product, person or customer; what the reference projects taught is written as behavior ("a CLI secret change once reverted the live code of a connected Worker"), never as their names.

## Testing

The new-app skill is exercised by a fresh agent building a stand-in app from one request, its intake answered in one line each, through the plan and the look to a passing check; the deploy skill by a fresh agent putting a project live on a throwaway Worker in the user's account, with a token the user supplies at the checkpoint, and deleting the resources afterwards (`wrangler delete`, `d1 delete`, `r2 bucket delete`), so that nothing of a run stays in the account. A run that needs the account is a spend of the user's attention and possibly money (a domain, a plan) and is confirmed as such; a run to the token checkpoint costs nothing. A change to either skill is dry-read before it is pushed; a run is read against the files as `skillcdn-skill-verification` says; what the platform or a tool did differently goes into the sentence of the set it bears on.
