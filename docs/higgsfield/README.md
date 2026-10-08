# Higgsfield: what its skills share

The skills that drive Higgsfield (`higgsfield-…`, in any area) share how the tools behave, how credits are quoted, how models and images are found, how a take is decoded, and what the video models do with the sounds of each language. That knowledge lives here once, one file per topic, and is kept current in one place; each skill links the file from the phase that reads it and carries its own workflow, checkpoints, verdicts and rules itself.

| Document | Holds | Read |
|---|---|---|
| [`models.md`](models.md) | Finding the latest models in the catalog, the lowest tier, the credit preflight, presets, free-trial unlimited generations, one job per call, refused and failed jobs, a higher resolution later; dated notes on costs, render times and what the generators accepted or refused. | Before the cost checkpoint, and when a job is refused. |
| [`cast.md`](cast.md) | The image models for portraits and first frames, the style line, the portrait prompt, the approval loop, how a frame becomes a take, reuse by id; dated notes on the image models. | Before portraits and first frames. |
| [`sandbox.md`](sandbox.md) | The sandbox's lease and polls, background jobs, the command limit, uploads and their reservations, files in, fonts, looking at images, the assembly's shape, verification; dated notes. | Before the first sandbox call. |
| [`decodes.md`](decodes.md) | The review pass that settles what a take says: two plain speech-to-text decodes, the tiebreak, what supports a reading and never decides, silence and hallucination; dated notes on the decoders. | Before the first take. |
| [`pronunciation.md`](pronunciation.md) | What the video models do with the sounds of each language run so far, and the dated outcomes. | When lines are written, and before a retry. |

## Who reads this

The skills of the repository that drive Higgsfield: [`higgsfield-shorts-ad`](../../marketing/skills/higgsfield-shorts-ad/SKILL.md) in marketing and [`higgsfield-shorts-drama`](../../media/skills/higgsfield-shorts-drama/SKILL.md) in media. Each reads these pages through the repository connection, with `read_repo_file` at `docs/higgsfield/<file>`, when the phase that links them comes. A skill mounted alone, installed as its area's plugin or copied into another agent does not have them: its Requirements say so and name this directory in the repository, which is where to fetch them. What a skill cannot work without (its workflow, its checkpoints, its verdict table, its hard rules) stays in the skill.

## What every Higgsfield skill does the same way

- **Spend only after a preflight.** `generate_video` and `generate_image` with `get_cost: true`, once per distinct parameter set; the sum with a reserve goes to the user before any job, images included.
- **`use_unlim` explicit on every call**, `false` unless the user asked for free-trial unlimited generations.
- **Lowest tier, one job per call, `count` 1, never a batch tool**, so the review of one take can stop a fault before the next take repeats it.
- **A role list is not proof that two roles combine in one call.** The first real take is the test, and the cost checkpoint names the fallback.
- **The model speaks.** Every spoken word is the video model's native audio; no text-to-speech, dubbing or voice tools.
- **Overlays are code.** Captions, text, cards, logos, inserts, end cards: ffmpeg and Pillow in the sandbox, never the video model.
- **Two plain decodes decide what was said.** A decode prompted with the intended line supports a reading and never overrules two plain ones; a word that is really wrong is never handed to the user as unsettled.
- **Captions and subtitles show the intended words;** speech-to-text supplies the clock.
- **A higher resolution is a separate step**, quoted at the delivery and started only on the user's word.
- **Generated people are delivered as generated.** The delivery says so; the platform's label for AI-made content is the user's to set.

Each skill states these in the form its own workflow gives them, in its hard rules or in the phase they belong to, so that they hold where these pages do not travel.

## Adding what a run taught

A tool that behaved differently from what a page says: trust the tool, and change the page in the same change, with the date and the model. A sound outcome goes to [`pronunciation.md`](pronunciation.md) under its language, and the sound moves to the list it belongs to. A note that holds for one skill only (its own phase, its own artifact) goes to that skill's `references/tool-notes.md`. Notes record behavior, a final consonant lost before a particle or a job refused with its error, never a run's product, persona, lines or story. An agent running a skill without the repository at hand reports the finding in its delivery, for whoever maintains the skill.
