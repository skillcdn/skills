---
name: skillcdn-document-pack
description: Turns documents a person has (PDF, Word, slides, spreadsheets, HTML, wiki and chat exports, plain text) into a pack of documents in the SkillCDN Format, in a repository they own, so that agents browse, search and read them through SkillCDN. Surveys the sources, plans the layout with the user, converts each document to Markdown with the tools the agent has, lays them out one file per document or chapter with a title and a description, writes the map of every document set, describes the figures and transcribes the scanned pages into text beside the images, declares the document roots and the language in the manifest, checks the pack with the indexer's own check and commits it. Use when the user wants a body of documents made searchable and readable by agents, wants to add documents to a pack, or asks for a handbook, a manual or an archive as a pack. To work with a pack that exists, use skillcdn-document-research.
license: MIT
compatibility: Needs a shell with git and Node.js in a checkout of the target repository, and whatever converts the user's formats on this machine, found at run time; a vision model of the agent for figures and scanned pages. Works in any agent that can read files, run a shell and look at an image.
metadata:
  author: skillcdn
  version: "1.0"
  tools: skillcdn
skillcdn:
  include:
    - references/layout.md
    - references/conversion.md
    - /engineering/docs/skillcdn/serving.md
  translations:
    ko:
      title: 문서를 SkillCDN 문서 팩으로 만들기
      description: 사용자가 가진 문서(PDF, 워드, 슬라이드, 스프레드시트, HTML, 위키와 채팅 내보내기, 텍스트)를 사용자의 저장소에 SkillCDN 포맷의 문서 팩으로 만들어, 에이전트가 SkillCDN을 통해 탐색하고 검색하고 읽게 합니다. 원본을 조사하고, 레이아웃을 사용자와 정하고, 에이전트가 가진 도구로 각 문서를 마크다운으로 바꾸고, 문서나 장 단위로 한 파일씩 제목과 설명을 붙여 배치하고, 문서 세트마다 지도를 쓰고, 그림은 설명하고 스캔된 쪽은 글자로 옮겨 이미지 옆에 두고, 매니페스트에 문서 디렉터리와 언어를 선언하고, 인덱서의 검사를 통과시킨 뒤 커밋합니다. 문서 모음을 에이전트가 검색하고 읽을 수 있게 만들 때, 팩에 문서를 더할 때, 핸드북이나 매뉴얼이나 아카이브를 팩으로 만들 때 쓰세요. 이미 있는 팩으로 일할 때는 skillcdn-document-research를 쓰세요.
---
# Documents into a pack

