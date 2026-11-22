---
name: dart-company-figures
description: Finds a Korean company's revenue and operating profit in its filings on DART, the Financial Supervisory Service's disclosure site, and checks what the company announced against them. Use when a user says "find this company's operating profit", "can we use the revenue they announced", "is this website really that company", "compare these companies on audited numbers" or "they say they are profitable, are they". web-market-entry-signals, web-business-idea-deep-dive and html-market-report-deck call it for a company's numbers. Reads the audit report, separate or consolidated, the business report, or the parent's report where a subsidiary is folded in, on the public site at a person's pace or through OpenDART with the user's own key. Each company comes back as one line with the figures in won, their basis, the check of the announced figure, how the website and the filing were shown to be one company, and what the filings show besides, such as the audit opinion. Korean filers only. Nothing is spent.
license: MIT
compatibility: Needs a shell with Node.js 22 or newer and network access to dart.fss.or.kr, or a browser the agent drives or a web-reading tool that opens the site's pages. Works in any agent that has one of them; a search engine's summary of a filing is not a substitute.
metadata:
  author: skillcdn
  version: "1.2"
  tools: dart
skillcdn:
  include:
    - /docs/market-research/evidence-grades.md
  translations:
    ko:
      title: DART 공시로 회사 매출과 영업이익 찾고 발표 값 대조하기
      description: 한국 회사의 매출과 영업이익을 금융감독원 전자공시(DART)의 공시에서 찾고, 회사가 발표한 값을 그 공시와 대조합니다. "이 회사 영업이익 구체적으로 찾아 줘", "회사가 발표한 매출 써도 되는지 확인해 줘", "이 홈페이지 이 회사 맞아?", "이 회사들 감사 값으로 비교해 줘", "흑자라던데 진짜야?"라고 할 때 쓰세요. web-market-entry-signals, web-business-idea-deep-dive, html-market-report-deck이 회사 숫자가 필요할 때 이 스킬을 부릅니다. 감사보고서(별도 또는 연결), 사업보고서, 자회사가 합쳐져 있으면 지배회사의 사업보고서를 공개 사이트에서 사람의 속도로 읽거나, 사용자의 인증키가 있으면 OpenDART로 읽습니다. 회사마다 한 줄로 원 단위 값, 기준, 발표 값의 대조 결과, 홈페이지와 공시가 같은 회사임을 확인한 근거, 감사의견 같은 공시의 다른 관찰을 드립니다. 한국에 공시하는 회사만 다룹니다. 비용은 들지 않습니다.
---
# A Korean company's figures from its filings on DART

A company goes in, by its name, its website or its business registration number, or a list of them; one line per company comes out: revenue and operating profit as the filing states them, the basis they are on, how what the company announced compares with them, how the website and the filing were shown to be the same company, and what the filing shows besides. An announcement says "profitable" or a round figure; the audit report says an amount, on a stated basis, signed by an auditor, and the two do not always agree. So the amount is read where it was filed, and the announcement is graded against it. DART holds companies that file in Korea; a company that files in the United States is read from its own filing on SEC EDGAR, and this skill has no method for that.

## How the user is involved

- **Questions:** none, unless a name matches several companies: "Two companies carry this name: <A (representative, address)>, <B>. Which one?", asked once.
- **Checkpoints:** none before the result. The result shows every announced figure with its check beside it.
- **Go-ahead:** there is no stop to skip; the question about a shared name is still asked.
- **Changes mid-run:** another fiscal year or another basis re-enters at phase 3; another company is a new row from phase 1.

## Requirements

| Need | Any one of, in this order | When missing |
|---|---|---|
| Read DART | A shell with Node.js 22 or newer that reaches `dart.fss.or.kr`, which runs [dart.example.mjs](scripts/dart.example.mjs); else a browser the agent drives or a web-reading tool that opens the same pages, by the routes of [dart-web.md](references/dart-web.md) | Stop and say what to add. A press article or a search result is not a filing, and a figure read from one is graded `press`, never `filing`. |
| Write the result | A file tool | Put the table and the rows in the reply. |

