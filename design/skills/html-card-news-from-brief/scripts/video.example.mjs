// Video for a slide, with ffmpeg alone: reads a video's size and length, draws a frame sheet, cuts a muted
// clip with its first frame as the poster, and lays a clip into an exported slide.
// Usage: node video.example.mjs probe <file | url>
//        node video.example.mjs sheet <file | url> <sheet.jpg> [--step=<seconds between frames>]
//        node video.example.mjs cut <file | url> <clip.mp4> --from=<s> --to=<s> [--crop=w:h:x:y] [--height=1350] [--width=<px>] [--crf=22]
//   FFMPEG  the ffmpeg binary, else "ffmpeg" on the path
// cut writes <clip>.mp4 (H.264, no sound) and <clip>-poster.jpg and prints JSON for the brief's two entries.
// export.example.mjs imports composeSlide and sheet for a slide whose picture carries data-video.
import { spawnSync } from "node:child_process";
import { statSync } from "node:fs";
import { pathToFileURL } from "node:url";

const bin = process.env.FFMPEG || "ffmpeg";
const even = (v) => Math.floor(v / 2) * 2;

export function hasFfmpeg() {
  try {
    return spawnSync(bin, ["-version"], { stdio: "ignore", windowsHide: true }).status === 0;
  } catch {
    return false;
  }
}

// The arguments go to ffmpeg as an array, never through a shell line, which loses a filter's commas and quotes.
export function ffmpeg(args, allowFail = false) {
  const r = spawnSync(bin, ["-hide_banner", "-nostdin", ...args], { encoding: "utf8", windowsHide: true, maxBuffer: 1 << 26 });
  if (r.error) throw new Error(`ffmpeg not found (${bin}): put it on the path or set FFMPEG`);
  if (r.status !== 0 && !allowFail) throw new Error("ffmpeg failed: " + String(r.stderr).trim().split("\n").slice(-3).join(" | "));
  return r;
}

