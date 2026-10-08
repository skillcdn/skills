# Writing a skill

The format is not defined here. It is the [SkillCDN Format](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/skill-repo.md), specified in the SkillCDN repository: what `SKILL.md` and `SKILLCDN.md` are, which front-matter fields exist and their limits, how names are validated, what is served and searched. If this page and the spec disagree, the spec wins and this page gets fixed. This repository is the spec's reference repository, so it follows every required point and every recommendation.

This page adds what this repository asks on top of the spec, and how to write the body.

## What this repository adds

- Every skill lives in an area: `<area>/skills/<name>/`. The area's `SKILLCDN.md` says who its skills are for and adds the rules they share; a skill inherits both and restates neither.
- Prefix the skill name with the tool family it drives (`higgsfield-…`, `github-…`) so related skills sort together. The directory name is the skill name.
- A skill carries what it cannot work without, because it may be mounted alone at `.../skills/<area>/skills/<name>`, installed as part of the area's Claude Code plugin, or copied into another agent: its workflow, checkpoints, verdicts and hard rules link only inside its own directory. What the skills of one tool family share lives once in `docs/<family>/` (in the area's `docs/` when one area holds every skill of the family) and is linked from the phase that reads it, with a root-relative path (`/docs/<family>/<topic>.md`); the Requirements say that those pages come with the repository connection and where to fetch them when the skill runs without it. `node scripts/check.mjs` rejects any other link that leaves the skill directory.
- A skill does not restate the rules of the repository or of its area. They are the bodies of the `SKILLCDN.md` files above it, and SkillCDN hands them to the agent before the skill's own body. A skill's own hard rules cover what is specific to it; where a shared rule takes a specific form in the skill (which step costs money, what is confirmed before it), the skill states that form, so that it stays safe when it is copied or installed without SkillCDN.
- A handover is written in the skill that needs it. A skill that can start from another skill's result says where that input comes from when the user has none, how it chooses among what the other skill returns, and what it takes over; it names the other skill in a sentence and does not restate its method. The skill that is used stays general: it says what it delivers and is not narrowed to one use of it. A skill mounted alone still works, and says what to add.
- No rendered media, screenshots or generated output. Skills ship text. Data an agent must read is small JSON in `assets/`.
- `license` is `MIT` unless stated, and it decides whether SkillCDN serves the skill in full or only describes it: keep it a license the indexer recognizes as permissive. `metadata.tools` names the tool family. Quote a `version` so it stays text, and keep `metadata` flat.
- What SkillCDN adds to the front-matter lives under `skillcdn`: `include` lists the references every run needs, relative to the skill directory, so that `load_skill` and the MCP skills extension return them with the skill (the rest stay linked from the phase that needs them; a shared page under `docs/` cannot be included and is read when its phase comes); `translations` carries a `title` and a `description` per language tag for people who read the page in that language. The `name` and the `description` stay in English, the language the root manifest declares; agents read those. The `skillcdn` key stays in the source: the `SKILL.md` a host receives is re-serialized without it, with the rules and the included files inside, so what arrives is a plain Agent Skills document.
- Size: the body and the included references together stay around 16 KiB of text. `load_skill` pages the context at that size, and the rules of the repository and of the area come first on the pages. Material only some phase needs is linked from that phase, not included. The skills extension lists a skill only when a host can hold it whole (the directory named after the skill, at most 512 files and 16 MiB in all); the `check` role prints whether it is listed and, if not, why.

## Body skeleton

The spec recommends this order; every `SKILL.md` here follows it so an agent that has read one knows where to look in the next:

1. **Title and one-paragraph summary.** What comes out, from what.
2. **Requirements.** The tools it calls, with what to do when one is missing.
3. **Inputs.** What the user must supply, what is optional, and the intake questions for gaps.
4. **Workflow.** Numbered phases. Each says what it consumes, what it produces, and where the user is consulted. Anything longer than a paragraph goes to `references/` and is linked from its phase.
5. **Hard rules.** The short list an agent must never break, so it can be re-read before every costly step.
6. **Terminology.** The words the skill uses with a fixed meaning.

## Style

- Write for an agent with no memory of the previous session: current facts and decisions, not history.
- Imperative mood, short sentences, one idea each.
- Name a tool by its exact tool name in backticks the first time; describe it in words after that. Where the tool is a capability that every assistant provides under another name (a browser it can drive, a shell), name the capability and say how to recognize it: a product's tool names do not carry over to the next agent or outlast the next release.
- Do not pin versions of models, products or APIs. Tell the agent to discover the latest through the tool's own catalog, and say how to choose when several qualify.
- Where a number matters (a limit, a cost), say how to obtain it at run time. A dated snapshot may illustrate the shape, clearly marked as such.
- Decision points get a table: condition, choice, why.
- Anything the agent must ask the user is written as the question to ask.
- The `description` field is what search ranks first and what a client is told on connect. Write it as the sentence a user would say, ending with when to use the skill. Say when another skill in the repository is the better choice where their purposes overlap.
