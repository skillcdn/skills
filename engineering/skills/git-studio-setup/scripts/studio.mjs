// What the studio's commands share: the configuration (studio.json), each kind of unit with its records, its ledger.
// No dependency. Node.js with ES modules; every path is taken from the repository's root.
import { existsSync, readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
export const readJson = (path) => JSON.parse(readFileSync(path, "utf8"));
export const writeJson = (path, value) => writeFileSync(path, JSON.stringify(value, null, 2) + "\n");
export const config = readJson(join(root, "studio.json"));
// The kinds of unit the studio holds, each with its folder, its states and its ledger. Most studios hold one.
export const units = Array.isArray(config.units) ? config.units : [];
export const recordName = (u) => `${u.unit}.json`;
// The files every unit of a kind works on, outside any unit: the watch list a round reads and adds to.
export const standing = (u) => [u.standing ?? []].flat();
export const SLUG = /^\d{4}-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+)*$/;
export const statesOf = (u) => [...u.states, "archived"];
// True from the state on, in the order studio.json gives; an archived unit has reached nothing.
export const reached = (u, data, state) => data.status !== "archived" && u.states.indexOf(data.status) >= u.states.indexOf(state);
// The day a record holds for its state: <state>.at (approved, published) or <state>_for (scheduled), else none.
export const dayOf = (data) => String(data[data.status]?.at ?? data[`${data.status}_for`] ?? "").slice(0, 10);

// The unit a command is about: its name as the first argument, which a studio of one kind may leave out.
export function pickUnit(positional) {
  const named = units.find((u) => u.unit === positional[0]);
  if (named) return { u: named, rest: positional.slice(1) };
  if (units.length === 1) return { u: units[0], rest: positional };
  console.error(`which unit? Name it first: ${units.map((u) => u.unit).join(" | ")}`);
  process.exit(1);
}

const folders = (dir) => (existsSync(dir) ? readdirSync(dir).filter((n) => !n.startsWith("_") && statSync(join(dir, n)).isDirectory()) : []);

// Every unit of one kind: in progress at <folder>/<slug>/, filed at <folder>/<filed state>/<day>/<slug>/. `dir` is relative to the root.
export function items(u) {
  const list = [];
  const add = (dir, slug, filed) => {
    const file = join(root, dir, recordName(u));
    let data = null, broken = null;
    try { data = readJson(file); } catch (e) { broken = existsSync(file) ? e.message : `no ${recordName(u)}`; }
    list.push({ u, slug, dir, filed, data, broken });
  };
  for (const name of folders(join(root, u.folder))) {
    if (name !== u.filed) { add(`${u.folder}/${name}`, name, false); continue; }
    for (const day of folders(join(root, u.folder, name))) {
      for (const slug of folders(join(root, u.folder, name, day))) add(`${u.folder}/${name}/${day}/${slug}`, slug, true);
    }
  }
  return list.sort((a, b) => a.slug.localeCompare(b.slug));
}
export const allItems = () => units.flatMap(items);

// Where two kinds meet: a record's field named as another unit's folder (a round's "creatives") holds slugs of that kind.
export const refsOf = (item) => units
  .filter((o) => o !== item.u && item.data?.[o.folder] != null)
  .map((o) => ({ u: o, slugs: [item.data[o.folder]].flat().map(String).filter(Boolean) }));

// A ledger is a Markdown table that ends its file: | slug | state | what | keys | who | note |
const cellsOf = (line) => line.split("|").slice(1, -1).map((c) => c.trim());
export function readLedger(u) {
  const file = join(root, u.ledger);
  if (!existsSync(file)) return null;
  const lines = readFileSync(file, "utf8").split("\n");
  const rows = [];
  lines.forEach((line, n) => {
    const c = cellsOf(line);
    if (c.length < 5 || !SLUG.test(c[0])) return;
    rows.push({ n, slug: c[0], state: c[1], what: c[2], keys: c[3].split(",").map((k) => k.trim().toLowerCase()).filter(Boolean), who: c[4], note: c[5] ?? "" });
  });
  return { file, lines, rows };
}
// The other rows that hold one of these keys, as "key (slug)"; a row whose note carries the person's word is passed over.
export const sharedKeys = (ledger, slug, keys) =>
  keys.flatMap((k) => ledger.rows.filter((r) => r.slug !== slug && !r.note && r.keys.includes(k)).map((r) => `${k} (${r.slug})`));
export function addRow(u, slug, { state, what = "", keys = "", who = "", note = "" }) {
  const file = join(root, u.ledger);
  const text = readFileSync(file, "utf8").replace(/\n*$/, "\n");
  writeFileSync(file, `${text}| ${slug} | ${state} | ${what} | ${keys} | ${who} | ${note} |\n`);
}
// Rewrites each row's state from the unit's record; returns the slugs whose row changed.
export function syncLedger(u) {
  const ledger = readLedger(u);
  if (!ledger) return [];
  const changed = [];
  for (const item of items(u)) {
    const row = ledger.rows.find((r) => r.slug === item.slug);
    if (!row || !item.data) continue;
    const state = [item.data.status, dayOf(item.data)].filter(Boolean).join(" ");
    if (row.state === state) continue;
    const c = cellsOf(ledger.lines[row.n]);
    c[1] = state;
    ledger.lines[row.n] = `| ${c.join(" | ")} |`;
    changed.push(item.slug);
  }
  if (changed.length) writeFileSync(ledger.file, ledger.lines.join("\n"));
  return changed;
}

// The files of a unit that match one of its kind's `previews`, a path with * in its last part; the first pattern that matches anything wins.
export function previews(item) {
  for (const pattern of item.u.previews ?? []) {
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
