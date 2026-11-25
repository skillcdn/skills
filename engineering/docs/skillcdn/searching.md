# Searching a pack of documents

How to ask a search over a pack so that it answers, and how to read what it found. How words are matched and results are ranked is SkillCDN's specification, not restated here ([the tools](skill://gh/skillcdn/skillcdn/docs/specs/tools.md), "Browse and search": a file of the pack `skillcdn/skillcdn`, at `github.com/skillcdn/skillcdn/blob/main/docs/specs/tools.md` on the git host); this page says what it means for a run.

## What a search does

- `search_repo` matches words, and meaning where the deployment embeds the pack. The connection's instructions say which (`search_repo matches original words`, or words and meaning), and a result's last line says how it was ranked: `Ranked by words and meaning.`; the same ending in `<n> of <m> documents embedded so far` while the pack is still being embedded, the rest found by their words, and by the sections that kept their text; `Ranked by words alone this time` when the search by meaning did not answer; `Ranked by words alone: a query of numbers and names is matched as written.` for a query of identifiers. A result with no such line was ranked by words alone.
- By words, any word of the query may match: a word few documents hold decides more than one every document repeats, and a match in a title, a description or a heading weighs more than one in the body. By meaning, the sections nearest the question are fused into the same order, so something is always returned: the heading path and the excerpt say whether a result bears on the question.
- A document result names the sections that matched, best first and at most two, each with its heading path, the `offset` and `limit` that read it with `read_repo_file`, and an excerpt. A page holds five results by default; `limit` raises it to twenty-five, and `nextCursor` continues.
- `path` scopes a search to a folder: the document set a map named. Scope first where a map puts the question in one set; a search over the whole pack ranks every set against every other.
- A result that is the `README.md` of its folder is marked as the folder's overview: it is the map, and the document it names is the one to read.
- A result marked `(made from other documents: quote what it points to)` is a note or a glossary made from the pack: what is quoted is the section its block quote links to, read there, never the note.
- The connection's instructions name the pack's manifest (`Manifest: read_repo_file SKILLCDN.md ...`) and, where the pack names one, the page to read first (`Start here, before a task: read_repo_file <path>.`). Read that page before the first search, and the manifest when the question is about the pack itself: its front-matter says what the pack is and what it was made from, its body the rules for reading it.

## Words

- Search in the language the pack is written in, which the connection's instructions name (`Written in ko`). A question in another language is translated into the pack's words first.
- English words are matched by their stems: `invoices` finds `invoice`. Korean, Japanese and Chinese words are matched by pairs of characters, so a particle written onto a word does not hide it; still, search for the stem (`연차`, `법인카드`) and not the sentence.
- A number, a code, a path or a version is matched as written: `429`, `SKILL.md`, `2026.2`. A token joined by hyphens, slashes, dots or underscores (`open/closed/held`, `TIDE_RATE_C2`) is found whole and by each of its parts, except a part of digits alone; a name joined by capitals (`TideRateTable`) is found by its words where it names something, a title, a path or a heading, and as written elsewhere. Ask for a clause or a table by its number or name as the pack writes it: a query of at most four such names and numbers is ranked by its words alone, and the document whose heading begins with them stands first.
- Use the pack's own words: the heading a map promised, the term the documents define. By words, a synonym the pack does not use finds nothing. Where the pack is searched by meaning too, ask once more in your own words, since a section near in meaning is found without the pack's word, unless it is one of those still to be embedded.
- Fewer words find more: two or three words a reader would use, not the question as a sentence.

## When a search finds nothing

In this order, one change at a time; a search that was scoped with `path` is first run again over the whole pack with the same words, which is not a change:

1. Another word for the thing, from the map or the description of the document that should hold it.
2. The stem or the base form, without the particle, the plural or the inflection.
3. The folder of the document set alone, with `path`, in case the whole pack buried it.
4. The outline of the document that should hold it: `browse_repo` with the file's path lists its headings; read the section whose heading fits.
5. Three searches and an outline that find nothing: the pack does not say it. The answer says so, and what was tried.

## Reading what was found

- Read the section the result named, with its offset and limit, before quoting; the excerpt is a glimpse, and a match can be in a heading or a table and not in the passage.
- A page lists the links in it after its text, by file, and where a link names a section (`#4.2.7`), that section with the offset and limit that read it: follow a reference by reading that section, not the file. A file of another pack, linked by a skill URI, is listed apart as not readable here, with how it is read at its own pack.
- A document's outline (`browse_repo` with the file's path) says how many tables and code blocks it holds and where they are had as data (`Tables: 2 with 40 rows; as data: <where>`): a table a task needs whole is fetched from there by a program, never copied out of a tool result.
- A section may defer to its neighbour ("see below"): read the neighbour. A section at the start of a document is often the introduction; the detail is in the sections after it.
- A document's outline and the first page of its text name the originals it was made from (`Original:`) with where their bytes are, and the pictures it links to with their words. A file that is not text, an original or a picture, is not read by `read_repo_file`: the answer says where the bytes are. A passage that describes a figure or transcribes a scan is the converting agent's words: an answer that hangs on it says so and names the original with the place in words ("page 12 of the original"), since a host sends an original as a download.
- A `Source` line names the commit a result came from; results of one run may come from different commits when the pack moves between calls, and the line says when a newer commit is still being indexed. Quote the path and the heading path, which hold across commits. An offset holds only for the commit named with it: a note kept for later carries none, and an answer given in the session that read it carries the offset and the limit with the commit, so that a reader opens the section in one call.
