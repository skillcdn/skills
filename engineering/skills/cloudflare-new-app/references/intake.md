# Intake: the questions and what they derive

The questions are asked in one message, in plain words, only where the request leaves them open; a question half answered by the request is asked for its missing half only. An answer stands for the run. What is not asked is derived and shown in the plan with its reason. A request that is a link to a mockup or a reference site is read first: it answers what it shows (the idea, the audience, the name, the look, a sign-in its text names), the message says what was taken from it, and the questions it leaves are asked, plus one it raises: whether the sample content it shows goes in as marked sample data (stack.md's `db/seed.sql`) or the site opens empty. When the user said to go ahead alone, questions 3 to 6 are not asked: their defaults go into the plan.

## The questions

1. **The idea.** "What should the app do, in a few sentences, and who is it for? Who runs it: you, or a company, where you are based, and a contact email for the site? If you have a name in mind, or an example site or a sketch, send it." Skipped where the request already says; the owner and contact may be "later", and the legal pages then carry a marked placeholder.
2. **Languages.** "Which languages should it speak? Name the main one first." Default when unanswered: the language the user wrote in, alone.
3. **Sign-in.** "Do people need an account? If yes, how should they sign in: with Google, with the sign-in most people in <the main market> use (<the provider auth.md's market table names for it>), with an email link (that one needs a sending service, set up at the launch), or a mix?" Default: Google when anything is kept per person, with the market's provider offered when the table names one; none when nothing is. In both cases the core action works for a guest first (auth.md "The guest path").
4. **Domain.** "Do you already have a web address (domain) for it, should I look for one to buy (I show the price first), or do we start on a free address and decide later?" Default: later.
5. **The look.** "How should it feel? A site you like, a few colors, a mood in two or three words, or I propose a look." Default: a proposal from the idea and the audience.
6. **Must-haves.** "Is there anything it must do from day one that I have not mentioned, such as taking payments, sending emails, or a page people already expect?" Default: none.

Then, in a second message, so that the questions stay short: "While I plan, you can create the Cloudflare key I will need to put it online: [the steps of tokens.md with its always rows; add the Registrar row if you want me to buy a domain]. Save it in a file named `.cf-token` in this folder (I move it into the project when the project exists) and tell me; that keeps it out of this chat."

## What the answers derive

| From | Derived | Shown as |
|---|---|---|
| The idea | The app's name (the one the user gave, else a short memorable word or two from the idea, offered as a proposal) and its slug (lowercase, hyphens: the folder, the Worker's name, the package name); the folder, `<current folder>/<slug>` unless the user names one; the pages and their routes; the entities kept and their fields; what is out of the first version | "Called <name>, in the folder <slug>; pages: ..., keeping: ..." |
| The audience and devices | Mobile first always; a desktop layout when the audience works at a desk; touch targets, bottom navigation when there are more than three sections | "Built for phones first" |
| The owner and contact | The organization data, the about sentence, the legal pages' operator, `llms.txt`'s contact; a placeholder marked `[owner]` in each when "later" | "Run by <owner>" |
| Languages | The locale list with the default first; the script each uses, hence the fonts; the regions, hence currencies, time zones and date formats; the routing scheme (localization.md) | "Speaks <list>; <main> is the main one" |
| Sign-in | The provider(s), the session cookie, the members table, the guest path; the keys the user will need to create and where | "Google sign-in; the deploy skill asks for its two keys with the exact addresses" |
| Domain | The launch path of the deploy skill; the site URL read from a public build variable, localhost until the launch sets it | "Starts on a free workers.dev address" |
| The look | Palette, type per script, radius, motion, tone; the symbol for the favicon and share image | "Calm, warm, serif headings" |
| Must-haves | Payments: a checkout provider as a later phase, never in the first commit; email: the sender and the plan it needs (platform.md); a page: added to the pages | Named in the plan |
| The user's language | The language of the project's documents (brief, brand, agreement, status); code, identifiers and commit messages stay in English | "Documents in <language>, code in English" |
| The team | Who will work in the repository (the user, developers, a planner, a designer), from the request; the user alone when nobody is named; it shapes the agreement's roles section | "You, for now" |
| An action only the operator does (posting, approving, removing) | An operator screen (`/admin`) behind `ADMIN_PASSWORD`, generated locally and handed over as a file (SKILL.md phase 4, step 6); who the operator is comes from question 1 | "You manage the schedule at /admin" |

## Pages every app gets

Besides the pages of the idea: the home page with the one-sentence entity statement and a short FAQ; an about page (a section of the home page for a small app); terms and privacy pages per locale (a refund page only when money is taken); a not-found page; the sign-in and account pages when sign-in exists; `sitemap.xml`, `robots.txt`, `llms.txt`; the share image per locale and the favicon set. "Small" is not a reason to drop any of these: they cost minutes and the delivery is judged on them. The app's own screen, when it shows only the visitor's data, is a private page: it exists, but it is kept out of the sitemap and marked `noindex` (seo-geo.md). The home page's entity sentence and the FAQ use only facts from the answers; a fact they need that the answers lack (where, since when, what it costs, how to join) is asked once in the plan message or left as a marked placeholder listed in `docs/status.md`.

## The plan message

Ten lines at most, one per label, no jargon beyond a name in parentheses:

> Here is the plan. **Name:** <name> (folder `<slug>`). **Pages:** home, <...>. **Keeps:** <entities in plain words>. **Languages:** <list>, <main> first. **Sign-in:** <provider or none>; saving works before signing in, on this device. **Look:** <direction>, I will show it before building the rest. **Runs on:** Cloudflare's <free plan, or the paid plan because ...>; a web address <is yours already / comes later / I look one up and show its price before buying>. **Also:** icons and share image, analytics, tests, the team's working agreement; documents in <language>. **Made with:** <framework> on the path Cloudflare recommends today, because <one reason>. **You will do:** create the Cloudflare key (now), the Google sign-in keys (at launch, I give the exact steps), <nameservers>. OK?
