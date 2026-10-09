#!/usr/bin/env python3
"""Print the turns of a Claude Code transcript in order.

For each turn: the user's messages, the agent's text, each tool call with its name
and the parameters that matter, and the first line of each tool result. Reads one
session file from ~/.claude/projects/<slug>/<session id>.jsonl; needs nothing but
Python 3.

Usage:
  python transcript_digest.example.py <session.jsonl> [--full] [--from N] [--grep WORD]

  --full      print whole texts instead of their first 300 characters
  --from N    start at item N (the number printed in the first column)
  --grep WORD print only the items whose text contains WORD, case-insensitively

An example, not a dependency: the host's file format is its own and may change.
When a line does not parse as expected, read the file directly.
"""
import json
import sys


def shorten(text, full, limit=300):
    text = (text or "").replace("\n", " ")
    if full or len(text) <= limit:
        return text
    return text[:limit] + "..."


def blocks_of(record):
    message = record.get("message") or {}
    content = message.get("content")
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return content if isinstance(content, list) else []


def describe(kind, block, full):
    if kind == "text":
        return shorten(block.get("text"), full)
    if kind == "tool_use":
        params = block.get("input") or {}
        shown = ", ".join(f"{k}={str(v)[:80]!r}" for k, v in list(params.items())[:4])
        return f"call {block.get('name')}({shown})"
    if kind == "tool_result":
        content = block.get("content")
        if isinstance(content, list):
            content = " ".join(x.get("text", "") for x in content if isinstance(x, dict))
        lines = (content or "").strip().splitlines()
        first = lines[0] if lines else ""
        flag = " ERROR" if block.get("is_error") else ""
        return f"result{flag}: {shorten(first, full, 200)}"
    return None


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 1
    path = argv[0]
    full = "--full" in argv
    start = int(argv[argv.index("--from") + 1]) if "--from" in argv else 0
    word = argv[argv.index("--grep") + 1].lower() if "--grep" in argv else None
    # A Windows console may not take every character a transcript holds.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    n = 0
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            role = record.get("type")
            if role not in ("user", "assistant"):
                continue
            stamp = (record.get("timestamp") or "")[11:19]
            for block in blocks_of(record):
                text = describe(block.get("type"), block, full)
                if text is None:
                    continue
                n += 1
                if n < start:
                    continue
                if word and word not in text.lower():
                    continue
                print(f"{n:5d} {stamp} {role}: {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
