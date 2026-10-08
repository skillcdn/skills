# Production log

One Markdown file per episode, next to the script. It is the record the next episode starts from and the proof behind the ledger. It is written as the run goes, not at the end.

## Where the series files live

The bible, the script and the log are files; `<series>` is the slug the bible gives the series. An agent with a filesystem keeps them in the user's working directory as `<series>/bible.md`, `<series>/ep<NN>-script.md` and `<series>/ep<NN>-log.md`. An agent without one writes each into the sandbox with a heredoc and uploads it with `media_upload` as a general file (a `.md` filename) at the delivery, and puts the permanent URLs in the message. The next episode takes the bible and the last log as files or as those links. The delivery says where they are. The log is opened in phase 4, when the first credit is spent, and written as the run goes.

## Sections

1. **Header.** Episode, the script file, the previous episode's folder or links.
2. **New references.** Key, prompt summary, job id, media id. Existing references are named by key and id only.
3. **First frames.** One row per cut: the frame's job id, approved or regenerated, and why.
4. **Cut table.** One row per take, accepted or not:

| Cut | Version | Job id | Length | Heard (both decodes, with times) | Verdict | Notes |
|---|---|---|---|---|---|---|

The notes say what the picture showed shot by shot, what was accepted as close enough, why a take was rejected, and what the retry changed (the word, the particle, the clause). A rejected take that still has a usable picture is marked as kept for inserts.

5. **Final cut.** One block per version, the current one first and marked so: file, duration, hosted media id, the command that produced it (with the environment overrides for replaced takes and line timings), timeline offsets, credits spent on it. An older version keeps its block, marked archived, with the one-line reason it was replaced (a logic error, a stray sound).
6. **Ledger.** Estimate, reserve, spent per item and retry, balance after.
7. **Handover.** What the next episode inherits: the references by key and id, the knowledge table's state at the ending hook, the last three lines and their takes for the previously-on, the lines accepted as close enough, the finalize or upscale offer and whether it was taken.

## Three-file sync

When a take is replaced or a line changes after the script checkpoint, three files change in the same turn: the bible (the knowledge table, the episode table's ending, the production notes), the script (the cut row, the edit plan, the ending hook in the header) and this log (the cut row, the final-cut block). A line that exists in the video and not in the script is a defect of the run.

## Delivery message

In plain words: the episode as a link and, where there is a filesystem, a file; the contact sheet; the accepted take per cut; the ledger against the estimate, retries called out with their reasons; the words accepted as close enough and what was heard; what was edited rather than regenerated; that the people are generated and the platform's label for AI-made content is the user's to set; the finalize offer with its price and the upscale offer, a spend the tool will not price first, neither started; what the next episode inherits and where the three files are. Then wait: the next episode starts only on the user's word, with its own estimate.
