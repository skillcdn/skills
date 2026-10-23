// Renders every slide of the served page (?slide=N) to a PNG at the canvas size, in ./out next to this file.
// Usage: node export.example.mjs
//   BASE     the served page, default http://localhost:8787/
//   SLIDES   how many slides, default 7
//   PREFIX   file name prefix, default "slide"  ->  out/slide-01.png ...
//   WIDTH, HEIGHT  the canvas, default 1080 x 1350
//   PLAYWRIGHT_FROM  a package.json of a project that has playwright-core installed, to borrow it;
//                    else playwright-core is resolved from this folder (npm install playwright-core).
import { createRequire } from "node:module";
import { mkdirSync } from "node:fs";
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
mkdirSync(outDir, { recursive: true });

async function launch() {
  // An installed browser by channel first; playwright-core's own Chromium last, where one is installed.
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
for (let n = 1; n <= count; n++) {
  await page.goto(`${base}?slide=${n}`, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  const file = join(outDir, `${prefix}-${String(n).padStart(2, "0")}.png`);
  await page.screenshot({ path: file, clip: { x: 0, y: 0, width, height } });
  console.log("wrote", file);
}
await browser.close();
