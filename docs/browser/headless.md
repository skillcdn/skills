# A headless Chromium-family browser from a shell

A shell with Node.js or Python and an installed Chrome, Edge or Chromium renders pages, prints PDFs, takes screenshots and dumps a page's DOM with no window opening. Skills that render their own HTML and skills that read a site that answers only a browser engine both launch it this way. Nothing here costs money; a browser download is the one step that is asked first.

## playwright-core from Node.js

- `playwright-core` is the driver without the browsers. Require it from where it is installed, in this order: a neighbouring project's `node_modules`, through `createRequire` of that project's `package.json`, named in the environment variable `PLAYWRIGHT_FROM` (no install); else `npm install playwright-core` once into a tools folder outside what is handed over, so that no `node_modules` lands in a deliverable, with `PLAYWRIGHT_FROM` pointing at its `package.json` (no browser download, a few seconds).
- Launch an installed browser by channel, `chrome` then `msedge`, and fall back to Playwright's own `chromium` where one is installed. A channel launch needs a `playwright-core` from the last year or so (checked 2026-10), and the launch is the test: when a borrowed copy fails to launch an installed browser by channel, leave it where it is and install the current `playwright-core` into the tools folder instead.
- Where no browser is installed at all, `npx playwright install chromium` downloads one, a few hundred megabytes: say so and run it only on the user's word.
- Check with one `require` from the shell before a skill's first message: `node -e "require('playwright-core')"` in the folder it is installed in, or with `PLAYWRIGHT_FROM` set.
- Write the scripts as ES modules (`.mjs`), so that they run whatever a neighbouring `package.json` sets as `"type"`; a CommonJS `.js` file fails with a reference error under `"type": "module"` (checked 2026-10).

```js
import { createRequire } from "node:module";
const require = createRequire(process.env.PLAYWRIGHT_FROM || new URL("./package.json", import.meta.url));
const { chromium } = require("playwright-core");

async function launch(args = []) {
  for (const channel of ["chrome", "msedge", "chromium"]) {
    try {
      return await chromium.launch(channel === "chromium" ? { args } : { channel, args });
    } catch {
      // try the next one
    }
  }
  throw new Error("no Chromium-family browser found: install Chrome or Edge, or run npx playwright install chromium");
}
```

## Playwright from Python

`from playwright.sync_api import sync_playwright`, then `p.chromium.launch()` inside `with sync_playwright() as p`; `launch(channel="chrome")` uses the installed Chrome. `pip install playwright` installs the driver, and `playwright install chromium` downloads a browser: ask first. Without Playwright, a skill that prints a PDF writes the HTML and says the PDF is printed from a browser's print dialog at the page size with background graphics on.

## Driving a page from a script

Where a skill names this route for a host that offers a shell and no browser tool, a headless browser driven by a script of the run's own stands in for the browser the agent drives. Every capability in [driven-browser.md](driven-browser.md) "Capabilities, and how to recognize them" is a Playwright call, and what that page says about the viewport, real clicks, prompts and walls, and pace holds unchanged.

| Capability | In Playwright from Node.js (Python: the same calls in snake case, options as keyword arguments, `page.url` a property) |
|---|---|
| Navigate, and report the URL | `page.goto(url, { waitUntil: "domcontentloaded" })`; `page.url()` after a click, which is how a step is confirmed |
| Read the page's text | `page.innerText("body")` |
| Run a script in the page | `page.evaluate(() => ...)`, which returns the value |
| Take a screenshot | `page.screenshot({ path })`: the viewport, to a file the agent reads |
| Zoom into a region | `page.screenshot({ path, clip: { x, y, width, height } })` in a context made with `deviceScaleFactor: 2` or `3`: the region is rendered at that scale (twice the width and the height for a clip at 2), not cut from a smaller image |
| Click and hover at coordinates | `page.mouse.move(x, y)`, then `page.mouse.click(x, y)`: input to the browser itself, so that a control that shows on hover appears and a carousel's arrow advances, which a `click()` run from `page.evaluate` does not do (driven-browser.md "Clicks that script cannot make") |
| Scroll with real input | `page.mouse.wheel(0, dy)` |
| Set the tab's viewport | `browser.newContext({ viewport: { width, height }, deviceScaleFactor })`, before the first page |
| Save a screenshot to a file | Every screenshot above is a file |

