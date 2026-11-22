#!/usr/bin/env node
// Checks a watch list (watch.json, schema market-watch/1) before a survey or a round is delivered.
// Usage: node check-watch.mjs [path/to/watch.json]      (default: ./watch.json, then ./market/watch.json)
// Exit 0 and one "ok" line when the file holds; exit 1 with one line per finding otherwise.
import { existsSync, readFileSync } from "node:fs";

const file = process.argv[2] ?? (existsSync("watch.json") ? "watch.json" : "market/watch.json");
const findings = [];
const fail = (where, what) => findings.push(`${where}: ${what}`);

const ID = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const DAY = /^\d{4}-\d{2}-\d{2}$/;
const PERIOD = /^\d{4}(-(Q[1-4]|\d{2}|\d{2}-\d{2}|W\d{2}))?$/;
const URL_RE = /^https?:\/\/\S+$/;
const CADENCES = ["weekly", "monthly", "quarterly", "yearly", "irregular"];
const KINDS = ["big", "rising"];
const STATUSES = ["watch", "candidate", "testing", "cooling", "dropped"];
const VERDICTS = ["pass", "partial", "fail", "unknown"];
const GATES = ["01", "02", "03", "04"];
const GRADES = ["official", "filing", "announced", "estimate", "press", "measured", "computed"];
const UNREAD = ["not published", "not reached"];

