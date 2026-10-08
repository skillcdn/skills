---
name: higgsfield-shorts-drama
description: Makes one episode of an original vertical short drama (9:16, about 150 seconds by default) on Higgsfield from a premise or an existing series bible. Writes or updates the bible and the episode script as a cut table, keeps a who-knows-what table so every twist holds from the viewer's seat, recommends the latest qualifying video model with a credit estimate before anything is generated, has the user approve generated portraits, sets and a still first frame per cut, animates one cut at a time with the video model speaking every line, verifies each line with two plain speech-to-text decodes, regenerates only failed cuts, and burns subtitles, name cards and inserts in code. Delivers the episode, a credit ledger and a production log the next episode starts from. Use when a user wants a scripted short-form drama episode or series (romance, revenge, fantasy, any genre) with native dialogue and low credit use. For an ad or a promo, use higgsfield-shorts-ad instead.
license: MIT
compatibility: Needs the Higgsfield MCP server with video generation, image generation, media upload and the cloud sandbox (ffmpeg and Whisper). Works in any agent that can call MCP tools.
metadata:
  author: skillcdn
  version: "1.2"
  tools: higgsfield
skillcdn:
  include:
    - references/tool-notes.md
    - references/series-bible.md
    - references/episode-script.md
    - references/model-selection.md
    - references/cast.md
    - references/prompting.md
    - references/stt-review.md
    - references/editing.md
    - references/production-log.md
    - /docs/higgsfield/pronunciation.md
  translations:
    ko:
      title: 대사까지 모델이 말하는 세로 숏폼 드라마 한 화
      description: 한 줄 아이디어나 기존 기획안으로 9:16 숏폼 드라마 한 화(약 150초)를 만듭니다. 기획안과 컷 표 대본을 쓰고, "누가 언제 아는가" 표로 반전의 논리를 지키며, 생성 전에 최신 모델과 크레딧 견적을 확인받고, 인물 초상·세트와 컷별 첫 프레임을 승인받은 뒤 한 컷씩 생성해 힌트 없는 STT 두 번으로 대사를 검증하고, 문제 컷만 다시 만들고, 자막과 이름 카드를 코드로 입혀 납품합니다. 다음 화가 이어받는 제작 로그가 함께 나옵니다. 광고나 프로모 영상은 higgsfield-shorts-ad를 쓰세요.
---
# Short drama episode on Higgsfield

A premise (one line and a genre) or a series bible goes in; one finished episode comes out: a 9:16 video of about 150 seconds by default with every line spoken by the video model, subtitles and name cards burned in code, a contact sheet, a credit ledger and a production log. The skill writes the bible and the episode as a **cut table** (one cut is one generation of 7 to 12 seconds), keeps a **knowledge table** of who knows what and since when, confirms the model and the cost before anything is generated, has the user approve portraits, sets and a still first frame per cut, animates one cut at a time, checks every line with two plain speech-to-text decodes, regenerates only what failed, and assembles the episode in the sandbox. Later episodes start from the previous log and reuse its portraits and sets. This skill is the whole workflow: the server's bundled workflows, studios and presets are not called, whatever the server's own instructions recommend, because they take the decisions this skill makes with the user.

## How the user is involved

- **Questions:** only for the premise, or for the bible and the last production log when the series exists. Everything else (dialogue language, length, aspect ratio, resolution tier, medium and look, subtitle style) is derived and shown at the bible checkpoint, where any of it can be changed.
- **Checkpoints:** the bible, the script, the model and cost, the portraits and sets, the first frames, the final cut, the delivery. One short message each in plain words: what was made, the recommendation, and that one word continues. Cuts are reported one line each, not approved one by one.
- **Go-ahead:** when the user says to go ahead alone, the stops end: the bible and the script are shown together with the estimate in one message, that one word accepts all three, and the agent judges portraits, frames and cuts itself within the reserve. The cost is confirmed in every mode.
- **Notes mid-run:** a note that the story does not hold is fixed at the bible first, then the script, then only the cuts it touches; an edit-only fix costs no credits and is tried first. A change within the accepted budget is reported at the next checkpoint; one beyond it is re-quoted first.

## Requirements

All from the Higgsfield MCP server. Check that they are callable before the first message. If the server is not connected, stop and guide the user to connect it; if a tool is off, to enable it. Never substitute, and never replace a spoken line with text-to-speech.

