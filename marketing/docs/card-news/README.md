# Card news: what its skills share

The skills that make card news in a reference account's format (`instagram-card-news-format-study`, `web-card-news-topic-brief`, `html-card-news-from-brief`) pass two artifacts between them: a **format spec**, measured from a reference account's posts, and a **topic brief**, the sourced facts and the images of one story. The shape of each lives here once, so that the skill that writes it and the skill that reads it agree without restating each other. Each skill carries its own method (how posts are read, how facts are sourced, how slides are composed and rendered) and its own rules.

| Document | Holds | Read |
|---|---|---|
| [`format-spec.md`](format-spec.md) | The fields of a format spec: canvas, slide types and their anatomy, density, register, caption conventions, what the account never does, fonts and colors, and how each field is measured and used. | By the study skill before it writes the spec and by the build skill before it plans slides; included with both. |
| [`topic-brief.md`](topic-brief.md) | The fields of a topic brief: audience with its market and language, angle, a working headline, facts with their source sentences, disagreements, unverified items, images with credits, sizes and licence terms, the candidates shown, the suggested beats, the articles read; and the files beside it (`img/`, `img-unused/`, `credits.md`, `facts.md`, `candidates.md`). | By the research skill before it writes the brief and by the build skill before it plans slides; included with both. |

## Who reads this

[`instagram-card-news-format-study`](../../skills/instagram-card-news-format-study/SKILL.md) includes `format-spec.md`; [`web-card-news-topic-brief`](../../skills/web-card-news-topic-brief/SKILL.md) includes `topic-brief.md`; [`html-card-news-from-brief`](../../skills/html-card-news-from-brief/SKILL.md) includes both. Every page is declared in the skill's `skillcdn.include` by its root-relative path, so that it arrives with the skill wherever SkillCDN serves it, and ships with the `marketing` plugin at `docs/card-news/`. A copy of a skill taken into another agent has neither page: its Requirements say so and name this directory in the repository as the place to fetch them.

## What every card-news skill does the same way

- **The reference account is studied, never copied, and it is the only design.** Its slide types, density and register are measured and reproduced; the build composes from those types alone and carries no layouts of its own; its photos, its copy and its name never enter a result.
- **Every sentence on a slide traces to a published sentence.** A number, a date, a quote or an interpretation comes from an article the agent read in full, cross-checked where two articles carry it; a frame's own caption counts as what the slide says only where it states a fact of the brief; what cannot be sourced is dropped or listed as unverified.
- **Every image shows the story and carries a credit.** Images come from where the articles point, in order: their own photographs, the clip or footage or post they cite, the subject's public pages, and an image search last; each is judged legible at phone size. The credit is the agency or the broadcaster and program, the photographer where named, the outlet or channel it appeared in, the date; and its licence terms where the publisher states them. An image under a "no modification" licence is not cropped, dimmed or overlaid. The images are the outlets', agencies', broadcasters' and subjects' material: the skills collect them with their credits for the user's decision and say so at every delivery, and a user who prefers their own images supplies them.
- **Nothing is posted.** The skills deliver files and text; publishing is the user's act.
- **Nothing is spent.** No paid tool; a shell, a browser and the open web.

Each skill states these in its hard rules, in the form its workflow gives them, so that they hold where these pages do not travel.

## How these pages are written

Each page describes an artifact by its fields: what the field holds, how it is obtained, who reads it. A field a run found missing is added to the page and to the skill that writes it in the same change. Examples use placeholders (`example-account`, `example-outlet.example`, `0000-00-00`); no real account, outlet, story or person is named.
