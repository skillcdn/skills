# Engineering documents

Document sets that serve the engineering area: directories of Markdown with no `SKILL.md`, discovered by SkillCDN next to the area's manifest ([SKILLCDN.md](../SKILLCDN.md)), listed and searched with `browse_repo` and `search_repo` and served with `read_repo_file` through the repository or the area connection, and shipped with the area's Claude Code plugin. A set that serves every area lives in the repository's [docs/](../../docs/README.md) instead.

| Document set | What it is |
|---|---|
| [`skillcdn/`](skillcdn/) | What the skills that work on a repository in the SkillCDN Format share: how a push becomes what an agent is served, how an agent with none of the session's context is started on each host, and where a session's record and memory are kept. One file per topic; the skills link each from the phase that reads it. |

Every document carries a front-matter `title` and `description`, or starts with a level-one heading followed by one summary paragraph, because that is what search shows. Links stay within what an agent can reach through the mount: skills, manifests, document directories, and the README of a served folder.
