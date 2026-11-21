// The studio's check, the same before a commit and in continuous integration. It reads only: the configuration,
// every item's record against its state, the ledger, large-file tracking, and the links of the Markdown.
// It needs no binary output: a large file may be a pointer. Usage: node scripts/check.mjs   (exit 1 on an error)
// The kind's own rules live in scripts/check-<unit>.mjs, where it exists: export default (items, { error, warn }) => {}.
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { pathToFileURL } from "node:url";
import { SLUG, config, dayOf, items, reached, readLedger, recordName, root, sharedKeys, states } from "./studio.mjs";

const errors = [], warnings = [];
const error = (where, what) => errors.push(`${where}: ${what}`);
const warn = (where, what) => warnings.push(`${where}: ${what}`);

// The configuration
for (const key of ["unit", "folder", "states", "person", "filed", "ledger"]) if (!config[key]) error("studio.json", `"${key}" is missing`);
for (const s of config.person ?? []) if (!config.states.includes(s)) error("studio.json", `person state "${s}" is not one of the states`);
if (!config.states.includes(config.filed)) error("studio.json", `filed state "${config.filed}" is not one of the states`);
if (!existsSync(join(root, config.folder, "_template", recordName))) error("studio.json", `${config.folder}/_template/${recordName} is missing`);
const ledger = readLedger();
if (!ledger) error(config.ledger, "the ledger is missing");

// Every item
const all = items();
const firstPerson = config.states.find((s) => config.person.includes(s));
for (const item of all) {
  const { slug, dir, data } = item;
  if (!SLUG.test(slug)) error(dir, "the folder is not named YYYY-MM-DD-words-in-kebab-case");
  if (!data) { error(dir, item.broken); continue; }
  if (data.slug !== slug) error(dir, `${recordName} says slug "${data.slug}"`);
  if (!states.includes(data.status)) { error(dir, `status "${data.status}" is not a state of studio.json`); continue; }
  for (const [state, files] of Object.entries(config.needs ?? {})) {
    if (reached(data, state)) for (const f of files) if (!existsSync(join(root, dir, f))) error(dir, `${f} is missing, which "${state}" needs`);
  }
  for (const state of config.person) {
    if (reached(data, state) && !(data[state]?.at && data[state]?.by)) error(dir, `"${state}" is a person's to give: ${recordName} holds no ${state}.at and ${state}.by`);
  }
  if (data.status === config.filed && !item.filed) warn(dir, `it is ${config.filed} and not filed: npm run file`);
  if (data.status !== config.filed && item.filed) error(dir, `it lies under ${config.folder}/${config.filed}/ and is "${data.status}"`);
  const due = data[`${data.status}_for`];
  if (due && Date.parse(due) < Date.now()) warn(dir, `its time (${due}) has passed while it is still "${data.status}": see where it stands, record it, npm run file`);
  if (data.format && !existsSync(join(root, "formats", data.format))) error(dir, `formats/${data.format} does not exist`);
  if (!ledger) continue;
  const row = ledger.rows.find((r) => r.slug === slug);
  if (!row) { error(dir, `no row in ${config.ledger}`); continue; }
  const state = [data.status, dayOf(data)].filter(Boolean).join(" ");
  if (row.state !== state) error(dir, `the ledger says "${row.state}" and the record "${state}": npm run file`);
  if (!row.what || !row.keys.length) (firstPerson && reached(data, firstPerson) ? error : warn)(dir, `its ledger row names no ${row.what ? "keys" : "content"}`);
  const shared = sharedKeys(ledger, slug, row.keys);
  if (shared.length && !row.note) error(dir, `made twice: ${shared.join(", ")}. The row's note holds the person's words where they allowed it`);
}
for (const row of ledger?.rows ?? []) if (!all.some((i) => i.slug === row.slug)) warn(config.ledger, `${row.slug} has a row and no folder`);

