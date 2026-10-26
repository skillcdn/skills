# Searching a pack of documents

How a search over a pack behaves, and how to ask it so that it answers. The rules are SkillCDN's ([the words that match](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/tools.md#the-words-that-match)); this page says what they mean for a run.

## What a search does

- `search_repo` matches words, and meaning where the deployment embeds the pack: the connection's instructions say which (`search_repo matches original words`, or words and meaning, in which case a question may also be asked in the agent's own words), and a result ends with a line on how it was ranked (`Ranked by words and meaning.`, or `Ranked by words alone this time` when the search by meaning did not answer). By words, any word of the query may match and the results are ordered by how well, a word few documents hold deciding more than one every document repeats, with titles and descriptions weighing more than body text; by meaning, the sections nearest the question are fused into the same order. Skills come before documents.
- A document result names the sections that matched, best first, each with its heading path, the `offset` and `limit` that read it with `read_repo_file`, and an excerpt of the passage. Over MCP a result names at most two sections and a page holds five results by default; `limit` raises it to twenty-five, and `nextCursor` continues.
- `path` scopes a search to a folder: the document set a map named. Scope first where a map puts the question in one set; a search over the whole pack ranks every set against every other.

## Words

- Search in the language the pack is written in, which the connection's instructions name (`Written in ko`). A question in another language is translated into the pack's words first.
- English words are matched by their stems: `invoices` finds `invoice`, `refunded` finds `refund`. Korean, Japanese and Chinese words are matched by pairs of characters, so an inflected word finds its stem and a particle written onto a word does not hide it; still, search for the stem (`연차`, `법인카드`) rather than the sentence.
- A number, a code, a path or a version is matched as written: `429`, `SKILL.md`, `2026.2`.
- Use the pack's own words: the heading a map promised, the term the documents define. By words, a synonym the pack does not use finds nothing; where the connection says the pack is searched by meaning too, ask once more in your own words, since a section near in meaning is found without the pack's word, and a commit embedded a moment ago may still answer by words alone for a while.
- Fewer words find more: two or three words a reader would use, not the question as a sentence. Stop words (`the`, `how`, `is`) are dropped anyway.

## When a search finds nothing

In this order, one change at a time; a search that was scoped with `path` is first run again over the whole pack with the same words, which is not a change:

1. Another word for the thing, from the map or the description of the document that should hold it.
2. The stem or the base form, without the particle, the plural or the inflection.
3. The folder of the document set alone, with `path`, in case the whole pack buried it.
4. The outline of the document that should hold it: `browse_repo` with the file's path lists its headings; read the section whose heading fits.
5. Three searches and an outline that find nothing: the pack does not say it. The answer says so, and what was tried.

## Reading what was found

- Read the section the result named, with its offset and limit, before quoting; the excerpt is a glimpse, and a match can be in a heading or a table rather than the passage.
- A section that starts with a heading and ends at the next heading may defer to its neighbour ("see below"): read the neighbour. A section at the start of a document is often the introduction; the detail is in the sections after it.
- A `Source` line names the commit a result came from; results of one run may come from different commits when the pack moves between calls, and while the pack's newest commit is still being indexed the line says so (`newest <commit> indexing`) and the result is read from the last indexed one. Quote the path and the heading path, which hold across commits; an offset holds only for the commit named with it, so a note kept for later carries none, and an answer given in the session that read it carries the offset and the limit with the commit, so that a reader opens the section in one call.
