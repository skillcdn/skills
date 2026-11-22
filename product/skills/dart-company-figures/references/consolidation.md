# When the announcement is consolidated and the filing is not

A company announces one figure for the whole group, its overseas subsidiary included, and files statements for itself alone. The two differ and neither is wrong. This page says how far the filings can confirm the announced figure, and which check each case gets.

## First, whose figure is it

Read the announcement for its scope: "including our overseas entity", "group revenue", a figure in another currency converted. Then look for the widest filing, in this order:

1. **The company's own consolidated statements**: a consolidated audit report (`F002`), or the consolidated statements in its business report. With one, compare directly: `matches` or `differs`.
2. **A parent that files a business report**: where the company is a subsidiary of a listed company, the parent's report holds a table of its subsidiaries' summary figures (assets, revenue, net income per subsidiary), in the notes to the consolidated statements under the subsidiaries (`종속기업`), with the list of subsidiaries near the end of the report. The company's own audit report names the parent and its stake in the first note.
3. **Neither**: the announced group figure has no filing behind it.

## Adding the parts up

With the parent's table:

1. Find the company and the other entity the announcement includes, each on its own row, for the same fiscal year.
2. Add their revenue. Compare the sum with the announced figure, in the same currency and unit; a difference inside the announcement's own rounding is none.
3. Open the related-party note (`특수관계자와의 거래`) of the company's audit report and read the sales between the two entities. With none, the sum is the group's revenue. With some, a sum would count them twice: subtract them where the note gives the amount, and say so.

| What the filings give | Check | The row carries |
|---|---|---|
| The parts add up to the announced revenue, and no sales run between them | `sums-up` | The announced figure with basis `consolidated`, and both filed parts in the observations with their addresses. |
| The parts are filed and the sum is near but not equal, or sales between them cannot be told | `scale-fits` | The company's own filed figure with basis `separate`; the announced one quoted beside it. |
| The table gives a subsidiary's net income and no operating profit, as most do | `scale-fits` for operating profit at most | The company's own operating profit, `separate`. A group operating profit is never built from net incomes. |
| No filing holds the other entity | `unverifiable` | The company's own filed figure; the announced one quoted beside it. |

Revenue and operating profit are graded each by itself: revenue that `sums-up` beside an operating profit that only `scale-fits` is the ordinary result, and the row says both.
