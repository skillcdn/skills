# Renders every look-*.html in a folder at a desktop width and a phone width with a headless Chromium
# (Playwright for Python, launched as docs/browser/headless.md says) and tiles the desktop screens into
# one contact sheet, out/sheet.png, the name under each, two per row at a third of their size.
# Usage: python shoot.example.py <folder> [desktop width] [desktop height] [--no-phone]   (defaults 1440 by
# 900; the phone width is 390 by 844). A slide or a post passes its own size and --no-phone, since it has
# no phone screen. The browser is an installed Chrome, then Edge, then Playwright's own Chromium.
import glob
import os
import sys

from playwright.sync_api import sync_playwright

args = [a for a in sys.argv[1:] if not a.startswith("--")]
folder = args[0]
width = int(args[1]) if len(args) > 1 else 1440
height = int(args[2]) if len(args) > 2 else 900
phone = "--no-phone" not in sys.argv  # a page gets a phone screen; a slide or a post at its own size passes --no-phone
looks = sorted(glob.glob(os.path.join(folder, "look-*.html")))
out = os.path.join(folder, "out")
os.makedirs(out, exist_ok=True)
names = [os.path.splitext(os.path.basename(p))[0] for p in looks]


def shoot(page, path, file, w, h):
    page.goto("file:///" + os.path.abspath(path).replace("\\", "/"))
    page.wait_for_load_state("networkidle")
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(300)
    page.screenshot(path=file, clip={"x": 0, "y": 0, "width": w, "height": h})


def launch(p):
    for channel in ("chrome", "msedge", None):
        try:
            return p.chromium.launch(channel=channel) if channel else p.chromium.launch()
        except Exception:
            continue
    raise SystemExit("no Chromium-family browser found: install Chrome or Edge, or run playwright install chromium (a download; ask first)")


with sync_playwright() as p:
    browser = launch(p)
    sizes = [(width, height, "desktop")] + ([(390, 844, "phone")] if phone else [])
    for w, h, tag in sizes:
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        for path, name in zip(looks, names):
            shoot(page, path, os.path.join(out, f"{name}-{tag}.png"), w, h)
            print("wrote", name, tag)
        page.close()
    tile_w, tile_h = width // 3, height // 3
    tiles = "".join(f'<figure><img src="out/{n}-desktop.png"><figcaption>{n}</figcaption></figure>' for n in names)
    sheet = os.path.join(folder, "sheet.html")
    with open(sheet, "w", encoding="utf-8") as f:
        f.write("<!doctype html><meta charset='utf-8'><style>body{margin:0;background:#111;padding:16px;font:14px sans-serif;color:#ddd}"
                f".g{{display:grid;grid-template-columns:repeat(2,{tile_w}px);gap:16px}}figure{{margin:0}}img{{display:block;width:{tile_w}px;height:{tile_h}px;object-fit:cover}}"
                "figcaption{padding:6px 0}</style><div class='g'>" + tiles + "</div>")
    page = browser.new_page(viewport={"width": tile_w * 2 + 48, "height": 400}, device_scale_factor=1)
    page.goto("file:///" + os.path.abspath(sheet).replace("\\", "/"))
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(out, "sheet.png"), full_page=True)
    print("wrote sheet")
    browser.close()
