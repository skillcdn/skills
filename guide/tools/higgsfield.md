# Higgsfield skills

How the skills that drive Higgsfield (`higgsfield-…`) are written and kept in step, for authors. What the skills share at run time is not here: it is the document set [`docs/higgsfield/`](../../docs/higgsfield/README.md), which agents read. This page says what goes there, what stays in a skill, and how a run's findings travel.

## One server, named tools

Higgsfield is one MCP server, so the skills name its tools by their exact names (`models_explore`, `generate_video`, `sandbox_exec`, ...) and say what to do when one is missing. Models are never named as requirements: a skill says what a model must do (take references, make its own audio, output 9:16, offer a lowest tier), how to find the latest that does with `models_explore`, and how to choose when several qualify. A model id appears only in a dated note.

## What every Higgsfield skill does the same way

The conventions are listed once, for agents, in the set's [README](../../docs/higgsfield/README.md): a preflight before any spend, `use_unlim` explicit, the lowest tier and one job per call, a role list is not proof, the model speaks, overlays are code, two plain decodes decide, the intended words on screen, a higher resolution as a separate step, generated people delivered as generated. Each skill states them in its hard rules in the form its workflow gives them (which call is preflighted, what its verdict table does with a wrong word), because a manifest's rules reach only the skills below it and the family spans areas, and because a copied or installed skill has only its hard rules.

## What is shared and what stays in the skill

| In `docs/higgsfield/` | In the skill |
|---|---|
| `models.md`: reading the catalog, the tier table, the preflight and its answers, `use_unlim`, one job per call, refused jobs, a higher resolution; dated notes on costs, render times and roles | Which models qualify for this skill and why, the reserve, the estimate's shape, the recommendation order, the fallback |
| `cast.md`: the image models, the style line, the portrait prompt, the approval loop, frame to take, reuse by id; dated notes | Who is cast (a site's own person, a voice with no face, one portrait per look, sets), what the skill's record keeps |
| `sandbox.md`: lease and polls, commands and scripts, uploads, files in, images, fonts, ffmpeg, verification; dated notes | The skill's own passes (the analysis of a reference, an assembly's steps), its example scripts |
| `decodes.md`: the review pass and how its output is read, silence and hallucination; dated notes on the decoders | The verdict table, the retry budget, how lines are written and retried |
| `pronunciation.md`: the sounds per language and the dated outcomes | Nothing |
| | `references/tool-notes.md`: what the tools did in this skill's own phases, dated |

The test for a sentence: would it be true, word for word, in the next Higgsfield skill? Then it belongs in the set. A page of the set is linked from the phase that reads it, with a root-relative path (`/docs/higgsfield/<topic>.md`), and never included: the spec keeps `skillcdn.include` inside the skill directory, so a shared page costs one `read_repo_file` call when its phase comes and no page of the skill's load.

A skill runs without the set when it is mounted alone, installed as a plugin or copied: its Requirements say so and name `docs/higgsfield/` in the repository as where to fetch the pages. Keep every hard rule and every step of the workflow in the skill for that case; the set holds knowledge, not rules.

## Where a finding goes

What a run taught goes into the files the same day, with the date and the model, as behavior and never as a run's product, persona, lines or story:

- A tool that behaved differently for every skill of the family (a refusal, a folding, a limit, a price shape): the topic page of the set, in its prose where it changes what every skill does, in its dated notes otherwise.
- A sound outcome: `pronunciation.md`, under its language, and the sound moves to the list it belongs to.
- An edge of one skill's own phase: that skill's `tool-notes.md`.
- A step a fresh agent had to guess: the skill's `SKILL.md` or the reference of that phase.

A skill run by an agent without the repository at hand reports its findings in the delivery, in a short list for whoever maintains the skill; both skills ask for that list.

## Testing

A skill is exercised from a fresh session that gets only the user's request and reads the skill through SkillCDN at the repository root, with the real server. First to the cost checkpoint (no credits), read against the skill's text; then one production with the checkpoints answered as the user would. What a fresh agent had to guess goes back into the files; what the tools did differently goes where "Where a finding goes" says. A change to a page of the set is read by every skill of the family: read each skill's links to that page before pushing.
