---
name: cloudflare-new-app
description: Builds a new web app from an idea and puts it live on Cloudflare. Asks a few plain questions anyone can answer (what it does and for whom, which languages, whether people sign in, a domain or not, the look), plans it, proposes a look, then builds a TypeScript app on the path Cloudflare's framework guide recommends that day (Next.js by default), mobile-first, every language designed in from the first commit, ready for search engines and AI engines (metadata, sitemap, hreflang, structured data, llms.txt), with a share image and favicon set made from its brand, sign-in, a database, analytics, tests and one check, and writes the working agreement a team of developers, planners and designers keeps working under (CLAUDE.md, AGENTS.md, README, status, decisions). Hands over to cloudflare-deploy for the launch. Use when the user wants a new app, site, service or landing page made and put online, with no expertise needed. For a project that exists and only needs to go live, cloudflare-deploy is the skill.
license: MIT
compatibility: Needs a shell with Node.js (the current LTS), npm and git, network access to the npm registry and to Cloudflare's documentation, and, for the launch, what cloudflare-deploy needs. A browser the agent can drive is optional, for looking at the pages. Works in any agent that can run a shell and write files.
metadata:
  author: skillcdn
  version: "1.1"
  tools: cloudflare
skillcdn:
  include:
    - references/intake.md
    - /engineering/docs/cloudflare/platform.md
  translations:
    ko:
      title: 아이디어에서 Cloudflare 위의 새 웹앱까지
      description: 아이디어 하나로 새 웹앱을 만들어 Cloudflare에 올립니다. 누구나 답할 수 있는 몇 가지 쉬운 질문(무엇을 하는 앱인지와 누가 쓰는지, 어떤 언어들인지, 로그인이 필요한지, 도메인이 있는지, 어떤 느낌인지)을 묻고, 계획을 세우고, 디자인을 제안한 뒤, 그날 Cloudflare 프레임워크 가이드가 권하는 방식(기본은 Next.js)으로 TypeScript 앱을 만듭니다. 모바일 우선, 첫 커밋부터 모든 언어를 설계에 넣고, 검색엔진과 AI 엔진을 위한 준비(메타데이터, 사이트맵, hreflang, 구조화 데이터, llms.txt), 브랜드로 만든 공유 이미지와 파비콘 세트, 로그인, 데이터베이스, 분석, 테스트와 하나의 검사 명령까지 갖추고, 개발자·기획자·디자이너가 계속 함께 일할 작업 약속(CLAUDE.md, AGENTS.md, README, 상태, 결정 기록)을 씁니다. 출시는 cloudflare-deploy에 넘깁니다. 새 앱·사이트·서비스·랜딩페이지를 만들어 온라인에 올려 달라고 할 때 쓰세요. 이미 있는 프로젝트를 올리기만 할 때는 cloudflare-deploy가 맞습니다.
---
# A new web app, from an idea to live

What goes in: an idea in the user's words and the answers to a few plain questions. What comes out: a git repository with a TypeScript web app that runs locally and passes one check, mobile-first, speaking every language the user named, ready for search and AI engines, with its share image and favicon set, sign-in, a database, analytics and tests; a brief, a look and a working agreement that let developers, planners and designers keep working in it with their own agents; and, through `cloudflare-deploy`, the app live at its address with deploys on every push. The user never needs to know the stack: every technical choice is derived from their answers, shown with its reason, and changed when they ask.

## How the user is involved

- **Questions:** one message at the start, the ones in [intake.md](references/intake.md) that the request leaves open, each in plain words. Everything else is derived and shown in the plan.
- **Checkpoints:** the plan, before any file of the project is written; the look, with the home page in front of them, before the pages are built on it; then the deploy skill's own stops (a purchase, the first deploy, every push). Each is one short message in plain words, with a recommendation, and one word continues.
- **Go-ahead:** when the user says to go ahead alone, the questions with defaults are not asked (the defaults are shown in the plan) and the look is reported instead of approved. The plan, and every stop of the deploy skill, hold in every mode.
- **Changes mid-run:** applied from that point. A changed plan after the build rewrites the parts it touches, not the whole app.

## Requirements

| What | Used for |
|---|---|
| A shell with Node.js (the current LTS, or an older LTS the scaffold accepts: say which in the first message and pin it in `.node-version`), npm and git | Scaffolding, running, checking, committing |
| Network access to the npm registry and to `developers.cloudflare.com` | Packages, and the framework guide that names the path of the day |
| Optional: a browser the agent can drive, or a screenshot tool | Looking at the pages at the design checkpoint and for the layout verdicts; without one, the user looks at the local address on a phone-width window and the layout verdicts are reported as not run |
| Optional: a design skill the host has installed (one that reviews or crafts interfaces) | The look; without one, [stack.md](references/stack.md) "The look" carries the method |
| For the launch: what `cloudflare-deploy` requires (the token, the account) | Prepared at intake so that the launch does not wait |

Check these before the first message. Without Node.js or git, stop and say what to install. Without network, stop: nothing can be scaffolded.

