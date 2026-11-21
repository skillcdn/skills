# Video slides

Read when the brief's `images` hold a `video-clip` entry. A slide of a type with one picture may show a clip in that picture's place: the type's anatomy, its text and its edges stay as the spec has them, and only the picture moves. How a clip is fetched, cut and composited is the repository's [video-clips.md](/docs/browser/video-clips.md); this page is what the build does with the clips a brief carries.

## What the brief gives

A clip is an `images[]` entry with `source_kind: "video-clip"`: the mp4 in `img/`, its `url`, its range `from` and `to` in seconds of the source, `seconds`, `px`, `shows` and `credit`. Its first frame is a second entry, a `video-frame` whose `poster_of` names the clip. The poster is the slide's image wherever a still is shown: the PNG, the phone-size copy, the grid. The build takes no clip from a video the brief does not carry: a video the user names at the build goes to the research, and the plan re-enters at its image step when the brief comes back.

## Without ffmpeg, or without a clip

The check before the first message says whether ffmpeg is there. Without it, each clip's poster is placed as a photograph and the post is PNGs: said in one line at the plan checkpoint and in the delivery, with what to install for the next run. A brief with no clip makes a post of photographs, which is a result like any other: nothing more is looked for and nothing is said of video.

## In the plan

- **Which slide.** The cover takes the clip whose first frame shows what the headline names, where the brief has one; each further clip goes on the body slide whose beat it shows. A clip is never placed so that the post has a video: one that shows a mood, or a scene the slide's text does not name, stays out.
- **A cover that reads better still.** The first frame is the post's thumbnail. Where a photograph of the brief reads better at phone size than the clip's first frame, the cover keeps the photograph and the clip moves to the second slide, said at the checkpoint for the user's pick. In an account's folder the policy's Pictures line settles both picks where it speaks of them.
- **Which type.** A type with one picture: cropped full-bleed, or whole in a box of the page. A type that stacks two frames takes stills. The account's text sits where the type puts it.
- **One scene once.** A clip, or a range that overlaps it, goes on one slide, and a scene a clip shows is not used again as a photograph on another.
- **The fields.** The slide takes `image` (the poster) and `video` (the clip) with the treatment and the position a photograph has: `{ "n": 1, "type": "cover", "lines": ["<line one>", "<line two>"], "facts": ["f1"], "image": "img/example-clip-12s-poster.jpg", "video": "img/example-clip-12s.mp4", "treatment": "full-bleed crop", "position": "62% 50%", "legibility": "clear" }`. A video slide is cropped by its position alone: what a scale on the page would push out of a photograph (a mark at an edge, a band) is cut out of the clip.
- **Length.** A video in a carousel runs 3 to 60 seconds on Instagram (checked 2026-11; its help page for carousel posts says the bounds), and four to eight read well on a slide.
- **Credit.** The caption's credit line names a clip as it names a photograph, from the entry's `credit` in the spec's pattern, and `credits.md` adds the range.

## In the page

The poster is the slide's `img`, sized to the picture (the box it covers, or its own ratio where the type keeps a frame whole), and carries `data-video` with the clip's path from the post folder. The export mode takes `overlay=1` beside `slide=N` and then adds the class `overlay` to the body; two rules make that render the layer above the picture on a transparent ground:

```css
body.overlay, body.overlay .stage .slide { background: transparent !important; }
body.overlay .stage img[data-video] { visibility: hidden; }
```

Nothing opaque sits behind the picture inside its box but the slide's own ground. Copy the clips with their posters into `img/`, and [video.example.mjs](../scripts/video.example.mjs) into the post folder beside the export script, which imports it.

## Export

For every slide whose picture carries `data-video`, the export script also writes `out/<post>-NN.mp4` (the canvas's size, the clip's length, no sound) and `out/video/<post>-NN.jpg`, one frame a second of that mp4. The mp4 is the slide's file for posting and the PNG beside it is its first frame. The helper lays the clip in as a rectangle with `object-fit: cover` at the image's `object-position`; a rounded box, or a picture set with `contain` inside a larger element, is not what it composes.

## Review

Open every frame sheet and read every frame, since the PNG shows the first alone. Then these rows, with the skill's verdicts:

| Result | Verdict |
|---|---|
| The account's text over the subject in any frame | Redo: the position moved, or the block where the type allows; else a range in which the subject stays clear of it |
| Something that enters after the first frame (a window, a player's control, a name on screen), a scene cut, or an edge that cuts a thing in two | Redo: a shorter range or a tighter crop, cut from the clip's own file with the helper's `cut` into a new file with its poster, `--offset` set to the clip's `from` so that the range it prints is the source's. The plan names the new file and `credits.md` its range; the brief stays as it is. Where no range is clean, the poster as a photograph |
| A clip, or a range that overlaps it, on two slides; a scene a clip shows used again as a photograph | Redo: one of the two takes another image of its beat from the brief, or goes without |
| A clip outside the platform's bounds | Redo: trimmed inside them; shorter than the lower bound, the poster as a photograph |
| A sound track in an exported mp4 (the export's line says so) | Redo: exported again without it; the helper drops it |
| A cover whose first frame does not show what the headline names | Redo: the range re-cut to start on a frame that does, or the cover takes a photograph and the clip moves to the second slide |
| A flat box or the ground in the mp4's first frame off the PNG's colour by more than a step or two | Redo: composed as video-clips.md "A clip in a page the agent rendered" says |
| A clip that shows a mood and not what its slide names | Redo: a photograph of the beat |
| No mp4 because ffmpeg is missing | Accept: the poster stands as a photograph, said in a line |

Write the frame sheet read and its verdict into `review.md` on the slide's line. The delivery attaches each mp4 with its sheet, or gives their paths.
