# Analysis brief

The artifact of phase 2: the sandbox pass that measures the reference, and the template the brief is written in. Fill every section; write "none" rather than leaving a section out, so the user can see what was looked for.

## Sandbox pass

Run in one `sandbox_exec` call, started with `background: true`, while `video_analysis_create` is processing. `<url>` is a link the sandbox can download: the original link when it points straight at a media file, otherwise the hosted URL of the confirmed upload or import (`show_medias` with type `video` lists it). Before the call, reserve an upload for the contact sheet with `media_upload` (filename `sheet.png`) and put its `upload_url` on the last line, so the sheet can be looked at by its hosted URL after `media_confirm`. The call returns a pid, a log path and a status path; poll them with later short calls (`sleep 20; cat <status path>; tail -n 60 <log path>`, a sleep of at most 25 seconds and `timeout_seconds` of at most 45, as [/docs/higgsfield/sandbox.md](/docs/higgsfield/sandbox.md) says). The pass takes about a minute, the Whisper model download included.

The scene analysis is never waited for ([tool-notes.md](tool-notes.md) "Scene analysis"): the brief is built from the frames and the transcript, and the analysis is folded in if it arrives.

```sh
curl -fsSL -o ref.mp4 '<url>' \
&& ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of json ref.mp4 \
&& mkdir -p frames \
&& ffmpeg -v error -i ref.mp4 -vf fps=1,scale=270:-2 frames/f%03d.png \
&& ROWS=$(( ($(ffprobe -v error -show_entries format=duration -of csv=p=0 ref.mp4 | cut -d. -f1) + 5) / 6 )) \
&& ffmpeg -v error -i ref.mp4 -vf "fps=1,scale=180:-2,tile=6x${ROWS}" sheet.png \
&& ffmpeg -v error -i ref.mp4 -vn -ac 1 -ar 16000 ref.wav \
&& ffmpeg -v error -i ref.wav -af "asetnsamples=16000,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=loudness.txt" -f null - \
&& python3 - <<'PY'
from faster_whisper import WhisperModel
m = WhisperModel("small")
segs, info = m.transcribe("ref.wav", vad_filter=False, word_timestamps=True, language=None)
print("language:", info.language)
segs = list(segs)
for s in segs:
    print(f"{s.start:6.2f} {s.end:6.2f} {s.text.strip()}")
import re
if not segs:
    print("delivery: no speech; measure the cut rhythm and the on-screen text cadence from the frames")
else:
    speech = sum(s.end - s.start for s in segs)
    text = "".join(s.text for s in segs)
    units = len(re.findall(r"[가-힣぀-ヿ一-鿿]", text)) or len(text.split())
    gaps = [b.start - a.end for a, b in zip(segs, segs[1:])]
    print(f"delivery: speech {speech:.1f}s of {info.duration:.1f}s ({speech / info.duration:.0%}), units {units}, rate {units / speech:.1f}/s, lines/10s {len(segs) / info.duration * 10:.1f}, longest gap {max(gaps) if gaps else 0:.2f}s, hook window {segs[0].end:.1f}s")
PY
curl -f -X PUT -H 'Content-Type: <the content type the media_upload result names>' --upload-file sheet.png '<upload_url>'
```

The delivery line is the ground truth for pace ([story.md](story.md) "Density"): a reference that feels calm may speak fast, and the script is written to the number, not the feeling. Whisper's segments stand in for lines; when it merges two lines into one segment, split them by the on-screen captions and recount.

The `tile` filter needs both dimensions, and the rows are computed from the duration so that one sheet holds the whole reference; the PUT carries the `Content-Type` the `media_upload` result names (the shared sandbox page says why). Voice detection is off for the reference: under a music bed it dropped whole lines and returned fragments with impossible timestamps, with the default split and with a 300-millisecond one; set `language` to the reference's language when it is known (the research names it; the ad's language may differ), else leave it for detection. Detection is on only for timing the captions of the master, as [captions.md](captions.md) says. The per-second loudness in `loudness.txt` shows where speech, music and silence are, which the transcript alone cannot.

