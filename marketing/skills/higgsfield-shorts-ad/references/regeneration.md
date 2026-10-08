# Regeneration

When a take's dialogue is ambiguous, regenerate that shot only. This page defines ambiguous, the retry budget, and the cheaper alternatives to try first. The agent applies it on its own as the takes come in; the user sees every verdict at the clean-master checkpoint and can ask for a retry there.

## What counts as ambiguous

Judge each take right after it is generated, from watching it and from its Whisper transcript compared with the intended line.

| Verdict | Definition | Action |
|---|---|---|
| Clear | The transcript matches the intended line, or differs only in what the ear does not hear: filler, contraction, punctuation, spacing, a numeral for its word, a loanword spelled another way, sounds the language's speakers do not tell apart. | Accept. |
| Close enough | An ordinary word is one sound off and comes out as no other word, so the sentence still says what it meant; or it is replaced by a word of the same meaning. Delivery is natural. | Accept, and name the word in the delivery with what was heard. The caption still shows the intended line. |
| Ambiguous | A word comes out as another word, or as sounds a listener would take for other words, even where the sentence can still be guessed; a word is missing or added; any real difference of sound in a key word; the line is cut off, mumbled, overlapped by another voice, or in the wrong language. | Fix in code if possible, otherwise regenerate. |
| Broken | No speech where there should be, or speech where there should be none, judged from loudness and Whisper's no-speech probability, not from the transcript alone; or the take starts mid-word, the line's first sound cut at the head (speech at full level in the first frame). | Regenerate; for a cut first sound, ask for about half a second of silence before the first word. |
| Flat | The words are right but the performance is not the beat: no visible emotion, the wrong emotion, no turn where the shot has one, or a dead pause. | Trim to the good part when it exists; otherwise regenerate once with the performance line made concrete (the expression, the gesture, the pace, the eye line), not longer. |
| Dragging | The words are right but the pace is not the reference's: the take's rate is more than twenty percent under the density target of the brief after the pauses have been tightened in code, or a dead pause sits where the reference has none ([story.md](story.md) "Density"). | Tighten pauses in code first. Otherwise regenerate once with the pace stated in numbers (units per second, pauses under half a second) and the take sized to the speaking time plus a second, not to the ad. |
| Drifted | The look changes inside the take or against the frame: a drawn character turning photoreal, a shift of style, palette or proportions, a background that changes. | Trim to the good part when it exists; otherwise regenerate once with the style line first in the prompt and the medium stated. |

**Key words** are the words that must come out right and must stay: the brand or product name, the product's own terms (what its page calls its things: a plan, a unit, a feature), the story's device, and every word of the hook, the signature line and the reveal. Every other word is ordinary.

Do not chase a perfect match. Two takes with the same meaning are both fine; the credits are better kept for a shot that is actually wrong. The exception is the key words: a tagline said almost right is said wrong, because the audience knows it. The opposite mistake costs the user more: a word that is really wrong, handed over as "the machine could not tell", leaves them to find it by ear.

## Reading the transcript

The verdict needs to know what was said before it can ask whether it matters. Decide that in this order:

1. **Two plain decodes.** Every speaking take is decoded twice without a prompt, with the small and the medium model. The small one writes what it hears more literally; the medium one corrects more.
2. **Spelling is not sound.** Set aside the differences the ear does not hear (the "Clear" row; [pronunciation.md](pronunciation.md) lists them for the languages run so far). Compare what would be heard, not what is written. A homophone of the intended word is no fault of the take: where it changes the meaning, the line should not have used the word.
3. **Agreement decides.** A word that neither decode writes as intended was not said as intended, at whatever probability, even where the two disagree on what they heard instead; so was a sound that comes back in a retake of the same word. A decode prompted with the intended line does not overrule them: the prompt alone makes the model write the intended word.
4. **Disagreement is unsettled.** A word that one decode writes as intended and the other does not may be the model's ear. The checks below (the envelope, the prompted decode) may settle it; when they do not, the word goes to the delivery as unsettled, with what each decode heard.
5. **Then the table.** A sound that is really different is weighed by what the listener gets: another word or a key word is a fault; a near miss in an ordinary line is not.

Look first at the key words marked as kept at risk when the lines were written ("Pronunciation" below).

## What the transcript cannot decide

- On near-silence, Whisper invents stock phrases. Before calling a silent shot "speech where there should be none", measure: a stretch more than about 12 dB under the take's real speech, with a no-speech probability above 0.5, is silence whatever the transcript says. Frames showing a closed, still mouth confirm it.
- A transcript that differs from the intended word only in a consonant's series (aspirated, tense or plain: Korean ㅎ-clusters written as ㄱ instead of ㅋ, for instance) is not a homophone spelling. It is a faithful record of a dropped or added sound: a real difference, weighed by the table like any other. Two takes in one run were accepted as "homophones" this way and both had the fault.
- Whisper normalizes dialect and homophones to standard spellings (a regional "you" becomes the standard one, two words that sound like one are written as one), and the medium model does the same as the small one, so the transcript cannot arbitrate a pronunciation question of that kind. Two free checks in the sandbox can: a 10-millisecond RMS envelope over the disputed word, where a closure gap of about 100 milliseconds means two words and its depth and length compare takes; and a second decode with the intended line as Whisper's `initial_prompt`, which shows whether the audio supports the intended reading. On a damaged take the prompted decode can return nothing usable; it supports a reading, it never decides alone, and it is no answer to two plain decodes that agree. When the checks tie, prefer the take made with the explicit pronunciation instruction, and say in the delivery that the machine check is not conclusive.

