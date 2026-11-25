# A browser the agent drives

A browser the agent operates through tools: an assistant's built-in browser or browser pane, a browser extension in the user's own browser, a cloud browser, or a Playwright or Chrome DevTools server driven from a shell. It reaches what a plain request cannot: pages that answer only a real browser engine, pages that render by script, and anything behind a click, a hover or a scroll. Hosts name their tools differently and replace them within months, so a skill names the capabilities below and recognizes a browser by what its tools do; a fact about one host's behavior carries the month it was seen.

## Capabilities, and how to recognize them

| Capability | Recognize it by | Needed for |
|---|---|---|
| Navigate to a URL, and report the URL the tab is on | A tool that takes an address; a tool or a result that returns the current address | Every site. The reported address confirms a step a click made (a slide index, a query parameter) |
| Read the page's text | A tool that returns the page as text or as an accessibility tree | Captions, labels, counts: the fastest read, and the one that keeps working while the window is in the background |
| Run a script in the page | A tool that evaluates JavaScript in the page and returns its value | Data embedded in the page, image elements, pressing a prompt's own close control, drawing the frames of a video |
| Take a screenshot | A tool that returns an image of the viewport | Reading type and layout; anything a text read loses |
| Zoom into a region | A tool that returns a region of the viewport larger, or a screenshot of one element at a higher pixel ratio | Small type on a slide or a card |
| Click and hover with real input | Tools that take x and y, or an element of the page's snapshot, and move a real pointer to it | Controls that script clicks do not move: an arrow that shows on hover, a menu, a player |
| Scroll with real input | A tool that scrolls the tab, or presses `End` and `Page Down` | Lists that load on scroll, where setting `scrollTop` from a script may load nothing: count the items before and after |
| Set the tab's viewport | A tool or a setting that takes a width and a height | The mobile layout; a slide read at zoom |
| Save a screenshot to a file | A tool that writes the image to a path | Frames of a clip kept as files; a render looked at later |

A capability the host lacks is worked around as the sections below say, and the delivery says what could not be done. Where a skill names the route, a host with a shell and no browser tool has every capability of the table in a headless browser driven by a script of the run's own ([headless.md](headless.md) "Driving a page from a script"). A browser the agent cannot drive at all is not replaced by a fetch tool where the site answers only a browser ([reading-pages.md](reading-pages.md) "Which tool reads a page").

## An agent account's browser

An agent account of a SkillCDN Console that runs on Claude Code is started with the browser its desk's `runner.json` names as `browser`, a headless one where it names none; under another product it is started with none (console 0.6.2, its specification, read 2026-11). Which name it uses is the account's own to choose, as the job needs it, and the runner takes the change between two turns; nobody but a supervisor may tell it to.

| `browser` | What the account drives |
|---|---|
| `headless` | A Chrome with no window and a profile of its own, through the tools of a server called `chrome-devtools` |
| `window` | The same browser and profile with its window, on a machine with a desktop logged in |
| `chrome` | The product's own browser tool in the Chrome of the account's machine, another profile |
| `none`, or another product | No browser tool: a skill that names the scripted route takes it ([headless.md](headless.md) "Driving a page from a script"), and any other stops as it does where a browser is missing |

