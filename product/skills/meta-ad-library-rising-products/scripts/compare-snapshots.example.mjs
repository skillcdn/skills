#!/usr/bin/env node
// Lays two snapshots of one market and category side by side, entry by entry, matched by `key`.
//
//   node compare-snapshots.example.mjs <snapshots folder> [<market> <category>] [--json]
//   node compare-snapshots.example.mjs <earlier.json> <later.json> [--json]
//
// A folder is read for files named <YYYY-MM-DD>-meta-<market>-<category>.json and the two latest of
// the series are taken. Every entry of either file is shown: the ones the later run counted, with the
// change in active ads and in life90, and under them the ones it did not count. Needs Node.js 22 or
// newer and nothing else. It reads the two files and writes nothing.

import { readFileSync, readdirSync, statSync } from "node:fs";
import { basename, join } from "node:path";

const NAME_RE = /^(\d{4}-\d{2}-\d{2})-meta-([a-z]{2,3})-(.+)\.json$/;
const GROW_SHARE = 0.25; // a quarter or more, and
const GROW_ADS = 10; // at least ten ads: anything smaller is the library's drift

function stop(message) {
  console.error(message);
  process.exit(2);
}

function load(path) {
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch (e) {
    stop(`cannot read ${path}: ${e.message}`);
  }
}

// The two latest files of one series in a folder.
function latestTwo(folder, market, category) {
  const series = new Map();
  for (const name of readdirSync(folder)) {
    const m = NAME_RE.exec(name);
    if (!m) continue;
    const id = `${m[2]} ${m[3]}`;
    if (!series.has(id)) series.set(id, []);
    series.get(id).push(name);
  }
  if (series.size === 0) stop(`no snapshot named <YYYY-MM-DD>-meta-<market>-<category>.json in ${folder}`);
  let id;
  if (market && category) id = `${market.toLowerCase()} ${category}`;
  else if (series.size === 1) id = [...series.keys()][0];
  else stop(`several series in ${folder}; name one as <market> <category>:\n  ${[...series.keys()].sort().join("\n  ")}`);
  const names = (series.get(id) ?? []).sort();
  if (names.length < 2) stop(`${names.length} snapshot(s) of "${id}" in ${folder}: two are needed to compare`);
  return names.slice(-2).map((n) => join(folder, n));
}

const share = (part, whole) => (typeof part === "number" && typeof whole === "number" && whole > 0 ? part / whole : null);
const life90 = (e) => (typeof e.life90 === "number" ? e.life90 : share(e.older90, e.active));
const percent = (x) => (x === null ? "-" : `${(x * 100).toFixed(1)}%`);
const signed = (n) => (n > 0 ? `+${n}` : `${n}`);

// What makes two counts comparable: the same phrase, search type, sort and locale.
function sameBasis(a, b, earlier, later) {
  if ((a.query ?? a.key) !== (b.query ?? b.key)) return false;
  if (a.search_type && b.search_type && a.search_type !== b.search_type) return false;
  for (const field of ["sort", "locale"]) {
    if (earlier[field] && later[field] && earlier[field] !== later[field]) return false;
  }
  return true;
}

function row(name, key, was, now, earlier, later) {
  const notes = [];
  const r = {
    key,
    name,
    earlier: was ? was.active : null,
    later: now.active,
    change: null,
    change_share: null,
    life90_earlier: was ? life90(was) : null,
    life90_later: life90(now),
    class: [now.class, now.pace].filter(Boolean).join(", "),
    notes,
  };
  if (!was) notes.push("new");
  else if (!sameBasis(was, now, earlier, later)) notes.push("new basis");
  else if (typeof was.active === "number" && typeof now.active === "number") {
    r.change = now.active - was.active;
    r.change_share = share(r.change, was.active);
    if (r.change_share !== null && Math.abs(r.change) >= GROW_ADS && Math.abs(r.change_share) >= GROW_SHARE) {
      notes.push(r.change > 0 ? "grew" : "fading");
    }
  }
  if (now.reported === false) notes.push("unranked");
  return r;
}

