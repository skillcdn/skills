# Model selection and credit estimate

Nothing is generated before the user accepts the model and the estimate. The video model is discovered at run time, never pinned, and the user sees the candidates' totals side by side.

## What the episode needs from a video model

| Needs | Why |
|---|---|
| Several reference images in one call, and a start frame | The portraits of every character in the cut keep the cast the same across many cuts; the approved first frame fixes the composition. A model that takes only references, or only a start frame, is a fallback, and the plan says what it loses. A role list is not proof that the two roles combine in one call: the preflight accepts what the generation may refuse, and the first cut is the test ([tool-notes.md](tool-notes.md)). |
| Native dialogue audio with lip sync | The model speaks every line; there is no text-to-speech. |
| 9:16 | Vertical platforms. |
| Durations that cover 7 to 12 seconds | The cut lengths of the table. A model with fixed options takes the nearest allowed length, and the table is written to them. |
| A lowest tier: the lowest resolution, the lowest quality mode, or a draft flag | Cost. Drafts are what the user pays for; an accepted take can be finalized or upscaled later as a separate, quoted step. |

## Finding the candidates

```
models_explore  action: recommend  type: video  query: several reference images of characters and a set in one call, start frame, native dialogue audio with lip sync, 9:16, 7 to 12 second clips, lowest resolution tier
models_explore  action: search  type: video  query: <each family the recommendation named>
```

The recommendation returns only part of the catalog (on 2026-10-08 it left out the cheapest candidate), so also page through `action: list` with `type: video` and keep every model that meets the table above, reading `medias[].roles` (a reference role such as `image_references`, and `start_image`), the audio parameter, `aspect_ratios` and the duration range. Within a family keep the latest general model: the highest generation number, not an edit, extension, turbo or product wrapper. Then read each candidate's parameters with `action: get`. Two or three candidates is usual; one is enough; none means the skill cannot run as written, and the user is told what is missing.

## Lowest tier

| The model exposes | Lock |
|---|---|
| A `resolution` parameter | Its lowest option. |
| A quality `mode` | Its lowest option. |
| A draft flag that makes a lower-resolution take finalizable later | The draft flag; the finalize price the preflight names goes to the delivery. |
| Several of these | All of them at their lowest. |
| None | The default; say so in the estimate. |

Audio stays on for every cut; a cut without a line still carries its sound. Never a higher tier for drafts, however small the difference looks.

## Preflight

Call `generate_video` with `get_cost: true` and the exact parameters a cut will use: the model, the tier, `9:16`, the duration, audio on, `use_unlim` explicit, and a reference media id where the model's reference mode needs one even to quote (any image the account holds serves; when none is at hand, or `show_medias` fails, make a tiny placeholder image in the sandbox with ImageMagick and upload it with `media_upload` and `media_confirm`, which costs no credits; the number does not depend on which). Nothing is submitted or charged. The cost depends on the model, the duration, the tier and the audio flag, not on the prompt, so preflight once per candidate and distinct duration of the cut table and reuse the numbers.

When the preflight returns a preset recommendation instead of a number, read the preset id from the answer and call again with it in `declined_preset_id`; pass the same field on the real generation. The skill uses no presets and does not put the notice to the user.

Images are preflighted with `generate_image` and `get_cost: true`, once per image model and setting ([cast.md](cast.md)): the portrait model for one portrait per character and look, the reference-capable model for one set per place and one frame per cut.

## The estimate

```
Model        Tier    Takes (per cut)                 Images                               Reserve                        Total
<candidate>  <low>   8, 10, 12, ... = <n> s = <c>     <p> portraits, <s> sets, <f> frames  +<r> takes, +<p+s> img, +<f/3>  <t>
<candidate>  <low>   ...                             ...                                  ...                            <t>
Balance: <credits> · Finalize at <res>: <price> per take, optional, not in the total · Free-trial unlimited generations: <available or not>
```

The shape is illustrative; present only numbers that came back from `get_cost` in this run. The reserve is one take per three cuts (rounded up) priced at the longest cuts, one retry per portrait and per set, one frame per three cuts; it is the whole retry budget, images included, and beyond it every retry needs consent. Read `balance` before presenting; when the total exceeds it, say so and offer a shorter episode or fewer cuts before anything else.

The user sees, in plain words: the recommended model with its total including the reserve and the reason in a line; the other candidate's total; the balance; the finalize price as a separate, optional line; and the **fallback**: what happens when the first cut shows the recommended model refusing the frame with the references, or speaking the dialogue language badly (a model the notes have never heard speak it is on trial in its first cut). The fallback is the next candidate at its quoted total, or the same model with the frame as reference image 1; when the user's word covered it, the switch happens without a second stop, and the images already made are kept; otherwise it is re-quoted. Recommend by these, in order: the model that takes both references and a start frame; a record in the dialogue language; the lower total; the durations the table needs. One word proceeds; the user may pick the other candidate or change the plan, which is preflighted again.

## Free-trial unlimited generations

If the catalog reports that the account can spend free-trial unlimited generations on a candidate, say so in the estimate. Use `use_unlim: true` only when the user explicitly asks for it; never add it to save credits on their behalf, and never drop it once they asked. Set `use_unlim` explicitly on every generation call, `false` unless the user asked: left out, the server may withhold the job and return a question (`unlim_choice`) instead of a take. If that happens anyway, put the question to the user once and call again with their answer.

## Refused and failed jobs

A job the server refuses (moderation, an invalid parameter) or that fails without a result is not a take and not the cut's retry: fix what it names (a fight described by its sound and the reaction on a face rather than the blow, a parameter read again from the catalog) and submit again. Check `transactions` when a charge is in doubt; a charge for a job that gave nothing is a ledger row with its reason, and it counts against the accepted estimate. After two refusals of one cut, stop and show the user the shot with what was refused. On a transport timeout the job may still have been submitted: read `show_generations` before submitting again.

## After the episode: a higher resolution

The episode is delivered at the draft tier. Two ways up, each quoted at the delivery and started only on the user's word: finalize every accepted take at the resolution the catalog names (the preflight showed the price per take; the assembly script is re-run with the finalized takes' URLs and nothing else changes), or upscale the assembled episode with `upscale_video`, which has no preflight: say so, quote the finalize route, and name the window the catalog gives for finalizing a draft. Neither is in the estimate.
