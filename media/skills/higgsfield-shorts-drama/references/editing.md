# Assembling the episode in code

One self-contained Python script runs in the sandbox and produces the final cut from the accepted takes. It is written into the sandbox by a heredoc inside one command (the command limit is 16,000 characters, so the script stays short and the take URLs go into a separate file written by the same command), uploaded from there to a presigned URL from `media_upload` as a general file so it has a permanent URL, and fetched by that URL in later calls; it is re-run with environment overrides (a replaced take, new line timings, finalized takes) rather than rewritten. [assemble.example.py](../scripts/assemble.example.py) shows the shape. Run it with `background: true` and poll its log; an encode of a whole episode plus its uploads exceeds the foreground transport timeout.

## Steps

1. **Fetch** every accepted take by its hosted URL and the fonts (open-licensed, covering the dialogue's script, from the google/fonts repository) into the working directory; skip what is already there. The sandbox is discarded between calls, so the script fetches everything it needs itself.
2. **Segments.** One row per piece of the timeline: output name, source take, start, duration, freeze padding, extra video filter, audio override. Each is normalized alone: scale to the output size, square pixels, fixed frame rate, a 30-millisecond audio fade in and a 40-millisecond fade out, padding to the exact duration. Encode with the same video and audio settings everywhere so the concatenation copies streams. Work at the takes' native resolution; do not upscale drafts.
3. **Trims.** Cut a take's head when the first line starts late, and its tail after the last line when the cut table left room; never trim a tail a line runs to.
4. **Flash inserts.** A half-second picture from another take (a memory, a fall), color-treated (desaturated, higher contrast, white fades of 80 milliseconds in and out). **Picture only:** the audio of the flash segment is taken from the surrounding take at the same timeline position, so the take's sound runs through unbroken. A flash that brought its own audio once carried a fragment of another cut's narration into the scene.
5. **Transitions.** A white fade of about half a second into the prologue; a freeze of the last frame and a fade to black at the end. No dissolves between dialogue cuts.
6. **Concatenate** the segments; print the total and each segment's timeline offset.
7. **Subtitles.** An ASS file with these styles: dialogue (white, bold, bottom), inner voice (a warm off-white, italic, bottom), name (large serif, top corner), role (small, colored, under the name), term (boxed, top center). A dialogue event per line: the script's words, the time from the take's review decode, offset to the timeline, the end padded by 0.2 to 0.3 seconds. A name card at a character's first appearance, with the relationship line; a term card at a coined word's first use; a fade of a quarter second on cards. Burn with ffmpeg's `subtitles` filter and the fonts directory.
8. **Loudness.** Normalize the whole program to -16 LUFS integrated, -1.5 dB true peak, with the channel layout stated on both sides of the filter.
9. **Contact sheet.** One frame every four seconds, tiled; looked at through `image_paths` in a short foreground call within the job's lease, and uploaded like the episode so the user has its link.
10. **Upload.** The output reserved with `media_upload` before the script runs and PUT at its end with the `Content-Type` the result names; `media_confirm` only after HTTP 200; a new reservation for every revision.

## Subtitle rules

- The words are the script's. A decode that heard a word wrong changes nothing on screen; that is a regeneration question.
- Two lines at most, broken at a comma; about 32 Latin or 18 Hangul or CJK characters per line at 480 pixels wide.
- The inner voice is styled apart so the viewer knows nobody is speaking.
- Name cards carry the relationship, never only the name; right-aligned when the character stands on the right; never over a face.
- Nothing else is written on the picture: no series title, no episode title, no next-episode card, unless the user asked. Explanation goes into name cards, term cards and the inner voice.
- Fonts: the sandbox's preinstalled caption fonts cover Latin only. For any other script fetch a font under the SIL Open Font License from the google/fonts repository on GitHub (the `ofl/<family>` directory, Noto Sans for the script) into a `fonts` directory, pass `fontsdir`, and check that the download is a font and not an error page; a missing font shows as empty or boxed subtitles, not as an error. The style's font name is the family's English name.

## Previously-on

From the second episode: three lines cut from the previous episode's accepted takes, with their subtitles, before the opening hook. Edit only; no credits.

## Verification before the checkpoint

- Duration within a second of the segment total; one video and one audio stream; the frame size and rate intended.
- Every flash region decoded again: no speech where the cut table has none. A stock phrase at word probability under 0.1 is a hallucination, not a line.
- Every region around a replaced take decoded again and compared with the script.
- The contact sheet looked at, and frames at the cards' midpoints: cards on the right characters, no card over a face, continuity across cuts.
- The output uploaded and confirmed; the link, and the file where the agent has a filesystem, both delivered.

## A higher resolution later

When the user accepts the finalize or upscale offer at the delivery, the finalized takes' URLs replace the drafts' in the script's environment and the script is re-run as it is; a timeline in seconds does not change with the resolution. An upscale of the assembled episode needs no re-run.
