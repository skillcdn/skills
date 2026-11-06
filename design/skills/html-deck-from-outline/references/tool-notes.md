# Tool notes

How the helper and the browsers behaved in runs of this skill, by topic. A fact that can go stale names where it was seen and the month.

## Printing the PDF

- Playwright from Python is often absent where the helper runs: a sandbox whose `pip` is refused (no root), a Windows PC with Python but neither Playwright nor PyMuPDF installed (seen 2026-10 and 2026-11). The helper's second route, Node.js with `playwright-core`, printed where a neighbouring project or a `tools/` folder had it; its third, the installed browser's own `--headless=new --print-to-pdf=<file> --no-pdf-header-footer <file url>`, honored the CSS page size in Edge on Windows (two pages of 13.333in by 7.5in came out as 960 by 540 points; checked 2026-11), so a PC with any Chromium-family browser prints without a driver. The route taken is printed in one line and named in the delivery.
- The bare browser needs `--headless=new` and a profile folder of the run's own (`--user-data-dir`), or on Windows it opens a window in the user's browser session; the helper makes the folder in the system's temporary directory and removes it, read-only files included.
- `playwright-core` installed by the helper into the tools folder in the user's cache (`npm install playwright-core`, no browser download, a few seconds) is said in a line, not asked; the browser it launches is the installed Chrome or Edge by channel, as [headless.md](/docs/browser/headless.md) says. A neighbouring project's copy is used only through `PLAYWRIGHT_FROM`; the helper does not search for one.

## The layout report

- The report runs a script in the page, so it needs a driver: Playwright from Python or `playwright-core` from Node. With the bare browser alone it is skipped with a message, and the review relies on the sheet; the delivery says so.
- A fill under the threshold on a slide with `valign: "center"` measures the blocks' own height, not their position: a centered short list is still a thin slide.
- The lone-word check compares the last line's width with the last word's; a line that mixes type sizes can be reported once too often, and the sheet decides.

## The contact sheet

- PyMuPDF was absent wherever Playwright from Python was. The sheet is then the browser's screenshot of a sheet page the helper writes beside it from the HTML, each slide scaled with `zoom` three per row; it differs from the PDF only where the print cut a page, which the layout report names.
- A sheet of a long deck is a tall image; the bare browser takes it with `--screenshot` and a window height the helper sets from the page count.

## Reading the helper through SkillCDN

- The helper is read with `read_repo_file` at its path, in sections by offset (it is about 80 KB, 2026-11), and saved beside the deck file; the same file at the git host's raw address of the served commit (for a GitHub repository, `https://raw.githubusercontent.com/<owner>/<repo>/<commit>/<path>`, the commit from the connection's `Source` line) is an alternative where the connection pages slowly: a run took it after one section of about 23,000 characters, and its length matched the connection's count of 82,633 (2026-11).
- `load_skill` returns SKILL.md with its included page in two pages of 16 KiB (checked 2026-11); layout.md, registers.md and this page are linked from their phases and read when the phase comes.

## Fonts and colors

- A web font that has not loaded prints as a system fallback: the helper waits for the network to go idle, then for `document.fonts.ready`, then 300 milliseconds, the wait [headless.md](/docs/browser/headless.md) gives. A font CDN unreachable from the host falls back to the system's Korean-capable sans, and the delivery names it.
- A second brand color written into `steel` entered the stack's tone sequence and one cover stripe and read as emphasis where none was meant (2026-10); it is `accent` now, and `steel` stays derived from `navy` (layout.md "Theme").

## Gantt labels

- A bar that ends at the milestone's date or spans it collided with the label at the diamond's left (2026-10). The helper places the label at the right where the row's bar reaches the date, and the layout report lists an overlap that remains.