function compare(earlier, later) {
  const before = new Map((earlier.items ?? []).map((e) => [e.key, e]));
  const after = new Map((later.items ?? []).map((e) => [e.key, e]));
  const deferred = new Set(later.deferred ?? []);
  const days = Math.round((Date.parse(later.taken) - Date.parse(earlier.taken)) / 86400000);
  const baseline =
    later.baseline &&
    row("(baseline) " + (later.baseline.query ?? ""), "(baseline)", earlier.baseline ?? null, later.baseline, earlier, later);
  const rows = [...after.values()].map((now) => row(now.name ?? now.key, now.key, before.get(now.key) ?? null, now, earlier, later));
  const absent = [...before.values()]
    .filter((was) => !after.has(was.key))
    .map((was) => ({
      key: was.key,
      name: was.name ?? was.key,
      earlier: was.active,
      life90_earlier: life90(was),
      note: deferred.has(was.key) ? "deferred" : "dropped out",
    }));
  return { days, baseline, rows, absent };
}

// Columns line up under Hangul, kana and Han, which take two cells each in a terminal.
function width(text) {
  let w = 0;
  for (const ch of String(text)) {
    const c = ch.codePointAt(0);
    const wide =
      (c >= 0x1100 && c <= 0x115f) ||
      (c >= 0x2e80 && c <= 0xa4cf) ||
      (c >= 0xac00 && c <= 0xd7a3) ||
      (c >= 0xf900 && c <= 0xfaff) ||
      (c >= 0xfe30 && c <= 0xfe4f) ||
      (c >= 0xff00 && c <= 0xff60) ||
      (c >= 0xffe0 && c <= 0xffe6) ||
      (c >= 0x1f300 && c <= 0x1faff);
    w += wide ? 2 : 1;
  }
  return w;
}

function table(head, lines) {
  const widths = head.map((h, i) => Math.max(width(h), ...lines.map((l) => width(l[i]))));
  const fit = (cells) => cells.map((c, i) => String(c) + " ".repeat(widths[i] - width(c))).join("  ").trimEnd();
  return [fit(head), fit(widths.map((w) => "-".repeat(w))), ...lines.map(fit)].join("\n");
}

const args = process.argv.slice(2);
const asJson = args.includes("--json");
const rest = args.filter((a) => a !== "--json");
if (rest.length === 0) stop("usage: compare-snapshots.example.mjs <snapshots folder> [<market> <category>] | <earlier.json> <later.json>  [--json]");

let paths;
if (statSync(rest[0], { throwIfNoEntry: false })?.isDirectory()) paths = latestTwo(rest[0], rest[1], rest[2]);
else if (rest.length === 2) paths = rest;
else stop("give a folder of snapshots, or an earlier and a later snapshot file");

const [earlier, later] = paths.map(load);
if (earlier.market && later.market && earlier.market !== later.market) {
  stop(`the two snapshots are of different markets (${earlier.market}, ${later.market}): counts of two countries are not compared`);
}
const result = compare(earlier, later);

if (asJson) {
  console.log(JSON.stringify({ earlier: basename(paths[0]), later: basename(paths[1]), ...result }, null, 2));
} else {
  console.log(`${basename(paths[0])} (${earlier.taken}, ${earlier.mode ?? "sweep"})  ->  ${basename(paths[1])} (${later.taken}, ${later.mode ?? "sweep"}), ${result.days} days apart`);
  const line = (r) => [
    r.name,
    r.earlier ?? "-",
    r.later ?? "-",
    r.change === null ? "-" : `${signed(r.change)} (${percent(r.change_share)})`,
    percent(r.life90_earlier),
    percent(r.life90_later),
    r.class || "-",
    r.notes.join(", "),
  ];
  const lines = [...(result.baseline ? [line(result.baseline)] : []), ...result.rows.map(line)];
  console.log(table(["entry", "A before", "A now", "change", "life90 before", "life90 now", "class, pace", "note"], lines));
  if (result.absent.length) {
    console.log("\nNot counted in the later run:");
    console.log(table(["entry", "A before", "life90 before", "note"], result.absent.map((a) => [a.name, a.earlier ?? "-", percent(a.life90_earlier), a.note])));
  }
  if ((later.deferred ?? []).length) console.log(`\nDeferred to the next run: ${later.deferred.join(", ")}`);
}
