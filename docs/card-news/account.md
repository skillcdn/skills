# The account record

An account that posts card news day after day keeps three things beside the posts: its **policy** (what it covers and how it speaks, in the person's words), a **record of each post** (where it stands between an idea and the grid), and a **ledger** of what it has covered. The card-news skills read and write them where they exist, so that a run asks nothing the policy answers, proposes no story the account has told, and leaves each post where the next run finds it. A one-off post in a folder of its own has none of the three, and every skill runs as written without them.

## Where the record is

A working folder is an account's when it holds `docs/policy.md` or `topics/covered.md`. `git-studio-setup` sets one up as a repository a team shares, with the check that holds the three together; a plain folder with the same paths serves one person.

| Path | Holds |
|---|---|
| `docs/policy.md` | The policy. |
| `formats/<name>/format-spec.json` | The format the account builds in, a new folder for a new version. |
| `posts/<YYYY-MM-DD-slug>/` | One post: `post.json`, the topic brief with its `img/` and `credits.md`, the slide plan, the caption, the rendered slides, `review.md`. The brief folder and the post folder the skills name are this one folder. The day in the name is the day it is meant for. |
| `posts/published/<upload day>/<slug>/` | The same folder, moved once the post is live. |
| `topics/covered.md` | The ledger. |
| `topics/<YYYY-MM-DD>.md` | The candidate list of one search, with what was picked. |

## The policy

One page under headings, each line the person's standing answer. A skill takes a line as the answer to the question it would otherwise ask and as a rule for what it proposes; a value the page does not state is asked as the skill says, and where the person says the answer stands for the account, the skill writes it into the page in the same run. A word of the person's that changes a line changes the line, never a note beside it.

| Heading | Says | Read by |
|---|---|---|
| Account | The handle, the platform, what the account is for. | Every skill. |
| Readers | The market, the language and who reads: the brief's `audience`. | The research. |
| Lane | Which stories the account tells and which it leaves, in the person's own distinctions (only stories that make a reader laugh; product news and nothing else; no private individuals). | The research, for its candidates. |
| Follow-ups | Whether a later turn of a story already told is a new story. | The research, with the ledger. |
| Window | How many days back a story may be, and whether a coming season or date adds to a story's timeliness. | The research. |
| Ranking | The criteria a candidate is scored on, the points of each and the score from which one is recommended. Left out, the research ranks as it does for any request. | The research. |
| Sources | Where candidates are looked for first: outlets, official pages, the communities whose talk counts as heat. | The research. |
| Stance and tone | The brief's `stance` and `tone`. | The research and the build. |
| Voice | The register of headlines, body and caption where the format spec leaves room; words the account does not use. | The build. |
| Pictures | Whether a video goes before a photo, what a cover must show. | The research and the build. |
| Cadence | Posts a day, the slots, how far the minutes vary, what may replace a booked post on the day. | The batch and the posting. |
| Approval | Who approves a post and what they are shown. | The batch and the posting. |

## A post's record

`post.json` in the post's folder: `slug`, `title`, `format` (the folder under `formats/`), `kind` (news, promo, update), `status`, `owner`, `task` (the board task where the work has one), `created_at`, `slides`, `notes`, and what the later states add.

| `status` | Means | Written by |
|---|---|---|
| `idea` | The topic is picked and the ledger has its row. | The research, or the batch for the topics it was given. |
| `brief` | `topic-brief.json` and `img/` are complete. | The research. |
| `draft` | The slide plan and the caption are written and the slides rendered. | The build. |
| `review` | The build's review passed; the post waits for the person. | The build, and in a batch the orchestrator after the reviewer's pass. |
| `approved` | The person said it may be posted: `approved` holds `at` and `by`. | Whoever received the person's answer, never before it. |
| `scheduled` | It is booked on the platform: `scheduled_for` with the zone. | The posting. |
| `published` | It was seen live: `published` holds `at` and `url`; the folder moves under `posts/published/`. | The posting. |
| `archived` | It will not be posted. | On the person's word. |

A post changed after `review` (a slide remade, a caption edited) is rendered again and goes back to `review`.

## The ledger

`topics/covered.md` has one row per post from the moment its topic is picked, so a post that is booked or still being made counts as covered: the slug, the state and its day, what happened in one line, two to four **topic keys**, and the protagonist. A topic key is a specific name of the event (a person, an organization, a thing, an act), never a broad word such as the field the account covers.

A candidate overlaps a row when it is the same event, when it is a later turn of that event and the policy says follow-ups are not new stories, or when the same subject does the same thing somewhere else. A story that only works the same way as an earlier one (the same kind of mistake by another subject) does not overlap; two of them in one batch are placed apart.

A candidate the ledger or the lane rules out is not dropped silently: the candidate list shows the hottest of them first, each with the rule that caught it, and the person may tell the account to cover one, which the row then records in their words. The row is added by the skill that takes the pick, before the brief is written, and its state is rewritten by the skill that moves the post.

## Who reads and writes what

| Skill | Reads | Writes |
|---|---|---|
| [`web-card-news-topic-brief`](/product/skills/web-card-news-topic-brief/SKILL.md) | The policy, the ledger, the last candidate lists. | The candidate list, the ledger row, the post folder to `brief`. |
| [`html-card-news-from-brief`](/design/skills/html-card-news-from-brief/SKILL.md) | The policy's voice and pictures, the format, `post.json`. | The post to `draft` and `review`. |
| `html-card-news-batch` | All of it. | Several posts to `review` at once, each by the two skills above. |
| `instagram-post-scheduling` | The approved posts, the cadence. | `scheduled`, `published`, the move under `posts/published/`, the ledger's state. |
