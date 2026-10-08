# Prompting a cut

One cut is one `generate_video` call: the approved first frame as `start_image`, the portraits of the characters in the cut in the model's reference role, audio on, the cut's duration. The prompt is written in this order every time, so the model gets the same shape.

## Structure

1. **Reference mapping.** One line per reference: the label, who it is, and what to take from it ("the face, hair and costume of <character>"). Then: "Use only the faces and costumes from the portraits, not their plain backgrounds. The first image is the opening frame; continue from it."
2. **Style and world line.** The style line verbatim, then the look of this cut in one sentence: period, place, light, palette, grading. Copied from the episode's prompt conventions.
3. **Shots.** "Shot N (a to b s): ..." with the camera, the action and the expression. One to three seconds each; a cut of 10 or 12 seconds holds three to five.
4. **Lines.** For each spoken line: "Between X and Y seconds <CHARACTER> speaks <language> with natural standard pronunciation, lips synced, every syllable articulated distinctly, no added syllables: '<the line>'", the line written in the language's own script, with the voice the bible gives the character in a few words. For the inner voice: "<language> voice-over in <CHARACTER>'s voice, <the bible's voice line>, calm pace, lips NOT moving: '<the line>'".
5. **Sound.** The effects the cut needs, named: wind, a slap, chains, thunder.
6. **Continuity clauses.** The ones the episode fixed, in capitals when a take has missed one before: "ENTIRELY DARK HAIR, NO WHITE", "bare hands, no ring", "the scar on the back of the left hand".
7. **Closing line.** "No music. No subtitles, no on-screen text."

## Rules

- Write the dialogue in the language's own script, directly. A line typed as escape sequences lost a final consonant once and cost a take.
- Put a word that is not said the way it is written in the prompt the way it sounds, and keep the script's spelling for the subtitle ([pronunciation.md](pronunciation.md)).
- Give the first line of a cut at least half a second of lead-in; a take can start mid-word. A name is never the first word of a line.
- Spectacle and a line do not share a second. Put the transformation, the fall or the crash in its own shot and the line before or after it.
- A character who must not see something (they fainted, they turned away) is described as not seeing it in the shot where it happens, or the take shows them watching.
- When a face must read, say "close-up" and the expression; when the world must read, say "wide" and what is in it. The model defaults to medium shots.
- When the server answers with a preset recommendation instead of a job, read the preset id from that answer and call again with it in `declined_preset_id`; the id is read from the answer each time, never remembered.
- The duration is the cut table's. Do not round up for safety; an unused tail is paid for and then trimmed.
- One cut per call, `count` 1, `use_unlim` explicit. The batch tool does not let the review stop a wrong line before the next cut repeats it.

## Regeneration prompts

Keep the frame, the portraits, the shots and the duration; change only what failed. A wrong ordinary word: a plainer word of the same meaning, as [pronunciation.md](pronunciation.md) says, and the line and the subtitle change with it. A wrong name or key word: the respelling for the ear, then the syllables named after the line. A continuity miss (hair, ring, costume): the clause in capitals at the top of the prompt. A missing event (no visible faint, no crash): the event in its own shot with a time window and what the viewer sees.
