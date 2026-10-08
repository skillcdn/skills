# Portraits and first frames

Every person in a Higgsfield video has an approved portrait, and every generated shot an approved still first frame. The portrait keeps a face the same from shot to shot and from run to run; the frame fixes a shot's composition for a fraction of a take's price, so a wrong outfit, setting or expression is caught and redone for that fraction. A skill says who is cast, what it keeps in its own record and what it reuses; this page is the method every skill shares, and the dated notes on the image models.

## Which image models

Find them at run time, never pin them. Two kinds are needed:

```
models_explore  action: recommend  type: image  query: photoreal portrait of a fictional person from a text description, identity reference for video generation, text-only input
models_explore  action: recommend  type: image  query: photoreal scene from reference images (portraits, a place), 9:16, image reference input
```

The first gives the **identity model** for portraits, the second the **reference-capable model** that makes first frames (and sets, where a skill has them) from the portraits. For an animated or stylized look, the identity-portrait models are photoreal and are not used: the reference-capable model makes portraits and frames alike, with the style line in every prompt, and a portrait is the character in front and three-quarter view on a plain ground, in the style; find it with the query below.

```
models_explore  action: recommend  type: image  query: character design of a fictional person in a described 2D animation style, consistent character for image-to-video, text and image reference input
``` When a recommendation returns more than one model that fits, take the cheaper at its lowest setting and name it as a derived setting. Read each model's parameters with `action: get` and lock the cheapest setting it exposes: the lowest `resolution` or `quality`, a `budget` at its minimum; a 1k image is more than the video model needs. Preflight each once with `generate_image` and `get_cost: true` ([`models.md`](models.md)).

The identity model may output a single aspect ratio, ignore the framing in the prompt and return a character sheet (front, back, face) instead of a portrait: a sheet is a better identity reference and is used as it is. Read the video model's `aspect_ratios` and `medias[].roles` before any image is made, so that every image is made in a ratio its role accepts.

## The style line

One sentence that fixes the medium and the look for every image and take prompt: for live action, photoreal, unretouched, natural skin texture, the light, the camera, the grading; for an animated or stylized piece, the style in words an image model follows (line, shading, palette, proportions, "flat cel shading, no painterly rendering" when the reference is flat). Repeated verbatim in every portrait, frame and take prompt, so they match; a portrait prompt may leave out its scene clauses (background, camera). Without it the images drift apart in finish, and a take drifts toward photoreal.

## The portrait prompt

One paragraph, in this order:

1. Framing: head-and-shoulders or three-quarter, eyes to camera, on a plain neutral ground in soft daylight (or a setting and light matching the piece's mood, when the skill wants the portrait to carry it).
2. The person: apparent age range, build, hair (color, length, style), skin tone, the facial features that matter, the baseline expression of the role, one line on how they carry themselves.
3. Clothing and accessories, exactly. They are repeated word for word in every later prompt for that character.
4. The style line.
5. Never: a real person, a celebrity likeness, a logo on clothing, text anywhere in the image.

## Approval

1. One call per portrait, `count` 1, `use_unlim` explicit; the calls may go out together and be collected with one `jobs_wait`.
2. Show each with its hosted link and the description it was made from; "OK" approves all, a change regenerates that one from the edited description, preflighted and recorded in the ledger. The reserve covers one retry per portrait; beyond it, ask.
3. Where the portrait differs from the words (a longer coat, a scar), the portrait wins: update the description and every prompt to match it, so the words and the picture agree.
4. The approved portrait's media id or job id goes into the skill's record (the shot list, the bible).

When the user has given the go-ahead, judge each image against its description yourself (age, hair, clothing, expression; no text; no artifacts) and regenerate at most once within the reserve.

## First frames

One per generated shot, 9:16, from the reference-capable model with the portraits of the people in the shot (and the set, where there is one) as reference inputs, and a prompt of the style line followed by the shot's first-frame description: framing, who stands where, the place, the light, the pose, the starting emotion, and the product image where the product appears. A shot with no character gets a frame too (the setting, the product). Send the frames together, collect them with one `jobs_wait`, and judge them as a set: the right people in the right costume, the place, the framing, the expression, the style held, no legible text, no artifacts. One failed frame is regenerated from the reserve. Checkpoint: all frames in order with one line each on what the shot does from there.

## From frame to take

The frame goes to the video model as `start_image`, the portrait of each person in the shot in the model's reference role where it has one, the style line, the motion, the line and the audio in the prompt; for animation the prompt says that this is a drawn, animated scene whose style holds throughout. Some models fold the start frame into the reference list ([`models.md`](models.md), 2026-10-08): read the echoed parameters of the first take, and when the frame is reference image 1, number the portraits from 2 in every mapping after. A frame belongs to its shot and is never reused.

## Reuse

Keep the media ids of approved portraits (and sets) in the skill's record and in the ledger. A later run for the same brand or series reuses them instead of generating new ones; the agent learns of an earlier run only from the user, from the skill's own files or from the account's media list. A photoreal portrait is at most a reference image, not a portrait, for an animated piece. The user's own images (a drawing, a photo they own) are imported with `media_import_url` and used as references like any approved image; nothing real goes in otherwise: no real person's photo, no brand, no one else's footage.

## Dated notes

- 2026-09-23: the identity-portrait recommendation (Soul Cast) produced only 16:9, took no reference input, ignored the prompt's framing and returned a 2048x1152 three-panel character sheet (full body front, full body back, face) every time, at 0.12 credits each where the preflight had shown a rounded 1. It served as the identity reference as it was; first frames needed a second, reference-capable image model (Nano Banana Pro that day), found with the second query above.
- 2026-10-02: a present-day cut rendered a character with the hair color of their other-period portrait. One portrait per look, with only the look's portrait among the cut's references, keeps it from happening; a continuity clause in capitals at the top of the prompt fixed it in the retry.
- 2026-10-08: a drama's portraits came back as character sheets again, and one of six first frames was redone; the frames held three characters' faces and two sets across six cuts.
