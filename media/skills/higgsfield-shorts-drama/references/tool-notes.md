# Tool notes

How the Higgsfield tools behaved in real runs of this skill, with the workaround that worked. Each note is dated; when a tool behaves differently, trust the tool and update the note. Nothing here changes the rules in SKILL.md.

## Sandbox (`sandbox_exec`)

The sandbox is discarded about ten seconds after a foreground call finishes, and a background job holds it for a fifteen-minute lease that short poll calls do not shorten (the tool's own description, read 2026-10-08). Two consequences:

- Run every review as a background job and poll it with short calls (a sleep of at most 25 seconds and `timeout_seconds` of at most 45; longer polls time out at the transport). A review started within the lease of the previous one finds the speech models cached; one started later downloads them again, which the log shows, and still fits inside the next cut's render time. Start the first warm-up (the model download, the fonts) as a background job while the first take renders.
- A long poll loop inside one foreground call came back as "the connector's server isn't responding" while the job kept running (2026-10-06); a short command afterwards read its output. Long work is `background: true`.
- A short foreground call with `image_paths` returns up to four PNG or JPEG files (512 KiB in all) to the agent as images (the tool's own description, read 2026-10-08). Contact sheets are looked at this way, within the lease of the job that made them, or after they are made again from the take.

- 2026-10-08: the review ran three plain Whisper sizes (small, medium, large-v3) and one prompted decode per take, each review as a background job. The medium model did not decode a whispered line at all while small and large-v3 did; a forced laugh right before a line dropped every decode's word probabilities under 0.1 while a 100-millisecond envelope showed the speech plainly. Fonts fetched from the google/fonts repository rendered Korean subtitles, name cards and the inner-voice style through the `subtitles` filter; `aformat=channel_layouts=stereo` was needed on both sides of `loudnorm`.
- 2026-10-02: `faster_whisper` models up to the largest ran in the sandbox on the CPU; the first load took about a minute. Loudness normalization before decoding raised a whispered line from undetected to clear.
- 2026-10-02: voice activity detection on missed a whispered line entirely and, in another take, invented a stock phrase over wind; the review runs with detection off and uses word probabilities and the no-speech probability instead.
- 2026-10-02: the assembly script was uploaded with `media_upload` as a general file (a `.py` filename, octet-stream content type) and got a permanent hosted URL; the sandbox fetched it with curl and ran it with environment overrides for replaced takes. A command is at most 16,000 characters and a presigned URL about 2 KB, so URLs are written into a file by the command that starts the script in the background, or in a call made back to back with the next (files survive between back-to-back calls). Presigned upload URLs are signed with the content type the result names and expire in a day.
- 2026-10-02: fonts under the Open Font License fetched from the google/fonts repository into a `fonts` directory and passed with `fontsdir` rendered the script needed; a missing font showed as empty subtitles, not as an error.
- 2026-10-06: ffmpeg's `subtitles` filter with ASS styles rendered name cards, role lines and term cards as positioned events; no separate drawtext pass was needed.

## Video generation (`generate_video`)

- 2026-10-08, first production run (six cuts of 10 and 12 seconds, Korean): Wan 3.0 listed `start_image` and `image_references` among its roles and priced a preflight with both, but the generation returned 422 ("start_image/end_image cannot be combined with reference media"); not charged. A role list does not prove that two roles combine in one call; only a generation does. The run switched to Seedance 2.5 and re-quoted.
- 2026-10-08: Seedance 2.5 accepted the frame as `start_image` with three portraits as `image_references`, but the echoed parameters showed the frame folded into the reference list as its first entry and no start frame; the takes still opened on the frame's composition. Read the echo of the first take: when the frame is reference image 1, the portraits are numbered from 2 in every mapping ([prompting.md](prompting.md)).
- 2026-10-08: the same preset recommendation (one id, triggered by "night" and "dark" in the prompt) came back on the first send of nearly every cut, on both models; sending that id in `declined_preset_id` from the start on a later cut was accepted without a notice.
- 2026-10-08: eight Seedance 2.5 takes at 480p draft with audio cost 3 credits per second (30 for 10 seconds, 36 for 12), charged at submission; a 12-second take rendered in two to three minutes, and the cut phase with its reviews took about 37 minutes for eight takes. Lines came up to a second earlier than their windows, which the edit absorbed. The draft's finalize at 1080p was priced at 12 credits per second and open for seven days; `upscale_video` takes no `get_cost`, so only the finalize route could be quoted.
- 2026-10-08: `show_medias` failed with an output-schema error; a plain grey PNG made in the sandbox with ImageMagick, uploaded with `media_upload` and confirmed, served as the preflight's reference placeholder at no cost.
- 2026-10-02: the reference mode of the current Seedance model took up to eleven reference images per call, labeled in the prompt; a `medias` entry sent with the role `image` was coerced to the reference role and accepted. Read the current role names from `models_explore` each run.
- 2026-10-02: at the lowest tier the cost was per second of output; a 12-second cut cost three times a 4-second one. Read the number with `get_cost: true` per distinct duration. An episode of about 165 generated seconds came in near five hundred credits plus retries (illustrative; the preflight of the run is the number).
- 2026-10-02: a 12-second cut rendered in four to five minutes; `jobs_wait` with 15-second polls finished reliably. A cut is never started before the previous review is done.
- 2026-10-02 and 2026-10-06: prompts that mentioned darkness, a red thread, the sea or water returned a preset recommendation instead of a job. The answer carries the preset id; the same call with that id in `declined_preset_id` ran. Three different presets did this in one series; the id is read from the answer each time.
- 2026-10-02: a line typed into the prompt as Unicode escapes lost a final consonant; lines are written in the language's own script directly.
- 2026-10-02: a present-day cut rendered a character with the hair color of their other-period portrait. The continuity clause in capitals at the top of the prompt fixed it; one portrait per look, with only the look's portrait among the cut's references, keeps it from happening.

## Media

- 2026-10-02: hosted take URLs stayed valid across days; the assembly script fetched by URL rather than by media id, so a re-run needed no new downloads from the client.
- 2026-10-06: `media_confirm` after the PUT was needed before the result appeared in the library; the confirmed id went into the log.
