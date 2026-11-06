# Registers: the two shapes a deck takes

A register is the shape a deck takes for its readers: what the cover carries, how a body page is framed, which blocks carry its content and what the design floor allows on top of the common floor in SKILL.md. There are two. The register is derived from the request and the outline in phase 1, confirmed on the look sheet at the plan checkpoint, and written into the deck file's `meta.register`. Its rules are applied in phase 1, when the slides are planned, never after a render.

## Which register

| The request or the outline says | Register | Why |
|---|---|---|
| A kickoff, a proposal, a status report, a presentation to a client or a partner, a meeting with people outside the organization | `proposal` | The deck is spoken over in a room, by the presenter, to people who know the project; each slide carries one message |
| A business plan, a plan for investors, a company presentation or introduction, an internal report, a plan for a board, "a proper PPT" for an idea | `report` | The deck is read as a document before or after the meeting: it needs a way to find a section, figures with their sources, and facts in tables |
| Neither | `report`, recommended on the look sheet with `proposal` as the alternative | A deck made from an idea or a plan is read more than it is presented |

The look sheet (SKILL.md, phase 1) shows the cover and one body slide, the one that carries a table, a schedule or the figures, in the recommended register's frame and in the other's, on one image with the recommendation; the blocks are the recommended register's in both, since the look compares the frames. "OK" takes the recommendation, the other register's name takes it instead, and the whole deck renders in the one chosen.

## Rules for both

- **Content from the outline and the user's answers.** A figure the outline gives is tagged with where it comes from (the organization's own count, a pilot's result); one the outline does not source, and anything the user left open, is "to be confirmed", in the deck's language. A section the outline gives nothing for is one slide that says what is to be confirmed, or is dropped and listed at the plan checkpoint; the length rules below bend before this rule.
- **A schedule only as the outline gives it.** Months make a Gantt chart; a horizon without months ("the first year") makes `steps` in stages or a `timeline` by quarter, the split said to be the agent's in the delivery; no cadence, no interim date, no "weekly" the outline does not say. A range given for several items in sequence is split, and the delivery says the split is the agent's.
- **Durations** that are alternatives per item are stated as alternatives with what decides the total, never summed.
- **Two products easily confused** (a tool and the service it runs on) are told apart: which one the work uses, what it talks to.

## proposal: an external proposal

Pages on a light gradient, an accent bar beside the title, a page number alone, no footer. The composition rules:

