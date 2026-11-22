---
name: web-news-anchor-report-script
description: Writes the script of a news anchor report from a sourced story, with the screen planned cut by cut for a video made later, about ninety seconds unless asked otherwise. Use when a user says "write an anchor report on this", "a news script for an anchor to read", "뉴스 앵커 리포트 써줘" or "뉴스 대본 써줘", or wants this week's story told as broadcast news. The facts come from a topic brief, which web-card-news-topic-brief researches first, without images, when the user brings none; a card news post from the same brief is html-card-news-from-brief, and the spoken lines of a drama or an ad are higgsfield-shorts-drama and higgsfield-shorts-ad. Leads from the viewer's side, writes short sentences as an anchor says them, each with one job and the form that says how it is known, plans the screen as graphics and labelled generated scenes, has a listener with only the script hear it once before the user does, and measures the spoken length. No video is generated and nothing is spent.
license: MIT
compatibility: Needs the tools of the topic brief skill when the story is still to be researched (a web search tool, a page reader, a shell) and a way to start an agent with none of the session's context for the cold listen (a subagent tool, or a second session the user opens); a shell counts the spoken length where there is one. Works in any agent that can write files.
metadata:
  author: skillcdn
  version: "1.5"
  tools: web
skillcdn:
  include:
    - references/script.md
  translations:
    ko:
      title: 출처가 붙은 뉴스 앵커 리포트 대본
      description: 출처가 확인된 이야기로 뉴스 앵커 리포트 대본을 씁니다. 나중에 영상으로 만들 수 있게 화면을 컷 단위로 함께 짜고, 따로 말하지 않으면 약 90초 분량입니다. "이걸로 앵커 리포트 써줘", "앵커가 읽을 뉴스 대본", "뉴스 앵커 리포트 써줘", "뉴스 대본 써줘"라고 하거나 이번 주 이야기를 방송 뉴스처럼 전하고 싶을 때 쓰세요. 사실은 소재 브리프에서 가져오며, 브리프가 없으면 web-card-news-topic-brief가 이미지 없이 먼저 조사합니다. 같은 브리프로 카드뉴스를 만드는 일은 html-card-news-from-brief가, 드라마나 광고의 대사는 higgsfield-shorts-drama와 higgsfield-shorts-ad가 맡습니다. 첫 멘트는 시청자 쪽에서 시작하고, 앵커가 말하듯 짧은 문장으로 쓰되 문장마다 맡은 일 하나와 어떻게 알게 된 내용인지 드러나는 어미를 주며, 그래픽과 표시를 단 생성 장면으로 화면을 짜고, 대본만 받은 청자가 한 번 들어 본 뒤에 사용자에게 보이며, 말하는 길이를 잽니다. 영상은 만들지 않고 비용도 들지 않습니다.
---
# The script of a news anchor report, with its screen

A story goes in: a topic brief, or a request that the pack's research skill turns into one. Out comes one file, `script.md`: the report as the anchor says it, in running paragraphs; the sentence table, which gives each sentence its number, its job and the facts it rests on; the cut sheet that says what the viewer sees under every sentence; and the list of what to confirm before it airs. The form is the anchor report, a news item the anchor tells alone with no reporter's piece: the lead on camera, a handover to the screen, then the anchor's voice over graphics and scenes to a close.

A viewer hears a report once and cannot go back, and the writer, having read the brief, cannot hear it as one: a script whose every sentence is true to its source can still leave a viewer lost. So three things are checked apart: the facts against their sources; the form of each sentence against [script.md](references/script.md), which says what the report tells and in what order, and [spoken.md](references/spoken.md), which says how a sentence is said; and the sense by a listener who is given the script and nothing else.

## How the user is involved

- **Questions:** one message at the start, only for what the request leaves open. With no story named and no brief: "Which field of news should I look in? I will bring this week's candidates and you pick one." An answer that leaves it open is the week's main news across fields. The length (ninety seconds) and the air date (today) are derived, said in that message and changed on a word. No reference is asked for: the form is the genre's and this skill's own, and no look is made here; a report the user names is followed for its form.
- **Checkpoints:** the research skill's own, when it runs; then one of this skill's, after the checks: the script itself, as it is read, with what the message of phase 5 lists. "OK" delivers.
- **Go-ahead:** when the user says to go ahead alone, the script checkpoint is skipped and the delivery carries the script and the same lists. The pick of the story stays the user's.
- **Changes mid-run:** a note on one sentence's wording, length or ending names a habit of the draft, so every sentence that has it is rewritten, and the delivery lists the phrase before and after. "Start from something else" re-enters at the plan: the lead, its picture, and where what the lead held now goes. "I do not see what this sentence is for" and "what do these two have to do with each other" send the sentence to the brief: its job or its link is found there and said, or the sentence goes; a rewording alone answers neither. A fact the user doubts is read again in its article. After any change the length is measured and the script heard cold again before it is shown.

