---
name: web-business-idea-deep-dive
description: Reviews one business idea in depth before anything is built, as one document with what exactly is sold to whom and who pays, how big the market is and when in the year it buys, who already sells it (the company behind each, its revenue, ads, price bands and when it came in), where the material the product needs can come from, the legal risks with a design that avoids each, a verdict on the idea as given and on a changed form, a pilot plan and the questions for a lawyer. Use when a user says "look into this idea properly", "research the law, the supply, the market and the competitors for this", "can we do this business", or picks one market from web-market-entry-signals, which finds the markets worth entering. Company figures come from dart-company-figures, competitors' ads from meta-ad-library-creative-research. Reads public sources in parallel branches. Research, not legal advice. Nothing is spent.
license: MIT
compatibility: Needs a web search tool and a way to read a page in full (a fetch tool, a driven browser, or a shell with curl). Optional, a tool that starts agents side by side for the branches, and what the two skills it calls need (a browser for the ad library, the DART website). Any agent with the first two can run it.
metadata:
  author: skillcdn
  version: "1.2"
  tools: web
skillcdn:
  include:
    - /docs/market-research/evidence-grades.md
  translations:
    ko:
      title: 사업 아이템 하나의 심층 검토
      description: 만들기 전에 사업 아이템 하나를 깊게 검토해 문서 한 편으로 냅니다. 무엇을 누구에게 팔고 누가 돈을 내는지, 시장이 얼마나 크고 한 해 가운데 언제 사는지, 이미 파는 곳은 어디인지(운영사, 매출, 광고, 가격대, 진입 시점), 상품에 드는 자료를 어디서 구할 수 있는지, 법 위험과 각각을 피하는 설계, 원래 형태와 고친 형태의 판정, 시범 계획, 변호사에게 물을 질문을 담습니다. "이 아이템 제대로 조사해 줘", "법, 재료 확보, 시장, 경쟁자까지 종합적으로 봐 줘", "이 사업 해도 되는지 봐 줘"라고 하거나 web-market-entry-signals의 결과에서 시장 하나를 골랐을 때 쓰세요. 들어갈 시장을 찾는 일은 web-market-entry-signals입니다. 회사 숫자는 dart-company-figures, 경쟁사 광고는 meta-ad-library-creative-research가 맡습니다. 공개 자료를 갈래별로 나눠 읽습니다. 법 부분은 조사이며 법률 자문이 아닙니다. 비용은 들지 않습니다.
---
# One business idea, reviewed in depth

An idea in one line goes in (what is sold, to whom, at about what price), in the user's words or as a row of a gates table. A review document comes out: the idea's structure, the market's size and its calendar, the competitors with the company behind each, the routes to the material the product is made from, the legal risks with a design that avoids each, a verdict, a pilot plan and the questions for a lawyer. The research runs as four branches that read public sources and write notes of facts; the review is written from the notes. The idea is judged twice, as given and in a changed form, because an idea that is stopped as given often works with a narrower scope, another source of material or another way of selling. The legal part is research for a lawyer to check, and says so.

## How the user is involved

- **Questions:** one, only when the request leaves it open: "What is the idea in one line: what is sold, to whom, and at about what price?"
- **Checkpoints:** the idea as given with the research plan, before any search; the review, in plain words, with what the user decides.
- **Go-ahead:** the first checkpoint is stated and not waited on. The review still lists what the user decides.
- **Changes mid-run:** a changed idea line re-enters at phase 2, for every branch. A changed country redoes the law branch from the start and reads prices and sizes again in that market.

## Requirements

| What | Used for |
|---|---|
| A web search tool | Every branch. Recognize it by its action: a query in, titles and links out. |
| A way to read a page in full: a fetch tool, a browser the agent drives, or a shell with curl | The statute, the terms of service, the statistics table, the price page: a figure counts only when its sentence was read on its page. [reading-pages.md](/docs/browser/reading-pages.md) says which tool reads what; a site the host cannot reach is met by [walls.md](/docs/browser/walls.md). |
| A file tool | The notes and the review. Without one, the review goes in the reply and the notes are summarized under it. |
| Optional: a tool that starts agents side by side | The four branches at once, as [fresh-agents.md](/engineering/docs/skillcdn/fresh-agents.md) "A subagent" says. Without it, one branch after another. |