## Try code first

Before spending credits, check whether the edit can absorb the problem:

- A bad word at the end of a line: trim the take there and cut to the next shot early.
- A bad word in the middle: cut around it on a beat, cover with a sound effect, or cut to an insert (product shot, title card) over the bad part while keeping the good audio.
- A line that is fine but too quiet or too loud: normalize in the mix.
- A line that is right but the caption is off: fix the caption alignment, not the take.

If none of these keeps the meaning and the delivery natural, regenerate.

## How to regenerate

- Same model, same tier, same aspect ratio, and the same duration unless the retry is a pickup. Regeneration is not the moment to upgrade quality.
- A take that holds several lines, one or two of them wrong, is not made again whole when the edit already cuts between lines (a monologue in jump cuts, a presenter over panels, a voice under pictures). Make a **pickup**: a short take of the wrong lines alone, a second of silence between two of them, from the same first frame and portrait, sized to the lines plus a second, preflighted because its duration is new, at the take's pace or a little under it, and cut in at each line. It costs the lines, not the take, and it is the shot's one retry.
- Put the line in the prompt in quotes, as intended except for the words that carry a prompt spelling, and state explicitly that the character says exactly these words, in which language, and nothing else. Keep the visual prompt unchanged so the take still cuts with its neighbors.
- Aim the retry at the word that failed. When the user rejects a take, quote their complaint word for word and check that word in the review; a retry that fixes a different word is a wasted take.
- Fix the word as "Pronunciation" below says, before spending the take.

## Pronunciation

Video models with native dialogue have no pronunciation dictionary, and the transcript often cannot even show the fault. This is the procedure; do not research it again. A fault kept out of the first take costs nothing; one found in a take costs a retry; one found by the user costs their trust.

1. **Write the line so it can be said, and heard.** Five to ten words per line, one language per line, the face front-on or three-quarter with the mouth unobstructed, no head turn while speaking. A line is heard before it is read: a word whose sound is another word's in the language, and would change the meaning without the caption (a homophone, or the bare short form of a compound term), is replaced or given its full form; the product's own compound term is preferred to its short form. Put the line in quotes and say that the character speaks exactly these words in that language with natural standard pronunciation and nothing else. Ask for about half a second of silence before the first word: a take can start mid-word and lose its first consonant, which no edit restores. The first word of a take is also the one the model says fastest, so a brand or persona name is never the first word of a line; give it a lead-in word. Longer speeches are split across shots.
2. **Spell for the ear in the prompt, from the first take.** A model reads letters. A word that is not said the way it is written goes into the take prompt the way it sounds, in the language's own script, while the intended line and the caption keep the spelling: for Korean, an aspirated cluster ("적혔다" prompted as "저켰다"), a final consonant carried onto the next vowel ("…님의" as "…니메"), a double final ("까닭" as "까닥"); for English, a name or a coined word as hyphenated syllables with the stressed one in capitals. This is the dictionary trick of text-to-speech tools. It has fixed every fault of this kind recorded in [pronunciation.md](pronunciation.md), so it is not saved for a retry. The shot list keeps each prompt spelling next to its word.
3. **Keep the key words clear of what the model slurs.** [pronunciation.md](pronunciation.md) also lists sounds the model has swallowed at speed that no spelling fixed. Where a key word's place can take a word without them that says the same, use it; a key word that has one stays, and the shot list marks it as kept at risk, so the review looks at it first. Ordinary words are left as written: most of them come out right, the review catches the rest, and a script rewritten around sounds loses its voice.
4. **Say an ordinary word another way in the retry.** An ordinary word that failed is not respelled: the retry uses a plainer word for it, picked by the agent and reported with the take, and the intended line and the caption change with it. A key word is never changed without the user.
5. **Give a key word that failed one more spelling, then the screen.** Spell it for the ear if it was not yet; when the fault is a swallowed consonant, name the word's syllables after the line (for Korean in Latin letters: "so and jae, with a clear j sound"). When that fails as well, the word goes on screen as text while the line goes on without it, or the user chooses another word.
6. **Check the word, not the sentence**, as "Reading the transcript" says: the two plain decodes first. Only where they disagree, or the user hears what neither wrote, decode once more with the intended line as `initial_prompt`, listen to the envelope of that syllable (an aspirated consonant shows a burst and a noisy onset before the vowel; a dropped one does not), and compare with the rejected take.
7. **Record the outcome** in [pronunciation.md](pronunciation.md), in every skill that carries the file: the word, what was tried, whether it worked, the model and the date; and move the sound to the right list there.
- Start from the same approved first frame and pass the same portrait as identity input, exactly as in the first take ([cast](cast.md)), so the cast and the composition stay consistent. Nothing from the reference video, ever.
- Generate one take. Judge it by the same table.

## Retry budget

- One retry per shot comes out of the reserve the user accepted and is taken without asking.
- A second retry for the same shot needs the user's consent, with the ledger shown: what was spent, what is left, and what the alternative in code would look like.
- When the reserve is gone, every retry needs consent.
- Never regenerate a shot that was already accepted to make it "better". Only ambiguous, broken, flat, drifted or dragging takes are retried.

## Record it

Each retry is a row in the budget ledger with the reason (ambiguous: which word; broken: what happened) and the verdict of the new take. The ledger is part of the delivery.
