# Evidence grades: the tags on a number and a verdict

The four small vocabularies the market research skills tag with, so that a note, a gates table, a watch list, a figures file and a magazine's ledger say the same thing with the same word. A tag stands beside its number with the address of the source: `1,240 (official, <url>)`. What a text may state from a source is in [facts.md](/docs/writing/facts.md); this page holds only the tags.

## The grade of a number

| Grade | The number is |
|---|---|
| `official` | A government's or a public body's statistic, read in its release or its table. |
| `filing` | In a filing a regulator publishes: an audit report, an annual report. |
| `announced` | What the company itself said: a press release, its site, an interview. |
| `estimate` | A research firm's, an analyst's or an analytics vendor's estimate. |
| `press` | Reported by an outlet with no document behind it that the run could read. |
| `measured` | Counted by the run itself on a named day: ads in a library, apps in a store, prices on pages. |
| `computed` | Worked out from other tagged numbers, with the formula beside it. |

## The check of a number against its source

| Check | Meaning |
|---|---|
| `confirmed` | The source was opened again and the sentence holds the number, for the same period and scope. |
| `differs` | The source says another number, period or scope; the text takes the source's, or drops the number. |
| `no-source` | No source could be opened. The number is not used in a verdict and not shown. |

## The check of a company's announced figure against its filing

| Check | Meaning |
|---|---|
| `matches` | The filing states the same figure on the same basis. A figure taken from the filing itself, with no announcement to check, is `matches` too. |
| `sums-up` | The announced figure is the sum of filed figures (a parent and a subsidiary), with no sales between them. |
| `scale-fits` | The filings bound it without stating it: the same order of size, no exact figure. |
| `differs` | The filing states another figure on the same basis. |
| `announced-only` | The company has no filing that carries the figure. |
| `unverifiable` | A filing exists and could not be read, or its basis cannot be told. |

## The verdict of a gate

| Verdict | Meaning |
|---|---|
| `pass` | The evidence meets the threshold, from a source of the kind the gate asks for. |
| `partial` | Met only through a proxy (customers in place of spend, an adjacent market), or for part of the theme. |
| `fail` | The evidence was read and does not meet it. |
| `unknown` | No evidence with an address was found. Never read as `fail`. |
