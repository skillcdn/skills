---
name: html-card-news-batch
description: "Makes several card news posts at once from picked topics and one format. A worker agent per post runs the research and the build in the post's own folder, a reviewer that made none of them reads each against its brief, and the posts come back together at review with a contact sheet each. Use when a user says \"make ten posts from these topics\", \"make this week's batch\", \"do all of these at once\" or \"remake every booked post with this change\". Each post is made by web-card-news-topic-brief and html-card-news-from-brief, where a request for one post starts; approved posts are booked by instagram-post-scheduling. Needs a host that starts agents side by side, and without one makes the posts one after another. Costs the tokens of its workers, estimated before any starts; nothing is posted."
license: MIT
compatibility: Needs a host tool that starts agents side by side and resumes one with a message, the pack in each of them, and what the research and the build need (a web search tool, a page reader, a shell with Node.js, a Chromium-family browser). Without such a tool the posts are made one after another.
metadata:
  author: skillcdn
  version: "1.1"
  tools: browser
skillcdn:
  include:
    - references/worker-brief.md
  translations:
    ko:
      title: 카드뉴스 여러 건 한 번에 만들기 (게시물마다 워커, 만들지 않은 리뷰어)
      description: 고른 소재 여러 건과 포맷 하나로 카드뉴스 게시물을 한 번에 만듭니다. 게시물마다 워커 에이전트 하나가 자기 폴더에서 조사와 제작을 끝까지 하고, 그 게시물을 만들지 않은 새 리뷰어가 브리프와 대조해 읽으며, 통과한 게시물을 컨택트 시트와 함께 한 메시지로 모아 승인을 받습니다. "이 소재들로 10건 만들어", "이번 주 배치 만들어", "이거 한꺼번에 다 만들어", "예약된 게시물 전부 이렇게 바꿔서 다시 만들어"라고 할 때 쓰세요. 게시물 하나는 web-card-news-topic-brief와 html-card-news-from-brief가 만들고, 한 건만 만들 때는 그 스킬에서 시작합니다. 승인된 게시물의 예약은 instagram-post-scheduling이 합니다. 에이전트를 나란히 띄울 수 있는 호스트가 필요하고, 없으면 한 건씩 차례로 만듭니다. 워커가 쓰는 토큰은 시작 전에 추정해 보여 드리고, 게시는 하지 않습니다.
---
# Card news in a batch: a worker per post, a reviewer that made none

Picked topics and one format go in; that many posts come out at review, each in its own folder with its brief, its slides and its caption, gathered in one message with a contact sheet per post. The skill is the orchestration alone. Every post is made by the two skills that make one, [web-card-news-topic-brief](/product/skills/web-card-news-topic-brief/SKILL.md) and [html-card-news-from-brief](/design/skills/html-card-news-from-brief/SKILL.md), run by a worker agent that is handed everything those skills would ask, so that it never stops; it is read by a reviewer that made none of it; and this session, the orchestrator, keeps what only one agent may hold: the picks, the ledger, the number of slides, the fixes and the person's approval.

## How the user is involved

- **Questions:** the topics, where the request gives a count and no stories: the research's candidate list is shown and the person picks ("Which of these? Numbers, or 'the top N'"); the count, where neither the request nor the account's policy gives one ("How many posts?"); the format, where none is beside the run, as the build asks for it. What a post's research and build would ask is answered once for the whole batch, at the plan.
- **Checkpoints:** the batch plan with its estimate, and the delivery, where the person approves post by post. The two skills' own checkpoints are not shown: the workers run under a go-ahead.
- **Go-ahead:** "go ahead alone" skips nothing here (hard rule 3).
- **Changes mid-run:** a change for every post ("shorter", "calmer", "video first") goes to every worker in one line, and each post is rendered and reviewed again; a change to one post goes to that post's worker. "I cannot follow these" at the delivery means clarity, not facts: each post goes back to its worker with the slide the person halted at, and a new reviewer gives it a first read. More posts than the estimate named is a new estimate.

## Requirements

| What | Used for |
|---|---|
| A tool that starts agents side by side with a model and an effort setting each, and a message that resumes one (in Claude Code, `Agent` and `SendMessage`, checked 2026-11): a brief in, the agent's last message out, an id that takes a further message | The workers and the reviewers. Each host's way is in [fresh-agents.md](/engineering/docs/skillcdn/fresh-agents.md) "A subagent"; where a batch departs from that page is tool-notes.md "Side by side". |
| The pack, in this session and in every agent it starts: the repository connection, or the skills where the host keeps them | This session loads both skills whole before phase 1 and works by them at the plan, the fixes and the alternative; a worker loads them again itself, a reviewer the build's verdicts. |
| What the two skills need: a web search tool, a page reader, a shell with Node.js, a Chromium-family browser `playwright-core` can launch | Checked once here, as each skill's Requirements say: every worker meets the same host. |
| A way to show images, or their paths | The contact sheets at the delivery. |

