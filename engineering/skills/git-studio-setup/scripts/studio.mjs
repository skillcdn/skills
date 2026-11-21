// What the studio's commands share: the configuration (studio.json), the items with their records, the ledger.
// No dependency. Node.js with ES modules; every path is taken from the repository's root.
import { existsSync, readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
export const readJson = (path) => JSON.parse(readFileSync(path, "utf8"));
export const writeJson = (path, value) => writeFileSync(path, JSON.stringify(value, null, 2) + "\n");
export const config = readJson(join(root, "studio.json"));
export const recordName = `${config.unit}.json`;
export const SLUG = /^\d{4}-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+)*$/;
export const states = [...config.states, "archived"];
// True from the state on, in the order studio.json gives; an archived item has reached nothing.
export const reached = (data, state) => data.status !== "archived" && config.states.indexOf(data.status) >= config.states.indexOf(state);
// The day a record holds for its state: <state>.at (approved, published) or <state>_for (scheduled), else none.
export const dayOf = (data) => String(data[data.status]?.at ?? data[`${data.status}_for`] ?? "").slice(0, 10);

const folders = (dir) => (existsSync(dir) ? readdirSync(dir).filter((n) => !n.startsWith("_") && statSync(join(dir, n)).isDirectory()) : []);

// Every item: in progress at <folder>/<slug>/, filed at <folder>/<filed state>/<day>/<slug>/. `dir` is relative to the root.
export function items() {
  const list = [];
  const add = (dir, slug, filed) => {
    const file = join(root, dir, recordName);
    let data = null, broken = null;
    try { data = readJson(file); } catch (e) { broken = existsSync(file) ? e.message : `no ${recordName}`; }
    list.push({ slug, dir, filed, data, broken });
  };
  for (const name of folders(join(root, config.folder))) {
    if (name !== config.filed) { add(`${config.folder}/${name}`, name, false); continue; }
    for (const day of folders(join(root, config.folder, name))) {
      for (const slug of folders(join(root, config.folder, name, day))) add(`${config.folder}/${name}/${day}/${slug}`, slug, true);
    }
  }
  return list.sort((a, b) => a.slug.localeCompare(b.slug));
}

// The ledger is a Markdown table that ends its file: | slug | state | what | keys | who | note |
export const ledgerFile = join(root, config.ledger);
const cellsOf = (line) => line.split("|").slice(1, -1).map((c) => c.trim());
export function readLedger() {
  if (!existsSync(ledgerFile)) return null;
  const lines = readFileSync(ledgerFile, "utf8").split("\n");
  const rows = [];
  lines.forEach((line, n) => {
    const c = cellsOf(line);
    if (c.length < 5 || !SLUG.test(c[0])) return;
    rows.push({ n, slug: c[0], state: c[1], what: c[2], keys: c[3].split(",").map((k) => k.trim().toLowerCase()).filter(Boolean), who: c[4], note: c[5] ?? "" });
  });
  return { lines, rows };
}
// The other rows that hold one of these keys, as "key (slug)"; a row whose note carries the person's word is passed over.
export const sharedKeys = (ledger, slug, keys) =>
  keys.flatMap((k) => ledger.rows.filter((r) => r.slug !== slug && !r.note && r.keys.includes(k)).map((r) => `${k} (${r.slug})`));
export function addRow(slug, { state, what = "", keys = "", who = "", note = "" }) {
  const text = readFileSync(ledgerFile, "utf8").replace(/\n*$/, "\n");
  writeFileSync(ledgerFile, `${text}| ${slug} | ${state} | ${what} | ${keys} | ${who} | ${note} |\n`);
}
// Rewrites each row's state from the item's record; returns the slugs whose row changed.
export function syncLedger() {
  const ledger = readLedger();
  if (!ledger) return [];
  const changed = [];
  for (const item of items()) {
    const row = ledger.rows.find((r) => r.slug === item.slug);
    if (!row || !item.data) continue;
    const state = [item.data.status, dayOf(item.data)].filter(Boolean).join(" ");
    if (row.state === state) continue;
    const c = cellsOf(ledger.lines[row.n]);
    c[1] = state;
    ledger.lines[row.n] = `| ${c.join(" | ")} |`;
    changed.push(item.slug);
  }
  if (changed.length) writeFileSync(ledgerFile, ledger.lines.join("\n"));
  return changed;
}

// The files of an item that match one of studio.json's `previews`, a path with * in its last part; the first pattern that matches anything wins.
export function previews(item) {
  for (const pattern of config.previews ?? []) {
    const at = pattern.lastIndexOf("/");
    const dir = pattern.slice(0, Math.max(at, 0));
    const escaped = pattern.slice(at + 1).replace(/[.+^$(){}|[\]\\]/g, "\\$&").replace(/\*/g, ".*");
    const name = new RegExp("^" + escaped + "$");
    const full = join(root, item.dir, dir);
    const found = existsSync(full) ? readdirSync(full).filter((f) => name.test(f)).sort() : [];
    if (found.length) return found.map((f) => [item.dir, dir, f].filter(Boolean).join("/"));
  }
  return [];
}

export function args(argv = process.argv.slice(2)) {
  const positional = [], options = {};
  for (const a of argv) {
    const m = /^--([^=]+)(?:=(.*))?$/.exec(a);
    if (m) options[m[1]] = m[2] ?? true; else positional.push(a);
  }
  return { positional, options };
}
