# Tool notes: how the tools behaved

What runs of this skill met in the review and in the render, by topic, with the day where a fact can go stale. What holds for any page the agent writes and renders (the host's preview and its server, the cached image reader, ES modules, `playwright-core` and the waits, fonts) is in [rendering-html.md](/docs/browser/rendering-html.md), included with this skill, and in [headless.md](/docs/browser/headless.md); this page holds what this skill's own slides met.

## Reading the PNGs

A slide judged at native size passed and failed at phone size in one run: a dark night scene and frames of a blurred face read as shapes at a third of the width, and the user's first words were that the slides could not be seen (checked 2026-10); the review reads every PNG at both sizes.

## Fonts

A label or a small heading the spec sets in italic, in a face with no true italic for its script, is set upright in the spec's label color and said at the checkpoint; a condensed width the spec measured, a display face served as a single `.woff` file, and a heavy outline around display type are set as rendering-html.md "Fonts" says.

## Rendering

A body sentence of the spec's maximum characters fit one line at the spec's sizes in a column of the canvas width less the margins; sentences a few characters over wrapped, which the review caught on the PNG and not in the grid, where the scaled slide hides it (checked 2026-10). A source tag placed top-right collided with text inside a photo at the top-right; the tag moved to the bottom-right on that slide. A scaled crop is checked on the PNG: a first guess cut the subject the slide was about. On a format that stacks two 16:9 frames whole on a 4:5 canvas, each frame at the canvas width is 1080 by 607.5 and the two leave 67.5 pixels above and below; the spec's measured margins decided the rounding, and the frames' own logos and captions stayed as the account keeps them (checked 2026-10). A cover made from a picture inside a frame (a photograph shown on a broadcast) was cropped and scaled 1.8 times to fill the canvas and read soft but recognizable; the factor goes in the checklist.