Check all four before the first message. Without the second or the third, stop and say what to add. Without the first, say so and offer the one alternative, the posts made one after another in this session, as tool-notes.md "One after another" says.

Links that start with `/` are files of the pack this skill is from: a copy of this directory, a plugin or a mount below the root that lacks one reads it through the pack's connection (`https://skillcdn.ai/gh/skillcdn/skills`) or at `github.com/skillcdn/skills`.

The area's rule to check the render takes this form here: every post is judged on its rendered slides by its worker in the build's review, by this session on the contact sheet and by the reviewer at phone size.

## Inputs

| Input | Source |
|---|---|
| Topics | The request's list, each a line with its links where the person has them; else the person's picks from the research's candidate list (`web-card-news-topic-brief`), made just before or run now to its candidate checkpoint and asked for enough cards to pick the batch from. A line without two articles has them searched for at the plan. For a remake ("remake every booked post with video") the posts are existing folders, and each brief carries the change in place of a topic. |
| Count | The request's; else what the account's policy gives for the days named; else asked. |
| Format | One spec for the batch: the account's (`formats/<name>/`), the folder the request names, or the one beside the run. With none, the format comes first, by the build's routes at their own stops, before the plan. |
| Readers, stance and tone, voice, pictures | The account's policy, each line handed to the workers as written. Without a policy, the request's words, and for what they leave open the research's own question, asked once at the plan for the whole batch. |
| Slides per post | Derived as the build's own count (the spec's `canvas.slides_per_post.typical`, within the `slides` range of the post kind's build under `kinds`), handed to the worker as a ceiling. |
| Roles | Derived from what the host's tool offers, read from its own parameters and said at the plan. A **worker** runs one tier below the model this session runs on, at a high effort setting, never a lower one. A **reviewer** is a new agent per post, of the worker's tier at a high effort setting. A tool that takes no model starts them on this session's model, and the estimate says so. |
| Workers at once | Derived: the batch in one wave up to ten, a larger one in waves of ten (tool-notes.md "Side by side"). |
| Where the posts go | In an account, `posts/<YYYY-MM-DD-slug>/` each, the brief folder and the post folder one. Elsewhere `card-news/<story>/` each, where the research puts a brief folder, the post in its `post/`. This session names every folder, so that no two workers choose one name. |
| The batch folder | Derived: `batch-<YYYY-MM-DD>/` under the host's scratch folder, with `batch.md`, a scratch folder per worker and the contact sheet script. None of it is delivered. |

## Workflow

### Phase 1: Plan

Read [tool-notes.md](references/tool-notes.md) before this phase. Produces the **batch record** (`batch.md`: a row per post with its topic, sources, folders, port, worker, reviewer and researcher ids, return, verdict and state) and the first checkpoint.

1. Settle the topics, the count and the format. In an account, read [account.md](/docs/card-news/account.md), then the policy and the ledger, first: a named topic that overlaps a row goes into the plan with the rule that caught it, and the days of "this week" are the policy's Cadence, else asked.
2. Mark the delicate topics.
3. Choose the roles, and estimate: per post, one worker and two reviewer passes, at the sizes of tool-notes.md "What a batch costs", illustrative until this batch's first return replaces them.