What goes in: documents a person has, in whatever formats, and a repository they own or a folder of one. What comes out: those documents as a pack in the SkillCDN Format, one Markdown file per document or chapter with a title and a description, a map in every document set, images described and scans transcribed as text, a manifest that declares the document roots and the language, a passing check, and a commit the user approved; then, once pushed, an agent that connects to the repository's address finds a section of any document by its words and reads it by its offset. SkillCDN never receives a file: everything happens in the checkout, and the service indexes what is pushed. The format is SkillCDN's and is not restated here ([document packs](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/skill-repo.md#document-packs)); this skill carries the method, from the sources to the commit.

## How the user is involved

- **Questions:** three at most, asked in one message at the start and only when the request leaves them open: where the documents are, which repository or folder they go into, and what language they are written in when the sources do not say.
- **Checkpoints:** the layout plan, before anything is converted; the pack, after the check passes and before it is committed; the delivery. One short message each, in plain words; one word continues.
- **Go-ahead:** when the user says to go ahead alone, the pack is committed without being shown first. Every push follows the agreement of the repository, and the user's word where it has none.
- **Changes mid-run:** a change to the layout after conversion began is applied to what is not converted yet, and the converted files are moved or renamed to match; nothing is converted twice for a rename.

## Requirements

| What | Used for |
|---|---|
| A shell with git and Node.js in a checkout of the target repository | The layout, the files, `npx @skillcdn/cli check`, the commit. |
| What converts each format on this machine, found at run time ([conversion.md](references/conversion.md) says how to look) | Turning each source into Markdown. A format nothing converts is reported, never guessed at. |
| The agent's own vision model | Describing a figure and reading a scanned page, written as text beside the image. |
| Optional: the SkillCDN connection to the repository, or the `skillcdn` command on a directory | Trying the pack as an agent will meet it, before and after the push. |

Check these before the first message. Without a checkout, stop: say that the pack is written into a checkout of a repository the user owns, and offer to make one (`git init` in a new directory, or a clone of theirs). Without a converter for a format, convert what can be converted, list the files that could not, and say what would convert them.

What the SkillCDN skills share is in [`engineering/docs/skillcdn/`](/engineering/docs/skillcdn/README.md); [serving.md](/engineering/docs/skillcdn/serving.md), which says how a push becomes what an agent is served and how to see it, is included and arrives with this skill wherever SkillCDN serves it. A copy of this skill's directory lacks it: say so in the first message and fetch it from `engineering/docs/skillcdn/` of the repository this skill comes from (for this pack, `github.com/skillcdn/skills`) where the agent can.

## Inputs

| Input | Source |
|---|---|
| The documents | A folder, an archive, a set of files or exports the user points to; a wiki or a drive they have exported. The agent reads them from its own environment: nothing is uploaded anywhere. |
| The repository | The checkout the agent is in, or the one the user names. A new pack goes at the root; documents added to a pack go into a document set of it. |
| The language | What the sources are written in: read from them, asked when they mix languages or the agent cannot tell. One manifest per language folder. |
| Everything else | Derived and shown at the layout checkpoint: the document sets, the files and their names, where a long document is split, what the maps say, what is left out. |

## Workflow

Each phase produces a named artifact. Scratch files stay outside the repository; only the pack is committed.

### Phase 1: Survey

Produces the **inventory**: every source with its format, size, language, the structure it has (chapters, headings, pages, sheets), the images and scans it holds, and what it is about in one line.

1. Walk the sources. Count them by format; open one of each format and note what structure the converter will keep ([conversion.md](references/conversion.md), "What each format keeps").
2. Note what must stay out: secrets, personal data, drafts the user did not mean, duplicates and older versions of the same document. The pack is served to whoever holds the address.
3. Note the language of each source, and where one source mixes languages.

### Phase 2: Plan the layout

Produces the **layout plan** by [layout.md](references/layout.md): the document sets, the file for each document or chapter with its name and its title, where a long document is split, the maps, the manifests, and what stays out, shown at the layout checkpoint.

1. Group the sources into document sets by what they are about and who reads them, one folder each under the document roots, with a `README.md` as the set's map.
2. One file per document or chapter, never per page ([layout.md](references/layout.md), "One file per document or chapter"): a chapter long enough to carry a title and a summary, short enough to read by sections, and under the per-file indexing limit the check prints.
3. A manifest at the root with the document roots and the language; a manifest of its own in a folder written in another language.

Checkpoint, in plain words: the sets and what each holds, how many files, which documents are split and where, the maps, the language of each folder, what stays out and why. "OK" converts.

### Phase 3: Convert

Produces the **converted files**, one per planned file, as Markdown.

1. Convert each source with the converter found for its format, as [conversion.md](references/conversion.md) says for it: headings kept as headings, tables as tables, lists as lists, footnotes at the end of their section, the text of the body and nothing of the page furniture (headers, footers, page numbers).
2. Split where the plan says, at headings, and give each part the heading path it came from so that a chapter read alone still says where it belongs.
3. Images: keep the image file beside the document when the user wants it in the pack, and write what the image shows as its alternative text and, for a figure that carries meaning, a caption paragraph under it ([conversion.md](references/conversion.md), "Figures and images"). A scanned page is read with the vision model and written as text, with the image kept or dropped as the user said.
4. Mark what the converter lost and the agent could not restore (a table too wide, an equation, a form) in a short note in the file, so that a reader knows to go to the source.

### Phase 4: Describe

Produces the **described pack**: every file with its front-matter, every set with its map, the manifests.

1. Front-matter on every file: `title`, the document's own title; `description`, one or two sentences of what the document holds and who reads it, in the words a reader would search with; `source`, where it came from (the file name, the export, the date), without anything private.
2. Headings that name the parts: where the source had none, add the headings the text supports and no more; a heading a search names should tell a reader what the section holds.
3. The map of each set: `README.md` with one line per document, as [layout.md](references/layout.md), "Maps" shows.
4. The manifests: `documents` listing the roots, `language` the language, `description` who the pack is for ([layout.md](references/layout.md), "Manifests").

### Phase 5: Check

Produces the **check report**.

1. `npx @skillcdn/cli check` in the checkout until it prints `ok: no index diagnostics`. Read the documents it lists with their section counts: a document with no sections has no headings and is read whole; a document named as too large to search is split. Read the instructions a client is told on connect: they quote the manifest's description.
2. Where the repository has a check of its own (`node scripts/check.mjs` in a fork of the reference pack), run it too.
3. Where the `skillcdn` command is at hand, `skillcdn find <directory> <words>` for three questions the documents answer, in the pack's language: each should name the document and the section that answers, and `skillcdn file <directory> <path> --offset <n> --limit <n>` with the numbers the result gave should read that section. A question that finds nothing is a title, a description or a heading that does not say what the text says: fix the words.

Checkpoint, skipped on a go-ahead: the tree of the pack, the counts, the check's last line, the three questions and what each found.

### Phase 6: Commit

Produces the **commit**.

1. Commit the pack's files and nothing else, as the repository's agreement says, naming any unrelated change left in the tree.
2. Push only as the repository's agreement allows, with the user's word: a push to the default branch is what SkillCDN serves ([serving.md](/engineering/docs/skillcdn/serving.md)). Once served, connect or open the address and ask one of the three questions through `search_repo`; read the section it names with `read_repo_file` and the offset and limit it gave.
3. Deliver in one message: the address or the directory, how many documents and sections, what was left out, the files whose conversion lost something and where the source is, and what to do next (connect an agent; the skill skillcdn-document-research of this area, for working the pack).

### Adding to a pack

The same phases over the new sources alone: the inventory covers them, the plan fits them into the sets that exist or adds a set, the maps and the manifests change where they must, and nothing that was there is converted again or reformatted in passing.

## Hard rules

1. Nothing is invented. The pack holds what the sources say, as they say it; a figure's description says what is visible; what the converter lost is marked, never filled in.
2. Nothing private enters the pack: secrets, personal data, customer material the user did not mean to publish. What is doubtful is asked about, and left out until answered.
3. One file per document or chapter, never per page, each with a title and a description, and a map in every set.
4. The language of a folder is declared in its manifest, and the words of titles, descriptions and headings are the words a reader would search with, in that language.
5. The sources are left as they were, and only the pack is committed; scratch files stay outside the repository.
6. The layout is approved before anything is converted; the pack is shown before it is committed unless the user said to go ahead; every push follows the repository's agreement and the user's word.
7. The check passes before the commit, and three questions are tried where the command or the connection is at hand.

## Terminology

| Term | Meaning |
|---|---|
| Document pack | A pack that is mostly documents: the format, the address and the tools of any pack, used for a body of documents. |
| Document set | A directory of Markdown under a document root, with a map; one set per subject or audience. |
| Map | The `README.md` of a document set: one line per document, what each holds. |
| Chapter | A part of a long document, one file, with the heading path it came from. |
| Section | The text under one heading, to the next heading: what a search names and an agent reads by its offset and limit. |
| Source | The file or export a document was converted from; named in the front-matter, never copied into the pack unless the user wants it there. |
| Inventory | The survey of the sources: formats, sizes, languages, structure, images, what stays out. |
| Layout plan | The pack before it is made: sets, files, splits, maps, manifests, what stays out. |
| Converter | What turns one format into Markdown on this machine, found at run time. |
