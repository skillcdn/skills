# Creating and scheduling a post on Instagram's web interface

The create dialog of a signed-in account, step by step: the files and their order, the crop, the edit step and a video's cover, the caption, the alternative text, the schedule switch with its date and time, and the confirmation. Whose session this is and the pace it is worked at are in [signed-in.md](signed-in.md); what happens to a booking afterwards is in [scheduled-posts.md](scheduled-posts.md). Controls are named by what they do and where they sit, because their labels follow the account's language. The site has no changelog: a fact carries the day it was checked.

## The dialog

The site's own web interface books a post; no other product of the platform is signed in to (checked 2026-11-05). The navigation's create control opens a dialog that runs through four steps: the files, the crop, the edit, the caption. The button at the right of the dialog's header moves to the next step, and on the last step shares the post at once or, with the schedule switch on, schedules it.

- The dialog widens between steps and its controls move with it. A click at a position read before the move hit the close mark, which asks whether to discard the draft (its cancel keeps the draft), or landed late on a filter tile of the edit step and laid that filter over the first slide (checked 2026-11-13). Read a control's position twice and click when both readings agree; confirm by the step's title that the step changed, since after the crop step a second press was sometimes needed. A filter set by accident is undone by going back a step and picking the original.
- The Escape key asks to discard the whole draft (checked 2026-11-05). A list of suggested accounts under the caption is closed by a click on the dialog's title, never with Escape.
- The caption step holds more than the caption: sections for accessibility, for scheduling and others, any of which may be folded. Read the step's text once it has rendered, find a section by what it names, and open a folded one with a real click on its heading.

## The files and their order

The first step holds a file input, an `input` of type `file` among its elements whether or not it is drawn. Give the file tool that element and every slide's path in order, images and mp4 together. The step's button that opens the system's file picker is not pressed: the agent cannot drive that window. The files become one carousel in that order, and the first may be a video (five images with one video, and video, video, image, were both booked, checked 2026-11-17). JPEG and mp4 are what was uploaded; the input's `accept` attribute lists the types the dialog takes, and the site stores an image as JPEG whatever went up. Posts of up to ten slides were booked this way; the platform's help page on carousels gives the limit of the day. With a video in the set the dialog may show, the first time, a notice that video posts are shared as reels: it is passed by its own button, and the post is still a carousel post ([scheduled-posts.md](scheduled-posts.md) "A post that went live").

## The crop step

The ratio is preset to a square. The ratio control at the bottom left of the preview offers the portrait ratio, 4:5; picked on the first slide it holds for every slide. Left square, a 4:5 slide loses its top and its bottom, and a video cover part of its headline (checked 2026-11-05 and 2026-11-17).

## The edit step and a video's cover

Nothing is set on this step: no filter, no adjustment. A video slide adds three items of its own: its cover, its trim and its sound. All three stay as they are.

- The cover defaults to the clip's first frame, which is also what the profile grid shows when the video is the first slide: a clip that opens a post starts on the frame the grid should show.
- A cover uploaded from the computer is cropped to the middle 9:16 even in a 4:5 carousel, saved 759 by 1350 pixels where 1080 by 1350 was given (checked 2026-11-17). The first frame is the only cover that fills the tile.
- The site takes the cover from what the preview is showing. A video the browser has not painted yet, in a tab that is not in front, was saved with a cover that was black from edge to edge while the video itself was intact (checked 2026-11-17). Before the next step, bring the tab to the front (the page's `document.visibilityState` reads `visible`), step to every video slide with the preview's arrow, and see its picture on a screenshot. A screenshot can time out while a video plays on one host; take it again.
- The preview's arrow moves when the dialog does. Find it on the screenshot each time, and confirm the step by the video items appearing or going.

A cover that came out wrong cannot be repaired on a booking: the booking is deleted and made again.

## The caption

The caption is pasted. Text sent as key presses came out wrong in a script whose characters are composed, two syllables fused into one (checked 2026-11-09), so a caption in such a script is never typed; where no clipboard can be filled, a caption in an alphabet typed key by key may be typed, and is then compared with the file character by character (untried, 2026-11). Put the caption file on the clipboard the browser pastes from ([signed-in.md](signed-in.md) "What the browser must do"), click the caption field, paste, then read the field's text back and compare it with the file, its length and its words.

- A paste into a dialog that is still drawing lands empty: set the date and the time first, paste after.
- A handle written directly after an opening bracket, `(@handle)`, is swallowed by the account suggestions and leaves `(@)`. Write a handle after a space (checked 2026-11-09).
- A caption whose last line is nothing but a handle takes no typing and no paste at its end. Selecting the field's whole text and pasting the whole caption over it works (checked 2026-11-09).
- The field counts to 2,200 characters and the platform takes at most 30 hashtags in a caption (the field's own counter, and the help page on hashtags). The first line is what a feed shows before the caption is opened.

## The alternative text

The caption step's accessibility section takes a text for each slide. The post's title goes there for the first slide, pasted as the caption is and read back, since typed text breaks the same way. The tile on the profile grid then carries it as its image's alternative text, which tells a live post from a tile that looks like it ([scheduled-posts.md](scheduled-posts.md) "A post that went live"). A first slide that is a video takes a text only where the section shows a field for it.

## The schedule switch, the date and the time

The caption step has a switch that schedules the post instead of sharing it (checked 2026-11-05). Turned on, it shows a date field that opens a calendar and a time in three fields, the hour, the minute and the half of the day; the header's button changes from sharing to scheduling, and that change is the proof the switch is on. A caption step with no such switch means the account cannot book from this dialog (the platform's help page on scheduling posts says which accounts can).

- All three time fields are set. The hour and the minute alone gave half past midnight where half past noon was meant, which the dialog refused as less than twenty minutes ahead (checked 2026-11-16).
- A slot is at least twenty minutes after the moment the button is pressed; the dialog's own message gives the bound.
- The calendar's rows shift from month to month. Find the day's number on a screenshot of the open calendar each time.
- The zone of the fields is the one the dialog names beside them; where it names none, it is taken to be the zone of the browser, as a web page reads its clock there, which is the zone of the machine the browser runs on and not always the person's or the account's. That this dialog does so was not checked from a browser in another zone (untried, 2026-11). Before a sitting's first booking, read the browser's zone once, with a script that only reads (`Intl.DateTimeFormat().resolvedOptions().timeZone`), and compare it with the zone the times were agreed in: where they differ, the fields take the slot converted into the browser's zone, its day too.
- The scheduled list shows a booking in the same zone as the dialog, so reading a booking back there does not catch a wrong zone. The post's own page does, once it is live: its moment is absolute ([scheduled-posts.md](scheduled-posts.md) "A post that went live").

The step's other switches are not changed, and they are read before the header's button is pressed. One that is on and would send the post beyond the account's own grid, to another service or to a linked account, is a second thing leaving with the booking: the skill that books says what is done about it. Which switches an account shows was not recorded (2026-11); read them from the step's text.

## Booking and its confirmation

Press the header's button once the switch is on, the date and the time read right and the caption compared equal. A progress state follows, thirty to fifty seconds with a video in the set, then a line that the post was scheduled (checked 2026-11-17): wait for that line. A message that the post could not be scheduled came now and then; see on the scheduled list that the post is not there, and start again from the files, which then booked (checked 2026-11-13).
