---
name: higgsfield-shorts-ad
description: Makes a short-form vertical AI ad, promo or commercial on Higgsfield from a product link and a reference video, found among the ads running now when the user has none. Use when a user wants a promo or ad short (TikTok, Reels, Shorts) for a product, brand or website in the spirit of a reference short, with credit use kept low and no expertise needed. The reference is found with meta-ad-library-creative-research. Learns what makes the reference work (the hook, the rule its story runs on, the device, the reveal, the measured pacing) and writes an original story for the product on the product's own world rather than a copy. Derives language, length, medium, look and brand typography itself, generates approved portraits and a still first frame per shot, directs each character's performance, recommends the latest model with a credit estimate, animates one draft take at a time, and adds captions, text and the end card in code.
license: MIT
compatibility: Needs the Higgsfield MCP server with video generation, image generation, video analysis, media upload and the cloud sandbox (ffmpeg and Whisper). Works in any agent that can call MCP tools.
metadata:
  author: skillcdn
  version: "1.12"
  tools: higgsfield
skillcdn:
  include:
    - references/intake.md
    - references/story.md
  translations:
    ko:
      title: 레퍼런스 영상으로 만드는 숏폼 AI 광고
      description: 레퍼런스 영상 하나와 제품 링크만으로 Higgsfield에서 세로형 숏폼 AI 광고와 프로모 영상을 만듭니다. 레퍼런스가 왜 통하는지(후킹, 이야기가 굴러가는 세계의 규칙, 장치, 반전, 측정한 호흡)를 배워 제품 자신의 세계 위에 새 이야기를 씁니다. 언어, 길이, 매체(레퍼런스처럼 실사 또는 애니메이션), 룩, 브랜드 타이포그래피를 스스로 정하고, 승인받은 인물 초상과 컷별 첫 프레임을 만든 뒤 최신 Kling 또는 Seedance 모델을 크레딧 견적과 함께 추천하고, 초안 테이크를 한 번에 하나씩 생성하며, 자막, 문구, 엔드 카드는 코드로 넣습니다. 제품, 브랜드, 웹사이트를 위한 프로모/광고 숏폼(TikTok, Reels, Shorts)을 레퍼런스 숏폼의 느낌으로, 크레딧을 아끼면서 전문 지식 없이 만들고 싶을 때 쓰세요. 레퍼런스가 없으면 meta-ad-library-creative-research로 지금 집행 중인 광고에서 먼저 찾습니다.
---
# Shorts-style AI ad from a reference video

One reference video and one product (a link is enough) go in; a captioned vertical ad, its clean master and a credit ledger come out. A user with no reference still gets one: it is found first, among the ads now running for that kind of product. The reference teaches what works (the hook, the rule its story runs on, the device that carries it, the reveal, the pacing as measured) and sets the medium and the look (live action or animation, in its style); the ad itself is written new, on the product's own world. Everything beyond the two inputs is derived and shown in plain words. Portraits and a still first frame per shot are approved before any video is paid for; the latest Kling or Seedance model animates one draft-quality take at a time and speaks every line itself; cuts, text, captions, effects and the end card are code in the sandbox. This skill is the whole workflow: no bundled Higgsfield workflow replaces it.

## How the user is involved

