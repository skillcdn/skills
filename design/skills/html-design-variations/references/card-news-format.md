# A card news format: what this skill's inputs and phases take

Read before the first message when the unit is a card news format. The seam is written in the variation set's [handoff.md](/docs/variation/handoff.md) "A card news format" (the start, the crowd, the unit, the distance, the handoff) and in [format-spec.md](/docs/card-news/format-spec.md) (the routes to a spec, and what a designed spec holds): read both now. This page says only where they enter this skill's run.

## Inputs

| Input | For a card news format |
|---|---|
| The design to vary | The format's cover and one body slide, as handoff.md "The unit" says. |
| The start | A format spec from [instagram-card-news-format-study](/design/skills/instagram-card-news-format-study/SKILL.md): the reference's, measured, by default, or the genre's common form where no account could be read, thin where it was read from samples and absent where the study found none; each field it lacks is filled from the build's stand-in, as handoff.md "The start" says. With no spec at hand, the study runs first, on the reference the request names or on the genre. The posts are read by the study, never by this skill. |
| The distance | As axes.md says for the route; a request for less or more text moves the density too, which otherwise holds at the start's. A palette or a typeface the user names is held by every look, and the looks move the other axes. |
| The words on it | The topic brief's working headline in the start's headline style, and one beat's facts written here as sentences at the start's density, with the brief's cover image and that beat's image; the build writes the post's own sentences later. Without a brief, the request's words. |
| The medium's size | The cover and the body slide at the spec's canvas, judged on the feed-width copy as a post is, with the spec's own type sizes, since its density is the start's. |
| Where the run goes | The run folder as for any unit; the designed spec goes to `card-news/<the format's name>/` beside the brief folders. |

## By phase

- **Phase 1.** The crowd is the genre's spec where the study read one, as handoff.md "The crowd" says.
- **Phase 2.** A slide type the measured format never uses, where the request asks for a slight change, and an imagery the brief does not hold are not positions: the build places only the brief's images. The look names the font family, since the build only reads `fonts`: the start spec's web font where type is held, else a free web font of the class with its documented path.
- **Phase 3.** Where the brief has fewer pictures than beats, the post will have slides of text alone: the look renders that slide type as a third file, so that the build does not meet it first. Two files per look, `look-<n>-<name>-1-cover.html` and `look-<n>-<name>-2-slide.html`, each one box at the canvas size with the spec's margins in place of the skeleton's page; the narrow-width rule gives way to the feed-width copy. Shoot them at the canvas with `--no-phone`, so that the sheet pairs them row by row. The family a look names is loaded from its documented path. The one beat is among the words the run writes itself.
- **Phase 4.** Each look is judged on its feed-width copies, each copy opened, not the sheet's tiles.
- **Phase 6.** Beside `handoff.md`, write the designed `format-spec.json` and `style-notes.md`, as handoff.md "The handoff" says. [html-card-news-from-brief](/design/skills/html-card-news-from-brief/SKILL.md) reads them next, in the run that offered the route; where the looks were asked for directly, the delivery names it as the next step, with [web-card-news-topic-brief](/product/skills/web-card-news-topic-brief/SKILL.md) before it where there is no brief.
