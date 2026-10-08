# Reviewing a take

Every take is reviewed before the next cut is generated: two plain speech-to-text decodes, word probabilities and a contact sheet. What was said is settled first; then the verdict table decides accept, fix in the edit, or regenerate. The user sees one-line verdicts as the cuts come in and the whole list at the final-cut checkpoint.

## The sandbox pass

One `sandbox_exec` call per take, run as a background job and polled ([tool-notes.md](tool-notes.md) "Sandbox"), with [stt_check.example.py](../scripts/stt_check.example.py) as the shape:

1. Normalize loudness (integrated -16 LUFS, true peak -1.5 dB), then 16 kHz mono WAV.
2. Decode twice with Whisper, **without a prompt**, with two model sizes (small and medium), the language set, voice activity detection off, word timestamps on. Print every segment with its times and its no-speech probability, and every word with its probability.
3. Only when the two disagree on a word: a third decode with the cut's lines as `initial_prompt`, and a 10-millisecond RMS envelope over the disputed word. These support a reading; they never decide alone.
4. A contact sheet at 2 frames per second, tiled, and the duration.

Voice activity detection stays off for takes: it has missed whispers and invented phrases over wind. Silence is settled by loudness and the no-speech probability, not by the transcript.

## Reading the decodes

Decide what was said in this order, before asking whether it matters:

1. **Spelling is not sound.** Set aside the differences the ear does not hear: a spelling of the same sound, spacing, punctuation, a numeral for its word, a loanword written another way ([pronunciation.md](pronunciation.md) lists them per language). Compare what would be heard, not what is written. A difference in a consonant's series (plain, tense, aspirated) is not a spelling: it is a faithful record of a dropped or added sound.
2. **Agreement decides.** A word that neither plain decode writes as intended was not said as intended, at whatever probability, even where the two disagree on what they heard instead. A decode prompted with the line does not overrule them: the prompt alone makes the model write the intended word.
3. **Disagreement is checked.** A word that one plain decode writes as intended and the other does not may be the model's ear. The prompted decode and the envelope (a closure gap means two words; a burst of noise before a vowel means an aspirated consonant) may settle it. When they do not, the word goes to the delivery as unsettled, with what each decode heard. A word is never handed over as unsettled when the two plain decodes agree.
4. **Then the table.** A sound that is really different is weighed by what the listener gets.

Look first at the names and the key words of the cut: the ending's lines, a secret spoken aloud, a term the series coined.

## Verdicts

| Heard | Verdict | Action |
|---|---|---|
| Both decodes match the line, or differ only in spelling the ear does not hear | Clear | Accept. |
| An ordinary word is one sound off and comes out as no other word, or is replaced by a word of the same meaning, and the delivery is natural | Close enough | Accept; list the word and what was heard in the delivery. The subtitle keeps the script. |
| A word comes out as another word, or as sounds a listener would take for other words; a syllable added or dropped (a particle doubled, a final consonant lost); any real difference in a name or a key word; a line cut off, mumbled, overlapped, or in the wrong language | Wrong word | Regenerate after changing the line ("Regeneration" below). |
| The line arrives outside its window, overlaps another line, or is cut at the head or the tail | Timing | Trim or move in the edit when the words are whole; otherwise regenerate with the window restated and half a second of lead-in. |
| Speech where there should be none, at word probability under 0.1 and a no-speech probability above 0.5, on a stretch more than about 12 dB under the take's real speech | Hallucination | Noise, not speech. Accept; note it. |
| A quiet line present with detection off and right in both decodes | Soft line | Accept; the edit may raise it. |
| The picture breaks continuity (hair, a ring, a costume, an age, the place), drifts from the frame or the style, or contradicts the knowledge table (a character watching what they must not see) | Continuity | Regenerate with the clause in capitals at the top of the prompt. |
| The event is weak (a crash that barely moves the frame, a transformation too short) but the words are right | Weak picture | Accept; strengthen in the edit (a speed ramp, a flash, a sound) and note it. |

Do not chase a perfect match. Two takes with the same meaning are both fine; the credits are better kept for a cut that is wrong. The exception is a name or a key word: said almost right is said wrong. The opposite mistake costs more: a word that is really wrong handed over as "the machine could not tell" leaves the user to find it by ear.

## Try the edit first

A bad word at the end of a line: trim there and cut to the next segment early. A bad word in the middle of a cut the edit already cuts around: cut on a beat, cover with an effect, or put a flash insert over it while the good audio runs. A line that is right but quiet: raise it in the mix. A subtitle that is off: fix the timing, not the take.

## Regeneration

- Same model, tier, frame, portraits and duration. Aim at the word or the frame that failed; keep the rest of the prompt unchanged so the take still cuts with its neighbors.
- Fix the word before spending the take, in this order: a plainer word of the same meaning for an ordinary word (the line and the subtitle change with it); for a name or a key word, a prompt spelling for the ear, then its syllables named after the line; a name dropped from the line when the sentence survives; a word moved to a term card. A name or a key word is never changed without the user. What the model does with the sounds of the language is in [pronunciation.md](pronunciation.md).
- One retry per cut comes from the reserve without asking. A second needs the user's consent with the ledger shown. When the reserve is gone, every retry does.
- Never regenerate an accepted cut to make it better.
- Record every verdict and retry in the production log: the word, what was tried, what came back, the model, the date. A new sound pattern goes into [pronunciation.md](pronunciation.md) in the same change, in every skill that carries the file.