- **No `chrome-devtools` tools in a session that should have them:** Google Chrome or the program is missing on the machine (`npm install -g chrome-devtools-mcp@latest`, on a Node.js it runs on). The account keeps its own machine's programs, as the console has it: it installs what is missing, says so in its next report and has the tools from the next session on; what its OS account may not install it asks of whoever keeps the machine.
- **How those tools do what "Capabilities" above asks** (run 2026-11 on Windows, as the runner starts the program; the session's list is what counts). They take an element by its id in the latest snapshot, and the pointer and the keys are real: a click stepped a carousel that a script's click does not, and an arrow that shows on hover is in the snapshot taken after the hover. No tool takes a point, turns the wheel or zooms:
  - What has no name or role (a plain box, a canvas, a video) is in the verbose snapshot alone, and its id is clicked at its middle. Another point of it, on a page nobody is signed in to: a script lays a box of two pixels there with `pointer-events: none`, a role and a label, and a click on that box's id lands on what is under it.
  - `End` and `Page Down` load what scrolling loads.
  - Small type is read from a screenshot of its element at a pixel ratio of 2 or 3. The emulation tool sets the viewport with the ratio, to any width, each call replacing the last; the resize tool stops at 500 pixels wide. The viewport a session begins with is the machine's own (1889 by 2045 on one): set it before the first page.
  - The script tool takes a function: a block of these pages that calls itself runs with its script format, and fails as "not a function" without it. A long answer goes to a file.
  - A file it writes, or hands to a file input, lies in the session's folder, in one added to it, or in the system's temporary folder; any other path is refused ("Access denied"): copy with the shell. A download the page starts lands in the OS account's downloads folder, and no tool says so.
- **The clipboard.** In `headless` it is the browser's own: what was copied there was not in the system's, and what a shell puts in the system's is not to be counted on there. A text to paste is written into a text field of a page of the run's own (an HTML file in the system's temporary folder, opened in a tab), selected and copied with the keys, and pasted with the keys in the tab it is for: a composed script, an emoji and blank lines came over exactly, into a text area and into an editable element (run 2026-11 on Windows, on pages made for it).
- **What a site sees.** The `headless` browser calls itself a headless one, and both it and `window` say they are driven. A site that refuses it has walled that browser ([walls.md](walls.md)); the emulation tool's user agent is never set to pass for another.
- **A person's sign-in** stays in the profile it was made in from one session to the next, `headless` and `window` sharing theirs; one that the site keeps only until the browser closes is gone with the session. The scripted route has none. Where a skill needs an account the agent account holds no sign-in of, or a step only a person can take (an approval on another device), it asks as a decision of whoever can sign in there, its manager where it knows of nobody else: the service, the account there, the machine, and which name the browser takes meanwhile, `chrome` or `window`. On their word it changes the name and ends its turn, the person signs in there themselves, and when the job that needed the sign-in is done they sign out where it was for that job alone, and the name goes back. A session a person signed in for one job is used for that job alone. Which of the two a site's skills may use, the pack's pages on that site say.
- **Its own sign-in.** Where a task needs a sign-in at a service and the account holds it, the account signs in itself in `headless` or `window`, as [signing-in.md](signing-in.md) says, read before a secret is taken from where it is kept. A login met by a skill that reads a site signed out stays a wall ("Prompts and walls" below), and a sign-in kept in the profile is for the work it was made for: such a skill opens that site in an isolated context of the same tools (the tool that opens a page takes a name for one, and a page in it was signed out while the profile was signed in, run 2026-11) or by the scripted route, and where it has neither it says so instead of reading signed in.
- **One at a time.** One browser opens the profile at once, so one agent of a session drives it: a second is told that the browser is already running, and the first goes on.

## The window and the viewport

- Screenshots time out while the browser window is in the background on one host; the page's text and scripts in the page keep working (checked 2026-10). Bring the window to the front before a screenshot, or read by text and script until a screenshot is needed.
- A desktop viewport serves a desktop layout. Narrower than about 768 CSS pixels, most sites serve their mobile layout, where a post or a card fills the width and reads at zoom. Set the viewport before the first page and reset it at the end of the run.
- On one host the zoom action cropped the downscaled screenshot rather than re-rendering the region, so small type at a desktop viewport could not be read; a narrower viewport, about 720 by 1050, made every line of a post readable at zoom (checked 2026-10). Where the viewport cannot be set, open the page in the narrowest window the host allows, or read the page's text and its embedded data and judge the type from one zoom.
- A zoom called inside a batch of actions returned no image on one host when a scale factor was passed with it; leaving the scale out returned the image (checked 2026-10). Zoom alone, with the region only.
- A post's or a card's region on a screenshot stays the same across the pages of one site at one viewport and one shape: find it once per shape and reuse the coordinates. A square post's box is shorter than a portrait one's, and the controls centered on it sit higher.

## Clicks that script cannot make

- A click dispatched from a script (`element.click()`) is a synthetic event: it does not open a menu or advance a control that listens for real pointer input, and it does not reveal a control that shows on hover (checked 2026-10 on two sites). Hover at the control's coordinates, take a screenshot to see it, click with a real pointer click at those coordinates, and confirm the step by the URL the browser reports or by what the page shows.
- A control that exposes no name or role to the accessibility tree cannot be addressed by a text tool, unless the host has a fuller snapshot that lists it. Where a site puts every filter in its URL, set the filter there and load the page anew.
- An element with the role of a dialog is not always a prompt: a site's header may be one. Read what it contains before closing it.

## Prompts and walls

- A modal that asks to sign up or sign in, a cookie or consent banner, an "open in the app" sheet, an interstitial with a "continue on web" link: close or pass it by its own control (the close mark at its top right, the link), found on a screenshot, because its coordinates depend on the viewport, with a real click or a script that presses that control and nothing else; a dialog closed that way takes about a second and a half to go (checked 2026-10). The prompt returns after some navigations: close it again.
- A wall ends the reading: a login the content needs, a paywall, a consent the page cannot be read without, a browser check or a CAPTCHA that does not pass by itself, an age gate. No sign-in, no form filled, no replay of a check, no disguised or patched browser. Say what stopped the reading and offer another source or the user's own browser.
- A page that shows nothing but a request to log in, or an error box, after pages that read fine is the site asking for a pause; a site whose first page already fails from the host's network while another site loads has walled the host. Both are in [walls.md](walls.md), with the ways to the same material in their order: for the pause, stop, say so and do not go on without the user; for the wall, say so and take the first way the host allows, with no proxy, no mirror and no disguised request, and say which way was taken.
- A browser the user already signed in belongs to them: read the page the skill needs and touch nothing else.

## Data embedded in a page

- Many sites embed a page's data as JSON in a `script` element of type `application/json` or `application/ld+json`: the whole of a caption the visible text cuts, timestamps, media sizes and addresses, counts. Read it with a script in the page: find the element whose text contains a key the page is known to carry, parse it, walk it to the object needed. Hold on to JSON keys and to visible labels; class names are generated and change.
- The data describes the page as first loaded. After a new URL, read it from a fresh load; what arrived by scrolling is read from the elements on the page.
- A help page, a settings page or a profile that renders by script returns nothing to a fetch tool; the driven browser reads it (checked 2026-10).

## Pace

One page at a time, a few seconds between loads, nothing in parallel. A page load is one navigation to the site, retries included; a skill that reads a site sets a budget and counts against it. These skills read a dozen or a few dozen pages for one user's own purpose; bulk or continuous collection is not what they do.
