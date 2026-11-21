// The review screen: writes gallery/index.html (every unit by state, what waits for a person first, the filed ones by
// day) and gallery/<slug>.html (one unit: its previews, the fields studio.json's `shows` names, its Markdown records,
// its record whole). Generated, never committed. Usage: node scripts/gallery.mjs, then node scripts/serve.mjs.
// Previews are large files: git lfs pull first.
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { pathToFileURL } from "node:url";
import { config, dayOf, items, previews, recordName, root } from "./studio.mjs";

// The page's own words, to be put in the team's language.
const WORDS = { waiting: "Waiting for a person", filed: "Filed", search: "Search", record: "Record", back: "All" };

const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const media = (path) => (/\.(mp4|webm|mov)$/i.test(path) ? `<video src="../${esc(path)}" muted loop playsinline controls></video>` : `<img src="../${esc(path)}" loading="lazy" alt="">`);
const say = (value) => (typeof value === "string" ? value : JSON.stringify(value));
const css = `body{font:15px/1.5 system-ui,sans-serif;margin:24px;background:#f6f6f4;color:#1a1a1a}h1{font-size:20px}h2{font-size:15px;margin:28px 0 10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}.card{background:#fff;border:1px solid #ddd;border-radius:8px;overflow:hidden;text-decoration:none;color:inherit}
.card img,.card video{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:#e9e9e6}.card div{padding:8px 10px}.card small{color:#666;display:block}
.state{display:inline-block;padding:0 8px;border-radius:10px;background:#1a1a1a;color:#fff;font-size:12px}.wait{outline:3px solid #d8a100}input{font:inherit;padding:6px 10px;width:260px}
.views img,.views video{max-width:360px;margin:0 10px 10px 0;border:1px solid #ddd;vertical-align:top}pre{background:#fff;border:1px solid #ddd;padding:12px;overflow:auto;white-space:pre-wrap}dt{color:#666;font-size:12px}dd{margin:0 0 8px}`;
const page = (title, body) => `<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><style>${css}</style>${body}`;

export function buildGallery() {
  const all = items().filter((i) => i.data);
  // A unit waits for a person when the state after its own is one only a person gives.
  const waits = (d) => config.person.includes(config.states[config.states.indexOf(d.status) + 1]);
  const shown = (d) => (config.shows ?? []).filter((k) => d[k] != null && d[k] !== "");
  const card = (i) => {
    const d = i.data, first = previews(i)[0];
    const line = [d.owner, d.task ? `#${d.task}` : "", dayOf(d)].filter(Boolean).join(" · ");
    const fields = shown(d).map((k) => `<small>${esc(k)}: ${esc(say(d[k]))}</small>`).join("");
    return `<a class="card${waits(d) ? " wait" : ""}" href="${esc(i.slug)}.html">${first ? media(first) : ""}<div><span class="state">${esc(d.status)}</span> ${esc(d.title || i.slug)}<small>${esc(i.slug)}</small><small>${esc(line)}</small>${fields}</div></a>`;
  };
  const section = (title, list) => (list.length ? `<h2>${esc(title)} (${list.length})</h2><div class="grid">${list.map(card).join("")}</div>` : "");
  const open = all.filter((i) => !i.filed);
  const dayFolder = (i) => i.dir.split("/").at(-2);
  const days = [...new Set(all.filter((i) => i.filed).map(dayFolder))].sort().reverse();
  const body = [
    `<h1>${esc(config.folder)}</h1><input placeholder="${WORDS.search}" oninput="for(const c of document.querySelectorAll('.card'))c.hidden=!c.textContent.toLowerCase().includes(this.value.toLowerCase())">`,
    section(WORDS.waiting, open.filter((i) => waits(i.data))),
    ...[...config.states, "archived"].map((s) => section(s, open.filter((i) => i.data.status === s && !waits(i.data)))),
    ...days.map((day) => section(`${WORDS.filed} ${day}`, all.filter((i) => i.filed && dayFolder(i) === day))),
  ].join("");
  const out = join(root, "gallery");
  mkdirSync(out, { recursive: true });
  writeFileSync(join(out, "index.html"), page(config.folder, body));
  for (const i of all) {
    const d = i.data;
    const notes = readdirSync(join(root, i.dir)).filter((f) => f.endsWith(".md") && f !== "README.md").sort();
    writeFileSync(join(out, `${i.slug}.html`), page(d.title || i.slug, [
      `<p><a href="index.html">${WORDS.back}</a> · <a href="../${esc(i.dir)}/">${esc(i.dir)}</a></p><h1><span class="state">${esc(d.status)}</span> ${esc(d.title || i.slug)}</h1>`,
      `<dl>${shown(d).map((k) => `<dt>${esc(k)}</dt><dd>${esc(say(d[k]))}</dd>`).join("")}</dl>`,
      `<div class="views">${previews(i).map(media).join("")}</div>`,
      ...notes.map((f) => `<h2>${esc(f)}</h2><pre>${esc(readFileSync(join(root, i.dir, f), "utf8"))}</pre>`),
      `<h2>${WORDS.record} (${esc(recordName)})</h2><pre>${esc(JSON.stringify(d, null, 2))}</pre>`,
    ].join("")));
  }
  return all.length;
}

if (process.argv[1] && pathToFileURL(process.argv[1]).href === import.meta.url && existsSync(root)) console.log(`gallery/index.html holds ${buildGallery()} ${config.unit}(s)`);
