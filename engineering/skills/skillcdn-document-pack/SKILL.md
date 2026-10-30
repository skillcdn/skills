---
name: skillcdn-document-pack
description: Turns documents a person has (PDF, Word, slides, spreadsheets, HTML, wiki and chat exports, plain text) into a pack of documents in the SkillCDN Format, in a repository they own, so that agents browse, search and read them through SkillCDN. Use when the user wants a body of documents made searchable and readable by agents, wants to add documents to a pack, or asks for a handbook, a manual or an archive as a pack. To work with a pack that exists, use skillcdn-document-research. Surveys the sources, plans the layout with the user, converts each document to Markdown with the tools the agent has, lays them out one file per document or chapter with a title and a description, keeps each original in sources/ beside its documents, writes the map of every set, keeps the figures with their words and transcribes the scans, points out what looks private with the repository's visibility for the user to decide, declares the roots and the language in the manifest, checks it with the indexer's own check and commits it.
license: MIT
compatibility: Needs a shell with git and Node.js in a checkout of the target repository, and whatever converts the user's formats on this machine, found at run time; a vision model of the agent for figures and scanned pages. Works in any agent that can read files, run a shell and look at an image.
metadata:
  author: skillcdn
  version: "1.2"
  tools: skillcdn
skillcdn:
  include:
    - references/layout.md
    - references/conversion.md
    - /engineering/docs/skillcdn/serving.md
  translations:
    ko:
      title: 문서를 SkillCDN 문서 팩으로 만들기
      description: 사용자가 가진 문서(PDF, 워드, 슬라이드, 스프레드시트, HTML, 위키와 채팅 내보내기, 텍스트)를 사용자의 저장소에 SkillCDN 포맷의 문서 팩으로 만들어, 에이전트가 SkillCDN을 통해 탐색하고 검색하고 읽게 합니다. 원본을 조사하고, 레이아웃을 사용자와 정하고, 에이전트가 가진 도구로 각 문서를 마크다운으로 바꾸고, 문서나 장 단위로 한 파일씩 제목과 설명을 붙여 배치하고, 원본 파일은 문서 옆 sources/에 두고 프런트매터에 적고, 문서 세트마다 지도를 쓰고, 그림은 에이전트가 읽을 글과 함께 두고 스캔된 쪽은 글자로 옮기고, 비밀이나 개인정보로 보이는 것은 저장소의 공개 여부와 함께 알려 사용자가 정하게 하고, 매니페스트에 문서 디렉터리와 언어를 선언하고, 인덱서의 검사를 통과시킨 뒤 커밋합니다. 문서 모음을 에이전트가 검색하고 읽을 수 있게 만들 때, 팩에 문서를 더할 때, 핸드북이나 매뉴얼이나 아카이브를 팩으로 만들 때 쓰세요. 이미 있는 팩으로 일할 때는 skillcdn-document-research를 쓰세요.
---
# Documents into a pack