// A note or a memo is one plain line: at most 200 characters, no line break, no Markdown.
function plainLine(where, text) {
  if (text === undefined || text === "") return;
  if (typeof text !== "string") return fail(where, "must be text");
  if (/[\r\n]/.test(text)) fail(where, "holds a line break: one line only, the course of events goes to log.md");
  if ([...text].length > 200) fail(where, `is ${[...text].length} characters: at most 200`);
  if (/(\*\*|__|`|\]\(|^#{1,6} |^[-*] |\|)/.test(text)) fail(where, "holds Markdown: plain text only");
}

function day(where, value, required = true) {
  if (value === undefined || value === null) return required ? fail(where, "is missing") : undefined;
  if (!DAY.test(value) || Number.isNaN(Date.parse(value))) fail(where, `is not a day (YYYY-MM-DD): ${value}`);
}

function unique(list, where) {
  const seen = new Set();
  for (const [i, item] of list.entries()) {
    const at = `${where}[${i}]`;
    if (typeof item.id !== "string" || !ID.test(item.id)) fail(at, `id must be lower-case words joined by hyphens: ${item.id}`);
    else if (seen.has(item.id)) fail(at, `id is used twice: ${item.id}`);
    seen.add(item.id);
  }
  return seen;
}

let watch;
try {
  watch = JSON.parse(readFileSync(file, "utf8"));
} catch (e) {
  console.error(`${file}: cannot be read as JSON: ${e.message}`);
  process.exit(1);
}

if (watch.schema !== "market-watch/1") fail("schema", `must be "market-watch/1": ${watch.schema}`);
day("updated", watch.updated);
for (const key of ["sources", "themes", "metrics"]) if (!Array.isArray(watch[key])) fail(key, "must be a list");
const sources = Array.isArray(watch.sources) ? watch.sources : [];
const themes = Array.isArray(watch.themes) ? watch.themes : [];
const metrics = Array.isArray(watch.metrics) ? watch.metrics : [];
if (watch.thresholds !== undefined) for (const g of GATES) plainLine(`thresholds.${g}`, watch.thresholds?.[g]);

const sourceIds = unique(sources, "sources");
for (const [i, s] of sources.entries()) {
  const at = `sources[${i}] ${s.id ?? ""}`;
  if (!s.name) fail(at, "name is missing");
  if (!URL_RE.test(s.url ?? "")) fail(at, `url is not an address: ${s.url}`);
  if (!CADENCES.includes(s.cadence)) fail(at, `cadence must be one of ${CADENCES.join(", ")}: ${s.cadence}`);
  plainLine(`${at} how`, s.how);
}

const themeIds = unique(themes, "themes");
for (const [i, t] of themes.entries()) {
  const at = `themes[${i}] ${t.id ?? ""}`;
  if (!t.name) fail(at, "name is missing");
  if (!KINDS.includes(t.kind)) fail(at, `kind must be one of ${KINDS.join(", ")}: ${t.kind}`);
  if (!STATUSES.includes(t.status)) fail(at, `status must be one of ${STATUSES.join(", ")}: ${t.status}`);
  day(`${at} added`, t.added);
  day(`${at} next_check`, t.next_check);
  plainLine(`${at} note`, t.note);
  plainLine(`${at} ai_role`, t.ai_role);
  if (t.status === "dropped" && !t.note) fail(at, "a dropped theme says why in its note");
  for (const [country, g] of Object.entries(t.gates ?? {})) {
    const gat = `${at} gates.${country}`;
    if (!/^[a-z]{2}$/.test(country)) fail(gat, "country is a two-letter code in lower case");
    for (const q of GATES) if (!VERDICTS.includes(g[q])) fail(gat, `question ${q} must be one of ${VERDICTS.join(", ")}: ${g[q]}`);
    if (!g.memo) fail(gat, "memo is missing: do entrants earn, and which year of the inflow");
    plainLine(`${gat} memo`, g.memo);
    day(`${gat} judged`, g.judged);
  }
}

unique(metrics, "metrics");
let observations = 0;
for (const [i, m] of metrics.entries()) {
  const at = `metrics[${i}] ${m.id ?? ""}`;
  if (!themeIds.has(m.theme)) fail(at, `theme is not in the list: ${m.theme}`);
  if (!m.name) fail(at, "name is missing");
  if (!m.unit) fail(at, "unit is missing");
  if (!sourceIds.has(m.source) && !URL_RE.test(m.source ?? "")) fail(at, `source is neither a source id nor an address: ${m.source}`);
  if (!GATES.includes(m.gate)) fail(at, `gate must be one of ${GATES.join(", ")}: ${m.gate}`);
  if (!/^[a-z]{2}$/.test(m.country ?? "")) fail(at, `country is a two-letter code in lower case: ${m.country}`);
  if (m.cadence !== undefined && !CADENCES.includes(m.cadence)) fail(at, `cadence must be one of ${CADENCES.join(", ")}: ${m.cadence}`);
  if (!Array.isArray(m.observations)) {
    fail(at, "observations must be a list");
    continue;
  }
  let last = "";
  for (const [j, o] of m.observations.entries()) {
    const oat = `${at} observations[${j}]`;
    observations += 1;
    day(`${oat} read`, o.read);
    if (typeof o.read === "string" && o.read < last) fail(oat, `read ${o.read} comes before ${last}: observations go in the order they were read`);
    if (typeof o.read === "string") last = o.read;
    if (!PERIOD.test(o.period ?? "")) fail(oat, `period must look like 2025, 2025-Q4, 2025-11, 2025-W47 or 2025-11-17: ${o.period}`);
    plainLine(`${oat} note`, o.note);
    if (o.value === null) {
      if (!UNREAD.includes(o.note)) fail(oat, `a reading without a value notes ${UNREAD.map((n) => `"${n}"`).join(" or ")}`);
    } else {
      if (typeof o.value !== "number" || !Number.isFinite(o.value)) fail(oat, `value must be a number, or null for a source that could not be read: ${o.value}`);
      if (!GRADES.includes(o.grade)) fail(oat, `grade must be one of ${GRADES.join(", ")}: ${o.grade}`);
      if (!URL_RE.test(o.url ?? "")) fail(oat, `url is not an address: ${o.url}`);
    }
  }
}

if (findings.length) {
  for (const f of findings) console.error(f);
  console.error(`${findings.length} finding(s) in ${file}`);
  process.exit(1);
}
console.log(`ok: ${file} holds ${sources.length} source(s), ${themes.length} theme(s), ${metrics.length} metric(s), ${observations} observation(s)`);
