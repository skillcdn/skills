---
name: web-concept-variations
description: Shows four to six concept directions that get a reference's effect by other means, for a product, a post, a page, a deck or a campaign, from a reference the user gives or one found among what is working now. Use when a user says "show me five different ways to get this effect", "give me concept directions for this", "alternatives to this idea that still work the same way", "variations on this reference", or wants directions before a post, a deck, a page or an ad is made. Reads the reference for its intent, effect, aesthetics, fun, expected effect and the prior knowledge it rests on, finds other references that get the same effect on the open web, places candidates on the axes a concept can move on with one near and one far, judges each for the AI feel before it is shown, compares them on one sheet with a recommendation and a runner-up, and hands the pick to the skill that produces. The look of a direction is html-design-variations. Nothing is spent.
license: MIT
compatibility: Needs a web search tool and a way to read a page (a fetch tool, or a browser the agent drives) for the reference and the other references, and a file tool for the brief and the sheet. Works in any agent that can search the web; without search, the user supplies the other references as links or text.
metadata:
  author: skillcdn
  version: "1.1"
  tools: web
skillcdn:
  include:
    - assets/concept-run.example.md
    - /docs/variation/effect-brief.md
    - /docs/variation/axes.md
    - /docs/variation/not-ai.md
    - /docs/variation/comparison.md
  translations:
    ko:
      title: 레퍼런스의 효과를 다른 방법으로 내는 기획 방향 여러 개
      description: 레퍼런스(광고, 게시물, 페이지, 덱, 캠페인) 하나의 효과를 다른 방법으로 내는 기획 방향을 넷에서 여섯 개 보여 줍니다. 레퍼런스를 겉모습보다 먼저 효과로 읽고(의도, 효과, 미감, 재미 요소, 기대 효과, 전제 지식), 같은 효과를 다른 방법으로 내는 다른 레퍼런스를 웹에서 찾고, 기획이 움직일 수 있는 축(이해관계, 화자, 장치, 형식, 어조, 말하는 순서, 배경, 증거)에 후보를 놓되 가까운 것 하나와 먼 것 하나를 포함하고, 보여 주기 전에 "AI 느낌"을 판정하고, 추천과 차석이 있는 비교표 한 장으로 비교한 뒤, 고른 방향을 제작 스킬에 넘깁니다. "이 레퍼런스 효과를 내는 다른 방법 다섯 개 보여줘", "이 아이디어의 기획 방향 뽑아줘", "이 레퍼런스로 배리에이션"이라고 할 때, 게시물·덱·페이지·광고를 만들기 전에 방향이 필요할 때 쓰세요. 방향의 룩은 html-design-variations가 맡습니다. 비용이 들지 않습니다.
---
# Concept directions that get a reference's effect by other means

