# Frames of a public clip

How stills of a public video (a broadcaster's clip of a report, footage an article cites, an ad's video) are taken for a brief, a breakdown or a reference, without downloading the video, by the route the agent has. The frames are working files of the run: nothing of the clip is kept beyond them, and the delivery cites the clip's address and the time of each frame.

## Routes

| Route | Needs | Gives |
|---|---|---|
| A watch page in a headless browser | A shell with Node.js, `playwright-core` and a Chromium-family browser ([headless.md](headless.md)) | Frames every few seconds of video, named by time code, with the served size, as files; a clip of minutes in minutes |
| A direct media address with ffmpeg | A shell with `ffmpeg` and `ffprobe`, and an address that serves the file to a plain request | A contact sheet of the first seconds and one of the whole clip, or one frame at a second, one command each; no copy of the video |
| A driven browser | The video's own address or its watch page in a tab ([driven-browser.md](driven-browser.md)); a script in the page, or pause and screenshot | Frames drawn side by side over the page and read from one screenshot, or screenshots at chosen seconds; kept as files only where the host saves screenshots |
| None | | The clip listed as a source by its address; the delivery says the frames were not taken |

The watch page of a public video platform answers a headless browser and a driven browser; a direct media address (a file behind a signed URL, as some libraries give) answers ffmpeg and a plain request. Nothing is signed in to, and a clip that needs a consent, an age gate or a check that does not pass by itself is listed, not captured.

## A watch page in a headless browser

- Use the platform's watch page, not its embed page: the embed refused to play in the same browser with a player configuration error (checked 2026-10).
- Launch with autoplay allowed (`--autoplay-policy=no-user-gesture-required`), a viewport of 1280 by 720 at device scale 1.5 for 1920 by 1080 files, wait for the `video` element, play it muted, and wait out an advertisement, taking frames only while none is showing. The player marks an advertisement with a class name, which drifts (checked 2026-10): read one page's elements when it changes.
- Move the `video` element to a fixed box over the page at the viewport's size, `object-fit: contain`, over a black backdrop, and screenshot clipped to that box. The player rewrites the element's inline size when it lays itself out again: pin the size before every capture and drop a frame shot during a relayout, or a frame fills two thirds of the file with black beside it (checked 2026-10).
- Play at normal speed. A stall (no progress for fifteen seconds while no advertisement shows) is met by one reload of the watch page at the time reached (its `t=<seconds>s` parameter), as a viewer would reload; a clip that stalls again is listed as a source with the frames taken so far. A raised rate stalled after about a minute (checked 2026-10).
- Choose the highest quality the player's own menu offers (its API sets the same) and record what was served: 1080p asked, 720p served on a short clip (checked 2026-10). The served width by height, read from the element, is the frame's size for any judgement of legibility, not the file's.
- Name each frame by its time in tenths of a second (`t00120.jpg` is 12.0 seconds, so `t=12s` in the citation) and append one line per frame (seconds, served size, file) to a table beside them; a rerun gets an empty folder.
- "frames 0" with no other output means the player never readied: a consent page, a check, an age gate. List the clip as a source and stop.
- The card-news research skill carries all of this, written against the largest video platform's watch page, as [`video-frames.example.mjs`](/marketing/skills/web-card-news-topic-brief/scripts/video-frames.example.mjs); for another platform's player, port its logic (pin, capture, reload on a stall) and not its selectors.

## A direct media address with ffmpeg

`ffmpeg` reads the address itself, so no copy of the video is kept: a sheet of the first seconds (`-t 3`, a few frames a second, tiled, wide enough to read words on screen), a sheet of the whole clip (one frame every N seconds, N the duration over the number of tiles, tiled in rows), and one frame at a second for small print, each one command with `-frames:v 1`; `ffprobe` gives the duration. One request at a time, as with pages. A sheet that was made and not looked at was not read: the breakdown names the sheets it comes from. The Meta Ad Library creative research skill carries the commands and the sizes that read in [`creative-analysis.md`](/marketing/skills/meta-ad-library-creative-research/references/creative-analysis.md) "Deep read".

## A driven browser

- Open the video's own address, or its watch page, in a tab. A script in the page pauses the video, seeks to the chosen seconds, draws each frame onto a canvas fixed over the page in the grid that shows them largest, and one screenshot reads them; the creative research skill carries the script in the same section. Two screenshots read a video (the first seconds, then the whole); a third enlarges a band for small print. Frames are not kept on this route unless the host saves screenshots to files, and the delivery says so.
- Where no script can run: pause the player and take a screenshot at the chosen seconds (the first three or four for a hook; the scenes a brief names; a few later moments), noting the time of each.
- Where the host saves a screenshot to a file: play, pause, save, note the time, which is the hand-stepped way to keep frames.

## What a frame records

The clip's address with the time, the served size, the text printed on the frame as printed (a subtitle, a name card, a graphic), the publisher as the clip shows it (a broadcaster and its program, a channel) and the clip's publication date; where the clip names the footage's origin (a viewer's camera, a subject's own channel, a public body), that origin. A frame of a re-enactment, an illustration or generated imagery inside the clip, labelled as such on screen, is not a photograph of the event and is marked. Faces the publisher blurred stay blurred, and a frame that is blur or mosaic alone shows nothing. What a frame may be used for, and what its caption may be taken to state, is the reading skill's rule.
