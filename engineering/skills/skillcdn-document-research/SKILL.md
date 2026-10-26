---
name: skillcdn-document-research
description: Answers a question from a large pack of documents (a handbook, a manual, an archive) through SkillCDN, compiles a reference or checks a claim, and keeps what it learned for the next time. Use when the user asks something of a handbook, a manual, an archive or any pack of documents, wants a summary or a comparison across its documents, or wants a question answered once and kept. To turn documents into a pack, use skillcdn-document-pack. Reads the map of each document set first, searches by the words the documents use in their own language, reads the sections a result names by their offset and limit rather than whole files, walks a long document by its outline, quotes every finding with its path and heading, says plainly what the pack does not say, and writes the answer as a research note committed to the pack's repository when the user owns it.
license: MIT
compatibility: Needs the SkillCDN connection to the pack (the MCP tools browse_repo, search_repo and read_repo_file) or the skillcdn command with the pack's address or directory; a shell with git in a checkout of the pack's repository to keep notes. Works in any agent that can call MCP tools or run a shell.
metadata:
  author: skillcdn
  version: "1.2"
  tools: skillcdn
skillcdn:
  include:
    - /engineering/docs/skillcdn/searching.md
    - references/notes.md
  translations:
    ko:
      title: SkillCDN 문서 팩으로 조사하기
      description: 큰 문서 팩을 SkillCDN을 통해 다루어 질문에 답하고, 참고 자료를 엮고, 주장을 확인하며, 알게 된 것을 다음을 위해 남깁니다. 문서 세트의 지도를 먼저 읽고, 문서가 쓰인 언어의 단어로 검색하고, 파일 전체가 아니라 결과가 가리키는 섹션을 오프셋과 길이로 읽고, 긴 문서는 아웃라인으로 걸어 내려가고, 모든 발견을 경로와 제목으로 인용하고, 팩이 말하지 않는 것은 그렇다고 말하고, 사용자가 저장소를 가졌으면 답을 조사 노트로 커밋합니다. 핸드북, 매뉴얼, 아카이브나 어떤 문서 팩에든 질문할 때, 문서들을 요약하거나 비교할 때, 한 번 답한 질문을 남겨 두고 싶을 때 쓰세요. 문서를 팩으로 만들 때는 skillcdn-document-pack을 쓰세요.
---
# Research in a pack of documents

What goes in: a question, a reference to compile or a claim to check, and a pack of documents served through SkillCDN. What comes out: an answer with every finding quoted from the pack by its path and heading, what the pack does not say said plainly, and, when the user owns the repository, a research note committed to it so that the next run finds the answer before it searches. The pack's structure does the work: the maps say what there is, a search names the sections that matched, and a section is read by its offset and limit in one call. The tools are SkillCDN's and are not restated here ([what an agent gets over MCP](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/tools.md)); this skill carries the method.

## How the user is involved

- **Questions:** one at most, at the start and only when the request leaves it open: which pack, when more than one is connected and the question does not say.
- **Checkpoints:** a scope the pack cannot settle (two document sets contradict each other, the question is wider than the pack), stated and asked about before the answer is written; the note, before it is committed. One short message each; one word continues.
- **Go-ahead:** when the user says to go ahead alone, the note is committed without being shown first. A push follows the agreement of the repository it lands in, and the user's word where it has none.
- **No repository:** when the user has no checkout, the note is delivered as text, with where it would go.

## Requirements