What goes in: documents a person has, in whatever formats, and a repository they own or a folder of one. What comes out: those documents as a pack in the SkillCDN Format, one Markdown file per document or chapter with a title and a description, each original kept beside its documents in `sources/` and named in their front-matter, a map in every document set, the images kept with the words an agent reads them by and the scans transcribed as text, a manifest that declares the document roots and the language, a passing check, and a commit the user approved; then, once pushed, an agent that connects to the repository's address finds a section of any document by its words, reads it by its offset, and reaches the original behind it through the link a result gives. SkillCDN never receives a file: everything happens in the checkout, and the service indexes what is pushed; the originals and the pictures are listed and never searched. Who reads the pack is decided by the visibility of its repository, not by what is left out of the text: a pack made from private material goes whole into a private repository, and a public one holds nothing that is not for everyone. The format is SkillCDN's and is not restated here ([document packs](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/skill-repo.md#document-packs)); this skill carries the method, from the sources to the commit.

## How the user is involved

- **Questions:** three at most, asked in one message at the start and only when the request leaves them open: where the documents are, which repository or folder they go into, and what language they are written in when the sources do not say.
- **Checkpoints:** the layout plan, before anything is converted; the pack, after the check passes and before it is committed; the delivery. One short message each, in plain words; one word continues.
- **Go-ahead:** when the user says to go ahead alone, the pack is committed without being shown first. Every push follows the agreement of the repository, and the user's word where it has none.
- **Changes mid-run:** a change to the layout after conversion began is applied to what is not converted yet, and the converted files are moved or renamed to match; nothing is converted twice for a rename.

## Requirements

| What | Used for |
|---|---|
| A shell with git and Node.js in a checkout of the target repository; Node.js 24 or newer for the check, which asks for it (checked 2026-10) | The layout, the files, `npx @skillcdn/cli check`, the commit. |
| What converts each format on this machine, found at run time ([conversion.md](references/conversion.md) says how to look) | Turning each source into Markdown. A format nothing converts is reported, never guessed at. |
| The agent's own vision model | Describing a figure and reading a scanned page, written as text beside the image. |
| Optional: Git LFS (`git lfs version`) | An original over what the host takes as a file as it is (100 MB at GitHub, checked 2026-10; another host's limit from its documentation, found by searching the host's name with "file size limit"), kept in the pack as a pointer the host serves the file for. LFS storage and bandwidth are metered by the host (GitHub gives an account a free quota and sells more; the account's billing page, which the owner opens, says what is left; checked 2026-10), so the layout checkpoint names each such file's size against it, and nothing is tracked before the user's word. |
| Optional: the SkillCDN connection to the repository, or the `skillcdn` command on a directory | Trying the pack as an agent will meet it, before and after the push. |

Check these before the first message. Without a checkout, stop: say that the pack is written into a checkout of a repository the user owns, and offer to make one (`git init` in a new directory, or a clone of theirs). Without a converter for a format, convert what can be converted, list the files that could not, and say what would convert them. A private repository is served only by a deployment configured for signing in, to the people the git host shows the repository to, through the deployment's app installed on it: the page of the address says how to sign in and install it, a person's AI app connects with an access token the deployment issues to them once signed in, and an agent with nobody to sign in gets a repository token the owner makes ([permissions](https://github.com/skillcdn/skillcdn/blob/main/docs/specs/permissions.md)); the address and the mount route answer nobody without one. Say so in the first message for a private repository, so that the user knows how their agents will reach the pack.

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

1. Walk the sources. Count them by format; open one of each format and note what structure the converter will keep ([conversion.md](references/conversion.md), "What each format keeps"); leaf through a scanned source with the vision model, its first pages and its table of contents, enough to plan its chapters, the transcription itself waiting for phase 3; note a Word file with tracked changes or comments; and note which files are over what the host takes as a file as it is (100 MB at GitHub, checked 2026-10), which go through Git LFS.
2. Note what looks secret or personal (a credential, a person's data, a customer's material) and what the user may not mean (drafts, duplicates, older versions of a document that exists in a final form), beside the repository's visibility, read from the host's page of the repository (a private one carries the host's lock and label), from the host's own command where the shell has one (`gh repo view --json visibility` at GitHub), else from the user's word, which the checkpoint repeats. Who reads the pack is decided by that visibility and not by what is left out of the text: the layout checkpoint lists each item, and the user decides to keep it, to leave it out of the converted text (which leaves it in the original, which the pack still carries), or to make the repository private; where the repository is private already, the choice is between the first two, and an original that holds a live credential is named on its own, since whether it goes into `sources/` is the user's word too. Nothing is left out on the agent's own judgment.
3. Note the language of each source, and where one source mixes languages.

### Phase 2: Plan the layout

Produces the **layout plan** by [layout.md](references/layout.md): the document sets, the file for each document or chapter with its name and its title, where a long document is split, the maps, the manifests, and what stays out, shown at the layout checkpoint.

1. Group the sources into document sets by what they are about and who reads them, one folder each under the document roots, with a `README.md` as the set's map.
2. One file per document or chapter, never per page ([layout.md](references/layout.md), "One file per document or chapter"): a chapter long enough to carry a title and a summary, short enough to read by sections, a few thousand words at most, which is far under the limit a deployment indexes a file up to; that limit is the deployment's configuration, and the check in phase 5 names a file over it, which is then split.
3. A manifest at the root with the document roots and the language; a manifest of its own in a folder written in another language; the `license`, offered with the default layout.md "Manifests" gives (none for an organization's own documents in a private repository, a permissive one only where anyone may pass the text on); and, offered for a pack whose text should stay out of the deployment's embedding model or out of its search across packs, the `search` field that keeps it out, with the recommendation layout.md gives ([layout.md](references/layout.md), "Manifests").
4. The originals: each source file copied as it is into `sources/` of the document set its documents belong to ([layout.md](references/layout.md), "Document sets"), so that an agent reaches the figure, the table or the page a chapter was made from through the link a result gives; a file over what the host takes as it is goes through Git LFS, named at the checkpoint since it needs the tool and the user's word. The images that carry meaning go beside their documents in `images/`.

Checkpoint, in plain words: the sets and what each holds, how many files, which documents are split and where, the maps, the originals and where each goes (which through LFS, each with its size against the owner's quota), the language of each folder, the license with its default, whether the documents stay out of the search by meaning or of the search across packs, with the recommendation; a Word file with tracked changes or comments, with the default (the changes accepted, the comments dropped, since the final text is what the document says and comments are editors' words that may name people); then what looks secret or personal, with the repository's visibility and the choices (keep it, leave it out of the text, make the repository private where it is not), and what the user may not mean. "OK" converts.

### Phase 3: Convert

Produces the **converted files**, one per planned file, as Markdown.

1. Copy the originals first, each as it is into `sources/` of its set as the plan says ([conversion.md](references/conversion.md), "The originals"), so that every `source` of phase 4 names a file the check finds; a file over the host's limit is tracked before it is added (`git lfs install` once, then `git lfs track "<path>"`, which writes `.gitattributes`, committed with the pack), on the word the checkpoint took.
2. Convert each source with the converter found for its format, as [conversion.md](references/conversion.md) says for it: headings kept as headings, tables as tables, lists as lists, footnotes at the end of their section, the text of the body and nothing of the page furniture (headers, footers, page numbers).
3. Split where the plan says, at headings, and give each part the heading path it came from so that a chapter read alone still says where it belongs.
4. Images: keep every image that carries meaning beside the document, in `images/` of the set, linked from where it was with alternative text that says what it shows in one sentence and, for a figure that carries meaning, a caption paragraph under it ([conversion.md](references/conversion.md), "Figures and images"); the check reports a picture without any words. A decorative image is dropped. A scanned page is rendered to an image for the vision model and written as text; its page image is not kept beside the document, since the original in `sources/` is the image, and a figure on it is kept as any figure is.
5. Mark what the converter lost and the agent could not restore (a table too wide, an equation, a form) in a short note in the file that says where it is in the original, in words ("the diagram is on page 12 of the original"), since the hosts send an original as a download and a link into a page of it does nothing.

### Phase 4: Describe

Produces the **described pack**: every file with its front-matter, every set with its map, the manifests.

1. Front-matter on every file: `title`, the document's own title, or for a chapter the chapter's with the document's title before it where the chapter's alone would not say what it belongs to, quoted in YAML when it holds a colon followed by a space; `description`, one or two sentences of what the document holds and who reads it, in the words a reader would search with; `source`, the original the document was made from, as the path of its file in `sources/` written as a link destination is, relative to the document (`sources/<file>.pdf`), or a list of them for a document made from several ([layout.md](references/layout.md), "Front-matter"); a source that is no file of the pack (an export of a system, a conversation) is named in words, which stay text. A result then names the original with the document and says where its bytes are.
2. Headings that name the parts: where the source had none, add the headings the text supports and no more; a heading a search names should tell a reader what the section holds.
3. The map of each set: `README.md` with one line per document, as [layout.md](references/layout.md), "Maps" shows.
4. The manifests: `documents` listing the roots, `language` the language, `description` who the pack is for, `license` as the layout checkpoint settled it, and `search` where the user chose at the layout checkpoint to keep the documents out of the search by meaning or of the search across packs ([layout.md](references/layout.md), "Manifests").

### Phase 5: Check

Produces the **check report**.

1. `npx @skillcdn/cli check` in the checkout until it prints `ok: no index diagnostics`. From version 0.4.1 of the command it reports a picture without alternative text, a picture, an original or a link that names no file of the repository, and a `source` written like a path that names none (checked 2026-10): fix each in the file it names. Read the documents it lists with their section counts: a document with no sections has no headings and is read whole; a document named as too large to search is split. Read the instructions a client is told on connect: they quote the manifest's description and name the manifest as what to read for the pack's metadata. The section counts, the sections in a search result and the matching of Korean, Japanese and Chinese words by their parts need the command from version 0.4.0 on; an older command lists the documents without counts, names the document alone in a search, and finds such a word only in the form the text uses (checked 2026-10).
2. Where the repository has a check of its own (`node scripts/check.mjs` in a fork of the reference pack), run it too.
3. Where the `skillcdn` command is at hand, `skillcdn find <directory> <words>` for three questions the documents answer, in the pack's language, one of them in each language the pack has: each should name the document and the section that answers, and `skillcdn file <directory> <path> --offset <n> --limit <n>` with the numbers the result gave should read that section. With an older command, which names the document alone, find the section by the headings of the file. A question that finds nothing is a title, a description or a heading that does not say what the text says: fix the words. Where neither the command nor a connection is at hand, write the three questions into the delivery for the user to try once connected, and report the step as not run.

Checkpoint, skipped on a go-ahead: the tree of the pack, the counts, the check's last line, the three questions and what each found, or that they wait for a connection.

### Phase 6: Commit

Produces the **commit**.

1. Commit the pack's files, with `.gitattributes` where LFS tracks an original, and nothing else, as the repository's agreement says, naming any unrelated change left in the tree.
2. Push only as the repository's agreement allows, with the user's word: a push to the default branch is what SkillCDN serves ([serving.md](/engineering/docs/skillcdn/serving.md)). Once served and connected (a private repository through the sign-in and the token the Requirements describe), ask one of the three questions through `search_repo`; read the section it names with `read_repo_file` and the offset and limit it gave, and outline one document with `browse_repo`, whose first page should name the document's original with where its bytes are and its pictures with their words.
3. Deliver in one message: the address or the directory, how many documents and sections, what was left out, the files whose conversion lost something and where the source is, and what to do next (connect an agent; the skill skillcdn-document-research of this area, for working the pack).

### Adding to a pack

The same phases over the new sources alone: the inventory covers them, the plan fits them into the sets that exist or adds a set, the maps and the manifests change where they must, and nothing that was there is converted again or reformatted in passing.

## Hard rules

1. Nothing is invented. The pack holds what the sources say, as they say it; a figure's description says what is visible; what the converter lost is marked, never filled in.
2. The repository's visibility decides who reads the pack, and the pack is faithful to its sources: nothing is left out of the text for being personal or secret on the agent's own judgment. What looks secret or personal is pointed out at the layout checkpoint with the repository's visibility, and the user chooses to keep it, to leave it out of the text, or to make the repository private; a public repository holds nothing that is not for everyone, so a secret found in a source is never written into a public repository's text, and the choice there is between leaving it out of the text and making the repository private.
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
| Source, original | The file a document was converted from, kept as it is in `sources/` of its set and named in the front-matter as a path; an export with no file is named in words. Listed and never searched; reached through the link a result gives. |
| Visibility | Whether the git host shows the repository to everyone or to its people alone; what decides who reads the pack. |
| Inventory | The survey of the sources: formats, sizes, languages, structure, images, what stays out. |
| Layout plan | The pack before it is made: sets, files, splits, maps, manifests, what stays out. |
| Converter | What turns one format into Markdown on this machine, found at run time. |
