// Reviews the served page before anyone looks: counts the lines the browser set against data-lines,
// measures every placed block's top and bottom edges in export mode, and writes a phone-size copy of
// every exported PNG, so that the review judges numbers and a phone's view rather than impressions.
// Usage: node review.example.mjs   (from the post folder, after the export)
//   BASE, SLIDES, PREFIX, WIDTH, HEIGHT and PLAYWRIGHT_FROM as for export.example.mjs.
// Markup it reads: every card carries data-n (its slide number), the export mode's stage element has
// the class "stage", every placed block carries data-block (the spec's block name) and every text
// block data-lines (the count the plan placed). Prints "lines ok" or one line per block whose count
// differs; one line per block and slide with its edges as percentages of the canvas; and the path of
// each copy in out/phone/, each PNG shown at a third of its width in a page and screenshotted, since
// Node.js has no image resize of its own.
import { createRequire } from "node:module";
import { existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const require = createRequire(process.env.PLAYWRIGHT_FROM || join(here, "package.json"));
const { chromium } = require("playwright-core");

const base = process.env.BASE || "http://localhost:8787/";
const count = Number(process.env.SLIDES) || 7;
const prefix = process.env.PREFIX || "slide";
const width = Number(process.env.WIDTH) || 1080;
const height = Number(process.env.HEIGHT) || 1350;
const outDir = join(here, "out");
const phoneDir = join(outDir, "phone");
mkdirSync(phoneDir, { recursive: true });
const nn = (n) => String(n).padStart(2, "0");

async function launch() {
  for (const channel of ["chrome", "msedge", "chromium"]) {
    try {
      return await chromium.launch(channel === "chromium" ? {} : { channel });
    } catch {
      // try the next one
    }
  }
  throw new Error("no Chromium-family browser found: install Chrome or Edge, or run npx playwright install chromium");
}

const browser = await launch();
const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });

// 1. Lines, in the served page and not in export mode: the rectangles of the text nodes alone, one row
//    per block whose rendered lines differ from the count the plan placed.
await page.goto(base, { waitUntil: "networkidle" });
await page.evaluate(() => document.fonts.ready);
const lines = await page.evaluate(() =>
  [...document.querySelectorAll(".slide [data-lines]")]
    .map((el) => {
      const tops = new Set();
      const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      for (let node; (node = walk.nextNode()); ) {
        const r = document.createRange();
        r.selectNodeContents(node);
        for (const box of r.getClientRects()) if (box.width) tops.add(Math.round(box.top));
      }
      return { slide: el.closest(".card")?.dataset.n, block: el.dataset.block || el.className, want: +el.dataset.lines, got: tops.size, text: el.innerText.slice(0, 30) };
    })
    .filter((x) => x.got !== x.want));
for (const x of lines) console.log(`lines  slide ${x.slide} ${x.block}: wanted ${x.want}, got ${x.got}  "${x.text}"`);
if (!lines.length) console.log("lines  ok");

// 2. Edges, in export mode: every placed block's top and bottom (and left and right) as percentages of
//    the canvas, to hold against the spec's anatomy; the stage holds the one slide at native size.
for (let n = 1; n <= count; n++) {
  await page.goto(`${base}?slide=${n}`, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  const edges = await page.evaluate(
    ({ width, height }) =>
      [...document.querySelectorAll(".stage .slide [data-block]")].map((el) => {
        const r = el.getBoundingClientRect();
        const pct = (v, of) => Math.round((v / of) * 1000) / 10;
        return { block: el.dataset.block, top: pct(r.top, height), bottom: pct(r.bottom, height), left: pct(r.left, width), right: pct(r.right, width) };
      }),
    { width, height },
  );
  for (const e of edges) console.log(`edges  slide ${nn(n)} ${e.block}: y ${e.top}-${e.bottom}%  x ${e.left}-${e.right}%`);
}

// 3. Phone-size copies: each exported PNG shown at a third of its width and screenshotted.
const w3 = Math.round(width / 3), h3 = Math.round(height / 3);
const phone = await browser.newPage({ viewport: { width: w3, height: h3 }, deviceScaleFactor: 1 });
for (let n = 1; n <= count; n++) {
  const file = join(outDir, `${prefix}-${nn(n)}.png`);
  if (!existsSync(file)) continue;
  const data = "data:image/png;base64," + readFileSync(file).toString("base64");
  await phone.setContent(`<body style="margin:0;background:#000"><img src="${data}" style="display:block;width:${w3}px"></body>`);
  await phone.waitForFunction(() => document.images[0] && document.images[0].complete);
  const out = join(phoneDir, `${prefix}-${nn(n)}.png`);
  await phone.screenshot({ path: out, clip: { x: 0, y: 0, width: w3, height: h3 } });
  console.log("wrote", out);
}
await browser.close();
