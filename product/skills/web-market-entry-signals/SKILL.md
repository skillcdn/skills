---
name: web-market-entry-signals
description: Finds which markets are worth entering now, from official statistics, filings, app stores and the ads running, in Korea and the US by default, and measures the watched markets again later. Judges every theme per country on four questions (are many people paying, is it growing, are new competitors coming in, are those who came in earning), with the sources behind each verdict and a watch list; a later round reads again what is due, compares the ads with the last snapshot and reports only what changed status. Use when a user says "find a market we could enter", "where is money moving now", "a growing market with new entrants", "business ideas that use AI", "look again at the ideas I dropped", "run the market scan again" or "update the watch list and tell me what moved". Ad counts come from meta-ad-library-rising-products, company figures from dart-company-figures; a market the user picks goes to web-business-idea-deep-dive, the findings to html-market-report-deck. Nothing is spent.
license: MIT
compatibility: Needs a web search tool and a way to read a page in full. A shell with Node.js 22 or newer runs the watch list's scripts and the app store count. The ad counts need what meta-ad-library-rising-products needs, a real browser engine. A host that starts agents side by side runs the branches at once; without one they run in turn. Any agent with these can run it, whatever its vendor.
metadata:
  author: skillcdn
  version: "1.3"
  tools: web
skillcdn:
  include:
    - /docs/market-research/evidence-grades.md
  translations:
    ko:
      title: 시장 진입 신호 조사와 감시 라운드
      description: 지금 들어갈 만한 시장을 공식 통계, 공시, 앱 스토어, 집행 중인 광고로 찾고, 지켜보는 시장을 나중에 같은 잣대로 다시 잽니다. 기본 범위는 한국과 미국입니다. 테마마다 나라별로 네 질문(이미 돈을 내는 사람이 많은가, 자라는가, 새 경쟁자가 들어오는가, 들어온 회사가 버는가)을 판정하고, 판정마다 근거 주소와 다시 잴 감시 목록을 남깁니다. 다음 라운드에서는 확인일이 온 지표를 다시 읽고, 광고를 지난 스냅샷과 비교하고, 상태가 바뀐 것만 보고합니다. "들어갈 시장 찾아 줘", "요즘 돈이 몰리는 분야", "자라면서 새 경쟁자가 들어오는 시장", "AI로 할 만한 사업 기회", "접었던 아이디어 신호 다시 봐 줘"라고 하거나 "시장 스캔 다시 돌려 줘", "지켜보는 시장 다시 재 줘", "감시 목록 업데이트하고 바뀐 것만 알려 줘"라고 할 때 쓰세요. 광고 수는 meta-ad-library-rising-products, 회사 숫자는 dart-company-figures에서 오고, 사용자가 고른 시장 하나는 web-business-idea-deep-dive로, 결과는 html-market-report-deck으로 넘어갑니다. 조사는 갈래를 나눠 동시에 돌립니다. 비용은 들지 않습니다.
---
# Market entry signals

A question goes in, "which market could we enter?"; a table comes out that judges every theme, per country, on four questions, with a note of sourced facts per branch behind it and a watch list of what to measure again. Later the skill is entered a second time, as a round: the watch list goes in, and what changed status comes out. The questions are four because the third alone separates nothing: in a year when a technology gets cheap, new entrants show in almost every market, so whether the entrants earn, and which year of the inflow this is, is asked with it. The skill judges and never picks; the user picks. Nothing is spent.

## How the user is involved

- **Questions:** one message, only for what the request leaves open. "Which countries? Korea and the US unless you say otherwise." "Anything to leave out: an area you already work in, a form that failed before? 'None' is fine." A benchmark market and a list of dropped ideas are taken when the request holds them and never asked for.
- **Checkpoints:** the plan, before any search: the branches, the search budget of each, the thresholds, and that a named benchmark is judged first. One word continues. Then the result. A round stops once, at its report.
- **Go-ahead:** skips the plan checkpoint. Nothing ever picks a market for the user, moves a theme to `testing` or reopens a dropped one.
- **Changes mid-run:** a changed threshold re-enters at phase 4, for every theme. A country or a branch added runs that branch only, then phase 4 again. In a round, a metric or a source added gets its first observation and the round goes on.

