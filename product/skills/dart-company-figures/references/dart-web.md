# DART on the web: the routes

How the public site `https://dart.fss.or.kr` is read without an account: the five pages a run opens, what each takes and what it gives. [dart.example.mjs](../scripts/dart.example.mjs) opens them from a shell; a driven browser or a web-reading tool opens the same addresses. Every route here answered on the live site in 2026-11. The site has no changelog: when a route stops answering, find it again as the last section says, and tell the user what changed.

## The session and the pace

Open the search page `/dsab007/main.do` first: it sets a session cookie. Send that cookie and a `Referer` of the site with every later request, as a browser does (the document viewer also answered without either, checked 2026-11; the form routes are the site's own background calls and are sent as the page sends them, as a form post). One page at a time, two seconds apart. A run for one company opens five to eight pages.

## A company by name

`POST /corp/searchCorpL.ax` with the form field `textCrpNm` (the name, a part of it, or a stock code) returns a table of matches. Each row holds the corp code in a hidden field named `hiddenCikCD…`, the name, a market tag (`유가증권시장` is KOSPI; `기타법인` is a company that is not listed), the stock code, the representative and the industry; the row's tooltip adds the English name and the business registration number. `POST /corp/searchExistAll.ax` with the same field answers the corp code alone when the name is exact and `null` otherwise.

In a browser: the search page's company field opens the same list.

## The overview of a company

`POST /dsae001/selectPopup.ax` with `selectKey=<corp code>` returns the company's overview: legal name, English name, stock code, representative, market, corporate and business registration numbers, address, homepage, industry, founding day, the month the fiscal year ends. The homepage is what the company filed; it can be a holding site, a recruiting site or blank.

## Filings in a period

`POST /dsab007/detailSearch.ax` with `textCrpCik=<corp code>`, `startDate` and `endDate` as `YYYYMMDD`, `finalReport=recent`, `sort=date`, `series=desc`, `currentPage=1`, `maxResults=100`, and one `publicType` field per type wanted:

| `publicType` | Filing |
|---|---|
| `A001` | Business report (annual). `A002` half-year, `A003` quarterly. |
| `F001` | Audit report. `F002` consolidated audit report. |
| `I002` | Fair disclosure on the exchange, where a provisional result is announced. |

Each result row gives the day filed, the report's name with its period (`사업보고서 (2025.12)`), the filer (the company for a business report, the audit firm for an audit report) and the filing's fourteen-digit `rcpNo` in the link `/dsaf001/main.do?rcpNo=…`. A remark tag says when a report includes consolidated statements. A corrected report carries `[기재정정]` before its name.

## A filing's table of contents

`GET /dsaf001/main.do?rcpNo=<rcpNo>` is the viewer. Its page builds the table of contents in a script: each entry sets `text` (the title), `dcmNo`, `eleId`, `offset`, `length` and `dtd`. Those five values address one section. A filing with attachments lists them in a selector, each with its `dcmNo`; an attachment is opened as `/dsaf001/main.do?rcpNo=…&dcmNo=…` and has a table of contents of its own (the script's `toc <rcpNo> --doc <dcmNo>`). A business report attaches its auditor's reports (`감사보고서`, `연결감사보고서`) this way.

| Filing | Where the income statement is |
|---|---|
| Business report | `III. 재무에 관한 사항`: `연결 손익계산서` under `2. 연결재무제표` and `손익계산서` under `4. 재무제표`, each a section of its own in a large filer's report and all inside the one section `연결재무제표` or `재무제표` in a smaller one's; the notes on segments (`부문별 보고`) and related parties (`특수관계자와의 거래`) follow. The audit opinions are summarized in `V. 회계감사인의 감사의견 등`. |
| Audit report | `(첨부)재무제표`: `손익계산서`, then `주석`. The auditor's opinion is `독립된 감사인의 감사보고서`. |

## One section

`GET /report/viewer.do?rcpNo=…&dcmNo=…&eleId=…&offset=…&length=…&dtd=…` returns that section as HTML: the statement as a table whose first lines give the periods and the unit (`(단위 : 원)`, `천원`, `백만원`), then one row per account with a column per period. Read the section, not the whole filing: an income statement is some tens of rows, a business report several megabytes.

In a browser: the viewer shows the same section when its title is clicked in the left pane; the section is an inner frame whose address is this route.

## Finding a route again

Open the search page in a visible browser with the network panel open, do the step by hand (type a company, press search, click a title), and read the request the page sent: its path and its form fields are the route. The script's regular expressions hold on to the field names above (`hiddenCikCD`, `rcpNo=`, `dcmNo`, `eleId`, `offset`, `length`, `dtd`); when one stops matching, compare with the page's source.
