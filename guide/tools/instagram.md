# Instagram skills

How the skills that work on Instagram are written and kept in step, for authors. What they share at run time is the document set [`docs/instagram/`](../../docs/instagram/README.md), which agents read; this page says what goes there, what stays in a skill, and how the site's facts are kept true. Two skills use the set: the card-news format study, which reads the site signed out, and the post scheduling, which books and confirms posts in a session signed in to the account ([roadmap.md](../roadmap.md)).

## The tool is a website

There is no MCP server and no account to connect: a skill's Requirements name capabilities, never a product's tool names.

**Reading** is done signed out: the pages a visitor without an account sees, with a browser the agent drives or a headless browser a script of the run's own drives. The site is not reachable from every host (a chat assistant's sandbox was refused, 2026-10): the browser set's `walls.md` says how that is recognized, the order of the ways around it and the go-ahead, this set says what still reads the site and where else an account publishes the same posts (its own site, a portal's channel page), and each skill names its own alternatives in that order (the account's own site, supplied slides, search samples for a genre, the looks from the genre as the agent knows it), each with its method and what the result then lacks, since the root rule says a missing route is reported and the way taken is said. The browser itself has its own set and page, `docs/browser/` and [`browser.md`](browser.md); this family's set keeps what Instagram does.

**Posting** is done in the site's own web interface, in a browser the agent drives that is signed in to the account, with a tool that hands files to a page's input and a clipboard to paste from: an extension in the person's browser or a pane they opened, signed in by them, or an agent account's own browser, which the account signs in itself where it holds the account's password and second step, the secrets kept out of the conversation as the browser set's `signing-in.md` says for any service. It is the one route the posting skill writes. A headless browser a script of the run launches keeps no session and is not the route, so without a browser that is or can be signed in the skill stops and asks a person. The signed-in pages keep the reading pages' rule of naming no account, and add one of their own: a control is named by what it does and where it sits, because its label follows the account's language.

## What is shared and what stays in the skill

| In `docs/instagram/` | In the skill |
|---|---|
| `signed-out.md`: what a signed-out visitor sees, the routes, the sign-in prompt in each layout, the viewport, the documented sizes | Which accounts and posts are read, the page budget, the checkpoint |
| `posts.md`: the post object and its keys, the date and the slide count, stepping a carousel at each ratio, reading a slide, a video post, the caption | What is measured on a slide and how, what a row of the log records, what the delivery holds (the format study's `reading-posts.md`) |
| `signed-in.md`: whose session it is, who signs in and how a secret stays out, what the browser must do, the screens that stop the work, the pace and what read as automation | Which posts are booked and on whose word, the schedule's checkpoint, what "go ahead" skips |
| `creating-posts.md`: the create dialog's steps, the crop's preset ratio, a video's cover, pasting the caption, the schedule switch and its time fields | How slots are given out, the order of the posts, the gate a post passes before it is booked |
| `scheduled-posts.md`: the scheduled list, reading a booking back, changing and deleting a booking, a post that went live | What is written to the post's record and the ledger, the filing of a live post, the verdicts |

The test for a sentence: would the next skill that works on Instagram meet it too? Then it belongs in the set. The set sits at the root because its skills are of two areas: the format study in `design/` and the post scheduling in `marketing/`; its included pages travel with every mount, and a plugin lacks the set. A skill includes the pages every run of it reads by their root-relative paths and links the ones only a phase reads; a change to an included page changes the served digest of every skill that includes it, as a manifest change does. The records the posting skill writes (a post's `post.json`, the ledger) are the card-news set's, `docs/card-news/account.md`, not this one's.

## Facts are dated

What a visitor sees, where a control sits, what a dialog presets and which key the post object carries change without notice. A statement carries the day it was checked and the way to find the value again; a run that finds one wrong fixes the sentence it bears on ([skill-authoring.md](../skill-authoring.md) "Knowledge pages"). No account, handle or post from a run is named.

## Testing

A reading skill is run from a fresh session with the browser the host has: a driven browser from an assistant that offers one, the headless route from an agent with a shell. The posting skill needs an account whose owner is at the browser and lets a test post be booked: a fresh session books one post for a time far enough ahead to be deleted before it goes out, reads it back, changes its time and deletes it, on the owner's word at each step; a run to a live post is made only with a post the owner wants published. A change to a page of the set is read against every skill that includes or links it before it is pushed.
