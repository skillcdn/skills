# The house style: characters and heading forms that stay out

An organization's own rule for the documents that leave it: characters and heading forms it does not use. This page holds the usual set, the question that settles it, how a text is written within it, where the answer is kept, and how the two skills that render a document check it.

## The usual set

- Middle dots in every form: `·`, `•`, `‧`, `∙`, `ㆍ`.
- The em dash, the en dash and the horizontal bar: `—`, `–`, `―`.
- Circled numbers: `①` to `⑳`.
- A bracketed head: a string that starts with `[`, as a label in brackets before a sentence does.

It is the default where neither the request nor the organization's records say otherwise.

## Asking for the house style

Asked once, at the skill's first stop with the user, in the user's language, and only when nothing at hand answers it:

"Does your organization ban any characters or heading forms in external documents? The usual set is middle dots, em and en dashes, circled numbers and bracketed heads; one word keeps that set."

Look first in the request, next to the material the user brought, and in the organization's brand folder or handbook.

## Writing within the house style

- A text for the outside is written within the house style from the first draft, the user's own words included. The check is a net, not the method.
- A middle dot joining two nouns becomes "and" or a comma. Where the user's own words were changed for the style, the delivery says so.

## Where the answer is kept

The minutes skill writes the answer into the organization's own records (a notes file in its brand folder, or its handbook where it has one), so that the next run, for any reader, finds it and does not ask again. The deck skill writes it into the deck file alone.

## How it is checked

The deck skill, the product deck skill and the minutes skill each have a helper that checks every string of the document's file against a set of characters and lists each offending string with where it is. The file is fixed and rendered again; a draft rendered without the check is for a look, never a delivery.

All read the same shape and apply the same default:

- The check runs where the document leaves the organization: a minutes file and a product deck unless they say `external: false`, a deck only where it says `external: true`.
- With no style in the file, the usual set. `usual: true` starts from the usual set and the file's `forbidden` adds to it; without it, `forbidden` is the whole set.
- `forbidden` maps a character, or a string of characters checked one by one, to its name.
- A bracketed head is any string that starts with `[`, banned with the usual set or where `no_bracket_heads` is set.

A set written for one skill's file reads the same in the others'; each skill's spec page gives its keys, and the product deck adds a list of phrases its user rejected.

The house style is the organization's rule for what leaves it. Inside any text, for any reader, a middle dot joining words in a sentence or a long dash setting off an aside reads as machine-written, and is rewritten as [`/docs/variation/not-ai.md`](/docs/variation/not-ai.md) says; as a separator outside a sentence either may stay.