- **Cover:** the title in one or two lines, one tagline, the logos. The tagline names the technical substance of the work in the audience's own terms (the task, the technology, the result), not a generic phrase and not a sentence. For a client, the client's logo comes first, then the presenter's. No client, date or brand footer unless the organization's own decks carry one (`footer: true`, or a string for one line of the organization's own, such as its domain).
- **Closing:** the thanks line, the logo and the contact lines, centered on a dark page. Contact lines carry what the organization's finished decks carry, and nothing is added that they do not.
- **A content slide is its title and its blocks.** A subtitle only where the slide needs its one sentence; most slides have none. No note at the foot of a page and no summary banner: a caveat is said in the meeting, and a block that restates the slide is a block the slide loses. No label above the title and no section numbers: the sequence carries nothing the room needs.
- **Structure from type, rules and real marks, not from boxes.** The overview is a statement in large type beside a definition list with thin rules. A quality bar is one bold sentence with its lead inline. Sequence is carried by numbers only where the order is the information (steps, a schedule). A real mark stands for a named thing; a line icon is for the rare item whose meaning a word does not carry, never one per item. Figures go into the definition list or the inline facts, never into number tiles, each with its source as a row of the list or a tag inline, since the page has no footnote.
- **Layout variety.** No two consecutive slides share a layout. The set to draw from: statement beside facts, numbered rows, a loop beside a numbered list, two brand panels, a process strip above a diagram, a Gantt chart, profiles. Same-size cards are the last resort, never the page structure.
- **Cut what the room already knows.** The project's name on the overview, the boundaries nobody will contest, an appendix of figures: out, unless the outline asks. A figure the audience needs goes into the definition list or the inline facts on the slide it belongs to.
- **Nothing said for the room's own ears.** An external proposal carries none of the outline's pricing logic, staffing, remarks about the audience or open doubts; the plan checkpoint lists what was left out. A report keeps them where its reader needs them (the use of funds, a role still to be hired, an open figure), each tagged.
- **A method that repeats** is a loop with the tools' marks at its center, beside the numbered steps; the facts that go with it (volumes, durations) sit under both as inline facts. The preparation the outline implies is in the steps.
- **The tools the work stands on** get one slide of brand panels: each panel its real wordmark or symbol and name, one line on what it is, the marks of where it lives with a fact beside each, and what it does in this work.
- **A system** is a full-width diagram with a numbered process strip above it; each step's number is a chip on the node where the step happens; the node that holds the tools carries their marks; the boundary that matters is the dashed frame, and what crosses it sits outside with its arrow across the line.
- **A schedule** whose phases differ in length is a Gantt chart: one row per phase, bars in the months the outline gives, equal bars for items given equal time, the delivery period as a bar and the deadline as a diamond. Equal phases with bullets under each are a timeline.
- **A team** is profiles: an initial, the name, the role in this work, then rows for the role, education and history, in the words of the organization's own profile cards.
- **Length:** eight to ten pages for a fifteen-minute talk. A page cut is a page cut; its content moves into a block on another page only when it is a fact the audience needs.

Blocks for this register:

| The outline has | Block | Why |
|---|---|---|
| The goal and the facts of the work (volume, outputs, period, deadline) | `columns` of `statement` + `facts` | The goal in large type, the facts in a list with rules; nothing boxed |
| Four to six numbered things (scope items, requests) | `rows` | A number, a name and a sentence each; the number is what the room refers to |
| A quality bar or one sentence to remember | `statement` with `lead` | One bold sentence with its lead inline; not a banner, not a note |
| A method that repeats, with its steps and durations | `columns` of `loop` + `numbered`, then `facts` inline | The loop shows the cycle and the tools; the numbers carry the order; the durations sit under both |
| The tools the work stands on | `columns` of two `brand` panels | Each tool by its real mark, where it lives, what it does here |
| A system of parts and where the work happens | `steps` + `diagram` with node `logos` | The strip names the procedure; the chips say where each step runs |
| A schedule with phases of different lengths; equal phases with bullets | `gantt`; `timeline` | Bars and a diamond; or one rail per phase |
| The people doing the work | `profiles` | One card per person in the organization's own card format |
| Questions the meeting must answer; next steps with an owner or a date | `rows` or `qa`; `rows`, or `numbered` without descriptions | Only when the outline asks for such a slide; the owner or the date goes in the description |
| A method that runs once, in order | `numbered` for up to six steps; `stack` when short labels build toward a result; `timeline` when the steps have dates | One block per method; a method that repeats is the loop |
| Three items, or seven or more | `rows` or `numbered` for three, never `cards`; seven or more split across two slides or grouped | A slide holds four to six things at most |

## report: a corporate report

White pages. Above the title, a section label: the number and the name of the section the slide belongs to, taken from the contents. A rule under the header. A footer with the organization's name, the document's name and the date at the left, the page number at the right. The composition rules:

- **Cover:** the kind of document as a label ("Business plan", "사업 기획안"), the title, one tagline, a table of the author, the date and the classification (`meta_rows`), the organization's white mark, and a photograph the organization or the user supplied where there is one (`photo`); without one, the stripes on the right. Nothing is generated.
- **Contents:** a slide with a `toc` block after the cover, two columns, each entry its number, its section's title and one line; the contents slide itself carries no section label. The body slides carry the same numbers in their section labels (`section`), and `toc.auto` builds the contents from them.
- **A section label only from the contents.** The label above a title is the section's number and name, never a kicker written for one slide.
- **Figures carry their source.** A `kpi` panel (one to three figures per deck, each a value with its unit, a label in one sentence, and its source or its tag) or a `table` with a `note` line naming the sources. An amount the outline does not give (the ask) is a panel whose value is "to be confirmed", or the numbered list alone.
- **Facts in rows are a table:** the features and their value to the user, the revenue lines, a comparison; a header row and the first column bold. A wide table splits across two slides rather than shrinking its type.
- **The problem, defined,** is a numbered `cards` grid of at most two by two, no icons, each card a title and one sentence; or `rows`.
- **A plan in stages** is `steps` with detail items (the stage, when, what, and the facts under the strip), or a `gantt` with a sub line under each row's label and the milestones where the outline gives months.
- **The ask** (funds, a decision) is a `kpi` panel in the navy tone with the amount, beside a `numbered` list of what it buys.
- **Photographs** only where the organization or the user supplied them, in a `photo` block beside a definition list or a numbered list, with the credit the source requires.
- **No note at the foot of a page** except the source line under a table or a panel. A caveat that matters is a row in the table or a tag on the figure.
- **Length:** twelve to sixteen pages when the outline fills them, the contents and the closing counted; a thin outline makes a shorter deck, never an invented one.

Blocks for this register:

| The outline has | Block | Why |
|---|---|---|
| The summary of the plan and its headline figures | `statement` + `kpi` (one to three) | The message in large type; the figures with their sources beside it |
| The problem or the need | `cards` with `numbered: true`, two by two at most; `rows` | Numbered, so that the solution can answer each; no icons |
| The product or the service, feature by feature | `table` (the feature, what it does, the value to the user) | Rows the reader scans and compares |
| The market and its figures | `table` with a `note` for the sources, or `kpi` with tags | A figure without its source is a claim |
| The business model, how money moves | `steps` detail | Stages with who pays whom and the facts under them |
| The schedule | `gantt` with `sub` lines and milestones where months are given; `steps` or `timeline` for a horizon | Phases with what each delivers |
| The team | `profiles` | The organization's own card format |
| The ask | `kpi` in the navy tone + `numbered` | The amount and what it buys |
| What the plan rests on, with a picture | `columns` of `photo` + `facts` | A supplied photograph beside the facts |
| An appendix of figures | `table`, one per slide | Readable type over a complete table |

## Mid-run notes

| The note | Re-enters at |
|---|---|
| On the whole deck's look or register (plain, not professional enough, not the kind of document expected, too much like a poster) | The register, chosen again by "Which register" with the note's own words: a note that names a kind of document ("like a company presentation", "like a business plan", "like a proposal") takes the register that table gives it, which may be the one in use, and "presentation" or "PT" for a company's own deck is a company presentation, a `report`; a note that only calls the deck plain or not professional takes a proposal to the report and keeps a report a report, its rules re-read. The look sheet of both registers, the one now recommended first, is shown before the whole deck renders, even after a go-ahead, since the note is the user's word on the look; then every slide is rebuilt from the deck file. After two such rounds the choice goes back to the user with both look sheets |
| On composition (predictable, too many icons, boxes everywhere) | The design floor, every slide |
| On one slide's content | That slide's entry in the deck file |
