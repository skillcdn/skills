# The sandbox

`sandbox_exec` is a Linux box with ffmpeg, sox, ImageMagick, Pillow, faster-whisper, Playwright with headless Chromium, curl and two Latin caption fonts, where a Higgsfield skill reads frames, decodes speech, captures pages, cuts, burns text and uploads what it made. This page is how it behaves and how every skill uses it; what each skill does in it (its analysis pass, its review, its assembly) is the skill's own.

## Lease and polls

The sandbox is discarded about ten seconds after a foreground call finishes. A background job (`background: true`) holds it for a fifteen-minute lease that short poll calls do not shorten (tool description, checked 2026-10). So:

- Long work runs as a background job: the call returns a pid, a log path and a status path, polled with later short calls (`sleep 20; cat <status path>; tail -n 60 <log path>`). A poll sleeps at most 25 seconds with `timeout_seconds` at most 45: longer polls time out at the transport well under the tool's own 120-second ceiling (a 60-second sleep with a timeout of 100 fails), and a long loop inside one foreground call comes back as "the connector's server isn't responding" while the job keeps running, so that a short command afterwards reads its output. An encode of a whole video plus its uploads exceeds a foreground call. An analysis pass with the speech model's download takes about a minute; the encode of a 30-second piece with its uploads about 50 seconds.
- Files survive between back-to-back calls and within a job's lease; after that the box is new. A speech model loaded within the lease of the previous job is cached; one loaded later downloads again (about a minute, which the log shows, and still within the next take's render time). Start the first warm-up (the model download, the fonts) as a background job while the first take renders. The agent's own shell may lack the speech models; the sandbox runs every decode.
- The sandbox is recycled during a long wait (a take's render). A script that must run after one fetches everything it needs itself.

## Commands, URLs and scripts

A command is at most 16,000 characters (tool description, checked 2026-10), and a presigned URL is about 2 KB, so a set of URLs goes into a file in one call and the script that reads them in the next, back to back. A script longer than a command is written into the sandbox by a heredoc in one call, uploaded from there with `media_upload` as a general file (a `.py` filename, `application/octet-stream`, `media_confirm` with type `file`), which gives it a permanent hosted URL, and fetched by that URL in later calls; it is re-run with environment overrides (a replaced take, new line timings, finalized takes) rather than rewritten. One self-contained script does a whole assembly: fetch takes, fonts and assets; cut, filter, mix, mux, probe; upload.

## Uploads

Outputs are reserved with `media_upload` (the filename and type) before the command that produces them; the result names the presigned URL and the `Content-Type` to send, because the URL is signed with it. The script ends with `curl -f -X PUT -H "Content-Type: <type>" --upload-file <file> "<url>"`; `media_confirm` only after HTTP 200, and the confirmed id is what the library and the log carry. A new reservation for every revision: a second PUT to a URL that already took a file comes back 412 (a re-upload before `media_confirm` has also gone through; count on neither), and a hosted URL is cached on its first fetch, so an overwrite after that stays invisible for about eight minutes and query strings do not bypass it, while an overwrite before the first fetch shows at once. Presigned upload URLs expire in a day; hosted URLs of finished media stay valid across days, so an assembly fetches by URL rather than by media id.

What the upload backend takes: video, images, audio (a `.wav` request may come back as an `.mp3` slot), and general files by filename (`.zip`, `.py`, `.md`). A subtitle file (`.srt`) is refused by the backend's whitelist: the cue text travels in the delivery instead.

## Files in

A hosted link is what the sandbox downloads (`curl -fsSL -o <file> '<url>'`). The user's own files come in through `media_upload_widget` where the client has one, or as links; an agent with a shell and no widget uploads a local file itself (reserve with `media_upload`, PUT from the shell with the named `Content-Type`, `media_confirm`) and uses the hosted URL. In an unattended agent with a tool allowlist that PUT may be refused, because the URL carries a credential: ask for a hosted link instead, uploaded beforehand by whoever can approve; the outputs are uploaded from the sandbox, which needs no local shell. A YouTube link alone feeds no download. A page's text comes from the sandbox's own curl, and a page's screens from Playwright at a phone's width, in the piece's language.

## Looking at images

A short foreground call with `image_paths` returns up to four PNG or JPEG files, 512 KiB in all, to the agent as images (tool description, checked 2026-10). Contact sheets and single frames are looked at this way, within the lease of the job that made them, or after they are made again from the take; a picture verdict is never guessed from text. Where the client cannot show images from the sandbox, a zipped `frames` directory uploaded as a general file can be downloaded and viewed on the client. ffmpeg's `tile` needs both dimensions (`6x0` is rejected, and in a chain of `&&` everything after it is skipped); compute the rows from the duration.

## Fonts

The preinstalled caption fonts (Metropolis, Montserrat) cover Latin only. For Korean, Japanese, Chinese, Cyrillic, Arabic, Thai, Devanagari and every other script, fetch a font under the SIL Open Font License from the google/fonts repository on GitHub (the `ofl/<family>` directory, for example `ofl/notosanskr`; Noto Sans or Noto Serif for the script) or from the Noto releases into a `fonts` directory, pass `fontsdir=fonts` to the `subtitles` filter, and name the family in the style or in `force_style='FontName=<family>'`. `FontName` is the family's English name; the first name record of a Korean font may be its Korean name. A variable font's filename carries brackets, which are URL-encoded in the download address. Check that the download is a font (a few megabytes, not an error page) before using it: a missing font shows as empty or boxed subtitles, not as an error. A glyph the family lacks (a hanja, a symbol) comes from a fallback font of the same classification (Noto Serif KR supplied two hanja that Nanum Myeongjo lacked). Fetch fonts while a take renders.

## ffmpeg and audio

- Encode every segment with the same video and audio settings so the concat demuxer copies streams; a dip to white is two fades around a cut, which it accepts.
- `loudnorm` on a joined file stops with "Cannot select channel layout" until the layout is stated on both sides of it: `aformat=channel_layouts=stereo` before the filter and `-ac 2` on the output. Program loudness: -16 LUFS integrated, -1.5 dB true peak. The takes' audio comes at 32 kHz; resample to 48 kHz.
- A take generated with audio off (`generate_audio: false`) has no audio stream at all. Give it room tone or silence (`anullsrc`, or sox noise low-passed) before concatenation, or the concat drops audio.
- Text is drawn from files with `drawtext` and `expansion=none`, which avoids escaping punctuation in non-Latin text; multi-line layouts are composed as PNG with Pillow and overlaid; a logo is rasterized from its SVG with `rsvg-convert`. ASS styles through the `subtitles` filter render positioned events (name cards, role lines, term cards) without a separate `drawtext` pass. ASS colours are `&HAABBGGRR`, blue first.
- `amix` with `normalize=0` keeps the levels that were set. Sound effects are synthesized with sox (a sine ding, a filtered-noise whoosh) or supplied by the user; keep synthetic accents clear of the first word of a line, because a caption step that finds speech onsets in the loudness curve reads an effect on an onset as speech.
- Work at the takes' native resolution; do not upscale drafts. Output 9:16 H.264 with AAC audio.

The server's bundled `subtitles` workflow spreads cues across pauses, ships no Korean font, burns only white, caps or paper looks, forbids a hand-rolled burn and asks the user about the look; the skills burn with ffmpeg directly, and its rule against a hand-rolled burn does not apply to them.

## Verification beyond ffprobe

The agent cannot play video. A master passes when its duration matches the plan within a second, it has one video and one audio stream at the intended size and rate, per-second loudness (`asetnsamples=16000,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=loudness.txt`) shows speech only in the planned windows, a contact sheet shows every shot in order, and frames sampled at every text moment show the text whole, inside safe zones and over no face. Regions the edit changed (a flash, a replaced take) are decoded again ([`decodes.md`](decodes.md)).
