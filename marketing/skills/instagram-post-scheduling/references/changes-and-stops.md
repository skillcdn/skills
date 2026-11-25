# Changed bookings, and what only some runs meet

What the skill does when a booking is changed, and three cases that hold only where their condition does: a browser in another zone than the schedule's, which adds a line; and an account's first booking by this skill and a switch that would send a post beyond the account's own grid, which stop the run, a go-ahead or not. Read the section whose case the run is in before acting on it; a run that meets none of them needs none of this page.

## A changed booking

Each change is shown before it is made, as the schedule is, follows the section of [scheduled-posts.md](/docs/instagram/scheduled-posts.md) that names it, is read back as a new booking is, and rewrites the same fields of the record with a line in `notes`.

- **"Move it to tomorrow"** changes the booking's time on the scheduled list. The new time is given in the browser's zone, as below.
- **"Use the video version"**, or a corrected slide, means new slides, made by [html-card-news-from-brief](/design/skills/html-card-news-from-brief/SKILL.md), which a booking cannot take: the remade post is approved again and replaces the booking as scheduled-posts.md "Replacing a booking's slides" says.
- **"Fix the caption"**: show the new caption whole, name the line that changes, and wait for the person's word, on a go-ahead too; a caption on a live post is public the moment it is saved. Then edit the caption of the booking, or of the live post, and read it back against the text that was shown.
- **"Take it out"** deletes the booking, and the post returns to `approved`, or to `archived` on the person's word.
- **A story that takes a booked slot on the day**, where the policy's Cadence allows one: the slot is the day's last that is still more than an hour ahead, the displaced booking moves to the first free slot of the days after by its time alone, and the new post is then booked in the slot.

## The browser in another zone

The dialog's fields and the scheduled list are taken to be in the browser's zone ([creating-posts.md](/docs/instagram/creating-posts.md) "The schedule switch, the date and the time"), which is untried from a browser in another zone than the schedule's. Where the two differ:

- The schedule carries a line with the browser's zone and the first slot as the dialog will be given it: "The browser is in <zone>: <day> <time> there."
- Every slot is converted before it is typed, its day too, and read back on the list as the converted time. The record's `scheduled_for` stays the slot in the schedule's zone with its offset, which names the same moment.
- Reading back does not prove the zone. The delivery says that the bookings were made from a browser in another zone and asks the person to look at one on their own device; the first post found live, whose page gives an absolute moment, is the proof, and the delivery of that tidy-up says which way it came out.

## An account's first booking

Where no record in the folder says `scheduled` or `published`, or the folder is a plain one and the person has not said the account was booked this way before, the schedule carries this, in the person's language, and waits for their word, on a go-ahead too:

"Before the first one: this books by driving Instagram's own web page as you would by hand, which is not a route the platform offers to software. One account worked this way was suspended for part of a day and then restored, with no reason given. The run keeps the pace adopted since: one post at a time, a few minutes apart, one day's posts a sitting. OK books them knowing that."

It is said once for an account: after the first booking the records say so, and in a plain folder the person's answer stands for the run.

## A switch that shares beyond the grid

The caption step's other switches are read before the header's button and never changed in passing (creating-posts.md "The schedule switch, the date and the time"). One that is on and would send the post to another service or a linked account, where neither the policy nor the person has named that sharing:

1. Stop before the button, with the draft kept: "<switch> is on, so this post would also go to <service>. I would turn it off and book it on the account alone: OK turns it off, 'keep' leaves it on."
2. On OK turn it off for this post with a real click and read that the switch changed; on "keep" leave it on.
3. The answer stands for the sitting; where the person says it stands for the account, an account folder's policy takes it into its Account line. The delivery names what each booking was shared to.

A wait long enough for a slot to come within twenty minutes moves that slot as the schedule's rules say, and the moved time is shown.
