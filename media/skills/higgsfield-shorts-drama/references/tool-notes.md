# Tool notes

How the Higgsfield tools behaved in real runs of this skill, with the workaround that worked. Each note is dated; when a tool behaves differently, trust the tool and update the note. Nothing here changes the rules in SKILL.md.

## Sandbox (`sandbox_exec`)

The sandbox is discarded about ten seconds after a foreground call finishes, and a background job holds it for a fifteen-minute lease that short poll calls do not shorten (the tool's own description, read 2026-10-08). Two consequences:

- Run every review as a background job and poll it with short calls (a sleep of at most 25 seconds and `timeout_seconds` of at most 45; longer polls time out at the transport). A review started within the lease of the previous one finds the speech models cached; one started later downloads them again, which the log shows, and still fits inside the next cut's render time. Start the first warm-up (the model download, the fonts) as a background job while the first take renders.
- A long poll loop inside one foreground call came back as "the connector's server isn't responding" while the job kept running (2026-10-06); a short command afterwards read its output. Long work is `background: true`.

- 2026-10-02: `faster_whisper` models up to the largest ran in the sandbox on the CPU; the first load took about a minute. Loudness normalization before decoding raised a whispered line from undetected to clear.
- 2026-10-02: voice activity detection on missed a whispered line entirely and, in another take, invented a stock phrase over wind; the review runs with detection off and uses word probabilities and the no-speech probability instead.
- 2026-10-02: the assembly script was uploaded with `media_upload` as a general file (a `.py` filename, octet-stream content type) and got a permanent hosted URL; the sandbox fetched it with curl and ran it with environment overrides for replaced takes. A command is at most 16,000 characters and a presigned URL about 2 KB, so URLs are written into a file in one call and read by the script in the next. Presigned upload URLs are signed with the content type the result names and expire in a day.
- 2026-10-02: fonts under the Open Font License fetched from the google/fonts repository into a `fonts` directory and passed with `fontsdir` rendered the script needed; a missing font showed as empty subtitles, not as an error.
- 2026-10-06: ffmpeg's `subtitles` filter with ASS styles rendered name cards, role lines and term cards as positioned events; no separate drawtext pass was needed.

## Video generation (`generate_video`)

- 2026-10-02: the reference mode of the current Seedance model took up to eleven reference images per call, labeled in the prompt; a `medias` entry sent with the role `image` was coerced to the reference role and accepted. Read the current role names from `models_explore` each run; the catalog read on 2026-10-08 listed `start_image` and `image_references` side by side, so a first frame and the portraits go in one call.
- 2026-10-02: at the lowest tier the cost was per second of output; a 12-second cut cost three times a 4-second one. Read the number with `get_cost: true` per distinct duration. An episode of about 165 generated seconds came in near five hundred credits plus retries (illustrative; the preflight of the run is the number).
- 2026-10-02: a 12-second cut rendered in four to five minutes; `jobs_wait` with 15-second polls finished reliably. A cut is never started before the previous review is done.
- 2026-10-02 and 2026-10-06: prompts that mentioned darkness, a red thread, the sea or water returned a preset recommendation instead of a job. The answer carries the preset id; the same call with that id in `declined_preset_id` ran. Three different presets did this in one series; the id is read from the answer each time.
- 2026-10-02: a line typed into the prompt as Unicode escapes lost a final consonant; lines are written in the language's own script directly.
- 2026-10-02: a present-day cut rendered a character with the hair color of their other-period portrait. The continuity clause in capitals at the top of the prompt fixed it; one portrait per look, with only the look's portrait among the cut's references, keeps it from happening.

## Media

- 2026-10-02: hosted take URLs stayed valid across days; the assembly script fetched by URL rather than by media id, so a re-run needed no new downloads from the client.
- 2026-10-06: `media_confirm` after the PUT was needed before the result appeared in the library; the confirmed id went into the log.