- **Questions:** only for the product, and for the reference video when the request has none and nothing at hand can find one. Nothing else is ever asked; it is derived. A missing reference is found, not asked for, wherever a skill that researches running ads is at hand (phase 1).
- **Checkpoints:** the research skill's own shortlist checkpoint when the reference is found, the concept directions' sheet from the variations skill when it is at hand (phase 3), then the plan with its cost, the portraits, the first frames, the clean master, the finished ad. Each is one message in plain words, as short as its content allows: what was made, the recommendation, and that one word ("OK" in the user's language) continues. Anything can be changed at a checkpoint. Takes are reported, not approved one by one.
- **Go-ahead:** when the user says to go ahead alone, the checkpoints after the cost are skipped; the cost is confirmed in every mode.
- **Changes mid-run:** applied from that point on; reported at the next checkpoint when within the accepted budget, re-quoted first when beyond it.

## Requirements

All from the Higgsfield MCP server. Check that they are callable before the first message. If the server is not connected, stop and guide the user to connect the Higgsfield MCP server; if a tool is off, to enable it. Never substitute.

| Tool | Used for |
|---|---|
| `models_explore` | The latest Kling and Seedance video models, the two image models, and their parameters. |
| `generate_video`, `generate_image`, each with `get_cost: true` first | Credit preflight, then one take, portrait or frame per call. |
| `video_analysis_create`, `video_analysis_status` | Scene analysis of the reference, as a supplement. |
| `media_import_url`, `media_upload`, `media_confirm`, `media_upload_widget` | Reference, product images and finished files in and out. |
| `sandbox_exec` | Frames, speech-to-text, the product page's images and type, cutting, text, captions, muxing. |
| `jobs_wait`, `show_generation_by_ids` | Collecting a finished job. |
| `balance` | Credits before the cost is presented. |

Optional: any web-reading tool for the product page's text; a skill that researches running ads, which finds the reference when the request has none. No text-to-speech. In a client without the upload widget everything comes in as links, or an agent with a shell uploads a local file itself ([intake.md](references/intake.md)).

[intake.md](references/intake.md) and [story.md](references/story.md), which the first message and the plan are written by, arrive with this skill. Every other page is read when the phase that names it begins, at its "Read first": this skill's own under `references/`, and what every Higgsfield skill shares (the sandbox, models and credits, portraits and frames, decoding a take, the sounds of each language) under [`docs/higgsfield/`](/docs/higgsfield/README.md). No phase is run from its summary here. Links that start with `/` are files of the pack this skill is from: a copy of this directory, a plugin or a mount below the root that lacks one reads it through the pack's connection (`https://skillcdn.ai/gh/skillcdn/skills`) or at `github.com/skillcdn/skills`.

## Inputs

| Input | Source |
|---|---|
| Reference video | A link straight to a media file, or a local file through the widget. When the request has none, it is found among the ads now running for that kind of product by a skill that researches them, in this pack [meta-ad-library-creative-research](/marketing/skills/meta-ad-library-creative-research/SKILL.md), which reads the Meta Ad Library, and chosen as [finding-a-reference.md](references/finding-a-reference.md) says. Asked for only when no such skill is at hand. |
| Product | Required. A link to its site or page, or a name with a sentence. Asked for only when missing. |
| Everything else | Derived, never asked: language (the product page's, in the user's language when the page has it, else the reference's), channel (the platform the reference runs on, or the one the user names, whose documented format is read at run time; the safe zones and sizes in [captions.md](references/captions.md) and [design.md](references/design.md) are the values last seen), length (the reference's), medium and look (the reference's: live action or animation, and its style in words), what changes (everything but the mechanism, the medium and the look), typography and colors (the brand's), product images (logo, one product image, the site's own people if cast), budget (quoted at the cost checkpoint). Stated at the plan checkpoint, changed on request. |

## Workflow

Each phase produces a named artifact. Phases stop only at the checkpoints above.

### Phase 1: Intake

Produces the **intake record**, by [intake.md](references/intake.md). Read [/docs/higgsfield/sandbox.md](/docs/higgsfield/sandbox.md) before the first sandbox call.

1. Both inputs in the request: ask nothing, say in a line what happens next, go on. The product missing: ask for it as "What is asked" there shows, and stop.
2. Read the product page as "Product brief" there: name, what it is, tagline, claims (only these may be spoken), language, images, and its type and colors.
3. The reference missing: read [finding-a-reference.md](references/finding-a-reference.md) and find one as it says, in the market of the ad's language, and say so in a line; ask for it only when no skill at hand can find one.
4. Derive the rest and record it. The artifacts of every phase are written in the folder the user named for the run, else in a folder named for the ad outside any repository; the delivery says where.

### Phase 2: Analyze the reference

Produces the **analysis brief**. Read first: [analysis-brief.md](references/analysis-brief.md) (the sandbox pass and the template), [tool-notes.md](references/tool-notes.md) and [editing-decisions.md](references/editing-decisions.md).

1. Import the reference. Start the scene analysis only for a reference uploaded through `media_upload` or given as a YouTube link, which is what the tool takes, and never wait for it. Run the sandbox pass in the background: probe, frames, contact sheet, transcript, the delivery line.
2. Fill every section of the template from the frames and the transcript: the medium and the look in words an image model can follow, the mood, the shots with their beats, the dialogue, the on-screen text and its look, the cast, the sound, and above all **why it works**: the hook in the first two seconds, the tension and the turn, the payoff, the call to action, the pacing that carries them. Then the **story engine**, the information order line by line and the measured **delivery** (speech rate, lines per ten seconds, longest pause, hook window) by [story.md](references/story.md) "Reading the reference".
3. Mark build routes (generate, edit, drop) by editing-decisions.md.
4. A reference this skill found comes with the research's breakdown of it and its readings of the market. They are a first look and they feed the concept, as finding-a-reference.md says; the sandbox pass still runs and the brief is still filled.
5. The reference, its frames, its sheet and its audio are for looking and listening only: none is passed to a model in any role, and none appears in the output. Open decisions go to the plan checkpoint; there is no checkpoint here.

### Phase 3: Concept and plan

Produces the **concept**, the **cast list**, the **shot list** ([example](assets/shot-list.example.json)) and the **edit plan**. Read first: [cast.md](references/cast.md) and [design.md](references/design.md); of [pronunciation.md](/docs/higgsfield/pronunciation.md), "In any language" and the section of the dialogue language; and, for every word the ad speaks or shows, [readers.md](/docs/writing/readers.md) (the viewer, the language, plain words) and [facts.md](/docs/writing/facts.md) (what the ad may say of the product). story.md and the pronunciation page are the lines' own rules and win where they are sharper.

Before the story, the directions: by the pack's rule on starting from a reference, [web-concept-variations](/product/skills/web-concept-variations/SKILL.md) runs on the reference where it is at hand (the mechanism as the analysis brief reads it, the product as the subject), stopping at its own sheet, and the user's pick is the story's rule, device, figure and hook as the variation set's [handoff.md](/docs/variation/handoff.md) "By producing skill" says; the reference's own mechanism carried straight is the second offer, taken when the user says so or when that skill is not at hand, said so in the plan. On a go-ahead the recommended direction is taken. Nothing is spent here: the directions are text.

1. **Story.** By story.md "Writing the new story", in its order: the rule of the world, taken from what the product itself claims to know or do; a device from the product's world; the figure (the site's own persona when it has one); five hooks scored against the table and one kept, with the runner-up; the signature line; the reveal; the lines in order, each adding one fact, at the reference's measured density. This is the concept: a different situation, setting, cast and lines that deliver the same mechanism in the reference's medium and look. A story that would work for any product in the category is rewritten. Write one alternative (another rule or device) in one line for the checkpoint. Only when the user asks for a close remake is the reference followed scene by scene, and the plan says so.
2. **Style line.** One sentence from the brief's medium and look that fixes the style for every image and take prompt: the medium, line, color and shading, backgrounds, light, camera. Repeated verbatim in every portrait, frame and take prompt, so they match; a portrait prompt may leave out its scene clauses (background, camera).
3. **Cast.** One description per character: age range, build, hair, skin tone, clothing, baseline expression, role. The product site's own people may be cast (cast.md).
4. **Lines.** Every spoken line is an **intended line**, written as story.md "Lines a model can say": short and speakable, with a prompt spelling for every word that is not said the way it is written and its key words kept clear of the sounds the model slurs. Every statement about the product comes from the product page or the user (story lines are fiction and free). The video model speaks the line in the take. A line spoken off screen (a voice-over, a speaker outside the frame) is marked so, and the character on screen does not mouth it. The script's unit count and line count are checked against the density target (story.md "Density") and both numbers go to the checkpoint.
5. **Shots.** One shot is one generation, merged only for continuity. Each records duration, cast, the first-frame description, the **performance** (emotion at the start, the turn, emotion at the end, delivery, eye line, the action), the intended line, the product image if any, audio on for a line. The form decides the shape: on-camera dialogue is one speaking take per shot; a narrator over pictures is one voice take for every line, sized to the speaking time plus a second, under silent takes or stills cut to its words (editing-decisions.md). Total length matches the reference within the model's durations; an end card the reference lacks adds its own seconds.
6. **Edit plan and design.** Cut order, inserts, on-screen text, effects, music, captions and the end card, in the brand's type and colors by design.md.

### Phase 4: Cost and the plan checkpoint

Produces the **estimate**, the **model choice** and the approved plan. Read first: [model-selection.md](references/model-selection.md) and [models.md](/docs/higgsfield/models.md).

1. Find the latest general model of each family with `models_explore`; lock the lowest tier, every one the model exposes (`480p`, `std`, a draft flag); read its roles and aspect ratios.
2. Preflight once per family, distinct duration and audio setting of the shot list for the takes, and the image model or models for portraits and frames; a preset recommendation instead of a number is answered with `declined_preset_id`. Reserve: one take per three shots at the dearest shots, one portrait per cast member, one frame per three shots. Read `balance`.
3. Recommend one family with its reason in one line, and name the fallback: the other family at its total, or the same model with the portrait alone as its reference and the frame's composition in the prompt, for when the first take refuses the frame together with the portrait. When the total exceeds the balance, say so and offer a shorter ad or the other family before anything else.
4. Checkpoint, in plain words: when the agent found the reference, its link, why it was chosen, and in a line what the ad keeps of it and what differs at a glance; the story as story.md "What the user sees" and its alternative, what the ad will be, the cast, what the edit adds, the derived settings and open decisions, the recommended model's total with reserve and the balance, the other family's total, the fallback. "OK" proceeds; the user may pick the alternative, the other family, or change anything. A changed plan is preflighted again.

### Phase 5: Cast portraits

Produces the **approved portraits**. Read first: the shared [cast.md](/docs/higgsfield/cast.md), with this skill's cast.md. One per cast member, in the style line, one call each (the calls may be sent together), cheapest setting, `use_unlim` explicit, in the ledger. Checkpoint: links and one line each; "OK" approves all, a change regenerates that one from the edited description (one retry per member in the reserve). Where a portrait differs from its description, the portrait wins and the prompts follow it. A plan that casts no generated person skips this checkpoint; the frames' is the first.

### Phase 6: First frames

Produces one **approved first frame** per generated shot, by the same two pages. A still in the take's aspect, 9:16 unless the edit plan composes the take into the 9:16 canvas (a split layout, an inset), from the portrait as reference, the style line and the shot's first-frame description, carrying the shot's starting emotion; one call each, sent together and collected with one `jobs_wait`, looked at as a set (right person, clothing, setting, framing, expression, the style held; no legible text, no artifacts), one failed frame regenerated from the reserve. Checkpoint: all frames in order with one line each on what the shot does from there.

### Phase 7: Takes, one at a time

Produces one **take** per shot and the **budget ledger**. Read first: [regeneration.md](references/regeneration.md) and [decodes.md](/docs/higgsfield/decodes.md).

1. One shot per call: the frame as `start_image`, the portrait in the identity role where one exists, audio on, `count` 1, `use_unlim` explicit, and a prompt made of the style line, the performance line, the delivery pace in the measured terms of story.md "Density" (never "slow" from a mood), and the intended line in quotes, with the instruction that, after about half a second of silence, the character speaks exactly these words in the dialogue language with natural standard pronunciation and nothing else; a word that has a prompt spelling is written in it. Never the batch tool. A preset recommendation instead of a job is answered with `declined_preset_id`; a job the server refuses is handled as models.md "Refused and failed jobs" says, and a refusal of the frame together with the portrait switches to the fallback named at the plan checkpoint. Poll `jobs_wait`; use the wait to warm up Whisper, fetch the font and prepare the assembly.
2. Review by the pass of decodes.md, from its contact sheet, its plain word-timed decodes and the loudness curve: the same person, setting and style as the frame (no drift toward photoreal or another drawing style), the speaker's mouth moving in the speech window and still outside it (for a voice-over, the on-screen mouth stays closed throughout), the performance matching the beat (the emotion and its turn visible), the pace within the density target (rate and longest pause), no text or artifacts, speech only where it should be. What was said is settled first, as that page says; then the verdict by regeneration.md: accept, accept with edit, or regenerate.
3. Ledger row and a one-line report per take; act on the verdict without stopping (one retry per shot from the reserve). Stop only for a second retry or when the ledger reaches the accepted estimate.

### Phase 8: Assemble and edit in code

Produces the **clean master**. One self-contained script in the background, as [sandbox.md](/docs/higgsfield/sandbox.md) says: takes, cuts, inserts, on-screen text, effects, music with ducking, the end card and the logo by design.md "Building it in the sandbox", verified by editing-decisions.md "Sandbox conventions"; output reserved with `media_upload`, a new reservation per revision, and PUT at the end; a take made without audio gets an audio track first. Checkpoint: the master's link, the take reports, what was added and dropped; "OK" continues, or any shot may be retried here.

### Phase 9: Captions

Produces the **captioned master**. Read first: [captions.md](references/captions.md). Word timestamps from the master, cues aligned to the intended lines starting at their own first word, burned in the brand's type by design.md, verified (every word present, no cue early or spread across a pause, frames at cue midpoints), uploaded. Shown in the delivery.

### Phase 10: Regenerate

regeneration.md decides during phase 7 and at the clean-master checkpoint: ambiguous, broken, flat, drifted or dragging takes only, same frame and portrait, one retry from the reserve, an ordinary word that failed said another way and a key word respelled, one bad line of a long take as a short pickup, a second retry only with consent.

### Phase 11: Deliver

One message in plain words:

- The captioned master and the clean master, as links; the portraits and the frames, for reuse.
- The lines as captioned, and the words accepted as close enough or left unsettled, each with what was heard.
- The ledger: estimated against spent, per item, retries called out.
- What was generated, what was made in code, and what of the reference was left out and why.
- What is the user's from here: the imported reference stays in their Higgsfield library, where they may remove it; when the cast is generated people in live action, they are not real people, and the platform's label for AI-made content is the user's to set when the ad is published.
- A higher resolution, as a separate step that is not started: the finalize of the accepted takes at its quoted price where the model's draft tier offers one, and an upscale of the master, a spend the tool will not price first (models.md "A higher resolution").

What a tool did differently from a page of this skill or of `docs/higgsfield/`, and a word that came out in a way the pronunciation page does not list, are written in the run's folder under the ledger and stay out of the message: whoever maintains the pack folds them into the pages.

## Hard rules

1. Only the reference and the product are asked for; everything else is derived, shown at the plan checkpoint, and changed on request.
2. Every checkpoint stops for the user unless the user gave the go-ahead; the cost is confirmed in every mode. No generation before the plan and the cost are approved.
3. The ad is an original concept built on what makes the reference work, in the reference's medium and look; the reference is followed scene by scene only when the user asks. Nothing of the reference (frame, clip, sound, person, line) is a model input or part of the output, even when it shows the product's own persona.
4. The story runs on a rule of the product's own world with a device from its vocabulary; the hook withholds the reveal; the script is written and the delivery directed to the reference's measured density, never to a mood.
5. The agent recommends a model family from a side-by-side estimate; the user confirms or picks the other. The latest general model of the family, found in the catalog at run time, never pinned.
6. Lowest tier only; cheapest image settings; one take per call, one shot at a time, `count` 1, no batch tool.
7. The cast is new: approved portraits, or the product site's own photos when the plan casts someone the site presents.
8. Every shot is animated from an approved still first frame, every shot carries a performance direction, and every image and take prompt carries the style line.
9. Every spoken word comes from the video model's native audio. No text-to-speech, dubbing or voice tools.
10. Overlays are code: captions, text, logos, end cards, inserts, in the brand's type and colors. Never asked of the video model.
11. Captions show the intended line; speech-to-text supplies timing only.
12. Two plain speech-to-text decodes (a small and a medium model, no prompt, voice detection off) decide what a take says; a decode prompted with the line never overrules them. Regenerate only ambiguous, broken, flat, drifted or dragging takes, or what the user asks for; close enough is accepted, except on key words. What a take says is settled before the user is asked to listen for it.
13. Every credit is preflighted, recorded, and never exceeds what the user accepted.
14. Free-trial unlimited generations only when the user asks; `use_unlim` set explicitly on every call.

## Terminology

| Term | Meaning |
|---|---|
| Reference video | The example the ad learns from: the user's, or one found among running ads when the user has none. |
| Concept | The new idea for the product that delivers the reference's mechanism with a different surface. |
| Rule of the world | The one sentence, "In this world, ...", that the story runs on; taken from what the product claims to know or do. |
| Device | The small concrete thing (an object, a number, a habit) that carries the rule and returns at the reveal. |
| Signature line | The quotable line in the figure's own voice that states the rule. |
| Reveal | The story's last fact, which re-reads everything before it in one step. |
| Density | The reference's measured speech rate, lines per ten seconds and longest pause; the script and the delivery are written to it. |
| Style line | The one sentence that fixes the medium and the look; repeated verbatim in every portrait, frame and take prompt. |
| First frame | The approved still a shot is animated from, carrying its starting emotion. |
| Performance | A shot's direction: emotion at the start, the turn, emotion at the end, delivery, eye line, action. |
| Intended line | The exact words a character says in a shot; the source of the captions. |
| Key word | A word that must come out right and must stay: the brand or product name, the product's own terms, the story's device, every word of the hook, the signature line and the reveal. |
| Prompt spelling | A word written in the take prompt the way it sounds; the intended line and the caption keep its spelling. |
| Preflight | A generation call with `get_cost: true`; a number, no job. |
| Budget ledger | Estimate, accepted budget and credits spent per item. |
| Clean master, captioned master | The assembled ad without and with captions; the second is the deliverable. |
