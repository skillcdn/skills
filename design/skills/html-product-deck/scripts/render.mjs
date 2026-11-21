// Renders a product deck written by hand (one <section class="slide"> per slide) and checks it.
// Usage: node render.mjs <deck.html> <out folder> [--name <file name, no extension>]
//   PLAYWRIGHT_FROM  a package.json of a project that has playwright-core installed, to borrow it;
//                    else playwright-core is resolved from this file's folder (npm install playwright-core).
// Writes into the out folder:
//   <name>.html   the deck in one file, every relative src="..." and url(...) embedded as a data URL
//   <name>.pdf    one page per slide at the canvas size
//   pages/NN.png  every slide at the canvas size
//   sheet.png     every slide small on one image, numbered
//   report.json   the slide count, the fonts that loaded, the faces that rendered the text, the findings, the notes
// Reads <script type="application/json" id="deck-meta"> in the deck: canvas ([width, height], default
// [1920, 1080]), banned (phrases that must not appear), style (the house style, in the keys the deck and
// minutes skills use: none means the usual set; usual: true adds forbidden to it; else forbidden alone;
// no_bracket_heads), external (false turns the house-style check off; banned is always checked).
// Findings, each with its slide number:
//   outside  an element reaches past the slide (an ancestor with data-bleed is meant to)
//   cut      text longer than its box (an ancestor with data-clip is meant to cut)
//   lone     a block of two lines or more whose last line is one word
//   repeat   two consecutive slides declare the same data-pattern
//   pattern  a slide declares no data-pattern
//   style    a character or a bracketed head the house style bans
//   banned   a phrase from the deck's banned list
//   unstable a slide whose image kept changing from one shot to the next
// Notes, which are no findings: fallback, a run of text partly rendered in a face its own stack does not name (a
// script the stack's faces lack fell to a system face), as the browser itself reports the faces it used.
// Exit code 0 with no finding, 1 with findings (the files are written either way), 2 when it cannot run.
import { createRequire } from "node:module";
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { basename, dirname, extname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const stop = (message) => {
  console.error(message);
  process.exit(2);
};

const args = process.argv.slice(2);
const nameAt = args.indexOf("--name");
const givenName = nameAt >= 0 ? args.splice(nameAt, 2)[1] : null;
if (args.length < 2) stop("usage: node render.mjs <deck.html> <out folder> [--name <file name, no extension>]");
const source = resolve(args[0]);
const outDir = resolve(args[1]);
const name = givenName || basename(dirname(source));
if (!existsSync(source)) stop(`no deck at ${source}`);

const MIME = {
  ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp",
  ".avif": "image/avif", ".gif": "image/gif", ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf",
};
const base = dirname(source);
const relative = (ref) => !/^([a-z][a-z0-9+.-]*:|\/\/|#)/i.test(ref);
function dataUrl(ref) {
  const file = resolve(base, decodeURIComponent(ref.split(/[?#]/)[0]));
  if (!existsSync(file)) stop(`asset not found: ${ref}`);
  const mime = MIME[extname(file).toLowerCase()] || "application/octet-stream";
  return `data:${mime};base64,${readFileSync(file).toString("base64")}`;
}
let doc = readFileSync(source, "utf8");
const metaMatch = doc.match(/<script type="application\/json" id="deck-meta">([\s\S]*?)<\/script>/);
let meta = {};
try {
  meta = metaMatch ? JSON.parse(metaMatch[1]) : {};
} catch (error) {
  stop(`deck-meta is not JSON: ${error.message}`);
}
doc = doc.replace(/\bsrc="([^"]+)"/g, (all, ref) => (relative(ref) ? `src="${dataUrl(ref)}"` : all));
doc = doc.replace(/url\((['"]?)([^)'"]+)\1\)/g, (all, quote, ref) => (relative(ref) ? `url('${dataUrl(ref)}')` : all));

const [width, height] = Array.isArray(meta.canvas) ? meta.canvas : [1920, 1080];
const pagesDir = join(outDir, "pages");
rmSync(pagesDir, { recursive: true, force: true });
mkdirSync(pagesDir, { recursive: true });
const htmlPath = join(outDir, `${name}.html`);
writeFileSync(htmlPath, doc, "utf8");

// The house style, resolved as the deck skill's helper resolves it.
const USUAL = { "·": "middle dot", "•": "bullet", "‧": "hyphenation point", "∙": "bullet operator", "ㆍ": "Hangul middle dot", "—": "em dash", "–": "en dash", "―": "horizontal bar" };
for (let i = 0; i < 20; i++) USUAL[String.fromCodePoint(0x2460 + i)] = "circled number";
function houseStyle() {
  if (meta.external === false) return { forbidden: {}, brackets: false, label: "off" };
  const style = meta.style;
  if (!style) return { forbidden: { ...USUAL }, brackets: true, label: "the usual set" };
  const forbidden = style.usual ? { ...USUAL } : {};
  const own = Array.isArray(style.forbidden) ? Object.fromEntries(style.forbidden.map((c) => [c, c])) : style.forbidden || {};
  for (const [chars, label] of Object.entries(own)) for (const ch of chars) forbidden[ch] = label;
  return { forbidden, brackets: style.no_bracket_heads ?? Boolean(style.usual), label: style.usual ? "the usual set and the deck's own" : "the deck's own set" };
}

// Runs in the page: every slide's visible text and declared pattern, and the layout findings.
const MEASURE = () => {
  const findings = [];
  const label = (el) => {
    const cls = typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/).join(".") : "";
    return `${el.tagName.toLowerCase()}${cls} "${(el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 40)}"`;
  };
  const slides = [...document.querySelectorAll("section.slide")].map((slide, i) => {
    const frame = slide.getBoundingClientRect();
    slide.querySelectorAll("*").forEach((el) => {
      const cs = getComputedStyle(el);
      if (cs.display === "none" || cs.visibility === "hidden") return;
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) return;
      if (!el.closest("[data-bleed]") && (r.left < frame.left - 1 || r.top < frame.top - 1 || r.right > frame.right + 1 || r.bottom > frame.bottom + 1)) findings.push({ slide: i + 1, kind: "outside", what: label(el) });
      if (el.closest("[data-clip]") || ["img", "svg", "figure", "picture", "video", "canvas"].includes(el.tagName.toLowerCase())) return;
      if (!(el.textContent || "").trim()) return;
      if ((el.scrollHeight > el.clientHeight + 2 && cs.overflowY !== "visible") || (el.scrollWidth > el.clientWidth + 2 && cs.overflowX !== "visible")) findings.push({ slide: i + 1, kind: "cut", what: label(el) });
      // A lone word: a block that wraps to two lines or more without a <br>, its last line one word.
      if (cs.display === "inline" || cs.display.includes("flex") || cs.display.includes("grid") || el.querySelector("br")) return;
      if (![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) return;
      const inlineOnly = (node) => {
        for (let p = node.parentElement; p && p !== el; p = p.parentElement) if (getComputedStyle(p).display !== "inline") return false;
        return true;
      };
      const lines = [];
      const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      for (let node; (node = walker.nextNode()); ) {
        if (!inlineOnly(node)) continue;
        const text = node.textContent;
        for (let k = 0; k < text.length; k++) {
          const range = document.createRange();
          range.setStart(node, k);
          range.setEnd(node, k + 1);
          const box = range.getBoundingClientRect();
          if (!box.height) continue;
          const mid = (box.top + box.bottom) / 2;
          let line = lines.find((l) => mid > l.top && mid < l.bottom);
          if (!line) lines.push((line = { top: box.top, bottom: box.bottom, text: "" }));
          line.text += text[k];
        }
      }
      if (lines.length < 2) return;
      lines.sort((a, b) => a.top - b.top);
      const last = lines[lines.length - 1].text.trim();
      if (last && last.split(/\s+/).length === 1) findings.push({ slide: i + 1, kind: "lone", what: `${label(el)}, last line "${last}"` });
    });
    return { text: slide.innerText, pattern: slide.dataset.pattern || "" };
  });
  const fonts = [...new Set([...document.fonts].filter((f) => f.status === "loaded").map((f) => f.family.replace(/["']/g, "")))];
  return { slides, findings, fonts };
};

let chromium;
try {
  ({ chromium } = createRequire(process.env.PLAYWRIGHT_FROM || join(here, "package.json"))("playwright-core"));
} catch {
  stop("playwright-core not found: set PLAYWRIGHT_FROM to the package.json of a project that has it, or run npm install playwright-core in a tools folder and point PLAYWRIGHT_FROM at its package.json");
}
async function launch() {
  for (const channel of ["chrome", "msedge", "chromium"]) {
    try {
      return await chromium.launch(channel === "chromium" ? {} : { channel });
    } catch {
      // try the next one
    }
  }
  stop("no Chromium-family browser found: install Chrome or Edge, or run npx playwright install chromium");
}

// The faces the browser rendered the text in, by the DevTools protocol: every family with its glyph count, and
// every run of text of which a part was rendered in a face its own stack does not name (a script the stack's faces
// lack fell to a system face). A family declared by @font-face is named by its local() sources too, and a face
// the page loaded from a file is always named. Returns no faces where the browser will not say.
const LOCALS = new Map();
for (const block of doc.match(/@font-face\s*{[^}]*}/g) || []) {
  const family = (block.match(/font-family:\s*(['"]?)([^;'"]+)\1/) || [])[2];
  if (!family) continue;
  const key = family.trim().toLowerCase();
  LOCALS.set(key, [...(LOCALS.get(key) || []), ...[...block.matchAll(/local\((['"]?)([^)'"]+)\1\)/g)].map((m) => m[2].trim().toLowerCase())]);
}
async function facesUsed(page) {
  try {
    const cdp = await page.context().newCDPSession(page);
    await cdp.send("DOM.enable");
    await cdp.send("CSS.enable");
    const { root } = await cdp.send("DOM.getDocument", { depth: -1 });
    const attr = (node, key) => {
      const at = (node.attributes || []).indexOf(key);
      return at >= 0 && at % 2 === 0 ? node.attributes[at + 1] : "";
    };
    const runs = [];
    let slide = 0;
    const walk = (node, parent, inSlide) => {
      const isSlide = node.nodeName === "SECTION" && attr(node, "class").split(/\s+/).includes("slide");
      if (isSlide) slide += 1;
      if (node.nodeType === 3 && inSlide && node.nodeValue.trim()) runs.push({ nodeId: node.nodeId, slide, parent, text: node.nodeValue.trim().replace(/\s+/g, " ") });
      for (const child of node.children || []) walk(child, node, inSlide || isSlide);
    };
    walk(root, null, false);
    const glyphs = new Map();
    const mixed = [];
    for (const run of runs) {
      const { fonts } = await cdp.send("CSS.getPlatformFontsForNode", { nodeId: run.nodeId });
      const byFamily = new Map();
      for (const font of fonts) if (font.glyphCount > 0) byFamily.set(font.familyName, (byFamily.get(font.familyName) || 0) + font.glyphCount);
      for (const [family, count] of byFamily) glyphs.set(family, (glyphs.get(family) || 0) + count);
      if (byFamily.size < 2) continue;
      const { computedStyle } = await cdp.send("CSS.getComputedStyleForNode", { nodeId: run.parent.nodeId });
      const stack = ((computedStyle.find((p) => p.name === "font-family") || {}).value || "").split(",").map((n) => n.trim().replace(/^['"]|['"]$/g, "").toLowerCase());
      const named = new Set(stack.flatMap((n) => [n, ...(LOCALS.get(n) || [])]));
      const strangers = [...new Set(fonts.filter((f) => f.glyphCount > 0 && !f.isCustomFont && !named.has(f.familyName.toLowerCase()) && !named.has((f.postScriptName || "").toLowerCase())).map((f) => f.familyName))];
      if (!strangers.length) continue;
      const cls = attr(run.parent, "class").trim();
      mixed.push({ slide: run.slide, kind: "fallback", what: `${run.parent.nodeName.toLowerCase()}${cls ? "." + cls.split(/\s+/).join(".") : ""} "${run.text.slice(0, 40)}" partly in ${strangers.join(" and ")}, which its stack (${stack.slice(0, 3).join(", ")}, ...) does not name` });
    }
    await cdp.detach();
    return { faces: [...glyphs].sort((x, y) => y[1] - x[1]).map(([family, count]) => ({ family, glyphs: count })), mixed };
  } catch {
    return { faces: null, mixed: [] };
  }
}

const browser = await launch();
const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "networkidle" });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(300);
const { slides, findings, fonts } = await page.evaluate(MEASURE);
if (!slides.length) {
  await browser.close();
  stop('no <section class="slide"> in the deck');
}

const style = houseStyle();
slides.forEach((slide, i) => {
  const n = i + 1;
  if (!slide.pattern) findings.push({ slide: n, kind: "pattern", what: "no data-pattern on the slide" });
  else if (i && slide.pattern === slides[i - 1].pattern) findings.push({ slide: n, kind: "repeat", what: `"${slide.pattern}" as on slide ${i}` });
  const around = (at, len) => slide.text.slice(Math.max(0, at - 20), at + len + 20).replace(/\s+/g, " ").trim();
  for (const ch of new Set(slide.text)) if (style.forbidden[ch]) findings.push({ slide: n, kind: "style", what: `${style.forbidden[ch]} (${ch}) in "${around(slide.text.indexOf(ch), 1)}"` });
  if (style.brackets) for (const line of slide.text.split("\n")) if (line.trim().startsWith("[")) findings.push({ slide: n, kind: "style", what: `bracketed head "${line.trim().slice(0, 40)}"` });
  for (const phrase of meta.banned || []) if (phrase && slide.text.includes(phrase)) findings.push({ slide: n, kind: "banned", what: `"${phrase}" in "${around(slide.text.indexOf(phrase), phrase.length)}"` });
});
const { faces, mixed } = await facesUsed(page);

await page.pdf({ path: join(outDir, `${name}.pdf`), width: `${width}px`, height: `${height}px`, printBackground: true, preferCSSPageSize: true });
// Every slide is shot until two shots in a row are the same image: a first shot of a slide far down a long page
// can come out part painted, and the next one whole.
const painted = () => page.evaluate(() => new Promise((done) => requestAnimationFrame(() => requestAnimationFrame(done))));
const shots = [];
for (let i = 0; i < slides.length; i++) {
  const file = `${String(i + 1).padStart(2, "0")}.png`;
  const slide = page.locator("section.slide").nth(i);
  await slide.scrollIntoViewIfNeeded();
  await painted();
  let shot = await slide.screenshot();
  let same = false;
  for (let tries = 0; tries < 4 && !same; tries++) {
    const again = await slide.screenshot();
    same = again.equals(shot);
    shot = again;
  }
  if (!same) findings.push({ slide: i + 1, kind: "unstable", what: "its image differed from one shot to the next, five shots in a row" });
  writeFileSync(join(pagesDir, file), shot);
  shots.push(file);
}
findings.sort((a, b) => a.slide - b.slide);

// The contact sheet: the page PNGs three to a row, numbered, taken as one screenshot.
const tile = 640;
const sheetHtml = join(pagesDir, "sheet.html");
writeFileSync(sheetHtml, `<!doctype html><meta charset="utf-8"><style>body{margin:0;padding:16px;background:#2b2f36;display:grid;grid-template-columns:repeat(3,${tile}px);gap:16px;width:max-content}
figure{margin:0;position:relative}img{display:block;width:${tile}px}b{position:absolute;left:0;top:0;padding:4px 10px;background:#000;color:#fff;font:600 16px sans-serif}</style>
${shots.map((file, i) => `<figure><img src="${file}"><b>${i + 1}</b></figure>`).join("\n")}`, "utf8");
const sheet = await browser.newPage({ viewport: { width: tile * 3 + 64, height: 400 }, deviceScaleFactor: 1 });
await sheet.goto(pathToFileURL(sheetHtml).href, { waitUntil: "networkidle" });
await sheet.screenshot({ path: join(outDir, "sheet.png"), fullPage: true });
await browser.close();
rmSync(sheetHtml);

writeFileSync(join(outDir, "report.json"), JSON.stringify({ slides: slides.length, canvas: [width, height], fonts, faces, house_style: style.label, findings, notes: mixed }, null, 2), "utf8");
console.log(`${slides.length} slides at ${width}x${height}; fonts loaded: ${fonts.join(", ") || "none (system fallback)"}; house style: ${style.label}`);
if (faces) console.log(`faces that rendered the text: ${faces.map((f) => `${f.family} (${f.glyphs} glyphs)`).join(", ") || "none"}`);
console.log(`${htmlPath}\n${join(outDir, `${name}.pdf`)}\n${join(outDir, "sheet.png")}\n${pagesDir}`);
for (const f of findings) console.log(`  slide ${f.slide} ${f.kind}: ${f.what}`);
for (const m of mixed.slice(0, 12)) console.log(`  slide ${m.slide} note, fallback: ${m.what}`);
if (mixed.length > 12) console.log(`  and ${mixed.length - 12} more notes in report.json`);
console.log(`${findings.length} findings${mixed.length ? `, ${mixed.length} notes` : ""}`);
process.exit(findings.length ? 1 : 0);