## Requirements

| What | Used for |
|---|---|
| A topic brief (a folder with `topic-brief.json` and `facts.md`), or the pack's research skill, [web-card-news-topic-brief](/product/skills/web-card-news-topic-brief/SKILL.md), with the tools it names | The facts with their source sentences, the angle, what is unverified. |
| A way to start an agent with none of this session's context: a subagent tool, or a second session the user opens ([fresh-agents.md](/engineering/docs/skillcdn/fresh-agents.md)) | The cold listen ([cold-listen.md](references/cold-listen.md)). Without either, say so before the first sentence is written; the delivery then says the script was not heard cold. |
| Optional: a shell | Counting the spoken length. Without one it is counted by hand, sentence by sentence. |

Check these before the first message. Nothing here costs money. [script.md](references/script.md) arrives with this skill; every other page is read when the phase that names it begins. Links that start with `/` are files of the pack this skill is from: a copy of this directory, a plugin or a mount below the root that lacks one reads it through the pack's connection (`https://skillcdn.ai/gh/skillcdn/skills`) or at `github.com/skillcdn/skills`.

The area's rule that a text is as firm as its sources takes this form here: every sentence the anchor says, the lead and the close included, and every word on the screen is a fact of the brief said for the ear; nothing the brief lists as unverified is said; and what rests on one outlet is listed for the user to confirm before it airs.

## Inputs

| Input | Source |
|---|---|
| The story | A brief folder the user names, or a story named in the request, which the research skill takes as the pick. With neither, the field the user names: the research skill finds this week's candidates in it, and the user picks. |
| The brief | The research skill's, run first when the user has none and started with these as its inputs, which answer its own questions: the categories are the field; the brief is for an anchor report script, takes no images, and this skill writes from it next; the readers are the report's viewers (people who know nothing of the subject, unless the request says who watches); the stance is a report and the tone calm unless the request says otherwise; its files go under `anchor-report/`, the candidate list there and the brief in `<story>/brief/`. Its pick and its brief checkpoint stay its own stops. Articles, a release or notes the user brings go to it as that story's sources, so that the facts table is made the same way. |
| The reference | A report the user names, as a link or a pasted script. It gives its form only ([reference.md](references/reference.md)). None is asked for, and with none the form is this skill's own. |
| Length | The request's; else ninety seconds. |
| Air date | The request's; else the day the script is written. Every "yesterday" and "next week" in the script rests on it. |
| Viewers, stance, tone, language | The brief's `audience`, `stance` and `tone`; the script is in the brief's language. |
| Where it goes | The folder the user names, else `anchor-report/<story in a few plain words>/` under the working folder (under the host's scratch folder when the working folder is a git checkout, under the user's home without one), holding `script.md`, the brief in `brief/` (a copy where the user brought one) and the working files in `work/`. Said in the message that creates it. |
| Everything else | Derived and shown at the checkpoint: the thread, the lead and its picture, the parts, what is left out. |

## Workflow

Each phase produces a named part of `script.md`, in this order: the plan, the script and its sentence table, the cut sheet, the checks, before air.

### Phase 1: The brief

Produces the **brief**. Take the folder the user names, or run the research skill with the inputs above, at its own stops. Read the result whole, by [topic-brief.md](/docs/card-news/topic-brief.md): `facts` with their source sentences and their `single_source` marks, `angle` with its outlet, `disagreements`, `unverified`, `audience`. Where the research skill ran, its brief checkpoint was the stop for this; a brief the user brought is said in a line (how many facts, the angle with its outlet) with the length and the air date, and the run goes on.

### Phase 2: The plan

Produces the **plan**, by [script.md](references/script.md) "The thread", "The lead" and "Parts and their jobs", and by [screen.md](references/screen.md) "What a screen can be", read now so that the opening picture is one the screen may show. A report the user named is read first, by [reference.md](references/reference.md).

1. Write the thread: the report in one sentence, from the brief's angle.
2. Choose the lead from the viewer's side, as strong as the facts and no stronger, and the opening picture with it. Choose the close with it: where what the lead opened on goes from here, and the fact kept for saying so.
3. Sort the facts. For each one that might enter, write its link to the thread in a clause the brief supports; a fact with no such clause is left out and listed with the reason. Of causes, demands or measures, two are told: those the brief's outlets weigh most.
4. For each case the report would tell (something that happened to someone), find in the brief why one thing led to the next. Where the brief gives the events and not the cause, the question goes back to the research skill, which reads the brief's articles again and one more in full and adds what it finds to the brief as a fact with its source sentence; with no answer the case is left out, and the count it belongs to stays.
5. Order the parts, each with its job and its fact ids, and split the length among them, the lead the shortest.

Say the thread and the lead in two lines, and go on.

### Phase 3: The script

