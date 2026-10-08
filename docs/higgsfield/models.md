# Models, tiers and credits

How a Higgsfield skill finds the models it needs in the catalog at run time, locks the lowest tier, quotes every credit before spending it, and handles what the server answers instead of a job. A skill says what its models must do, how it sizes its reserve and how it recommends among candidates; this page is the mechanics every skill shares. Nothing is pinned: a model is named here only as the one a fact was seen on, with the month it was checked.

## Finding models

`models_explore` is the catalog. Three ways in, used together:

- `action: recommend` with `type` and a query in words of what the model must take and produce. It returns part of the catalog, not all of it: it has left out the cheapest candidate that met a skill's needs.
- `action: search` with a family name (`kling`, `seedance`, `wan`) for every model of that family.
- `action: list` with `type`, paged, when a skill must see every candidate.

Within a family keep the latest general model: the highest generation number, a text-to-video or image-to-video model, not a turbo, edit, extension or legacy variant and not a product wrapper around one. Then read its parameters with `action: get`: `medias[].roles` (a start-frame role such as `start_image`, a reference role such as `image_references`), the audio parameter, `aspect_ratios`, the duration range or options, and how quality is selected. `get` may return nothing beyond what `search` carried; read the roles from whichever answer has them, each run.

Roles seen so far (checked 2026-10): Seedance 2.5 takes `image_references`, up to eleven labeled in the prompt, and folds a `start_image` sent with them into that list as its first entry, while the take still opens on the frame's composition (read the echoed parameters of the first take, and number the portraits from 2 in every mapping when the frame is reference image 1); a `medias` entry sent with the role `image` is coerced to the reference role. Kling 3.0 exposes `start_image` and `end_image` only, no identity role. Wan 3.0 lists `start_image` and `image_references` and refuses them together.

**A role list is not proof that two roles combine in one call.** The preflight accepts what the generation may refuse: a model has priced a preflight with a start frame and reference images and refused the generation with 422 ("start_image/end_image cannot be combined with reference media"), without charge. The first real take is the test, and a skill names its fallback at the cost checkpoint.

## Lowest tier

| The model exposes | Lock |
|---|---|
| A `resolution` parameter | Its lowest option (`480p` where it exists). |
| A quality `mode` | Its lowest option (`std`). |
| A draft flag that makes a lower-resolution take finalizable later | The draft flag; the finalize price the preflight names goes to the delivery. |
| Several of these | All of them at their lowest. |
| None | The default; say so in the estimate. |

Never a higher tier for drafts, however small the difference looks; a higher resolution is a separate step after the delivery (below). A 1k image is more than a video model needs. Audio stays on for every take with a line or a sound tied to an action. Turning it off is cheaper on some models and changes nothing on others (cheaper on Kling 3.0, a flat per-second price on Seedance 2.5, checked 2026-09), and a take generated with audio off has no audio stream at all, not a silent one ([`sandbox.md`](sandbox.md)).

## Preflight

Every spend is quoted first: `generate_video` or `generate_image` with `get_cost: true` and the exact parameters the job will use. Nothing is submitted or charged. The cost depends on the model, the duration, the tier and the audio flag, not on the prompt or on which media is attached (identical image preflights return identical numbers), so preflight once per distinct parameter set and reuse the number. Present only numbers that came back in this run; the table at the end of this page only shows the shape.

```
generate_video  params: { model: <id>, prompt: <prompt>, duration: <s>, aspect_ratio: "9:16", <tier parameters>, use_unlim: false, get_cost: true }
```

A model whose reference mode needs an image input even to quote is preflighted with any image media id the account holds; the number does not depend on which. When none is at hand, or `show_medias` fails (it has answered with an output-schema error), a tiny grey PNG made in the sandbox with ImageMagick, uploaded with `media_upload` and confirmed, serves at no cost.

Images are preflighted the same way with `generate_image`, once per image model and setting; it has not returned preset notices. An image preflight may round (`credits: 1` with `credits_exact: 0.12`): the estimate uses the rounded figure, the ledger what the transaction shows.

Read `balance` before presenting an estimate. A balance that falls during a preflight-only phase is another session's spending on the same account: check `transactions` before blaming a preflight, and say so to the user in one line.

