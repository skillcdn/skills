# Tool notes

How the Higgsfield tools behave in what is this skill's own: the reference's analysis, the product's pages, pickups, the captions of a master. What holds for every Higgsfield skill (the sandbox, the preflight and the presets, the models and what they accept or refuse, the decoders, the sounds of a language) is in the repository's shared pages under [/docs/higgsfield/](/docs/higgsfield/README.md); read those before the first sandbox call of phase 1. When a tool behaves differently from what a sentence here says, trust the tool and change the sentence. Nothing here changes the rules in SKILL.md.

## Scene analysis

`video_analysis_create` takes a video uploaded through `media_upload` or a YouTube link, names no cost, and says it typically finishes in three to five minutes (its description, checked 2026-10). For a reference imported from a direct link it has never finished for this skill: `queued`, with an unchanged `updated_at`, through polls over an hour and more, in every run so far (four of four; 27- and 38-second references, live action and animated). Start it only for an upload or a YouTube link, never wait for it, build the brief from the frames and the Whisper transcript as the template allows, and poll it between later phases in case it arrives.

## The reference and the product's pages

- The sandbox's own curl of the product page returns the whole page text, so a separate web-reading tool is not needed for the words; it is still useful when a page is script-rendered.
- A reference found with the research skill feeds the sandbox pass by its library address as it is, minutes after it was read.
- A reference of 38 seconds fits one `tile=6x7` sheet; frames zipped and uploaded as a general file can be downloaded and viewed on the client where `image_paths` is not at hand.
- An ad that shows the product's screens: the site's pages are captured in the sandbox with Playwright at a phone's width in the ad's language and cropped into panels; the ad is composed on a 1080x1920 canvas so their text reads, with the 480p takes scaled into it full-frame and as a round inset.

## Takes and pickups

- A voice-over take sized to the ad and prompted by mood drags: a 25-second take asked for "unhurried and hushed, slow weighty delivery" spoke eight lines at about 5 syllables per second with pauses up to 1.5 seconds, against the reference's 7 per second and no pause over half a second, and the ad dragged even after the pauses were cut in code. The pace is measured and written into the prompt in numbers ([story.md](story.md)), and a voice take is sized to the speech, not the ad. The voice-over's picture (hands at work, no face) cut under the other shots, with the narration as the spine, works.
- A pickup of one line costs its seconds, not the take's: a 4-second pickup cost 12 credits against 54 for its 18-second take, and cut in as one more jump cut, its framing and light a little off the take around it. A 10-second pickup held two lines from different places of the first take, a second of silence between them, and was cut in at both.
- A monologue in jump cuts, or a presenter over the product's screens, is two takes of about 20 seconds with seven lines each. From the research to the delivery such a run takes about forty minutes: twelve for the research and the plan, twenty-six for the production.
- A preflight with the same media as `start_image` and in `image_references` was priced, not refused (Seedance 2.5, checked 2026-10); the first take is still the test, as the shared models page says.
- A split layout (a screen above, a reaction below) is composed on the 9:16 canvas from a 16:9 reaction take; the frame and the take share that aspect, and the plan says so.

## Captions on the master

- On a mixed master, Whisper's default voice-detection split of two seconds pushes word starts back into pauses and onto a chime (five of seven cues failed the onset check); a 300-millisecond split plus onset snapping and cut clamping passes them all ([captions.md](captions.md)).
- An SRT cannot be uploaded (the backend's whitelist), so the cue text travels in the delivery.
