// Saves frames of a public video clip as JPEGs, one every few seconds of video, named by time code, so that
// the frames of a report or footage the articles cite can be chosen for the brief. Reads the public watch
// page only, in a headless browser; no sign-in, nothing downloaded but screenshots.
// Usage: node video-frames.example.mjs <watch URL or video id> <outDir> [interval=3] [rate=2] [start=0] [end]
//   interval  seconds of video between frames      rate   playback rate (2 halves the wall time)
//   start/end seconds of video to cover            PLAYWRIGHT_FROM  a package.json of a project that has
//             playwright-core installed, to borrow it; else playwright-core is resolved from this folder.
// Written against the watch page of the largest video platform (its t= parameter and its player API,
// checked 2026-10). Playback stalled after about a minute at a raised rate, so the page is reloaded at the
// next time code every CHUNK seconds of video. Frames are 1280 by 720 CSS pixels at device scale 1.5,
// which gives 1920 by 1080 files; the served resolution is written to frames.tsv beside them.
import { createRequire } from "node:module";
import { appendFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const require = createRequire(process.env.PLAYWRIGHT_FROM || join(here, "package.json"));
const { chromium } = require("playwright-core");

const [target, outDir, intervalArg, rateArg, startArg, endArg] = process.argv.slice(2);
if (!target || !outDir) {
  console.error("usage: node video-frames.example.mjs <watch URL or video id> <outDir> [interval] [rate] [start] [end]");
  process.exit(1);
}
const interval = Number(intervalArg) || 3;
const rate = Number(rateArg) || 2;
const start = Number(startArg) || 0;
const CHUNK = 50;
const W = 1280, H = 720;
const id = /^[\w-]{6,}$/.test(target) ? target : new URL(target).searchParams.get("v") || new URL(target).pathname.split("/").pop();
const watch = (t) => `https://www.youtube.com/watch?v=${id}&t=${Math.floor(t)}s`;
mkdirSync(outDir, { recursive: true });

async function launch() {
  for (const channel of ["chrome", "msedge", "chromium"]) {
    try {
      return await chromium.launch(channel === "chromium" ? {} : { channel, args: ["--autoplay-policy=no-user-gesture-required"] });
    } catch {
      // try the next one
    }
  }
  throw new Error("no Chromium-family browser found: install Chrome or Edge, or run npx playwright install chromium");
}

const browser = await launch();
const context = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1.5 });
const page = await context.newPage();

// Plays the clip from `from` with the video element pinned over the page; returns the clip's duration.
async function prepare(from) {
  await page.goto(watch(from), { waitUntil: "domcontentloaded" });
  await page.waitForSelector("video", { timeout: 60000 });
  for (let i = 0; i < 120; i++) {
    const state = await page.evaluate(() => {
      const v = document.querySelector("video");
      v.muted = true;
      v.play().catch(() => {});
      const skip = document.querySelector(".ytp-skip-ad-button, .ytp-ad-skip-button, .ytp-ad-skip-button-modern");
      if (skip) skip.click();
      return { ad: !!document.querySelector(".ad-showing"), duration: v.duration, ready: v.readyState };
    });
    if (!state.ad && isFinite(state.duration) && state.duration > 0 && state.ready >= 3) break;
    await page.waitForTimeout(1000);
  }
  return page.evaluate(async ({ from, rate, W, H }) => {
    const player = document.getElementById("movie_player");
    try { player.setPlaybackQualityRange("hd1080", "hd1080"); } catch {}
    try { player.seekTo(Math.max(from, 0.1), true); } catch {}
    const v = document.querySelector("video");
    const backdrop = document.createElement("div");
    backdrop.style.cssText = `position:fixed;left:0;top:0;width:${W}px;height:${H}px;background:#000;z-index:2147483646`;
    document.body.appendChild(backdrop);
    v.style.cssText = `position:fixed!important;left:0!important;top:0!important;width:${W}px!important;height:${H}px!important;z-index:2147483647!important;object-fit:contain!important;transform:none!important`;
    document.body.appendChild(v);
    v.muted = true;
    v.playbackRate = rate;
    await v.play().catch(() => {});
    return player && player.getDuration ? player.getDuration() : v.duration;
  }, { from, rate, W, H });
}

let end = Number(endArg) || Infinity;
let from = start;
let next = start;
let stalls = 0;
let frames = 0;
while (from < end) {
  const duration = await prepare(from);
  if (end === Infinity) { end = duration; console.log("duration", duration); }
  const stop = Math.min(from + CHUNK, end);
  let lastTime = -1, lastMove = Date.now(), reached = false;
  while (true) {
    const state = await page.evaluate(() => {
      const v = document.querySelector("video");
      return { time: v.currentTime, size: `${v.videoWidth}x${v.videoHeight}`, ad: !!document.querySelector(".ad-showing"), ended: v.ended, paused: v.paused };
    });
    if (state.ended || state.time >= stop - 0.3) { reached = true; break; }
    if (state.time !== lastTime) { lastTime = state.time; lastMove = Date.now(); }
    else if (!state.ad && Date.now() - lastMove > 15000) { console.log("stalled at", state.time.toFixed(1)); break; }
    if (state.paused && !state.ad) await page.evaluate(() => document.querySelector("video").play().catch(() => {}));
    if (!state.ad && state.time >= next) {
      const file = join(outDir, `t${String(Math.round(state.time * 10)).padStart(5, "0")}.jpg`);
      await page.screenshot({ path: file, type: "jpeg", quality: 92, clip: { x: 0, y: 0, width: W, height: H } });
      appendFileSync(join(outDir, "frames.tsv"), `${state.time.toFixed(2)}\t${state.size}\t${file}\n`);
      frames++;
      next = state.time + interval;
    }
    await page.waitForTimeout(100);
  }
  if (reached) { from = stop; stalls = 0; }
  else if (lastTime > from + 1) { from = lastTime; stalls = 0; }
  else if (++stalls >= 3) { console.log("gave up at", from); break; }
}
console.log("frames", frames, "in", outDir);
await browser.close();