- One run of the script is one page, or one post with its slides: it opens the page, acts, writes its screenshots and what it read into a folder of the run's own under the host's scratch folder, never the folder of what is delivered, closes the browser and ends; the agent reads the files and gives the next run what it found on them (where a prompt's close control sits, where a carousel's next control sits). A control is addressed by its role and name where it exposes one (`page.getByRole("button", { name })`), else at coordinates read from a screenshot. A `chromium.connect` to a `launchServer()` endpoint does not keep a page across shell calls: a client's contexts close when it disconnects.
- The browser's cookies go from run to run in a state file of the run's own (`context.storageState({ path })` before the browser closes, `storageState: path` in the next `newContext`), so that the site sees one visitor through the skill's run, as it sees a person's browser, and what it counts per visitor applies to the run and not to a new visitor on every page; the file lives beside the screenshots and goes with them. A prompt that returns after some navigations in a window returns here too and is closed the same way. A later run does not undo what the site said on an earlier one: a request to log in or an error box after pages that read fine ends the skill's run, not only that script run (driven-browser.md "Prompts and walls"). Playwright's own temporary profile folder goes when the browser closes; a run cut by a timeout can leave one (`playwright_chromiumdev_profile-*`) in the system's temporary folder: remove the one this run made.
- The browser goes to the site as Playwright launches it and is never made to pass for another browser or device. A wall the site shows it ends the reading, as any wall does (driven-browser.md "Prompts and walls"): say what stopped it; the reading is not moved to another browser to get past it.
- A page at a time, a few seconds between loads within a run and between runs, nothing in parallel, and no more pages than the skill's budget, a dozen or a few dozen for one user's own purpose: never a list of pages handed to one run, a loop left running or a run on a schedule (driven-browser.md "Pace").
- The screenshots are the agent's reading material: kept out of what is delivered and removed when the skill's run ends, as the skill's rules on images say.

## The bare browser with --dump-dom

One run per URL prints the page as the browser built it, with the page's embedded JSON inside; two to nine seconds a page, and a site that answers only a browser engine answers this.

```sh
"<browser>" --headless=new --disable-gpu --no-first-run --user-data-dir="<a folder kept for the run>" --dump-dom "<url>"
```

- Never start the browser without `--headless=new` and that folder, not even to ask its version: on Windows the bare command, `--version` included, opens a window in the user's own browser session (checked 2026-10).
- One profile folder per run: the site's cookies live there. Remove it when the run ends; the browser leaves read-only files that Windows will not delete as they are, so clear the attribute first. A profile path near 260 characters makes no profile on Windows and every load runs to the timeout: keep the path short, or put the profile in the system's temporary folder.
- A timeout of about a minute per run. Quote the URL: it carries `&` and brackets.
- `--virtual-time-budget=<milliseconds>` lets the page's own scripts finish before the dump, as they would in a window, for a page that is still running when a plain dump returns; on ordinary pages the flag made some runs hang until killed, so it is added to such a load only. It gives a page time and nothing else: a check that does not pass on its own in that time ends the reading (reading-pages.md "Walls").
- Chrome and Chromium print the page; on Windows, Edge printed nothing in the same test (checked 2026-10). When the output is empty for every URL, try another browser or a driven browser.
- Find the binary by the `CHROME` environment variable, then the names on the path (`google-chrome`, `chromium`, `chromium-browser`), then the usual install paths of each system. A restricted shell may refuse a look at the disk while it allows the run: the run is the test.

## Waiting for a page

- Before a screenshot or a PDF: wait for the network to go idle (`waitUntil: "networkidle"`, Python `wait_for_load_state("networkidle")`), then for `document.fonts.ready`, then about 300 milliseconds for images to finish decoding. Without the fonts wait a web font falls back and the render is wrong.
- A page that loads its content by script: wait for an element the content has (`waitForSelector`), never for a fixed time alone.

## Screenshots

- A screenshot clipped to a rectangle at `deviceScaleFactor: 1` is exactly that many pixels: set the viewport to the canvas and clip to it for a render. At 1.5, a 1280 by 720 clip gives a 1920 by 1080 file: set the scale for a frame.
- PNG for a render whose pixels are measured; JPEG at a quality around 90 for frames of a clip.

## PDF

`page.pdf({ path, width: "13.333in", height: "7.5in", printBackground: true, preferCSSPageSize: true })` in Node.js, `page.pdf(path=..., width=..., height=..., print_background=True, prefer_css_page_size=True)` in Python, after the waits above. The CSS declares `@page { size: <w> <h>; margin: 0 }` and gives every page element that size with `break-after: page`. Background graphics are off by default: set them on, or every tint disappears.

## Long runs

A capture of a clip of several minutes runs for minutes: run it in the background and read its output when it ends. A shell tool's timeout cuts a foreground run; pass a few URLs per call to a script that dumps pages (about eight; sixteen took one to three minutes).

## The check before the first message

A skill that needs this names it in its Requirements and checks before its first message: Node.js or Python; a Chromium-family browser, which is an installed Chrome or Edge or Playwright's own; `playwright-core` or Playwright resolvable where the skill launches it. Without a browser, stop and say what to install (Chrome or Edge, or the download above with consent); without `playwright-core`, borrow or install it as above. A browser looked for on the disk and not found proves nothing: the launch is the test.
