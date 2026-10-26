# The script: thesis, thread, density, register, caption

How the slides' text is written from the brief in the spec's format, and the checks each sentence passes before it is set.

## The thesis

One sentence, the brief's `angle` in the post's language. It is not the headline; the headline is made from it in the spec's headline style (a news title states the fact or the claim in two lines of the spec's characters per line). A post whose brief has no angle is a report: its thesis is its leading fact.

## The thread

The beats in the order that carries the thesis, one per slide, from the spec's typical count. Two shapes cover most posts:

| The post is | The thread |
|---|---|
| A story (why something is happening, who, what it means) | Phenomenon (what is happening, the numbers), a turn (what is not obvious about it), the reason (the angle, in the outlet's reading), the close (what it looks like from here) |
| An announcement or a guide (a rule, an event, a day that changes) | Why now, where, when and what changes, how much (the numbers), what to do |

Not every slide carries text of the account's. Which slides do is the spec's: a beat that is a mood, a quote or a scene takes the type the account uses for it (a photo alone, a photo with a note element, a captured frame whose own caption is the beat), and a build whose types carry material alone (frames stacked whole, the story told by their captions) has text of the account's on the cover only. A deck that puts sentences on every slide to fill it reads as an explainer, and a deck that writes over material the account shows as it is reads as another account's.

Each beat names the fact ids from the brief it carries; a beat carried by material names the fact ids the material's own caption states. An element's lines come from the brief too: an image's printed caption, the angle's quoted sentence or a fact's source sentence, shortened to the spec's line length and marked with what they came from; an element that would need words the brief does not hold is left off. A beat whose facts the brief lacks is dropped or kept as material, and the checkpoint says so with the offer to extend the brief.

## Density

From the spec's `density` per slide type and element, as counts: the sub's characters, the lines, the sentences, the characters per line; the cover's headline characters per line. The line is the unit on the slide: where the spec's sentences are longer than a line (two sentences over three lines), the plan places each break by hand at a clause or phrase end within the characters per line, and no line is left for the renderer to break. A line the renderer broke on its own is the first thing a reader of the format sees. One fact per sentence where the spec says so. What does not fit goes to the caption, which carries the detail in the format's own posts.

Count before setting: characters in the post's script, spaces included, against the spec's range for each line. A line at the top of the range is a candidate to shorten. A note keeps the length its source gives it, within the spec's range or below it, never padded.

## Register

The spec's `register` patterns, applied sentence by sentence. The checks, with what each prevents:

| Check | Right | Wrong |
|---|---|---|
| The headline | The spec's `register.headline`: a news title that states the fact, or the account's own device (a fragment with the account's tail, a quote) in its lines and characters | The other device: a teaser where the account states, a flat title where the account teases; a pun the story does not earn |
| The sub | The spec's `register.sub` in the spec's characters | A full sentence where the account uses a noun phrase; an explanation of the slide |
| Body endings | The spec's `register.body`: its speech level and endings, mixed at the spec's proportion | Every sentence ending the same way; the caption's register on a slide |
| Closers | None; the last sentence is a fact or a noun phrase | A sentence that tells the reader what the slide meant ("this is the story they are watching", "that is what one reader said") |
| Hedges | None | "it seems", "reportedly" where the fact has a source; the source goes in the caption |
| Voice | The account's, as the spec's patterns give it | The agent's; a first-person line on a slide unless the spec shows one |
| A quote | As the article printed it, marked as a quote, with who said it in the sub or the sentence | Paraphrased as a fact |

A sentence that fails a check is rewritten, not softened. Read the finished slides once more as the account's editor would: a line a news desk would not print is rewritten.

## The caption

The spec's `caption.parts` in their order, in the spec's caption register: the leading facts with their dates and outlets (from the brief's sources), the context, a closing line in the voice the spec describes, the credit line from the brief's `credits.md` rewritten in the spec's pattern (the outlet with the photographer where the brief names one), for the images placed on slides only, or built from `images[].credit` when the brief has no credits file, the mentions (only a handle the brief carries as a fact with its source; an unverified handle goes to the checklist, not the caption), and for an event the spec's information block. Where the spec gives no order for a part, the credit line comes after the closing line and the information block last; no hashtags unless the spec shows them. The caption is where the numbers and the detail the slides left out live; a reader who wants the whole story reads it there. It is written into `caption.txt` with the plan and finished at the delivery.

## The plan's text block

For every slide in the plan: the spec's type (and variant or elements), the account's own text as the type has it (the headline's lines; the sub and the sentences each followed by its fact ids in brackets; an element's lines with what they came from; the parts the spec's type names) or "material only" with the material's own caption and the fact ids it states, and the image file with its treatment, its position or crop and its legibility. The checkpoint shows this block as a numbered list; the build reads it.
