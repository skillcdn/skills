# Tool notes

How the Higgsfield tools behave in what is this skill's own. What holds for every Higgsfield skill (the sandbox and its lease, the preflight and the presets, the models and what they accept or refuse, the decoders, the sounds of a language) is in the repository's shared pages under [/docs/higgsfield/](/docs/higgsfield/README.md); read those before phase 3. When a tool behaves differently from what a sentence here says, trust the tool and change the sentence. Nothing here changes the rules in SKILL.md.

## Cost and time of an episode

- An episode of about 165 generated seconds at the lowest tier comes in near five hundred credits plus retries (Seedance 2.5 at 3 credits per second of take, checked 2026-10; illustrative, the preflight of the run is the number). A 60-second episode of six cuts with two retries spent about 260.
- A 12-second cut renders in two to five minutes, and a cut is never started before the previous review is done, so the cut phase sets the length of the run: about 37 minutes for eight takes with their reviews.
- The same preset recommendation comes back on the first send of nearly every cut of a series; sending its id from the start on a later cut is accepted without a notice ([/docs/higgsfield/models.md](/docs/higgsfield/models.md) "Presets").

## Picture and timing

- A character with two looks renders with the other look's hair when both portraits are among a cut's references: one portrait per look, only the look's portrait in the cut, and the continuity clause in capitals at the top of the prompt when a take has missed it ([prompting.md](prompting.md)).
- Lines come up to a second earlier than their windows; the edit absorbs it, and the review's clock, not the window, times the subtitle.
- Name cards, role lines and term cards render as positioned ASS events through the `subtitles` filter, with no separate `drawtext` pass ([editing.md](editing.md)).