To look at frames larger than the sheet, pass them in `image_paths` in a short call, or zip the `frames` directory and upload it as a general file for the client to download ([/docs/higgsfield/sandbox.md](/docs/higgsfield/sandbox.md) "Looking at images").

Look at the contact sheet (by its hosted URL, or downloaded where the client can view images) and at individual frames for cast appearance and on-screen text. Frames are the ground truth for text, look and structure; the transcript is the ground truth for dialogue; the scene analysis, when it arrives, adds scene boundaries and descriptions to check the shot list against.

The template's cast section is the source of the cast list and the portraits ([cast.md](cast.md)): it describes people and never identifies one.

## Template

```markdown
# Analysis brief: <reference name>

Duration: <s> · Frame: <w>x<h> (<aspect>) · Language: <code> · Shots: <n>

## Why it works
<The mechanism, not the content. Hook: what stops the thumb in the first two seconds and how (a question, a shock, a face, a claim). Tension: what the viewer wants resolved. Turn: the moment the ad changes direction. Payoff: what the product delivers and how it is shown. Call to action: its wording and timing. Pacing: how cut rhythm carries these. Keep: the mechanism, the medium and the look. Reinvent: the situation, the setting, the cast, the lines.>

## Story engine
<By [story.md](story.md) "Reading the reference". Form: on-camera dialogue, a narrator over pictures, a testimonial, a demo. Genre and register: the kind of story, the conventions it borrows, its tone words, the words it never uses. Rule of the world: one sentence, "In this world, ...". Device: the concrete thing that carries the rule, where it appears, whether it returns. Figure: who holds authority and how the story proves it. Signature line: the quotable line, verbatim. Reveal: the last fact, and the sentence the viewer thinks after it.>

## Information order
| # | Line (as spoken) | Adds | Withholds | Mark |
|---|---|---|---|---|
| 1 | ... | a legendary figure did one odd thing for one person | why | hook |
<Marks: hook, rule, exception, question, answer, reveal, CTA. The order is what the new story keeps.>

## Delivery
Speaking time: <s> of <runtime> (<share>) · Units: <n> (syllables or words) · Rate: <n>/s · Lines per 10 s: <n> · Longest pause: <s> · Hook window: <s> · Picture: <still, slow moves or cut on every line>
<From the sandbox pass's delivery line. The script of the new ad is written to these numbers ([story.md](story.md) "Density").>

## Medium and look
<Live action, 2D animation, 3D animation, stop motion or mixed, and the style in the words an image model follows: line (clean, sketchy, none), color and shading (flat, cel, painterly), backgrounds (painted, photographic), light, camera (static, slow pans, handheld), how faces are drawn, and how flat or rich the finish is (say "flat cel shading, no painterly rendering" when the reference is flat: image models default to a richer finish). This becomes the style line of phase 3.>

## Mood and pacing
<Two or three sentences: tone, energy, color, camera style, cut rhythm.>

## Shot list
| # | In–out | What is on screen | Beat (what the viewer feels, and why) | Camera | Cut or move | Build route |
|---|---|---|---|---|---|---|
| 1 | 0.0–2.1 | ... | discomfort: a question the viewer has heard too | handheld close-up | hard cut | generate |

## Dialogue (as spoken)
| # | In–out | Speaker | Transcript |
|---|---|---|---|

## On-screen text and captions
| In–out | Text | Kind (caption / title / sticker / price / CTA) | Position | Look (family class, weight, case, outline, color, motion) | Build route |
|---|---|---|---|---|---|

## Cast
<One entry per person: apparent age range, build, hair, skin tone, clothing, expression, role; in an animated reference, how the style draws people (proportions, line, eyes). Descriptive only; never identify a real person.>

## Sound design
<Music: yes/no, genre, where it starts. Effects: list with timing. Silence or room tone. Voice: on-camera, voice-over, or none.>

## Inserts and effects
<Picture-in-picture, product shots cut in, zooms, freeze frames, transitions. Each with a build route.>

## Build routes summary
Generate: <shots>. Edit: <elements>. Drop: <elements, with why>.
```
