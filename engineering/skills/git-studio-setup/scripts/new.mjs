// Starts an item: copies <folder>/_template to <folder>/<slug>, fills its record and adds its row to the ledger.
// Usage: node scripts/new.mjs <YYYY-MM-DD-slug> --title="..." --what="what it is, in a line" --keys="name, name" [--who="its subject"]
//        [--task=<board task>] [--format=<folder under formats/>] [--owner=<login>] [--allowed="<the person's words>"]
// The day in the slug is the day the item is meant for. A key another row holds stops the command, unless
// --allowed carries the words of the person who said to make it all the same; they go into the row's note.
import { execSync } from "node:child_process";
import { cpSync, existsSync } from "node:fs";
import { join } from "node:path";
import { SLUG, addRow, args, config, items, readJson, readLedger, recordName, root, sharedKeys, writeJson } from "./studio.mjs";

const { positional: [slug], options } = args();
const stop = (message) => { console.error(message); process.exit(1); };
if (!slug || !SLUG.test(slug)) stop(`usage: node scripts/new.mjs <YYYY-MM-DD-slug> --title=... --what=... --keys=...  (got "${slug ?? ""}")`);
if (items().some((i) => i.slug === slug)) stop(`${slug} exists already`);
const ledger = readLedger();
if (!ledger) stop(`${config.ledger} is missing: the ledger holds a row for every ${config.unit}`);
const keys = String(options.keys ?? "").split(",").map((k) => k.trim().toLowerCase()).filter(Boolean);
const shared = sharedKeys(ledger, slug, keys);
if (shared.length && !options.allowed) stop(`already in the ledger: ${shared.join(", ")}. Made twice only on the person's word: --allowed="<their words>"`);

const dir = join(root, config.folder, slug);
cpSync(join(root, config.folder, "_template"), dir, { recursive: true });
const gitEmail = () => { try { return execSync("git config user.email", { encoding: "utf8" }).trim(); } catch { return ""; } };
const data = readJson(join(dir, recordName));
Object.assign(data, {
  slug,
  title: options.title ?? "",
  status: config.states[0],
  owner: options.owner ?? gitEmail(),
  task: options.task ? Number(options.task) : null,
  created_at: new Date().toISOString().slice(0, 10),
});
if (options.format) data.format = options.format;
if (data.format && !existsSync(join(root, "formats", data.format))) console.warn(`formats/${data.format} is not there yet`);
writeJson(join(dir, recordName), data);
addRow(slug, { state: data.status, what: options.what, keys: keys.join(", "), who: options.who, note: options.allowed === true ? "" : options.allowed });
console.log(`${config.folder}/${slug} is started; its row is in ${config.ledger}`);
