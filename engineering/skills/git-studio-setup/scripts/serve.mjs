// Serves the repository on this machine so that the gallery and the items' pages open in a browser:
// http://localhost:<port>/gallery/, built again on every visit, nothing cached. Ctrl+C stops it.
// Usage: node scripts/serve.mjs [--port=8787]   (a port in use gives way to a free one)
import { createReadStream, existsSync, readdirSync, statSync } from "node:fs";
import { createServer } from "node:http";
import { extname, join, normalize } from "node:path";
import { buildGallery } from "./gallery.mjs";
import { args, root } from "./studio.mjs";

const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".mjs": "text/javascript", ".json": "application/json", ".md": "text/plain; charset=utf-8", ".txt": "text/plain; charset=utf-8", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".svg": "image/svg+xml", ".mp4": "video/mp4", ".webm": "video/webm" };
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

const server = createServer((req, res) => {
  const path = decodeURIComponent(new URL(req.url, "http://localhost").pathname);
  const send = (code, type, body) => { res.writeHead(code, { "content-type": type, "cache-control": "no-store" }); res.end(body); };
  if (path === "/") { res.writeHead(302, { location: "/gallery/" }); return res.end(); }
  if (path === "/gallery/" || path === "/gallery/index.html") { try { buildGallery(); } catch (e) { return send(500, "text/plain", String(e)); } }
  let file = normalize(join(root, path));
  if (!file.startsWith(root)) return send(403, "text/plain", "outside the repository");
  if (existsSync(file) && statSync(file).isDirectory()) {
    if (!path.endsWith("/")) { res.writeHead(302, { location: `${path}/` }); return res.end(); }
    if (existsSync(join(file, "index.html"))) file = join(file, "index.html");
    else return send(200, TYPES[".html"], `<meta charset="utf-8"><ul>${readdirSync(file).map((n) => `<li><a href="${encodeURIComponent(n)}">${esc(n)}</a>`).join("")}</ul>`);
  }
  if (!existsSync(file)) return send(404, "text/plain", "not found");
  res.writeHead(200, { "content-type": TYPES[extname(file).toLowerCase()] ?? "application/octet-stream", "cache-control": "no-store" });
  createReadStream(file).pipe(res);
});

const port = Number(args().options.port) || Number(process.env.PORT) || 8787;
const listen = (p) => server.listen(p, "127.0.0.1", () => console.log(`http://localhost:${server.address().port}/gallery/`));
server.on("error", (e) => { if (e.code === "EADDRINUSE") { console.error(`port ${port} is in use; taking a free one`); listen(0); } else throw e; });
listen(port);