Checkpoint, one message: the posts in a numbered list (the topic line, its sources, its folder, delicate or not); the format and the ceiling; the answers every worker will carry (readers, stance, tone, the policy's lines); the roles as chosen and how many run at once; whether the browser driver is borrowed or will be installed; the estimate in tokens and minutes, marked rough. "OK" starts the workers. The run waits, whatever was said before: this is the consent to spend.

### Phase 2: Prepare

Produces the **post folders** and a filled **worker brief** per post.

1. The folders. In an account each pick gets its folder, its ledger row and its `post.json` at `idea`, as account.md says, by the repository's own command where it has one; elsewhere an empty brief folder.
2. The browser: `playwright-core` resolved once, borrowed or installed into the tools folder as the build's Requirements say, its `PLAYWRIGHT_FROM` path written into every brief. A worker installs nothing.
3. A port per worker for the build's preview server, which otherwise all take the same one, and a scratch folder per worker.
4. A delicate topic has its research run first, beside the wave, by an agent of this session's tier started with the worker's brief and the line "stop after the research's delivery"; its worker starts from the finished brief when that agent returns. In such stories that research overturned the topic line's premise in two posts of three: a story that is then no longer the one picked leaves the batch with its reason.
5. Fill the block of [worker-brief.md](references/worker-brief.md) for each post. A topic line taken from a candidate card says so.

### Phase 3: Workers

Produces the **returns**. Start the workers of a wave in one message, each with its brief and nothing else, at the worker's model and effort, in this checkout and not an isolated copy of it, in the background where the host allows. Record each id in `batch.md` as it starts: a fix goes back to the same agent.

While they run, this session keeps to hard rule 1. A worker that ends without its return block is resumed once with "finish and return the block"; one that cannot be resumed is replaced by a new worker with the same brief and the line "the folder holds the work so far: go on from it".

### Phase 4: Gather

Produces a **contact sheet** per post (`out/contact-sheet.png` in its post folder) and this session's own check of each.

1. For each `draft` returned, see that the files the build delivers are there and the PNGs number what the return says. Make the sheet with [contact-sheet.example.mjs](scripts/contact-sheet.example.mjs), or as [rendering-html.md](/docs/browser/rendering-html.md) "A contact sheet of many pages" says, and look at it.
2. Hold it against what a worker gets wrong most: more slides than the ceiling, or a slide with nothing to say; a cover that does not show what its headline names; a picture that only relates to the story; one picture used twice. Then hold the posts against each other, which no worker could: two with the same sequence of slide types, where the build varies it, is a fix for the later one.
3. Where the repository has a check of its own, run it on the post folders.

What fails here is settled before any reviewer reads the post (Verdicts).

### Phase 5: Review

Produces the **verdicts**. Start one reviewer per clean post, all in one message, each with [reviewer-brief.md](references/reviewer-brief.md) filled and nothing else (hard rule 2).

Rule on each list of fixes before anything goes back (hard rule 5), and drop a point that is taste in wording. Then:

- **Fixes.** A fix of a line or two this session makes in the slide plan itself, once that post's worker has returned, and renders again by the build's export and review. Anything more goes to the worker that made the post, resumed with its context, in one message: each item with what is wrong, where, and the limit it must stay within (the spec's characters per line for that element); and the slides to cut. The worker returns the same block.
- **Second pass.** The same reviewer, resumed, reads the fixes and what they touched. Two passes are the most.
- **A pass.** The sheet is made again where slides changed. In an account the post's `post.json` goes to `review` and its ledger row with it, both written by this session, by the repository's command where it has one.

### Phase 6: Deliver

One message. Per post: the contact sheet attached, or its path; the headline, the folder and the slide count; the reviewer's verdict with what was fixed after it; what was corrected in the topic line; the brief's unverified items and anything a person must decide. Then the posts that left the batch, each with its reason; the tokens and the time against the estimate; and "Which may be posted? Numbers, or all."

In an account the answer is written to each named post's record as `approved`, with when and by whom, the ledger following as at a pass; booking is [instagram-post-scheduling](/marketing/skills/instagram-post-scheduling/SKILL.md)'s, and a remade post that was already booked keeps its booking until the person approves the remake. In a repository the posts are committed as its agreement (`AGENTS.md`) says.

## Verdicts

Read before phase 4 and before a fix goes back.

| Result | Verdict |
|---|---|
| A return that is not the block, files missing, slides over the ceiling, problems the build's review left | Back to the same worker, once, before any reviewer |
| `blocked`, or no return after one resume | The post leaves the batch, its folder kept and its reason said at the delivery; this session makes it with the two skills on the person's word |
| `unchanged` on a remake: nothing usable was found and no file changed | Accept: a normal result, with nothing to review |
| A cover filled with a picture that only relates, for want of one of the event | Fix: a picture or a document of the event itself, else the beat without a picture, as the build's verdicts say |
| `fix` again after the second pass, or `reject` | The post leaves the batch, as a `blocked` one does |
| The running count of tokens passes the estimate | Stop and ask before another agent starts |

## Hard rules

1. One writer per file. A worker writes its own two folders and its scratch folder; the ledger, every record outside a post's folder, git and the board are this session's, and it writes no post folder and runs no git command while a worker is writing. Two workers that shared a scratch folder overwrote each other's script, and a pull that stashed took the folders from under workers still writing.
2. The reviewer made nothing of the post it reads and is given no word of its worker's; its fixes are checked by the same reviewer. Posts their makers had reviewed and passed each showed a fresh reader a problem on the first pass.
3. The picks, the word on the estimate and `approved` are the person's. No worker starts before that word, the running count is held against the estimate, and a post goes no further than `review` without their answer.
4. Two review passes at most. A third round of fact fixes left the sentences worse than the first, and the person read them as rambling.
5. This session rules on the slide count and the pictures and sends limits, never sentences. Workers made more slides than the story held in most posts of a batch, and an example sentence sent with a fix broke the line limit and was copied.
6. Nothing is posted.

## Terminology

| Term | Meaning |
|---|---|
| Wave | The workers started in one message. |
| Batch record | `batch.md` in the batch folder, a row per post, kept current, so that a cut-off run goes on from it. |
| Delicate topic | A story whose facts hang on who said what: a criminal case, health, money, a private individual. |
