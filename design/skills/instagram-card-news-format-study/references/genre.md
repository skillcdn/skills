# A genre: candidates for the reference, and the genre's common form

Read before phase 1 when the reference is a genre (the kind of account the user's own will be, with no account named) or when the request is for something new from a reference. A genre gives the user candidates to pick one reference from; its common form is read only where the user asks for the form itself, or where no single account can be read from the host ([walled-host.md](walled-host.md)).

## Finding the candidates

Three to five accounts that post card news for the user's kind of account and audience, in the market's language (the request's, unless it names another market), any the user names first. Find them with a web search for the genre's outlets (an outlet's home page names its Instagram account) and for the genre's words with "card news"; without a search tool, the accounts are the ones the user names. Open each profile as phase 1 says and list it in `profile.md` with its name line and the post phase 2 would read; an account with no carousel among its visible posts is replaced.

## The candidates checkpoint

Show the candidates before anything is measured: each in a line with its name line, what its card news looks like and one post's link, with the recommendation, the account whose kind and audience are nearest the user's with card news among its visible posts. One word picks. The pick is the reference, read from here on as a named account is, into `card-news/<handle>/`. On a go-ahead the recommended candidate stands as the reference, said so.

## The genre's common form

Read only where the user asks for the genre's form itself. On each account, read one recent carousel of the user's kind (the kind the request's story is, else the genre's most common), another post where the first is not a carousel, slide by slide as phase 2 says. The spec goes to `card-news/genre-<a few words>/`. The categories are the genre's: the kinds its grids show, named in plain words without shares, since one post per account is opened; no cadence is counted. A slide type is confirmed where two accounts use it.

## Something new from a reference

The reference is read as a named account, and its genre is read in the same run as the crowd the variations leave: one post on each of three to five other accounts of its kind, into `card-news/genre-<a few words>/` beside the reference's spec.

## Deriving a genre's spec

In phase 3 the spec holds what two or more of the accounts share (a slide type, a density, a register pattern), each with `seen_in` naming the posts; what one account alone does goes into the style notes as that account's. `never` stays empty, a build's `order` is `varies` unless two accounts' builds match, and `cadence` is left out, since no kind is read twice on one account. `source.read` is `genre`.

## Verdicts

| Result | Verdict |
|---|---|
| A genre whose accounts share no slide type | The spec holds what two share, the style notes describe each account's build, and the delivery says the genre has no common form and names the account closest to the request as the start for the variations |
| An account with no carousel among its visible posts | Replaced by another of the kind before the candidates are shown |
