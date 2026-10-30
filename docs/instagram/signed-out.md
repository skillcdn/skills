# Reading Instagram without signing in

What a visitor without an account sees on Instagram, the routes a browser takes to it, the sign-in prompt the site puts over the page, the viewport that makes a slide readable, and where the platform documents its sizes. The site has no changelog: a fact that can go stale carries the day it was checked. What any browser does on any site is in [driven-browser.md](/docs/browser/driven-browser.md) and [headless.md](/docs/browser/headless.md); this page holds what this site does.

## What is visible

A profile at `https://www.instagram.com/<handle>/` shows its name line, its bio and links, its counts, and a grid of about a dozen recent posts once the grid is scrolled to the end of what loads signed out; older posts, and in one run the weekend's posts, needed an account (checked 2026-10). The grid shows neither dates nor captions. Each tile links to a post page at `/<handle>/p/<id>/`, a video's to `/<handle>/reel/<id>/`, and a post page opens from its URL without an account, with every slide of a carousel and the whole caption ([posts.md](posts.md)). The profile also shows its highlights by name and cover: sets of stories, not posts, where an account may keep older card news the grid no longer shows (checked 2026-10). Signed out, a pinned post carries no label: posts at the head of the grid whose dates are older than the ones after them are pinned. The sample is therefore the account's last week or two with its pinned posts. A handle that does not exist, a private account, or a profile with nothing visible signed out cannot be read at all.

## Routes

| Route | Needs | Reads |
|---|---|---|
| A browser the agent drives | Navigate and report the URL, set the viewport, take a screenshot, click and hover at coordinates, zoom into a region, read the page's text, run a script in the page ([driven-browser.md](/docs/browser/driven-browser.md)) | Every page on this one and in [posts.md](posts.md) |
| A headless browser a script of the run's own drives | A shell with Node.js or Python and an installed Chrome, Edge or Chromium ([headless.md](/docs/browser/headless.md) "Driving a page from a script") | The same: a headless Chrome launched by channel, at 720 by 1050 and a scale of 2, its cookie state carried from run to run, read a profile, every post visible on it and the help page with no wall (checked 2026-10) |
| A fetch tool, a plain request | Nothing | Not the posts, whose slides carry their text in the images, nor the help site, which renders by script and returned nothing (checked 2026-10) |

The site closes its door to some networks: from the sandbox of a chat assistant, the profile and the post pages did not load at all while other sites did (2026-10), which is the host's wall and not a prompt to close ([driven-browser.md](/docs/browser/driven-browser.md) "Prompts and walls"). Recognize it by the first page of the site failing where a second site reads fine; then the routes above are gone for that host, and what reads the site is a browser of the user's own that the host drives (an extension in the user's browser, a browser pane the user opened), or an agent on a machine the site answers (a local agent with a shell). Where neither is at hand, the posts reach the agent only as images the user supplies (a screenshot or a saved image of every slide, in order, with the post's date and caption), read as a post page's slides are; a skill says which of its results that leaves out, and nothing is fetched through a proxy or a mirror.

## The sign-in prompt

A modal asking to sign up or log in covers the page a moment after a profile or a post loads, and again after some navigations. Close it by its close control at the top right of the modal, found on a screenshot, since its coordinates depend on the viewport. In a window narrower than about 768 pixels the site serves its mobile layout and the prompt is an "open in the app" sheet, closed by the X at its top right; a reel's page becomes an interstitial with a "continue on web" link, which is clicked (checked 2026-10). A headless browser at 720 by 1050 got the modal instead of the sheet, with its close control just past the viewport's right edge, where no click lands; a script that pressed that control and nothing else closed it (checked 2026-10). The prompt is closed, never answered.

## The viewport

At about 720 by 1050 the post's image box is 720 pixels wide and every line of a slide reads at zoom (checked 2026-10). Set the viewport before the first page and reset it at the end of the run; why a narrower viewport serves better than zoom at a desktop one, and what to do where the viewport cannot be set, is in driven-browser.md "The window and the viewport".

## The documented sizes

The platform's help page on post sizes, found by searching its help site for the photo or post size, gave a maximum width of 1080 pixels and supported ratios from 1.91:1 to 3:4, not a fixed portrait size (checked 2026-10-23). A slide's size is that width over the ratio measured on the posts: 1080 by 1350 for 4:5, 1080 by 1080 for 1:1. The help site renders by script: a driven or a headless browser reads it, a fetch tool does not.
