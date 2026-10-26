// Saves frames of a public video clip as JPEGs, one every few seconds of video, named by time code, so that
// the frames of a report or footage the articles cite can be chosen for the brief. Reads the public watch
// page only, in a headless browser; no sign-in, nothing downloaded but screenshots.
// Usage: node video-frames.example.mjs <watch URL or video id> <outDir> [interval=3] [rate=1] [start=0] [end]
//   interval  seconds of video between frames      rate   playback rate, 1 by default
//   start/end seconds of video to cover            PLAYWRIGHT_FROM  a package.json of a project that has
//             playwright-core installed, to borrow it; else playwright-core is resolved from this folder.
// Written against the watch page of the largest video platform (its t= parameter, its player API and
// the class name it marks an advertisement with, which drift; checked 2026-10); an advertisement is waited
// out, never skipped. A stall (no progress for fifteen seconds while no
// advertisement shows) is met by one reload at the time reached, as a viewer would; a clip that stalls
// again keeps the frames taken so far. Frames
// are 1280 by 720 CSS pixels at device scale 1.5, which gives 1920 by 1080 files whatever was served;
// frames.tsv beside them holds, per frame, the seconds, the served width by height (the entry's px)
// and the file, appended on every run. File names are tenths of a second: t00120.jpg is 12.0 s.
// A clip of several minutes runs for minutes: run it in the background. "frames 0" with no other line
// means the player never readied (a consent page, a bot check, an age gate): the clip is then listed
// as a source and the frames are not taken. The install hint below downloads a browser; ask first.
import { createRequire } from "node:module";
import { appendFileSync, mkdirSync, unlinkSync } from "node:fs";
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
const rate = Number(rateArg) || 1;
const start = Number(startArg) || 0;
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

// Pins the video element over the page at the box's size and says whether it fills the box. The player
// rewrites the element's inline size when it lays itself out again (a frame then fills two thirds of
// the file, the rest black), so this runs before every capture, not once (checked 2026-10).
const pin = ({ W, H }) => {
  const v = document.querySelector("video");
  const wanted = { position: "fixed", left: "0px", top: "0px", width: `${W}px`, height: `${H}px`, "z-index": "2147483647", "object-fit": "contain", transform: "none" };
  for (const [name, value] of Object.entries(wanted)) {
    if (v.style.getPropertyValue(name) !== value || v.style.getPropertyPriority(name) !== "important") v.style.setProperty(name, value, "important");
  }
  const r = v.getBoundingClientRect();
  return Math.round(r.left) === 0 && Math.round(r.top) === 0 && Math.round(r.width) === W && Math.round(r.height) === H;
};

// Plays the clip from `from` with the video element pinned over the page; returns the clip's duration.
async function prepare(from) {
  await page.goto(watch(from), { waitUntil: "domcontentloaded" });
  await page.waitForSelector("video", { timeout: 60000 });
  for (let i = 0; i < 120; i++) {
    const state = await page.evaluate(() => {
      const v = document.querySelector("video");
      v.muted = true;
      v.play().catch(() => {});
      return { ad: !!document.querySelector(".ad-showing"), duration: v.duration, ready: v.readyState };
    });
    if (!state.ad && isFinite(state.duration) && state.duration > 0 && state.ready >= 3) break;
    await page.waitForTimeout(1000);
  }
  const duration = await page.evaluate(async ({ from, rate, W, H }) => {
    const player = document.getElementById("movie_player");
    try { player.setPlaybackQualityRange("hd1080", "hd1080"); } catch {}
    try { player.seekTo(Math.max(from, 0.1), true); } catch {}
    const v = document.querySelector("video");
    const backdrop = document.createElement("div");
    backdrop.style.cssText = `position:fixed;left:0;top:0;width:${W}px;height:${H}px;background:#000;z-index:2147483646`;
    document.body.appendChild(backdrop);
    document.body.appendChild(v);
    v.muted = true;
    v.playbackRate = rate;
    await v.play().catch(() => {});
    return player && player.getDuration ? player.getDuration() : v.duration;
  }, { from, rate, W, H });
  await page.evaluate(pin, { W, H });
  return duration;
}

let end = Number(endArg) || Infinity;
let from = start;
let next = start;
let reloaded = false;
let frames = 0;
while (from < end) {
  const duration = await prepare(from);
  if (end === Infinity) { end = duration; console.log("duration", duration); }
  const stop = end;
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
      // Pin, shoot, then check that the element still filled the box; a frame shot during a relayout is dropped and retaken.
      if (!(await page.evaluate(pin, { W, H }))) { await page.waitForTimeout(100); continue; }
      const file = join(outDir, `t${String(Math.round(state.time * 10)).padStart(5, "0")}.jpg`);
      await page.screenshot({ path: file, type: "jpeg", quality: 92, clip: { x: 0, y: 0, width: W, height: H } });
      if (!(await page.evaluate(pin, { W, H }))) { unlinkSync(file); continue; }
      appendFileSync(join(outDir, "frames.tsv"), `${state.time.toFixed(2)}\t${state.size}\t${file}\n`);
      frames++;
      next = state.time + interval;
    }
    await page.waitForTimeout(100);
  }
  if (reached) break;
  if (reloaded) { console.log("stalled again at", lastTime.toFixed(1), "- the frames taken so far are kept"); break; }
  reloaded = true;  // one reload, as a viewer would; a second stall ends the capture
  from = Math.max(lastTime, from);
  console.log("reloading once at", from.toFixed(1));
}
console.log("frames", frames, "in", outDir);
await browser.close();
