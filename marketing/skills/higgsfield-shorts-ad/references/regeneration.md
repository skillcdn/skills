# Regeneration

When a take's dialogue is ambiguous, regenerate that shot only. This page defines ambiguous, the cheaper alternatives to try first, how a retry is made and the retry budget. Read before the first take. The agent applies it on its own as the takes come in; the user sees every verdict at the clean-master checkpoint and can ask for a retry there.

## What counts as ambiguous

Judge each take right after it is generated, from watching it and from its Whisper transcript compared with the intended line.

| Verdict | Definition | Action |
|---|---|---|
| Clear | The transcript matches the intended line, or differs only in what the ear does not hear: filler, contraction, punctuation, spacing, a numeral for its word, a loanword spelled another way, sounds the language's speakers do not tell apart. | Accept. |
| Close enough | An ordinary word is one sound off and comes out as no other word, so the sentence still says what it meant; or it is replaced by a word of the same meaning. Delivery is natural. | Accept, and name the word in the delivery with what was heard. The caption still shows the intended line. |
| Ambiguous | A word comes out as another word, or as sounds a listener would take for other words, even where the sentence can still be guessed; a word is missing or added; any real difference of sound in a key word; the line is cut off, mumbled, overlapped by another voice, or in the wrong language. | Fix in code if possible, otherwise regenerate. |
| Broken | No speech where there should be, or speech where there should be none, judged from loudness and Whisper's no-speech probability, not from the transcript alone (a stretch about 12 dB under the take's real speech with a no-speech probability above 0.5 is silence, whatever the transcript says); or the take starts mid-word, the line's first sound cut at the head (speech at full level in the first frame). | Regenerate; for a cut first sound, ask for about half a second of silence before the first word. |
| Flat | The words are right but the performance is not the beat: no visible emotion, the wrong emotion, no turn where the shot has one, or a dead pause. | Trim to the good part when it exists; otherwise regenerate once with the performance line made concrete (the expression, the gesture, the pace, the eye line), not longer. |
| Dragging | The words are right but the pace is not the reference's: the take's rate is more than twenty percent under the density target of the brief after the pauses have been tightened in code, or a dead pause sits where the reference has none ([story.md](story.md) "Density"). | Tighten pauses in code first. Otherwise regenerate once with the pace stated in numbers (units per second, pauses under half a second) and the take sized to the speaking time plus a second, not to the ad. |
| Drifted | The look changes inside the take or against the frame: a drawn character turning photoreal, a shift of style, palette or proportions, a background that changes. | Trim to the good part when it exists; otherwise regenerate once with the style line first in the prompt and the medium stated. |

**Key words** are the words that must come out right and must stay: the brand or product name, the product's own terms, the story's device, and every word of the hook, the signature line and the reveal. Every other word is ordinary.

Do not chase a perfect match. Two takes with the same meaning are both fine; the credits are better kept for a shot that is actually wrong. The exception is the key words: a tagline said almost right is said wrong, because the audience knows it. The opposite mistake costs the user more: a word that is really wrong, handed over as "the machine could not tell", leaves them to find it by ear.

## Reading the transcript

What was said is settled by the pass of [/docs/higgsfield/decodes.md](/docs/higgsfield/decodes.md) before the table above asks whether it matters: two plain decodes without a prompt, a third plain decode with the largest model when they disagree; spelling the ear does not hear set aside, a consonant's series never among it; agreement deciding; a decode prompted with the intended line and the loudness envelope supporting a reading and never deciding; a word handed over as unsettled only when nothing settled it, and never when two plain decodes agree; silence settled by loudness and the no-speech probability, not by the transcript. A homophone of the intended word is no fault of the take: where it changes the meaning, the line should not have used the word.

Look first at the key words the shot list marks as kept at risk, and at the word the user named when they rejected a take.

## Try code first

Before spending credits, check whether the edit can absorb the problem:

- A bad word at the end of a line: trim the take there and cut to the next shot early.
- A bad word in the middle: cut around it on a beat, cover with a sound effect, or cut to an insert (product shot, title card) over the bad part while keeping the good audio.
- A line that is fine but too quiet or too loud: normalize in the mix.
- A line that is right but the caption is off: fix the caption alignment, not the take.

If none of these keeps the meaning and the delivery natural, regenerate.

## How to regenerate

- Same model, same tier, same aspect ratio, and the same duration unless the retry is a pickup. Regeneration is not the moment to upgrade quality.
- The same approved first frame and the same portrait as identity input, exactly as in the first take ([cast.md](cast.md)), so the cast and the composition stay consistent. Keep the visual prompt unchanged so the take still cuts with its neighbors.
- A take that holds several lines, one or two of them wrong, is not made again whole when the edit already cuts between lines (a monologue in jump cuts, a presenter over panels, a voice under pictures). Make a **pickup**: a short take of the wrong lines alone, a second of silence between two of them, from the same first frame and portrait, sized to the lines plus a second, preflighted because its duration is new, at the take's pace or a little under it, and cut in at each line. It costs the lines, not the take, and it is the shot's one retry.
- Put the line in the prompt in quotes, as intended except for the words that carry a prompt spelling, and state explicitly that the character says exactly these words, in which language, and nothing else.
- Aim the retry at the word that failed, fixed as "Fixing a word" says before the take is spent. When the user rejects a take, quote their complaint word for word and check that word in the review; a retry that fixes a different word is a wasted take.
- Generate one take. Judge it by the same table.

## Fixing a word

The lines were written to be said, with prompt spellings from the first take ([story.md](story.md) "Lines a model can say"); the sounds each language's lines have lost, and what fixed each, are in [/docs/higgsfield/pronunciation.md](/docs/higgsfield/pronunciation.md). A word that failed all the same:

1. **An ordinary word is said another way.** It is not respelled: the retry uses a plainer word for it, picked by the agent and reported with the take, and the intended line and the caption change with it. A key word is never changed without the user.
2. **A key word gets one more spelling, then the screen.** Spell it for the ear if it was not yet; when the fault is a swallowed consonant, name the word's syllables after the line (for Korean in Latin letters: "so and jae, with a clear j sound"). When that fails as well, the word goes on screen as text while the line goes on without it, or the user chooses another word.
3. **Check the word, not the sentence**, as "Reading the transcript" says: the plain decodes first. Only where they disagree, or the user hears what neither wrote, the third decode, then the envelope of that syllable and the prompted decode, compared with the rejected take.
4. **Record the outcome** in the run's folder, under the ledger: the word, what was tried, whether it worked, the model and the month. A run changes no file of the pack.

## Retry budget

- One retry per shot comes out of the reserve the user accepted and is taken without asking.
- A second retry for the same shot needs the user's consent, with the ledger shown: what was spent, what is left, and what the alternative in code would look like.
- When the reserve is gone, every retry needs consent.
- Never regenerate a shot that was already accepted to make it "better". Only ambiguous, broken, flat, drifted or dragging takes are retried.

## Record it

Each retry is a row in the budget ledger with the reason (ambiguous: which word; broken: what happened) and the verdict of the new take. The ledger is part of the delivery.
