# Layouts: the spec's slide types as the page's classes

A post is composed from the reference account's own slide types, as the format spec measured them, and from nothing else: this skill carries no layouts of its own. The spec's `cover`, `slide_types` and `elements` are the classes of the page, their anatomy the CSS, the spec's `kinds` the sequence, `variants_by_content` the choice by content and `never` the limits. A build that composed slides from a catalogue of the skill's own, with the spec only adjusting its defaults, was sent back twice as "not the format": the user holds the result against the account's posts, and a type the account does not use is the first thing they see, before any sentence is read.

## From the spec to classes

| Spec field | Becomes |
|---|---|
| `canvas.size` | The slide box |
| `cover` | The `.cover` class: the photo treatment; the label's position, color, weight and italic where the cover has one (its words are the user's own label or a category word, never the account's series name); the headline's lines, size, weight, color, stroke or shadow where the spec records one, and its top and bottom edges; the cover `variants` as modifier classes |
| `slide_types[]` | One class per type, named as the spec names it: the photo treatment (full-bleed and cropped; whole with its marks and the margins the spec measured around it; two photos stacked or side by side; flat color), the gradient or dim overlay with its darkness, each text block at its measured edges with its size, weight, color and line height, and which text on the slide is the account's own and which belongs to the material shown |
| `elements[]` | A class that rides on the types the spec names: a note, an inset, a talk box, a source tag, a source card, at its measured place, in the corner or the area the spec gives it and away from text inside the photo |
| `fonts`, `colors` | The stylesheet links or `@font-face` rules and the CSS variables; a font the spec marks `guess` is the closest free face it names, loaded from the path it gives |
| `density` | The counts each block of the account's own text is written to (script.md) |

A value the spec marks `estimate` may move where the render shows text unreadable; the checkpoint says by how much. A measurement the spec lacks for a type (no vertical edges, no line height) is taken from the study's `slide-log.md` where it sits beside the spec, else set so that the block sits where the type leaves room, and said at the checkpoint.

## Photo treatment

The type's `anatomy.photo` decides how an image is placed (with `frames_per_slide`, `frame_edges`, `marks_kept` and `background` where the type keeps frames whole), and the licence decides what may be done to it:

| The type's photo is | The image is placed |
|---|---|
| Full-bleed, cropped to the canvas | `object-fit: cover` at the object position that keeps the subject; a mark, a logo or a credit at an edge cropped out by a scale transform with its origin away from the mark, by only as much as the mark needs, checked on the PNG; the type's gradient or dim over it |
| Whole, with its marks (a captured frame of a broadcast or a post with the broadcaster's logo, labels and captions, in the margins the spec measured) | At its own ratio, uncropped, at the spec's edges; its marks stay, because the account keeps them; nothing of the account's is drawn over the material's own text |
| Two images | Stacked where the type stacks them, side by side where it sets them beside each other, exactly as many as the type holds; a frame left over goes on a one-frame type the spec has, else into the caption's sources, said at the checkpoint; each treated as above |
| Flat color or none | The spec's color |

An image whose licence forbids modification takes no crop, overlay or gradient whatever the type: whole at its own ratio on the spec's `background` color, else its darkest measured color (its dim or gradient value), else black, said at the checkpoint, or not at all. An image whose terms are unknown is treated as the type treats its photos, with its credit.

## Choosing a type for a beat

1. The build: in the spec's `kinds`, the kind of post first, read from the brief (SKILL.md "Inputs"); among its builds, the one whose `text_on` matches what the brief's images carry (captioned frames take the build told by the material's captions, photographs with nothing written take a build of the account's sentences); where two still fit, the one whose slide range holds the beats. Its `typical_order` is the starting sequence.
2. The cover is the spec's cover, in the variant whose `for` names the post's kind or build, else the plain cover.
3. Each other beat takes the type whose `carries` names what the beat is (one step in sentences, a photo with nothing to add, two related photos, a list, a date, a quote, a captured frame whose own caption is the beat), `variants_by_content` deciding where the account uses a particular type or element for that content.
4. A beat the spec has no type for takes the nearest type the account has for content of that shape, said at the checkpoint; never a type the account does not use. Where the nearest type carries text of the account's and the beat has none, the beat is that type's photo alone.

## Variation

Variation is the account's, read from the spec. Where the build's `order` is `varies`, its `typical_order` is a starting sequence and not a rule: the plan stays within the build's set of types and its count, and differs from each `post/slide-plan.json` of the brief folders beside this one that names the same spec in at least two slots, compared by position, a slide past the shorter plan's count counting as a difference. Where `order` is `fixed`, the sequence is the `typical_order`. Where the account's build repeats one type slide after slide (a stack of captured frames), the plan repeats it the same way, and nothing is varied to look less repetitive: the repetition is the format. A type repeated where the account varies, or varied where the account repeats, is the review's first verdict.

## With no spec

The build needs the study first; say so and offer it. A user who wants slides anyway, with no account to follow, gets the stand-in in [no-spec.md](no-spec.md), said to be one at every checkpoint and in the delivery.