What the Cloudflare skills share is the area's document set [`engineering/docs/cloudflare/`](/engineering/docs/cloudflare/README.md). [platform.md](/engineering/docs/cloudflare/platform.md) (what the runtime can do, the configuration, bindings and secrets, the framework paths, the plans), which every run reads, is included and arrives with this skill wherever SkillCDN serves it. [tokens.md](/engineering/docs/cloudflare/tokens.md) (the steps the user takes for a token) is linked from the intake and [automation.md](/engineering/docs/cloudflare/automation.md) from the launch; both are read with `read_repo_file` through the repository or the engineering connection, or as files under `docs/cloudflare/` of the engineering plugin, or at `engineering/docs/cloudflare/` of a checkout of this repository. A copy of this skill's directory lacks all three, and a mount of it alone lacks the linked two: say so in the first message, fetch what is missing from `engineering/docs/cloudflare/` of the repository this skill comes from (for this collection, `github.com/skillcdn/skills`) where the agent can, and otherwise run on this skill's own files, which carry its workflow and its rules. The launch is the `cloudflare-deploy` skill of the same area; where it cannot be loaded, the delivery says so and gives the user its name and address.

## Inputs

| Input | Source |
|---|---|
| The idea: what the app does, for whom, who runs it | The request; the missing half asked |
| The languages, the main one first | Asked; the default is the language the user wrote in |
| Sign-in, and how | Asked; the default is Google, no sign-in when nothing is kept per person |
| The domain: owned, to buy, or none yet | Asked; none yet is the default |
| The look: a site they like, colors, a mood, or "propose one" | Asked; the default is a proposal |
| Everything else | Derived and shown in the plan: the app's name and folder, the pages (with the ones every app gets), the data, the stack and its adapter (platform.md), the structure (stack.md), the brand files, analytics, the team facts (who works in the repository, the language of its documents), what the user prepares for the launch |

The questions are written in intake.md, in the words to use; intake.md also says what each answer derives and holds the plan message.

## Workflow

Each phase produces a named artifact and ends with one line to the user. The build's pieces are reported, not approved one by one.

### Phase 1: Intake

Produces the **brief** as text in the agent's notes: the idea in a paragraph, who uses it and on what, who runs it, the languages, the pages and what each does, what is kept (the data, in plain words), sign-in, the domain, the look direction, and what is out of scope for the first version. Ask the questions of intake.md in one message, derive the rest. Tell the user to create the Cloudflare token now with the steps of [tokens.md](/engineering/docs/cloudflare/tokens.md), saved as `.cf-token` in the folder the project will be created in, so that the launch does not wait; the run goes on while they do. The brief is written to `docs/brief.md` once the project exists (phase 4).

### Phase 2: Plan

Produces the **plan**, shown at the checkpoint with the message intake.md gives, and kept in the brief. From the brief: the name and the folder, the pages and their routes (intake.md "Pages every app gets"), the data model, the locales, sign-in and the guest path, the stack with the adapter the framework guide names today (platform.md "Next.js and other frameworks"), the folder structure and packages ([stack.md](references/stack.md)), the brand files, analytics, the tests, the agreement, the launch steps and what they cost (platform.md "Plans"). The technical choices are one phrase each, with the reason; the user may change any, including the name.

### Phase 3: Design

Produces the **look** (`docs/brand.md`, the tokens in the stylesheet, the brand symbol as SVG) and the home page built on it. Derive a palette, type per script, spacing, radius, motion and tone from the look direction (stack.md "The look"); when the host has a design skill installed, use it for this phase and record what it decided in `docs/brand.md`. Scaffold the project (phase 4, step 1) so that the home page can be rendered, build the home page, and show it: a screenshot when a browser is available, otherwise the local address with "run `npm run dev` in the project folder, then open it on your phone or in a narrow window", because a server the agent starts ends with its turn. Checkpoint: "Here is the look: <three words>, <palette>, <type>. The alternative would be <one line>. Keep it?"

### Phase 4: Build

Produces the **app**. In this order, each step reported in a line and verified before the next:

1. Scaffold with the path platform.md names, as stack.md "Scaffold" says (the command and its flags, what it makes, what is moved, the versions pinned, the branch renamed), keep the commit the scaffold makes when it makes one, write `docs/brief.md`, then the project files of stack.md "Files at the root": `.gitignore`, `.gitattributes`, `.editorconfig`, the Node.js version file, `.dev.vars.example`, `.claude/settings.json`, and the scripts `check`, `typecheck`, `lint`, `test`.
2. The structure of stack.md: the single sources (`config/i18n.ts`, `config/site.ts` with the site URL read from the public build variable, `config/features.ts`), the platform access module, the folders, the database entry with its placeholder id.
3. Localization as [localization.md](references/localization.md) says: the locale list, the dictionaries typed for completeness, the routing, per-locale metadata, formatting, the switcher.
4. The pages of the brief on the tokens, mobile-first (stack.md "Mobile first"), with the shell (header, footer, switcher, sign-in state).
5. The data: the first migration, a module per entity under `lib/db/`, applied locally.
6. Sign-in as [auth.md](references/auth.md) says: the core action works for a guest on this device, sign-in claims it, and the provider stays off until its keys exist. Generate the local `SESSION_SECRET` into `.dev.vars` here (never shown), so that the dev server signs sessions without a warning; the deploy skill generates the live one.
7. Search and AI readiness, the share image and the favicon set, analytics with its slot for the beacon token, as [seo-geo.md](references/seo-geo.md) says.
8. Tests: the dictionary test, the boundary test where the framework has a server and client split, a test per pure module that holds a rule; `npm run check` passes.
9. Run: the dev server, every public page in every locale answers 200, the sign-in button appears only when its keys are set (placeholder values in `.dev.vars` show it; the round trip waits for real keys), the seo-geo.md check runs against the local address; a screenshot or the address for the user.

