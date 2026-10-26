# The pack: how an agent finds its way

Two pages for the agent that has just connected to this pack and must decide whether a skill exists for the job in front of it, and which one: how a skill is found, and an index of the jobs the skills do in the words a user says. They serve every area, so they live at the root; they are documents, searched and read like any other, and no skill includes them.

| Document | Holds | Read |
|---|---|---|
| [`finding-a-skill.md`](finding-a-skill.md) | How the pack is laid out (areas, the name of a skill, the document sets), the three ways to find a skill (the jobs index, browsing an area, searching the whole pack with English words), how a result is read, what to do when no skill fits, and dated examples of what the search returned. | On connecting, before choosing a skill; whenever a request does not name a skill. |
| [`jobs.md`](jobs.md) | One section per job: the sentence a user says, what comes back, the skill's path, other ways the job is asked for, and the skill that looks alike but does something else. | First, with `search_repo` scoped to `docs/pack`, or whole. |

## How these pages are kept

Every skill in the pack has a section in `jobs.md`, and `scripts/check.mjs` fails when one is missing, as it fails for a skill missing from a catalog. The section's heading is the sentence a user says, because a search names the sections that matched and ranks a heading above a body; the body names the skill by its path so that `load_skill` can take it as it is. A new skill brings its section with it; a skill that changes what it does changes its section in the same change. The examples in `finding-a-skill.md` are what a search returned on the day named beside them; they are checked again when the search changes or a skill is renamed. Nothing here restates a skill: a section says what the job is and where the skill is, and the skill says the rest.
