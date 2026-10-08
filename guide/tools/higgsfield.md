# Higgsfield skills

Conventions shared by the skills that drive Higgsfield (`higgsfield-…`). For authors: a skill still carries what it cannot work without in its own `references/`, because it may be mounted alone and this page is not discoverable.

## One server, named tools

Higgsfield is one MCP server, so the skills name its tools by their exact names (`models_explore`, `generate_video`, `sandbox_exec`, ...) and say what to do when one is missing. Models are never named as requirements: a skill says what a model must do (take references, make its own audio, output 9:16, offer a lowest tier), how to find the latest that does with `models_explore`, and how to choose when several qualify. A model id appears only in a dated note.

## What every Higgsfield skill does the same way

- **Spend only after a preflight.** `generate_video` and `generate_image` with `get_cost: true`, once per distinct parameter set; the sum with a reserve goes to the user before any job, images included. A preset recommendation instead of a number is answered with `declined_preset_id`.
- **`use_unlim` explicit on every call**, `false` unless the user asked for free-trial unlimited generations; left out, the server may return a question instead of a job.
- **Lowest tier, one job per call, `count` 1, never a batch tool**, so the review of one take can stop a fault before the next take repeats it.
- **The model speaks.** Every spoken word is the video model's native audio; no text-to-speech, dubbing or voice tools.
- **Overlays are code.** Captions, text, cards, logos, inserts, end cards: ffmpeg and Pillow in the sandbox, never the video model.
- **Two plain decodes decide what was said.** Every speaking take is decoded twice with Whisper without a prompt, with two model sizes; spelling the ear does not hear is set aside; agreement decides; a decode prompted with the intended line supports a reading but never overrules two plain ones; a word that is really wrong is never handed to the user as unsettled.
- **Captions and subtitles show the intended words;** speech-to-text supplies the clock.
- **A higher resolution is a separate step**, quoted at the delivery and started only on the user's word.

## The sandbox

`sandbox_exec` is a Linux box with ffmpeg, sox, Pillow, faster-whisper, Playwright and caption fonts, discarded about ten seconds after a foreground call ends and held for fifteen minutes by a background job. Long work runs with `background: true` and is polled with short calls (a sleep of at most 25 seconds, `timeout_seconds` at most 45). A command is at most 16,000 characters and a presigned URL about 2 KB, so URLs go into a file in one call and a script in the next. Outputs are reserved with `media_upload` before the producing command, PUT with the `Content-Type` the result names, confirmed with `media_confirm` after HTTP 200, and reserved anew for every revision. Fonts beyond Latin are fetched from the google/fonts repository under the Open Font License.

## Shared file, kept identical

| File | Holds |
|---|---|
| `references/pronunciation.md` | What the video models do with the sounds of each language run so far, and the dated outcomes. Included with every skill that speaks. |

The same file in every Higgsfield skill. Change every copy in one commit and compare them before committing:

```sh
diff marketing/skills/higgsfield-shorts-ad/references/pronunciation.md media/skills/higgsfield-shorts-drama/references/pronunciation.md
```

What belongs to one skill (how its lines are written, its verdict table, its retry budget) lives in that skill's own reference. Each skill's `tool-notes.md` is its own; a note about a tool's behavior that holds for every skill is copied to the others' notes with its date.

## Testing

A skill is exercised from a fresh session that gets only the user's request and reads the skill through SkillCDN, with the real server. First to the cost checkpoint (no credits), read against the skill's text; then one production with the checkpoint answered as the user would. What a fresh agent had to guess goes back into the files; what the tools did differently goes into the skill's `tool-notes.md` with its date, and a sound outcome into `pronunciation.md` in every copy. Notes record the behavior, never a run's product, persona, lines or story.