A reference and a subject go in (what the direction is for: a product, an account's next post, a page, a deck, a campaign); a sheet of four to six directions comes out, each a position on the axes a concept can move on, with the lines it would open with, judged for the AI feel before it is shown, with a recommendation and a runner-up, and the user's pick written as a handoff for the skill that makes the thing. The reference is read for what it does before what it looks like, so that the directions keep its mechanism and change everything the viewer would recognize; other references that get the same effect by other means are where the directions come from. Nothing here is produced in the final medium and nothing is spent: a direction is lines on a sheet, and the medium's own skill makes it.

## How the user is involved

- **Questions:** in one message, only what nothing at hand answers: the subject, when the request names only a reference ("directions for what: which product, account, page or deck?"); the subject's page or two lines about it, when the request names a subject that has neither ("where is its page, or what does it claim, in two lines?"); the audience, when neither the request nor the subject's page says ("who is it for: which market, and in which language will it run?"); and a reference described but not named, confirmed in the same message by the piece the search found ("I take the reference to be <the piece>; say so if not"), said in a first message even when nothing else is asked, and the run goes on without waiting for it. The reference itself is asked for only when the request has none and no research skill at hand can find one.
- **Checkpoint:** the sheet, once: the directions with their positions, the opening lines, the recommendation and the runner-up. The user picks one, merges two, asks for more on one axis, or disputes a reading; the pick is theirs and the run waits.
- **Go-ahead:** when the user says to go ahead alone, the sheet is still shown and the recommendation is taken as the pick, said so.
- **Changes mid-run:** a disputed reading re-opens the effect brief; a merge or "more on this axis" re-enters at the candidates and goes through the verdict again.

## Requirements

| What | Used for |
|---|---|
| A web search tool | Finding the other references that get the same effect, by the effect and the device; finding analyses of an old reference whose maker's account is public. Recognize it by its action: a query in, titles and links out. |
| A way to read a page in full: a fetch tool, or a browser the agent drives | Reading the reference's page, the subject's own page (its claims, its words, its persona) and the other references. A video is read from its public page, its description, its transcript or its analyses; it is never downloaded here. |
| A file tool | The effect brief, the candidates, the sheet and the handoff, written in a run folder. |
| Optional: a research skill of the pack for the medium (ads running now, an account's posts) | Finding a reference when the request has none, or the other references for that medium; its method and its checkpoint are its own and are not cut short. |

Check search and a page reader before the first message; without search, say so and ask the user for three other references as links or text. The method every variation skill shares is in the repository's document set [`docs/variation/`](/docs/variation/README.md): [effect-brief.md](/docs/variation/effect-brief.md), [axes.md](/docs/variation/axes.md), [not-ai.md](/docs/variation/not-ai.md) and [comparison.md](/docs/variation/comparison.md) are included and arrive with this skill wherever SkillCDN serves it; [handoff.md](/docs/variation/handoff.md) is read when phase 6 comes, through the repository connection. The shared pages live under `docs/variation/`, outside this directory: a copy of this directory and the area's plugin have none of them, and a mount of one area or one skill has the included ones only; say so and fetch what is missing from `docs/variation/` of the repository this skill comes from (for this pack, `github.com/skillcdn/skills`). The shape of every artifact is in [concept-run.example.md](assets/concept-run.example.md), which comes with the skill.

## Inputs

| Input | Source |
|---|---|
| The reference | A link, a file or a description in the request: an ad, a post, a page, a deck, a scene, a campaign. A described piece is identified by search before the first message and named in it for a yes; the two nearest are named when several fit, and the description itself is read as the reference when none does, said so in the brief. With no reference at all, one is found by the pack's research skill for the medium (for a product's ad, the one that reads running ads) when its Requirements are met here, choosing among what it returns by the effect wanted, said in a line, with that skill's own checkpoint as one more stop; with no such skill, asked for. |
| The subject | What the directions are for, from the request; asked when it names only a reference. Its own page is read for its claims, its words and its persona, which, with the user's own sentences, are the only claims a direction may make; a subject with no page is read from the user's two lines, and the brief says so. |
| The audience | Derived from the subject's page or the request (who it is for, which market, which language; the request's own language when nothing else says); asked when neither says, as "who is it for: which market, and in which language will it run?". |
| The medium of the piece | From the request where it says (a page, a post, a deck, a video); else the reference's own medium and length, which the brief keeps, said in the first message. |
| Where the run goes | Derived: the folder the user names, else `variations/<the subject in a few words>/` under the working folder, under the host's scratch folder when the working folder is a git checkout, and beside the working folder when there is no scratch folder; said in the first message. The run's files never enter a repository. |

## Workflow

Each phase produces a named artifact in the run folder (`effect-brief.md`, `candidates.md`, `verdict.md`, `sheet.md`, `handoff.md`); the shapes are in [concept-run.example.md](assets/concept-run.example.md). Each phase ends with a line to the user; a candidate's lines are shown only at the sheet, after the verdict.

### Phase 1: The effect brief

