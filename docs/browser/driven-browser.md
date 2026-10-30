# A browser the agent drives

A browser the agent operates through tools: an assistant's built-in browser or browser pane, a browser extension in the user's own browser, a cloud browser, or a Playwright or Chrome DevTools server driven from a shell. It reaches what a plain request cannot: pages that answer only a real browser engine, pages that render by script, and anything behind a click, a hover or a scroll. Hosts name their tools differently and replace them within months, so a skill names the capabilities below and recognizes a browser by what its tools do; a fact about one host's behavior carries the month it was seen.

## Capabilities, and how to recognize them

| Capability | Recognize it by | Needed for |
|---|---|---|
| Navigate to a URL, and report the URL the tab is on | A tool that takes an address; a tool or a result that returns the current address | Every site. The reported address confirms a step a click made (a slide index, a query parameter) |
| Read the page's text | A tool that returns the page as text or as an accessibility tree | Captions, labels, counts: the fastest read, and the one that keeps working while the window is in the background |
| Run a script in the page | A tool that evaluates JavaScript in the page and returns its value | Data embedded in the page, image elements, pressing a prompt's own close control, drawing the frames of a video |
| Take a screenshot | A tool that returns an image of the viewport | Reading type and layout; anything a text read loses |
| Zoom into a region | A tool that returns a region of the viewport larger | Small type on a slide or a card |
| Click and hover at coordinates | Tools that take x and y | Controls that script clicks do not move: an arrow that shows on hover, a menu, a player |
| Scroll with real input | A tool that scrolls the tab | Lists that load on scroll; setting `scrollTop` from a script loads nothing on such sites |
| Set the tab's viewport | A tool or a setting that takes a width and a height | The mobile layout; a slide read at zoom |
| Save a screenshot to a file | A tool that writes the image to a path | Frames of a clip kept as files; a render looked at later |

A capability the host lacks is worked around as the sections below say, and the delivery says what could not be done. Where a skill names the route, a host with a shell and no browser tool has every capability of the table in a headless browser driven by a script of the run's own ([headless.md](headless.md) "Driving a page from a script"). A browser the agent cannot drive at all is not replaced by a fetch tool where the site answers only a browser ([reading-pages.md](reading-pages.md) "Which tool reads a page").

## The window and the viewport

- Screenshots time out while the browser window is in the background on one host; the page's text and scripts in the page keep working (checked 2026-10). Bring the window to the front before a screenshot, or read by text and script until a screenshot is needed.
- A desktop viewport serves a desktop layout. Narrower than about 768 CSS pixels, most sites serve their mobile layout, where a post or a card fills the width and reads at zoom. Set the viewport before the first page and reset it at the end of the run.
- On one host the zoom action cropped the downscaled screenshot rather than re-rendering the region, so small type at a desktop viewport could not be read; a narrower viewport, about 720 by 1050, made every line of a post readable at zoom (checked 2026-10). Where the viewport cannot be set, open the page in the narrowest window the host allows, or read the page's text and its embedded data and judge the type from one zoom.
- A zoom called inside a batch of actions returned no image on one host when a scale factor was passed with it; leaving the scale out returned the image (checked 2026-10). Zoom alone, with the region only.
- A post's or a card's region on a screenshot stays the same across the pages of one site at one viewport and one shape: find it once per shape and reuse the coordinates. A square post's box is shorter than a portrait one's, and the controls centered on it sit higher.

## Clicks that script cannot make

- A click dispatched from a script (`element.click()`) is a synthetic event: it does not open a menu or advance a control that listens for real pointer input, and it does not reveal a control that shows on hover (checked 2026-10 on two sites). Hover at the control's coordinates, take a screenshot to see it, click with a real pointer click at those coordinates, and confirm the step by the URL the browser reports or by what the page shows.
- A control that exposes no name or role to the accessibility tree cannot be addressed by a text tool. Where a site puts every filter in its URL, set the filter there and load the page anew.
- An element with the role of a dialog is not always a prompt: a site's header may be one. Read what it contains before closing it.

## Prompts and walls

- A modal that asks to sign up or sign in, a cookie or consent banner, an "open in the app" sheet, an interstitial with a "continue on web" link: close or pass it by its own control (the close mark at its top right, the link), found on a screenshot, because its coordinates depend on the viewport, with a real click or a script that presses that control and nothing else; a dialog closed that way takes about a second and a half to go (checked 2026-10). The prompt returns after some navigations: close it again.
- A wall ends the reading: a login the content needs, a paywall, a consent the page cannot be read without, a browser check or a CAPTCHA that does not pass by itself, an age gate. No sign-in, no form filled, no replay of a check, no disguised or patched browser. Say what stopped the reading and offer another source or the user's own browser.
- A page that shows nothing but a request to log in, or an error box, after pages that read fine, is the site asking for a pause: stop, say so, and do not go on without the user.
- A site whose first page already fails from the host's network (a refusal, an error page, a load that never completes) while another site loads has closed its door to that network, which some sites do to the sandboxes of chat assistants (2026-10): not a wall of the page but of the host, told apart from the pause above by the first page failing. Say so, read the site through a browser of the user's own where the host drives one, or take the alternative the skill names, and say which way was taken ([reading-pages.md](reading-pages.md) "Walls"); no proxy, no mirror, no disguised request.
- A browser the user already signed in belongs to them: read the page the skill needs and touch nothing else.

## Data embedded in a page

- Many sites embed a page's data as JSON in a `script` element of type `application/json` or `application/ld+json`: the whole of a caption the visible text cuts, timestamps, media sizes and addresses, counts. Read it with a script in the page: find the element whose text contains a key the page is known to carry, parse it, walk it to the object needed. Hold on to JSON keys and to visible labels; class names are generated and change.
- The data describes the page as first loaded. After a new URL, read it from a fresh load; what arrived by scrolling is read from the elements on the page.
- A help page, a settings page or a profile that renders by script returns nothing to a fetch tool; the driven browser reads it (checked 2026-10).

## Pace

One page at a time, a few seconds between loads, nothing in parallel. A page load is one navigation to the site, retries included; a skill that reads a site sets a budget and counts against it. These skills read a dozen or a few dozen pages for one user's own purpose; bulk or continuous collection is not what they do.
