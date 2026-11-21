// Renders every slide of the served page (?slide=N) to a PNG at the canvas size, in ./out next to this file.
// Usage: node export.example.mjs
//   BASE     the served page, default http://localhost:8787/
//   SLIDES   how many slides, default 7
//   PREFIX   file name prefix, default "slide"  ->  out/slide-01.png ...
//   WIDTH, HEIGHT  the canvas, default 1080 x 1350
//   PLAYWRIGHT_FROM  a package.json of a project that has playwright-core installed, to borrow it;
//                    else playwright-core is resolved from this folder (npm install playwright-core).
// A video slide (its picture is an img with data-video, the clip's path from this folder; the img shows the
// poster) also gets out/<prefix>-NN.mp4, the clip where the picture is with everything the slide draws over
// it, and out/video/<prefix>-NN.jpg, one frame a second of that mp4. It takes ffmpeg and video.example.mjs
// beside this file; without ffmpeg the PNG with the poster stands and a line says so.
import { createRequire } from "node:module";
import { mkdirSync, rmSync } from "node:fs";
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

async function open(page, query) {
  await page.goto(`${base}${query}`, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
}

const clipBox = { x: 0, y: 0, width, height };
const browser = await launch();
const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
for (let n = 1; n <= count; n++) {
  const name = `${prefix}-${String(n).padStart(2, "0")}`;
  await open(page, `?slide=${n}`);
  const png = join(outDir, `${name}.png`);
  await page.screenshot({ path: png, clip: clipBox });
  console.log("wrote", png);
  const video = await page.evaluate(() => {
    const img = document.querySelector(".stage .slide img[data-video]");
    if (!img) return null;
    const b = img.getBoundingClientRect();
    return { clip: img.dataset.video, focus: getComputedStyle(img).objectPosition, rect: { x: b.left, y: b.top, w: b.width, h: b.height } };
  });
  if (!video) continue;
  const { composeSlide, sheet, hasFfmpeg } = await import("./video.example.mjs").catch(() => ({ hasFfmpeg: () => false }));
  if (!hasFfmpeg()) {
    console.log(`video  slide ${n}: no ffmpeg, or video.example.mjs is not beside this script; the PNG with the poster stands`);
    continue;
  }
  // Everything the slide draws over its picture, on a transparent ground.
  const overlay = join(outDir, `.overlay-${name}.png`);
  await open(page, `?slide=${n}&overlay=1`);
  await page.screenshot({ path: overlay, omitBackground: true, clip: clipBox });
  const mp4 = join(outDir, `${name}.mp4`);
  const made = composeSlide({ clip: join(here, video.clip), base: png, overlay, rect: video.rect, focus: video.focus, out: mp4 });
  rmSync(overlay);
  mkdirSync(join(outDir, "video"), { recursive: true });
  sheet(mp4, join(outDir, "video", `${name}.jpg`), { step: 1, width: 360, cols: 4 });
  console.log(`wrote ${mp4} (${made.duration?.toFixed(1)}s${made.audio ? ", SOUND LEFT IN" : ""}) and out/video/${name}.jpg`);
}
await browser.close();
