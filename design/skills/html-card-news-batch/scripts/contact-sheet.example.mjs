// Tiles a post's slides into one image, <post folder>/out/contact-sheet.png, for each post folder named.
// Usage: node contact-sheet.example.mjs <post folder> [<post folder> ...]
//   Reads <post folder>/out/phone/*.png in name order (the build's review writes them); where there are
//   none, <post folder>/out/*.png, shown at the tile width.
//   COLUMNS  slides per row, default 4
//   TILE     the width of one slide on the sheet in pixels, default 360 (a third of a 1080 canvas)
//   PLAYWRIGHT_FROM  a package.json of a project that has playwright-core installed, to borrow it;
//                    else playwright-core is resolved from this folder (npm install playwright-core).
import { createRequire } from "node:module";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const require = createRequire(process.env.PLAYWRIGHT_FROM || join(here, "package.json"));
const { chromium } = require("playwright-core");

const columns = Number(process.env.COLUMNS) || 4;
const tile = Number(process.env.TILE) || 360;
const folders = process.argv.slice(2);
if (!folders.length) {
  console.log("usage: node contact-sheet.example.mjs <post folder> [<post folder> ...]");
  process.exit(1);
}

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

const pngs = (dir) =>
  existsSync(dir) ? readdirSync(dir).filter((f) => f.endsWith(".png") && f !== "contact-sheet.png").sort().map((f) => join(dir, f)) : [];

const browser = await launch();
const page = await browser.newPage({ viewport: { width: columns * (tile + 12) + 12, height: 600 }, deviceScaleFactor: 1 });
let failed = 0;
for (const folder of folders) {
  const out = join(resolve(folder), "out");
  const phone = pngs(join(out, "phone"));
  const files = phone.length ? phone : pngs(out);
  if (!files.length) {
    console.log("no slides in", out);
    failed++;
    continue;
  }
  const cells = files
    .map((file, i) => {
      const data = "data:image/png;base64," + readFileSync(file).toString("base64");
      return `<figure><img src="${data}"><figcaption>${String(i + 1).padStart(2, "0")}</figcaption></figure>`;
    })
    .join("");
  await page.setContent(
    `<style>body{margin:0;padding:12px;background:#222;display:grid;grid-template-columns:repeat(${columns},${tile}px);gap:12px;width:max-content}` +
      `figure{margin:0}img{display:block;width:${tile}px}figcaption{font:12px sans-serif;color:#ccc;padding-top:4px}</style>${cells}`,
  );
  await page.waitForFunction(() => [...document.images].every((img) => img.complete && img.naturalWidth > 0));
  const sheet = join(out, "contact-sheet.png");
  await page.screenshot({ path: sheet, fullPage: true });
  console.log("wrote", sheet, `(${files.length} slides)`);
}
await browser.close();
if (failed) process.exitCode = 2;
