# Marketing documents

Document sets that serve the marketing area: directories of Markdown with no `SKILL.md`, discovered by SkillCDN next to the area's manifest ([SKILLCDN.md](../SKILLCDN.md)), listed and searched with `browse_repo` and `search_repo` and served with `read_repo_file` through the repository or the area connection, and shipped with the area's Claude Code plugin. A set that serves every area lives in the repository's [docs/](../../docs/README.md) instead.

| Document set | What it is |
|---|---|
| [`meta-ad-library/`](meta-ad-library/) | What the skills that read the Meta Ad Library share: what the library is evidence of, the routes into it and their code, the URL parameters, the record a result yields, counting by age, manners and limits. One file per topic; the skills link each from the phase that reads it. |
| [`card-news/`](card-news/) | What the three card-news skills share: the fields of the format spec (measured by the study skill, built from by the build skill) and of the topic brief (written by the research skill, read by the build skill), with how each field is obtained and used, and what every card-news skill does the same way. Each skill includes the page it writes or reads. |
| [`instagram/`](instagram/) | What the skills that read Instagram share: what a visitor without an account sees and the routes a browser takes to it, the sign-in prompt, the viewport, the documented sizes, a post page's data, stepping a carousel, reading a slide, the caption. One file per topic; the format study includes both. |

Every document carries a front-matter `title` and `description`, or starts with a level-one heading followed by one summary paragraph, because that is what search shows, and headings that name its parts, because a search result names the sections that matched and `browse_repo` outlines a file by them. Links stay within what an agent can reach through the mount: skills, manifests, document directories, and the README of a served folder.
