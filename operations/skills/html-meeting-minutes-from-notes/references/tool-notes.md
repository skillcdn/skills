# Tool notes: what the helper did in runs

How `scripts/render.py` and the browser behaved in this skill's own phases, by topic, as it holds now. A fact that can go stale names where it was seen and the month; a fact about how the tools work carries no date and changes when a run finds it wrong. What any browser skill shares is in the repository's [`docs/browser/`](/docs/browser/README.md).

## The browser launch

- Playwright from Python launches the installed Chrome by channel (`chromium.launch(channel="chrome")`) with no browser download, the driver installed with `pip install playwright` into a virtual environment; the helper tries `chrome`, then `msedge`, then Playwright's own Chromium, and the first that launches prints the PDF (Windows, Chrome, checked 2026-10). `--browser-check` runs that loop alone and names the channel.
- The whole render, check to PDF and preview, took about five seconds for two pages (checked 2026-10).

## The files

- A file name with spaces and Hangul, which the output-name pattern produces, loads through the `file:///` URL the helper builds from the absolute path and prints (checked 2026-10).
- The page count is read from the PDF's own page objects by a regular expression; Chromium wrote them in the clear, so the count matched the pages (checked 2026-10). When it reads zero, the helper prints no count, and the pages are counted in the PDF reader.
- The preview is a full-page screenshot of the HTML at A4 width, 794 pixels, before the print: it shows the content and the composition, not the page breaks, which the PDF shows.

## The style check

- The check walks every string of the file except the skipped keys and reports each offending string with its path, so that the fix is one edit in the minutes file; a file whose `style` lists only a few characters replaces the usual set, which is why `style` is left out when the usual set is meant, or starts with `usual: true`.
