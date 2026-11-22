# Tool notes: what DART and its filings do

What the site and the filings do that the workflow does not say, by topic. A fact about the site carries the month it was seen; how a filing is written changes with the filer, not with time.

## Reading an income statement

- **The unit line decides the figure.** An audit report an auditor filed is usually in won; a listed company's statements are in thousands or millions of won (`천원`, `백만원`). The script prints the unit line whatever words are asked for: convert to won before anything is compared or written.
- **Revenue has several names.** `매출액`, `영업수익` (a platform or a service company), `수익(매출액)`, and under K-IFRS sometimes `수익`. Operating profit is `영업이익` or `영업이익(손실)`; a figure in parentheses is negative.
- **Titles and accounts may be spaced out.** An audit report writes `손 익 계 산 서` and `매 출 액`. The script compares without spaces; by hand, search for the first syllable.
- **The statements may be one section.** A smaller filer's business report has no section named for the income statement: `toc` with `손익계산서` prints nothing, so take the section `연결재무제표` or `재무제표` and filter its rows with the same word list. The section then holds every statement: read the rows under the income statement's own heading.
- **Two columns, two years.** The statement shows the fiscal year and the one before it. The prior year's figure is taken from the newer filing, which carries any restatement.
- **A fiscal year that does not end in December.** The overview names the closing month. The row's `fiscal_year` is the year the period ends in, and the table says the period where it is not the calendar year.

## Which figure is the company's

- **Separate and consolidated differ by the subsidiaries.** A business report carries both. Use the consolidated one for what the company is, and say `consolidated`; an announcement about "the company" may mean either, so compare with both before grading `differs`.
- **A provisional result is the company's own early figure.** It is filed on the exchange weeks before the audit and can change: the audited filing's figure is the row's.
- **No filing is a finding.** A company below the size that requires an external audit files nothing. Its announced figure stays `announced-only`, and the row says that DART has no filing, with the day it was looked for.

## The company's own site

The official site is, in this order: the homepage in the DART overview; the site a web search returns whose footer carries the filer's business registration number; the address the user gives. A filed homepage that does not open is not the end: a company often has a second official domain (a product site beside a corporate one), and the overview's address and registration number tell which search result is theirs. A site that cannot be found is said so; a logo or a figure is never taken from a namesake.

## The site

- The company lookup takes the Korean name, with or without `주식회사`, a part of it, or a stock code. An English name returns nothing, even the one the overview shows (checked 2026-11): look the brand up for its Korean legal name first.
- The filing search returns only the types asked for. An audit report its auditor filed is not among the business report types, nor the reverse: ask for `A001,F001,F002` together, as the script does by default, and read the filer column to tell who filed.