// Size, length and sound from what `ffmpeg -i` prints, so that ffprobe is not needed.
export function probe(src) {
  const text = String(ffmpeg(["-i", src], true).stderr || "");
  const v = text.match(/Stream #\d+:\d+.*?: Video: (\w+).*?, (\d{2,5})x(\d{2,5})/);
  if (!v) return null;
  const d = text.match(/Duration: (\d+):(\d+):([\d.]+)/);
  return { codec: v[1], width: +v[2], height: +v[3], duration: d ? d[1] * 3600 + d[2] * 60 + +d[3] : null, audio: /Stream #\d+:\d+.*?: Audio:/.test(text) };
}

// One image of the whole video: frame k, left to right and top to bottom, is at k * step seconds.
export function sheet(src, out, { step, width = 240, cols = 8 } = {}) {
  const d = probe(src)?.duration || 0;
  const every = Number(step) || Math.max(1, Math.ceil(d / 40));
  const frames = Math.max(1, Math.floor(d / every) + 1);
  ffmpeg(["-y", "-i", src, "-vf", `fps=1/${every},scale=${width}:-2,tile=${cols}x${Math.ceil(frames / cols)}:padding=4`, "-frames:v", "1", "-q:v", "4", "-update", "1", out]);
  return { sheet: out, step: every, frames };
}

export function cut(src, out, { from, to, crop, height = 1350, width = 0, crf = 22 }) {
  const meta = probe(src);
  if (!meta) throw new Error(`no video ffmpeg can read at ${src}`);
  const seconds = Number(to) - Number(from);
  if (!(seconds > 0)) throw new Error("--from and --to are seconds of the source, --to the later");
  const filters = [];
  let [w, h] = [meta.width, meta.height];
  if (crop) {
    [w, h] = String(crop).split(":").map(Number);
    filters.push(`crop=${crop}`);
  }
  const shrink = Math.min(1, height / h, width > 0 ? width / w : 1);
  filters.push(`scale=${even(w * shrink)}:${even(h * shrink)}:flags=lanczos`);
  ffmpeg(["-y", "-ss", String(from), "-t", String(seconds), "-i", src, "-vf", filters.join(","), "-an", "-c:v", "libx264", "-preset", "slow", "-crf", String(crf), "-maxrate", "8M", "-bufsize", "16M", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]);
  // HD video is BT.709 and a JPEG is BT.601 full range: convert, or the poster's colours shift.
  const made = probe(out);
  const poster = out.replace(/\.mp4$/i, "") + "-poster.jpg";
  const toJpeg = made.height >= 720 ? "scale=in_color_matrix=bt709:out_color_matrix=bt601:out_range=full,format=yuvj420p" : "format=yuvj420p";
  ffmpeg(["-y", "-i", out, "-frames:v", "1", "-vf", toJpeg, "-q:v", "2", "-update", "1", poster]);
  const px = { w: made.width, h: made.height };
  return { clip: { file: out, source_kind: "video-clip", from: Number(from), to: Number(to), seconds: made.duration, px }, poster: { file: poster, source_kind: "video-frame", poster_of: out, px }, bytes: statSync(out).size };
}

// One slide as mp4: the slide's PNG, the clip laid over the picture's box as CSS lays the poster there
// (object-fit: cover at the object position), then the part of the overlay PNG that covers that box, which is
// everything the slide draws over its picture on a transparent ground. Composited in planar RGB and converted
// once at the end, or a box's colour shifts; an HD clip with no colour tag is read as BT.709, as a browser reads it.
export function composeSlide({ clip, base, overlay, rect, focus, out, fps = 30, crf = 23 }) {
  const m = probe(clip), page = probe(base);
  if (!m || !page) throw new Error(`cannot read ${m ? base : clip}`);
  const x0 = Math.max(0, Math.round(rect.x)), y0 = Math.max(0, Math.round(rect.y));
  const r = { x: x0, y: y0, w: Math.min(page.width - x0, Math.round(rect.w)), h: Math.min(page.height - y0, Math.round(rect.h)) };
  const [fx, fy] = String(focus || "50% 50%").split(/\s+/).map((s) => (/%$/.test(s) ? Math.min(1, Math.max(0, parseFloat(s) / 100)) : 0.5));
  const fit = Math.max(r.w / m.width, r.h / m.height);
  const sw = Math.max(r.w, Math.ceil(m.width * fit)), sh = Math.max(r.h, Math.ceil(m.height * fit));
  const matrix = m.height >= 720 ? ":in_color_matrix=bt709" : "";
  const graph = [
    `[0:v]scale=${sw}:${sh}:flags=lanczos${matrix},crop=${r.w}:${r.h}:${Math.round((sw - r.w) * fx)}:${Math.round((sh - r.h) * (fy ?? 0.5))},setsar=1,fps=${fps},format=gbrp[pic]`,
    `[1:v]format=gbrp[page]`,
    `[page][pic]overlay=${r.x}:${r.y}:format=gbrp:shortest=1[under]`,
    `[2:v]crop=${r.w}:${r.h}:${r.x}:${r.y}[over]`,
    `[under][over]overlay=${r.x}:${r.y}:format=gbrp[rgb]`,
    `[rgb]scale=out_color_matrix=bt709:out_range=limited,format=yuv420p[v]`,
  ].join(";");
  ffmpeg(["-y", "-i", clip, "-loop", "1", "-framerate", String(fps), "-i", base, "-i", overlay, "-filter_complex", graph, "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", String(crf), "-maxrate", "6M", "-bufsize", "12M", "-profile:v", "high", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", out]);
  return { ...probe(out), rect: r };
}

if (import.meta.url === pathToFileURL(process.argv[1] || "").href) {
  const [command, ...rest] = process.argv.slice(2);
  const args = rest.filter((a) => !a.startsWith("--"));
  const opt = Object.fromEntries(rest.filter((a) => a.startsWith("--")).map((a) => a.slice(2).split("=")));
  const run = { probe: () => probe(args[0]), sheet: () => sheet(args[0], args[1], opt), cut: () => cut(args[0], args[1], opt) }[command];
  if (!run || !args[0]) {
    console.log("usage: node video.example.mjs probe <src> | sheet <src> <sheet.jpg> [--step=5] | cut <src> <clip.mp4> --from=12 --to=18 [--crop=w:h:x:y] [--height=1350] [--width=1080]");
    process.exit(1);
  }
  console.log(JSON.stringify(run(), null, 2));
}
