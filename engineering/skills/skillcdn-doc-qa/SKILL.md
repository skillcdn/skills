---
name: skillcdn-doc-qa
description: Answers a question from a pack of documents served through SkillCDN (a handbook, a manual, a policy set, an archive), with every citation verified against the section it quotes, and says plainly what the pack does not say. Use when a user asks "what does the handbook say about this", "answer this from our documents", "is this true according to the manual", "which document covers this", or puts a question to any document pack, and wants the answer now with its sources rather than a note kept for later. Frames the question in the pack's words, reads the maps, searches by words and by meaning where the deployment does, reads the sections a result names by their offset and limit, drafts the answer, re-reads every cited section to check each quote word for word and drops what does not hold, and answers with the path, the heading, the offset and the limit of each citation. To keep the answer as a note in the pack, or compile a reference, use skillcdn-document-research. Nothing is spent.
license: MIT
compatibility: Needs the SkillCDN connection to the pack (the MCP tools browse_repo, search_repo and read_repo_file) or the skillcdn command with the pack's address or directory. Works in any agent that can call MCP tools or run a shell; no file tool is needed, since the answer is the delivery.
metadata:
  author: skillcdn
  version: "1.0"
  tools: skillcdn
skillcdn:
  include:
    - assets/answer.example.md
    - /engineering/docs/skillcdn/searching.md
  translations:
    ko:
      title: 문서 팩에서 인용을 검증한 답
      description: SkillCDN으로 서빙되는 문서 팩(핸드북, 매뉴얼, 규정집, 아카이브)에서 질문에 답합니다. 인용은 모두 인용한 섹션을 다시 읽어 검증하고, 팩이 말하지 않는 것은 그렇다고 분명히 말합니다. "핸드북에 이건 뭐라고 돼 있어", "우리 문서에서 답 찾아줘", "매뉴얼대로면 이게 맞아?", "규정 어디에 있어"라고 묻거나, 어떤 문서 팩에든 질문하면서 나중에 남길 노트가 아니라 지금 출처가 붙은 답을 원할 때 쓰세요. 질문을 팩의 말로 바꾸고, 지도를 읽고, 단어로, 배포가 의미 검색을 하면 의미로도 검색하고, 결과가 가리키는 섹션을 오프셋과 길이로 읽고, 답을 쓴 뒤 인용한 섹션을 모두 다시 읽어 한 글자씩 맞는지 확인하고 맞지 않는 것은 뺀 다음, 인용마다 경로·제목·오프셋과 길이를 달아 답합니다. 답을 팩에 조사 노트로 남기거나 여러 문서를 가로지르는 참고 자료를 엮을 때는 skillcdn-document-research를 쓰세요. 비용이 들지 않습니다.
---
# An answer from a pack of documents, with every citation checked

A question goes in, with a pack of documents served through SkillCDN; an answer comes out that leads with the answer itself, then the quotes that support it, each with the path, the heading path and the offset and limit of the section it was read from, and then what the pack does not say. Every quote is checked once more against the section before the answer is sent, so that a reader who opens the citation finds the words. Nothing is written into the pack and nothing is spent: the answer is the delivery, and a user who wants it kept for the next time starts the research skill, which writes notes.

## How the user is involved

- **Questions:** one at most, at the start and only when the request leaves it open: which pack, when more than one is connected and the question does not say, asked as "Which pack is this for: <the connected packs, by name>?".
- **Checkpoints:** none; nothing waits for a reply. Each phase ends with one line in the chat, as the rules served with this skill ask: the frame, the sets the maps named, the candidates by path and heading, the sections read, the quotes that held and any dropped; then the answer. A scope the pack cannot settle (two documents contradict each other, the question is wider than the pack) is said in the answer, with both readings quoted.
- **Several questions:** a request that holds two (a rule, and a claim about it) gets a frame per question in the order asked, each with its own searches, and one answer that takes them in that order; a question that comes later is answered as it comes. The sections read for an earlier question are candidates for the next, and a citation reused says so.
- **A question the pack does not cover:** said after three searches and an outline, with the nearest passage read, checked and quoted so that the user sees where the pack stops, and where else to look when the pack names it.

## Requirements

