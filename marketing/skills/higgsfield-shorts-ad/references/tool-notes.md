# Tool notes

How the Higgsfield tools behaved in real runs of this skill, with the workaround that worked, for what is this skill's own: the reference's analysis, the product's pages, pickups, the captions of a master. What holds for every Higgsfield skill (the sandbox, the preflight and the presets, the models and what they accepted or refused, the decoders, the sounds of a language) is in the repository's shared pages under [/docs/higgsfield/](/docs/higgsfield/README.md), dated there; read those before phase 2. Each note is dated; when a tool behaves differently from what a note says, trust the tool and update the note. Nothing here changes the rules in SKILL.md.

## Scene analysis (`video_analysis_create`, `video_analysis_status`)

- 2026-09-23: a 27-second reference imported from a direct link stayed `queued`, with an unchanged `updated_at`, through eight polls over fifteen minutes and never completed or failed. The brief was built from the frames and the Whisper transcript instead, as the template allows. Do not let this block phase 2.
- 2026-09-23, second run: the same with a 38-second animated reference; still queued after 80 minutes.
- 2026-09-30, third and fourth runs: queued for the whole run again, twice. Four runs out of four; do not wait for it.

## The reference and the product's pages

- 2026-09-23: the sandbox's own curl of the product page returned the whole page text, so a separate web-reading tool was not needed for the words; it is still useful when a page is script-rendered.
- 2026-09-23, second run: a 38-second reference fit one `tile=6x7` sheet; the frames zipped and uploaded as a general file could be downloaded and viewed on the client.
- 2026-10-02, sixth run (the reference found with the research skill): the library's video address fed the sandbox pass as it was, minutes after it was read.
- 2026-10-02, seventh run (a product named without a link and no reference; a presenter talking to camera over the product's own screens): the research and the plan took twelve minutes and the production twenty-six. The site's pages were captured in the sandbox with Playwright at a phone's width in the ad's language and cropped into panels; the ad was composed on a 1080x1920 canvas so their text read, with the 480p takes scaled into it full-frame and as a round inset.

## Takes and pickups

- 2026-09-30, third run: a 25-second voice-over take prompted as "unhurried and hushed, slow weighty delivery" spoke eight lines at about 5 syllables per second with pauses up to 1.5 seconds, against the reference's 7 per second and no pause over half a second; the ad dragged even after the pauses were cut in code. The pace is now measured and written into the prompt in numbers ([story.md](story.md)), and a voice take is sized to the speech, not the ad. The voice-over's picture (hands at work, no face) was cut under the other shots with the narration as the spine, which worked.
- 2026-10-02, sixth run (a monologue in jump cuts): two takes of 19 and 18 seconds, seven lines each. One word of the second was wrong; a 4-second pickup of that line alone cost 12 credits against 54 for the take and cut in as one more jump cut, its framing and light a little off the take around it.
- 2026-10-02, seventh run: two takes of 22 and 18 seconds. One 10-second pickup held two lines from different places of the first take, a second of silence between them, and was cut in at both.

## Captions on the master

- 2026-09-23: on the mixed master, Whisper's default voice-detection split of two seconds pushed word starts back into pauses and onto a chime, so five of seven cues failed the onset check; a 300-millisecond split plus onset snapping and cut clamping passed all seven ([captions.md](captions.md)).
- 2026-09-23: an SRT cannot be uploaded (the backend's whitelist), so the cue text travels in the delivery.
