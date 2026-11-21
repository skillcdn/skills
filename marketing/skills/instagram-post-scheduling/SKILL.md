---
name: instagram-post-scheduling
description: "Schedules approved Instagram posts (card news carousels of images and video slides with their captions) on the account's web interface, in the browser the person is signed in to, reads each booking back on the scheduled list, and once a slot has passed finds the post live, records its address and files its folder. Use when a user says \"book the five I approved from noon tomorrow, thirty minutes apart\", \"schedule these on our Instagram\", \"swap that booking for the video version\", \"did they all go up?\", \"승인한 것들 예약 걸어 줘\". The posts come from html-card-news-from-brief or html-card-news-batch; an account folder's post records and ledger are read and written, and a plain folder of slides with a caption is booked the same way. To read another account's posts, instagram-card-news-format-study. The person signs in; the agent drives the dialog with real clicks, one post at a time, and books only what the person approved, after showing the schedule. Nothing is spent."
license: MIT
compatibility: Needs a browser the agent drives in which the person is signed in to the account (an extension in their own browser, or a browser pane they opened), with a tool that hands files to a page's file input, and a shell on the same machine for the clipboard and the records. A headless browser the agent launches has no session and cannot do this.
metadata:
  author: skillcdn
  version: "1.1"
  tools: instagram
skillcdn:
  include:
    - /docs/instagram/signed-in.md
  translations:
    ko:
      title: 인스타그램 게시물 예약과 게시 확인
      description: "승인된 인스타그램 게시물(사진과 영상 장으로 된 카드뉴스 캐러셀과 캡션)을 사용자가 로그인해 둔 브라우저에서 인스타그램 웹 화면으로 예약합니다. 예약마다 예약 목록에서 시각, 표지, 장 수, 캡션을 다시 확인하고, 시각이 지나면 실제로 올라간 게시물을 찾아 주소를 기록하고 폴더를 올라간 날짜별로 정리합니다. '승인한 5개 내일 12시부터 30분 간격으로 예약 걸어 줘', '우리 인스타에 예약해 줘', '이 예약 영상 버전으로 바꿔 줘', '내일로 옮겨 줘', '다 올라갔어?'라고 할 때 쓰세요. 게시물은 html-card-news-from-brief가 만들고, 여러 건은 html-card-news-batch가 한 번에 만듭니다. 계정 폴더라면 게시물마다의 post.json과 다룬 소재 장부를 읽고 고치며, 슬라이드와 캡션만 있는 폴더도 같은 방법으로 예약합니다. 다른 계정의 게시물을 읽는 일은 instagram-card-news-format-study가 합니다. 로그인은 사용자가 직접 하고, 에이전트는 실제 클릭과 붙여넣기로 한 건씩 진행합니다. 사용자가 승인한 게시물만, 예약표를 보여 드린 뒤에 겁니다. 비용은 들지 않습니다."
---
# Instagram posts, booked and confirmed in the person's own browser

Approved posts go in: carousels of images and video slides, each with its caption. They come out booked on the account for the times the person or the account's cadence gives, every booking read back on the site's scheduled list; and once a time has passed, each post is found live, its address recorded and, in an account folder, its folder filed under the day it went up. The work is done in the site's own web interface, in a browser the person signed in themselves, because a carousel with video slides is booked there with no app, token or public file address to set up first. The agent drives the dialog a person would use, at a person's pace, and the platform posts at the booked time: nothing here presses a control that posts at once.

## How the user is involved

- **Questions:** one message, only what neither the request nor the account's policy says: which posts ("Which posts should I book: every approved one?") and when ("From which day and time, and how far apart?"). The sign-in is asked for only when the browser is not signed in to the account: "Please sign in to <handle> in this browser and tell me when you are in."
- **Checkpoints:** the schedule, before the first booking (phase 4); "OK" books. A swap and a moved time are shown the same way before they are made, and a booking the person did not name is not deleted without their word. Then the delivery.
- **Go-ahead:** told to go ahead alone, or where the policy's Approval line says approved posts are booked without a further question, the schedule is shown and the booking goes on without a stop. Never skipped: the person's approval of each post, their own sign-in, and the stop at a security screen.
- **Changes mid-run:** "move it to tomorrow" changes the booking's time on the scheduled list. "Use the video version" or a corrected slide means new slides, which a booking cannot take: the remade post is approved again and replaces the booking as scheduled-posts.md "Replacing a booking's slides" says. "Fix the caption" edits the caption of the booking, or of the live post. "Take it out" deletes the booking, and the post returns to `approved`, or to `archived` on the person's word. A story that takes a booked slot on the day, where the policy's Cadence allows one: the slot is the day's last that is still more than an hour ahead, the displaced booking moves to the first free slot of the days after by its time alone, and the new post is then booked in the slot.

## Requirements

Capabilities, not product names. Before the first message, look at what the agent has:

