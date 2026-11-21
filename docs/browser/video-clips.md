# A clip cut from a public video

How a few seconds of a public video (footage of an event, a subject's own upload, a product's demonstration, a site in use) become a short muted clip with its first frame as a poster, and how that clip is laid into a slide or a page the agent rendered. Stills read from a video without a download are [video-frames.md](video-frames.md); this page is the job that fetches the video, cuts it and writes an mp4.

## What it takes

| Capability | Recognize it by | Used for |
|---|---|---|
| A shell | A tool that runs a command and returns its output | Everything below |
| ffmpeg | `ffmpeg -version` exits with 0. Look for it in this order: the path a variable of the environment names (the helper below reads `FFMPEG`), the shell's path, a static build that a package of the project brings (npm's `ffmpeg-static` did, checked 2026-11) | Probing, the frame sheet, the cut, the poster, the composition |
| A downloader for page videos | An open-source command that reads a page's video and its metadata without signing in; `yt-dlp` read the watch pages of the large video platforms, social posts and news pages (checked 2026-11). `yt-dlp --version` prints the day of its release | A video that sits in a page's player |
| A headless browser | [headless.md](headless.md) | A recording of a site in use |

A missing downloader closes only the route that needs it: say what to add (its release page, or `pip install yt-dlp`) and go on by the others. A missing ffmpeg closes the whole job: the run uses stills, and says so in a line. The sites change their players within weeks and an old downloader fails on the largest of them first, so a failure on a page that plays for a visitor is met by updating the downloader (`yt-dlp -U`, or the package manager that installed it) before the video is given up.

The card-news build skill carries the commands of this page as [`video.example.mjs`](/design/skills/html-card-news-from-brief/scripts/video.example.mjs) (`probe`, `sheet`, `cut`, and the composition its export calls), with ffmpeg as its one dependency.

## Where the video comes from

| The video is | Fetched by | Notes |
|---|---|---|
| In a page's player (a watch page, a social post, a news page) | The downloader, once, into a cache folder of the run outside what is delivered: the metadata first (`--dump-single-json`: title, uploader, duration, the page's canonical address), then the file as mp4, a rendition no taller than 1920 pixels and H.264 where the page offers one (`-f "bv*[height<=1920][vcodec^=avc1]+ba/bv*[height<=1920]+ba/b[height<=1920]/b" --merge-output-format mp4 --no-playlist`; the merge takes ffmpeg) | No cookies and no login: a video that shows only to a signed-in visitor fails with the downloader's own message and is not fetched |
| At a direct media address (`.mp4`, `.webm`) | ffmpeg itself, which reads the range it is asked for from the address | Nothing is downloaded whole |
| A file the user gave | ffmpeg | |
| What a site does on screen (an app's flow, a page that animates) | A recording by the headless browser: a context made with `recordVideo: { dir, size }`, the `size` equal to the viewport, since it is otherwise scaled down to fit 800 by 800 | The WebM is written when the context closes, and its length is not the time waited: a wait of two and a half seconds gave a file of one second (playwright-core, checked 2026-11), so record longer than the range and read the length from the file. Another visitor's name on the page is hidden with CSS before the recording starts |

What cannot be fetched is not worked around: the run goes on with the stills of [video-frames.md](video-frames.md) or with photographs, and says which video it could not reach. The downloaded file is a working file of the run, removed when the run ends; the clip and its poster are what is kept.

## Seeing the video before cutting

`ffmpeg -i <file>` prints the size, the length, the frame rate and whether there is a sound track on its error stream, which is enough without `ffprobe`. A frame sheet shows the whole video in one image: one frame every N seconds, N the length over about forty, each 240 pixels wide and tiled eight to a row (`-vf "fps=1/N,scale=240:-2,tile=8xR" -frames:v 1`), so that frame k, left to right and top to bottom, is at k times N seconds. Read the sheet, pick the range by it, and look at single frames (`-ss <second> -frames:v 1`) at its start and its end, where a scene cut hides between two frames of the sheet.

## Which range

A clip is worth cutting when all of these hold; where one fails, a still of the same scene serves better.

- It shows the thing itself: what the sentence beside it names, moving. Mood footage and a talking head add nothing a frame does not.
- It reads without sound in its first second.
- The range has no scene cut and none of the player's controls, and nothing enters it that a still of the scene would not show (a dialog window, a visitor's name, a number on a signboard).
- The subject stays inside the strip that will be shown for the whole range.
- It is sharp after the cut: the shown strip is near the canvas's size or above it.
- Four to eight seconds reads well. A platform bounds the length (a video in a carousel on one social network: 3 to 60 seconds, checked 2026-11): read the bound from the platform's help page for the kind of post.

