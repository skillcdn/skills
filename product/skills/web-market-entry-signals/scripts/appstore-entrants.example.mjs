#!/usr/bin/env node
// Counts the entrants of a theme by the year each app was first released, from the public App Store search
// (itunes.apple.com/search: no key, at most 200 apps a term). An example to adapt: the tests below decide
// what counts as an entrant, and they are the run's own. references/entrant-count.md says how to choose them.
//
// Usage: node appstore-entrants.example.mjs config.json
// config.json:
//   { "country": "us",
//     "terms": ["<search term>", "..."],          about twenty, the words a buyer types
//     "core": ["<word of the theme's business>"],  an app counts when its name or the start of its description holds one
//     "ai": ["AI", "GPT"],                         optional: with it, an app also needs an AI mark (see isAi)
//     "exclude": ["<word of another business>"],   an app whose name holds one is left out
//     "out": "entrants.csv" }
// Prints the count by release year and writes every kept app to the CSV, so that the count can be made again and read.
import { readFileSync, writeFileSync } from "node:fs";

const config = JSON.parse(readFileSync(process.argv[2] ?? "config.json", "utf8"));
const { country = "us", terms = [], core = [], ai = [], exclude = [], out = "entrants.csv" } = config;
if (!terms.length || !core.length) {
  console.error("config needs terms (what to search) and core (the words that make an app one of the theme's business)");
  process.exit(1);
}

const PAUSE_MS = 3500; // the search allows about twenty calls a minute
const HEAD = 300; // how much of a description counts as its start
const NEAR = 40; // an AI word and a core word this close in one sentence
const lower = (s) => String(s ?? "").toLowerCase();
const holds = (text, words) => words.some((w) => lower(text).includes(lower(w)));
// Where a word stands in a text. A short Latin word such as "AI" is matched as a word, so that "paint" or
// "mail" is not an AI mark; a longer word or one in another script is matched wherever it stands.
function positions(text, word) {
  const escaped = word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const re = /^[a-z0-9]{1,3}$/i.test(word) ? new RegExp(`(?<![a-z0-9])${escaped}(?![a-z0-9])`, "gi") : new RegExp(escaped, "gi");
  return [...String(text ?? "").matchAll(re)].map((m) => m.index);
}

function isCore(app) {
  return holds(app.trackName, core) || holds(String(app.description ?? "").slice(0, HEAD), core);
}
// The AI mark: an AI word in the name, or an AI word within NEAR characters of a core word in one sentence.
function isAi(app) {
  if (!ai.length) return true;
  if (ai.some((a) => positions(app.trackName, a).length)) return true;
  for (const sentence of String(app.description ?? "").split(/[.!?\n。]+/)) {
    const marks = ai.flatMap((a) => positions(sentence, a));
    const cores = core.flatMap((c) => positions(sentence, c));
    if (marks.some((m) => cores.some((c) => Math.abs(m - c) <= NEAR))) return true;
  }
  return false;
}

const apps = new Map();
let read = 0;
for (const [i, term] of terms.entries()) {
  if (i) await new Promise((r) => setTimeout(r, PAUSE_MS));
  const url = `https://itunes.apple.com/search?term=${encodeURIComponent(term)}&country=${country}&entity=software&limit=200`;
  const res = await fetch(url);
  if (!res.ok) {
    console.error(`"${term}": the search answered ${res.status}; stopped here, ${i} of ${terms.length} terms read`);
    break;
  }
  const { results = [] } = await res.json();
  read += 1;
  for (const app of results) if (!apps.has(app.trackId)) apps.set(app.trackId, { ...app, term });
  console.error(`"${term}": ${results.length} apps`);
}

const kept = [...apps.values()].filter((a) => isCore(a) && isAi(a) && !holds(a.trackName, exclude));
const byYear = new Map();
for (const a of kept) {
  const y = String(a.releaseDate ?? "").slice(0, 4) || "unknown";
  byYear.set(y, (byYear.get(y) ?? 0) + 1);
}

const csv = (v) => `"${String(v ?? "").replaceAll('"', '""')}"`;
const rows = kept
  .sort((a, b) => String(a.releaseDate).localeCompare(String(b.releaseDate)))
  .map((a) => [a.trackId, a.trackName, a.sellerName, String(a.releaseDate ?? "").slice(0, 10), a.trackViewUrl, a.term].map(csv).join(","));
writeFileSync(out, ["id,name,seller,first_release,url,found_by", ...rows].join("\n") + "\n");

console.log(`App Store, ${country}, read ${new Date().toISOString().slice(0, 10)}: ${read} of ${terms.length} terms, ${apps.size} apps found, ${kept.length} kept`);
console.log("first release  apps");
for (const y of [...byYear.keys()].sort()) console.log(`${y.padEnd(13)}  ${byYear.get(y)}`);
console.log(`Kept apps: ${out}. Limits: only apps in the store today; a web service or a messenger channel is not counted; a first release may be older than the app's present business.`);
