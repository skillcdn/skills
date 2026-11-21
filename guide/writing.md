# Writing skills

How the pack's rules for text are kept in one place, for authors. What the skills share at run time is the document set [`docs/writing/`](../docs/writing/README.md), which agents read; this page says what went into the set and from where, what stays in a skill, what is duplicated on purpose for now, where the skills disagree today, and how the `writing/` area and the set are tested.

## Where the set came from

Each sentence of the set generalizes a rule a skill already carried for one medium, written from that skill's own runs and review rounds; a rule only one medium has is named with its medium, and the one sentence that bridges two rules, on the hedge, is named below:

| In the set | Generalized from |
|---|---|
| `readers.md`: the reader and what they do with the text | The minutes skill's review notes (the reader who acts the day after), the deck skill's two registers (a deck spoken over, a deck read as a document), the topic brief's readers and their own case |
| `readers.md`: the language, the terms, one word for one thing | The minutes skill's language input and its terms, the new-app skill's localization page, the creative research's report words |
| `readers.md`: the register, the stance and the tone, the voice | The minutes skill's neutral written register, the card news build's register measured from the format's spec, the topic brief's stance and tone, the AI-feel page's voice signal |
| `sentences.md`: one idea a sentence, a lead and a plain sentence, titles, headings | The deck's spec, the deck's reviewer notes, the minutes skill's composition rules and review notes |
| `sentences.md`: what is cut, rewriting | The AI-feel page's closers and summaries, the card news build's register checks, the minutes skill's cut rules |
| `facts.md`: nothing the inputs do not hold, a figure, to be confirmed | The hard rules of the deck, the minutes, the card news build, the topic brief and the document skills; the deck's spec for the tag; the research reports' counts and labels |
| `facts.md`: a hedge | The AI-feel page (no hedge where a fact has a source), the minutes skill (a decision firm, an answer no firmer than what was said), the topic brief (a reading is the outlet's, never the agent's) and the research reports (the report's own readings, counted), which read as opposite until they are set side by side. "A hedge belongs where the source is hedged" is the set's own sentence for all four |
| `facts.md`: a quote and a claim, dates and names | The card news build's script page, the topic brief's sourcing page, the document answer skill's hard rules, the minutes skill's meeting facts |
| `outside-readers.md` | The operations area's rule that nothing internal crosses, the deck's proposal register, the minutes skill's split and its wording notes |
| `house-style.md` | The question both the deck and the minutes skills ask, the minutes helper's usual set, the deck's replacement for a middle dot, the minutes skill's record of the answer |

A sentence that is true of a text in any medium went into the set; a sentence true of one medium stayed in its skill. Text that reads as machine-written stayed where it was, in `docs/variation/not-ai.md`, which the set links: that page is included by the two variation skills, and moving its word signals would have changed both.

## What stays in a skill

A skill carries what it cannot work without, so it keeps the form its own medium gives each rule: the deck's slide strings and blocks, the minutes' sections and their terms, the card news build's counts per line from the spec, the ad's hook table. The set holds no limit of one medium (characters per line, words per cue, pages) and no layout rule. The sharper list wins in its skill, as `not-ai.md` says of its own.

## Duplicated on purpose, for now

No existing skill links the set yet. Each skill that writes text states its rules in its own files, as it did before the set, and a run of it reads those. Making a skill read the set is a change to that skill: its Requirements name the page, the phase that writes links it, and a fresh agent runs it once (`guide/adding.md`, "Changing an existing skill"). That is done one skill at a time, when the skill is next revised, and the general sentences its references then repeat are cut to the medium's own form. Until then the set is reached by search, by the jobs index's section on jobs with no skill, and by the writing skills to come, which include its pages.

The order that costs least: the minutes skill and the deck skill first, since both render with a helper and spend nothing; the card news build with the topic brief next, as one chain.

## Where the skills disagree today

Found when the set was written (2026-11), and stated in the set as they are, not smoothed over:

- **Where the house style's answer is kept.** The minutes skill records the organization's answer for the next run; the deck skill keeps it in the deck file and asks again. The two helpers read one shape and apply one default since 2026-11: before, the deck's banned nothing unless the deck file declared a set, its example set lacked the Hangul middle dot and four other characters the minutes set has, and it read a `forbidden` map the minutes' did not, so that a deck with a Hangul middle dot passed where the same sentence failed the minutes.
- **Naming tools.** The minutes name the organization's own tooling by a generic noun; a proposal deck names the tools the work stands on by their real names. Both are right for their document, and `outside-readers.md` gives each its row.
- **The hedge and the reading.** No skill is wrong; the rule was said from several sides. A news post prints no reading of the agent's own, and a research report's readings are its findings. `facts.md` has one table, with a row for each.
- **The default language.** The minutes take the language of the notes, the research reports the user's language whatever the ads are in, the topic brief the language asked for or the market's. `readers.md` states the three as cases of one rule, the reader's language.

## How the set's pages are written and kept

As knowledge pages (`skill-authoring.md`, "Knowledge pages"): one section per topic under a heading an agent would search with, a rule as a statement, a fact that can go stale with its month. No run's subject, person or line. What a run of any writing skill teaches about text in general changes the sentence of the set it bears on; what it teaches about one kind of text goes into that skill.

## The area and its skills

`writing/` holds the skills whose result is the text itself, read as it is: an article, a report, a self-introduction, a briefing ([roadmap.md](roadmap.md), "M9: Writing"). It was created before its first skill, with its manifest and its catalog, so that the set had its home; a skill arrives as every skill does, written from the job done once. A skill whose text is a part of another area's job stays in that area (the launch posts in marketing, the opportunity brief in product) and reads the same set.

Every writing skill includes the set's pages its runs need, which the format serves from the root's `docs/` to a skill of any area, and states only what its kind of text adds: the parts of the text and their order, the questions it asks, its checkpoint with the text itself, and its review.

## Testing

A change to a page of the set is dry-read by a fresh agent against the skills it was generalized from: a sentence that contradicts a skill's own rule is a finding, about the set or about the skill. Once skills include the set, a change to an included page is a change under each of them, verified as the verification skill's change review says. A request for a text with no skill ("write a press release for this") is a case of the finding round ([finding.md](finding.md)): the agent says no skill fits and names the set as what it would write by.
