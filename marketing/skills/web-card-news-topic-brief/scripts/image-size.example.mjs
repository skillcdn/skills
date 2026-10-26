// Prints the pixel size of image files: JPEG (the first frame header), PNG (IHDR) and WebP (VP8, VP8L, VP8X).
// Usage: node image-size.example.mjs img/*.jpg img/*.png
import { readFileSync } from "node:fs";

function size(buffer) {
  // PNG: 8-byte signature, then the IHDR chunk with width and height.
  if (buffer.length > 24 && buffer.readUInt32BE(0) === 0x89504e47) {
    return { w: buffer.readUInt32BE(16), h: buffer.readUInt32BE(20), type: "png" };
  }
  // JPEG: walk the markers to the first start-of-frame (C0..CF except C4, C8, CC).
  if (buffer[0] === 0xff && buffer[1] === 0xd8) {
    let i = 2;
    while (i < buffer.length) {
      if (buffer[i] !== 0xff) { i++; continue; }
      const marker = buffer[i + 1];
      if (marker >= 0xc0 && marker <= 0xcf && marker !== 0xc4 && marker !== 0xc8 && marker !== 0xcc) {
        return { w: buffer.readUInt16BE(i + 7), h: buffer.readUInt16BE(i + 5), type: "jpeg" };
      }
      i += 2 + buffer.readUInt16BE(i + 2);
    }
  }
  // WebP: RIFF....WEBP, then a VP8 (lossy), VP8L (lossless) or VP8X (extended) chunk.
  if (buffer.length > 30 && buffer.toString("ascii", 0, 4) === "RIFF" && buffer.toString("ascii", 8, 12) === "WEBP") {
    const chunk = buffer.toString("ascii", 12, 16);
    if (chunk === "VP8 ") return { w: buffer.readUInt16LE(26) & 0x3fff, h: buffer.readUInt16LE(28) & 0x3fff, type: "webp" };
    if (chunk === "VP8L") {
      const b = buffer.readUInt32LE(21);
      return { w: (b & 0x3fff) + 1, h: ((b >> 14) & 0x3fff) + 1, type: "webp" };
    }
    if (chunk === "VP8X") return { w: buffer.readUIntLE(24, 3) + 1, h: buffer.readUIntLE(27, 3) + 1, type: "webp" };
  }
  return null;
}

for (const file of process.argv.slice(2)) {
  const s = size(readFileSync(file));
  console.log(s ? `${file}\t${s.w}x${s.h}\t${s.type}` : `${file}\tunknown format`);
}