| What | Used for | When missing |
|---|---|---|
| A browser the agent drives in which the person is signed in to the account: an extension in their own browser, or a browser pane they opened. Recognize it by a browser tool that lists the person's own tabs, with real clicks, key presses, screenshots, the page's text and a tool that hands files to a page's file input | Everything on the site | Stop and say what to add. A headless browser the agent launches has no session, and the agent signs in nowhere |
| A shell on the machine that browser runs on | The clipboard a caption is pasted from (`Set-Clipboard`, `pbcopy`, `wl-copy`), the records, the folder moved | With no clipboard command the caption is typed by the browser tool and compared with the file character by character; a difference stops that booking |

[signed-in.md](/docs/instagram/signed-in.md) is included and arrives with this skill: whose session it is, the screens that stop the work, the pace. Two more pages of the set [`docs/instagram/`](/docs/instagram/README.md) are read through the repository connection: [creating-posts.md](/docs/instagram/creating-posts.md) before phase 1, since the gate and the schedule hold a post to the dialog's limits, and [scheduled-posts.md](/docs/instagram/scheduled-posts.md) before phase 3. Where the folder is an account's, [account.md](/docs/card-news/account.md) is read before phase 1; the browser's capabilities are in [driven-browser.md](/docs/browser/driven-browser.md). A mount of this skill alone or of its area, the area's plugin and a copy of this directory lack the linked pages, and a copy lacks the included one too: fetch them from `docs/instagram/`, `docs/card-news/` and `docs/browser/` of the repository this skill comes from (`github.com/skillcdn/skills`, served at `skillcdn.ai/gh/skillcdn/skills`) before the first booking, since the dialog's steps are only there.

The area's rule that a result fits its channel takes this form: the number of slides a post takes, the caption's length and the ratio are what the dialog and the platform's help pages say on the day; the numbers in the pages are dated readings.

## Inputs

| Input | Source |
|---|---|
| The posts | In an account folder ([account.md](/docs/card-news/account.md)): every post whose `post.json` says `approved`, or the ones the request names. Otherwise the folder the user names, with the slides as numbered files and the caption as a text file or in the request. Asked when neither is at hand. |
| When | The request; else the policy's Cadence (posts a day, the slots, how far the minutes vary); else asked. |
| The account | The policy's Account line, else the account the browser is signed in to, named in the schedule. |
| Everything else | Derived and shown in the schedule: the order of the posts across the slots, the zone (the policy's, else the machine's), the alternative text of the first slide (the post's title). |

## Workflow

### Phase 1: The work list

Produces the **work list**: the bookings to confirm and the posts to book. In an account folder, a post whose `post.json` says `scheduled` with a `scheduled_for` in the past is a booking to confirm, and comes before anything new. A post to book passes the gate when:

- its record holds `approved` with `at` and `by` (in a plain folder, the person named it in this conversation);
- no file of the upload set, `slide-plan.json` or `caption.txt` is newer than `approved.at` (the files' times, or the repository's history);
- its **upload set** is complete: one file per slide in the slides' order, an image or an mp4 for a video slide, at full size (the build's publish copies where the post folder holds them, `out/publish/`, else its renders in `out/`, never the phone-size copies), as many as `post.json`'s `slides`;
- its caption is not empty and within the limits of creating-posts.md "The caption".

A post that fails is not booked and is named in the schedule with what it lacks. Where the repository's agreement names a command for a step (a check before booking, the filing of phase 3), run that command instead of doing the step by hand.

### Phase 2: The session

Produces the **session**: the person's browser on the site, signed in to the account. Open the site's home page and read which account is signed in ([signed-in.md](/docs/instagram/signed-in.md) "Whose session"). Nobody signed in, or another account than the policy names: ask the person to sign in, and wait. A security screen stops the run (Verdicts).

### Phase 3: What went live

Produces the **published records**, one per booking whose time has passed, by [scheduled-posts.md](/docs/instagram/scheduled-posts.md) "A post that went live": find the post's tile at the head of the profile grid, open its page, and read the moment it was posted and the first line of its caption. When both match the record:

1. Write `published` with `at` (the page's moment) and `url`, and `status: "published"`.
2. Move the folder to `posts/published/<upload day>/<slug>/`, the day in the account's zone, with the repository's own move where it is one. Rewrite the paths inside the folder that point out of it: the slide plan names its format spec relative to itself.
3. In the ledger, change only the state cell of the row that begins with the slug, to `published <day>`; in a repository, read the diff.

A plain folder has no record: the address goes in the delivery.

### Phase 4: The schedule

Produces the **schedule** and the checkpoint. Give each gated post a slot, an account's posts in the order of their folders' days unless the request gives another:

- A slot is at least twenty minutes after the moment its booking will be pressed, counting the bookings and the pauses before it. "From today" means today's first slot that still meets this.
- Where the policy says the minutes vary, each slot moves by a random amount within that range; otherwise slots are as given.
- Two stories that work the same way are not placed back to back or on one day where the list allows.
- One sitting books one day's posts. Later days are listed as left for the next sitting, and booked now only on the person's word.

The message, one line per post, then what is not booked and what is left:

```
Schedule for <handle>, times in <zone>. OK books them.
1. <day> <time>  <title>  cover: <what it shows>  <n> slides (<m> video)  "<the caption's first line>"
Not booked: <post>, <what it lacks>.
Left for the next sitting: <n> posts for <day>.
```

### Phase 5: Book

Produces the **bookings**, one post at a time in slot order, by [creating-posts.md](/docs/instagram/creating-posts.md): the files in order, the portrait ratio at the crop step, nothing set at the edit step and every video slide seen painted, the date and all three time fields, the caption pasted and compared with the file, the post's title pasted as the first slide's alternative text, the header's button once it says it schedules, then the wait for the line that the post was scheduled.

Read the booking back on the scheduled list ([scheduled-posts.md](/docs/instagram/scheduled-posts.md) "Reading a booking back"): the time, the cover, the number of slides, the caption's first line. Then write the record, before the next post is begun: `status: "scheduled"` and `scheduled_for` as the time with its zone offset, a line in `notes` for a swap or a moved time, and the ledger row's state cell as `scheduled <day>`. The next booking begins two to five minutes after the last one was read back.

A changed booking (Changes mid-run) follows the section of scheduled-posts.md that names it, is read back the same way, and rewrites the same fields.

### Phase 6: Deliver

One message: each booking with its time as the scheduled list shows it; each post found live with its address; what was not booked or not found and why; what is left for the next sitting; and what the person has to do themselves (a file set picked by hand, a screen to deal with). In a repository the records are committed as its agreement says.

## Verdicts

| Result | Verdict |
|---|---|
| A post with no approval recorded, an incomplete upload set, or a caption that is empty or over the limit | Not booked; named in the schedule with what it lacks |
| A post changed after its approval (a slide remade, the caption rewritten) | Back to `review`; booked after the person approves it again |
| The upload set is over what the file tool takes in one call | The person picks the files in the dialog; the run goes on from the crop step |
| A video slide shows black at the edit step | Wait with the tab in front until it is painted; never go on with it black |
| The booking read back shows another time, a black, cropped or tinted cover, a wrong number of slides or another caption | Delete that booking and make it again; a second failure stops the run with what was seen |
| The site says the post could not be scheduled | See that the list does not hold it and start that post again; a second failure stops the run |
| A login form, an identity check, a notice about automated behavior, a restricted or suspended account | Stop at once, press nothing, say what the screen says; the person deals with it |
| A slot has passed and the post is not on the grid | The record stays `scheduled`; say so with what the scheduled list shows; the person decides, and the sharing control is not the remedy |
| A post is live but its moment is more than a minute off the slot, or its caption begins otherwise | No record written; say what differs |
| Booked, read back and recorded; or live, read and filed | Delivered |

## Hard rules

1. **Only a post the person approved is booked, and the schedule is shown first.** The approval recorded on a post is that post's confirmation; the schedule, a swap and a moved time are each shown before they are made, without a stop only where the policy's Approval line or the person's go-ahead says so. What leaves the account is the person's.
2. **The person signs in.** The agent types no password, code or recovery answer, and at a security screen presses nothing. The account is theirs to answer for.
3. **The control that shares at once is never pressed**, in the create dialog or on an opened booking: a booking posts by the platform's clock.
4. **Real clicks and pastes, one post at a time, a pause between two, one day's posts a sitting, one session on the browser.** Nothing is requested from inside the page and no script presses a control. This is what keeps the account from being read as automated ([signed-in.md](/docs/instagram/signed-in.md)).
5. **The record follows the site.** `scheduled` is written after the booking was read back on the scheduled list, `published` after the post's own page was read; never from the dialog's last message alone.
6. **A booking is deleted only when the run made it wrong, when its replacement has been read back, or when the person names it.** A deletion cannot be undone. A live post is deleted by the person.
7. **Only the create dialog, the scheduled list, the account's profile and its own posts are opened.** The browser is the person's.
8. **Nothing is spent.**

## Terminology

| Term | Meaning |
|---|---|
| Account folder | A working folder with the account's policy, post records and ledger ([account.md](/docs/card-news/account.md)). |
| Upload set | The files of one post in slide order, an image or an mp4 each, at full size. |
| Slot | The day and time a post is booked for. |
| Booking | A post on the site's scheduled list, waiting for its slot. |
| Reading back | Checking a booking on the scheduled list: its time, cover, slides and caption. |
| Sitting | One session that opens the site to book; it books one day's posts. |
| Tidy-up | Phase 3: confirming what went live and filing it. |