## Presets

A preflight or a generation may answer with a preset recommendation instead of a number or a job. Read the preset id from the answer and call again with it in `declined_preset_id`; pass the same field on the real generation. Skills use no presets and do not put the notice to the user. Words such as "night" or "dark", a color, water or the sea in the prompt trigger it; near-identical prompts do not all trigger it, and several different presets can come back in one run. When the same id has come back on every call of a run so far, send it from the start on the next call (it is accepted without a notice) and read a new id from the answer when another comes.

## Free-trial unlimited generations

If the catalog reports that the account can spend free-trial unlimited generations on a model, say so in the estimate. `use_unlim: true` only when the user explicitly asks for it; never add it to save credits on their behalf, and never drop it once they asked. Set `use_unlim` explicitly on every generation call, `false` unless the user asked: left out, the server may withhold the job and return a question (`unlim_choice`) instead of a take. If that happens anyway, put the question to the user once and call again with their answer. A rejected unlimited request comes back as an error, never as a silent charge.

## One job per call

One generation per call, `count` 1, never the batch tools: the review of one take must be able to stop a fault before the next take repeats it. Image jobs that nothing depends on reviewing one by one (the portraits, a set of first frames) may be sent together and collected in one round.

`jobs_wait` takes the job ids of `generate_image` or `generate_video`, one or several (the tool text's mention of batch ids is not a restriction), and is capped at about 15 seconds per wait. It may report a take as in progress for minutes after its file and its charge exist, and list video jobs with type `image`; prepare the next step during the wait rather than polling faster. A take is charged at submission, and every charge has equalled its preflight.

Write dialogue in the language's own script, directly: a line typed as Unicode escapes lost a final consonant.

## Refused and failed jobs

A job the server refuses (moderation, an invalid parameter, two roles that do not combine) or that fails without a result is not a take and not a retry: fix what it names (a fight described by its sound and the reaction on a face rather than the blow; a parameter read again from the catalog; the fallback model named at the cost checkpoint) and submit again. Check `transactions` when a charge is in doubt; a charge for a job that gave nothing is a ledger row with its reason and counts against the accepted estimate. After two refusals of one shot, stop and show the user the shot with what was refused. On a transport timeout the job may still have been submitted: read `show_generations` before submitting again.

## A higher resolution

Drafts are what the user pays for. Two ways up, each a separate step after the delivery, started only on the user's word, neither in the estimate:

- **Finalize.** A model with a draft flag re-renders an accepted take at the resolution the catalog names, within a window after the draft; the draft's preflight names the price and the window (Seedance 2.5: 1080p at 12 credits per second of take, within seven days, checked 2026-10). The assembly is re-run with the finalized takes' URLs and nothing else changes. This is the route that can be quoted.
- **Upscale.** `upscale_video` enhances the assembled video with an upscaling model, not a re-render: provider `bytedance` (presets by content type, 1080p, 2K or 4K, 24, 30 or 60 fps, the source width and height required, fps above 30 doubling the cost) or `topaz` (1080p or 2160p, by aspect ratio) (tool description, checked 2026-10). It costs credits and takes no `get_cost`, so it cannot be quoted: say so, quote the finalize route instead, and start an upscale only when the user accepts a spend the tool will not price first; the ledger then records what `transactions` shows.

## Prices and times seen

Illustrative: the preflight of the run is the number. A take is priced by the second, so a pickup of one line costs its seconds, not the take's.

| Model and setting | Price | Render time | Checked |
|---|---|---|---|
| Seedance 2.5, 480p draft, audio on | 3 credits per second of take; the finalize at 1080p 12 per second, within seven days | A 10- or 12-second take in two to five minutes; a 4-second take in about three and a half | 2026-10 |
| Kling 3.0, std, sound on | 2 credits per second | | 2026-09 |
| The reference-capable image model (Nano Banana Pro) at its lowest setting, 9:16 or 3:4 | 0.25 per image, with or without a reference input | | 2026-09 |
| The identity portrait model (Soul Cast) | 0.12 per portrait, shown as a rounded 1 by the preflight | | 2026-09 |
