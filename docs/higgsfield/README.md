# Higgsfield: what its skills share

The skills that drive Higgsfield (`higgsfield-…`, in any area) share how the tools behave, how credits are quoted, how models and images are found, how a take is decoded, and what the video models do with the sounds of each language. That knowledge lives here once, one file per topic, and is kept current in one place; each skill links the file from the phase that reads it and carries its own workflow, checkpoints, verdicts and rules itself.

| Document | Holds | Read |
|---|---|---|
| [`models.md`](models.md) | Finding the latest models in the catalog and the roles seen so far, the lowest tier, the credit preflight, presets, free-trial unlimited generations, one job per call, refused and failed jobs, a higher resolution later, the prices and times seen. | Before the cost checkpoint, and when a job is refused. |
| [`cast.md`](cast.md) | The image models for portraits and first frames and how they behave, the style line, the portrait prompt, the approval loop, how a frame becomes a take, reuse by id. | Before portraits and first frames. |
| [`sandbox.md`](sandbox.md) | The sandbox's lease and polls, commands and scripts, uploads, files in, looking at images, fonts, ffmpeg and audio, verification. | Before the first sandbox call. |
| [`decodes.md`](decodes.md) | The review pass that settles what a take says: two plain speech-to-text decodes, the tiebreak, what supports a reading and never decides, what the decodes cannot settle. | Before the first take. |
| [`pronunciation.md`](pronunciation.md) | What the video models do with the sounds of each language run so far, by kind of sound, with what fixed each. | When lines are written, and before a retry; included with each skill. |

## Who reads this

The skills of the repository that drive Higgsfield: [`higgsfield-shorts-ad`](../../marketing/skills/higgsfield-shorts-ad/SKILL.md) in marketing and [`higgsfield-shorts-drama`](../../media/skills/higgsfield-shorts-drama/SKILL.md) in media. Each declares `pronunciation.md`, which every run writes and reviews lines with, in its `skillcdn.include` by its root-relative path, so that the page arrives with the skill wherever SkillCDN serves it, and reads the other pages through the repository connection, with `read_repo_file` at `docs/higgsfield/<file>`, when the phase that links them comes. Without that connection (a mount of an area or of one skill, a host that takes skills through the skills extension) the linked pages cannot be read, and a skill installed as its area's plugin or copied into another agent has none of them: its Requirements say so and name this directory in the repository, which is where to fetch them. What a skill cannot work without (its workflow, its checkpoints, its verdict table, its hard rules) stays in the skill.

## What every Higgsfield skill does the same way

- **Spend only after a preflight.** `generate_video` and `generate_image` with `get_cost: true`, once per distinct parameter set; the sum with a reserve goes to the user before any job, images included.
- **`use_unlim` explicit on every call**, `false` unless the user asked for free-trial unlimited generations.
- **Lowest tier, one job per call, `count` 1, never a batch tool**, so the review of one take can stop a fault before the next take repeats it.
- **A role list is not proof that two roles combine in one call.** The first real take is the test, and the cost checkpoint names the fallback.
- **The model speaks.** Every spoken word is the video model's native audio; no text-to-speech, dubbing or voice tools.
- **Overlays are code.** Captions, text, cards, logos, inserts, end cards: ffmpeg and Pillow in the sandbox, never the video model.
- **Two plain decodes decide what was said.** A decode prompted with the intended line supports a reading and never overrules two plain ones; a word that is really wrong is never handed to the user as unsettled.
- **Captions and subtitles show the intended words;** speech-to-text supplies the clock.
- **A higher resolution is a separate step**, offered at the delivery and started only on the user's word.
- **Generated people are delivered as generated.** The delivery says so; the platform's label for AI-made content is the user's to set.

Each skill states these in the form its own workflow gives them, in its hard rules or in the phase they belong to, so that they hold where these pages do not travel.

## How these pages are written

Each page is organized by topic and says what holds now, so that an agent finds a fact where it would look for it, not where it was learned. A fact that can go stale (a price, a model's roles or quirks, a limit read from a tool's description) names the model or the source it was seen on and the month it was checked, at the end of the sentence; a fact about how a tool works carries no date, and changes when a run finds it wrong. The evidence that makes a fact credible (a number, an error text, what the decoders wrote) sits in the sentence it supports. There is no chronological log and no run narrative.

## Adding what a run taught

A tool that behaved differently from what a sentence says: trust the tool, and change that sentence in the same change, with the model and the month where the fact can go stale. A sound outcome goes to [`pronunciation.md`](pronunciation.md), into the list it belongs to, with the word as a sound example and what settled it. A note that holds for one skill only (its own phase, its own artifact) goes to that skill's `references/tool-notes.md`, in the same shape. Notes record behavior, a final consonant lost before a particle or a job refused with its error, never a run's product, persona, lines or story. An agent running a skill without the repository at hand reports the finding in its delivery, for whoever maintains the skill.
