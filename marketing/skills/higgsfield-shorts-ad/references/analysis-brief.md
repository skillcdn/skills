# Analysis brief

The artifact of phase 2. Fill every section; write "none" rather than leaving a section out, so the user can see what was looked for.

## Sandbox pass

Run in one `sandbox_exec` call, started with `background: true`, while `video_analysis_create` is processing. `<url>` is a link the sandbox can download: the original link when it points straight at a media file, otherwise the hosted URL of the confirmed upload or import (`show_medias` with type `video` lists it). Before the call, reserve an upload for the contact sheet with `media_upload` (filename `sheet.png`) and put its `upload_url` on the last line, so the sheet can be looked at by its hosted URL after `media_confirm`. The call returns a pid, a log path and a status path; poll them with a later `sandbox_exec` (`sleep 20; cat <status path>; tail -n 60 <log path>`). Keep each poll short: a `sleep` of at most 25 seconds and `timeout_seconds` of at most 45, because longer polls time out at the transport before the tool's own limit. The pass takes about a minute, the Whisper model download included.

If `video_analysis_status` still says queued after about five minutes, do not wait for it: build the brief from the frames and the transcript, poll it again between later phases, and fold the scene analysis in if it arrives. The frames are the ground truth for look and text in any case.

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
speech = sum(s.end - s.start for s in segs)
text = "".join(s.text for s in segs)
units = len(re.findall(r"[가-힣぀-ヿ一-鿿]", text)) or len(text.split())
gaps = [b.start - a.end for a, b in zip(segs, segs[1:])]
print(f"delivery: speech {speech:.1f}s of {info.duration:.1f}s ({speech / info.duration:.0%}), units {units}, rate {units / speech:.1f}/s, lines/10s {len(segs) / info.duration * 10:.1f}, longest gap {max(gaps) if gaps else 0:.2f}s, hook window {segs[0].end:.1f}s")
PY
curl -f -X PUT -H 'Content-Type: image/png' --upload-file sheet.png '<upload_url>'
```

The delivery line is the ground truth for pace ([story.md](story.md) "Density"): a reference that feels calm may speak fast, and the script is written to the number, not the feeling. Whisper's segments stand in for lines; when it merges two lines into one segment, split them by the on-screen captions and recount.

The `tile` filter needs both dimensions on the sandbox's ffmpeg (`6x0` is rejected, and because the command is one chain, everything after it would be skipped); the rows are computed from the duration so that one sheet holds the whole reference. The PUT carries the `Content-Type` the `media_upload` result names, because the presigned URL is signed with it. Voice detection is off for the reference: under a music bed it dropped whole lines and returned fragments with impossible timestamps, with the default split and with a 300-millisecond one; set `language` when the product page gave it. The takes are clean speech and are decoded with detection on, as [captions.md](captions.md) says. The per-second loudness in `loudness.txt` shows where speech, music and silence are, which the transcript alone cannot.

To look at frames larger than the sheet, zip the `frames` directory and upload it as a general file (`media_upload` with a `.zip` filename, PUT with `Content-Type: application/octet-stream`, `media_confirm` with type `file`); the client downloads it and views the images.

Look at the contact sheet (by its hosted URL, or downloaded where the client can view images) and at individual frames for cast appearance and on-screen text. Frames are the ground truth for text, look and structure; the transcript is the ground truth for dialogue; the scene analysis, when it arrives, adds scene boundaries and descriptions to check the shot list against.

The frames, the sheet, the audio and the imported reference are for looking and listening only. None of them is ever passed to a model as a start frame, a reference, a motion source or an audio source, and none appears in the output. The cast section below is the source of the cast list and the portraits ([cast.md](cast.md)); it describes, it never copies.

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

## Intake

Ask only for what the request did not give and what cannot be found:

1. The product: a link to its site or page, or a name and one sentence about it.
2. The reference video: a link straight to a media file, or a local file through the upload widget where the client has one. An agent with a shell and no widget uploads a local file itself: reserve with `media_upload` (the file's name and type), PUT the file from the shell with the `Content-Type` the result names, `media_confirm` it, and use the hosted URL (`show_medias`, type `video`) as the link the sandbox downloads. A YouTube link alone is not enough: it feeds the scene analysis but not the frames or the transcript. Short is better; analysis accuracy drops with length. When the request has none, it is found before it is asked for ("When there is no reference" below), and asked for only when nothing at hand can find one.

The message is short: the one or two things needed (for the reference, that the link must lead straight to a media file), one line on what happens next (the reference is analyzed, then a plan with its cost is shown), and nothing else. Never ask about language, length, captions, cast, setting, images or budget. Those are derived and shown at the plan checkpoint, where the user can change any of them. When the request already has both, there is no intake message at all.

## When there is no reference

A user who names only the product still gets an ad built on what works: the reference is found among the ads now running for that kind of product. A skill that researches running ads does the finding (in this collection `meta-ad-library-creative-research`, which reads the Meta Ad Library), and this skill chooses from what it returns. Say in a line that a reference is being looked for and that the user's own is welcome at any point. With no such skill at hand, ask for the reference as "Intake" says and name the skill that would find one.

1. **Research.** Run the research skill with the product as its subject, through to its delivery. Its method, its limits and its checkpoint are its own: none of it is repeated here, and none of it is cut short because an ad comes next.
2. **Choose** among the videos on its shortlist, in this order:

| Step | Rule | Why |
|---|---|---|
| Candidates | The shortlisted videos whose frames the research looked at (its report says which). Nothing off the shortlist, however well it fits. | The reference teaches a video's hook and pacing, and the shortlist is where proof was checked. |
| Honest | Drop a mechanism that rests on what the product lacks: a creator's or a customer's own experience of it, a before and after, a number or an offer its page does not state. | The ad may say only what the product's page or the user says. An invented experience is a false claim. |
| Fit | Take the candidate whose mechanism the product can carry most fully with what its own page has: its claims, its persona, its story, its reviews, its images. | What transfers is the mechanism. A reference that fits half-way leaves the ad leaning on its surface. |
| Proof | Between two that fit alike, the one the research gives the stronger proof, and one it ranks as working now before an old one it keeps as a benchmark. | Fit chooses among proven ads; it does not replace proof. An old ad shows that its mechanism lasts, and is the one its viewers have seen longest. |
| Cost | Then the shorter video, with fewer people and places. | A take is paid by the second, and every person and place adds shots. |

3. **Say what the choice rests on.** The plan checkpoint opens with the reference (the advertiser, its library link), its proof, its weak signs, why the product can carry it, and the runner-up with what it would have given instead. The weak signs are read from its record even when the research's breakdown names none: a single use, a low place among its advertiser's own ads, an old ad kept only as a benchmark. A choice that passes over the ads the research ranks as working now says in a line what they lacked. The user can pick another, or send their own, before anything is paid for. When no candidate fits, do not force one: say which came nearest and what the user would have to supply for it (a real customer, a result that can be shown), and stop for their choice.

From the chosen reference on, the phases run as for any reference, with these differences:

- **The address is the link.** The video's address is in the research's record of that ad, and the sandbox downloads it as it is. It expires within days: run the sandbox pass in the same run, and once it has expired have the research skill load that ad again for a fresh one.
- **The breakdown is a first look, not the brief.** Frames the research made may stand in for the pass's own when they cover the whole reference; the transcript and the delivery are measured here, and every section of the template is filled.
- **The readings feed the concept.** Keep the mechanism that shows proof. Leave the surface the market crowds: the opening, the proof shot and the offer line that most of its ads share. Take the open angle where the product's own world covers it.
- **The reference is a competitor's ad.** Its viewers may see the new ad too, so the plan says what the ad keeps (the mechanism, the medium, the look in kind) and what differs at a glance: the cast, the first frame, the colors and the type, the device, every line. A line that is the reference's with the words swapped is rewritten, the hook and the closing line first: the odd act and the last turn of phrase must be the product's own, not the reference's with another year, another seller or another verb.
- **It speaks after its turn.** A direct-response ad names the product, the offer and a call to action after its story turns. The new script keeps those marks in the reference's order ([story.md](story.md) "Writing the new story", step 7), in the product's own words and with only an offer its page states.

## Product brief

From the product page (or the user's sentence), record:

- Name, what it is, who it is for: one line each.
- The tagline, if any, verbatim.
- The claims the page makes, as a short list. Only these, or what the user states, may be spoken in the ad.
- The page's language, which becomes the dialogue and caption language.
- The page's type and colors: font families from its stylesheet, the ground, text and accent colors, the logo's clear space ([design.md](design.md)).
- Images: the logo, one product image, and the photo of any person the site presents as the brand's own (a founder, a face of the brand, a mascot). Fetch the page in the sandbox (`curl -sL '<url>'`), read the `og:image` tag and the `img` sources whose path, alt or class mentions logo, product, hero, portrait or the product's name; download the candidates, look at them, and keep what serves: a logo for the end card and overlays, a product image for overlays and as a product reference where the video model takes one, a person's photo for casting ([cast.md](cast.md)). Import them with `media_import_url`. They are the advertiser's own assets and may be used as they are or as references; nothing is taken from any other site.

A text-only web tool gives the words; the images need the sandbox. Without either, ask the user for two lines about the product and go on without images.
