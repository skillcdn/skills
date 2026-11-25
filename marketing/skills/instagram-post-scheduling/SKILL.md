---
name: instagram-post-scheduling
description: "Schedules approved Instagram posts (card news carousels of images and video slides with their captions) on the account's web interface, in a browser signed in to it, reads each booking back on the scheduled list, and once a slot has passed finds the post live, records its address and files its folder. Use when a user says \"book the five I approved from noon tomorrow, thirty minutes apart\", \"schedule these on our Instagram\", \"swap that booking for the video version\", \"did they all go up?\", \"승인한 것들 예약 걸어 줘\". The posts come from html-card-news-from-brief or html-card-news-batch; an account folder's post records and ledger are read and written, and a plain folder of slides with a caption is booked the same way. To read another account's posts, instagram-card-news-format-study. A person signs in, or an agent account that holds the sign-in; it drives the dialog with real clicks, one post at a time, and books only what the person approved, after showing the schedule. Nothing is spent."
license: MIT
compatibility: Needs a browser the agent drives that is signed in to the account (an extension in the person's browser, a pane they opened, or an agent account's own), or an agent account's own browser and the account's sign-in in its secret store, with a tool that hands files to a page's file input, and a shell on the same machine for the clipboard and the records. Signing in from a headless browser is untried on this site.
metadata:
  author: skillcdn
  version: "1.4"
  tools: instagram
skillcdn:
  include:
    - /docs/instagram/signed-in.md
  translations:
    ko:
      title: 인스타그램 게시물 예약과 게시 확인
      description: "승인된 인스타그램 게시물(사진과 영상 장으로 된 카드뉴스 캐러셀과 캡션)을 계정에 로그인된 브라우저에서 인스타그램 웹 화면으로 예약합니다. 예약마다 예약 목록에서 시각, 표지, 장 수, 캡션을 다시 확인하고, 시각이 지나면 실제로 올라간 게시물을 찾아 주소를 기록하고 폴더를 올라간 날짜별로 정리합니다. '승인한 5개 내일 12시부터 30분 간격으로 예약 걸어 줘', '우리 인스타에 예약해 줘', '이 예약 영상 버전으로 바꿔 줘', '내일로 옮겨 줘', '다 올라갔어?'라고 할 때 쓰세요. 게시물은 html-card-news-from-brief가 만들고, 여러 건은 html-card-news-batch가 한 번에 만듭니다. 계정 폴더라면 게시물마다의 post.json과 다룬 소재 장부를 읽고 고치며, 슬라이드와 캡션만 있는 폴더도 같은 방법으로 예약합니다. 다른 계정의 게시물을 읽는 일은 instagram-card-news-format-study가 합니다. 로그인된 세션이 있으면 그 세션으로 일하고, 없으면 로그인 수단을 가진 에이전트 계정은 스스로 로그인하며, 둘 다 아니면 사람에게 청합니다. 진행은 실제 클릭과 붙여넣기로 한 건씩 합니다. 사용자가 승인한 게시물만, 예약표를 보여 드린 뒤에 겁니다. 비용은 들지 않습니다."
---
# Instagram posts, booked and confirmed in the account's web interface

Approved posts go in: carousels of images and video slides, each with its caption. They come out booked on the account for the times the person or the account's cadence gives, every booking read back on the site's scheduled list; and once a time has passed, each post is found live, its address recorded and, in an account folder, its folder filed under the day it went up. The work is done in the site's own web interface, in a browser signed in to the account, by a person or by an agent account that holds its sign-in, because a carousel with video slides is booked there with no app, token or public file address to set up first. The agent drives the dialog a person would use, at a person's pace, and the platform posts at the booked time: nothing here presses a control that posts at once.

## How the user is involved