Save the script as it is served into the working folder and run it there; it writes no file. Before the first message, prove the route on the first company: `node dart.example.mjs corp "<name>"` prints at least one line with a corp code. `NOT READ` is a stop: say what the script printed and offer the next route of the table. With `DART_API_KEY` set in the environment, a key of OpenDART the user holds, phase 3 takes its figures from the API where the company files a business report ([opendart.md](references/opendart.md)); the key is never asked for.

Links that start with `/` are files of the pack this skill is from: a copy of this directory, a plugin or a mount below the root that lacks one reads it through the pack's connection (`https://skillcdn.ai/gh/skillcdn/skills`) or at `github.com/skillcdn/skills`.

## Inputs

| Input | Source |
|---|---|
| The company, or several | The request: a name, a website or a business registration number. A calling skill passes its list; a company whose row of the same fiscal year another `figures.json` of the same market folder already holds is carried over from it, an observation saying so. |
| What the company announced | Optional: a figure or a phrase in the request, or the address of the release or the article. With it the announcement is checked; without it the row carries the filing's figures alone. A request that asks for the check and names no announcement: the company's own release of the year's results, found on the homepage or the IR homepage the overview filed (following its redirect), then by a web search for the year's results with the company's name; an article that quotes the company is the address only where no release is found, and the row says so. |
| More companies of the same kind | Only when the request asks for others beside the one named: candidates from a web search for the kind of company, each then looked up like any other and put in the same table. |
| Everything else | Derived: the fiscal year (the latest one an audited filing covers, with the year before beside it), the basis (consolidated where the company files one, else separate), the folder (the one the user or the calling skill named, else `company-figures-<YYYYMMDD>/` in the working directory). |

## Workflow

Each phase produces a named result. The commands are the script's; without a shell the same pages are opened by hand as [dart-web.md](references/dart-web.md) says, and [tool-notes.md](references/tool-notes.md) holds what the site and the filings do that nobody would guess. Read tool-notes.md before phase 3.

### Phase 1: Identify

Produces the **company**: its corp code and its overview. `corp "<name>"` lists the companies a name matches with corp code, market, representative, business registration number and industry; `info <corp code>` adds the address, the homepage the company filed, the founding day and the month its fiscal year ends. A website or a registration number in the request is matched against those fields. Several matches that the request does not settle: the question. No match for a brand or a site: read the operator's name and business registration number in the site's footer or terms ([identity.md](references/identity.md)) and look that name up, which settles phase 5 as well. Still no match: try a shorter part of the legal name and the stock code once each, then say that DART has no filer of that name and grade whatever the company announced `announced-only`.

### Phase 2: Find the filings

Produces the **documents**: `search <corp code> <from> <to>` over the fifteen months before today lists the filings by type.

| The company | The figures are in | Basis |
|---|---|---|
| Files a business report (listed, or unlisted with many shareholders) | The business report of the fiscal year: its consolidated statements, and its own beside them | `consolidated`, else `separate` |
| Is audited and files no business report | The audit report its auditor filed, and the consolidated audit report where there is one | `separate`, or `consolidated` |
| Has no filing of either kind | Nowhere on DART | `announced`, with the check `announced-only` |

A report filed again as a correction replaces the one it corrects. A provisional result (type `I002`) is read only to compare: where the confirmed filing differs from it, the row takes the confirmed figure and the difference is an observation.

### Phase 3: Read the figures

Produces the **figures**. `toc <rcpNo> "손익계산서"` names the income statement's section, and `sect … "매출,영업수익,영업이익"` prints its rows with the unit line; read that section and no more of the filing. Take revenue and operating profit for the fiscal year and the year before from the statement's two columns, as written, and convert by the unit line to won. A figure in parentheses is a loss and is written negative. A segment's figure comes from the segment note, with the basis `segment`. With the OpenDART key set and a business report filed, read opendart.md and take the two figures from the API; the sections of phases 4 to 6 are still read on the site.

### Phase 4: Check the announcement