Produces the **effect brief** (`effect-brief.md`), by [effect-brief.md](/docs/variation/effect-brief.md): the six readings, each one entry with its evidence and where it was read (the piece itself, its public description, the account of whoever had it made, an analysis, the user's own words), the mechanism line with the rule of the piece's world where it tells a story, what stays and what is free. An old or famous reference is read from what is public about it as much as from the piece; a video read from its page, its transcript or its analyses places its moments by beat and not by seconds, and says so. A reading of "none" counts as written; where Effect or Fun is none the mechanism line cannot be written, and the brief is shown to the user for the reading they can supply (what the piece did for them) before any candidate. The phase ends with the six readings in six lines to the user.

### Phase 2: Other references

Adds to the brief the **other references** (three to five): pieces that get the same Effect reading by other means, found by that effect and the device in a short phrase each ("a figure's one exception to their own rule", "the maker doing the work on camera", "a thing named exactly where the genre stays vague"), never by the subject's category alone, which returns the category's lookalikes. The category search is run once all the same, and the positions every result of it shares (the opening, the proof, the offer line, the look) are recorded in the brief as the **crowd**, which the far candidate leaves. The pack's research skill does the finding for a medium it covers when its Requirements are met here, with its own checkpoint as one more stop, said so. For each reference: where it was seen, what it keeps of the mechanism, what it does differently to the same end, in one line; these are cited, never reused. Three searches by effect and device that find fewer than three pieces exhaust the search: the brief says what was tried, and the user is asked, as this phase's one question, for pieces that had the effect on them. The phase ends with the references in one line each.

### Phase 3: Candidates on the axes

Produces the **candidates** (`candidates.md`), by [axes.md](/docs/variation/axes.md): four to six, each a position on two or three concept axes with the rest held at the reference's position, written as positions before any line is written, the reference's own positions as the first row so that "holds" has a value. The device moves in every candidate, because the reference's device is the reference's: one near (the device alone moved, to another device that carries the same rule: the control), one far (two or three of the crowd's positions left, the mechanism line held), the rest on different sets of axes. For each, the rule of its world in one sentence ("In this world, ..."), the opening lines, the signature line and the reveal or the ask as they would be read or spoken in the audience's language, then the mechanism line with this candidate's device and figure in it; a position is written in the producing skill's vocabulary where the medium and the skill are known, else in plain words. A candidate that moves on every axis, or that differs from another in words only, is remade. The phase ends with the positions as a table to the user, names and axes only.

### Phase 4: The verdict

Produces the **verdict** (`verdict.md`), by [not-ai.md](/docs/variation/not-ai.md): every candidate against the signals in words and in a story, quoted by their row in a few words, the bundles, and the positive tests (the thumb test, take the product away, a person chose this, the reference's followers would not name it, and, on the set as a whole, one is not like the others), with what failed and the fix made; a signal kept on purpose is named with its reason, which the sheet's verdict column carries. A candidate that cannot be fixed on its axes is dropped and replaced; none is carried to the sheet failing. The phase ends with one line per candidate on what was fixed.

### Phase 5: The sheet

Produces the **sheet** (`sheet.md`), by [comparison.md](/docs/variation/comparison.md): one row per candidate (name, position, mechanism, keeps and changes, verdict, risk, to produce in the medium's own units where the medium is known and never a figure of money or credits, the opening lines and the signature line), the recommendation argued in the brief's readings, the runner-up with what it would give instead, the far candidate's reason for being there.

Checkpoint, in plain words: the readings in six lines; the directions as a numbered list, each with its axes moved, its opening lines, its risk; the recommendation and why; the runner-up and what it would give instead; the far one's reason; "pick a number, merge two, ask for more on an axis, or say which reading is wrong"; "ok" takes the recommendation. The pick is the user's; the run waits.

### Phase 6: The handoff

Produces the **handoff** (`handoff.md`), by [handoff.md](/docs/variation/handoff.md): the brief, the pick's row, the mechanism line and the rule, what must stay, the sample, the fixes, the other references by where seen, the assumptions the run rests on (which piece was read, the market, the medium) and what was left out, and the producing skill's inputs filled as far as the pick fills them, in that skill's vocabulary where the skill is known. A merge, or more on an axis, is placed on the axes, judged, and shown once more on the sheet within six, the weakest kept ones dropped, before it is handed off. The delivery: the run folder's path, the pick in one line, the producing skill to start next (or that the pack has none for this medium, in which case the handoff is the brief for whoever makes it, and the looks skill is named for the piece's cover or first screen) and what it will ask that the pick does not answer, and that nothing was made in the medium here.

## Verdicts

| Result | Verdict |
|---|---|
| A reading written as a paragraph, or about the genre and not the piece | Redo: one entry (a sentence, or one per moment or choice), with the device, from the evidence |
| Effect or Fun read as "none" | The brief is shown and the user supplies what the piece did for them; no candidate before |
| Other references found by the subject, or fewer than three | Redo: search by the effect and the device; with search exhausted, ask the user for pieces that had the effect on them |
| A candidate that keeps the reference's device, or moves on every axis | Redo: the device moved; two or three axes, the rest held at the reference's position |
| Two candidates that differ in words only | Redo: one of them on another set of axes |
| A candidate that fails a signal or a positive test | Fix on its axes; drop and replace when the fix moves it onto another candidate's axes |
| A sheet with no near or no far candidate, or more than six | Redo: the near one is the control and the far one the open angle |
| A recommendation argued by taste | Redo: argued in the readings |
| A "to produce" the medium's pages do not give | Left as "not estimated here"; never a figure of this skill's own |

## Hard rules

1. Effect before surface. No candidate is written before the six readings and the mechanism line are; a direction that keeps the reference's words, people, marks or device is the reference and is not a direction.
2. Other references are read and cited, never reused. A line that is any of theirs with the words swapped is rewritten.
3. Every claim a direction makes about the subject comes from the subject's own page or the user. A proof the subject cannot supply is not a candidate's proof.
4. The verdict is a phase, before the sheet, and nothing fails it in public: a candidate is fixed or replaced before the user sees it. The user's word for what this prevents is "it sounds like AI".
5. The pick is the user's, at the sheet; the skill recommends and never chooses. A go-ahead takes the recommendation and says so.
6. Nothing is produced in the medium and nothing is spent. The handoff is in the producing skill's terms; that skill is started by the user and estimates its own cost.

## Terminology

| Term | Meaning |
|---|---|
| Reference | The piece whose effect the directions keep. |
| Subject | What the directions are for: a product, an account, a page, a deck, a campaign. |
| Reading | One of the six sentences of the effect brief: intent, effect, aesthetics, fun, expected effect, prior knowledge. |
| Mechanism line | The one sentence that joins the readings; what every direction keeps. |
| Rule | The sentence a story's world runs on, "In this world, ..."; the device carries it, and every candidate writes its own. |
| Device | The one concrete thing that carries the rule: an object, a number, a habit, an act, a line. Never the piece's premise (a confession, a refusal, a tour), which is its genre and order of telling and may hold. The reference's device is never taken. |
| Axis | A dimension a concept moves on: stake, figure, device, form, genre and register, order of telling, setting, proof. |
| Crowd | The positions every piece of the subject's category shares, recorded from one category search; what the far candidate leaves. |
| Near, far | The candidate that moves the device alone (the control); the one that leaves two or three of the crowd's positions (the open angle). |
| Verdict | The pass of every candidate against the AI-feel signals and the positive tests, before the sheet. |
| Sheet | The comparison the user picks from: positions, mechanisms, samples, a recommendation and a runner-up. |
| Handoff | The pick written in the producing skill's own terms, for the user to start that skill with. |