- **Questions:** one message, only what neither the request nor the account's policy says: which posts ("Which posts should I book: every approved one?") and when ("From which day and time, and how far apart?"). The sign-in is asked for only when the browser is not signed in to the account and no agent account's own sign-in is at hand ([signed-in.md](/docs/instagram/signed-in.md) "Whose session"): "Please sign in to <handle> in this browser and tell me when you are in."; an agent account, whose `headless` browser nobody sees, asks it as driven-browser.md "A person's sign-in" says.
- **Checkpoints:** the schedule, before the first booking (phase 4); "OK" books. A swap and a moved time are shown the same way before they are made, a changed caption with its new text whole, and a booking the person did not name is not deleted without their word. Then the delivery.
- **Go-ahead:** told to go ahead alone, or where the policy's Approval line says approved posts are booked without a further question, the schedule is shown and the booking goes on without a stop. Never skipped: the person's approval of each post, the account confirmed where no policy names it, the word on a changed caption, the notice before an account's first booking, the word on a switch that would share a post beyond the account's grid, a person's sign-in where no agent account holds one, and the stop at a screen that is a person's to answer.
- **Changes mid-run:** a moved time, new slides ("use the video version"), a fixed caption, a booking taken out, a story that takes a booked slot on the day: read [changes-and-stops.md](references/changes-and-stops.md) "A changed booking" before making one. Each is shown first, and no caption on the account changes unseen.

## Requirements

Capabilities, not product names. Before the first message, look at what the agent has:

| What | Used for | When missing |
|---|---|---|
| A browser the agent drives that is signed in to the account: an extension in the person's own browser, a browser pane they opened, or an agent account's own browser, which the account also signs in itself where its secret store holds the sign-in. Recognize it by a browser tool with real clicks, key presses, screenshots, the page's text and a tool that hands files to a page's file input | Everything on the site | Stop and say what to add. A headless browser a script of the run launches keeps no session and is not used |
| A shell on the machine that browser runs on | The clipboard a caption is pasted from (`Set-Clipboard`, `pbcopy`, `wl-copy`; a headless browser pastes from its own, filled as signed-in.md says), the records, the folder moved | With no clipboard to fill, a caption in an alphabet typed key by key is typed by the browser tool and compared with the file character by character, a difference stopping that booking; a caption in a script whose characters are composed is not typed (creating-posts.md "The caption"): stop and say what to add |

How hosts differ in the browser they drive is in [driven-browser.md](/docs/browser/driven-browser.md). Links that start with `/` are files of the pack this skill is from: a copy of this directory, a plugin or a mount below the root that lacks one reads it through the pack's connection (`https://skillcdn.ai/gh/skillcdn/skills`) or at `github.com/skillcdn/skills`.

The area's rule that a result fits its channel takes this form: the number of slides a post takes, the caption's length and the ratio are what the dialog and the platform's help pages say on the day; the numbers in the pages are dated readings.

## Inputs

| Input | Source |
|---|---|
| The posts | In an account folder ([account.md](/docs/card-news/account.md)): every post whose `post.json` says `approved`, or the ones the request names. Otherwise the folder the user names, with the slides as numbered files and the caption as a text file or in the request. Asked when neither is at hand. |
| When | The request; else the policy's Cadence (posts a day, the slots, how far the minutes vary); else asked. |
| The account | The policy's Account line; else the one the browser is signed in to, confirmed by the person (phase 2). |
| Everything else | Derived and shown in the schedule: the order of the posts across the slots, the zone (the request's, else the policy's, else that of the machine the browser runs on), the alternative text of the first slide (the post's title). |

## Workflow

### Phase 1: The work list

Read [creating-posts.md](/docs/instagram/creating-posts.md) before this phase, since the gate and the schedule hold a post to the dialog's limits, and in an account folder account.md. Produces the **work list**: the bookings to confirm and the posts to book. In an account folder, a post whose `post.json` says `scheduled` with a `scheduled_for` in the past is a booking to confirm, and comes before anything new. A post to book passes the gate when:

- its record holds `approved` with `at` and `by` (in a plain folder, the person named it in this conversation);
- no file of the upload set, `slide-plan.json` or `caption.txt` changed after `approved.at`. In a repository none differs from the commit that first wrote that moment into the record (`git log --reverse --format=%H -S"<approved.at>" -- <post.json>`, its first line; then `git diff --stat <commit> -- <the files>` prints nothing), since a fresh clone resets every file's time and a file approved before it was committed is not changed; by the files' times where git does not track them, the approval is not committed yet, or there is no repository;
- its **upload set** is complete: one file per slide in the slides' order, an image or an mp4 for a video slide, at full size (the build's renders in `out/`, or the copies for upload where the repository's agreement or the post's record names a folder of them; never the phone-size copies), as many as `post.json`'s `slides`;
- its caption is not empty and within the limits of creating-posts.md "The caption".

