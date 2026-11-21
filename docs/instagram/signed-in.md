# Working in a signed-in Instagram session

What a skill that posts to an account needs from the browser, whose session it works in, which screens stop it, what it opens, and the pace that keeps the account from being read as automated. The reading pages of this set stay signed out; this page and the two it leads to ([creating-posts.md](creating-posts.md), [scheduled-posts.md](scheduled-posts.md)) are the signed-in side. A fact that can go stale carries the day it was checked.

## Whose session

The person signs in to the account themselves, in their own browser, and the agent drives that browser: an extension in the person's browser, or a browser pane they opened and signed in ([walls.md](/docs/browser/walls.md), the first of its ways). The agent never types a password, a code or a recovery answer, and a headless browser a script launches has no session and is given none. Which account is signed in is read from the profile link in the page's own navigation, whose address is `/<handle>/`; a home page that shows a login form means nobody is.

## What the browser must do

The capabilities of [driven-browser.md](/docs/browser/driven-browser.md), and three more:

| Capability | Recognize it by | Needed for |
|---|---|---|
| Hand files to a page's file input | A tool that takes file paths and an input or a file chooser | The slides of a post. One host's tool took at most 10 MB in one call (checked 2026-11-17); a set over the tool's limit is picked by the person in the dialog, and the run goes on from the crop step |
| Send key presses to the focused field | A tool that presses a key or a chord | Pasting a caption, selecting a field's whole text |
| Put text on the clipboard of the machine the browser runs on | A shell there with the system's clipboard command | The caption, which is pasted and never typed |

## Screens that stop the work

A login form in the middle of a session, a request to confirm who the person is, a notice about automated behavior, a notice that the account is restricted or suspended: nothing on such a screen is pressed. The run stops, says what the screen says, and the person deals with it in their own time.

## Pace, and what reads as automation

One account that was driven through this interface was suspended one morning and restored the same day, with no reason given; in the hour or so of the evening before, a driven browser had booked four posts and changed the times of fifteen, and a tidy-up had called the site's internal media address from inside the page several times (2026-11). The practice since:

- **Nothing is requested from inside the page.** No `fetch` to the site's own addresses (`/api/`, `graphql`), no header added, no image downloaded to be measured. What a post is and when it went up is read from what the screen and the post's own page show.
- **Real input only.** Every action is a real click at a control found on the screen, or a paste; no script presses a button or sets a field's value. A script that only reads (a control's position, a field's text) runs once or twice a screen, not in a loop.
- **Not in bulk.** One sitting books at most one day's posts, and changes at most as many bookings; between one post and the next there is a pause of two to five minutes. More than that is spread over sittings or days.
- **Few openings.** The site is opened for a sitting that books and for one tidy-up a day, after the day's last slot, and not between.

Whether an account posts on fixed slots or varies its minutes is its own policy; the account above kept its fixed slots.

## One session at a time

Two agent sessions that drove the same browser at the same hour both stalled, one of them inside a browser call for days (one host, checked 2026-11-16). A sitting is the only session using the browser, and a job that opens the site on a timer is set for an hour when nobody books.

## What is opened

The create dialog, the scheduled list, the account's own profile and its own posts. Messages, notifications, settings, other accounts and the feed are not opened, and nothing is liked, followed, commented on or answered.
