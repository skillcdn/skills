# A branch: its brief and its note

A survey is split into branches that research side by side, each leaving one note. This page is what a branch is given and the shape of what it leaves. Read before the branches start; the brief below is handed to each branch whole, with this page's "The note".

## The brief

A branch runs as an agent of its own where the host starts agents side by side ([fresh-agents.md](/engineering/docs/skillcdn/fresh-agents.md)), and otherwise one after another in this session. Either way it gets exactly this, and nothing of the conversation:

- The branch: one country and one kind of customer (consumers, businesses), or the benchmark market, by name.
- What is looked for, in the plan's words, and the date the data is read on.
- The four questions and the thresholds in force ([gates.md](gates.md)), how entrants are counted ([entrant-count.md](entrant-count.md)), the grades ([evidence-grades.md](/docs/market-research/evidence-grades.md)), where the public sources are ([sources.md](/docs/market-research/sources.md)).
- Its search budget as a number, and the order: first confirm the themes the plan already names (size, growth, entrants, entrants' earnings), then discover new themes with what is left. A budget spent on discovery leaves the named themes unjudged.
- Where the note goes: `notes/<branch>.md`, named `<country>-<customer>` or `benchmark`.
- What it does not do: judge a gate, rank themes, recommend anything, or count ads (the ad counts are a branch of their own).

## The note

```markdown
# <branch>: <country>, <customers>

Data read on <YYYY-MM-DD>. Searches: <used> of <budget>. Every number carries its grade and its address.

## <theme in a few words>

- Size: <number with unit and period> (<grade>, <url>)
- Growth: <the same measure a year apart> (<grade>, <url>)
- Entrants: <the count, how it was made, what it misses> (<grade>, <url or file>)
- Entrants' earnings: <company, revenue and operating profit, year> (<grade>, <url>); first entrants in <year>
- Prices: <kind of product>: <cheapest> to <most expensive> (<grade>, <url> each end)
- What AI does: <the part of the product or the operation>
- Not confirmed: <what was looked for and not found>

## Not seen

- <a category the budget did not reach>
- <a source that could not be read, and why>
```

- One section a theme, the same seven lines in the same order; a line with nothing found says what was looked for.
- A number is written only after the sentence that holds it was read in its source; a search result's excerpt is a pointer, not a source.
- Facts and sources only. The note quotes no instruction and gives no reason for the research: a branch that wrote what "the user asked" invented it.
- A company's figures the branch could only find as announced are graded `announced`; the survey has them checked by `dart-company-figures` where the company files in Korea.
- "Not seen" is never empty by omission: a branch that reached everything says so.