| What | Used for |
|---|---|
| The SkillCDN connection to the pack, or the `skillcdn` command (`skillcdn browse`, `skillcdn find`, `skillcdn file` with the pack's address or directory) | Reading the maps, searching, reading sections by offset and limit, re-reading a cited section. The connection's instructions name the pack and its language. |

Check it before the first message. Without a connection or the command, stop and say what to connect: the pack's address at a deployment, or the command on a directory. How a search over a pack behaves, and how to ask it so that it answers, is in the area's document set [`engineering/docs/skillcdn/`](/engineering/docs/skillcdn/README.md): [searching.md](/engineering/docs/skillcdn/searching.md) is included and arrives with this skill wherever SkillCDN serves it; a copy of this directory lacks it, and fetches it from `engineering/docs/skillcdn/` of the repository this skill comes from (`github.com/skillcdn/skills`, which is not the pack the question is put to) or reads it as a file at `docs/skillcdn/` of the engineering plugin. The pack under question is its own connection: `read_repo_file` on it reads that pack, and this skill's pages are read only through the connection that served the skill. The shape of an answer is in [answer.example.md](assets/answer.example.md), which comes with the skill.

## Inputs

| Input | Source |
|---|---|
| The question | The user's words. A claim to check ("is it true that ...") is answered true where a section states it or a rule of the pack covers the case in the pack's own words, false where a section states the contrary (another and only another, or the case excluded), true with the condition where a section adds one to the case asked (a second approver above a limit), and not stated otherwise; a section about the case outranks a general rule, and both are quoted. A term the user uses that the pack names differently is read as the pack's term only where the pack itself equates them, and the answer says which reading it took. |
| The pack | The connection the request names, or the only one connected; the folder the connection mounts, when it is to one folder of a repository rather than to its root. Connected to a deployment's root (an address with no pack in it) rather than to a pack, `search_packs` names the packs that match, and the pack is the one the user then connects. |
| The language of the pack | What the connection's instructions say (`Written in ko`), else the language of the maps; the search and the quotes are in that language. |
| Everything else | Derived: which document sets the question concerns, how many sections to read, whether an earlier question's sections serve. |

## Workflow

The answer is built from sections read, never from a result's excerpt alone.

### Phase 1: Frame

Produces the **frame**: the question in one line, the shape of its answer (a number, a rule, a procedure, a list, a yes or no), and the words it is likely written with in the pack's language, translated where the user's language differs, with the pack's own term where the question uses a synonym ([searching.md](/engineering/docs/skillcdn/searching.md) "Words"); the terms the maps use are added in phase 2, before the first search.

### Phase 2: Map

Produces the **map reading**: the document sets the connection's instructions name, or `browse_repo` on the root lists, and the `README.md` of each set the question could concern, read whole (the folder's overview that `browse_repo` names; a set without one is listed with `browse_repo`); a document of many sections that the question is about is outlined with `browse_repo` on its path. The frame's words are revised with the terms the maps use (the heading a map promised, the term a description defines). The first search takes one set, with `path`, when the maps put the question in one set, and the whole pack when they do not; a scoped search that finds nothing is run again over the whole pack with the same words before anything else, and that run is not one of the three searches.

### Phase 3: Search

Produces the **candidates**: the sections a search named, with their path, heading path, offset and limit, in the order of the search.