A post that fails is not booked and is named in the schedule with what it lacks. Where the repository's agreement names a command for a step (a check before booking, the filing of phase 3), run that command instead of doing the step by hand.

### Phase 2: The session

Produces the **session**: the browser on the site, signed in to the account. Open the site's home page and read which account is signed in ([signed-in.md](/docs/instagram/signed-in.md) "Whose session"). Nobody signed in: where the policy or the request names the account and an agent account holds its sign-in, it signs in itself, as signed-in.md "Signing in" says, and reads again which account is in; where neither names it, ask which account before any sign-in; without a sign-in of its own the agent asks the person to sign in, and waits. Another account than the policy names: ask the person, and wait. No policy names one: "This browser is signed in to <handle>. Is that the account these posts go to, now and from here on?", go-ahead or not; in an account folder a yes becomes the policy's Account line, shown as that line. A screen that is a person's to answer stops the run (Verdicts).

### Phase 3: What went live

Read [scheduled-posts.md](/docs/instagram/scheduled-posts.md) before this phase. Produces the **published records**, one per booking whose time has passed, by its "A post that went live": find the post's tile at the head of the profile grid, open its page, and read the moment it was posted and the first line of its caption. When both match the record:

1. Write `published` with `at` (the page's moment) and `url`, and `status: "published"`.
2. Move the folder to `posts/published/<upload day>/<slug>/`, the day in the account's zone, with the repository's own move where it is one. Rewrite the paths inside the folder that point out of it: the slide plan names its format spec relative to itself.
3. In the ledger, change only the state cell of the row that begins with the slug, to `published <day>`; in a repository, read the diff.

A plain folder has no record: the address goes in the delivery.

### Phase 4: The schedule

Produces the **schedule** and the checkpoint. Days and times are the schedule's zone's, a day the request names among them. First read the browser's zone (creating-posts.md "The schedule switch, the date and the time") and what the scheduled list already holds on the days to be booked, turned into the schedule's zone. Then give each post that passed the gate a slot, with no gap left for one that did not: an account's posts in the order of their folders' days, then of the ledger's rows, unless the request gives another:

- A slot is at least twenty minutes after the moment its booking will be pressed, counting the bookings and the pauses before it. "From today" means today's first slot that still meets this.
- A time a booking already holds is not given; a booking no record of the folder accounts for is named in the schedule and left alone.
- Where the policy says the minutes vary, each slot taken from its Cadence moves by a random amount within that range; a time the request gives is kept as given.
- Two stories that work the same way are not placed back to back or on one day where the list allows.
- One sitting books one day's posts. Later days are listed as left for the next sitting, and booked now only on the person's word.

The message, one line per post, then what is not booked and what is left:

```
Schedule for <handle>, times in <zone>. OK books them.
1. <day> <time>  <title>  cover: <what it shows>  <n> slides (<m> video)  "<the caption's first line>"
Already on the list: <day> <time>, <what its cover shows>.
Not booked: <post>, <what it lacks>.
Left for the next sitting: <n> posts for <day>.
```

Where the browser's zone is another than the schedule's, or the account has no booking by this skill yet (no record says `scheduled` or `published`, or a plain folder), read [changes-and-stops.md](references/changes-and-stops.md) before sending it: the first adds a line, the second a stop that a go-ahead does not skip.

### Phase 5: Book

Produces the **bookings**, one post at a time in slot order, by [creating-posts.md](/docs/instagram/creating-posts.md): the files in order, the portrait ratio at the crop step, nothing set at the edit step and every video slide seen painted, the date and all three time fields in the browser's zone, the caption pasted and compared with the file, the post's title pasted as the first slide's alternative text, the step's other switches read, the header's button once it says it schedules, then the wait for the line that the post was scheduled. A switch that is on and would send the post beyond the account's own grid, named by neither the policy nor the person, stops that booking before the button (changes-and-stops.md "A switch that shares beyond the grid").

Read the booking back on the scheduled list ([scheduled-posts.md](/docs/instagram/scheduled-posts.md) "Reading a booking back"): the time, the cover, the number of slides, the caption's first line. Then write the record, before the next post is begun: `status: "scheduled"` and `scheduled_for` as the slot in the schedule's zone with its offset (`2026-11-27T12:00:00+09:00`), a line in `notes` for a swap or a moved time, and the ledger row's state cell as `scheduled <the slot's day>`. The next booking begins two to five minutes after the last one was read back.

A changed booking (Changes mid-run) is read back the same way and rewrites the same fields.

### Phase 6: Deliver

One message: each booking with its time as the scheduled list shows it; each post found live with its address; what was not booked or not found and why; what is left for the next sitting; what the person has to do themselves (a file set picked by hand, a screen to deal with); what the site showed at a sign-in signed-in.md calls untried; and what changes-and-stops.md says a run reports. In a repository the records are committed as its agreement says.

## Verdicts

| Result | Verdict |
|---|---|
| A post with no approval recorded, an incomplete upload set, or a caption that is empty or over the limit | Not booked; named in the schedule with what it lacks |
| A post changed after its approval (a slide remade, the caption rewritten) | Named in the schedule with what changed, and once that is answered its record and its ledger row go back to `review`; booked after whoever approved it approves it again |
| The upload set is over what the file tool takes in one call | The person picks the files in the dialog; the run goes on from the crop step |
| A video slide shows black at the edit step | Wait with the tab in front until it is painted; never go on with it black |
| The booking read back shows another time, a black, cropped or tinted cover, a wrong number of slides or another caption | Delete that booking and make it again; a second failure stops the run with what was seen |
| The site says the post could not be scheduled | See that the list does not hold it and start that post again; a second failure stops the run |
| Nobody signed in as the sitting begins, and an agent account holds the sign-in | Sign in as signed-in.md "Signing in" says, once; a sign-in the site refuses stops the run |
| A login form later in the sitting, a check not answered by a code the account holds or a person gives, a notice about automated behavior, a restricted or suspended account | Stop at once, press nothing, say what the screen says; a person deals with it |
| A slot has passed and the post is not on the grid | The record stays `scheduled`; say so with what the scheduled list shows; the person decides, and the sharing control is not the remedy |
| A post is live but its moment is more than a minute off the slot, or its caption begins otherwise | No record written; say what differs. Off by whole or half hours points to the zone: say so, with the bookings still waiting; the person decides |
| Booked, read back and recorded; or live, read and filed | Delivered |

## Hard rules

1. **Only a post the person approved is booked, and the schedule is shown first.** The approval recorded on a post is that post's confirmation; the schedule, a swap and a moved time are each shown before they are made, without a stop only where the policy's Approval line or the person's go-ahead says so; a changed caption and an account no policy names wait for the person's word every time. What leaves the account is the person's.
2. **A signed-in session, else an agent account's own sign-in, else a person's.** A session already signed in to the account is worked in. An agent account whose secret store holds the sign-in signs in itself, in its own `headless` or `window` browser and only with [signing-in.md](/docs/browser/signing-in.md) read; the password and every code go from where it keeps them to the field, never into the conversation, a message, a record, a file the run keeps or the delivery, but for a code a person gives it. A password written in the conversation is not used. Any other agent, one that cannot read that page and one at a screen that is a person's to answer presses nothing there and asks a person. The account is its owner's to answer for.
3. **The control that shares at once is never pressed**, in the create dialog or on an opened booking: a booking posts by the platform's clock.
4. **Real clicks and pastes, one post at a time, a pause between two, one day's posts a sitting, one session on the browser.** Nothing is requested from inside the page and no script presses a control. This is what keeps the account from being read as automated ([signed-in.md](/docs/instagram/signed-in.md)).
5. **The record follows the site.** `scheduled` is written after the booking was read back on the scheduled list, `published` after the post's own page was read; never from the dialog's last message alone.
6. **A booking is deleted only when the run made it wrong, when its replacement has been read back, or when the person names it.** A deletion cannot be undone. A live post is deleted by the person.
7. **Only the home page for its navigation, the sign-in, the create dialog, the scheduled list, the account's profile and its own posts are opened.** A browser a person signed in is theirs.
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