Check the first two before the first message; without either, stop and say what to add. The two skills this one calls check their own tools when they run.

Links that start with `/` are files of the pack this skill is from: a copy of this directory, a plugin or a mount below the root that lacks one reads it through the pack's connection (`https://skillcdn.ai/gh/skillcdn/skills`) or at `github.com/skillcdn/skills`.

The area's rules take this form here: what was observed stands in the notes and the sections with its grade and its address, the verdict is the inference and names the sections it rests on, and the sizing's assumptions and everything not verified are listed in the review.

## Inputs

| Input | Source |
|---|---|
| The idea | The request, or the row the user picked from the gates table (`report.md`) of [web-market-entry-signals](/product/skills/web-market-entry-signals/SKILL.md): its theme, country and source addresses start the notes. A table with no pick: ask which row. No idea and no table: the question above. |
| Country | The request or the picked row; else the country the request's language points to. Stated at the first checkpoint, because the law is that country's. |
| What the user rules out | Optional, the user's own: a business they already run, a form that failed them before. It narrows the changed form and is written nowhere but as "ruled out by the user". |
| Everything else | Derived and shown at the first checkpoint: who pays when it is not who uses, the material the product is made from, the branches and their search budgets, today's date from the system, and the idea's folder: `<YYYY-MM-DD>-<idea>/`, the idea in a few hyphenated words, inside the market folder of [watch-record.md](/docs/market-research/watch-record.md) (`market/` under the working folder, or the unit's folder in a studio). |

## Workflow

Each phase produces a named result in the idea's folder. The reference a phase names is read before it.

### Phase 1: Intake

Produces **the idea as given**: one line (what is sold, to whom, at what price), who pays, the kinds of material the product is made from (documents, data, images, people's work), the country and the date. Split the host's search allowance between the branches, or, where the host states none, set fifteen a branch and twenty for the law, and say each branch's share before any search.

Checkpoint: the line, who pays, the material, the country, the four branches with their budgets, and "OK, or change the line".

### Phase 2: Branches

Produces **four notes**, `notes/<branch>.md`, by [branch-note.md](references/branch-note.md): the brief each branch agent gets, the note's head, its grades, its sources and its list of what was not seen. One agent a branch where the host starts them side by side; else the session works the branches in turn, by the same pages. Each branch confirms what the idea line claims first and spends what is left of its budget on discovery.

| Branch | Finds | By |
|---|---|---|
| `competition` | Who sells the same result to the same payer, the company behind each, its price bands, when it came in | [competitors.md](references/competitors.md) |
| `market` | How many could buy, what they spend today, when in the year they buy | [sizing.md](references/sizing.md), with the sources of [sources.md](/docs/market-research/sources.md) |
| `supply` | Every route to the material, what each yields, costs and risks | [supply.md](references/supply.md) |
| `law` | The laws the idea meets, by article or case, and a design that avoids each risk | [legal-table.md](references/legal-table.md) |

### Phase 3: Sections

Produces the review's four **sections**, each from its note and checked against "Verdicts" before the next.

1. **Competition.** For each Korean operator run [dart-company-figures](/product/skills/dart-company-figures/SKILL.md), its `figures.json` in the idea's folder, and take its `figures.json` rows whose `check` is `matches` or `sums-up` into the table; `announced-only` is shown as announced and listed for the user to confirm. An operator of another country is read from its own filing where it is listed. A competitor whose ads are how it sells is read with [meta-ad-library-creative-research](/marketing/skills/meta-ad-library-creative-research/SKILL.md), one run for all of them as [competitors.md](references/competitors.md) "Ads" says, at that skill's own stops (a go-ahead given here covers its shortlist), for how many ads each runs and since when. Two tables, consumers and businesses, and the closest competitor in depth.
2. **Market.** The assumptions table, three sizes kept apart, the calendar. Figures are written by [facts.md](/docs/writing/facts.md).
3. **Supply.** The routes table and the combination that reaches what a pilot needs. A route's legal standing is the law note's finding, by the row it points at; a route the law note did not cover goes back to the law branch first.
4. **Law.** The head that says it is research, the risk table, the design principles, the questions for a lawyer.

### Phase 4: Verdict

Produces **`review.md`**, in the user's language and the shape of [review.example.md](assets/review.example.md): the four sections, then

- **The idea as given:** holds, or is stopped, reason by reason (a crowded field, a risk no design avoids, material that cannot be had), each naming its section.
- **A changed form:** what changes in scope, in where the material comes from and in how it is sold, judged by the same four sections; or "none", with why. A form the risk table or the routes table stops is not proposed.
- **Where to win and what to avoid**, from the competitors' observed gaps.
- **A pilot:** who, when (from the calendar), where, and success criteria that can be measured (the cost to win a buyer at or under the first payment, repeat purchase, the rate of error reports), with a schedule. A target the research cannot set is a marked blank and one of the things the user decides.
- **For the user to decide**, then the sources and what was not verified.

Checkpoint: both verdicts in a sentence each, the three findings that weigh most, what the user decides, what was not verified, and where the file is. Phase 5 waits for the user's word.

### Phase 5: Deliver

The idea's folder holds `review.md` and `notes/`. Where the market folder has a `watch.json`, change that theme's line, or add one with the status `watch`, as watch-record.md "The file" defines it: `name` (the changed form, unless the theme holds another country's gates: then the name stays and the changed form opens `note`), `ai_role`, `doc` (the review's path), `note` (one plain line), and a metric with its first observation for each figure worth measuring again. No status is moved and no id renamed; `log.md` gets one dated line. Say in one message what was made and that the review is internal: which of its numbers may appear in anything published is the user's to say.

## Verdicts

| Result | Accepted | Accepted with a change | Redone |
|---|---|---|---|
| A competitor | Its operator, with the page that names it | Operator not found: "operator unconfirmed" | A list of app or site names: fill operator, price band and entry date |
| The market's size | Base and spend from official statistics, every assumption a row | Spend is an estimate: its grade and a range | A share with no source multiplied in: find its source or take it out |
| A legal risk | The article or the case, at its source's address | Commentary only: marked as commentary and turned into a question | "It is fine" with no basis: deleted |
| The verdict | Two forms, each sentence naming its section | No changed form: "none", with why | Stronger than its sections: lowered |

## Hard rules

1. The law section begins by saying it is research and not legal advice. A statute or a case is cited by its source's address, commentary is marked as commentary, and what is unsure or disputed becomes a question for a lawyer, never a conclusion.
2. Every figure carries its grade and its address, and is used only when its sentence was read on its page.
3. A price is a band from the cheapest to the dearest of a kind of product. One value, or a ratio of two single values, is not a finding.
4. A competitor is described by what was observed: its prices, its scope, when it came in, the evidence of a gap. No sentence passes judgment on a company.
5. The verdict comes in two forms, as given and changed, and says nothing its sections do not carry.

## Terminology

| Term | Meaning |
|---|---|
| Idea as given | The user's idea in one line, before any change. |
| Changed form | The idea with its scope, its material's source or its way of selling changed so that what stopped it no longer does. |
| Branch, note | One of the four lines of research, and the file of facts and sources it writes. |
| Operator | The company behind a service, as its terms or its business details name it. |
| Material | What the product is made from: documents, data, images, people's work. |
| Route | One way to obtain the material. |
| Band | A price range for one kind of product, low to high. |
| Base | The number of people or organizations that could buy. |
| Calendar | When in the year demand gathers. |