1. `search_repo` with the frame's words, at the scope phase 2 set. Where the result's last line says the ranking was by words and meaning, search once more in the agent's own words for the thing, a short phrase rather than the pack's terms, since a search by meaning finds a section near in meaning without the pack's word; where it says by words alone this time, search once more with other words of the pack's ([searching.md](/engineering/docs/skillcdn/searching.md) "What a search does"). These are two of the three searches.
2. A search finds nothing when no section it names bears on the frame: a search ranked by meaning always returns its nearest sections, so the heading path and the excerpt say so for a section far from the frame, and a section near it is read (phase 4's read of it) before it is dismissed; a search whose sections were read and gave no answer has found nothing. A search that finds nothing changes one thing at a time, in the order searching.md "When a search finds nothing" gives. Three searches, counting the two of step 1, and the outline of the document that should hold it, that find nothing mean the pack does not say it: the nearest passage any search returned becomes the candidate, is read in phase 4 and checked in phase 5 like any citation, and phase 6 says what was tried.
3. The sections an earlier question of the session already read are candidates too, named as such.

### Phase 4: Read

Produces the **evidence**: the passages read, each quoted with its path, heading path, offset and limit.

1. Read each candidate with `read_repo_file` at its offset and limit; read the neighbouring section where the passage defers to it, and follow a link to another document of the pack where the passage points there.
2. Stop when a section answers the frame and a second section says the same or defers to it, or when every candidate is read. A frame one section alone answers is answered from it, and the answer says that no other section read says the same; candidates all read with no answer send the search back to phase 3 for its next change. A rule about money, access or safety is quoted, never only paraphrased: the lead may say it in its own words, and the quote beneath carries the rule's own numbers, names and conditions.

### Phase 5: Draft and verify

Produces the **draft** and the **verification**: the answer in the frame's shape with its quotes, then every quote re-read.

1. Draft: the answer first; then each quote in the pack's language, with its citation.
2. Verify: for every citation, read the cited section once more at its path, offset and limit. Where the read returns another section (the pack moved between calls, which the `Source` line says), find the section by its heading through the document's outline and re-cite it first. Then find the quoted words in the section word for word; a table is quoted as its row's cells in order and checked cell by cell. A quote that is not there as written is corrected to the words that are, or dropped with its claim, and the answer says in one line that a quote was dropped, without its claim. Nothing that failed the check stays in the answer.

### Phase 6: Answer

Produces the **answer**, as [answer.example.md](assets/answer.example.md) shapes it: the answer in two or three sentences; the citations, each as the quote with `path`, the heading path and `offset`/`limit` (`docs/billing.md, Billing > Late fees, offset 1200 limit 800`), so that a reader with the connection opens the section in one call; where two documents disagree, both quoted and said so; what the pack does not say, and the nearest passage where the question is outside the pack; and one line on what to do next where the pack names it. The commit of the check's read, from its `Source` line, is named once, because offsets belong to it; a citation checked at another commit names its own. When the user wants the answer kept, say that `skillcdn-document-research` writes it as a note in the pack.

## Verdicts

| Result | Verdict |
|---|---|
| A quote that the re-read does not find word for word | Corrected to the section's words, or dropped with its claim; never sent as it was |
| A citation whose offset returns another section | Re-cited from the document's outline by its heading |
| A finding from a result's excerpt that no section was read for | Not evidence; the section is read or the finding dropped |
| Two documents that answer differently | Both quoted, the difference said; no choice made without saying so |
| Three searches and an outline that find nothing | The pack does not say it; the nearest passage read, checked and quoted, what was tried listed |
| A question wider than the pack | The part the pack answers, answered; the rest named as not in the pack |
| A claim to check | True where a section states it or a rule covers the case, false where a section states the contrary, true with the condition where a section adds one to the case asked, else "not stated by the pack" with the nearest passage; the section about the case outranks the general rule and both are quoted; the reading of a term the pack names differently said |

## Hard rules

1. Every citation is read twice: once to find it, once to check its words before the answer is sent. An excerpt in a search result is a pointer, never evidence.
2. The pack is the source. What it does not say is said to be not said; nothing is filled in from memory or from outside the pack unless the user asks for it, and the answer then marks it as outside the pack.
3. Search in the pack's language, with its words; three searches and an outline that find nothing end the search, and the answer says what was tried.
4. Sections are read by their offset and limit; a whole document is read only when it is a map or the question is about the document.
5. Nothing is written into the pack and nothing is spent; a note is the research skill's.
6. Two documents that disagree are both quoted; the agent does not choose between them without saying so.

## Terminology

| Term | Meaning |
|---|---|
| Pack | A repository, or a folder of one, served through SkillCDN as one unit; a document pack holds mostly documents. |
| Map | The connection's instructions or `browse_repo` on the root, which name the document sets, and the `README.md` of a set, one line per document. Read before searching. |
| Section | The text under one heading, to the next; what a search result names, with its heading path, offset and limit. |
| Frame | The question in one line, the shape of its answer, and the words it is likely written with. |
| Candidate | A section a search named, not yet read. |
| Evidence | A passage read, quoted with its path, heading path, offset and limit. |
| Verification | The second read of every cited section, in which each quote is found word for word or dropped. |
| Nearest passage | The section a search returned closest to a question the pack does not answer, quoted so that the reader sees where the pack stops. |