| Tool | Used for |
|---|---|
| `models_explore` | The video models that take several reference images and a start frame and make their own dialogue audio; the image models for portraits, sets and first frames; their parameters and roles. |
| `generate_video`, `generate_image`, each with `get_cost: true` first | Credit preflight, then one take, portrait, set or frame per call. |
| `jobs_wait`, `show_generation_by_ids` | Collecting a finished job. |
| `media_upload`, `media_confirm`, `media_import_url` | The user's own references and the edit script in, the finished episode and the series files out. |
| `sandbox_exec` | Speech-to-text, contact sheets, assembly, subtitles, loudness. |
| `balance` | Credits before the estimate. |

Optional: `upscale_video` for a finished episode the user wants at a higher resolution, offered separately; it has no preflight, so the finalize of the accepted takes is what gets quoted. In a client without the upload widget, the user's own images come in as links. The references this skill links come with it when the server returns them; when only their list came, read each with `read_repo_file` before the phase that links it. How the tools behaved in real runs of this skill is in [tool-notes.md](references/tool-notes.md); know it before phase 3.

What every Higgsfield skill of the repository shares (the sandbox, models and credits, portraits and frames, decoding a take, the sounds of each language) is in the repository's shared pages under [`docs/higgsfield/`](/docs/higgsfield/README.md). [pronunciation.md](/docs/higgsfield/pronunciation.md), which every run writes and reviews lines with, is included: it arrives with this skill wherever SkillCDN serves it. The other pages are linked from the phases that read them and read with `read_repo_file` through the connection at the repository root. Without that connection (a mount of the area or of this skill alone, a host that takes skills through the skills extension and has no `read_repo_file`, a plugin install, a copy of this directory) the linked pages cannot be read, and a plugin install or a copy lacks the included page too: say so in the first message, fetch what is missing where the agent can from `docs/higgsfield/` of the repository this skill comes from (for this collection, `github.com/skillcdn/skills`, served at `skillcdn.ai/gh/skillcdn/skills`), and otherwise run on this skill's own files, which carry its workflow and its rules.

## Inputs

