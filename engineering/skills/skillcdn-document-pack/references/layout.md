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
    images/
      billing-flow.png      a figure, linked from billing.md with the words that say what it shows
    sources/
      handbook-2026.docx    the original billing.md and getting-started.md were made from
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

The default document root is `docs` next to a manifest; `documents` in the manifest names others. A folder written in another language is a folder of its own with a manifest that declares the language, under the root or beside it. The originals a set's documents were made from sit in `sources/` inside the set, and its pictures in `images/`; the chapters of one original share its entry.

## One file per document or chapter

A file is what a search lists and an agent reads: it carries a title and a description, and its sections are what a result names. The right size is a document or a chapter of one.

| Source | Files |
|---|---|
| A document of a few pages | One file. |
| A long document with chapters | One file per chapter, named by the chapter, its `title` the chapter's own with the document's title before it where the chapter's alone would not say what it belongs to (quoted in YAML when it holds a colon followed by a space), the heading path at the top of its body; the set's map lists them in the order of the original. |
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
source: sources/install-guide-2026.pdf
---
```

- `title`: the document's own title, as its readers know it.
- `description`: one or two sentences of what the document holds and who reads it, in the words a reader would search with. This is what a search ranks after the title and what the map repeats.
- `source`: the original the document was made from, as the path of its file in `sources/`, written as a link destination is, relative to the document or from the repository root, or a list of them for a document made from several. A result names the original with the document, the outline in its header and a read on its first page, each with where its bytes are, so that a reader opens the original in one step. A source that is no file of the pack (an export of a system, a conversation, a date) is said in words, which stay text; a value written like a path that names no file is reported by the check.

A file without front-matter is listed by its first level-one heading and the paragraph after it; write the front-matter anyway, so that the description is written for search rather than taken from the text.

## Headings

Headings are the structure a search names and an agent walks: `browse_repo` lists them with the offset and the length of each section, and a result names the section that matched. A heading tells what its section holds, in the reader's words; "Refunds and credit notes" rather than "Section 4.2". Keep the levels of the source; where the source has none, add the headings the text supports, and no more. A section of two or three paragraphs is the grain a result reads well; a section of twenty pages is a chapter.

## Maps

The `README.md` of a document set is its map: what the set is, in a sentence, then one line per document, in the order a reader meets them.

```markdown
# The Acme handbook

Everything a workspace owner, dispatcher or technician needs, one document per topic.

| Document | What it covers |
|---|---|
| getting-started.md | Creating a workspace, inviting the team, the first job, the mobile app. |
| billing.md | Quotes, invoices, payment terms, deposits, late fees, refunds, sales tax. |
| api/README.md | The REST API: authentication, jobs, customers, pagination and limits. |
```

Write each document's name as a link to its file, in the order a reader meets them, and for a set cut from one original the chapters in the order of the original, so that a person reading the map on the git host opens it too. A map is read by an agent before it searches, and shown as the folder's introduction; a search marks it as the overview of its folder, so that an agent goes on to the document it names. A map under a document root is also a document of its own, found by its words: keep the line of a document to what the document's title and description say, not more, so that the map does not outrank the document it points to. The map at the root of the pack also points to the folders written in other languages, in a sentence, so that an agent reading the English map knows the Korean documents exist and how to search them.

## Manifests

The root manifest, `SKILLCDN.md`, names the pack, says who it is for, declares the document roots and the language, and may carry a rule or two for how the documents are read:

```markdown
---
name: Acme handbook
description: The handbook of Acme, a scheduling and invoicing app, as a pack of documents. Use to find how a feature works, what a role may do, and how billing behaves.
documents:
  - docs
language: en
license: MIT
---
# Rules for reading this handbook

Read the map in `docs/README.md` first, then search for the words of the question and read the section a result names before answering.
```

A folder in another language carries a manifest with `language` and a description of its own. `language` chooses how the words are matched, by stems for English and by pairs of characters for Korean, Japanese and Chinese, and tells an agent what language to search in; a Korean folder without it is matched as English text would be.

The `license` decides what a deployment may pass on: a permissive license serves the documents in full; without one the pack is served in full with a provenance notice, to whoever the host lets see the repository; a restrictive one has the documents described only, with a link to the source ([licenses](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/skill-repo.md#licenses)). The user chooses at the layout checkpoint, with this default: none for an organization's own documents in a private repository, which are served in full to the people the host shows the repository to, and a permissive license only where the user means to let anyone pass the text on; a restrictive license defeats the pack, and is named as such. The example above carries `license: MIT` because it is a public pack.

`search` keeps the documents out of a search the user does not want them in: `search: { meaning: false }` in a manifest keeps the documents it governs to the search by words, so that their text is never sent to the embedding model a deployment runs, and `search: { hub: false }` in the root manifest keeps the pack out of the search across every pack of the deployment, found at its own address alone; by default a pack is searched by meaning where the deployment offers it and found across packs. Offer both at the layout checkpoint, with the recommendation to keep the defaults unless the text must not reach a model the deployment runs; a private pack is in no search across packs, since that search covers public packs alone, so `hub` arises for a public pack only. Write what the user chose.

## What goes in a private repository, and what stays out

- The repository's visibility decides who reads the pack: the host shows a private repository to its people alone, and SkillCDN serves it to them alone. Material that is not for everyone (a secret, personal data, a customer's material) goes in a private repository, with its originals, and nothing is stripped from the text on the agent's own judgment; what looks secret or personal is pointed out at the layout checkpoint for the user to decide: keep it, leave it out of the text (the original keeps it), or make the repository private.
- Drafts and older versions of a document that exists in a final form, unless the history is the point.
- Page furniture: running headers and footers, page numbers, tables of contents the maps replace.
- Files that are not text an agent can read (binaries, rendered media), other than the originals in `sources/` and the pictures of the documents in `images/`, which are listed, never searched, and reached through the link a result gives.
