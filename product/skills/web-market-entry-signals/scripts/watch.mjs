#!/usr/bin/env node
// Prints a watch list (watch.json, schema market-watch/1) as tables. Reads only; writes nothing.
// Usage: node watch.mjs [path/to/watch.json] [option]     (default file: ./watch.json, then ./market/watch.json)
//   (no option)        every theme: status, kind, id, its latest reading with the change, the next check
//   --due [YYYY-MM-DD] the themes whose next check has come by that day (today when none), dropped ones included,
//                      with each metric's cadence and the last period read
//   --id <theme>       every observation of one theme, with the change from the period before
//   --gates            the verdicts on the four questions by country, themes that pass all four first
//   --ads              the two latest ad snapshots of each market and category beside the file, to compare
//   --sources          the sources and their cadence
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";

const args = process.argv.slice(2);
const fileArg = args.find((a) => a.endsWith(".json"));
const file = fileArg ?? (existsSync("watch.json") ? "watch.json" : "market/watch.json");
const option = args.find((a) => a.startsWith("--")) ?? "";
const valueAfter = (name) => {
  const i = args.indexOf(name);
  const v = i >= 0 ? args[i + 1] : undefined;
  return v && !v.startsWith("--") && !v.endsWith(".json") ? v : undefined;
};

const watch = JSON.parse(readFileSync(file, "utf8"));
const sources = watch.sources ?? [];
const themes = watch.themes ?? [];
const metrics = watch.metrics ?? [];

// Width of a string in a terminal: a Hangul, kana, CJK or full-width character takes two columns.
const wide = (cp) =>
  (cp >= 0x1100 && cp <= 0x115f) || (cp >= 0x2e80 && cp <= 0xa4cf) || (cp >= 0xac00 && cp <= 0xd7a3) ||
  (cp >= 0xf900 && cp <= 0xfaff) || (cp >= 0xfe30 && cp <= 0xfe4f) || (cp >= 0xff00 && cp <= 0xff60) || (cp >= 0xffe0 && cp <= 0xffe6);
const width = (s) => [...String(s)].reduce((n, ch) => n + (wide(ch.codePointAt(0)) ? 2 : 1), 0);
const pad = (s, n) => String(s) + " ".repeat(Math.max(0, n - width(s)));
function table(head, rows) {
  if (!rows.length) return console.log("(none)");
  const widths = head.map((h, i) => Math.max(width(h), ...rows.map((r) => width(r[i] ?? ""))));
  const line = (cells) => cells.map((c, i) => pad(c ?? "", widths[i])).join("  ").trimEnd();
  console.log(line(head));
  console.log(widths.map((w) => "-".repeat(w)).join("  "));
  for (const r of rows) console.log(line(r));
}

// The value of each period is its latest reading; a change is measured against the period before.
function periods(metric) {
  const byPeriod = new Map();
  for (const o of metric.observations ?? []) if (o.value !== null && o.value !== undefined) byPeriod.set(o.period, o);
  return [...byPeriod.values()].sort((a, b) => (a.period < b.period ? -1 : a.period > b.period ? 1 : 0));
}
const change = (now, before) => (before && before.value ? `${now.value >= before.value ? "+" : ""}${(((now.value - before.value) / Math.abs(before.value)) * 100).toFixed(1)}%` : "");
const fmt = (v) => (typeof v === "number" ? v.toLocaleString("en-US", { maximumFractionDigits: 2 }) : "");
const cadenceOf = (m) => m.cadence ?? sources.find((s) => s.id === m.source)?.cadence ?? "once";
const STATUS_ORDER = ["candidate", "testing", "watch", "cooling", "dropped"];
const byStatus = (a, b) => STATUS_ORDER.indexOf(a.status) - STATUS_ORDER.indexOf(b.status) || (a.id < b.id ? -1 : 1);

function latestOf(theme) {
  const rows = metrics.filter((m) => m.theme === theme.id).map((m) => ({ m, p: periods(m) })).filter((x) => x.p.length);
  if (!rows.length) return ["", "", ""];
  const { m, p } = rows.sort((a, b) => (a.p.at(-1).read < b.p.at(-1).read ? 1 : -1))[0];
  return [m.id, `${fmt(p.at(-1).value)} ${m.unit} (${p.at(-1).period})`, change(p.at(-1), p.at(-2))];
}