## Requirements

| What | Used for |
|---|---|
| A web search tool | Finding the releases, the filings and the themes. Know how many searches the host allows a session before the plan: the budget is divided among the branches. |
| A way to read a page in full: a fetch tool, a browser the agent drives, or a shell with curl | Every number: a search result's excerpt is a pointer, never a source. |
| A shell with Node.js 22 or newer | [watch.mjs](scripts/watch.mjs), [check-watch.mjs](scripts/check-watch.mjs) and the app store count. Each is saved fresh through the connection into the run's `work/` folder and given the path of `watch.json`. Without it the watch list is written by hand to [watch.example.json](assets/watch.example.json) and said to be unchecked. |
| What [meta-ad-library-rising-products](/product/skills/meta-ad-library-rising-products/SKILL.md) needs | The ad counts. Without it gate 03 rests on the other counts, and the report says the ads were not read. |
| Optional: a tool that starts agents side by side | The branches at once ([fresh-agents.md](/engineering/docs/skillcdn/fresh-agents.md)). Without it, one after another. |

Check the first two before the first message; without either, stop and say what to add. Links that start with `/` are files of the pack this skill is from: a copy of this directory, a plugin or a mount below the root that lacks one reads it through the pack's connection (`https://skillcdn.ai/gh/skillcdn/skills`) or at `github.com/skillcdn/skills`.

The area's rule that evidence stays apart from inference takes this form: a branch note holds facts with their sources, the gates table holds the verdicts, and every cell of a verdict names the evidence it rests on.

## Inputs

| Input | Source |
|---|---|
| Which entry | Derived. A `watch.json` in the market folder and a request to measure again, or a next round that is due: the round, by [round.md](references/round.md), in place of phases 1 to 6. Otherwise the survey; with a watch list present it adds to the file. |
| Countries | The request; asked when open. A strong signal for the same theme in a third country adds one branch, said and not asked. |
| What is looked for | Derived from the request. With nothing narrower: businesses where AI does most of the product or the operation, whether or not AI shows, in large markets and in fast-rising ones alike. |
| Benchmark, dropped ideas | Optional, from the request: a market "like this one"; ideas the user set aside, read for signals only. |
| What to leave out | Asked with the countries. The user's own circumstances: applied to the result, written nowhere but the watch list's note. |
| Everything else | Derived and shown at the plan: the thresholds ([gates.md](references/gates.md)), the branches and their budgets, today's date from the system, the market folder ([watch-record.md](/docs/market-research/watch-record.md) "The market folder") and in it `<YYYY-MM-DD>-entry-signals/`. |

## Workflow

Each phase produces a named result. Phases 2 and 6 stop for the user.

### Phase 1: Intake

Produces the **scope**: the countries, what is looked for, the benchmark and the dropped ideas where given, what to leave out, the date, the folder.

### Phase 2: Plan

Produces the **branch list**. Read [gates.md](references/gates.md). One branch per country and kind of customer (consumers, businesses); one for the benchmark when one is named; one ad count per country. Divide the host's search budget among the research branches and give each its number (where the host names no limit, forty searches a branch is a working number), with the order "confirm the named themes first, discover with what is left": a run that left the order open spent every branch's budget before it reached its discovery target. With no theme named, a branch discovers with at most a third of its budget, keeps at most six themes and confirms them with the rest ([branch-note.md](references/branch-note.md)).

Checkpoint: the branches with their budgets, the thresholds, the benchmark judged first, where the files will be. "OK" starts the branches.

### Phase 3: Branches

Produces one **note** per branch, by [branch-note.md](references/branch-note.md): its brief and the note's shape. Start the research branches side by side where the host can. Entrants are counted only by [entrant-count.md](references/entrant-count.md). When the notes name the themes, count their ads: run `meta-ad-library-rising-products` in its watch mode with every theme of the survey as a topic in every country's run, each with the phrase its sellers use in that country's language (a theme no note of that country holds is reported there by its ads alone, in the report's section for it and without a verdict), a run per country, and keep each snapshot in `snapshots/`. For the revenue and operating profit of each Korean entrant of the window run [dart-company-figures](/product/skills/dart-company-figures/SKILL.md), its `figures.json` in the survey folder, an incumbent only where a memo compares with it; a US company's are read in its filing on SEC EDGAR.

