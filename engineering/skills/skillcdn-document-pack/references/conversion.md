# Conversion: from each format to Markdown

What converts a format is whatever the machine has; this page says how to look, what each format keeps, and what to do with what is lost. Values here are discovered at run time; nothing is pinned.

## Finding a converter

Look before converting, in this order, and tell the user what was found:

1. A converter already installed: a document converter that reads many formats and writes Markdown (`pandoc --version`), a PDF text extractor (`pdftotext -v`), the office suite's own command line (`soffice --version`), or a Python with the libraries that read PDF, Word and spreadsheets (`python3 -c "import ..."`). The host's own file reading often reads PDF, Word and spreadsheets too; when it does, it is the simplest path for a few documents.
2. Something installable without administrator rights, with the user's agreement: a package of the language runtime at hand (`pipx`, `npx`), named as the user's platform installs it that day.
3. For images and scans, the agent's own vision model: look at the image, write what it shows.

A format nothing converts is reported with the files that have it, and what would convert them, and left out of this run.

## What each format keeps

| Format | What survives conversion | What to check |
|---|---|---|
| Word (`.docx`) | Headings by style, lists, tables, footnotes, embedded images | Headings made by hand (bold text on its own line) arrive as paragraphs: promote them. Tracked changes: accept or reject before converting, as the user says. |
| PDF, text-based | The text in reading order, mostly; headings by size, sometimes | Two-column layouts interleave: convert by region or fix by hand. Hyphenation at line ends. Running headers and footers repeat on every page: strip them. |
| PDF, scanned | Nothing; the pages are images | Read each page with the vision model and write the text, page by page, with a heading per page or per chapter; keep the images if the user wants them. |
| Slides | Titles as headings, bullets as lists, notes when exported | One slide per section, the deck as one file or one per part; speaker notes under the slide's bullets as a paragraph. Pictures described. |
| Spreadsheets | Sheets as tables | One document per workbook, a heading per sheet, a table per sheet; a sheet too wide for a table is described in a paragraph and its columns listed. Formulas become values. |
| HTML, a wiki export | Headings, lists, tables, links | Navigation, menus and footers come along: cut them. Relative links to other pages of the export become links to the files they became. |
| Chat and email exports | Messages in order | One file per thread or per day, a heading per message with who and when, the body as paragraphs; attachments listed, not embedded. Personal data is the first thing to check. |
| Plain text, Markdown | Everything | Add the front-matter and the headings the text supports. |

## Keeping the structure

- Headings keep their levels; the file's title is a level-one heading or the front-matter title, and the sections start at level two.
- Tables stay tables where they have a handful of columns; a wide table becomes a paragraph per row or a list, and the note says the source has the table.
- Footnotes go to the end of the section they belong to, or to a "Notes" section at the end of a short document, as text; a reference-style footnote is a link to its own note.
- Cross-references to other documents of the pack become links to their files, root-relative (`/docs/billing.md`) when the file is in another set.
- Page numbers, running headers and footers, and the source's own table of contents are dropped: the maps and the headings replace them.
- Equations, forms and diagrams that do not survive are marked with one line where they were: "A diagram of the payment flow is in the source, page 12."

## Figures and images

An image an agent cannot see is a hole in the document. For every image that carries meaning:

- Keep the image file beside the document, in an `images/` folder of the set, when the user wants it in the pack; link it from where it was, with alternative text that says what it shows in one sentence.
- Under a figure that carries meaning (a chart, a diagram, a screenshot of a setting), write a caption paragraph with what the figure says: the values a chart shows, the steps a diagram draws, the labels of a screenshot. This is what a search finds and an agent reads; the picture is for a person.
- A decorative image (a logo, a divider, a stock photograph) is dropped with no note.
- A scanned page or a photograph of text is transcribed in full, as text, with a line that says it was transcribed from an image, so a reader knows to check the source for a doubtful character.

The server embeds no image and runs no vision model: what the agent writes at conversion is all a search will ever know of a picture.

## Checking a conversion

Open three converted files against their sources and compare: the headings, a table, a list, a passage in the middle. Count the sections `npx @skillcdn/cli check` reports for a document against the headings of the source. Where a document lost something the agent cannot restore, the note in the file says so and names the source.
