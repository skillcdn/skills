# Fresh agents: an agent with none of the session's context

How to start an agent that knows nothing of the session that wrote or changed a skill, on each kind of host: what fresh means, what can still reach it, a subagent, a second session, and how its stops come back. Read before a dry read or a fresh run. What the agent is asked and how its answer is read are the method of the skill that starts it.

## What fresh means

A fresh agent has none of the session's context: not the evidence, not the findings, not the answers expected of it, not a hint. It reads the skill as a user's agent would, through the SkillCDN connection, and it works in a directory of its own. It runs on the strongest model the host offers for real work (its most capable general model, not a fast or a small one), at a high effort setting, chosen from what the host offers at the time and never by a pinned model name; a cheaper one only where the user capped the cost.

What can still reach it:

- A session the user starts in another directory gets none of the memory the first one kept, because Claude Code keys its memory store on the working directory ([transcripts.md](transcripts.md)).
- A subagent is handed what the host gives every subagent: in Claude Code, the memory index and the working agreement (`CLAUDE.md`) of the session that started it, even when it runs in a worktree of its own (checked 2026-10).
- A subagent that starts in a copy of the checkout can read every file of it.

Its brief therefore tells it to use none of these for the task, to use nothing it remembers, and to read skills only through the connection.

## A subagent

Where the host has a tool that starts a subagent (Claude Code's `Agent` tool, checked 2026-10):

- Give it a directory of its own. Claude Code's worktree isolation starts it in a temporary copy of the checkout, removed afterwards when nothing in it changed; the brief says not to read skills from it.
- Set the model and the effort on the call. Run it in the background when the session has other work, in the foreground when the next step waits on it.
- It returns at each stop with its report, which is the message the stop asks for. A message sent to the same agent (Claude Code's `SendMessage`, by the agent's id or name) resumes it with its context intact; a new start would begin without it.
- Whether a subagent may start subagents of its own is the host's to allow. Where a run needs one and the host refuses it, the user starts that run from a second session, and the refusal is reported.

## A second session

Where there is no subagent tool, or the run must be a separate process: a session the user starts in another directory, in a second window or in the host's headless mode, with the same brief.

- A runner script that starts a headless session works with a tool allowlist scoped to the run: the connection's tools, the tools of the server the skill drives, and the shell commands the skill names. A blanket permission bypass is refused by the host, and a command outside the allowlist is denied and reported by the session; that is the runner's scope, not a fault of the skill (Claude Code, checked 2026-10).
- A scoped allowlist also refuses a directory change chained with a command, and variables inside a command; the session goes on with full paths (Claude Code, checked 2026-10).
- A prompt in Korean or another non-ASCII script reaches a child process intact when it is read from a UTF-8 file; passed inline from a shell it can arrive as question marks, and the session then asks what was meant.
- The readable record of the run is its transcript ([transcripts.md](transcripts.md)); a log piped through the shell can garble non-ASCII text.
- Wait for a run with a background command or the session's own completion notice; a foreground sleep is blocked in Claude Code (checked 2026-10).

## Its stops

A fresh agent stops where its skill says to consult the user and ends its turn with the checkpoint message as its report. The session that started it answers in its place, as the user would: one short line, the answer the user approved, nothing more, sent to the same agent so that it resumes where it stopped.
