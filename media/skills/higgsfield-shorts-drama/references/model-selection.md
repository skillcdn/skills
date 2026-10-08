# Model selection and credit estimate

Nothing is generated before the user accepts the model and the estimate. The video model is discovered at run time, never pinned, and the user sees the candidates' totals side by side. The mechanics every Higgsfield skill shares (reading the catalog, the lowest tier, the preflight and what it may answer instead of a number, `use_unlim`, one job per call, refused and failed jobs, a higher resolution later) are in [/docs/higgsfield/models.md](/docs/higgsfield/models.md); this page is what the episode adds.

## What the episode needs from a video model

| Needs | Why |
|---|---|
| Several reference images in one call, and a start frame | The portraits of every character in the cut keep the cast the same across many cuts; the approved first frame fixes the composition. A model that takes only references, or only a start frame, is a fallback, and the plan says what it loses. A role list is not proof that the two roles combine in one call: the preflight accepts what the generation may refuse, and the first cut is the test (the shared page has the case). |
| Native dialogue audio with lip sync | The model speaks every line; there is no text-to-speech. |
| 9:16 | Vertical platforms. |
| Durations that cover 7 to 12 seconds | The cut lengths of the table. A model with fixed options takes the nearest allowed length, and the table is written to them. |
| A lowest tier: the lowest resolution, the lowest quality mode, or a draft flag | Cost. Drafts are what the user pays for; an accepted take can be finalized or upscaled later as a separate, quoted step. |

## Finding the candidates

```
models_explore  action: recommend  type: video  query: several reference images of characters and a set in one call, start frame, native dialogue audio with lip sync, 9:16, 7 to 12 second clips, lowest resolution tier
models_explore  action: search  type: video  query: <each family the recommendation named>
```

The recommendation returns only part of the catalog, so also page through `action: list` with `type: video` and keep every model that meets the table above, reading `medias[].roles` (a reference role such as `image_references`, and `start_image`), the audio parameter, `aspect_ratios` and the duration range. Within a family keep the latest general model, as the shared page says, and read each candidate's parameters with `action: get`. Two or three candidates is usual; one is enough; none means the skill cannot run as written, and the user is told what is missing.

## Tier and audio

The lowest tier the shared page's table gives, every parameter at its lowest, a draft flag where there is one with its finalize price on its own line of the delivery. Audio stays on for every cut; a cut without a line still carries its sound.

## Preflight

Once per candidate and distinct duration of the cut table, with the exact parameters a cut will use: the model, the tier, `9:16`, the duration, audio on, `use_unlim` explicit, and a reference media id where the model's reference mode needs one even to quote (any image the account holds, or the placeholder the shared page describes). Once per image model and setting ([cast.md](cast.md)): the portrait model for one portrait per character and look, the reference-capable model for one set per place and one frame per cut.

## The estimate

```
Model        Tier    Takes (per cut)                 Images                               Reserve                        Total
<candidate>  <low>   8, 10, 12, ... = <n> s = <c>     <p> portraits, <s> sets, <f> frames  +<r> takes, +<p+s> img, +<f/3>  <t>
<candidate>  <low>   ...                             ...                                  ...                            <t>
Balance: <credits> · Finalize at <res>: <price> per take, optional, not in the total · Free-trial unlimited generations: <available or not>
```

The shape is illustrative; present only numbers that came back from `get_cost` in this run. The reserve is one take per three cuts (rounded up) priced at the longest cuts, one retry per portrait and per set, one frame per three cuts; it is the whole retry budget, images included, and beyond it every retry needs consent. Read `balance` before presenting; when the total exceeds it, say so and offer a shorter episode or fewer cuts before anything else.

The user sees, in plain words: the recommended model with its total including the reserve and the reason in a line; the other candidate's total; the balance; the finalize price as a separate, optional line; free-trial unlimited generations where the catalog offers them, set as the shared page says; and the **fallback**: what happens when the first cut shows the recommended model refusing the frame with the references, or speaking the dialogue language badly (a model the notes have never heard speak it is on trial in its first cut). The fallback is the next candidate at its quoted total, or the same model with the frame as reference image 1; when the user's word covered it, the switch happens without a second stop, and the images already made are kept; otherwise it is re-quoted. Recommend by these, in order: the model that takes both references and a start frame; a record in the dialogue language; the lower total; the durations the table needs. One word proceeds; the user may pick the other candidate or change the plan, which is preflighted again.

## Refused and failed jobs

A job the server refuses or that fails without a result is not a take and not the cut's retry: fix what it names and submit again, as the shared page says. After two refusals of one cut, stop and show the user the shot with what was refused. On a transport timeout the job may still have been submitted: read `show_generations` before submitting again, and `transactions` when a charge is in doubt.

## After the episode: a higher resolution

The episode is delivered at the draft tier. The finalize of the accepted takes is quoted at the delivery and an upscale of the episode is offered without a quote, as the shared page says; neither is in the estimate. A finalize re-runs the assembly script with the finalized takes' URLs ([editing.md](editing.md)) and nothing else changes.
