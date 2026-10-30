# Conversion: from each format to Markdown

What converts a format is whatever the machine has; this page says how to look, what each format keeps, and what to do with what is lost. Values here are discovered at run time; nothing is pinned.

## Finding a converter

Look before converting, in this order, and tell the user what was found:

1. A converter already installed: a document converter that reads many formats and writes Markdown (`pandoc --version`; it does not read PDF), a PDF text extractor with its companions (`pdftotext -v`; `pdftoppm` renders a page to an image and `pdfimages` pulls the pictures out, in the same poppler tools), the office suite's own command line (`soffice --version`), or a Python with the libraries that read PDF with the sizes of its text (PyMuPDF, `python3 -c "import fitz"`), Word and spreadsheets (`python3 -c "import ..."`). The host's own file reading often reads PDF, Word and spreadsheets too; when it does, it is the simplest path for a few documents.
2. Something installable without administrator rights, with the user's agreement: a package of the language runtime at hand (`pipx`, `npx`), named as the user's platform installs it that day.
3. For images and scans, the agent's own vision model: look at the image, write what it shows.

A format nothing converts is reported with the files that have it, and what would convert them, and left out of this run.

## The originals

Every source file goes into the pack as it is, copied unchanged into `sources/` of the document set its documents belong to ([layout.md](layout.md) "Document sets"), before anything is converted from it, and the document names it in its front-matter `source`. Its name is kept, except that spaces and the characters a link or an LFS pattern cannot carry are replaced with hyphens, and the set's map names the original by the name it had. It is what an agent opens when the converted text is not enough: a figure described in a sentence, a table flattened, a scanned page transcribed. A result names it with the document and says where its bytes are; the hosts send it as a download, so a place in it is said in words ("page 12 of the original"). A file over what the host takes as it is (100 MB at GitHub, checked 2026-10) goes through Git LFS (`git lfs track "<pattern>"`, with the user's word), and a reader of the pack is sent to where the host serves the file. Nothing is stripped from an original and nothing is edited in it; a file that cannot be in the pack is a file for a private repository.

## What each format keeps

| Format | What survives conversion | What to check |
|---|---|---|
| Word (`.docx`) | Headings by style, lists, tables, footnotes, embedded images (`pandoc --extract-media=<dir>` writes them out) | Headings made by hand (bold text on its own line) arrive as paragraphs: promote them. Tracked changes are accepted or rejected before converting (`pandoc --track-changes=accept`, or `reject`), as the layout checkpoint settled, the default being to accept them; comments are dropped, since they are the editors' words and may name people. |
| PDF, text-based | The text in reading order, mostly (`pdftotext -layout` keeps columns apart); headings only from a reader that gives the sizes of the text (PyMuPDF's `page.get_text("dict")`), since plain text extraction carries no sizes; the pictures with `pdfimages -png` or PyMuPDF | Two-column layouts interleave: convert by region or fix by hand. Hyphenation at line ends. Running headers and footers repeat on every page: strip them. |
| PDF, scanned | Nothing; the pages are images | Render each page to an image (`pdftoppm -r 150 -png`, or PyMuPDF's `get_pixmap`), read it with the vision model and write the text, page by page, with a heading per page or per chapter. The page images are not kept, since the original in `sources/` is the image; a figure on a page is kept as a figure is. |
| Slides | Titles as headings, bullets as lists, notes when exported | One slide per section, the deck as one file or one per part; speaker notes under the slide's bullets as a paragraph. Pictures described. |
| Spreadsheets | Sheets as tables | One document per workbook, a heading per sheet, a table per sheet; a sheet too wide for a table is described in a paragraph and its columns listed. Formulas become values. |
| HTML, a wiki export | Headings, lists, tables, links | Navigation, menus and footers come along: cut them. Relative links to other pages of the export become links to the files they became. |
| Chat and email exports | Messages in order | One file per thread or per day, a heading per message with who and when, the body as paragraphs; attachments listed, not embedded. Personal data is the first thing to point out at the layout checkpoint, with the repository's visibility. |
| Plain text, Markdown | Everything | Add the front-matter and the headings the text supports. |

## Keeping the structure

- Headings keep their levels; the file's title is a level-one heading or the front-matter title, and the sections start at level two.
- Tables stay tables where they have a handful of columns; a wide table becomes a paragraph per row or a list, and the note says the source has the table.
- Footnotes go to the end of the section they belong to, or to a "Notes" section at the end of a short document, as text; a reference-style footnote is a link to its own note.
- Cross-references to other documents of the pack become links to their files, root-relative (`/docs/billing.md`) when the file is in another set.
- Page numbers, running headers and footers, and the source's own table of contents are dropped: the maps and the headings replace them.
- Equations, forms and diagrams that do not survive are marked with one line where they were, in words, since the hosts send an original as a download and a link into a page of it does nothing: "A diagram of the payment flow is on page 12 of the original."

## Figures and images

An image an agent cannot see is a hole in the document, and a picture is part of the document it belongs to. For every image that carries meaning:

- Keep the image file beside the document, in an `images/` folder of the set, and link it from where it was with alternative text that says what it shows in one sentence. The index searches those words and embeds no picture; the check reports a picture without any words, and a picture that is not there.
- Under a figure that carries meaning (a chart, a diagram, a screenshot of a setting), write a caption paragraph with what the figure says: the values a chart shows, the steps a diagram draws, the labels of a screenshot. This is what a search finds and an agent reads; the picture is for a person, and the outline of the document names it with its words.
- A decorative image (a logo, a divider, a stock photograph) is dropped with no note.
- A scanned page or a photograph of text is transcribed in full, as text, with a line that says it was transcribed from an image, so a reader knows to check the original for a doubtful character; the page image itself is not kept, since the original in `sources/` is the image, and a figure on the page is kept as any figure is.

The server embeds no image and runs no vision model: what the agent writes at conversion is all a search will ever know of a picture; the picture itself reaches a person through the link the outline gives.

## Checking a conversion

Open three converted files against their sources and compare: the headings, a table, a list, a passage in the middle. Count the sections `npx @skillcdn/cli check` reports for a document against the headings of the source. Where a document lost something the agent cannot restore, the note in the file says so and names the source.
