# Reviewer notes: what a draft is sent back for

The composition rules of each register ([registers.md](registers.md)) and the design floor in SKILL.md came out of review rounds on real decks. This page keeps what reviewers reject, in its general form, with the move that answers each, so that the next agent recognizes the default on its own draft and makes the move before a reviewer has to. Read it when a draft comes back with notes, and before planning a deck for a reviewer who has sent one back before. Nothing here names a deck, a client or a product; a note on one slide usually names a default the whole deck repeats, and the move fixes the default.

## The whole deck

| The default rejected | The move |
|---|---|
| The whole deck's look, called plain, not professional enough, or not the kind of document expected: the register is wrong, not the composition | The look sheet with both registers; the user picks; every slide rebuilt from the deck file. A plan or a report composed as a poster (one photograph, big type, no figures) goes to the report register. |
| A second draft that looks no better than the first | After two rounds on the look, the register choice goes back to the user with both look sheets rather than a third guess. |
| A label over a bar, or a half-empty page, found only after the delivery | The layout report before the sheet: an overlap, a cut, a wrapped value and an under-filled slide are measured, not seen; a deck is delivered with an empty report. |

## The cover

| The default rejected | The move |
|---|---|
| A subtitle that is a long explanatory sentence | One tagline under ten words; the cover is the title, the tagline and the logos, matched to the organization's finished deck. |
| A tagline that names nothing of the substance | The tagline names the technical substance of the work (the task, the technology, the result) in the audience's own terms. |
| A client's deck without the client's logo first | `client_logo` on the cover, a thin rule, then the presenter's logo. |

## Pages

| The default rejected | The move |
|---|---|
| A subtitle on every page | A subtitle only where the slide needs its one sentence; most slides have none. |
| A note at the foot of every page, and a summary banner on most | Both out. A caveat is said in the meeting; a quality bar is one bold sentence on the scope slide. In a report, the source line under a table or a panel is the one note that stays. |
| A product's logo in the slide header | Out of the header; a product's mark belongs in its brand panel. |
| A title that states the speaker's stance toward the room | A title that names the slide's content ("Items to confirm"). |

## Structure

| The default rejected | The move |
|---|---|
| Every slide a grid of same-size cards of icon, heading and text, an icon on every item | A different layout per slide: a statement beside a definition list, numbered rows, a loop beside a numbered list, two brand panels, a strip above a diagram, a Gantt chart, profiles. No icon per item; the design floor checked in phase 4. |
| A system drawn as bullets beside a small diagram | A full-width diagram with a numbered process strip above it, step numbers as chips on the nodes, the boundary that matters as a dashed frame. |
| A named product shown as a generic icon | The real marks of every named product from their brand assets; the client's logo. |
| A value wrapped inside a tile | A definition list instead of tiles; `word-break: keep-all`; wrapped values measured by the layout report. |
| A method that repeats, drawn as a list | The `loop` block: the repeating steps around a ring with the tools' marks at the center, beside the numbered steps. |

## Content

| The default rejected | The move |
|---|---|
| A schedule with a cadence or an interim date the outline never gave | Only the outline's schedule, as a Gantt chart: a bar per phase, a diamond for the deadline. |
| A slide of things to decide today, and an appendix of figures | Both out; the figures the audience needs go into the slide of the method they belong to. |
| An overview that repeats what the room knows (the project's name, the boundaries nobody contests) | The overview is the goal and the facts. |
| Alternative durations per item presented as if they added up | Stated as alternatives, with the rule that decides the total. |
| A method without its preparation | The preparation the outline implies (what is set up before the cycle runs) is a step of the method. |
| A platform the work stands on, left invisible | A slide of its own: what it is, where it comes from, what it does here. |
| Items given equal time with unequal bars; the delivery period missing from the schedule | Equal bars for the sequence, the delivery period as a bar, the deadline as a diamond. |
| A quality bar that names who signs off | The floor and the open ceiling, two sentences, nothing about sign-off. |
| Two products easily confused, one shown where the other is used | Told apart in the brand panel: which one the work uses, what it talks to, each with its own mark. |
| A figure the room does not need beside the one it does | The figure that matters kept, the other cut. |
| A figure on a report slide with no source | The `kpi` tag names the source, or says the figure is to be confirmed; a table carries its sources in its note line. |

## Wording

| The default rejected | The move |
|---|---|
| A word that is awkward, or reads as foreign in the audience's language | A plain word, with "to be confirmed" where that matters; the ordinary term, and the audience's ear decides. |
| A team slide whose titles do not say each person's role in this work | A subtitle that names the team's specialty; titles that name the role in this work, in the organization's own words. |

## What generalizes

- A note that names one slide usually names a default the whole deck repeats. Fix the default, then every slide.
- A note on composition (icon card grids, predictable layouts, boxes everywhere) is answered by the design floor; a note on the whole deck's look or its professionalism is answered by the register choice, with the look sheet. Neither is answered by writing the HTML by hand.
- Real marks beat icons every time a thing has a name. An icon is for the rare item whose meaning a word does not carry.
- A visual check is a check only when it is written down or measured: a wrapped value, a word broken inside, an overlap, an empty half page are on the layout report or the phase 4 list because each one has reached a reviewer.
- Facts a reviewer confirms (a name, a date, a title) are recorded where the organization keeps its records, and the deck file is the only thing edited.
