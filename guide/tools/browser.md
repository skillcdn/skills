# Browser skills

How the skills that read a website or render a page with a browser are written and kept in step, for authors. What the skills share at run time is the document set [`docs/browser/`](../../docs/browser/README.md), which agents read; this page says what goes there, what stays in a skill or in a site's own family set, how the facts are dated, and how the family is tested. The family spans areas (marketing's card-news skills and Meta Ad Library skills, design's deck draft, engineering skills that look at a page they built), which is why the set sits at the root.

## The tool is a capability

A browser is not one product. A skill's Requirements name what it needs (a browser the agent drives that can navigate, click at coordinates, zoom and run a script in the page; a shell with a Chromium-family browser `playwright-core` can launch; a fetch tool) and how to recognize each by what a tool does. The browsing tools of every host are renamed and replaced within months: a product's tool name appears only as a dated example, and the set names a host only as "one host". The `metadata.tools` value is `browser` for a skill whose tool is the browser itself (a page the agent wrote, rendered to PNG or PDF); a skill whose tool is a site it reads with a browser keeps the site as its family (`instagram`, `meta-ad-library`, `web`).

## What is shared and what stays where

| In `docs/browser/` | In a site's family set or a skill's `tool-notes.md` | In the skill |
|---|---|---|
| `driven-browser.md`: the capabilities and how to recognize them, the window and the viewport, screenshots and zoom, script clicks against real clicks, prompts and walls, embedded data, pace | What one site shows without signing in, where its controls sit, what its prompts look like, which keys its JSON carries, with the day (the Meta Ad Library set; the card-news study's `tool-notes.md`) | Which pages the skill opens, in what order, and what it records |
| `headless.md`: `playwright-core` borrowed or installed, the channel launch, the download asked first, Python Playwright, a page driven from a script with a driven browser's capabilities, `--dump-dom`, waits, screenshots, PDF, long runs, the check | A site's own first-load check, which a browser passes by itself given time, and the flags that give it that time (the Meta set's `page-dump.md`) | The skill's scripts (`scripts/*.example.mjs`, `render.py`) and the environment they take |
| `reading-pages.md`: which tool reads what, read to the end, walls, pages that render by script, the images on a page, downloading, pixel sizes | | What counts as a source, where images are looked for and in what order, what an entry records |
| `rendering-html.md`: boxes at native size and the export mode, serving and the host's preview, PNG, PDF, fonts, the line check, looking at a render, a contact sheet | | The page's design: slide types, blocks, tokens, what the review looks for and the verdicts |
| `video-frames.md`: the routes, the watch page in a headless browser, ffmpeg from a media address, the driven browser, what a frame records | A platform's player facts that one script depends on, in that script's comments | The capture folder, which frames are kept and why, the entry's fields |

The test for a sentence: would it hold for the next skill that opens a browser on another site or renders another page? Then it belongs in the set. A sentence about one site belongs with that site's readers; a sentence about one skill's artifact belongs in the skill. A skill includes the page every run of it reads (`skillcdn.include`, root-relative) and links the rest from the phase that reads them; the included page is digested with the skill, so a change to it re-asks every host that verified those skills, as a manifest change does. The scripts stay in the skills that use them, and the set links them by root-relative path; a skill mounted alone or copied has no page of the set, which its Requirements say.

## Facts are dated

A host's browser behaves differently from one month to the next and a site changes without notice. A fact about a host (a screenshot that timed out in a background window, a zoom that cropped instead of re-rendering, a port that did or did not arrive in the environment) carries the month it was seen and says "one host"; a fact about a site carries the day and the way to find the value again, and lives with the site's readers; a fact about how a browser works (a synthetic click, `document.fonts.ready`, a clip at scale 1) carries no date and changes when a run finds it wrong ([skill-authoring.md](../skill-authoring.md) "Knowledge pages"). No run narrative, no product, account, outlet or client from a run.

## Manners are part of the skill

No sign-in, nothing past a wall, no disguised browser, one page at a time, a download only with consent, no window on the user's screen. The set states them once for agents; each skill states what applies to it in its hard rules, because a copied or installed skill has only those.

## Testing

Each skill is exercised from a fresh session with the browser the host has: a driven browser from an assistant that offers one, the headless route from an agent with a shell. A change to a page of the set is read against every skill that includes or links it before it is pushed, and the included pages are checked with `npx @skillcdn/cli check`, which prints them under each skill as "shared pages returned with the skill". What a fresh agent had to guess goes back into the files; what a host did differently changes the sentence of the set that it bears on, with the month.