// Large files are tracked by git LFS (skipped where git or the attributes cannot be read)
const large = [];
const walk = (dir, visit) => { for (const n of readdirSync(dir)) { const p = join(dir, n); statSync(p).isDirectory() ? walk(p, visit) : visit(p); } };
for (const item of all) for (const sub of config.large ?? []) {
  const dir = join(root, item.dir, sub);
  if (existsSync(dir)) walk(dir, (p) => large.push(p.slice(root.length + 1).replaceAll("\\", "/")));
}
if (large.length) {
  try {
    const out = execFileSync("git", ["check-attr", "filter", "--stdin"], { cwd: root, input: large.join("\n"), encoding: "utf8" });
    for (const line of out.split("\n")) if (line && !line.endsWith(": lfs")) error(line.split(": filter: ")[0], "is not tracked by git LFS (.gitattributes)");
  } catch { warn("git", "large-file tracking was not checked"); }
}

// Every relative link of the Markdown resolves
const skip = new Set([".git", "node_modules", "gallery", ...(config.large ?? [])]);
const rel = (p) => p.slice(root.length + 1).replaceAll("\\", "/");
const markdown = [], linked = new Set();
const collect = (dir) => { for (const n of readdirSync(dir)) { if (skip.has(n)) continue; const p = join(dir, n); statSync(p).isDirectory() ? collect(p) : n.endsWith(".md") && markdown.push(p); } };
collect(root);
for (const file of markdown) {
  const text = readFileSync(file, "utf8").replace(/^```[\s\S]*?^```/gm, "");
  for (const [, target] of text.matchAll(/\]\(([^)\s]+)\)/g)) {
    if (/^([a-z]+:|#|<)/i.test(target)) continue;
    const path = decodeURIComponent(target.split("#")[0]);
    const full = path.startsWith("/") ? join(root, path) : join(dirname(file), path);
    if (!existsSync(full)) error(rel(file), `the link ${target} leads nowhere`);
    else if (full !== file) linked.add(rel(full));
  }
}

// The know-how stays cheap to read: what every session reads is small, a job's skill is small, a page is one read,
// every page of docs/ is linked from somewhere, and the agreement routes to every skill of the studio.
const limits = { "AGENTS.md": 12000, "SKILLCDN.md": 3000, "docs/policy.md": 8000, skill: 8000, page: 16000, ...config.limits };
const pages = markdown.map(rel);
const read = (path) => readFileSync(join(root, path), "utf8");
const agreement = existsSync(join(root, "AGENTS.md")) ? read("AGENTS.md") : null;
const map = existsSync(join(root, "docs", "README.md"));
if (agreement === null) warn("AGENTS.md", "not written yet: its routes to the skills are not checked");
if (!map) warn("docs/README.md", "not written yet: orphan pages are not checked");
for (const path of pages) {
  const isSkill = /^skills\/[^/]+\/SKILL\.md$/.test(path);
  if (!isSkill) continue;
  // A page a skill includes (skillcdn.include in its front-matter) is linked.
  const head = read(path).split(/^---\s*$/m)[1] ?? "";
  for (const [, target] of head.matchAll(/^\s*-\s+(\S+\.md)\s*$/gm)) linked.add(target.startsWith("/") ? target.slice(1) : `${dirname(path)}/${target}`);
  if (agreement !== null && !agreement.includes(dirname(path) + "/")) error(path, "AGENTS.md does not route to it");
}
for (const path of pages) {
  const limit = limits[path] ?? (/^skills\/[^/]+\/SKILL\.md$/.test(path) ? limits.skill : path.startsWith("docs/") ? limits.page : 0);
  const size = read(path).length;
  if (limit && size > limit) error(path, `${size} characters, over its ${limit}: move what one phase reads to the page of that step`);
  if (map && path.startsWith("docs/") && path !== "docs/README.md" && !linked.has(path)) error(path, "no page links it: give it a row in docs/README.md, or link it from the phase that reads it");
}

// The kind's own rules
const own = join(root, "scripts", `check-${config.unit}.mjs`);
if (existsSync(own)) await (await import(pathToFileURL(own).href)).default(all, { error, warn });

for (const w of warnings) console.log(`warning  ${w}`);
for (const e of errors) console.log(`error    ${e}`);
console.log(`${all.length} ${config.unit}(s), ${errors.length} error(s), ${warnings.length} warning(s)`);
process.exit(errors.length ? 1 : 0);
