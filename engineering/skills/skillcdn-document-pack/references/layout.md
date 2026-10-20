# Layout: how a pack of documents is cut and described

The format says what is served and searched ([document packs](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/skill-repo.md#document-packs)). This page says how to cut a body of documents into files that an agent finds and reads well, and how to describe them.

## Document sets

A document set is a directory of Markdown under a document root, with a map. Cut by subject and audience: a handbook's chapters are one set, the manuals of one product one set, the reports of one year one set. A set of two or three documents is fine; a set of two hundred wants subsets, each with its map. Name a set in one or two lowercase words with hyphens (`billing`, `api`, `release-notes`), as a path an agent will type.

```
handbook/
  SKILLCDN.md
  docs/
    README.md
    getting-started.md
    billing.md
    api/
      README.md
      auth.md
      jobs.md
  ko/
    SKILLCDN.md             language: ko
    docs/
      README.md
      onboarding.md
```

The default document root is `docs` next to a manifest; `documents` in the manifest names others. A folder written in another language is a folder of its own with a manifest that declares the language, under the root or beside it.

## One file per document or chapter

A file is what a search lists and an agent reads: it carries a title and a description, and its sections are what a result names. The right size is a document or a chapter of one.

| Source | Files |
|---|---|
| A document of a few pages | One file. |
| A long document with chapters | One file per chapter, named by the chapter, each with the document's title and the chapter's in its front-matter; the document's own map lists them in order. |
| A long document without chapters | Split at its top-level headings, or at the headings the text supports, into parts a reader can take in one sitting. |
| A page of a book, a slide, a sheet | Never a file of its own: join pages into their chapter, slides into their deck or its sections, sheets into one document per workbook with a heading per sheet. |
| Many short notes on one subject | One file per note when each stands alone, else one file per subject with a heading per note. |

The bounds: a deployment indexes a file up to its per-file limit and serves it up to its read limit, both configuration with defaults ([deploy](https://github.com/skillcdn/skillcdn/blob/main/deploy/README.md)); `npx @skillcdn/cli check` names a file too large to be searched, which is the sign to split it. A file of a few thousand words is far under both. Keep the chapter's heading path at the top of a split file (`# The Guide: Installing`), so that a chapter read alone says what it belongs to.

## Front-matter

Every file carries:

```markdown
---
title: Installing on Windows
description: Where the installer is, what it asks, and what to do when the service does not start. For administrators of a Windows workstation.
source: install-guide-2026.pdf, chapter 3, exported 2026-10
---
```

- `title`: the document's own title, as its readers know it.
- `description`: one or two sentences of what the document holds and who reads it, in the words a reader would search with. This is what a search ranks after the title and what the map repeats.
- `source`: where it came from and when, without anything private. SkillCDN ignores the field and keeps it in the file for whoever reads the source text.

A file without front-matter is listed by its first level-one heading and the paragraph after it; write the front-matter anyway, so that the description is written for search rather than taken from the text.

## Headings

Headings are the structure a search names and an agent walks: `browse_repo` lists them with the offset and the length of each section, and a result names the section that matched. A heading tells what its section holds, in the reader's words; "Refunds and credit notes" rather than "Section 4.2". Keep the levels of the source; where the source has none, add the headings the text supports, and no more. A section of two or three paragraphs is the grain a result reads well; a section of twenty pages is a chapter.

## Maps

The `README.md` of a document set is its map: what the set is, in a sentence, then one line per document, in the order a reader meets them.

```markdown
# The Tidewell handbook

Everything a workspace owner, dispatcher or technician needs, one document per topic.

| Document | What it covers |
|---|---|
| getting-started.md | Creating a workspace, inviting the team, the first job, the mobile app. |
| billing.md | Quotes, invoices, payment terms, deposits, late fees, refunds, sales tax. |
| api/README.md | The REST API: authentication, jobs, customers, pagination and limits. |
```

Write each document's name as a link to its file, so that a person reading the map on the git host opens it too. A map is read by an agent before it searches, and shown as the folder's introduction. A map under a document root is also a document of its own, found by its words: keep the line of a document to what the document's title and description say, not more, so that the map does not outrank the document it points to. The map at the root of the pack also points to the folders written in other languages, in a sentence, so that an agent reading the English map knows the Korean documents exist and how to search them.

## Manifests

The root manifest, `SKILLCDN.md`, names the pack, says who it is for, declares the document roots and the language, and may carry a rule or two for how the documents are read:

```markdown
---
name: Tidewell handbook
description: The handbook of Tidewell, a scheduling and invoicing app, as a pack of documents. Use to find how a feature works, what a role may do, and how billing behaves.
documents:
  - docs
language: en
license: MIT
---
# Rules for reading this handbook

Read the map in `docs/README.md` first, then search for the words of the question and read the section a result names before answering.
```

A folder in another language carries a manifest with `language` and a description of its own. `language` chooses how the words are matched, by stems for English and by pairs of characters for Korean, Japanese and Chinese, and tells an agent what language to search in; a Korean folder without it is matched as English text would be.

The `license` decides what a deployment may pass on: a permissive license serves the documents in full; without one the pack is served with a provenance notice; a restrictive one has the documents described only, with a link to the source ([licenses](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/skill-repo.md#licenses)). The user chooses; the manifest says.

## What stays out

- Secrets, credentials, personal data, customer material: the pack is served to whoever holds the address.
- Drafts and older versions of a document that exists in a final form, unless the history is the point.
- Page furniture: running headers and footers, page numbers, tables of contents the maps replace.
- Files that are not text an agent can read (binaries, rendered media) unless they are the images of the documents, kept beside them.
