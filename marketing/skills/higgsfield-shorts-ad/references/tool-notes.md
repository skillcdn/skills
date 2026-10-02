# Tool notes

How the Higgsfield tools behaved in real runs of this skill, with the workaround that worked. Each note is dated; when a tool behaves differently from what a note says, trust the tool and update the note. Nothing here changes the rules in SKILL.md; it saves the next run from rediscovering the same edges.

## Sandbox (`sandbox_exec`)

- 2026-09-23: a poll that slept 60 seconds with `timeout_seconds` 100 timed out at the transport ("The operation timed out") well under the tool's 120-second ceiling. Polls with a 20 to 25 second sleep and a timeout of 40 to 45 worked every time.
- 2026-09-23: the sandbox's ffmpeg rejects `tile=6x0`; both tile dimensions must be given. Because the analysis command is one `&&` chain, a failure there skips the transcript and the upload. The brief template uses `tile=6x6` and `sheet%02d.png`.
- 2026-09-23: a presigned upload URL from `media_upload` is signed with the content type. A PUT without `-H 'Content-Type: ...'` fails; the `media_upload` result names the header to send.
- 2026-09-23: the sandbox's own curl of the product page returned the whole page text, so a separate web-reading tool was not needed for the words; it is still useful when a page is script-rendered.
- 2026-09-23, second run: the whole analysis pass, Whisper download included, finished in about 40 seconds. A 38-second reference fit one `tile=6x7` sheet. Frames zipped and uploaded as a general file (`.zip`, `application/octet-stream`, `media_confirm` type `file`) could be downloaded and viewed on the client.

- 2026-09-30, third run (Claude Code, no upload widget): a local reference was uploaded from the agent's own shell, `media_upload` for the presigned URL, `curl -X PUT` with the named `Content-Type`, then `media_confirm`; the hosted URL served the sandbox pass. A `.wav` upload request came back as an `.mp3` slot, so the narration stem was uploaded as MP3. Whisper was not installed locally; the sandbox ran it.

