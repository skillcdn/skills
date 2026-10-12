# Reading the document: text with hierarchy, images, layout types

How a PDF becomes the content map: text runs with their sizes and breaks, blocks with hierarchy levels, images ready for upload, and a layout type per page. Read in phase 2. The map's shape is [content-map.example.json](../assets/content-map.example.json); [pdf_extract.example.mjs](../scripts/pdf_extract.example.mjs) is one way to produce the text and the page renders.

## Setup

In the scratch folder, which stays the working directory for every script (the example's font and map paths are relative to it): `npm init -y`, then install a PDF library that exposes text runs with their transforms and renders pages (the example uses `pdfjs-dist` with its legacy build) and a canvas package it can render into (the example uses `@napi-rs/canvas`, which needs no native build). The host's own PDF reading tool, where it has one, is enough for looking at pages but not for sizes and positions; a tool that only extracts plain text loses the hierarchy. A document in another format is exported to PDF first.

## Text runs

For each page, every text run with: the string, its x and y (y measured from the top), its font size (the length of the transform's first column), its font name, its width, and whether it ends a line. Pages are 1-based.

Group runs into lines (same baseline within a pixel, in reading order), lines into blocks (consecutive lines of one size, closer than one and a half line heights, with the same left edge or a centered axis). A block's text is its lines joined with `\n`: those breaks are the document's and travel into the slides.

## Hierarchy levels

Rank the distinct sizes on each page from the largest down, then across the document. The largest on a content page is the title; the next, when it sits under the title, is the lead; a size that opens a card or a column is a heading; a bold size between the heading and the body that opens a group inside a card or a column is a sub-heading; the most frequent size by character count is the body; smaller than the body is a caption or page furniture (page numbers, footers, recognized by position at the page's edge). A bold run at the body size is a label inside its body block (recorded on the block as `labels: true`, built in the heading's weight and color), not a level. Record the level on each block; a block that resists the rule (a number in a circle, a tile's label) gets its level from its region in the layout.

## Images

Embedded images come out through the library's operator list: the paint-image operations of a page name image objects, read from the page's object store as width, height and raw pixel data in one, three or four channels (pdfjs-dist, `getOperatorList`, `OPS.paintImageXObject`, `page.objs`; checked 2026-10); the example script's `--images` mode writes them as PNG. Their size and placement say which block they belong to. Where the image is drawn as vectors (a device mockup, a diagram), render the page at three or four times and crop it by the region's coordinates. A crop carries the page's background in its margins: flood-fill from the border, turning pixels near the background color transparent, so that the crop sits on any slide fill (the script's `--transparent` mode). Name each file by page and role; the map lists them.

## Layout types

Read each page's render and assign one type; the plan maps it to the deck's parts (deck-spec.md "Layouts").

| Type | Cues on the page |
|---|---|
| Cover | One large title, a subtitle or date, a logo, little else |
| Headings and paragraphs | A title, then headings and running text down the page, no boxes or columns; the common shape of a report page |
| Lead and cards | A title, a lead sentence, two or three equal blocks side by side, each with a heading |
| Tiles with descriptions | A column of labelled shapes, each with a description beside it; often a side block of lists |
| Numbered rows | Several rows, each with a number or a label at the left and a description at the right |
| Device mockups | Phone or screen images in a row with a caption under each |
| Timeline | Dates or phases down one or two columns with items under each |
| Two columns | Two headed lists or paragraphs side by side |
| Closing | A thank-you line, a logo, contact lines |

A page that fits two types takes the one with fewer parts; a page that fits none is built from the title group and cards and named in the delivery as a guess.