The first frame stands for the clip wherever it is shown before it plays (a feed's grid, a share preview): start the range on the frame that should be seen there, after the motion has begun and with the subject in view.

## Cutting

One command: seek before the input (`-ss <from> -t <seconds> -i <source>`), crop, scale down to the canvas's height, drop the sound, encode H.264.

```sh
ffmpeg -y -ss 160 -t 6 -i <source> -vf "crop=<w>:<h>:<x>:<y>,scale=<w2>:<h2>:flags=lanczos" -an -c:v libx264 -preset slow -crf 22 -maxrate 8M -bufsize 16M -pix_fmt yuv420p -movflags +faststart <name>-clip-160s.mp4
```

- Cut to the strip the slide shows, where the slide is known. A clip taken before its slide is chosen (a research that gathers a story's material) keeps the source's ratio, and the composite below crops it. A picture that fills a 4:5 canvas shows a strip of the clip 0.8 times its height wide: the sides outside it are cropped away, with a margin for the position the slide sets. An eight-second clip went from 18 MB to 10 MB that way. A picture shown whole in a box of the page keeps its ratio and is scaled to the box's width.
- The crop also removes what sits at an edge of the source: a browser's bar in a recording, a letterbox band, a broadcaster's mark where the slide does not keep it.
- Width and height are even numbers, or the encoder refuses them.
- A quality two or three steps lower (a higher `-crf`) showed no difference once the platform had encoded the post again. As a shape: five seconds at 1200 by 1180 was 3.6 MB, eight seconds 7.9 MB, seven seconds at 1080 by 600 3.6 MB (libx264 at `-crf 22`, illustrative).
- Name the file by where it starts (`<name>-clip-<from>s.mp4`), so that two ranges of one source do not collide and a citation can be made from the name.

## The poster

The clip's first frame as a JPEG beside it (`<name>-clip-<from>s-poster.jpg`): the picture every still render, thumbnail and contact sheet shows. HD video is BT.709 and a JPEG is BT.601 at full range, so the frame is converted on the way, or the poster's colours differ from the clip's:

```sh
ffmpeg -y -i <clip>.mp4 -frames:v 1 -vf "scale=in_color_matrix=bt709:out_color_matrix=bt601:out_range=full,format=yuvj420p" -q:v 2 -update 1 <clip>-poster.jpg
```

## A clip in a page the agent rendered

A unit of a rendered page ([rendering-html.md](rendering-html.md)) whose picture is a clip becomes an mp4 from three layers, bottom to top:

1. The unit's own PNG, the poster in the picture's place.
2. The clip, scaled and cropped into the picture's box exactly as CSS lays the poster there (`object-fit: cover` at the `object-position`), for the clip's length.
3. Everything the unit draws over its picture (a headline, a gradient, a box, a mark): the unit rendered once more with its picture hidden and its ground transparent, screenshotted with the background omitted, and cropped to the picture's box.

The same three layers serve a picture that fills the unit and one that sits in a box with nothing over it. Three things keep the result true to the PNG:

- ffmpeg reads HD video that carries no colour tag as BT.601, where a browser reads it as BT.709: name the matrix on the way in (`scale=...:in_color_matrix=bt709` for a source 720 pixels high or more).
- Composite in planar RGB (`format=gbrp` on the layers, `overlay=...:format=gbrp`) and convert once at the end (`scale=out_color_matrix=bt709:out_range=limited,format=yuv420p`, with the stream tagged BT.709). An RGB layer laid straight over the video's YUV changed the colour of every flat box.
- The looped PNG never ends, so the overlay that lays the clip on it takes `shortest=1`.

To check the colours, take the mp4's first frame out as a PNG and compare it with the unit's PNG as two stills, region by region: the two agree within a step or two per channel. A comparison made inside one ffmpeg graph reported the same picture as a different one (a PSNR of 17 to 20 dB, where the stills gave 33 to 37).

The output is the canvas's size at 30 frames a second, H.264, no sound, the index at the front (`-movflags +faststart`); `-crf 23` with a ceiling of 6 Mbit/s gave 2.5 MB for five seconds of a full canvas and 1.9 MB for seven seconds in a box (illustrative).

## The frame sheet of the result

One frame a second of the finished mp4, tiled (`-vf "fps=1,scale=360:-2,tile=4xR"`), and every frame looked at: the poster shows the first frame alone, and what enters later is found only here. A window of the footage's own slid in at one edge three seconds into a clip whose poster was clean, and the border of a legend showed in the corner of a map clip until the crop took another thirty pixels off it. On each frame: the unit's text over the subject, an edge that cuts something in two, a thing that entered.

## Running ffmpeg from a script

Pass ffmpeg its arguments as a list from a script file, never as one line of a shell: on Windows a filter with commas inside quotes (a `select` expression, a graph of several chains) typed on a command line lost them and ffmpeg answered `No such filter` (checked 2026-11).

## What a clip records

The page's address, the range in seconds of the source, the clip's own length and size in pixels, who posted the video as the page shows it (the uploader or the channel, and the outlet where it is a broadcaster's) with the day, and what the clip shows. The poster records the clip it is the first frame of. A citation is the address with the range.
