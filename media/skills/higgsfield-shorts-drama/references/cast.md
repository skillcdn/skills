# Portraits, sets and first frames

Every character has an approved portrait, every recurring place an approved set image, and every cut an approved first frame. The portrait keeps a face the same from cut to cut and from episode to episode; the frame fixes a cut's composition for a fraction of a take's price. Nothing real goes in: no real person's photo, no brand, no one else's footage. The user's own drawings or generated images may be imported with `media_import_url` and used as references like any approved image.

## Which image models

Find them at run time, never pin them.

```
models_explore  action: recommend  type: image  query: photoreal portrait of a fictional person from a text description, identity reference for video generation, text-only input
models_explore  action: recommend  type: image  query: photoreal scene from several reference images (portraits and a place), 9:16, image reference input
```

The first gives the portrait model, the second the reference-capable model that makes sets and first frames. For a stylized look (the bible names animation), the identity-portrait models are photoreal and are not used: the general reference-capable model makes portraits, sets and frames alike, with the style line in every prompt. When a recommendation returns more than one model that fits, take the cheaper at its lowest setting and name it as a derived setting. Lock each model's cheapest setting (the lowest `resolution` or `quality`, a `budget` at its minimum; a 1k image is more than the video model needs), and preflight each once.

The identity model may return a character sheet instead of a portrait, or ignore the framing; a sheet is a better identity reference and is used as it is. Read the video model's `aspect_ratios` and reference roles in phase 3 so that every image is made in a ratio its role accepts.

## The style line

One sentence in the bible that fixes the medium and the look for every image and take prompt: photoreal, unretouched, natural skin texture, the light, the camera, the grading of the period or world. Repeated verbatim in every portrait, set, frame and take prompt; a portrait prompt may leave out its scene clauses.

## Portraits

One per character and look, on a plain neutral ground, head and shoulders or three-quarter, eyes to camera, in the character's main costume of the episode, with the baseline expression of the role. A costume change inside the episode (night clothes, then a wedding dress) is not a new look: the frame and the clothing clause of each cut carry it, and the portrait stays. The prompt, in this order: framing; the person (apparent age range, build, hair, skin tone, the features that matter, how they carry themselves); clothing and accessories exactly, repeated word for word in every later prompt; the ground and the light; the style line; never a real person, a celebrity likeness, a logo or text. A character who appears in two periods or states (a past life, a transformation, a disguise) gets one portrait per look, named apart, and a cut's references carry only the look of its period.

One call each, `count` 1, `use_unlim` explicit; the calls may go out together and be collected with one `jobs_wait`. Show each with its link and the description it came from; "OK" approves all, a change regenerates that one from the edited description, one retry each in the reserve. Where the portrait differs from the words (a longer coat, a scar), the portrait wins: update the bible and every prompt.

## Sets

One image per recurring place or object: the room, the edge, the hall, the ring. Wide, empty of people, in the style line, in the look of the period. A set is a reference input for first frames; the video model gets the frame, not the set.

## First frames

One per cut, 9:16, from the reference-capable image model with the portraits of the characters in the cut and its set as reference inputs, and a prompt of the style line followed by the cut's first-frame description: framing, who stands where, the place, the light, the pose and the starting emotion. A cut with no character gets a frame too. Send the frames together, collect them with one `jobs_wait`, judge them as a set: the right people in the right costume, the place, the framing, the expression, the style held, no text, no artifacts, no character seeing what they must not. One failed frame is regenerated from the reserve. Checkpoint: all frames in order with one line each on what the cut does from there.

When the user has given the go-ahead, judge portraits, sets and frames yourself against their descriptions and regenerate within the reserve (one retry per portrait and per set, one frame per three cuts); beyond it, ask.

## Reuse across episodes

The bible's production notes carry the media id or job id of every approved portrait and set. The next episode reuses them and generates only what is new (a new character, a new place, a new look). A frame is never reused; it belongs to its cut.
