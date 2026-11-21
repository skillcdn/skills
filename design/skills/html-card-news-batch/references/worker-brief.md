# The worker's brief

A worker is started with everything below the line, the block filled, and nothing else. It sees nothing of the session, so the block answers what the research and the build would ask; a line the block has nothing for is removed. Where the repository keeps a worker's brief of its own, that brief is used, with this block and this return.

---

You make one card news post, alone, from the topic below to reviewed slides. Nobody can answer you, so do not stop to ask. End with the return block and nothing after it.

## This post

```
slides: at most {n}, fewer where the story holds fewer beats
topic: {one line}                        (from a candidate card: yes | no)
sources: {two or more article links}
brief folder: {path}                     post folder: {path}
brief: to write | already in the brief folder
format: {path of format-spec.json}
readers: {market, language, who reads}
stance and tone: {report | commentary | advocacy for <side>}, {calm | aggressive}
policy: {the account's lines on voice and pictures, as written}
port: {n}                                browser: PLAYWRIGHT_FROM={path}
scratch: {a folder of your own}
change: {a remake only: what changes, what stays}
```

## How you work

1. Load `product/skills/web-card-news-topic-brief` and `design/skills/html-card-news-from-brief` whole, {how this host loads a skill}, every part of each before you act on either. They are the method; this brief says only what differs with no user there.
2. Run the research on the topic as a story handed over, so no candidate list is shown, into the brief folder. A topic line from a candidate card was written from headlines and is often wrong: read the article bodies, correct the premise, and say under `premise` what you corrected. Where the brief is already in the folder, start at step 3.
3. Run the build from that brief, in the format given, into the post folder. The format is settled: no route to one, no study, no variations.
4. Both skills run under a go-ahead: their checkpoints are skipped, their steps and the build's review are not. Where a skill would ask, the block answers; where it does not, take the skill's default and name it under `decided`.
5. The slide count is the block's: a slide with nothing to say is cut, not filled. Serve the preview on your own port and give the export and the review that address. Use the `playwright-core` the block names and install nothing.
6. Write only in your two folders and your scratch folder. The ledger, a candidate list, the format, a script or a document of the repository, another post's folder: read them, never write them. Where a skill says to write one, leave it and say so under `left`. In an account your skills take `post.json` to `brief` and `draft`; `review` is not yours to write. No commit, no push, no board command.
7. A picture or a clip is of the story, or it is not used. Where none of the event can be had, do not fill the cover with one that only relates: take the build's way for a beat with no image and say so under `open`.
8. Return `blocked`, with the reason and the folders as they are, where fewer than two outlets carry the story, where nothing shows it, or where the build's review still fails after two rounds of fixes.
9. A remake changes what `change` names and leaves the rest. Where nothing usable is found, change no file and return `unchanged`: that is a normal result. Where a picture or a clip changes, rewrite every record that tells of the old one (the brief's image entries and what it searched for, the beats' images, the plan's notes, the credits, the caption's credit line) and render every slide again.

## Return

```
post: {post folder}
status: draft | blocked | unchanged
slides: <n>      review: <problems left, or clean>
images: <n> (<count by source_kind>)      clips: <n>
facts: <n> (single-source <n>)      unverified: <n>
premise: <what the topic line had wrong, or "as given">
decided: <the defaults taken where a skill would have asked, or none>
left: <what a skill said to write outside your folders, or none>
open: <what a person must decide, or none>
minutes: <n>      notes: <one or two lines: what was hard, what this brief lacked>
```

A fix comes back to you as one message of numbered items, each naming a limit. Fix them in the plan, render every slide again, run the build's review, and end with the same block.
