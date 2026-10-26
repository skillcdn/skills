# Design documents

Document sets that serve the design area: directories of Markdown with no `SKILL.md`, discovered by SkillCDN next to the area's manifest ([SKILLCDN.md](../SKILLCDN.md)), listed and searched with `browse_repo` and `search_repo` and served with `read_repo_file` through the repository or the area connection, and shipped with the area's Claude Code plugin. A set that serves every area lives in the repository's [docs/](../../docs/README.md) instead.

| Document set | What it is |
|---|---|
| [`card-news/`](card-news/) | What the card-news skills share: the four routes to a format spec (a reference as it is, a slight change, a format of the user's own from the genre's references, something new from a reference) and the fields of the spec, measured by the format study or designed by the design variations and built from by the build; the fields of the topic brief, written by the research skill in the product area and read by the build; how each field is obtained and used; and what every card-news skill does the same way. The study and the build include the page each writes or reads; the variations link the spec's page and the research links the brief's. |

Every document carries a front-matter `title` and `description`, or starts with a level-one heading followed by one summary paragraph, because that is what search shows, and headings that name its parts, because a search result names the sections that matched and `browse_repo` outlines a file by them. Links stay within what an agent can reach through the mount: skills, manifests, document directories, and the README of a served folder.