if (option === "--sources") {
  table(["id", "cadence", "free", "name", "url"], sources.map((s) => [s.id, s.cadence, s.free === false ? "no" : "yes", s.name, s.url]));
} else if (option === "--gates") {
  const rows = [];
  for (const t of themes) {
    for (const [country, g] of Object.entries(t.gates ?? {})) {
      const passes = ["01", "02", "03", "04"].filter((q) => g[q] === "pass").length;
      rows.push({ passes, cells: [t.id, country, g["01"], g["02"], g["03"], g["04"], t.status, g.judged ?? "", g.memo ?? ""] });
    }
  }
  rows.sort((a, b) => b.passes - a.passes || (a.cells[0] < b.cells[0] ? -1 : 1));
  table(["theme", "country", "01 paying", "02 growing", "03 entering", "04 earning", "status", "judged", "memo"], rows.map((r) => r.cells));
} else if (option === "--id") {
  const id = valueAfter("--id");
  const theme = themes.find((t) => t.id === id);
  if (!theme) {
    console.error(`no theme with the id ${id}; the ids: ${themes.map((t) => t.id).join(", ")}`);
    process.exit(1);
  }
  console.log(`${theme.id}: ${theme.name} (${theme.kind}, ${theme.status}, next check ${theme.next_check})`);
  for (const m of metrics.filter((x) => x.theme === id)) {
    console.log(`\n${m.id}: ${m.name}, ${m.unit}, question ${m.gate}, ${m.country}, ${cadenceOf(m)}`);
    const p = periods(m);
    const rows = (m.observations ?? []).map((o) => {
      const i = p.indexOf(o);
      const note = o.value === null ? o.note : i < 0 ? `revised later. ${o.note ?? ""}`.trim() : o.note ?? "";
      return [o.read, o.period, fmt(o.value), i > 0 ? change(o, p[i - 1]) : "", o.grade ?? "", note];
    });
    table(["read", "period", "value", "change", "grade", "note"], rows);
  }
} else if (option === "--due") {
  const today = valueAfter("--due") ?? new Date().toISOString().slice(0, 10);
  const due = themes.filter((t) => t.next_check <= today).sort(byStatus);
  console.log(`Themes whose next check has come by ${today}: ${due.length} of ${themes.length}`);
  const rows = [];
  for (const t of due) {
    const own = metrics.filter((m) => m.theme === t.id);
    if (!own.length) rows.push([t.status, t.id, t.next_check, "(no metric)", "", ""]);
    for (const m of own) rows.push([t.status, t.id, t.next_check, m.id, cadenceOf(m), periods(m).at(-1)?.period ?? "(never read)"]);
  }
  table(["status", "theme", "next check", "metric", "cadence", "last period"], rows);
} else if (option === "--ads") {
  const dir = join(dirname(file), "snapshots");
  const groups = new Map();
  for (const name of existsSync(dir) ? readdirSync(dir).sort() : []) {
    const m = /^(\d{4}-\d{2}-\d{2})-meta-([a-z]{2})-(.+)\.json$/i.exec(name);
    if (m) groups.set(`${m[2]} ${m[3]}`, [...(groups.get(`${m[2]} ${m[3]}`) ?? []), name]);
  }
  if (!groups.size) console.log(`No snapshot named <YYYY-MM-DD>-meta-<market>-<category>.json in ${dir}`);
  for (const [key, names] of groups) {
    const [older, newer] = names.slice(-2);
    if (!newer) console.log(`${key}: one snapshot (${older}); nothing to compare until the next round`);
    else console.log(`${key}: compare ${join(dir, older)} with ${join(dir, newer)}, using the compare script of meta-ad-library-rising-products`);
  }
} else {
  const today = new Date().toISOString().slice(0, 10);
  const rows = [...themes].sort(byStatus).map((t) => [t.status, t.kind, t.id, ...latestOf(t), t.next_check <= today ? `${t.next_check} due` : t.next_check]);
  table(["status", "kind", "theme", "metric", "latest", "change", "next check"], rows);
}
