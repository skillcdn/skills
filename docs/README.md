# Document sets

Document sets that serve every area: directories of Markdown with no `SKILL.md`. This directory is declared in the repository manifest (`SKILLCDN.md`, `documents: [docs]`), so SkillCDN lists and searches everything here with `browse_repo` and `search_repo` and serves it with `read_repo_file`, without any skill. A document set that serves one area lives in that area's `docs/` instead, discovered by default next to the area's manifest. What the skills of one tool family share, whichever areas they are in, lives here as `<family>/`.

| Document set | What it is |
|---|---|
| [`higgsfield/`](higgsfield/) | What the skills that drive Higgsfield share: the sandbox, models and credits, portraits and first frames, decoding a take, and the sounds of each language, as real runs showed it. One file per topic, organized by what holds now; the skills link each from the phase that reads it. |
| [`browser/`](browser/) | What the skills that read a website or render a page with a browser share, whichever area they are in: a browser the agent drives and how hosts differ, a headless Chromium-family browser from a shell, reading a page in full and taking its images, rendering an HTML page the agent wrote to PNG or PDF, frames of a public clip. One file per topic; each skill includes the page every run needs and links the rest from the phase that reads it. |

Handbooks and playbooks an area's people work from, written so that an agent finds and reads them without a skill, will join them.

Every document carries a front-matter `title` and `description`, or starts with a level-one heading followed by one summary paragraph, because that is what search shows, and headings that name its parts, because a search result names the sections that matched and `browse_repo` outlines a file by them. Links stay within what an agent can reach through the mount: skills, manifests, document directories, and the README of a served folder.
