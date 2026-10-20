# Notes: keeping what a run learned

A question answered once is answered for everyone who asks it next, when the answer is kept where the next run looks: in the pack, as a document, found by its words.

## Where notes live

A document set named `notes` under the pack's document roots (`docs/notes/` where `docs` is the root), with a map, declared in the manifest like any set. A pack of several areas keeps a notes set per area where the questions belong to one area. The next run's phase 1 searches it first, scoped with `path`, before searching the pack.

## The shape of a note

One file per question, named by the question in a few words (`refund-timing.md`), with the front-matter every document carries and five parts:

```markdown
---
title: How long a refund takes
description: What the handbook says about when a refunded card payment reaches the customer, and what it does not say about bank transfers. Answered 2026-10.
source: research note, 2026-10
---

# How long a refund takes

**Question.** How long does a refund take to reach the customer?

**Answer.** Five to ten business days for a card payment, depending on the customer's bank. The handbook does not give a time for a payment recorded by hand.

**Evidence.**

- `docs/invoicing.md`, Invoicing > Refunds and credit notes: "the refund reaches the customer within five to ten business days, depending on their bank."

**Not found.** No time is given for a refund of a bank transfer or cash.

**Checked.** 2026-10, against the handbook as served then.
```

- The description says what the note answers, in the words someone would ask with: it is what a search ranks.
- Every quote carries its path and heading path, so that the next reader opens the section and sees whether the pack still says it.
- A question asked again updates its note: the answer, the evidence and the date change; the file does not multiply.

## What stays out

- Anything the question or the user's context carried that is not about the pack: names, customers, the matter the question served.
- Guesses: a note holds what the pack says and what it does not, never what the agent supposes.
- Offsets and limits: they change with every edit of the document; the path and the heading path hold.

## The map and the manifest

The notes set has a `README.md` with one line per note, like every set; a new note adds its line. A new notes set is also a line in the map of the set it sits under (`docs/README.md` for `docs/notes/`), as any subfolder with a map is, so that a person reading the map finds the notes; and it is added to the `documents` of the manifest that governs it when the root is not the default `docs` next to the manifest. The commit follows the repository's agreement; a push to the default branch is served within minutes, and the note is found by the next run.
