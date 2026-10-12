// Text runs with sizes and positions, a render of every page, the embedded images, and
// transparent margins for a crop, from one PDF. An example, not a dependency: the skill
// works without it. Run from the scratch folder where `npm install pdfjs-dist @napi-rs/canvas`
// has been done, with Node.js 20 or newer:
//
//   node pdf_extract.example.mjs <document.pdf> [renderWidthPx]   text.json and page-<n>.png
//   node pdf_extract.example.mjs --images <document.pdf>          img-p<page>-<i>.png, the embedded images
//   node pdf_extract.example.mjs --transparent <crop.png> [out.png]   margins flood-filled to transparent
//
// The library's names below are those of pdfjs-dist at the time of writing (checked 2026-10);
// when they change, read its own documentation for the equivalents.
import { getDocument, OPS } from 'pdfjs-dist/legacy/build/pdf.mjs';
import { createCanvas, loadImage, ImageData } from '@napi-rs/canvas';
import fs from 'node:fs';

const args = process.argv.slice(2);
const mode = args[0]?.startsWith('--') ? args.shift() : '--text';
const [file, extra] = args;
if (!file) { console.error('usage: see the header of this script'); process.exit(1); }

const openPdf = () => getDocument({
  data: new Uint8Array(fs.readFileSync(file)),
  cMapUrl: 'node_modules/pdfjs-dist/cmaps/', cMapPacked: true,
  standardFontDataUrl: 'node_modules/pdfjs-dist/standard_fonts/',
}).promise;

if (mode === '--text') {
  const renderWidth = Number(extra) || 1600;
  const pdf = await openPdf();
  const pages = [];
  for (let p = 1; p <= pdf.numPages; p++) {
    const page = await pdf.getPage(p);
    const vp = page.getViewport({ scale: 1 });
    const tc = await page.getTextContent();
    const runs = tc.items.filter((i) => i.str !== undefined).map((i) => ({
      str: i.str,
      x: +i.transform[4].toFixed(1),
      y: +(vp.height - i.transform[5]).toFixed(1),          // from the top
      size: +Math.hypot(i.transform[0], i.transform[1]).toFixed(1),
      font: tc.styles[i.fontName]?.fontFamily,
      width: +i.width.toFixed(1),
      eol: Boolean(i.hasEOL),
    }));
    pages.push({ page: p, width: vp.width, height: vp.height, runs });

    const v2 = page.getViewport({ scale: renderWidth / vp.width });
    const canvas = createCanvas(Math.round(v2.width), Math.round(v2.height));
    await page.render({ canvasContext: canvas.getContext('2d'), viewport: v2 }).promise;
    fs.writeFileSync(`page-${p}.png`, canvas.toBuffer('image/png'));
  }
  fs.writeFileSync('text.json', JSON.stringify(pages, null, 1));
  console.log(`pages ${pdf.numPages}`);
}

if (mode === '--images') {
  const pdf = await openPdf();
  for (let p = 1; p <= pdf.numPages; p++) {
    const page = await pdf.getPage(p);
    const ops = await page.getOperatorList();
    let idx = 0;
    for (let i = 0; i < ops.fnArray.length; i++) {
      if (ops.fnArray[i] !== OPS.paintImageXObject && ops.fnArray[i] !== OPS.paintInlineImageXObject) continue;
      const name = ops.argsArray[i][0];
      let img;
      try { img = page.objs.get(name); } catch { try { img = page.commonObjs.get(name); } catch { continue; } }
      if (!img?.width) continue;
      const n = img.width * img.height;
      let rgba;
      if (img.data.length === n * 4) rgba = new Uint8ClampedArray(img.data);
      else if (img.data.length === n * 3) { rgba = new Uint8ClampedArray(n * 4); for (let k = 0, j = 0; k < img.data.length; k += 3, j += 4) { rgba[j] = img.data[k]; rgba[j + 1] = img.data[k + 1]; rgba[j + 2] = img.data[k + 2]; rgba[j + 3] = 255; } }
      else if (img.data.length === n) { rgba = new Uint8ClampedArray(n * 4); for (let k = 0, j = 0; k < n; k++, j += 4) { rgba[j] = rgba[j + 1] = rgba[j + 2] = img.data[k]; rgba[j + 3] = 255; } }
      else { console.log(`skip ${name}: unknown pixel format`); continue; }
      const canvas = createCanvas(img.width, img.height);
      canvas.getContext('2d').putImageData(new ImageData(rgba, img.width, img.height), 0, 0);
      const out = `img-p${p}-${idx++}.png`;
      fs.writeFileSync(out, canvas.toBuffer('image/png'));
      console.log(`${out} ${img.width}x${img.height}`);
    }
  }
}

if (mode === '--transparent') {
  // Pixels reachable from the border through near-background (light) pixels become transparent;
  // the subject, enclosed by its own darker outline, stays. Adjust `light` for a dark page.
  const img = await loadImage(file);
  const w = img.width, h = img.height;
  const canvas = createCanvas(w, h); const ctx = canvas.getContext('2d'); ctx.drawImage(img, 0, 0);
  const d = ctx.getImageData(0, 0, w, h); const px = d.data;
  const light = (k) => px[k] > 200 && px[k + 1] > 200 && px[k + 2] > 200;
  const seen = new Uint8Array(w * h); const stack = [];
  for (let x = 0; x < w; x++) stack.push(x, (h - 1) * w + x);
  for (let y = 0; y < h; y++) stack.push(y * w, y * w + w - 1);
  let cleared = 0;
  while (stack.length) {
    const p = stack.pop(); if (seen[p]) continue; seen[p] = 1;
    const k = p * 4; if (!light(k)) continue;
    px[k + 3] = 0; cleared++;
    const x = p % w, y = (p - x) / w;
    if (x > 0) stack.push(p - 1); if (x < w - 1) stack.push(p + 1);
    if (y > 0) stack.push(p - w); if (y < h - 1) stack.push(p + w);
  }
  ctx.putImageData(d, 0, 0);
  const out = extra || file.replace(/\.png$/i, '') + '-t.png';
  fs.writeFileSync(out, canvas.toBuffer('image/png'));
  console.log(`${out} transparent px: ${cleared}`);
}