Produces the **check**, one value of the company-figure vocabulary in the grades page that comes with this skill. Compare like with like: the same fiscal year, the same basis. An announced figure that rounds to the filed one `matches`. An adjective with no amount ("profitable", "record sales") is compared by its sign and its direction and is never copied: the row carries the filed amount. Where the announcement is consolidated and the company files only separate statements, read [consolidation.md](references/consolidation.md) before grading: it says when the parts add up (`sums-up`), when the filings only bound the figure (`scale-fits`) and when nothing can be said (`unverifiable`). A row with no announcement to compare, whose figures are the filing's own, carries `matches`. An announcement on both bases is checked on each: the row's basis in the row, the other basis with its check in an observation. A growth rate it states is checked against the statement's two columns and written as computed.

### Phase 5: Show it is the same company

Produces the **identity**: the one fact that ties the website, or the brand the user named, to the filer, by the order of [identity.md](references/identity.md), which is read before this phase whenever the request named a website or a brand and not the legal name. A row asked for by its legal name, with one match on DART, says that and no more. A name alone ties no website to a filer.

### Phase 6: Note what else the filing shows

Produces the **observations**, as plain facts from the sections already open and the auditor's opinion (`toc <rcpNo> "감사인"` names its section in either kind of filing): an audit opinion that is not unqualified, a doubt about the going concern, revenue that comes mostly from one customer or from related parties, the parent and its stake, a provisional figure the audit changed, a change of auditor between the two years, an operating profit far apart on the two bases (the gap computed; its cause is in the notes, read only when the user asks). An unqualified opinion is not an observation. Each is a sentence with its address.

### Phase 7: Deliver

`figures.json` in the folder, shaped like [figures.example.json](assets/figures.example.json), one row per company (a file already there gains the rows, and a row of the same company and fiscal year is replaced; amounts are whole won, `basis` and `check` take their fixed words, `listed` is `KOSPI`, `KOSDAQ`, `KONEX` or `no`), and a table in the user's language (a line per basis where one company was announced on both): company (founded, listed or not), revenue and operating profit of the year and the year before in units of 100 million won beside the won figure, the basis, the announced figure with its check, the identity, the observations, the filing's address. One message: the table, which rows a card or a text may show (`matches` and `sums-up`), which wait on the user (`announced-only`, `scale-fits`, `unverifiable`, `differs`) and why, and what could not be read.

## Verdicts

| Result | Accept | Accept with a change | Redo |
|---|---|---|---|
| A figure | The amount as the statement has it, with its unit, basis and the filing's address | Rounded to another unit: the won figure goes beside it | Taken from an article, a summary or a data service's table, even one that says it read the filings: find the filing, or grade it `press` and keep it out of the row |
| The announcement | `matches` or `sums-up` | `scale-fits`, `announced-only`, `unverifiable`: the check and its reason go to the user's list | `differs`: the row carries the filed figure, and the announced one is quoted beside it |
| The identity | The registration number agrees, or two filed facts agree with the site | One fact: said so in the row | The name alone: back to phase 5 |

## Hard rules

1. Profit is an amount. An adjective from an announcement is replaced by the filed figure or left out, never passed on: announcements have said "profitable" where the audit report showed an operating loss.
2. Every figure carries its basis and the address of its filing, and figures on different bases never stand in one column without the basis beside them.
3. Observations are stated as the filing states them and are never dropped; no sentence judges the company.
4. DART is read one page at a time, two seconds apart, and only the sections the figures are in. Collecting many companies' filings in bulk is outside this skill; OpenDART exists for that.
5. The OpenDART key is read from the environment. It is never asked for in chat, written to a file or printed.

## Terminology

| Term | Meaning |
|---|---|
| DART | The Financial Supervisory Service's public disclosure site, `dart.fss.or.kr`. OpenDART is its API, which needs a free key. |
| Corp code | DART's eight-digit number for a filer. `rcpNo` is the fourteen-digit number of one filing. |
| Business report | The annual report a listed company, or an unlisted one with many shareholders, files itself. |
| Audit report | The auditor's report with the statements attached, filed by the auditor for a company under external audit. |
| Basis | What a figure covers: `separate` (the company alone), `consolidated` (with its subsidiaries), `segment` (one line of business), `announced` (the company's word, no filing). |
| Check | How an announced figure stands against the filing, in the words of the grades page. |
| Observation | A fact the filing states beside the figures that a reader of the figures should know. |
