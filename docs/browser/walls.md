# Walls: a page's, a site's and the host's

What stops a reading and what the skill does then: a page that gates its content, a site that asks for a pause, and a site that refuses the host's network from its first page. The first two are never passed; the host's wall is the one a skill works around, by the ways below in their order, each with what its result then lacks. How a prompt is closed in a driven browser is in [driven-browser.md](driven-browser.md) "Prompts and walls"; what one site does when it walls a host (where else its material is published, which way read it) stays with the family that reads that site, and each skill names its own rungs in its own words.

## A page's wall

A login the content needs, a paid subscription, a consent the page cannot be read without, a browser check or a CAPTCHA that does not pass by itself given the time to run, an age gate. The reading ends there: no sign-in, no account made, no form filled, no replay of a check, no disguised or patched browser. A prompt that only covers the page (a sign-up modal, a cookie banner, an "open in the app" sheet, an interstitial with a "continue on web" link) is closed or passed by its own control and the page read. A browser the user already signed in belongs to them: read the page the skill needs and touch nothing else. Another source is read in the page's place where the skill has one; a clip whose player never readies is listed as a source by its address ([video-frames.md](video-frames.md)).

## A site's pause

A page that shows nothing but a request to log in, or an error box, after pages of the same site read fine, is the site asking for a pause: stop, say so, and do not go on without the user. The only other move is a browser of the user's own, visible to them. A retry, a second browser or a changed address is what the pause asks the agent not to do.

## The host's wall

A site whose first page already fails from where the agent runs (a refusal, an error page, a load that never completes) while another site loads has closed its door to that network, which some sites do to the sandboxes of chat assistants (a social network's pages from one assistant's sandbox, 2026-10). It is a wall of the host and not of the page, told apart from the pause by the first page failing. Nothing of the site is read from that host: no proxy, no mirror, no cached copy, no request dressed up as a browser's; a fetch tool, a search tool's page reader or curl aimed at the site is the same request from the same network and fails, or disguises, the same way.

**The check.** A skill that reads a site known to wall some hosts opens the site's first page before its first message, once more after a few seconds when it fails, against a second site that loads, with the browser the check of [headless.md](headless.md) "The check before the first message" found, and says in its first message what it found; a skill that meets the wall on a later site of a run says so at the step where it happens. The wall is said once, at once, with the way the skill takes next, so that the user is never told after the fact that a reference was never read.

## The ways to the same material

The ways around a host's wall reach the same material by another road, and each road leaves out something the one above it carried. In this order, each offered with what it lacks:

| Way | What it takes | What its result lacks |
|---|---|---|
| 1. A browser of the user's own that the host drives | An extension in the user's browser or a browser pane the user opened: the host's tools act in a browser whose network is the user's. Recognize it by a browser tool that lists the user's own tabs or opens a pane beside the chat. The pages read as they would for any visitor | Nothing: the pages were read |
| 2. An agent on a machine the site answers | A local agent with a shell on the user's own machine, or the same skill run from a host the site does not refuse, which is usually the user's own computer; the skill says to run it there and come back with the result | Nothing: the run moves |
| 3. The same material where its owner publishes it elsewhere | An outlet's, a party's or an organization's own site, a portal's channel page of the account's own, an API the service offers for the material where the user already holds its token: found by a web search for the owner's name with the material's kind in its language, never by a guessed address, which answered with an error or nothing (2026-10). Read as the site's own pages are read, with the day of what was read, since such a page may carry only old posts or only some | What only the walled site shows: its counts, its dates where the copy has none, the posts the copy does not carry, what sits behind a click |
| 4. Material the user hand-carries | The addresses given to the user a few at a time; they open each in their own browser and paste the page's text or attach screenshots or saved images, in order, with the date and the caption or label of each, since a screenshot cuts a caption. Read as the site's pages are read, each shown at its own size | What the user did not carry: anything past what they scrolled to, exact counts, frames of a video, the page's embedded data |
| 5. A substitute | Samples of the same kind found by a web search and read from the pages they sit on; what the agent knows of the kind, marked unseen; a stand-in the skill carries for a run with nothing else | The material itself: the result is of the kind and not of the reference, said so at every checkpoint and in the delivery, and never presented as the reference's |

A way the host has not got (no browser of the user's, no machine the site answers, no page where the owner publishes, no material carried) is named as what to add and gives way to the next. The skill names its own rungs in its own words (which site, which page, what is read on it, what each leaves out of its result) and keeps them where it can run without this page.

## The go-ahead and the fall-through

Where the skill offers these ways at a stop, the message gives them in their order with what each lacks and the recommendation, and one word continues. A go-ahead ("go on", "your call", a run told to go ahead alone) takes the first way the host allows, said so, and a way that fails on the host gives way to the next in order; the run never goes straight to a substitute while a way above it is open, and never asks the user for material (way 4) without having said what ways 1 to 3 gave. A way is taken by its method, with the tools it names, or it is not taken: a fresh run told to go ahead with a text-only search tool went past the sample way to the stand-in, and another measured a search page's thumbnails for samples (2026-10).

## Saying which way was taken

The step's message and the delivery both say which way read the material, what it did not reach, and what the result lacks because of it, in the words of the skill's own result (a field left out, a count unknown, a format of the kind and not of the reference); the spec, the brief or the report records the way beside its source. A result that reached the user by a way other than the skill's main route is never presented as the main route's.

## A service with no other way

A service a step writes through or calls (a payments API, a platform's API, a model's server) that the host cannot reach has no other road to the same result: the skill stops and says what to add or where to run, as the repository's rule on missing tools says, and never substitutes a service that changes the result or the cost.
