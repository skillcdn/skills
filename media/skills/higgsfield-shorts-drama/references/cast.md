# Portraits, sets and first frames

Every character has an approved portrait, every recurring place an approved set image, and every cut an approved first frame. The method every Higgsfield skill shares (which image models and how they are found, the style line, the portrait prompt, the approval loop, how a frame becomes a take, reuse by id) is in [/docs/higgsfield/cast.md](/docs/higgsfield/cast.md); this page is what a series adds. Nothing real goes in: no real person's photo, no brand, no one else's footage. The user's own drawings or generated images may be imported with `media_import_url` and used as references like any approved image, and one may stand as a character's approved portrait; a photo of a real person is not used.

## Models for a series

The identity model makes the portraits, and the reference-capable model makes the sets and the first frames from several reference images at once (the portraits of the characters in the cut and its set). For a stylized look (the bible names animation), the reference-capable model makes portraits, sets and frames alike, with the style line in every prompt. Each is found at run time with `models_explore` (`recommend`, type `image`, a query in words of what it must take and make; the shared page has the queries), locked at its cheapest setting and preflighted once. The style line is the bible's. Read the video model's `aspect_ratios` and reference roles in phase 3, so that every image is made in a ratio its role accepts.

## Portraits: one per character and look

In the character's main costume of the episode, with the baseline expression of the role, named by the key the reference table gives it. A costume change inside the episode (night clothes, then a wedding dress) is not a new look: the cut's first-frame description names the clothing and its prompt repeats it as the clothing clause, while the portrait stays and its own clothing is repeated in every other cut, as the shared page says. A character who appears in two periods or states (a past life, a transformation, a disguise) gets one portrait per look, named apart, and a cut's references carry only the look of its period: a cut that carried both looks once rendered the wrong hair. Where the portrait differs from the words (a longer coat, a scar), the portrait wins: update the bible and every prompt.

## Sets

One image per recurring place or object: the room, the edge, the hall, the ring. Wide, empty of people, in the style line, in the look of the period. A set is a reference input for first frames; the video model gets the frame, not the set.

## First frames

One per cut, 9:16, from the reference-capable model with the portraits of the characters in the cut and its set as reference inputs, and a prompt of the style line followed by the cut's first-frame description: framing, who stands where, the place, the light, the pose and the starting emotion. A cut with no character gets a frame too. Judged as a set, as the shared page says, and besides: the right costume for the moment, and no character seeing what they must not. Look at them as one sheet: tile the frames with ffmpeg in the sandbox and pass the sheet through `image_paths`, at most four files of 512 KiB in all per call ([/docs/higgsfield/sandbox.md](/docs/higgsfield/sandbox.md) "Looking at images"); a portrait sheet of 2048x1152 is scaled down the same way.

When the user has given the go-ahead, judge portraits, sets and frames yourself against their descriptions and regenerate within the reserve (one retry per portrait and per set, one frame per three cuts); beyond it, ask.

## Reuse across episodes

The bible's production notes carry the media id or job id of every approved portrait and set. The next episode reuses them and generates only what is new (a new character, a new place, a new look). A frame is never reused; it belongs to its cut.
