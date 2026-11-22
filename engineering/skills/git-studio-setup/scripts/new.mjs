// Starts a unit: copies <folder>/_template to <folder>/<slug>, fills its record and adds its row to the ledger.
// Usage: node scripts/new.mjs [<unit>] <YYYY-MM-DD-slug> --title="..." --what="what it is, in a line" --keys="name, name"
//        [--who="its subject"] [--task=<board task>] [--format=<folder under formats/>] [--owner=<login>]
//        [--for=<a time with its zone>] [--<another unit's folder>="slug, slug"] [--allowed="<the person's words>"]
// The unit's name comes first where the studio holds more than one kind. The day in the slug is the day the unit is
// meant for. A key another row holds stops the command, unless --allowed carries the words of the person who said to
// make it all the same; they go into the row's note. An option named as another unit's folder (--creatives on a round)
// records the units of that kind this one is about. --for writes the time the first state waits for (planned_for):
// the check warns once it has passed, which is how the next round is put on the calendar.
import { execSync } from "node:child_process";
import { cpSync, existsSync } from "node:fs";
import { join } from "node:path";
import { SLUG, addRow, args, items, pickUnit, readJson, readLedger, recordName, root, sharedKeys, units, writeJson } from "./studio.mjs";

const { positional, options } = args();
const { u, rest: [slug] } = pickUnit(positional);
const stop = (message) => { console.error(message); process.exit(1); };
if (!slug || !SLUG.test(slug)) stop(`usage: node scripts/new.mjs [<unit>] <YYYY-MM-DD-slug> --title=... --what=... --keys=...  (got "${slug ?? ""}")`);
if (items(u).some((i) => i.slug === slug)) stop(`${u.folder}/${slug} exists already`);
const ledger = readLedger(u);
if (!ledger) stop(`${u.ledger} is missing: the ledger holds a row for every ${u.unit}`);
const keys = String(options.keys ?? "").split(",").map((k) => k.trim().toLowerCase()).filter(Boolean);
const shared = sharedKeys(ledger, slug, keys);
if (shared.length && !options.allowed) stop(`already in the ledger: ${shared.join(", ")}. Made twice only on the person's word: --allowed="<their words>"`);

const dir = join(root, u.folder, slug);
cpSync(join(root, u.folder, "_template"), dir, { recursive: true });
const gitEmail = () => { try { return execSync("git config user.email", { encoding: "utf8" }).trim(); } catch { return ""; } };
const data = readJson(join(dir, recordName(u)));
Object.assign(data, {
  slug,
  title: options.title ?? "",
  status: u.states[0],
  owner: options.owner ?? gitEmail(),
  task: options.task ? Number(options.task) : null,
  created_at: new Date().toISOString().slice(0, 10),
});
if (options.format) data.format = options.format;
if (typeof options.for === "string") {
  if (Number.isNaN(Date.parse(options.for))) stop(`--for is not a time: "${options.for}" (write it with its zone, 2026-01-05T09:00+09:00)`);
  data[`${u.states[0]}_for`] = options.for;
}
if (data.format && !existsSync(join(root, "formats", data.format))) console.warn(`formats/${data.format} is not there yet`);
for (const o of units) if (o !== u && typeof options[o.folder] === "string") data[o.folder] = options[o.folder].split(",").map((s) => s.trim()).filter(Boolean);
writeJson(join(dir, recordName(u)), data);
addRow(u, slug, { state: data.status, what: options.what, keys: keys.join(", "), who: options.who, note: options.allowed === true ? "" : options.allowed });
console.log(`${u.folder}/${slug} is started; its row is in ${u.ledger}`);