| What | Used for |
|---|---|
| The SkillCDN connection to the pack, or the `skillcdn` command (`skillcdn browse`, `skillcdn find`, `skillcdn file` with the pack's address or directory) | Reading the maps, searching, reading sections, outlining a document. The connection's instructions name the pack and its language. |
| Optional: a shell with git in a checkout of the pack's repository | Keeping the note ([notes.md](references/notes.md)). Without it, the note is text in the delivery. |

Check these before the first message. Without a connection or the command, stop and say what to connect: the pack's address at a deployment, or the command on a directory. How a search over a pack behaves, and how to ask it so that it answers, is in the area's document set [`engineering/docs/skillcdn/`](/engineering/docs/skillcdn/README.md): [searching.md](/engineering/docs/skillcdn/searching.md) is included and arrives with this skill wherever SkillCDN serves it; a copy of this directory lacks it, and fetches it from `engineering/docs/skillcdn/` of the repository this skill comes from (`github.com/skillcdn/skills`, which is not the pack the question is put to) or reads it as a file at `docs/skillcdn/` of the engineering plugin.

## Inputs

| Input | Source |
|---|---|
| The question | The user's words. A reference to compile (everything the pack says about one subject) and a claim to check (is this true according to the pack) are questions too. |
| The pack | The connection the request names, or the only one connected; the mounted folder when the connection is to a folder. Where the agent is connected to a deployment's root rather than to a pack, its one tool, `search_packs`, searches every public pack the deployment serves and names the address of each pack that matched; the pack is the one whose address the user then connects, for the four tools. |
| The language | What the connection's instructions say the pack is written in (`Written in ko`), else the language of the maps; the search is in that language. |
| Everything else | Derived: which document sets the question concerns, how many results to read, what the note is called. |

## Workflow

Each phase produces a named artifact. The answer is built from sections read, never from a result's excerpt alone.

### Phase 1: Frame

Produces the **frame**: the question in one line, what would answer it (a number, a rule, a procedure, a list, a yes or no), and the words it is likely written with in the pack's language.

1. Say what kind of answer the question wants, so that a section is recognized as the answer when it is read.
2. Where the user's words and the pack's language differ, translate the words the pack would use; where the question uses a synonym or an abbreviation, note the words the pack might use instead ([searching.md](/engineering/docs/skillcdn/searching.md), "Words").
3. Where a research note on the question exists in the pack ([notes.md](references/notes.md), "Where notes live"), read it first: the answer may be there, with its sources to check.

### Phase 2: Map

Produces the **map reading**: the document sets the question concerns, and the documents in them that are likely to answer.

1. Read the connection's instructions, then the map of each document set the question may concern: the `README.md` of the folder, named as the folder's overview by `browse_repo`. A pack of thousands of pages has many sets; the maps say which to search.
2. Where a document is long and the question is about one part of it, outline it: `browse_repo` with the file's path lists its headings with the offset and limit that read each section.

### Phase 3: Search

Produces the **candidate sections**: the sections a search named, with their path, heading, offset and limit.

1. `search_repo` with the words of the frame, in the pack's language, scoped with `path` to the document set the map named when the pack is large. Where the connection's instructions say the pack is searched by meaning as well as by words, search once more in the frame's own words ([searching.md](/engineering/docs/skillcdn/searching.md), "What a search does"). Each document result names the sections that matched, best first, each with its heading path, its offset and limit, and an excerpt.
2. Search again with other words when the first search misses ([searching.md](/engineering/docs/skillcdn/searching.md), "When a search finds nothing"): the pack's words for the thing, a particle or an inflection dropped, the heading a map promised. Three searches and the outline of the document that should hold it that find nothing mean the pack does not say it, and the answer says so.
3. Keep the candidates in order of the search; read them in that order.

### Phase 4: Read

Produces the **evidence**: the passages read, quoted with their path and heading path.

1. Read a candidate section with `read_repo_file`, the path and the offset and limit the result gave. Read the neighbouring section when the passage refers to it, and the whole document when the question is about the document rather than a passage.
2. Follow a link in the passage to another document of the pack when the passage defers to it; the link is a repository-root path when it starts with `/`.
3. Stop reading when the frame is answered and a second section confirms it, or when the candidates are exhausted. A rule about money, access or safety is quoted, never paraphrased.

### Phase 5: Answer

Produces the **answer**: the finding, the quotes that support it, each with its path and heading path, and what the pack does not say.

1. Lead with the answer in the shape the frame asked for. Then the evidence: each quote with `path` and the heading path (`docs/billing.md, Billing > Late fees`), so that a reader opens the section.
2. Where two documents disagree, say so and quote both; where the pack is silent, say "the pack does not say" rather than inferring. A claim to check is answered true, false or not stated by the pack, with the quote.
3. Where the question was wider than the pack, say what part was answered and what was not.

### Phase 6: Keep

Produces the **note**, when the user owns the repository ([notes.md](references/notes.md)).

1. Write the note in the notes document set: the question, the date, the answer, the quotes with their sources, and what was not found. One note per question; a question asked again updates its note.
2. Add the note's line to the set's map, and the set to the manifest's roots when it is new.
3. Checkpoint, skipped on a go-ahead: the note as it will be committed. Commit as the repository's agreement says, and push only as it allows; once served, the next run's phase 1 finds the note by its words.

## Hard rules

1. Every finding is quoted from a section that was read, with its path and heading path, and checked against the text word for word before the answer is written. An excerpt in a search result is a pointer, not evidence.
2. The pack is the source. What it does not say is said to be not said; nothing is filled in from memory or from outside the pack unless the user asks for it and the answer marks it as such.
3. Search in the pack's language, with its words; three searches that find nothing end the search, and the answer says what was tried.
4. Sections are read by their offset and limit; a whole document is read only when the question is about the document.
5. A note holds the question, the answer and the sources, and nothing private that the question or the user's context carried; it is shown before it is committed unless the user said to go ahead, and pushed only as the repository's agreement allows.
6. Two documents that disagree are both quoted; the agent does not choose between them without saying so.

## Terminology

| Term | Meaning |
|---|---|
| Pack | A repository, or a folder of one, served through SkillCDN as one unit; a document pack holds mostly documents. |
| Map | The `README.md` of a document set: one line per document, what each holds. Read before searching. |
| Section | The text under one heading, to the next heading; what a search result names, with its heading path, offset and limit. |
| Outline | The headings of a document with the offset and limit of each section, answered by `browse_repo` for a file. |
| Frame | The question in one line, the shape of its answer, and the words it is likely written with. |
| Candidate | A section a search named, not yet read. |
| Evidence | A passage read, quoted with its path and heading path. |
| Note | A research note: the question, its answer and its sources, kept in the pack's notes set. |
