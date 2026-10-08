# Episode script: the cut table

One episode is one Markdown file: a header table, the reference table, the cut table, the edit plan, and the prompt conventions that hold for the episode. An example of the cut table as data is [cut-list.example.json](../assets/cut-list.example.json).

## Header

| Field | Value |
|---|---|
| Target length | After the edit, about 150 seconds unless the user named a length; generate about 10 percent more. |
| Format and model | 9:16, the model chosen in phase 3, lowest tier, audio on. |
| Method | Every cut new, one at a time, from its approved first frame; two plain speech-to-text decodes and a contact sheet per cut; only failed cuts regenerated. |
| What the viewer knows by second thirty | Copied from the bible. |
| What a character does not know | The knowledge-table facts this episode turns on, so the ending is checked against them. |
| Ending hook | The last three lines, verbatim. |
| Estimated credits | From the preflight, with the reserve; filled in phase 3. |

## The episode formula

| Beat | Time | Content |
|---|---|---|
| Previously | 0:00 to 0:08 | From the second episode on: three lines cut from the previous episode's accepted takes. Edit only, no credits. |
| Opening hook | to about 0:20 | Right after the last ending; straight into an event. |
| The wrong | to about 1:00 | Insults, threats and harm done in the open. |
| The payback | to about 1:40 | Answered in this episode, clearly. |
| The bigger blow | to about 2:15 | The emotional or spectacular peak. |
| Ending hook | about 2:30 | A clear new event. |

A shorter episode keeps every beat and shortens each in proportion; the wrong and the payback are never dropped.

## The reference table

One row per portrait and set the episode needs: the key, what it is, the look (a character in two periods has two rows), whether it exists (the media id from the bible) or is new.

## The cut table

| Column | Content |
|---|---|
| Number | E1, E2, ... in shooting order, which is screen order. |
| Length | 7 to 12 seconds, within the model's durations. A cut with two or more lines needs 10 or 12. |
| References | The keys of the portraits in the cut (the look of the period) and its set. |
| First frame | The opening image in one sentence: framing, who stands where, the place, the light, the pose and the starting emotion. The image model makes it from the references; the video model starts from it. |
| Shots | Numbered shots with the camera and the action, one to three seconds each; the look of the period or world in brackets at the start. |
| Lines and sound | Each line with its speaker and its time window inside the cut; voice-over marked as inner voice; sound effects after a marker. |
| Edit note | What the edit adds here (a name card, a flash, a fade) and any line that was changed for pronunciation, with the reason. |

Total the lengths under the table.

## Writing lines

- Short. Five to twelve words, one breath, commas where the voice should pause. Lines in one cut are at least a second apart; the last line ends at least half a second before the cut does, or the edit cannot trim the tail.
- Plain words. A word the viewer must decode, a coined term, or a sound the model is known to slur in the dialogue language ([pronunciation.md](pronunciation.md)) is replaced with a plain word of the same meaning before the first take. Ordinary words are otherwise left as written; a script rewritten around sounds loses its voice.
- A character's name is never the first word of a line, and a name whose sound the model has bent before is left out of the line when the sentence survives without it. Names and key words (a secret said aloud, the ending's lines) are what the review looks at first; they carry a prompt spelling from the first take when they are not said the way they are written.
- A line that must land in a window is given one: "between 3 and 5.5 seconds".
- The inner voice narrates the situation at turning points, in the character's own voice, in the tense the bible fixed; it is marked so the prompt keeps the mouth closed.
- Every line is read against the knowledge table before the checkpoint: who hears it, and what do they know at this second.

## Edit plan

A table of position and overlay: where the name cards go (first appearance, top of frame, name plus relationship), term cards, flash inserts (picture only), fades, freeze at the end. End it with the line "Not on screen: series title, next-episode card" unless the user asked for them.

## Prompt conventions for the episode

The lines that every prompt of this episode repeats: the style line, the reference mapping, the continuity clauses (hair color, a ring worn or not, a scar, the period grading), the dialogue instruction with the language named, the no-text instruction. They are written once here and copied into every cut's prompt by [prompting.md](prompting.md).

## Generation order

1. New portraits and sets (phase 4), then the first frames (phase 5).
2. Cuts in screen order, one at a time, review after each (phase 6).
3. Assembly, verification, delivery (phases 7 and 8).