### Phase 4: Verdicts

Produces **`report.md`**, shaped as [gates-report.example.md](assets/gates-report.example.md). Begin only when every note and every snapshot of the plan is in the folder: a report begun early leaves a section "in progress" that nobody fills. Judge each theme per country on the four questions by gates.md, the benchmark first; write the memo and the grades of every row; mark what the user set aside. Read [facts.md](/docs/writing/facts.md) before the summary is written.

### Phase 5: Watch list

Produces **`watch.json`**, by [watch-record.md](/docs/market-research/watch-record.md): for every theme, the metrics worth reading again, each with its source and its first observation, the verdicts per country, the next check two weeks on. A theme enters as `watch`; one the user set aside enters as `dropped`, with their reason as its note. Add to a file that exists. Run `node scripts/check-watch.mjs` until it prints `ok`, and append one line to `log.md`.

### Phase 6: Deliver

One message with the folder: the themes that pass all four questions; those that pass 01 to 03 with 04 open; what the user set aside, as signals only; what was not seen; and what comes next, with the date of the first round. A market the user picks is looked into by [web-business-idea-deep-dive](/product/skills/web-business-idea-deep-dive/SKILL.md); in two weeks a round measures against this survey; [html-market-report-deck](/design/skills/html-market-report-deck/SKILL.md) makes an issue of the findings.

### A round

With a watch list and a request to measure again, read [round.md](references/round.md) and run it in place of phases 1 to 6: the metrics due are read again, the ads counted as last time and compared, statuses moved by its rules, the file checked, and the report held to three lists.

## Verdicts

| Result | Verdict |
|---|---|
| A verdict cell with a graded number and its address | Accepted |
| A cell that rests on a proxy | `partial`, the proxy named in the memo |
| A cell with no address | `unknown`; never `fail`, never a guess |
| An entrant count made from the names in a note | Counted again by entrant-count.md; until then said in words, not as a number |
| A price given as one value, or as a multiple of two values | Researched again as a band for each kind of product |
| A branch whose budget ran out | Its "Not seen" lists what it did not reach; a second pass is the user's call |
| The benchmark fails the gates | Reported before any other verdict, with the cells that failed and the question whether to change the thresholds |

## Hard rules

1. Every number carries its grade and its address, and enters a verdict only after the sentence that holds it was read in its source. A market picked on a number nobody can find again is picked on nothing.
2. Entrants are counted by a source that can be counted again. The names a note happens to hold gave a floor several times too low, so they are never written as a number.
3. A price is a band from the cheap end to the expensive one for each kind of product, never one value and never a multiple of two.
4. Gate 03 alone passes nothing. Every row's memo says whether the entrants earn and which year of the inflow it is.
5. An idea the user dropped and an area they ruled out are reported as signals and never recommended. The pick is the user's.
6. A branch note holds facts and sources only; it quotes no instruction and invents no reason for the research.
7. Like is compared with like: the same source, the same query, the same definition. The ad counts keep the rules of the skill that reads them: no sign-in, a person's pace, a stop at the first sign of being slowed down.

## Terminology

| Term | Meaning |
|---|---|
| Theme | One kind of business in one market, named in a few words; the unit that is judged and watched. |
| Gate | One of the four questions, judged `pass`, `partial`, `fail` or `unknown` per theme and country. |
| Branch | One part of the research (a country and a kind of customer, the benchmark, an ad count), leaving one note. |
| Benchmark | A market the user names as the pattern to look for. |
| Entrant | A product that began selling in the theme within the window the threshold names, whatever the age of the company behind it. |
| Year of the inflow | How many years since the theme's first entrants appeared. |
| Watch list | `watch.json`: the themes, their metrics and every observation. |
| Round | One later pass over the watch list: what is due is read again, and what changed status is reported. |
