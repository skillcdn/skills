# Working in a signed-in Instagram session

What a skill that posts to an account needs from the browser, whose session it works in and who signs in, which screens stop it, what it opens, and the pace that keeps the account from being read as automated. The reading pages of this set stay signed out; this page and the two it leads to ([creating-posts.md](creating-posts.md), [scheduled-posts.md](scheduled-posts.md)) are the signed-in side. A fact that can go stale carries the day it was checked.

## Whose session

The work is done in a browser the agent drives that is signed in to the account, reached in this order:

1. **Signed in already.** An extension in the person's browser or a browser pane they opened and signed in ([walls.md](/docs/browser/walls.md), the first of its ways), or an agent account's own browser whose profile kept an earlier sign-in: the agent works in that session.
2. **The agent signs in.** Nobody is signed in, and the agent holds the account's sign-in, its password and whatever its second step asks: it signs in itself, as "Signing in" says.
3. **A person signs in.** The agent holds no sign-in of the account, or the site asks what it cannot answer ("Screens that stop the work"): it stops and asks a person, who signs in in their own browser, or in an agent account's as [driven-browser.md](/docs/browser/driven-browser.md) "A person's sign-in" says.

An agent account drives the browser its `runner.json` names ([driven-browser.md](/docs/browser/driven-browser.md) "An agent account's browser"): in `headless`, the default, or in `window` it signs in itself, and the sign-in stays in the profile for the sittings after; in `chrome` it works in a person's sign-in. A headless browser a script of the run launches keeps no session and is not used here. Which account is signed in is read from the profile link in the page's own navigation, whose address is `/<handle>/`; a home page that shows a login form means nobody is. Another account than the one the work is for is not signed out by the agent: the run stops and asks the person.

## Signing in

The agent signs in as [driven-browser.md](/docs/browser/driven-browser.md) "Its own sign-in" says, which is where the way a secret reaches a field is written: the password from where the agent keeps its secrets (an agent account of a SkillCDN Console: the console's secret store), a second step by the authenticator key it keeps or the mailbox the code is sent to, and a code only a person receives asked of that person. A secret goes from there to the field and nowhere else: not into the conversation, a message, a record, a file the run keeps or the delivery. The button that signs in is a real click.

Signing in to this site from `headless` or `window` is untried (2026-11). The way of that page was used on other sites, not on this one. The `headless` browser says it is headless and driven ([driven-browser.md](/docs/browser/driven-browser.md) "What a site sees"), and whether the site lets it sign in, or reads it as automation, is not known: a refusal or a check that does not pass is a wall, never worked around, and the run stops and asks a person. The first run that signs in from either says in its delivery what the site showed.

## What the browser must do

The capabilities of [driven-browser.md](/docs/browser/driven-browser.md), and three more:

| Capability | Recognize it by | Needed for |
|---|---|---|
| Hand files to a page's file input | A tool that takes file paths and an input element of the page | The slides of a post. One host's tool took at most 10 MB in one call (checked 2026-11-17) |
| Send key presses to the focused field | A tool that presses a key or a chord | Pasting a caption, selecting a field's whole text |
| Put text on the clipboard of the machine the browser runs on | A shell there with the system's clipboard command | The caption, which is pasted and never typed |

## Screens that stop the work

A login form in the middle of a session is signed in again as "Signing in" says, by an agent that holds the sign-in, once a sitting; a second in the same sitting stops the run. A request to confirm who is signing in is answered only with a code the agent holds the source of or a person gives. Anything else such a request asks (an approval on another device, a photo, a document), a notice about automated behavior, a notice that the account is restricted or suspended: nothing on such a screen is pressed. The run stops, says what the screen says, and a person deals with it in their own time.

## Pace, and what reads as automation

One account that was driven through this interface was suspended one morning and restored the same day, with no reason given; in the hour or so of the evening before, a driven browser had booked four posts and changed the times of fifteen, and a tidy-up had called the site's internal media address from inside the page several times (2026-11). The practice since:

- **Nothing is requested from inside the page.** No `fetch` to the site's own addresses (`/api/`, `graphql`), no header added, no image downloaded to be measured. What a post is and when it went up is read from what the screen and the post's own page show.
- **Real input only.** Every action is a real click at a control found on the screen, or a paste; no script presses a button or sets a field's value, but for a secret put into a field of the sign-in ("Signing in"). A script that only reads (a control's position, a field's text) runs once or twice a screen, not in a loop.
- **Not in bulk.** One sitting books at most one day's posts, and changes at most as many bookings; between one post and the next there is a pause of two to five minutes. More than that is spread over sittings or days.
- **Few openings.** The site is opened for a sitting that books and for one tidy-up a day, after the day's last slot, and not between.

Whether an account posts on fixed slots or varies its minutes is its own policy; the account above kept its fixed slots.

## One session at a time

Two agent sessions that drove the same browser at the same hour both stalled, one of them inside a browser call for days (one host, checked 2026-11-16). A sitting is the only session using the browser, and a job that opens the site on a timer is set for an hour when nobody books.

## What is opened

The site's home page for its navigation alone (who is signed in, the create control), its feed neither scrolled nor read; the sign-in and the checks it leads to, the create dialog, the scheduled list, the account's own profile and its own posts. Messages, notifications, settings and other accounts are not opened, and nothing is liked, followed, commented on or answered.
