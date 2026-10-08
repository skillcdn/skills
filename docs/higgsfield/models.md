# Models, tiers and credits

How a Higgsfield skill finds the models it needs in the catalog at run time, locks the lowest tier, quotes every credit before spending it, and handles what the server answers instead of a job. A skill says what its models must do, how it sizes its reserve and how it recommends among candidates; this page is the mechanics every skill shares, with what the tools did in real runs, dated. A model id appears here only in a dated note; nothing is pinned.

## Finding models

`models_explore` is the catalog. Three ways in, used together:

- `action: recommend` with `type` and a query in words: what the model must take and produce. It returns part of the catalog, not all of it (on 2026-10-08 it left out the cheapest candidate for a drama's needs).
- `action: search` with a family name (`kling`, `seedance`, `wan`) for every model of that family.
- `action: list` with `type`, paged, when a skill must see every candidate.

Within a family keep the latest general model: the highest generation number, a text-to-video or image-to-video model, not a turbo, edit, extension or legacy variant and not a product wrapper around one. Then read its parameters with `action: get`: `medias[].roles` (a start-frame role such as `start_image`, a reference role such as `image_references`), the audio parameter, `aspect_ratios`, the duration range or options, and how quality is selected. `get` has returned nothing beyond what `search` carried (2026-09-23); read the roles from whichever answer has them, each run.

A role list is not proof that two roles combine in one call. The preflight accepts what the generation may refuse: on 2026-10-08 a model listed `start_image` and `image_references`, priced a preflight with both, and refused the generation with 422 ("start_image/end_image cannot be combined with reference media"), without charge. The first real take is the test, and a skill names its fallback at the cost checkpoint.

## Lowest tier

| The model exposes | Lock |
|---|---|
| A `resolution` parameter | Its lowest option (`480p` where it exists). |
| A quality `mode` | Its lowest option (`std`). |
| A draft flag that makes a lower-resolution take finalizable later | The draft flag; the finalize price the preflight names goes to the delivery. |
| Several of these | All of them at their lowest. |
| None | The default; say so in the estimate. |

Never a higher tier for drafts, however small the difference looks; a higher resolution is a separate step after the delivery ("A higher resolution" below). A 1k image is more than a video model needs. Audio stays on for every take with a line or a sound tied to an action; turning it off is cheaper on some models and changes nothing on others (2026-09-23: cheaper on one family, a flat per-second price on the other), and a take generated with audio off has no audio stream at all, not a silent one ([`sandbox.md`](sandbox.md)).

## Preflight

Every spend is quoted first: `generate_video` or `generate_image` with `get_cost: true` and the exact parameters the job will use. Nothing is submitted or charged. The cost depends on the model, the duration, the tier and the audio flag, not on the prompt or on which media is attached (seven identical image preflights returned identical numbers, 2026-09-23), so preflight once per distinct parameter set and reuse the number. Prices have been flat per second so far; present only numbers that came back in this run.

```
generate_video  params: { model: <id>, prompt: <prompt>, duration: <s>, aspect_ratio: "9:16", <tier parameters>, use_unlim: false, get_cost: true }
```

What a preflight may answer instead of a number:

- **A preset recommendation.** Read the preset id from the answer and call again with it in `declined_preset_id`; pass the same field on the real generation. Skills use no presets and do not put the notice to the user. Words such as "night" or "dark", a color, water or the sea in the prompt trigger it, and three different presets did in one series (2026-10-02, 2026-10-06); near-identical prompts do not all trigger it. When the same id has come back on every call of a run so far, send it from the start on the next call, which saves a round trip (accepted without a notice, 2026-10-08), and read a new id from the answer when another comes.
- **A refusal of a reference mode without a reference.** A model whose reference mode needs an image input even to quote is preflighted with any image media id the account holds; the number does not depend on which. When none is at hand, or `show_medias` fails (an output-schema error, 2026-10-08), a tiny grey PNG made in the sandbox with ImageMagick, uploaded with `media_upload` and confirmed, serves at no cost.

Images are preflighted the same way with `generate_image`, once per image model and setting; it has not returned preset notices (2026-09-23). An image preflight may round (`credits: 1` with `credits_exact: 0.12`): the estimate uses the rounded figure, the ledger what the transaction shows.

Read `balance` before presenting an estimate. A balance that fell during a preflight-only phase was another session's spending on the same account (2026-09-23): check `transactions` before blaming a preflight, and say so to the user in one line.

## Free-trial unlimited generations

If the catalog reports that the account can spend free-trial unlimited generations on a model, say so in the estimate. `use_unlim: true` only when the user explicitly asks for it; never add it to save credits on their behalf, and never drop it once they asked. Set `use_unlim` explicitly on every generation call, `false` unless the user asked: left out, the server may withhold the job and return a question (`unlim_choice`) instead of a take. If that happens anyway, put the question to the user once and call again with their answer. A rejected unlimited request comes back as an error, never as a silent charge.

## One job per call

One generation per call, `count` 1, never the batch tools: the review of one take must be able to stop a fault before the next take repeats it. Image jobs that nothing depends on reviewing one by one (the portraits, a set of first frames) may be sent together and collected with one `jobs_wait`.

`jobs_wait` takes the job ids of `generate_image` or `generate_video`, one or several (the tool text's mention of batch ids is not a restriction), and is capped at about 15 seconds per wait. It has reported a take as in progress for three to ten minutes after its file and its charge existed, and listed video jobs with type `image` (2026-09-23); a five-shot run polled about 75 times. Prepare the next step during the wait rather than polling faster. A take is charged at submission, and every charge has equalled its preflight.

## Refused and failed jobs

A job the server refuses (moderation, an invalid parameter, two roles that do not combine) or that fails without a result is not a take and not a retry: fix what it names (a fight described by its sound and the reaction on a face rather than the blow; a parameter read again from the catalog; the fallback model named at the cost checkpoint) and submit again. Check `transactions` when a charge is in doubt; a charge for a job that gave nothing is a ledger row with its reason and counts against the accepted estimate. After two refusals of one shot, stop and show the user the shot with what was refused. On a transport timeout the job may still have been submitted: read `show_generations` before submitting again.

## A higher resolution

Drafts are what the user pays for. Two ways up, each quoted at the delivery and started only on the user's word, neither in the estimate: finalize each accepted take at the resolution the catalog names (a draft flag's preflight names the price per take and the window, seven days on 2026-09-30 and on 2026-10-08; the assembly is re-run with the finalized takes' URLs and nothing else changes), or upscale the assembled video with `upscale_video`, which takes no `get_cost`: say so, quote the finalize route instead, and name the window the catalog gives for finalizing a draft.

## Dated notes

- 2026-09-23: six of ten video preflights returned a preset recommendation and no cost; twelve in the next run returned none. Seedance 2.5 at 480p with audio cost 3 credits per second at 4, 5, 6, 8 and 10 seconds; Kling 3.0 std with sound 2 per second; the reference-capable image model 0.25 per image at its lowest setting in 9:16 and 3:4, with or without a reference input, and the other candidate 2. Kling 3.0 exposed `start_image` and `end_image` only, no identity role; Seedance 2.5 exposed `image_references`. A 4-second take at 480p rendered in about three and a half minutes, a 10-second one in five to eight.
- 2026-09-30: `draft: true` on Seedance 2.5 was the cheapest setting (75 credits for 25 seconds with audio) and left the take finalizable at 1080p for seven days at 60 credits; the preflight named both. The same preset recommendation returned on every video call and was declined each time.
- 2026-10-02: the reference mode of the current Seedance model took up to eleven reference images per call, labeled in the prompt; a `medias` entry sent with the role `image` was coerced to the reference role and accepted. At the lowest tier the cost was per second of output: a 12-second cut cost three times a 4-second one. A 12-second cut rendered in four to five minutes; two takes of 19 and 18 seconds rendered in two to three minutes each, and a 4-second pickup cost 12 credits against 54 for its take.
- 2026-10-02: a line typed into the prompt as Unicode escapes lost a final consonant; lines are written in the language's own script directly.
- 2026-10-08: Wan 3.0 refused `start_image` with `image_references` (422, not charged) after a clean preflight. Seedance 2.5 accepted the frame as `start_image` with three portraits as `image_references`, but its echoed parameters showed the frame folded into the reference list as its first entry and no start frame, while the takes still opened on the frame's composition: read the echo of the first take, and number the portraits from 2 in every mapping when the frame is reference image 1.
- 2026-10-08: eight Seedance 2.5 takes at 480p draft with audio cost 3 credits per second (30 for 10 seconds, 36 for 12), charged at submission; a 12-second take rendered in two to three minutes; the finalize at 1080p was priced at 12 credits per second, open for seven days.