- 2026-09-30, fourth run (an unattended Claude Code session with a tool allowlist): the PUT of a local reference to the presigned upload URL was refused by the harness (the URL carries a credential token, which needs a person's approval), so the sandbox pass could not run. Giving the run a hosted link to the reference instead (uploaded beforehand by whoever can approve) made everything work; the outputs are uploaded from the sandbox, which needs no local shell. In an unattended agent, ask for a link.

## Scene analysis (`video_analysis_create`, `video_analysis_status`)

- 2026-09-23: a 27-second reference imported from a direct link stayed `queued`, with an unchanged `updated_at`, through eight polls over fifteen minutes and never completed or failed. The brief was built from the frames and the Whisper transcript instead, as the template allows. Do not let this block phase 2.
- 2026-09-23, second run: the same with a 38-second animated reference; still queued after 80 minutes.
- 2026-09-30, third and fourth runs: queued for the whole run again, twice. Four runs out of four; do not wait for it.

## Preflight (`generate_video` and `generate_image` with `get_cost: true`)

- 2026-09-23: six of ten video preflights came back with a preset recommendation and no cost. Calling again with `declined_preset_id` set to the recommended preset returned the cost. Near-identical prompts did not all trigger it. Pass the same `declined_preset_id` on the real generation.
- 2026-09-23: cost did not depend on the prompt or on which reference media was attached, only on model, duration, tier and audio. Seven identical image preflights returned identical numbers; one per parameter set is enough.
- 2026-09-23: a reference-mode video model (Seedance 2.5 `omni_reference`) needs a media input even for a preflight; the product image's media id served as the placeholder.
- 2026-09-23: turning native audio off made Kling 3.0 cheaper and Seedance 2.5 not at all (a flat per-second price either way).
- 2026-09-23: an image model's preflight returned `credits: 1` with `credits_exact: 0.12`; the estimate used the rounded figure, and the ledger records what the transaction shows.
- 2026-09-23, second run: none of twelve video preflights returned a preset notice. Prices were flat per second (Seedance 2.5 480p with audio 3 per second at 4, 5, 6, 8 and 10 seconds; Kling 3.0 std with sound 2 per second); the reference-capable image model cost 0.25 per image at its lowest setting in 9:16 and 3:4, with or without a reference input, and the other candidate 2.
- 2026-09-23, second run: the balance fell by 96 during a preflight-only phase. `transactions` and `show_generations` showed four generations from another session on the same account minutes earlier. Check `transactions` before blaming a preflight, and say so to the user in one line.

## Models (`models_explore`)

- 2026-09-23: the identity-portrait recommendation (Soul Cast) produced only 16:9 and took no reference input, so first frames needed a second, reference-capable image model (Nano Banana Pro that day). cast.md now finds the two models separately.
- 2026-09-23: Soul Cast ignored the prompt's framing and returned a 2048x1152 three-panel character sheet (full body front, full body back, face) every time. It served as the identity reference as it was. Four portraits cost 0.12 credits each; the preflight had shown a rounded 1.
- 2026-09-23, second run: Kling 3.0 exposed `start_image` and `end_image` only, no identity role; Seedance 2.5 exposed `image_references`. `models_explore` with `get` returned nothing beyond what `search` had already carried.

## Jobs (`generate_image`, `generate_video`, `jobs_wait`)

- 2026-09-23: `jobs_wait` accepted a single job id from `generate_image` (not from a batch tool) and returned the result URL when the job finished, in two 15-second waits per portrait. The tool text's mention of batch job ids is not a restriction.
- 2026-09-23: `generate_image` never returned the preset notice that `generate_video` preflights did.
- 2026-09-23, second run: `jobs_wait` reported a take as in progress for three to ten minutes after its result file and its charge existed, and listed in-progress video jobs with type `image`; seven takes took about 45 polls. Prepare the next step during the wait rather than polling faster.

## Takes and assembly

- 2026-09-23: a 4-second Seedance 2.5 take at 480p rendered in about three and a half minutes, a 10-second one in five to eight; `jobs_wait` is capped at 15 seconds, so a five-shot run polled about 75 times. Every charge equalled its preflight.
- 2026-09-23: a take generated with `generate_audio: false` came back with no audio stream at all. The assembly synthesized room tone for it before the concat.
- 2026-09-23, second run: a Seedance 2.5 voice-over take started mid-word at frame 0 and lost its first consonant (묻는 was heard as 웃는); the retry, prompted for about half a second of silence before the line, came with a 0.47-second lead and the exact words.
- 2026-09-23, second run: a hosted media URL was cached by the CDN on its first fetch; an overwrite after that stayed invisible for about eight minutes and query strings did not bypass it, while an overwrite before the first fetch showed at once. Files in the sandbox survived back-to-back calls, which allowed a patch-and-rerun; presigned URLs of about 2.3 KB each made the 16,000-character command limit binding.
- 2026-09-23, second run: Nanum Myeongjo has no hanja (占, 絲); Noto Serif KR supplied those two glyphs. The subtitles filter needs the English family name, and Nanum Myeongjo's first name record is Korean.
- 2026-09-23: the assembly encode (29 seconds of video plus uploads) took about 50 seconds; run as a background script it finished cleanly, where a foreground call would have hit the transport timeout seen in phase 2. The sandbox had been recycled during the last take's wait, so the script re-fetched every input; a self-contained script is the safe shape.
- 2026-09-23: the bundled `subtitles` workflow spread cues across pauses, ships no Korean font, burns only white, caps or paper looks, forbids a hand-rolled burn and asks the user about the look; captions.md therefore burns with ffmpeg directly. An SRT cannot be uploaded (backend whitelist), so the cue text travels in the delivery.

- 2026-09-30, third run: a 25-second Seedance 2.5 voice-over take (480p, `draft: true`) prompted as "unhurried and hushed, slow weighty delivery" spoke eight lines at about 5 syllables per second with pauses up to 1.5 seconds, against the reference's 7 per second and no pause over half a second; the ad dragged even after the pauses were cut in code. The pace is now measured and written into the prompt in numbers ([story.md](story.md)), and a voice take is sized to the speech, not the ad. The voice-over's picture (a hand and a brush, no face) was cut under the other shots with the narration as the spine, which worked.
- 2026-09-30, third run: `draft: true` on Seedance 2.5 was the cheapest setting (75 credits for 25 seconds with audio, 3 per second) and left the take finalizable at 1080p for seven days at 60 credits each; the preflight names both. The same preset recommendation returned on every video call and was declined with `declined_preset_id` each time.

- 2026-10-02, sixth run (the reference found by the research skill in the Meta Ad Library, a 37-second monologue in jump cuts): the library's video address fed the sandbox pass as it was, minutes after it was read. Two Seedance 2.5 takes of 19 and 18 seconds, seven lines each, rendered in two to three minutes each. One word of the second was wrong; a 4-second pickup of that line alone cost 12 credits against 54 for the take and cut in as one more jump cut, its framing and light a little off the take around it. The assembly script was too long for one command with its upload URLs: it was written into the sandbox in one call, uploaded from there as a general file, and fetched by its hosted URL in the later calls. A second PUT to an upload URL that had already taken a file came back 412; a new reservation per revision, as the conventions say.

## Pronunciation outcomes

- 2026-09-23, Seedance 2.5, Korean: "적혔다" came out without its aspiration in two takes (Whisper wrote "적겼다" at about 0.85 both times, and that was the truth, not a homophone). Respelling it in the prompt as "저켰다" while the intended line stayed "적혔다" fixed it on the first retry: Whisper then wrote "적혔다" at 0.98, and the syllable's onset carried about 50 milliseconds of aspiration noise against 10 to 20 in the failed takes. A 10-second take with three lines took about four and a half minutes.

- 2026-09-30, Seedance 2.5, Korean: "스님" lost its final consonant in three places of one take (heard as "스니" by Whisper small and medium). Respelling in the prompt as "스니메" for "스님의" and "스니믄" for "스님은", with the intended line unchanged, fixed it on the first retry (0.99); the retry then blurred "발견됐다", which the first take had clean, so the edit took that sentence from the first take.

- 2026-09-30, Seedance 2.5, Korean, fourth run: a 23-second voice-over of 160 syllables prompted with the pace in numbers (about 7 per second, pauses under half a second, half a second of lead) came out at 7.27 per second with no pause over half a second, every syllable present. The first word, the persona's name "현묵", was the only doubtful one: sung too fast for its vowel to be certain, on both takes, and a retry that asked for the name to be said clearly changed nothing and blurred another word. A name is not the first word of a voice take.

- 2026-10-01, Seedance 2.5, Korean, fifth run: the hook's last word "까닭" came out as "가도" on the first voice take (the meaning of the hook gone). Respelled in the prompt as "까닥" (the standard pronunciation), it came out right on the retry, 23 seconds of 149 syllables at about 6.5 per second. The discarded take's picture still served as two inserts, at no cost.

- 2026-10-02, Seedance 2.5, Korean, sixth run: "권" in "사백여 권이야" lost its glide at about six syllables per second: heard as "간" in an 18-second take (small and medium, about 0.68), and as "건" in a 4-second pickup prompted with the respelling "사배겨 궈니야". The prompted decode read "권" at 0.41, so the machine check did not settle it and the delivery asked the user to listen.

## Speech-to-text (Whisper in the sandbox)

- 2026-09-23: on the mixed master, Whisper's default voice-detection split of two seconds pushed word starts back into pauses and onto a chime, so five of seven cues failed the onset check; a 300-millisecond split plus onset snapping and cut clamping passed all seven. Re-uploading a corrected file to the same presigned URL before `media_confirm` worked.

- 2026-09-23: Whisper normalized a dialect pronoun to the standard one and wrote a two-word tagline as one word in both takes of the same shot; the medium model did the same. The user heard the first take as unnatural; the retry, prompted with "natural standard pronunciation", was chosen after a 10-millisecond RMS envelope showed a slightly longer closure gap inside the disputed word and a decode with the intended line as `initial_prompt` read it as two words.
- 2026-09-23: on a sighing shot with no dialogue, Whisper with voice detection returned a low-confidence phrase on a stretch 13 dB under real speech, and without voice detection returned stock Korean phrases. Loudness and no-speech probability, not the transcript, settled it as silence.
- 2026-09-23, second run: on the reference, whose speech sat 13 to 20 dB above a piano bed, voice detection (the default split and a 300-millisecond one) returned two garbage fragments with impossible timestamps; a decode without it and with `language="ko"` recovered all twelve lines. The brief's pass now decodes the reference without voice detection; the takes keep it.

- 2026-09-23: Whisper `small` heard a Korean line as "니가 엄마 손재 기다린다" where the burned caption read "느그 엄마 손주 기다린다", and missed two on-screen lines that were never spoken. Frames are the ground truth for text; the transcript is the clock.