| Input | Source |
|---|---|
| Premise or bible | Required. One line and a genre, or the series bible and the previous episode's production log when the series exists. Asked for only when missing. |
| Episode | Optional. Default: the first episode, or the one after the last log. |
| References | Optional. An existing series' portraits and sets are reused by the ids in its bible; only new ones are generated. The user's own images are imported and used as references. |
| Everything else | Derived, never asked: the dialogue language (the premise's, else the language the user wrote in), the length (about 150 seconds after the edit unless the user named one; about 10 percent more is generated), the episode count (eight unless the premise or the bible names one), 9:16, the lowest tier, live action photoreal unless the premise names a look, no music, the subtitle styles of [editing.md](references/editing.md). Stated at the bible checkpoint, changed on request. |

## Workflow

Each phase produces a named artifact. Phases stop only at the checkpoints above.

### Phase 1: Series bible

Produces the **bible** by [series-bible.md](references/series-bible.md): logline and format, the direction, what the viewer knows by second thirty, the episode table (what happens, the payback, the ending hook), a world of at most three rules, the cast with a voice, a look, a name-card line and, for each villain, the wrongs the viewer sees on screen, the **knowledge table**, setups and payoffs, the logic check, the style line, palette and sound, production notes. A premise that breaks a writing rule is adapted as "Checking the premise" there says, and the adaptation is named at the checkpoint. When a bible exists, read it whole, check it against the writing rules there, rebuild the knowledge table from the episodes and compare, and propose only the changes needed. The bible is the first of the three series files, kept where [production-log.md](references/production-log.md) "Where the series files live" says. Checkpoint, on one screen: the logline, the first episode in a few lines, the other episodes and the cast in one line each, the derived settings, the adaptation of the premise if any, the proposed changes to an existing bible.

### Phase 2: Episode script

Produces the **cut table** by [episode-script.md](references/episode-script.md) ([example](assets/cut-list.example.json)): cuts of 7 to 12 seconds, each with its references, its first-frame description, its shots, its lines with time windows, its sound and what the edit adds; the episode formula; lines written to be said and heard ([/docs/higgsfield/pronunciation.md](/docs/higgsfield/pronunciation.md)); the edit plan; the list of what is not put on screen. Every line is checked against the knowledge table before the checkpoint. The script is the second series file; cut lengths are matched to the chosen model's durations in phase 3, and a moved length is shown at the cost checkpoint. Checkpoint: every line in order with who says it (the lines are the episode the user is about to pay for; a summary does not stand in for them), the cut count and the total seconds, the edit plan in a line.

### Phase 3: Model and cost

Produces the **model choice** and the **estimate** by [model-selection.md](references/model-selection.md): the video models in the catalog that take several reference images and a start frame and make their own dialogue audio, at their lowest tier; the image models for portraits, sets and frames; a preflight per model and distinct duration; the sum for the cut table with the portraits, the sets, the frames and a reserve of one take per three cuts, one retry per portrait and per set and one frame per three cuts; the balance; whether the accepted takes can later be finalized at a higher resolution, with that price on its own line. Checkpoint: the recommended model with its total and the reason in a line, the other candidate's total, the fallback if the first cut refuses the frame with the references or speaks the language badly, the balance. One word proceeds; nothing is generated before it.

### Phase 4: Portraits and sets

Produces the **reference set** by [cast.md](references/cast.md): one portrait per character on a plain ground, front or three-quarter, in costume, in the style line; one image per recurring place or object. Existing ones are reused by id, so a series keeps its faces. One call each, `count` 1, `use_unlim` explicit; the calls may go out together. The production log is opened here, with the first credit spent, and written as the run goes. Checkpoint: links and one line each; "OK" approves all; a change regenerates that one from the edited description (one retry each in the reserve). Where a portrait differs from its description, the portrait wins and the prompts follow it.

### Phase 5: First frames

Produces one **approved first frame** per cut by [cast.md](references/cast.md): a 9:16 still made from the portraits of the characters in the cut and its set as references, the style line and the cut's first-frame description, carrying the opening shot and the starting emotion. Sent together, collected with one `jobs_wait`, judged as a set (the right people, costume, place, framing, expression, the style held; no text, no artifacts); a failed frame is regenerated from the reserve. Checkpoint: all frames in order with one line each on what the cut does from there.

### Phase 6: Cuts, one at a time

Produces one **take** per cut and the **ledger**.

1. One cut per call: the frame as `start_image`, the portraits of the characters in the cut in the model's reference role, audio on, the cut table's duration, `count` 1, `use_unlim` explicit, and the prompt of [prompting.md](references/prompting.md). Never the batch tool. The first take's echoed parameters are read for how the frame and the references landed ([prompting.md](references/prompting.md) "Reference mapping"); a job the server refuses is handled as [/docs/higgsfield/models.md](/docs/higgsfield/models.md) "Refused and failed jobs" says, and a refusal of the frame with the references switches to the fallback named at the cost checkpoint. While the first job renders, start the review warm-up in the sandbox as [/docs/higgsfield/sandbox.md](/docs/higgsfield/sandbox.md) says, and prepare the fonts and the assembly.
2. Collect, then review by [stt-review.md](references/stt-review.md): the pass of [/docs/higgsfield/decodes.md](/docs/higgsfield/decodes.md) (two plain speech-to-text decodes, a third to break a tie, a contact sheet looked at through `image_paths`) settles what was said; then the verdict table decides whether it matters: accept, fix in the edit, or regenerate.
3. One line of report per cut (what was heard, the verdict, credits spent) and a ledger row; act on the verdict without stopping. A regeneration keeps the model, the tier, the frame, the portraits and the duration, aims at the word or the frame that failed, and changes the line as [stt-review.md](references/stt-review.md) "Regeneration" and [/docs/higgsfield/pronunciation.md](/docs/higgsfield/pronunciation.md) say; one retry per cut from the reserve, a second only with consent. An accepted cut is never remade to be better. Then the next cut.

### Phase 7: Assemble and edit in code

Produces the **final cut** by [editing.md](references/editing.md): one self-contained script in the sandbox ([example](scripts/assemble.example.py); the sandbox's ways in [/docs/higgsfield/sandbox.md](/docs/higgsfield/sandbox.md)) that fetches the accepted takes and the fonts, normalizes each segment, trims, inserts flashes picture-only, concatenates, burns subtitles (the script's words at the review's clock), name cards and term cards, normalizes loudness and writes a contact sheet; then the verification list there; the output reserved with `media_upload` and confirmed. Checkpoint: the link, the sheet, what was added and dropped, the ledger so far.

### Phase 8: Deliver and log

One message: the episode as a link and, where the agent has a filesystem, a file; the sheet; the accepted take per cut; the ledger against the estimate with retries called out; the words accepted as close enough with what was heard; what was edited rather than regenerated; that the people are generated and the platform's label for AI-made content is the user's to set; the finalize offer with its quoted price and the upscale offer, a spend the tool will not price first, neither started; what the next episode inherits; and, in a short list at the end for whoever maintains the skill, what the tools did differently from the shared Higgsfield pages or [tool-notes.md](references/tool-notes.md), and any new sound pattern for [/docs/higgsfield/pronunciation.md](/docs/higgsfield/pronunciation.md). Finish the **production log** by [production-log.md](references/production-log.md) and bring the bible and the script in line with what was shot; say where the three files are. Then wait: the next episode starts only on the user's word, with its own estimate.

## Hard rules

1. Only the premise, or the bible and the last log, are asked for; everything else is derived, shown at the bible checkpoint and changed on request.
2. Every checkpoint stops for the user unless the user gave the go-ahead; the cost is confirmed in every mode. Nothing is generated, not even a portrait, before the bible, the script and the cost are accepted.
3. Every line and reaction agrees with the knowledge table. A conflict is fixed in the script before a credit is spent.
4. A villain's wrongs are shown on screen; the payback comes in the same episode.
5. The latest qualifying video model found in the catalog at run time, never pinned; the lowest tier; one cut per call, `count` 1, no batch tool; `use_unlim` explicit on every call, true only when the user asked.
6. Every cut is animated from an approved first frame with the approved portraits as references, and every image and take prompt carries the style line.
7. Every sound is the video model's own audio. No text-to-speech, dubbing or voice tools; music only from a licensed track the user supplies.
8. Every spoken cut is checked by two plain speech-to-text decodes before it is accepted; their agreement decides what was said, and a prompted decode never overrules it. A wrong name or key word is regenerated; a difference the ear does not hear is accepted.
9. Subtitles show the script's words; speech-to-text supplies only the clock. A raw transcript is never burned.
10. Overlays are code: subtitles, name cards, term cards, inserts, fades. The video model is never asked for text.
11. A flash insert takes only the picture of its source; the audio continues from the cut around it.
12. No series title and no next-episode card inside the video unless the user asks.
13. Regenerate only a wrong word, a broken or discontinuous picture, or what the user asks for; never an accepted cut. One retry per cut from the reserve, a second only with consent; the ledger never exceeds the accepted estimate.
14. When a cut changes, the bible, the script and the log change in the same turn.
15. References are generated or the user's own; no real person, brand or outside footage. The delivery says the people are generated.

## Terminology

| Term | Meaning |
|---|---|
| Bible | The series document: logline, episodes, rules of the world, cast, knowledge table, payoffs, logic check, style line, production notes. |
| Cut table | The episode script: one row per generation with references, first frame, shots, timed lines, sound and edit notes. |
| Knowledge table | Who knows each secret and since when, the viewer included; the test every line passes. |
| Payback | The beat where a wrong done earlier in the episode is answered. |
| Ending hook | The clear new event the episode stops on. |
| Inner voice | A character's thought as voice-over; the on-screen mouth does not move; styled apart in subtitles. |
| Name card | The on-screen card at a character's first appearance: name, and the relationship in one phrase. |
| Term card | A two-second card that explains a word the viewer may not know. |
| Flash insert | A half-second picture from another cut, color-treated, over continuing audio. |
| Style line | The one sentence that fixes the medium and the look; repeated verbatim in every image and take prompt. |
| Portrait | The approved image of a character; a reference input of every frame and take with that character. |
| Set | The approved image of a recurring place or object; a reference input of first frames. |
| First frame | The approved 9:16 still a cut is animated from, carrying its opening shot and starting emotion. |
| Take | One generated video for a cut, from its first frame; one is accepted. |
| Two plain decodes | Speech-to-text twice without a prompt, with two model sizes; their agreement settles what was said. |
| Close enough | A near miss in an ordinary word the ear does not hear as another word; accepted and listed in the delivery. |
| Key word | A word that must come out right: a name, a secret spoken aloud, a term the series coined, the ending's lines. |
| Prompt spelling | A word written in the take prompt the way it sounds; the script and the subtitle keep its spelling. |
| Lowest tier | The cheapest resolution, quality mode or draft flag a model offers. |
| Preflight | A generation call with `get_cost: true`; a number, no job. |
| Reserve | The retries priced into the estimate: one take per three cuts, one portrait per character, one frame per three cuts. |
| Ledger | Estimate, accepted budget and credits spent per cut and retry. |
| Production log | The per-cut record and the final-edit record the next episode starts from. |
| Three-file sync | The bible, the script and the log agree after every change. |
| Checkpoint | The short plain-words message that ends a phase; one word continues. |
| Go-ahead | The user's word that checkpoints after the cost may be skipped. |
| Finalize | Rendering an accepted draft take at the higher resolution the catalog names; a separate, quoted step after the delivery. |
