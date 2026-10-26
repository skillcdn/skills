# Instagram skills

How the skills that read Instagram are written and kept in step, for authors. What they share at run time is the document set [`marketing/docs/instagram/`](../../marketing/docs/instagram/README.md), which agents read; this page says what goes there, what stays in a skill, and how the site's facts are kept true. Today one skill reads the site, the card-news format study; the set was made before the second, because more Instagram skills are planned ([roadmap.md](../roadmap.md)).

## The tool is a website

There is no MCP server and no account to connect for reading: the skills read the pages a visitor without an account sees, with a browser the agent drives or a headless browser a script of the run's own drives. A skill's Requirements name those capabilities, never a product's tool names. The browser itself has its own set and page, `docs/browser/` and [`browser.md`](browser.md); this family's set keeps what Instagram does. A skill that posts to an account works signed in, with the account the user provides, and brings its own rules and pages for that; the reading pages stay signed out.

## What is shared and what stays in the skill

| In `marketing/docs/instagram/` | In the skill |
|---|---|
| `signed-out.md`: what a signed-out visitor sees, the routes, the sign-in prompt in each layout, the viewport, the documented sizes | Which accounts and posts are read, the page budget, the checkpoint |
| `posts.md`: the post object and its keys, the date and the slide count, stepping a carousel at each ratio, reading a slide, a video post, the caption | What is measured on a slide and how, what a row of the log records, what the delivery holds (the format study's `reading-posts.md`) |

The test for a sentence: would the next skill that reads Instagram meet it too? Then it belongs in the set. The set sits in the area's `docs/` because the skills that read Instagram are marketing skills; it travels with the marketing mount and plugin. A skill includes the pages every run of it reads by their root-relative paths; a change to an included page changes the served digest of every skill that includes it, as a manifest change does.

## Facts are dated

What a signed-out visitor sees, where a control sits and which key the post object carries change without notice. A statement carries the day it was checked and the way to find the value again; a run that finds one wrong fixes the sentence it bears on ([skill-authoring.md](../skill-authoring.md) "Knowledge pages"). No account, handle or post from a run is named.

## Testing

A skill of the family is run from a fresh session with the browser the host has: a driven browser from an assistant that offers one, the headless route from an agent with a shell. A change to a page of the set is read against every skill that includes it before it is pushed.
