# Decoding a take

What a take says is settled by machine before anyone asks whether it matters: two plain speech-to-text decodes, a third to break a tie, word probabilities, a loudness envelope and a contact sheet. This page is the pass and how its output is read; the verdict a skill draws from it (accept, fix in the edit, regenerate) is in that skill's own reference. The opposite mistake costs more than a retry: a word that is really wrong, handed over as "the machine could not tell", leaves the user to find it by ear.

## The pass

One `sandbox_exec` call per take, as a background job polled with short calls ([`sandbox.md`](sandbox.md)); the sandbox has the models, and an agent's own shell may not:

1. Normalize loudness (integrated -16 LUFS, true peak -1.5 dB), then 16 kHz mono WAV. Normalizing first raises a whispered line from undetected to clear.
2. Decode twice with Whisper (`faster_whisper`), **without a prompt**, with two model sizes (`small` and `medium`), the language set, voice activity detection off, word timestamps on. Print every segment with its times and its no-speech probability, and every word with its probability. The small model writes what it hears more literally; the medium one corrects more. Models up to the largest run on the sandbox's CPU; the first load takes about a minute.
3. When the two plain decodes disagree on a word, a third plain decode with the largest model (`large-v3`) breaks the tie: two of three plain decodes agreeing settle what was said. It may run in the same pass and is read only then.
4. Support, never a decision: a decode with the take's intended lines as `initial_prompt`, and a 10-millisecond RMS envelope over the disputed word, from the 16 kHz WAV: `asetnsamples=160,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=env.txt` writes one value per 10 milliseconds. A dip of about 20 dB lasting around 100 milliseconds is the closure between two words; a burst of noise right before a vowel is an aspirated consonant; its depth and length compare two takes of the same word.
5. A contact sheet at 2 frames per second, tiled, and the duration. Look at the sheet with a short foreground call that passes it in `image_paths`, within the job's lease.

```python
from faster_whisper import WhisperModel
def decode(size, prompt=None):
    model = WhisperModel(size, device="cpu", compute_type="int8")
    segs, _ = model.transcribe("norm.wav", language=lang, word_timestamps=True, vad_filter=False,
                               initial_prompt=prompt, beam_size=5)
    for s in segs:
        print(f"[{s.start:.2f}-{s.end:.2f}] no_speech={s.no_speech_prob:.2f} {s.text.strip()}")
        print("   " + " ".join(f"{w.word.strip()}({w.probability:.2f})" for w in (s.words or [])))
```

Voice activity detection stays off for takes: it misses a whispered line entirely, invents a stock phrase over wind, and on a sighing shot returns a low-confidence phrase on a stretch 13 dB under real speech. Silence is settled by loudness and the no-speech probability, not by the transcript. Detection has its one use on a mixed master, for caption timing only: there the default two-second split pushes word starts back into pauses and onto a chime, and a split of about 300 milliseconds with onset snapping and cut clamping gets every cue right ([the ad skill's captions](../../marketing/skills/higgsfield-shorts-ad/references/captions.md)).

## Reading the decodes

Decide what was said in this order, before asking whether it matters:

1. **Spelling is not sound.** Set aside the differences the ear does not hear: a spelling of the same sound, spacing, punctuation, a numeral for its word, a loanword written another way ([`pronunciation.md`](pronunciation.md) lists them per language). Compare what would be heard, not what is written. A difference in a consonant's series (plain, tense, aspirated: a Korean ㅎ-cluster written with ㄱ instead of ㅋ) is not a spelling: it is a faithful record of a dropped or added sound, a real difference. Two takes in one run were accepted as homophones this way and both had the fault.
2. **Agreement decides.** A word that neither plain decode writes as intended was not said as intended, at whatever probability, even where the two disagree on what they heard instead; so was a sound that comes back in a retake of the same word. A decode prompted with the line does not overrule them: the prompt alone makes the model write the intended word, and on a damaged take it can return nothing usable. A word both plain decodes had written as another word, in a take and again in its pickup, was once handed to the user as unsettled on the strength of a prompted decode, and the user heard it as wrong at once.
3. **Disagreement is checked.** A word that one plain decode writes as intended and the other does not may be the model's ear: a verb ending written differently by one size, a plain initial written tense, a whispered line the medium model did not decode at all while the small and the largest did, a vowel the medium and the largest heard as another while the small heard it right. The third plain decode settles it when two of the three agree; otherwise the prompted decode and the envelope may. When nothing does, the word goes to the delivery as unsettled, with what each decode heard. A word is never handed over as unsettled when two plain decodes agree.
4. **Then the skill's verdict table.** A sound that is really different is weighed by what the listener gets: another word, a key word, a near miss in an ordinary line.

Look first at the names and the key words of the take: a brand or product name, its terms, a secret spoken aloud, the lines of the hook, the signature line and the reveal. A line that one decode writes with a word the user heard as wrong is checked for that word, not for the sentence: a retry that fixes another word is a wasted take.

## What the decodes cannot settle

- **Silence and hallucination.** On near-silence Whisper invents stock phrases. A stretch more than about 12 dB under the take's real speech (per-second RMS from `asetnsamples=16000` in the same filter chain), with a no-speech probability above 0.5 and word probabilities under 0.1, is noise, not speech, whatever the transcript says; frames showing a closed, still mouth confirm it. A forced laugh right before a line drops every decode's probabilities for the next word under 0.1 while the envelope shows the speech and the words are right.
- **Dialect and homophones.** Whisper normalizes a dialect pronoun to the standard one and writes two words that sound like one as one, in every size. The envelope (a closure gap means two words) and the prompted decode (whether the audio supports the intended reading) can arbitrate; when they tie, prefer the take made with the explicit pronunciation instruction and say in the delivery that the machine check is not conclusive.
- **On-screen text.** A decode of a reference or a master hears speech, not captions: the small model misheard two words of a dialect line that its burned caption showed, and missed two on-screen lines never spoken. Frames are the ground truth for text; the transcript is the clock.
- **A reference under music.** With detection on, the default split and a 300-millisecond one both return garbage fragments with impossible timestamps on speech 13 to 20 dB above a piano bed; a decode without detection and with the language set recovers every line.
