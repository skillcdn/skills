// Run after any change of state: brings every ledger's states up to the records, and moves each unit that reached
// its kind's filed state to <folder>/<filed state>/<day of its <state>.at>/<slug>/ with git mv, so history follows.
// Usage: node scripts/file.mjs [--dry-run]
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, readdirSync, renameSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { args, dayOf, items, root, syncLedger, units } from "./studio.mjs";

const dry = Boolean(args().options["dry-run"]);
let moved = 0;
const rows = [];
for (const u of units) {
  for (const item of items(u)) {
    if (!item.data || item.filed || item.data.status !== u.filed) continue;
    const day = dayOf(item.data);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(day)) { console.warn(`skip ${item.dir}: ${u.filed}.at holds no day`); continue; }
    const to = `${u.folder}/${u.filed}/${day}/${item.slug}`;
    if (existsSync(join(root, to))) { console.warn(`skip ${item.dir}: ${to} exists already`); continue; }
    console.log(`${dry ? "would move" : "moved"} ${item.dir} -> ${to}`);
    moved += 1;
    if (dry) continue;
    mkdirSync(dirname(join(root, to)), { recursive: true });
    try { execFileSync("git", ["mv", item.dir, to], { cwd: root, stdio: "pipe" }); } catch { renameSync(join(root, item.dir), join(root, to)); }
    // A path in the unit's JSON that climbed to the root (a plan naming its format) is two folders deeper now.
    for (const name of readdirSync(join(root, to)).filter((f) => f.endsWith(".json"))) {
      const text = readFileSync(join(root, to, name), "utf8");
      const fixed = text.replaceAll('"../../', '"../../../../');
      if (fixed !== text) writeFileSync(join(root, to, name), fixed);
    }
  }
  if (!dry) rows.push(...syncLedger(u).map((slug) => `${u.folder}/${slug}`));
}
console.log(`${moved} filed; ${rows.length} ledger row(s) brought up to the records${rows.length ? `: ${rows.join(", ")}` : ""}`);
