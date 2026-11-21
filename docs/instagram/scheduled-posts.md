# The scheduled list, a changed booking, and a post that went live

Where a signed-in account's booked posts are listed, how a booking is read back, how its time, its caption or its slides are changed, how it is deleted, and how a post is found and read once the platform has posted it. The create dialog is in [creating-posts.md](creating-posts.md); the session and its pace in [signed-in.md](signed-in.md). Controls are named by what they do and where they sit, because their labels follow the account's language. A fact carries the day it was checked.

## The scheduled list

`https://www.instagram.com/scheduled_content/` shows the account's booked posts on a week's calendar, each with its time and its cover (checked 2026-11-05). A click on a booking opens it: the slides one at a time with a next arrow, the caption, the date and the time, and three controls at the bottom, which delete the booking, **share it at once**, and save a change. The sharing control posts the moment it is pressed and sits beside the saving one: it is never pressed. A video slide shows there re-encoded small, 720 by 900 pixels, which is the preview's size and not the post's (checked 2026-11-17).

## Reading a booking back

After a booking is made, on the list and in the opened booking, by eye on a screenshot:

- the time is the slot;
- the cover is the first slide whole, its headline complete from side to side, not black, and with no tint the file does not have (a filter set by accident shows here);
- stepping through gives the post's number of slides, in order;
- the caption begins with the file's first line.

Nothing is downloaded to be measured ([signed-in.md](signed-in.md) "Pace, and what reads as automation").

## Changing a booking's time

Open the booking, change the date and the time and nothing else, and press the saving control. The caption's counter in that view may read zero of 2,200 while the caption is kept (checked 2026-11). The list then shows the booking at its new time.

## Changing a caption

On a booking: the opened booking's caption field, then the saving control. On a live post: the post's own menu, its edit entry, the caption, then the control that finishes the edit, pressed with a real click, since a click from a script once left the edit unsaved (checked 2026-11-09). The pasting rules of [creating-posts.md](creating-posts.md) "The caption" hold in both.

## Replacing a booking's slides

A booking's slides cannot be changed, added to or reordered. The new version is booked at the same time, read back, and only then is the old booking deleted, so that the slot is never empty. Two bookings at one time sit side by side in no fixed order, the newer above one time and below the next (checked 2026-11-17): open both and tell them apart by a slide that differs, stepping as far as that slide where the covers are the same.

## Deleting a booking

The deleting control of the opened booking asks once more and cannot be undone (checked 2026-11-16). A deleted booking is made again from the create dialog.

## A post that went live

The platform posts a booking at its time, and the booking leaves the list. On the account's profile the new post heads the grid, after any pinned ones.

- The tile shows the first slide, and for a video its first frame. A carousel with video slides carries the carousel mark, its address is `/p/<id>/` and not `/reel/<id>/`, and the profile gained no reels tab from it (checked 2026-11-17).
- The tile's image carries the alternative text given to the first slide, which names the post where two tiles look alike.
- Open the post's page as a visitor would and read two things: the moment it was posted, from the page's `time` element (its `datetime`), and the first line of the caption. The moment equals the booked time to within a minute (checked 2026-11-17). What else a post page carries is in [posts.md](posts.md).
- A posted video slide is 1080 by 1350 pixels, plays muted when its slide is in view and loops (checked 2026-11-17).

A booking whose time passed while the account was restricted was not posted (2026-11); whether it still stands is read on the scheduled list, and the person decides what becomes of it.

## Changing a live post

A live post's caption can be edited. Its slides cannot be changed or reordered: the post is deleted, which is the person's decision, and posted again, and its address changes.