### Phase 5: Agreement

Produces the **working agreement**: `CLAUDE.md`, `AGENTS.md`, `README.md`, `docs/status.md`, `docs/decisions.md`, as [working-agreement.md](references/working-agreement.md) says, written for the people the brief names and in the team's language. Then the first commit of the skill's work on top of the scaffold's, with everything above and nothing secret. Nothing is pushed here: pushing is the deploy skill's stop.

### Phase 6: Launch

Hands over to **`cloudflare-deploy`** with: the project path, the token file the user prepared, the domain answer, the secrets by name with which are generated and which the user holds (the sign-in provider's keys, which the deploy skill asks for with the exact callback URLs once the address is known), and the repository answer when the deploy skill asks it. Its stops are the user's. When the deploy skill cannot be loaded, say so, and give the user its name and address to run it next.

### Phase 7: Delivery

One message: the address (or the local one, when the launch waits on the user), what was built in the user's words, what the check verified and what was not run (a layout verdict without a browser), what is placeholder or waiting (a key, nameservers, the owner's details, content marked in `docs/status.md`), and how the team continues: open the repository, read `CLAUDE.md`, and the loop it describes.

### Verdicts

| Result | Verdict |
|---|---|
| `npm run check` passes (types, lint, tests, build); every public page answers 200 in every locale; canonical, hreflang, the share image URL and the favicon files resolve on the local address; the sitemap lists every locale | Accepted |
| Sign-in cannot be tried because its keys are "later"; a page carries marked placeholder content; a layout verdict could not run without a browser | Accepted, with the gap named in `docs/status.md` and the delivery |
| A page in one locale shows another language or an empty string; the home page scrolls sideways at 360 px wide; a tap target is under 44 px | Redone: the dictionary, the layout |

## Hard rules

1. The questions stay in plain words. A technical choice is derived, shown with its reason, and changed on request; the user is never asked to pick between technologies by name unless they ask to.
2. The plan is approved before a file of the project is written, and the look before pages are built on it. A go-ahead skips the look, never the plan: the plan carries the data and the cost.
3. Secrets never enter the repository or the agent's own words: `.dev.vars`, `.env*` and `.cf-token` are ignored from the first commit; example files carry names and comments only; a generated value is written to `.dev.vars` and never shown; a token the user pastes is moved to its file and not repeated.
4. Every language is in from the first commit: one locale list, dictionaries complete by type, metadata per locale on every public page, no money or date formatted by hand. Adding a language touches the configuration and the dictionaries and nothing else.
5. Discover, do not remember: package versions from the registry, the adapter from the framework guide of the day, the scaffold's prompts from the tool; the files written say what was found and when.
6. Whatever the next person needs is in the repository: the brief, the look, the agreement, the status, the decisions. Chat and the agent's own memory are not where the project lives.
7. Pushing, deploying and buying are the deploy skill's stops; this skill never pushes on the way to something else.
8. Nothing invented in the pages: no testimonials, counts, logos, partner names, or an owner's details that are not true; a placeholder is marked as one and listed in `docs/status.md` for the user to replace.

## Terminology

| Term | Meaning |
|---|---|
| Brief | `docs/brief.md`: what the app is, for whom, who runs it, its pages, data, languages, sign-in, domain, look direction, and what is out of the first version. |
| Look | `docs/brand.md` and the tokens: palette, type, spacing, radius, motion, tone, the symbol. |
| Locale | One language-and-region the app speaks, as a tag (`ko`, `en`, `zh-TW`); the first named is the default. |
| Dictionary | A typed object with every string of one piece of the interface in every locale. |
| Single source | A configuration file that is the only place a fact lives (locales, site, prices, features). |
| Public page | A page anyone can open without signing in; the sitemap lists them. |
| Guest path | The core action working on one device before sign-in, claimed by the account on sign-in. |
| Check | `npm run check`: typecheck, lint, tests and build, in one command; green before every commit. |
| Agreement | `CLAUDE.md` and what it links: how the team and its agents work in the repository. |
| Status | `docs/status.md`: what is done, what is next, what is open; the handover between sessions. |
| Placeholder | Content marked for the user to replace; never passed off as real. |
| Launch | The deploy skill's run: token, resources, secrets, deploy, domain, builds. |