Produces the **script** and its **sentence table**. Before the first sentence, read [spoken.md](references/spoken.md), whose last section is the record of what users corrected in the script's language, then [readers.md](/docs/writing/readers.md), [sentences.md](/docs/writing/sentences.md) and [facts.md](/docs/writing/facts.md) of the writing set; script.md and spoken.md are their sharper form for a spoken report and win where they differ.

Write the report as the anchor says it, by script.md for what each sentence is for and by spoken.md for how it is said: running speech in short paragraphs, a paragraph to a part, the two stretches marked (on camera, over the screen), with no numbers and no fact ids in it. Under it keep the sentence table, a row to a sentence: its number, its first words, its job in a few words, how its content is known, its fact ids. Count the spoken length as soon as the draft stands (script.md "Length"), and the count over the sentences with it (spoken.md "One breath, one point"); cut to the target before the screen is planned.

### Phase 4: The screen

Produces the **cut sheet**, by [screen.md](references/screen.md): one row per cut with its sentences, its seconds, what the screen is and where it would come from, the text on screen, and the facts that text rests on.

### Phase 5: The checks

Produces the **checks**, in this order, each recorded with its result.

1. **Facts.** Every sentence, and every text on screen, against the source sentences of its facts; a quote word for word; nothing from `unverified`. A sentence that leaves out a condition of its source for the ear passes where no viewer would take it to mean otherwise.
2. **Form.** Every sentence against script.md and spoken.md, by its row of the sentence table: its job named in a few words, its ending or its attribution matched to how its content is known, no word its point does not need and none the newscast would not use, one number, terms explained where they first come. Then the script in order, said aloud: each opening tied to what came before, a sentence that sets up followed by one that lands, no one ending throughout, what the lead named said again where the body reaches it, two of a kind at most, the close answering the lead. Then as text, against [not-ai.md](/docs/variation/not-ai.md) "Signals in words".
3. **The cold listen**, by [cold-listen.md](references/cold-listen.md): a fresh listener with only the script reports where it stumbled; rewrite and listen again as that page says.
4. **Length.** The final text counted again as script.md "Length" says, within a twentieth of the target, and the count over the sentences beside it.

A rewrite made for one check is taken through the others again: a sentence cut for length is heard again, and a link added for the listener is counted again. Then write **before air** into `script.md`, as phase 6 lists it.

Checkpoint, in plain words: the script itself, whole, as it is read; the thread in a line; the measured length; the cuts in a line (how many, and what must be made: graphics, generated scenes); what the last listener still stumbled on and why it stays; what was left out and why; what to confirm before air. "OK" delivers.

### Phase 6: Deliver

One message: the path of `script.md`; the script itself; the length; what the cut sheet asks a video stage to make; **before air** (each fact that rests on one outlet, each quote that is another outlet's reporting and is named so on screen, what the sources do not say, and that anything after the brief's last article is unread); what a video stage still decides, which is its own job with its own estimate: the voice of the narrated part, the model, the cost; and each wording the user corrected in this run, as the phrase before and after, for the record at the end of spoken.md. Working files (article text, scripts) stay in the report's folder, under `work/`, and are named. Nothing is published and nothing is sent.

## Verdicts

| Result | Verdict |
|---|---|
| A sentence, or a text on screen, with no fact of the brief under it | Cut, or traced; never kept for its sound |
| A lead that states an effect the sources only fear, or sizes it past their count | Rewritten to the strength of the facts |

## Hard rules

1. Every sentence and every text on screen rests on a fact of the brief, the lead and the close included. A lead written for effect past its sources is the first thing a viewer who knows the story catches.
2. A sentence says how its content is known. What someone announced, demanded, counted, said or expects is never stated flat in the anchor's own voice, because the viewer hears that as the newsroom vouching for it.
3. A sentence has one job the listener could name.
4. Wording never supplies a link the sources lack: a cause between two events, or how a neighbouring event bears on the story.
5. A reference gives its form only. Its story, its people, its sentences and its outlet's name enter neither the script nor any file the run keeps. A source of the brief that is itself a broadcast report gives its facts, as any article does, and none of its wording.
6. A script that no listener with only the script has heard is not shown as checked: the delivery says so.
7. A generated scene is labelled as generated and never stands for the event itself.
8. No video and no image is generated here.

## Terminology

| Term | Meaning |
|---|---|
| Lead | What the anchor says on camera before the handover. |
| Thread | The report in one sentence; what every part serves. |
| Sentence table | The rows under the script, one a sentence: its number, its first words, its job, how its content is known, its fact ids. Its numbers serve the checks, the listener's copy and the cut sheet; the script itself carries none. |
| Cut sheet | The table of cuts, each a stretch of the report under one picture: its sentences, its seconds, the screen and where it comes from, the text on screen. |
| Cold listen | One hearing of the script by an agent that has the script and nothing else. |
| Before air | The list of what the user confirms before the report is shown to anyone. |
