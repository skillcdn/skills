# Review rounds: what came back, and what replaced it

The composition rules and the design floor in SKILL.md were learned from the review rounds of one external kickoff deck, four rounds from the first render to the version the reviewer accepted. This file keeps each note as a pair, the note as the reviewer said it and the move that answered it, so that the next agent recognizes the same note on its own draft and makes the move before the reviewer has to.

## Round 1: structure

| The note | The move |
|---|---|
| The cover subtitle is a long explanatory sentence. | One tagline under ten words; the cover is the title, the tagline and the logos, matched to the organization's finished deck. |
| Subtitles on every page. | A subtitle only where the slide needs its one sentence; most slides have none. |
| A note at the foot of every page, and a summary banner on most. | Both removed. A caveat is said in the meeting; the quality bar became one bold sentence on the scope slide. |
| The environment is bullets beside a small diagram. | A full-width diagram with a numbered process strip above it, step numbers as chips on the nodes, the boundary as a dashed frame. |
| The schedule carries a weekly cadence and an interim date the outline never gave. | Only the outline's schedule, as a Gantt chart: a bar per phase, a diamond for the deadline. |
| A "things to decide today" slide and an appendix of figures. | Both cut. The figures the audience needs moved into the method slide. |

## Round 2: content

| The note | The move |
|---|---|
| The client's logo is missing from the cover; it always comes first. | `client_logo` on the cover, a thin rule, then the presenter's logo. |
| The tagline should carry the technical keywords the audience cares about. | The tagline names what is searched, generated and automated, in the audience's terms. |
| The overview repeats the project's name, which everyone in the room knows. | Cut. The overview is the goal and the facts. |
| The out-of-scope list need not be spelled out. | Cut. |
| Two durations that are alternatives per page were presented as if they added up. | Stated as alternatives, with the rule that decides the total (the share of pages of each kind). |
| The method skips the preparation: the document map, the table of contents, writing the procedures as skills. | Added as steps of the method. |
| The platform the work stands on is invisible. | A slide of its own: what it is, how it is distributed, who maintains it, what it does here. |
| Items the outline gives equal time should have equal bars; the delivery month is work too. | Equal bars for the sequence, the delivery month as a bar, the deadline as a diamond. |

## Round 3: design

| The note | The move |
|---|---|
| The layout is predictable and icons are overused. Is there no better way to make slides? | The way was fine; the defaults were not. Every slide had been a grid of same-size cards of icon, heading and text. Replaced by a different layout per slide: a statement beside a definition list, numbered rows, a loop beside a numbered list, two brand panels, a strip above a diagram, a Gantt chart, profiles. Icons removed from every item; the design floor added to the phase 4 checks. |
| Why does the quality bar talk about who signs off? | Cut. A quality bar is the floor and the open ceiling, two sentences. |
| The product's logo in the slide header is out of place. | Removed from the header. A product's mark belongs in its brand panel. |
| A package registry shown as a generic icon; use its real logo. Use logos and symbols, not an icon pack. | The registry's, the code host's, the editor's and the agent's own marks, from their brand assets; the platform's wordmark and symbol; the client's logo. |
| A date wrapped inside a tile and nobody checked. | The tile row removed in favor of a definition list; `word-break: keep-all` for Korean so that no word breaks inside; wrapped values added to the review list. |
| Does the deck show that the agent works in a loop inside the platform's structure, on feedback? | The `loop` block: search, generate, review, apply around a ring with the platform's and the agent's marks at the center, beside the numbered steps. |
| The agent is a specific product, installed as an editor extension and brought into the closed network; only the agent is used, not its maker's model; show its logo. | The agent's brand panel: how it is installed and brought in, which model it talks to, the sentence that its maker's model is not used; its mark on the node that holds it. |

## Round 4: wording

| The note | The move |
|---|---|
| The contract period on the overview means nothing to the room; the deadline is what matters. | The period row cut; the deadline kept. |
| Where a model is named beside the agent, show the model's own mark, not the agent's. | The model's mark from a brand-icon set. |
| The word chosen for the hardware is awkward. | A plain word ("work laptop"), with "to be delivered" where that matters. |
| The team slide wants a subtitle that names the team's specialty, and each person's title should name their role in that specialty. | A subtitle on the team slide; titles such as "CEO, AX developer" and "AX designer (UI/UX)". |
| The slide title for the asks should be plain. | "Items to confirm" rather than "what we ask of you". |
| A compound the reviewer's language reads as foreign. | Replaced by the ordinary term; the reviewer's ear decides. |

## What generalizes

- A note that names one slide usually names a default the whole deck repeats. Fix the default, then every slide.
- The reviewer asks "is there a better way?" when the composition is lazy, not when the tool is wrong. The answer is the design floor, not a different tool.
- Real marks beat icons every time a thing has a name. An icon is for the rare item whose meaning a word does not carry.
- A visual check is a check only when it is written down: a wrapped value, a word broken inside, a loop whose center touches its nodes are on the phase 4 list because each one shipped once.
- Facts the reviewer confirms (a model name, a deadline, a title) are recorded where the organization keeps its records, and the deck file is the only thing edited.
