# Variation skills

How the skills that make variations (`web-concept-variations` in product, `html-design-variations` in design) are written and kept in step, for authors. What the skills share at run time is the document set [`docs/variation/`](../docs/variation/README.md), which agents read; this page says what went into the set and from where, what stays in a skill, what was left duplicated on purpose, and how the family is tested.

## Where the method came from

The set generalizes techniques the producing skills already carried, each written for one medium:

| In the set | Generalized from |
|---|---|
| `effect-brief.md`: the six readings and the mechanism line; other references by the effect and the device | The ad skill's analysis brief ("Why it works": hook, tension, turn, payoff; "Reading the reference": the rule of the world, the device, the figure, the signature line, the reveal) and its "Choose" rule among researched ads (candidates, honest, fit, proof, cost); the user's own words for what a variation must judge (intent, effect, aesthetics, fun, expected effect) |
| `axes.md`: the concept axes | The ad skill's story page (stake, figure, device, form, genre and register, order of telling); the card news build's rule that variation is the account's (a sequence that differs in two slots within the build's set) |
| `axes.md`: the design axes | The new-app skill's look (palette, type, shape and motion, tone, symbol); the Figma skill's layout types; the deck skill's "layout variety" |
| `not-ai.md`: signals in words | The card news build's register checks (closers, hedges, the same endings, the agent's voice) |
| `not-ai.md`: signals in a story | The ad skill's hook table (no decoding, a stake, a norm broken, concrete, specific, does not add up, withholds the turn) and its thumb test; "take the product away" |
| `not-ai.md`: signals in a look | The deck skill's design floor (icon card grids, number tiles, kickers, gradient text, blur, left borders, emoji as icons, breaks inside words) |
| `comparison.md`: a recommendation and a runner-up, the sheet the user picks from | The ad skill's "the runner-up is shown at the plan checkpoint" and its plan checkpoint; the deck skill's contact sheet |

A sentence that is true of a variation in any medium went into the set; a sentence true of one medium stayed in its skill and is cited from the set as an example. The ad skill's hook table is the sharpest list for a spoken hook and stays there; `not-ai.md` carries its general form.

## Duplicated on purpose, for now

The ad and drama skills were not changed when the set was written, because no run of them could be made in the authoring environment at the time. Their hook table, their "Choose" rule and their plan checkpoint therefore exist twice: in those skills, in their own form, and in the set, generalized. The duplication is deliberate and temporary: when a run of the ad skill can be made again, fold its references to the general form (cite `not-ai.md` and `effect-brief.md` from the story page, keep the hook table), test the seam in `handoff.md` with one request that needs both skills, and mark the row tested. Until then the `handoff.md` rows for the ad and the drama say untried, and `guide/tools/higgsfield.md` carries the same note.

## What stays in a skill

The intake (what is asked and what is derived), the phases and their artifacts, the verdict table in the skill's own terms, the hard rules, the example of the artifacts' shape; for the design skill, the look skeleton with its narrow-width rule and the script that renders and tiles. The set holds the method; a copy or a plugin has the method only where the skill includes it, which its Requirements say.

## What the first runs taught

Both skills were written from one free run each on a stand-in subject with a public, well-documented reference, before any fresh-session run:

- Positions first, lines second: a draft that wrote lines first made three candidates that differed in words only.
- Every candidate failed one signal on its first draft (a hook that needed decoding, an explanatory closer, a triad, a scene that worked for any product); the verdict is a phase, not a check at the end.
- Finding other references by the device and the effect works; by the subject it returns lookalikes of the reference.
- The phone screen is part of the design verdict: two of four looks read at the desktop width and failed at a phone width (one word per line; two columns too narrow), and were fixed with a narrow-width rule before the sheet.
- A sheet needs "to produce" in the medium's own units, or the recommendation argues cost by impression.

The runs' subject, reference, candidates and screens stay out of the repository; the method is what came in.

## Testing

Each skill is exercised from a fresh session with a stand-in subject and a public reference, to the sheet and the user's pick (nothing is spent). A seam is tested with one request that needs the variation skill and a producing skill, run through to the producing skill's first checkpoint; `handoff.md` marks the row with the date. The acceptance search for the pack's guide ("four looks for this landing") is run again after the design skill is served, and its examples page updated.
