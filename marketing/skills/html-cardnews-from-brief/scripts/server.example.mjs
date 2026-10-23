// Serves the post folder (this file's directory) so that the page shows its images in a host's browser pane.
// Usage: node server.example.mjs   (PORT from the environment, else 8787)
// A host's preview tool that starts servers from a launch configuration assigns the port itself; it is honored.
import { createServer } from "node:http";
import { createReadStream, existsSync, statSync } from "node:fs";
import { dirname, extname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const port = Number(process.env.PORT) || 8787;
const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css",
  ".js": "text/javascript",
  ".mjs": "text/javascript",
  ".json": "application/json",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".woff2": "font/woff2",
};

createServer((req, res) => {
  let path = decodeURIComponent(req.url.split("?")[0]);
  if (path === "/") path = "/index.html";
  const file = join(root, path);
  if (!file.startsWith(root) || !existsSync(file) || statSync(file).isDirectory()) {
    res.writeHead(404);
    res.end("not found");
    return;
  }
  res.writeHead(200, { "Content-Type": types[extname(file)] || "application/octet-stream", "Cache-Control": "no-store" });
  createReadStream(file).pipe(res);
}).listen(port, () => console.log(`card news preview on http://localhost:${port}`));
