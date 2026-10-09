# Captions

Captions show the **intended line**. Speech-to-text supplies the **clock**. Never burn a raw transcript.

## Why not the transcript

A model speaks the line it was given, mostly. Speech-to-text then hears the line, mostly. Burning what was heard doubles the error: a brand name becomes a common word, a number changes, a filler word appears. The intended line is what the user approved in the shot list, so it is what the caption says. If the take does not actually say the intended line, that is a regeneration question ([regeneration.md](regeneration.md)), not a caption question.

## Pipeline

Four steps, in one `sandbox_exec` call on the clean master, in this order. Skipping the verification step is how captions drift.

1. **Transcribe** the clean master's audio with Whisper, word timestamps on, voice activity detection on with its silence split set to about 300 milliseconds (the default of two seconds stretches word starts backwards into pauses and effects, and every cue after a pause comes out early), language set to the dialogue language. On a mixed track (music under speech), band-pass the voice range first or transcribe the pre-mix speech stems if the edit kept them. Then snap each cue start to the loudness onset of its first word: the first 30-millisecond run above the shot's own peak minus 18 dB, searched from 0.2 seconds before to 0.6 seconds after Whisper's time for that word. A fixed threshold is crossed by loudness-normalized room tone, and Whisper may put a first word before its sound. Clamp every cue to the cut boundaries of its shot so no caption lingers over the next shot.
2. **Align** each intended line to the transcript: match line by line in order, take the first and last word times of the matched span as the cue window, then split the line into cues of at most five words and two lines at the design size (about 32 Latin or 18 Hangul or CJK characters per line on a 480-pixel-wide frame), at commas where possible, each cue starting at its own first word's timestamp. Cues come from word timestamps, never from segments or from a block window spread by word count: Whisper may return one segment for several sentences, and a spread window swallows the pauses between them, so every later cue shows up early. A pause longer than half a second inside a matched span closes the cue at the last word before it. A cue never starts more than 0.2 seconds before its first word or ends more than 0.5 seconds after its last. Report a similarity score per line; below 0.9, look at the line by hand before burning. A low score caused by spelling alone (dialect, homophones the intended line writes differently) is fine when every cue start is within 0.3 seconds of the master's own word timestamps.
3. **Burn** in the brand's look ("Look" below). Position follows the reference, when its captions sit inside the platform safe zones and off faces (top of frame or beside the speaker are common); otherwise bottom of frame. Safe zones for portrait, the values seen for Reels and Shorts (checked 2026-10; the platform the user names is read at run time): the top 12 percent and the bottom 17 percent of the height are kept for overlays only when the reference uses them, and 11 percent margins on the sides always. One or two lines, never over a face or the prop in hand: when a hand or a prop moves through the caption band in a shot, move that shot's cues, checked on frames sampled across the shot. No animation, no emoji, no karaoke highlighting.
4. **Verify**: output duration equals input within one second, audio stream intact, every intended word present in the cue file, every cue start within 0.3 seconds of the speech onset in the master's loudness curve, and two frames at cue midpoints extracted and inspected. A tool that reports contiguous cues with no gap across a pause has spread a window; rebuild the cues from word timestamps.

## Burning

Write an ASS or SRT file from the aligned intended lines and burn it with ffmpeg's `subtitles` filter, with `fontsdir` and `force_style` in the brand's type and color ([design.md](design.md)), in one background script. Keep the cue file next to the output for verification; it cannot be uploaded, so the delivery carries the cue text.

The server's bundled `subtitles` workflow is not used ([/docs/higgsfield/sandbox.md](/docs/higgsfield/sandbox.md) says why); its rule against a hand-rolled burn does not apply here.

## Look

The caption look is the brand's: family, weight, color and size from [design.md](design.md), placement from the reference. The bold white UGC look is used only when the reference is UGC-style and the brand has no type of its own.

## Language and fonts

Captions are in the dialogue language unless the user asked for another. A translated caption is still aligned to the spoken line's clock. "Caps" in the looks table applies only to scripts that have case.

Fonts beyond Latin are fetched as [/docs/higgsfield/sandbox.md](/docs/higgsfield/sandbox.md) "Fonts" says, while a take renders, so the caption step does not wait for them; `FontName` is the family's English name, and an empty or boxed caption is a font failure, not a timing failure.
