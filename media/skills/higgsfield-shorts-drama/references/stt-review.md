# Reviewing a take

Every take is reviewed before the next cut is generated. What was said is settled first by the pass of [/docs/higgsfield/decodes.md](/docs/higgsfield/decodes.md): two plain speech-to-text decodes, a third to break a tie, word probabilities, a loudness envelope and a contact sheet looked at through `image_paths`; [stt_check.example.py](../scripts/stt_check.example.py) is the shape of the pass as one background job. Then the verdict table below decides accept, fix in the edit, or regenerate. The user sees one-line verdicts as the cuts come in and the whole list at the final-cut checkpoint.

## What the pass settles

As the shared page says, in this order: spelling the ear does not hear is set aside, a consonant's series never among it; two plain decodes that agree decide; a disagreement goes to the third plain decode, then to the prompted decode and the envelope as support; what nothing settles goes to the delivery as unsettled with what each decode heard, and never a word two plain decodes agree on; silence is loudness and the no-speech probability, not the transcript. Look first at the names and the key words of the cut: the ending's lines, a secret spoken aloud, a term the series coined.

## Verdicts

| Heard | Verdict | Action |
|---|---|---|
| Both decodes match the line, or differ only in spelling the ear does not hear | Clear | Accept. |
| An ordinary word is one sound off and comes out as no other word, or is replaced by a word of the same meaning | Close enough | Accept; list the word and what was heard in the delivery. The subtitle keeps the script. |
| A word comes out as another word, or as sounds a listener would take for other words; a syllable added or dropped (a particle doubled, a final consonant lost); any real difference in a name or a key word; a line cut off, mumbled, overlapped, or in the wrong language | Wrong word | Regenerate after changing the line ("Regeneration" below). |
| The line arrives more than a second outside its window, overlaps another line, or is cut at the head or the tail | Timing | Trim or move in the edit when the words are whole; otherwise regenerate with the window restated and half a second of lead-in. |
| Speech where there should be none, at word probability under 0.1 and a no-speech probability above 0.5, on a stretch more than about 12 dB under the take's real speech | Hallucination | Noise, not speech. Accept; note it. |
| A quiet line present with detection off and right in both decodes | Soft line | Accept; the edit may raise it. |
| The picture breaks continuity (hair, a ring, a costume, an age, the place), drifts from the frame or the style, or contradicts the knowledge table (a character watching what they must not see) | Continuity | Regenerate with the clause in capitals at the top of the prompt. |
| The event is weak (a crash that barely moves the frame, a transformation too short) but the words are right | Weak picture | Accept; strengthen in the edit (a speed ramp, a flash, a sound) and note it. |
| The line is spoken by another character's mouth, or the on-screen mouth moves during an inner-voice line (the contact sheet shows it) | Wrong mouth | Regenerate with the speaker, and the closed mouth, named in capitals at the top of the prompt. |
| A clear line the script does not have | Added line | Inside a line's window: Wrong word. After the last line: trim in the edit. |
| Music or a score where the prompt asked for none (the envelope shows a bed under the speech) | Stray music | Regenerate when it runs under a line; otherwise accept and say so in the delivery, since the edit cannot remove it. |
| The voice differs from the character's last cut | Unheard | The decodes cannot judge it: name the cut in the delivery as unverified by ear. |

Do not chase a perfect match. Two takes with the same meaning are both fine; the credits are better kept for a cut that is wrong. The exception is a name or a key word: said almost right is said wrong. The opposite mistake costs more: a word that is really wrong handed over as "the machine could not tell" leaves the user to find it by ear.

## Try the edit first

A bad word at the end of a line: trim there and cut to the next segment early; the trimmed words leave the script and the subtitle with it (the three-file sync). A bad word in the middle of a cut the edit already cuts around: cut on a beat, cover with an effect, or put a flash insert over it while the good audio runs. A line that is right but quiet: raise it in the mix. A subtitle that is off: fix the timing, not the take.

## Regeneration

- Same model, tier, frame, portraits and duration. Aim at the word or the frame that failed; keep the rest of the prompt unchanged so the take still cuts with its neighbors. When the first frame itself caused the fault (a wrong person, a wrong place), remake the frame from the frame reserve, show it in the cut's report line, and then the take.
- Fix the word before spending the take, in this order: a plainer word of the same meaning for an ordinary word (the line and the subtitle change with it); for a name or a key word, a prompt spelling for the ear, then its syllables named after the line; a name dropped from the line when the sentence survives; a word moved to a term card. A name or a key word is never changed without the user. What the model does with the sounds of the language is in [/docs/higgsfield/pronunciation.md](/docs/higgsfield/pronunciation.md).
- One retry per cut comes from the reserve without asking. A second needs the user's consent with the ledger shown. When the reserve is gone, every retry does.
- Never regenerate an accepted cut to make it better.
- Record every verdict and retry in the production log: the word, what was tried, what came back, the model, the date. A new sound pattern is reported at the delivery for whoever maintains the skill, so that it reaches [/docs/higgsfield/pronunciation.md](/docs/higgsfield/pronunciation.md), recorded there by the maintainer after the run; a run changes no file of the repository.
