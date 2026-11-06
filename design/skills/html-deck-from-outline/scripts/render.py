# -*- coding: utf-8 -*-
"""Render a deck file (see ../references/deck-spec.md) to one HTML file, print it to PDF, measure it, tile it.

Usage:
  python render.py <deck.json> <out.html> [--pdf <out.pdf>] [--report <out.json>] [--sheet <out.png>]
                   [--page <n> <page.png>] [--fill <ratio>] [--route python|node|bare] [--no-check]
  python render.py <deck.json> <look.html> --look <look.png> [--look-slide <index>] [--route ...]

- One slide is one 13.333in x 7.5in page, on screen and in print. meta.register picks the frame: "proposal" (a light
  gradient, an accent bar beside the title, a page number) or "report" (white pages, a section label above the title,
  a rule under the header, a footer with the brand, the document name, the date and the page number).
- Cover: proposal, two title lines, a tagline, the client's and the presenter's logos, four stripes; report, a navy
  panel with the kind label, the title, the tagline and the meta rows, a supplied photograph or the stripes at the right.
  Closing: a dark page with the thanks line, the white logo and the contact lines.
- Blocks: columns / statement / facts / numbered / toc / table / kpi / photo / loop / brand / rows / steps / diagram /
  gantt / profiles / timeline / stack / cards / banner / stats / bullets / qa / shots / split / note. Every block's root
  carries data-path ($.slides[3].blocks[0]) and every slide data-slide, which the layout report names findings by.
- Line icons (ICONS) exist for the rare item whose meaning a word does not carry; a named product gets its real logo.
- When meta.external is true, the strings of meta and slides are checked against meta.style before rendering; a failure
  lists each string with its path. --no-check renders anyway, for a look at a draft; a delivery never uses it.
- The browser route is the first the host has: Playwright from Python; Node.js with playwright-core (PLAYWRIGHT_FROM,
  or a tools folder in the user's cache, installed there once); the installed browser's own --print-to-pdf and
  --screenshot (no layout report on that route). --route forces one. The route taken is printed.
- --report measures the rendered pages in the browser: overflow, cut text, overlapping texts, a lone word on a last line,
  wrapped values, and a content slide filled under --fill (0.5). --sheet tiles the pages three per row, from the PDF
  with PyMuPDF where it is installed, else from the HTML through the browser. --look prints the cover and one body
  slide in both registers on one image, for the plan checkpoint.
- Image paths are resolved relative to the deck file; a path that does not exist prints a warning and draws nothing.
"""
import base64
import html
import json
import math
import os
import pathlib
import re
import shutil
import stat
import subprocess
import sys
import tempfile

DEFAULT_THEME = {
    "navy": "#22408E", "steel": "#7089BF", "accent": None, "ink": "#2A3242", "mute": "#5A6478",
    "tint": "#E7EDFA", "tint2": "#D9E2F6", "line": "#E2E8F5", "pale": "#BFD0EC",
    "rule": "#C9D1E3", "faint": "#8A94A8",
    "font": "Pretendard",
    "font_css": "https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.min.css",
}
SKIP_KEYS = ("logo", "logo_white", "client_logo", "logos", "symbol", "center_logos", "photo", "src", "id", "icon", "font_css")
PAGE_W, PAGE_H = 13.333, 7.5

# Line icons (24x24, stroke = currentColor), for the rare item whose meaning a word does not carry.
ICONS = {
    "file": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h6"/>',
    "layers": '<path d="M12 3 3 7.5l9 4.5 9-4.5z"/><path d="M3 12l9 4.5 9-4.5"/><path d="M3 16.5 12 21l9-4.5"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20.5 20.5 16 16"/>',
    "cpu": '<rect x="5" y="5" width="14" height="14" rx="2"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>',
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    "clipboard": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M9 3v2h6V3"/><path d="M8 10h8M8 14h8M8 18h5"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
    "refresh": '<path d="M21 12a9 9 0 1 1-2.6-6.4"/><path d="M21 3v6h-6"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 15.5A5 5 0 0 1 22 20"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "download": '<path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M4 20h16"/>',
    "laptop": '<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M1 20h22"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/>',
    "edit": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "flag": '<path d="M5 22V4"/><path d="M5 4h12l-2 4 2 4H5"/>',
    "server": '<rect x="3" y="4" width="18" height="6" rx="1.5"/><rect x="3" y="14" width="18" height="6" rx="1.5"/><path d="M7 7h.01M7 17h.01"/>',
}


def _walk_strings(obj, path="$"):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _walk_strings(v, f"{path}[{i}]")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in SKIP_KEYS:
                continue
            yield from _walk_strings(v, f"{path}.{k}")


def check_style(spec):
    """Return the list of house-style violations (empty when the deck passes)."""
    style = spec.get("meta", {}).get("style", {})
    forbidden = style.get("forbidden", {})
    problems = []
    checked = {"meta": {k: v for k, v in spec.get("meta", {}).items() if k not in ("style", "theme")}, "slides": spec["slides"]}
    for path, s in _walk_strings(checked):
        for chars, name in forbidden.items():
            for ch in chars:  # a key of several characters is a set, each checked
                if ch in s:
                    problems.append(f"{path}: {name} ({ch}) in: {s[:60]}")
                    break
        if style.get("no_bracket_heads") and re.match(r"^\s*\[[^\]]+\]", s):
            problems.append(f"{path}: bracket head in: {s[:60]}")
    return problems


def _e(s):
    return html.escape("" if s is None else str(s), quote=False)


def _luma(hex_color):
    """Relative luminance of a #rrggbb color, 0 (black) to 1 (white)."""
    h = (hex_color or "").lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    try:
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        return 0.5
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


BASE_DIR = ""  # the deck file's folder: image paths are resolved relative to it


def _img_data(path):
    if not path:
        return None
    full = path if os.path.isabs(path) else os.path.join(BASE_DIR, path)
    if not os.path.exists(full):
        print(f"warning: image not found, nothing drawn: {path}", file=sys.stderr)
        return None
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = {"svg": "image/svg+xml", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}.get(ext, "image/png")
    with open(full, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def _img(path, cls="", h=None):
    d = _img_data(path)
    if not d:
        return ""
    hs = f' style="height:{h}in"' if h else ""
    return f'<img class="{cls}" src="{d}"{hs}>'


def _icon(name, size=0.3, extra=""):
    inner = ICONS.get(name or "")
    if not inner:
        return ""
    return (f'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" style="width:{size}in;height:{size}in;{extra}">{inner}</svg>')


def _disc(icon, size=0.3):
    return f'<div class="idisc">{_icon(icon, size)}</div>' if icon else ""


CSS_T = """
@FONT_IMPORT
@page { size: 13.333in 7.5in; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #9aa3b5; }
body { font-family: @FONT, "Malgun Gothic", "Apple SD Gothic Neo", sans-serif; color: @INK; -webkit-print-color-adjust: exact; print-color-adjust: exact; word-break: keep-all; overflow-wrap: break-word; }
.slide { position: relative; width: 13.333in; height: 7.5in; overflow: hidden; margin: 0 auto 0.25in auto; background: linear-gradient(155deg, #FFFFFF 0%, @TINT 100%); page-break-after: always; break-after: page; }
.slide.report { background: #fff; }
.slide:last-child { margin-bottom: 0; }
@media print { body { background: none; } .slide { margin: 0; } }
.content { position: absolute; left: 0.55in; right: 0.55in; top: 0.42in; bottom: 0.45in; display: flex; flex-direction: column; }
.report .content { bottom: 0.55in; }
.header { position: relative; padding-left: 0.18in; margin-bottom: 0.3in; }
.header::before { content: ""; position: absolute; left: 0; top: 0.08in; width: 5.5pt; height: 0.5in; background: @ACCENT; }
.header h1 { margin: 0; font-size: 26pt; font-weight: 700; color: @NAVY; line-height: 1.2; }
.header h2 { margin: 0.1in 0 0 0.02in; font-size: 14pt; font-weight: 400; color: @MUTE; }
.header.rep { padding-left: 0; padding-bottom: 0.14in; border-bottom: 1.5pt solid @NAVY; margin-bottom: 0.28in; }
.header.rep::before { display: none; }
.header.rep .sec { font-size: 10.5pt; font-weight: 700; color: @ACCENT; letter-spacing: 0.08em; margin-bottom: 0.08in; }
.header.rep h1 { font-size: 24pt; }
.hlogo { position: absolute; right: 0; top: 0.06in; height: 0.46in; }
.tag { position: absolute; right: 0; top: 0.1in; background: @NAVY; color: #fff; font-size: 12pt; font-weight: 700; padding: 0.06in 0.3in; border-radius: 999px; }
.body { flex: 1; display: flex; flex-direction: column; gap: 0.26in; min-height: 0; }
.body.center { justify-content: center; padding-bottom: 0.3in; }
.note { position: absolute; left: 0.55in; right: 0.55in; bottom: 0.12in; font-size: 10.5pt; color: @MUTE; line-height: 1.35; }
.pageno { position: absolute; right: 0.5in; bottom: 0.26in; font-size: 9.5pt; color: @FAINT; letter-spacing: 0.05em; }
.footer { position: absolute; left: 0.55in; right: 0.55in; bottom: 0.22in; display: flex; justify-content: space-between; align-items: baseline; font-size: 9pt; color: @FAINT; letter-spacing: 0.03em; }
.footer .fl span + span::before { content: "  |  "; white-space: pre; }
.ic { display: block; flex: none; }
.idisc { flex: none; width: 0.52in; height: 0.52in; border-radius: 50%; background: @TINT; color: @NAVY; display: flex; align-items: center; justify-content: center; }
.tnote { font-size: 9.5pt; color: @MUTE; margin-top: 0.1in; line-height: 1.4; }

/* columns */
.cols { display: grid; align-items: start; }
.cols.stretch { align-items: stretch; }

/* statement */
.statement .st { margin: 0; font-weight: 700; color: @NAVY; line-height: 1.42; letter-spacing: -0.01em; }
.statement .st b { color: @ACCENT; margin-right: 0.16in; }
.statement .sb { margin: 0.24in 0 0; font-size: 13.5pt; color: @INK; line-height: 1.6; }

/* facts (definition list) */
.facts { display: grid; margin: 0; }
.facts .f { display: grid; column-gap: 0.2in; padding: 0.13in 0; border-top: 1px solid @RULE; }
.facts .f:last-child { border-bottom: 1px solid @RULE; }
.facts dt { margin: 0; font-size: 11.5pt; color: @MUTE; padding-top: 0.03in; }
.facts dd { margin: 0; font-size: 14pt; font-weight: 600; color: @INK; line-height: 1.4; }
.facts.inline { grid-auto-flow: column; column-gap: 0.4in; border-top: 1px solid @RULE; padding-top: 0.14in; }
.facts.inline .f { display: block; border: 0; padding: 0; }
.facts.inline dt { margin-bottom: 0.05in; }
.facts.inline dd { font-size: 12pt; font-weight: 500; line-height: 1.45; }

/* numbered list */
.numbered { display: grid; }
.numbered .ni { display: grid; grid-template-columns: 0.42in 1fr; column-gap: 0.1in; padding: 0.1in 0; border-top: 1px solid @LINE; align-items: start; }
.numbered .ni:last-child { border-bottom: 1px solid @LINE; }
.numbered .nn { width: 0.3in; height: 0.3in; border-radius: 50%; background: @NAVY; color: #fff; font-size: 10.5pt; font-weight: 700; display: flex; align-items: center; justify-content: center; margin-top: 0.02in; }
.numbered .nt { font-size: 13.5pt; font-weight: 700; color: @INK; line-height: 1.3; }
.numbered .nd { font-size: 11.5pt; color: @MUTE; line-height: 1.4; margin-top: 0.03in; }

/* contents */
.toc { display: grid; column-gap: 0.6in; align-content: start; }
.toc .ti { display: grid; grid-template-columns: 0.75in 1fr; column-gap: 0.15in; padding: 0.14in 0; border-bottom: 1px solid @RULE; align-items: start; }
.toc .ti.first { border-top: 1px solid @RULE; }
.toc .tn { font-size: 20pt; font-weight: 700; color: @ACCENT; line-height: 1.1; }
.toc .tt { font-size: 14.5pt; font-weight: 700; color: @INK; line-height: 1.3; }
.toc .ts { font-size: 11.5pt; color: @MUTE; margin-top: 0.03in; line-height: 1.4; }

/* table */
.table { width: 100%; border-collapse: collapse; }
.table th { background: @TINT; color: @NAVY; font-weight: 700; text-align: left; padding: 0.1in 0.14in; border-bottom: 1px solid @RULE; line-height: 1.3; }
.table td { padding: 0.1in 0.14in; border-bottom: 1px solid @LINE; vertical-align: top; line-height: 1.4; color: @INK; }
.table.firstbold td:first-child { font-weight: 700; }

/* kpi */
.kpis { display: grid; gap: 0.25in; }
.kpi { background: #fff; border: 1px solid @LINE; border-radius: 0.12in; padding: 0.26in 0.3in; display: flex; flex-direction: column; gap: 0.08in; }
.kpi .kv { font-size: 30pt; font-weight: 700; color: @NAVY; line-height: 1.1; letter-spacing: -0.01em; }
.kpi .kv small { font-size: 14pt; font-weight: 600; margin-left: 0.06in; }
.kpi .kl { font-size: 12pt; color: @INK; line-height: 1.45; }
.kpi .kt { align-self: flex-start; font-size: 9.5pt; font-weight: 700; color: @MUTE; background: @TINT; border-radius: 999px; padding: 0.03in 0.14in; }
.kpi .kb { height: 0.09in; background: @LINE; border-radius: 999px; overflow: hidden; margin-top: 0.06in; }
.kpi .kb i { display: block; height: 100%; background: @ACCENT; }
.kpi.navy { background: @NAVY; border-color: @NAVY; }
.kpi.navy .kv, .kpi.navy .kl { color: #fff; }
.kpi.navy .kt { background: rgba(255,255,255,0.18); color: #fff; }
.kpi.navy .kb { background: rgba(255,255,255,0.25); }
.kpi.navy .kb i { background: #fff; }

/* photo */
.photo { display: flex; flex-direction: column; gap: 0.08in; }
.photo .pf { border-radius: 0.12in; overflow: hidden; background: @TINT; }
.photo .pf img { display: block; width: 100%; height: 100%; }
.photo .pc { font-size: 11pt; color: @MUTE; line-height: 1.4; }
.photo .pcr { font-size: 9pt; color: @FAINT; }

/* loop */
.loop { position: relative; }
.loop svg { position: absolute; left: 0; top: 0; width: 100%; height: 100%; }
.loop .ln { position: absolute; transform: translate(-50%, -50%); background: #fff; border: 1px solid @RULE; border-radius: 0.1in; padding: 0.1in 0.14in; text-align: center; }
.loop .ln b { display: block; font-size: 12.5pt; color: @NAVY; }
.loop .ln span { display: block; font-size: 10pt; color: @MUTE; line-height: 1.35; margin-top: 0.03in; }
.loop .lc { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); text-align: center; }
.loop .lc .ll { display: flex; justify-content: center; align-items: center; gap: 0.16in; margin-bottom: 0.1in; }
.loop .lc img { height: 0.4in; }
.loop .lc div { font-size: 10.5pt; color: @INK; line-height: 1.4; }

/* brand panel */
.brand { background: #fff; border: 1px solid @LINE; border-radius: 0.12in; padding: 0.32in 0.38in; height: 100%; }
.brand .bh { display: flex; align-items: center; gap: 0.16in; height: 0.52in; margin-bottom: 0.2in; }
.brand .bh img.bl { height: 0.4in; }
.brand .bh img.bs { height: 0.46in; }
.brand .bh .bn { font-size: 21pt; font-weight: 700; color: @INK; letter-spacing: -0.01em; }
.brand .bt { margin: 0 0 0.2in; font-size: 12.5pt; color: @INK; line-height: 1.55; }
.brand .bf { border-top: 1px solid @LINE; border-bottom: 1px solid @LINE; padding: 0.08in 0; margin-bottom: 0.2in; }
.brand .bfi { display: flex; align-items: center; gap: 0.16in; padding: 0.08in 0; font-size: 12pt; line-height: 1.35; }
.brand .bfi img { width: 0.32in; height: 0.32in; object-fit: contain; flex: none; }
.brand .ticks li { font-size: 12pt; margin-bottom: 0.08in; }

.cards { display: grid; gap: 0.25in; }
.card { background: #fff; border: 1px solid @LINE; border-radius: 0.1in; padding: 0.26in 0.3in; }
.card .idisc { margin-bottom: 0.16in; }
.card .num { width: 0.42in; height: 0.42in; border-radius: 50%; background: @NAVY; color: #fff; font-weight: 700; font-size: 13pt; display: flex; align-items: center; justify-content: center; margin-bottom: 0.14in; }
.card .ch { display: flex; align-items: center; gap: 0.14in; margin-bottom: 0.12in; }
.card .ch .idisc { width: 0.44in; height: 0.44in; margin: 0; }
.card .ch h3 { margin: 0; }
.card h3 { margin: 0 0 0.14in 0; font-size: 15pt; color: @NAVY; }
.card p { margin: 0; font-size: 12.5pt; line-height: 1.5; }
.card .ticks li { font-size: 12.5pt; margin-bottom: 0.08in; }

.banner { background: @TINT; border-radius: 0.16in; padding: 0.2in 0.35in; display: flex; align-items: center; font-size: 13.5pt; line-height: 1.45; }
.banner b { color: @NAVY; margin-right: 0.15in; white-space: nowrap; }
.banner .idisc { background: #fff; margin-right: 0.28in; }

.rows { display: flex; flex-direction: column; gap: 0.12in; }
.row { display: grid; grid-template-columns: 0.72in 3.1in 1fr auto; align-items: center; background: #fff; border: 1px solid @LINE; border-radius: 0.14in; padding: 0.1in 0.18in 0.1in 0; }
.row.plain { grid-template-columns: 0.46in 3.1in 1fr auto; }
.row .no { width: 0.34in; height: 0.34in; border-radius: 50%; background: @NAVY; color: #fff; font-weight: 700; font-size: 12pt; display: flex; align-items: center; justify-content: center; margin-left: 0.18in; }
.row .no.opt { background: @STEEL; }
.row .dot { width: 0.09in; height: 0.09in; border-radius: 50%; background: @ACCENT; margin-left: 0.2in; }
.row .idisc { width: 0.44in; height: 0.44in; margin-left: 0.14in; }
.row .t { font-size: 13.5pt; font-weight: 700; padding-right: 0.2in; }
.row .d { font-size: 12pt; color: @MUTE; line-height: 1.4; }
.row .chip { margin-left: 0.2in; font-size: 11.5pt; font-weight: 700; padding: 0.05in 0.25in; border-radius: 999px; background: @TINT2; color: @NAVY; }
.row .chip.basic { background: @NAVY; color: #fff; }

.ticks { list-style: none; margin: 0; padding: 0; }
.ticks li { line-height: 1.45; }
.ticks li::before { content: "|  "; color: @ACCENT; font-weight: 700; }
.ticks b { color: @NAVY; }

.stats { display: grid; gap: 0.2in; }
.stats .cap { grid-column: 1 / -1; font-size: 11pt; font-weight: 700; color: @MUTE; margin-bottom: -0.06in; }
.stat { background: #fff; border: 1px solid @LINE; border-radius: 0.12in; padding: 0.18in 0.24in; display: flex; align-items: center; gap: 0.2in; }
.stat .idisc { width: 0.6in; height: 0.6in; }
.stat .v { font-size: 18pt; font-weight: 700; color: @NAVY; line-height: 1.15; }
.stat .l { font-size: 10.5pt; color: @MUTE; margin-top: 0.04in; line-height: 1.35; }

.stack { display: grid; column-gap: 0.25in; row-gap: 0.14in; align-items: stretch; }
.stack .lab { display: flex; align-items: center; justify-content: center; text-align: center; border-radius: 0.14in; font-size: 14.5pt; font-weight: 700; padding: 0.1in 0.2in; }
.stack .desc { background: #fff; border: 1px solid @LINE; border-radius: 0.1in; padding: 0.12in 0.25in; display: flex; align-items: center; font-size: 12pt; line-height: 1.4; }
.stack .aside { grid-column: 3; background: #fff; border: 1px solid @LINE; border-radius: 0.08in; padding: 0.2in 0.25in; }
.stack .aside h3 { margin: 0 0 0.15in 0; font-size: 14pt; color: @NAVY; }
.stack .aside .ticks li { font-size: 11.5pt; margin-bottom: 0.1in; }
.stack .aside .ticks b { color: @INK; }

.timeline { flex: 1; display: grid; column-gap: 0.3in; }
.tcol { position: relative; padding-left: 0.3in; }
.tcol::before { content: ""; position: absolute; left: 0.12in; top: 0; bottom: 0; width: 3.5pt; background: @PALE; }
.tentry { position: relative; margin-bottom: 0.25in; }
.tentry::before { content: ""; position: absolute; left: -0.3in; top: 0.1in; width: 0.2in; height: 0.2in; border-radius: 50%; background: @NAVY; margin-left: 0.03in; }
.tentry.opt::before { background: @STEEL; }
.tentry .when { font-size: 12pt; font-weight: 700; color: @ACCENT; }
.tentry .ttl { font-size: 16pt; font-weight: 700; color: @NAVY; margin: 0.03in 0 0.12in 0; }
.tentry .ticks li { font-size: 12.5pt; margin-bottom: 0.06in; }

.qa .q { font-size: 16pt; font-weight: 700; color: @NAVY; margin: 0 0 0.08in 0; }
.qa .a { font-size: 12.5pt; line-height: 1.45; margin: 0 0 0.3in 0; }

.split { flex: 1; display: grid; column-gap: 0.25in; min-height: 0; }
.shots { display: flex; flex-direction: column; gap: 0.2in; height: 100%; }
.shot { flex: 1; background: #F4F6FB; border: 1.1pt solid @ACCENT; border-radius: 0.06in; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 0.2in; }
.shot .lb { font-size: 12pt; font-weight: 700; color: @ACCENT; }
.shot .cap { font-size: 11pt; color: @MUTE; margin-top: 0.05in; }

/* profiles */
.profiles { display: grid; gap: 0.35in; }
.profile { background: #fff; border: 1px solid @LINE; border-radius: 0.14in; padding: 0.36in 0.45in 0.3in; }
.profile .ph { display: flex; align-items: center; gap: 0.22in; margin-bottom: 0.26in; }
.profile .avatar { flex: none; width: 0.8in; height: 0.8in; border-radius: 50%; border: 2pt solid @INK; display: flex; align-items: center; justify-content: center; font-size: 22pt; font-weight: 700; color: @INK; }
.profile .nm { font-size: 21pt; font-weight: 700; color: @INK; line-height: 1.15; }
.profile .role { font-size: 10.5pt; color: @MUTE; letter-spacing: 0.06em; margin-top: 0.05in; }
.profile .pr { display: grid; grid-template-columns: 0.85in 1fr; column-gap: 0.1in; margin-top: 0.18in; align-items: start; }
.profile .pr .k { font-size: 13pt; font-weight: 700; color: @INK; padding-top: 0.02in; }
.profile .pr .v div { border-left: 1.5pt solid @RULE; padding-left: 0.16in; font-size: 12.5pt; line-height: 1.35; margin-bottom: 0.07in; }

/* steps */
.steps { display: flex; align-items: center; gap: 0.07in; }
.step { flex: 1; display: flex; align-items: center; gap: 0.09in; background: #fff; border: 1px solid @LINE; border-radius: 999px; padding: 0.1in 0.14in; font-size: 11pt; font-weight: 700; color: @INK; line-height: 1.2; }
.step .n { flex: none; width: 0.3in; height: 0.3in; border-radius: 50%; background: @NAVY; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 10.5pt; }
.step .ic { color: @ACCENT; }
.sa { color: @ACCENT; font-size: 15pt; line-height: 1; flex: none; }
.steps.tiles .step { flex-direction: column; border-radius: 0.14in; padding: 0.12in 0.1in; text-align: center; gap: 0.07in; align-self: stretch; justify-content: flex-start; }
.steps.tiles .sh { display: flex; align-items: center; gap: 0.08in; }
.steps.tiles .sl { font-size: 11pt; line-height: 1.25; }
.steps.detail { align-items: stretch; }
.steps.detail .step { flex-direction: column; align-items: stretch; border-radius: 0.14in; padding: 0.18in 0.22in; gap: 0.05in; text-align: left; font-weight: 400; }
.steps.detail .sk { font-size: 9.5pt; font-weight: 700; letter-spacing: 0.08em; color: @ACCENT; }
.steps.detail .sw { font-size: 10.5pt; color: @MUTE; }
.steps.detail .st2 { font-size: 13.5pt; font-weight: 700; color: @NAVY; line-height: 1.3; margin-top: 0.03in; }
.steps.detail .sd { font-size: 10.5pt; color: @INK; line-height: 1.4; margin-top: 0.04in; }
.steps.detail .sa { align-self: center; }
.stepsw .facts.inline { margin-top: 0.26in; }

/* diagram */
.diagram { height: 100%; background: #fff; border: 1px solid @LINE; border-radius: 0.1in; padding: 0.3in 0.25in; display: grid; grid-template-columns: 1.35in 0.45in 1fr 0.45in 1.35in; grid-template-rows: auto 0.4in auto 0.4in auto; column-gap: 0.08in; align-items: center; align-content: center; }
.dn { border: 1px solid @PALE; background: @TINT; border-radius: 0.1in; padding: 0.14in 0.16in; text-align: center; }
.dn.accent { background: @NAVY; color: #fff; border-color: @NAVY; }
.dn.strong { background: #fff; border: 2pt solid @NAVY; }
.dn h4 { margin: 0 0 0.05in 0; font-size: 12.5pt; display: flex; align-items: center; justify-content: center; gap: 0.08in; }
.dn h4 .ic { color: @ACCENT; }
.dn.accent h4 .ic { color: #fff; }
.dn p { margin: 0; font-size: 10.5pt; line-height: 1.35; color: inherit; opacity: 0.9; }
.dn .chips { display: flex; justify-content: center; gap: 0.05in; margin-bottom: 0.08in; }
.dn .chips i { font-style: normal; width: 0.24in; height: 0.24in; border-radius: 50%; background: @NAVY; color: #fff; font-size: 9pt; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.dn.accent .chips i { background: #fff; color: @NAVY; }
.dn .nl { display: flex; justify-content: center; align-items: center; gap: 0.14in; margin-bottom: 0.08in; }
.dn .nl img { height: 0.34in; }
.arrow { text-align: center; font-size: 10pt; color: @MUTE; line-height: 1.1; }
.arrow span { display: block; font-size: 18pt; color: @ACCENT; line-height: 1; }
.arrow.v { display: flex; align-items: center; justify-content: center; gap: 0.08in; }
.arrow.v span { display: inline; }
.diag { display: flex; flex-direction: column; }
.diag .dn { padding: 0.18in 0.2in; }
.diag .dn h4 { font-size: 13.5pt; margin-bottom: 0.06in; }
.diag .dn p { font-size: 11pt; }
.diag .arrow { font-size: 10.5pt; }
.diag .arrow span { font-size: 20pt; }
.dframe { position: relative; border: 1.5pt dashed @PALE; border-radius: 0.16in; padding: 0.38in 0.3in 0.26in; }
.dlabel { position: absolute; top: -0.15in; left: 0.3in; background: @TINT; color: @NAVY; font-size: 10.5pt; font-weight: 700; padding: 0.04in 0.18in; border-radius: 999px; border: 1px solid @PALE; }
.dlabel.r { left: auto; right: 0.3in; background: #fff; color: @MUTE; font-weight: 400; }
.dgrid { display: grid; grid-template-columns: 2.6in 0.75in 1fr 0.75in 2.6in; column-gap: 0.1in; align-items: center; }

/* gantt */
.gantt { display: grid; grid-template-columns: 2.9in 1fr; row-gap: 0.1in; align-content: start; }
.gantt .gmonths { display: grid; border-bottom: 1px solid @RULE; }
.gantt .gmonths div { font-size: 11.5pt; font-weight: 700; color: @NAVY; padding: 0 0 0.08in 0.1in; border-left: 1px solid @LINE; }
.gantt .gl { font-size: 13pt; font-weight: 700; color: @INK; display: flex; flex-direction: column; justify-content: center; height: 0.6in; padding-right: 0.2in; line-height: 1.25; }
.gantt .gl .sub { font-size: 10.5pt; font-weight: 400; color: @MUTE; margin-top: 0.02in; }
.gantt .gt { position: relative; height: 0.6in; background-image: linear-gradient(to right, @LINE 1px, transparent 1px); }
.gantt .gbar { position: absolute; top: 0.12in; height: 0.36in; border-radius: 0.18in; display: flex; align-items: center; padding: 0 0.16in; font-size: 11pt; white-space: nowrap; overflow: hidden; }
.gantt .gms { position: absolute; top: 0; height: 100%; }
.gantt .gms i { position: absolute; top: 0.19in; left: -0.11in; width: 0.22in; height: 0.22in; background: @NAVY; transform: rotate(45deg); }
.gantt .gms span { position: absolute; right: 0.2in; top: 0.16in; font-size: 12pt; font-weight: 700; color: @NAVY; white-space: nowrap; }
.gantt .gms.right span { right: auto; left: 0.2in; }

/* cover */
.cover .stripe { position: absolute; border-radius: 999px; transform: rotate(40deg); }
.cover .ttl { position: absolute; left: 0.75in; top: 2.05in; width: 10.5in; }
.cover .ttl h1 { margin: 0; font-size: 50pt; font-weight: 700; color: @NAVY; line-height: 1.22; }
.cover .tagline { margin: 0.35in 0 0 0.03in; font-size: 16pt; color: @MUTE; }
.cover .logos { position: absolute; left: 0.75in; top: 5.5in; display: flex; align-items: center; gap: 0.3in; }
.cover .logos img { height: 0.36in; display: block; }
.cover .logos img.client { height: 0.4in; }
.cover .logos .sep { width: 1px; height: 0.42in; background: @PALE; }
.cover .foot { position: absolute; left: 0.75in; top: 6.2in; font-size: 12pt; font-weight: 700; color: @MUTE; }
.cover.report { background: linear-gradient(155deg, #FFFFFF 0%, @TINT 100%); }
.cover.report .panel { position: absolute; left: 0; top: 0; width: 7.4in; height: 100%; background: @NAVY; color: #fff; padding: 0.75in; }
.cover.report .plogo { height: 0.36in; display: block; }
.cover.report .pbrand { color: #fff; font-size: 16pt; font-weight: 700; letter-spacing: 0.04em; }
.cover.report .kind { margin-top: 1.1in; font-size: 12pt; font-weight: 700; letter-spacing: 0.12em; color: @PALE; }
.cover.report .ttl { position: static; width: auto; margin-top: 0.25in; }
.cover.report .ttl h1 { color: #fff; font-size: 40pt; line-height: 1.2; }
.cover.report .tagline { color: @PALE; margin-top: 0.3in; }
.cover.report .meta { position: absolute; left: 0.75in; right: 0.75in; bottom: 0.75in; margin: 0; display: grid; grid-template-columns: 1.2in 1fr; row-gap: 0.08in; font-size: 11pt; }
.cover.report .meta dt { margin: 0; color: @PALE; }
.cover.report .meta dd { margin: 0; color: #fff; font-weight: 600; }
.cover.report .pimg { position: absolute; left: 7.4in; top: 0; width: 5.933in; height: 100%; object-fit: cover; }

/* closing */
.closing { background: @NAVY; }
.closing h1 { position: absolute; left: 0; right: 0; top: 2.75in; margin: 0; text-align: center; font-size: 44pt; font-weight: 700; color: #fff; }
.closing .logo { position: absolute; left: 50%; transform: translateX(-50%); top: 5.15in; height: 0.3in; }
.closing .brandname { height: auto; white-space: nowrap; color: #fff; font-size: 16pt; font-weight: 700; letter-spacing: 0.04em; }
.closing .contact { position: absolute; left: 0; right: 0; top: 5.65in; text-align: center; font-size: 12pt; color: @PALE; line-height: 1.6; }
"""


def css(t):
    out = CSS_T.replace("@FONT_IMPORT", f"@import url('{t['font_css']}');" if t.get("font_css") else "")
    out = out.replace("@ACCENT", t.get("accent") or t["steel"])
    for key in ("navy", "steel", "ink", "mute", "tint2", "tint", "line", "pale", "rule", "faint", "font"):
        out = out.replace("@" + key.upper(), t[key])
    return out


def sections_of(slides):
    """The contents a report derives from its slides: one [no, title, sub] per distinct `section`, in order."""
    out, seen = [], {}
    for s in slides:
        if s.get("type", "content") != "content" or not s.get("section"):
            continue
        sec = str(s["section"]).strip()
        if sec in seen:
            if not seen[sec][2] and s.get("toc_sub"):
                seen[sec][2] = s["toc_sub"]
            continue
        m = re.match(r"^(\d+[.)]?)\s+(.*)$", sec)
        entry = [m.group(1), m.group(2), s.get("toc_sub", "")] if m else ["", sec, s.get("toc_sub", "")]
        seen[sec] = entry
        out.append(entry)
    return out


def _with_path(markup, path):
    """Mark the block's root element with its path in the deck file, for the layout report."""
    return re.sub(r"^(<\w+)", lambda m: f'{m.group(1)} data-path="{path}"', markup, count=1)


class Renderer:
    def __init__(self, theme, register="proposal"):
        self.t = theme
        self.reg = "report" if register == "report" else "proposal"
        self.css = css(theme)
        self.step = [theme["tint"], theme["pale"], theme["steel"], theme["navy"]]
        self.sections = []
        self.labels = {"step": "STEP", "q": "Q."}
        self.doc_name = ""
        # cover stripes: (center x, center y, width, length, color) in inches
        self.stripes = [
            (5.3, 0.85, 0.9, 2.4, theme["tint2"]),
            (9.3, 2.1, 0.85, 6.1, theme["line"]),
            (8.7, 4.2, 1.05, 6.2, theme["tint"]),
            (9.9, 4.7, 0.75, 3.1, theme["steel"]),
        ]

    def fg_on(self, bg):
        return "#fff" if _luma(bg) < 0.45 else self.t["navy"]

    def ticks(self, items, size=None, gap=None):
        """[head, body] renders a bold head and its sentence; [text] or "text" renders plain text."""
        style = f"font-size:{size}pt;" if size else ""
        out = [f'<ul class="ticks" style="{style}">']
        for it in items:
            if isinstance(it, str):
                it = [it]
            head, body = it[0], (it[1] if len(it) > 1 else "")
            gs = f' style="margin-bottom:{gap}pt"' if gap else ""
            if body:
                out.append(f"<li{gs}><b>{_e(head)}</b>&nbsp;&nbsp;&nbsp;{_e(body)}</li>")
            else:
                out.append(f"<li{gs}>{_e(head)}</li>")
        out.append("</ul>")
        return "".join(out)

    def columns(self, blk, path):
        inner = "".join(f'<div class="col">{self.block(b, f"{path}.blocks[{i}]")}</div>' for i, b in enumerate(blk["blocks"]))
        cls = " stretch" if blk.get("stretch") else ""
        return f'<div class="cols{cls}" style="grid-template-columns:{blk.get("widths", "1fr 1fr")};column-gap:{blk.get("gap", 0.4)}in">{inner}</div>'

    def statement(self, blk):
        lead = f"<b>{_e(blk['lead'])}</b>" if blk.get("lead") else ""
        body = f'<p class="sb">{_e(blk["body"])}</p>' if blk.get("body") else ""
        return f'<div class="statement"><p class="st" style="font-size:{blk.get("size", 20)}pt">{lead}{_e(blk["text"])}</p>{body}</div>'

    def facts(self, blk):
        rows = []
        for label, value in blk["items"]:
            v = "<br>".join(_e(x) for x in value) if isinstance(value, list) else _e(value)
            rows.append(f'<div class="f" style="grid-template-columns:{blk.get("label_w", "1.3in")} 1fr"><dt>{_e(label)}</dt><dd>{v}</dd></div>')
        cls = " inline" if blk.get("inline") else ""
        return f'<dl class="facts{cls}">{"".join(rows)}</dl>'

    def numbered(self, blk):
        items = "".join(f'<div class="ni"><div class="nn">{it.get("no", i + 1)}</div><div><div class="nt">{_e(it["title"])}</div>'
                        f'{("<div class=nd>" + _e(it["desc"]) + "</div>") if it.get("desc") else ""}</div></div>'
                        for i, it in enumerate(blk["items"]))
        return f'<div class="numbered" style="grid-template-columns:repeat({blk.get("cols", 1)},1fr);column-gap:0.4in">{items}</div>'

    def toc(self, blk):
        """The contents: entries of [no, title, sub], given or derived from the slides' `section` fields."""
        items = blk.get("items") or self.sections
        cols = max(1, int(blk.get("cols", 2)))
        n = max(1, len(items))
        rows = -(-n // cols)
        cells = []
        for i, it in enumerate(items):
            no, title, sub = (list(it) + ["", "", ""])[:3]
            first = " first" if i % rows == 0 else ""
            subh = f'<div class="ts">{_e(sub)}</div>' if sub else ""
            cells.append(f'<div class="ti{first}"><div class="tn">{_e(no)}</div><div><div class="tt">{_e(title)}</div>{subh}</div></div>')
        return (f'<div class="toc" style="grid-template-columns:repeat({cols},1fr);grid-template-rows:repeat({rows},auto);'
                f'grid-auto-flow:column">{"".join(cells)}</div>')

    def table(self, blk):
        widths = blk.get("widths")
        colgroup = ("<colgroup>" + "".join(f'<col style="width:{w}">' for w in widths) + "</colgroup>") if widths else ""
        head = "".join(f"<th>{_e(c)}</th>" for c in blk["columns"])
        body = "".join("<tr>" + "".join(f"<td>{_e(c)}</td>" for c in row) + "</tr>" for row in blk["rows"])
        cls = " firstbold" if blk.get("first_col") == "bold" else ""
        note = f'<div class="tnote">{_e(blk["note"])}</div>' if blk.get("note") else ""
        return (f'<div class="tablew"><table class="table{cls}" style="font-size:{blk.get("size", 11.5)}pt">{colgroup}'
                f'<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>{note}</div>')

    def kpi(self, blk):
        n = blk.get("cols", len(blk["items"]))
        panels = []
        for it in blk["items"]:
            tone = " navy" if it.get("tone") == "navy" else ""
            unit = f'<small>{_e(it["unit"])}</small>' if it.get("unit") else ""
            tag = f'<div class="kt">{_e(it["tag"])}</div>' if it.get("tag") else ""
            bar = ""
            if it.get("bar") is not None:
                pct = min(max(float(it["bar"]), 0.0), 1.0) * 100
                bar = f'<div class="kb"><i style="width:{pct:.1f}%"></i></div>'
            panels.append(f'<div class="kpi{tone}"><div class="kv">{_e(it["value"])}{unit}</div>'
                          f'<div class="kl">{_e(it.get("label", ""))}</div>{bar}{tag}</div>')
        note = f'<div class="tnote">{_e(blk["note"])}</div>' if blk.get("note") else ""
        return f'<div class="kpiw"><div class="kpis" style="grid-template-columns:repeat({n},1fr)">{"".join(panels)}</div>{note}</div>'

    def photo(self, blk):
        img = _img_data(blk.get("src"))
        fit = blk.get("fit", "cover")
        frame = f'<div class="pf" style="height:{blk.get("h", 3.6)}in">' + (f'<img src="{img}" style="object-fit:{fit}">' if img else "") + "</div>"
        cap = f'<div class="pc">{_e(blk["caption"])}</div>' if blk.get("caption") else ""
        cr = f'<div class="pcr">{_e(blk["credit"])}</div>' if blk.get("credit") else ""
        return f'<div class="photo">{frame}{cap}{cr}</div>'

    def loop(self, blk):
        """Four nodes (top, right, bottom, left) joined clockwise by a ring; logos and a caption at the center."""
        w, h, r = blk.get("width", 4.6), blk.get("height", 4.0), blk.get("r", 1.45)
        cx, cy, sc = w / 2, h / 2, 100
        accent = self.t.get("accent") or self.t["steel"]
        heads = []
        for deg in (-45, 45, 135, 225):
            th = math.radians(deg)
            x, y = (cx + r * math.cos(th)) * sc, (cy + r * math.sin(th)) * sc
            heads.append(f'<path d="M-9,-6 L9,0 L-9,6 Z" fill="{accent}" transform="translate({x:.1f},{y:.1f}) rotate({deg + 90})"/>')
        svg = (f'<svg viewBox="0 0 {w * sc:.0f} {h * sc:.0f}"><circle cx="{cx * sc:.1f}" cy="{cy * sc:.1f}" r="{r * sc:.1f}" '
               f'fill="none" stroke="{self.t["pale"]}" stroke-width="3"/>{"".join(heads)}</svg>')
        pos = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
        nw = blk.get("node_w", 1.3)
        nodes = "".join(f'<div class="ln" style="left:{x:.2f}in;top:{y:.2f}in;width:{nw}in"><b>{_e(n["title"])}</b>'
                        f'{("<span>" + _e(n["sub"]) + "</span>") if n.get("sub") else ""}</div>'
                        for n, (x, y) in zip(blk["nodes"], pos))
        logos = "".join(_img(p) for p in blk.get("center_logos", []))
        center = (f'<div class="lc" style="width:{blk.get("center_w", 1.45)}in">{("<div class=ll>" + logos + "</div>") if logos else ""}'
                  + "".join(f"<div>{_e(x)}</div>" for x in blk.get("center", [])) + "</div>")
        return f'<div class="loop" style="width:{w}in;height:{h}in">{svg}{nodes}{center}</div>'

    def brand(self, blk):
        if blk.get("logo"):
            head = _img(blk["logo"], "bl")
        else:
            head = _img(blk.get("symbol"), "bs") + f'<span class="bn">{_e(blk.get("name", ""))}</span>'
        tag = f'<p class="bt">{_e(blk["tagline"])}</p>' if blk.get("tagline") else ""
        facts = ""
        if blk.get("facts"):
            facts = '<div class="bf">' + "".join(f'<div class="bfi">{_img(f.get("logo"))}<span>{_e(f["text"])}</span></div>' for f in blk["facts"]) + "</div>"
        items = self.ticks(blk["items"]) if blk.get("items") else ""
        return f'<div class="brand"><div class="bh">{head}</div>{tag}{facts}{items}</div>'

    def cards(self, blk):
        n = blk.get("cols", len(blk["items"]))
        hs = f"min-height:{blk['h']}in;" if blk.get("h") else ""
        cards = []
        for i, it in enumerate(blk["items"]):
            inner = f'<p>{_e(it["body"])}</p>' if it.get("body") else ""
            if it.get("items"):
                inner += self.ticks(it["items"])
            if blk.get("numbered"):
                head = f'<div class="num">{it.get("no", i + 1)}</div><h3>{_e(it["title"])}</h3>'
            elif blk.get("icon_pos") == "inline":
                head = f'<div class="ch">{_disc(it.get("icon"), 0.26)}<h3>{_e(it["title"])}</h3></div>'
            else:
                head = f'{_disc(it.get("icon"))}<h3>{_e(it["title"])}</h3>'
            cards.append(f'<div class="card" style="{hs}">{head}{inner}</div>')
        return f'<div class="cards" style="grid-template-columns:repeat({n},1fr)">{"".join(cards)}</div>'

    def banner(self, blk):
        lead = f"<b>{_e(blk['lead'])}</b>" if blk.get("lead") else ""
        return (f'<div class="banner" style="min-height:{blk.get("h", 0.95)}in">{_disc(blk.get("icon"), 0.32)}'
                f'<div>{lead}{_e(blk.get("body", ""))}</div></div>')

    def rows(self, blk):
        rh = blk.get("row_h", 0.78)
        plain = blk.get("numbered") is False
        rows = []
        for i, it in enumerate(blk["items"]):
            tag = it.get("tag")
            basic = blk.get("basic_tag")
            opt = " opt" if tag and tag != basic else ""
            chip = f'<span class="chip{" basic" if tag == basic else ""}">{_e(tag)}</span>' if tag else "<span></span>"
            if it.get("icon"):
                lead = _disc(it["icon"], 0.26)
            elif plain:
                lead = '<div class="dot"></div>'
            else:
                lead = f'<div class="no{opt}">{it.get("no", i + 1)}</div>'
            rows.append(f'<div class="row{" plain" if plain else ""}" style="min-height:{rh}in">{lead}'
                        f'<div class="t">{_e(it["title"])}</div><div class="d">{_e(it["desc"])}</div>{chip}</div>')
        return f'<div class="rows">{"".join(rows)}</div>'

    def stats(self, blk):
        n = blk.get("cols", len(blk["items"]))
        cap = f'<div class="cap">{_e(blk["caption"])}</div>' if blk.get("caption") else ""
        tiles = "".join(f'<div class="stat">{_disc(it.get("icon"), 0.32)}<div><div class="v">{_e(it["value"])}</div>'
                        f'<div class="l">{_e(it.get("label", ""))}</div></div></div>' for it in blk["items"])
        return f'<div class="stats" style="grid-template-columns:repeat({n},1fr)">{cap}{tiles}</div>'

    def shots(self, items):
        return '<div class="shots">' + "".join(
            f'<div class="shot">{("<div class=lb>" + _e(it["label_above"]) + "</div>") if it.get("label_above") else ""}'
            f'<div class="lb">{_e(it.get("label", "screenshot"))}</div><div class="cap">{_e(it["caption"])}</div></div>'
            for it in items) + "</div>"

    def stack(self, blk):
        items = blk["items"]
        rh = blk.get("row_h", 1.05)
        cells = []
        for i, it in enumerate(items):
            c = self.step[min(i, len(self.step) - 1)] if len(items) > 2 else [self.t["steel"], self.t["navy"]][i % 2]
            cells.append(f'<div class="lab" style="background:{c};color:{self.fg_on(c)};min-height:{rh}in;grid-row:{i + 1}">{_e(it["label"])}</div>'
                         f'<div class="desc" style="grid-row:{i + 1}">{_e(it["desc"])}</div>')
        aside = blk.get("aside")
        if aside:
            cells.append(f'<div class="aside" style="grid-row:1 / span {len(items)}"><h3>{_e(aside["title"])}</h3>{self.ticks(aside["items"])}</div>')
        cols = blk.get("cols", "3in 5.6in 1fr" if aside else "3in 1fr")
        return f'<div class="stack" style="grid-template-columns:{cols}">{"".join(cells)}</div>'

    def timeline(self, blk):
        cols = blk["cols"]
        out = [f'<div class="timeline" style="grid-template-columns:repeat({len(cols)},1fr)">']
        for entries in cols:
            out.append('<div class="tcol">')
            for e in entries:
                out.append(f'<div class="tentry{" opt" if e.get("option") else ""}"><div class="when">{_e(e["when"])}</div>'
                           f'<div class="ttl">{_e(e["title"])}</div>{self.ticks(e.get("items", []))}</div>')
            out.append("</div>")
        out.append("</div>")
        return "".join(out)

    def qa(self, blk):
        return '<div class="qa">' + "".join(f'<p class="q">{_e(self.labels["q"])} {_e(it["q"])}</p><p class="a">{_e(it["a"])}</p>' for it in blk["items"]) + "</div>"

    def profiles(self, blk):
        cards = []
        for p in blk["items"]:
            rows = "".join(
                f'<div class="pr"><div class="k">{_e(k)}</div><div class="v">{"".join(f"<div>{_e(x)}</div>" for x in lines)}</div></div>'
                for k, lines in p["rows"])
            cards.append(f'<div class="profile"><div class="ph"><div class="avatar">{_e(p.get("initial", p["name"][0]))}</div>'
                         f'<div><div class="nm">{_e(p["name"])}</div><div class="role">{_e(p.get("title", ""))}</div></div></div>{rows}</div>')
        return f'<div class="profiles" style="grid-template-columns:repeat({blk.get("cols", len(cards))},1fr)">{"".join(cards)}</div>'

    def steps(self, blk):
        """Strings render as pills in one line; items with icons, or style: tiles, as tiles (number above the label);
        items with `when` or `desc` as detail tiles (STEP n, when, the label, the sentence), with the block's facts under the strip."""
        items = blk["items"]
        detail = any(isinstance(s, dict) and (s.get("desc") or s.get("when")) for s in items)
        tiles = not detail and (blk.get("style") == "tiles" or any(isinstance(s, dict) and s.get("icon") for s in items))
        parts = []
        for i, s in enumerate(items):
            if i:
                parts.append('<div class="sa">&#8594;</div>')
            if isinstance(s, str):
                label, icon, when, desc = s, None, "", ""
            else:
                label, icon, when, desc = s.get("label", s.get("title", "")), s.get("icon"), s.get("when", ""), s.get("desc", "")
            if detail:
                whenh = f'<div class="sw">{_e(when)}</div>' if when else ""
                desch = f'<div class="sd">{_e(desc)}</div>' if desc else ""
                parts.append(f'<div class="step"><div class="sk">{_e(self.labels["step"])} {i + 1}</div>{whenh}<div class="st2">{_e(label)}</div>{desch}</div>')
            elif tiles:
                parts.append(f'<div class="step"><div class="sh"><span class="n">{i + 1}</span>{_icon(icon, 0.28)}</div><span class="sl">{_e(label)}</span></div>')
            else:
                parts.append(f'<div class="step"><span class="n">{i + 1}</span>{_icon(icon, 0.26)}<span>{_e(label)}</span></div>')
        cls = " detail" if detail else (" tiles" if tiles else "")
        strip = f'<div class="steps{cls}">{"".join(parts)}</div>'
        if blk.get("facts"):
            return f'<div class="stepsw">{strip}{self.facts({"items": blk["facts"], "inline": True})}</div>'
        return strip

    def gantt(self, blk):
        months = blk["months"]
        n = len(months)
        t = self.t
        tones = {"tint": (t["tint"], t["navy"]), "pale": (t["pale"], t["navy"]), "steel": (t["steel"], self.fg_on(t["steel"])), "navy": (t["navy"], "#fff")}
        head = "".join(f"<div>{_e(m)}</div>" for m in months)
        out = [f'<div class="gantt"><div></div><div class="gmonths" style="grid-template-columns:repeat({n},1fr)">{head}</div>']
        for r in blk["rows"]:
            sub = f'<div class="sub">{_e(r["sub"])}</div>' if r.get("sub") else ""
            out.append(f'<div class="gl"><div>{_e(r["label"])}</div>{sub}</div>')
            track = ""
            if "start" in r:
                bg, fg = tones.get(r.get("tone", "navy"), tones["navy"])
                left = r["start"] / n * 100
                width = (r["end"] - r["start"]) / n * 100
                track += f'<div class="gbar" style="left:{left:.3f}%;width:{width:.3f}%;background:{bg};color:{fg}">{_e(r.get("text", ""))}</div>'
            if "milestone" in r:
                ms = r["milestone"]
                pct = ms / n * 100
                mtext = r.get("mtext", "" if "start" in r else r.get("text", ""))
                # the label sits at the diamond's left, unless the row's bar reaches the date: then at its right
                right = "start" in r and r["end"] >= ms - 0.05 and r["start"] <= ms + 0.05
                track += f'<div class="gms{" right" if right else ""}" style="left:{pct:.3f}%"><i></i><span>{_e(mtext)}</span></div>'
            out.append(f'<div class="gt" style="background-size:calc(100% / {n}) 100%;">{track}</div>')
        out.append("</div>")
        return "".join(out)

    def diagram(self, d, full=False):
        """Five nodes in a fixed arrangement: source (left), center, service (above), output (right), update (below)."""
        nodes = {n["id"]: n for n in d["nodes"]}
        order = [n["id"] for n in d["nodes"]]
        labels = {(a, b): l for a, b, l in d["edges"]}

        def node(nid, extra=""):
            n = nodes[nid]
            chips = "".join(f"<i>{_e(c)}</i>" for c in n.get("chips", []))
            chips = f'<div class="chips">{chips}</div>' if chips else ""
            logos = "".join(_img(p) for p in n.get("logos", []))
            logos = f'<div class="nl">{logos}</div>' if logos else ""
            cls = " accent" if n.get("accent") else (" strong" if n.get("strong") else "")
            return (f'<div class="dn{cls}" style="{extra}">{chips}{logos}'
                    f'<h4>{_icon(n.get("icon"), 0.26)}<span>{_e(n["title"])}</span></h4><p>{_e(n.get("body", ""))}</p></div>')

        def arrow(txt, glyph="&#8594;", extra="", v=False):
            return f'<div class="arrow{" v" if v else ""}" style="{extra}"><span>{glyph}</span>{_e(txt)}</div>'

        src, core, aux, out, upd = order[:5]
        if not full:
            return ('<div class="diagram">'
                    + node(aux, "grid-column:3;grid-row:1")
                    + arrow(labels.get((core, aux), ""), "&#8597;", "grid-column:3;grid-row:2", v=True)
                    + node(src, "grid-column:1;grid-row:3")
                    + arrow(labels.get((src, core), ""), extra="grid-column:2;grid-row:3")
                    + node(core, "grid-column:3;grid-row:3")
                    + arrow(labels.get((core, out), ""), extra="grid-column:4;grid-row:3")
                    + node(out, "grid-column:5;grid-row:3")
                    + arrow(labels.get((upd, core), ""), "&#8593;", "grid-column:3;grid-row:4", v=True)
                    + node(upd, "grid-column:3;grid-row:5")
                    + "</div>")
        mid_w = d.get("mid_w", 3.6)
        inner = (node(aux, f"grid-column:3;grid-row:1;justify-self:center;width:{mid_w}in")
                 + arrow(labels.get((core, aux), ""), "&#8597;", "grid-column:3;grid-row:2", v=True)
                 + node(src, "grid-column:1;grid-row:3")
                 + arrow(labels.get((src, core), ""), extra="grid-column:2;grid-row:3")
                 + node(core, "grid-column:3;grid-row:3")
                 + arrow(labels.get((core, out), ""), extra="grid-column:4;grid-row:3")
                 + node(out, "grid-column:5;grid-row:3"))
        fl = f'<span class="dlabel">{_e(d["frame"])}</span>' if d.get("frame") else ""
        fr = f'<span class="dlabel r">{_e(d["frame_note"])}</span>' if d.get("frame_note") else ""
        below = (arrow(labels.get((upd, core), ""), "&#8593;", "grid-column:3;grid-row:1", v=True)
                 + node(upd, f"grid-column:3;grid-row:2;justify-self:center;width:{mid_w}in"))
        return (f'<div class="diag"><div class="dframe">{fl}{fr}<div class="dgrid" style="grid-template-rows:auto 0.5in auto">{inner}</div></div>'
                f'<div class="dgrid" style="grid-template-rows:0.45in auto">{below}</div></div>')

    def split(self, blk):
        left, right = blk["left"], blk["right"]
        lhtml = self.ticks(left["items"], left.get("size", 13), left.get("gap", 11))
        rhtml = self.diagram(right["diagram"]) if right.get("diagram") else self.shots(right["items"])
        return f'<div class="split" style="grid-template-columns:{blk.get("left_w", 6.0)}in 1fr"><div>{lhtml}</div><div>{rhtml}</div></div>'

    def block(self, blk, path="$"):
        k = blk["kind"]
        if k == "bullets":
            out = self.ticks(blk["items"], blk.get("size", 13), blk.get("gap", 10))
        elif k == "shots":
            out = self.shots(blk["items"])
        elif k == "diagram":
            out = self.diagram(blk, full=True)
        elif k == "note":
            return ""
        elif k == "columns":
            out = self.columns(blk, path)
        else:
            fn = getattr(self, k, None)
            if fn is None or k in ("block", "slide", "html", "ticks", "fg_on"):
                raise ValueError(f"unknown block kind: {k}")
            out = fn(blk)
        return _with_path(out, path)

    def cover(self, s, meta, idx, label=None):
        tag = s.get("tagline") or s.get("subtitle") or ""
        stripes = "".join(
            f'<div class="stripe" style="left:{cx - w / 2:.2f}in;top:{cy - l / 2:.2f}in;width:{w}in;height:{l}in;background:{c}"></div>'
            for cx, cy, w, l, c in self.stripes)
        lab = f' data-label="{_e(label)}"' if label else ""
        if self.reg == "report":
            photo = _img_data(s.get("photo"))
            right = f'<img class="pimg" src="{photo}">' if photo else stripes
            wl = _img_data(meta.get("logo_white"))
            mark = f'<img class="plogo" src="{wl}">' if wl else (f'<div class="pbrand">{_e(meta["brand"])}</div>' if meta.get("brand") else "")
            kind = f'<div class="kind">{_e(s["kind"])}</div>' if s.get("kind") else ""
            rows = "".join(f"<dt>{_e(k)}</dt><dd>{_e(v)}</dd>" for k, v in s.get("meta_rows", []))
            metah = f'<dl class="meta">{rows}</dl>' if rows else ""
            return (f'<section class="slide cover report" data-slide="{idx + 1}"{lab}>{right}<div class="panel">{mark}{kind}'
                    f'<div class="ttl"><h1>{"<br>".join(_e(x) for x in s["title_lines"])}</h1>'
                    + (f'<p class="tagline">{_e(tag)}</p>' if tag else "") + f"</div>{metah}</div></section>")
        logo = _img_data(meta.get("logo"))
        clogo = _img_data(meta.get("client_logo"))
        logos = (f'<img class="client" src="{clogo}"><span class="sep"></span>' if clogo else "") + (f'<img src="{logo}">' if logo else "")
        foot = ""
        if isinstance(s.get("footer"), str):
            foot = f'<div class="foot">{_e(s["footer"])}</div>'
        elif s.get("footer"):
            foot = '<div class="foot">' + "&nbsp;&nbsp;|&nbsp;&nbsp;".join(_e(v) for v in [meta.get("client"), meta.get("date"), meta.get("brand")] if v) + "</div>"
        return (f'<section class="slide cover" data-slide="{idx + 1}"{lab}>{stripes}'
                f'<div class="ttl"><h1>{"<br>".join(_e(x) for x in s["title_lines"])}</h1>'
                + (f'<p class="tagline">{_e(tag)}</p>' if tag else "") + "</div>"
                + (f'<div class="logos">{logos}</div>' if logos else "") + foot + "</section>")

    def slide(self, s, meta, idx, label=None):
        t = s.get("type", "content")
        lab = f' data-label="{_e(label)}"' if label else ""
        if t == "cover":
            return self.cover(s, meta, idx, label)
        if t == "closing":
            logo = _img_data(meta.get("logo_white"))
            return (f'<section class="slide closing" data-slide="{idx + 1}"{lab}><h1>{_e(s.get("title", "Thank you"))}</h1>'
                    + (f'<img class="logo" src="{logo}">' if logo else (f'<div class="logo brandname">{_e(meta["brand"])}</div>' if meta.get("brand") else ""))
                    + f'<div class="contact">{"<br>".join(_e(c) for c in s.get("contact", []))}</div></section>')
        blocks = s.get("blocks", [])
        notes = [b["text"] for b in blocks if b["kind"] == "note"]
        body = "".join(self.block(b, f"$.slides[{idx}].blocks[{i}]") for i, b in enumerate(blocks) if b["kind"] != "note")
        tag = f'<div class="tag">{_e(s["tag"])}</div>' if s.get("tag") else ""
        hlogo = _img_data(s.get("logo"))
        hlogo = f'<img class="hlogo" src="{hlogo}">' if hlogo else ""
        sub = f'<h2>{_e(s["subtitle"])}</h2>' if s.get("subtitle") else ""
        note = f'<div class="note">{"<br>".join(_e(n) for n in notes)}</div>' if notes else ""
        cls = " center" if s.get("valign") == "center" else ""
        numbered = meta.get("page_numbers", True)
        if self.reg == "report":
            sec = f'<div class="sec">{_e(s["section"])}</div>' if s.get("section") else ""
            header = f'<div class="header rep">{tag}{hlogo}{sec}<h1>{_e(s["title"])}</h1>{sub}</div>'
            foot = ""
            if meta.get("footer", True):
                parts = [meta.get("brand"), meta.get("doc_name") or self.doc_name, meta.get("date")]
                left = "".join(f"<span>{_e(p)}</span>" for p in parts if p)
                right = f"{idx + 1:02d}" if numbered else ""
                foot = f'<div class="footer"><div class="fl">{left}</div><div class="fr">{right}</div></div>'
            return (f'<section class="slide report" data-slide="{idx + 1}"{lab}><div class="content">{header}'
                    f'<div class="body{cls}">{body}</div></div>{note}{foot}</section>')
        pageno = f'<div class="pageno">{idx + 1:02d}</div>' if numbered else ""
        return (f'<section class="slide" data-slide="{idx + 1}"{lab}><div class="content"><div class="header">{tag}{hlogo}<h1>{_e(s["title"])}</h1>{sub}</div>'
                f'<div class="body{cls}">{body}</div></div>{note}{pageno}</section>')

    def prepare(self, spec):
        slides = spec["slides"]
        self.sections = sections_of(slides)
        self.labels = {"step": "STEP", "q": "Q.", **spec.get("meta", {}).get("labels", {})}
        lines = slides[0].get("title_lines", []) if slides and slides[0].get("type") == "cover" else []
        self.doc_name = lines[0] if lines else ""

    def html(self, spec):
        meta = spec.get("meta", {})
        slides = spec["slides"]
        self.prepare(spec)
        title = " ".join(slides[0].get("title_lines", ["deck"])) if slides else "deck"
        pages = "\n".join(self.slide(s, meta, i) for i, s in enumerate(slides))
        return document(title, self.css, pages)


def document(title, style, pages, extra_css=""):
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>{_e(title)}</title>'
            f"<style>{style}</style>{('<style>' + extra_css + '</style>') if extra_css else ''}</head><body>\n{pages}\n</body></html>")


SHEET_CSS = """
@page { size: auto; margin: 0; }
body { background: #e9edf3; display: grid; grid-template-columns: repeat(@COLS, max-content); gap: 0.12in; padding: 0.12in; width: max-content; margin: 0; counter-reset: s; }
.slide { zoom: @ZOOM; margin: 0 !important; counter-increment: s; box-shadow: 0 0 0 1px #c5ccd8; }
.slide::after { content: counter(s, decimal-leading-zero); position: absolute; right: 0.14in; top: 0.1in; font: 700 26pt sans-serif; color: rgba(34,64,142,0.5); z-index: 9; }
.slide[data-label]::after { content: attr(data-label); font-size: 20pt; }
"""


def sheet_page(deck_html, cols, zoom):
    """The deck's HTML laid out cols per row at the given zoom, for a screenshot."""
    extra = SHEET_CSS.replace("@COLS", str(cols)).replace("@ZOOM", str(zoom))
    return deck_html.replace("</head>", f"<style>{extra}</style></head>", 1)


# ---------------------------------------------------------------- browser routes

MEASURE_JS = r"""
(() => {
  const FILL = window.__fill || 0.5;
  const out = { fill_threshold: FILL, findings: 0, slides: [] };
  const rect = (el) => el.getBoundingClientRect();
  const pathOf = (el) => { const p = el.closest("[data-path]"); return p ? p.dataset.path : ""; };
  const textLeaves = (root) => [...root.querySelectorAll("*")].filter((el) => {
    if (el.tagName === "SCRIPT" || el.tagName === "STYLE") return false;
    for (const n of el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) return true;
    return false;
  });
  // the line boxes of an element's text: rects that overlap vertically are one line, whatever their type size
  const lineBoxes = (el) => {
    const rects = []; const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    for (let n; (n = walk.nextNode()); ) { const rg = document.createRange(); rg.selectNodeContents(n); for (const b of rg.getClientRects()) if (b.width > 0.5 && b.height > 0.5) rects.push({ top: b.top, bottom: b.bottom, width: b.width }); }
    rects.sort((a, b) => a.top - b.top);
    const lines = [];
    for (const r of rects) {
      const L = lines[lines.length - 1];
      if (L && Math.min(L.bottom, r.bottom) - Math.max(L.top, r.top) > 0.5 * Math.min(L.bottom - L.top, r.bottom - r.top)) { L.width += r.width; L.top = Math.min(L.top, r.top); L.bottom = Math.max(L.bottom, r.bottom); }
      else lines.push({ top: r.top, bottom: r.bottom, width: r.width });
    }
    return lines;
  };
  document.querySelectorAll("section.slide").forEach((s, i) => {
    const r = { n: i + 1, kind: s.classList.contains("cover") ? "cover" : s.classList.contains("closing") ? "closing" : "content",
      overflow: [], cut: [], overlaps: [], lone_words: [], wrapped_values: [] };
    const sr = rect(s);
    const content = s.querySelector(".content");
    const body = s.querySelector(".body");
    const cr = content ? rect(content) : null;
    for (const el of s.querySelectorAll("[data-path], .header, .footer, .pageno")) {
      const er = rect(el); if (er.width === 0 && er.height === 0) continue;
      const path = el.dataset.path || pathOf(el) || el.className;
      if (er.right > sr.right + 2 || er.bottom > sr.bottom + 2 || er.left < sr.left - 2 || er.top < sr.top - 2)
        r.overflow.push({ path, where: "beyond the page", by: Math.round(Math.max(er.right - sr.right, er.bottom - sr.bottom)) });
      else if (cr && el.dataset.path && er.bottom > cr.bottom + 2)
        r.overflow.push({ path, where: "below the content frame", by: Math.round(er.bottom - cr.bottom) });
    }
    for (const el of s.querySelectorAll("*")) {
      const cs = getComputedStyle(el);
      if ((cs.overflowX === "hidden" || cs.overflowY === "hidden") && el.tagName !== "SECTION" && el.innerText && el.innerText.trim()) {
        if (el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2)
          r.cut.push({ path: pathOf(el), text: el.innerText.trim().slice(0, 30), by: Math.max(el.scrollHeight - el.clientHeight, el.scrollWidth - el.clientWidth) });
      }
    }
    const leaves = textLeaves(s).map((el) => ({ el, r: rect(el) })).filter((x) => x.r.width > 0 && x.r.height > 0);
    for (let a = 0; a < leaves.length; a++) for (let b = a + 1; b < leaves.length; b++) {
      const A = leaves[a], B = leaves[b];
      if (A.el.contains(B.el) || B.el.contains(A.el)) continue;
      const w = Math.min(A.r.right, B.r.right) - Math.max(A.r.left, B.r.left), h = Math.min(A.r.bottom, B.r.bottom) - Math.max(A.r.top, B.r.top);
      if (w > 2 && h > 2) r.overlaps.push({ path: pathOf(A.el) || pathOf(B.el), a: A.el.innerText.trim().slice(0, 30), b: B.el.innerText.trim().slice(0, 30) });
    }
    if (body && r.kind === "content") {
      const br = rect(body); let low = br.top, high = br.bottom;
      for (const el of body.children) { const e = rect(el); if (e.height === 0) continue; low = Math.max(low, e.bottom); high = Math.min(high, e.top); }
      r.fill = br.height > 0 && low > high ? Math.round(((low - high) / br.height) * 100) / 100 : 0;
      if (r.fill < FILL && !body.querySelector(".toc")) r.under_filled = true;  // the contents slide is exempt
    }
    for (const el of s.querySelectorAll(".facts dd, .row .t, .nt, .st, .header h1, .kpi .kv, .gantt .gbar, .toc .tt, .stack .lab, .card h3, .steps .st2")) {
      const lines = lineBoxes(el); if (lines.length < 2) continue;
      if (el.matches(".facts dd, .row .t, .kpi .kv, .gantt .gbar, .stack .lab")) {
        if (!el.matches(".facts dd") || !el.querySelector("br")) r.wrapped_values.push({ path: pathOf(el), text: el.innerText.trim().slice(0, 30), lines: lines.length });
        continue;
      }
      const text = el.innerText.trim(); const words = text.split(/\s+/); if (words.length < 2) continue;
      const last = words[words.length - 1];
      let lastNode = null; const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      for (let n; (n = walk.nextNode()); ) if (n.textContent.trim()) lastNode = n;
      if (!lastNode) continue; const idx = lastNode.textContent.lastIndexOf(last); if (idx < 0) continue;
      const rg = document.createRange(); rg.setStart(lastNode, idx); rg.setEnd(lastNode, idx + last.length);
      const wr = rg.getBoundingClientRect(); const lw = lines[lines.length - 1].width;
      if (lw > 0 && Math.abs(lw - wr.width) < 3) r.lone_words.push({ path: pathOf(el), text: text.slice(0, 30), word: last });
    }
    r.findings = r.overflow.length + r.cut.length + r.overlaps.length + r.lone_words.length + r.wrapped_values.length + (r.under_filled ? 1 : 0);
    out.findings += r.findings;
    out.slides.push(r);
  });
  return out;
})()
"""

NODE_SCRIPT = r"""// Written by render.py: pdf | report | shot with playwright-core and an installed browser.
import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";
const require = createRequire(process.env.PLAYWRIGHT_FROM);
const { chromium } = require("playwright-core");
const [cmd, input, out, extra, extra2] = process.argv.slice(2);
async function launch() {
  for (const channel of ["chrome", "msedge", "chromium"]) {
    try { return await chromium.launch(channel === "chromium" ? {} : { channel }); } catch {}
  }
  throw new Error("no Chromium-family browser found: install Chrome or Edge, or run npx playwright install chromium");
}
const browser = await launch();
try {
  const ctx = await browser.newContext({ viewport: { width: Number(extra2) || 1300, height: 900 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto("file:///" + path.resolve(input).replace(/\\/g, "/"), { waitUntil: "networkidle" });
  await page.evaluate("document.fonts.ready");
  await page.waitForTimeout(300);
  if (cmd === "pdf") {
    await page.pdf({ path: out, width: "13.333in", height: "7.5in", printBackground: true, preferCSSPageSize: true });
  } else if (cmd === "report") {
    await page.evaluate(`window.__fill = ${Number(extra) || 0.5}`);
    const result = await page.evaluate(fs.readFileSync(process.env.DECK_MEASURE, "utf8"));
    fs.writeFileSync(out, JSON.stringify(result, null, 1));
  } else if (cmd === "shot") {
    await page.screenshot({ path: out, fullPage: true });
  } else {
    throw new Error("unknown command " + cmd);
  }
} finally {
  await browser.close();
}
"""


def _tools_dir():
    base = os.environ.get("DECK_TOOLS")
    if not base:
        if sys.platform.startswith("win"):
            base = os.path.join(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir(), "html-deck-tools")
        else:
            base = os.path.join(os.environ.get("XDG_CACHE_HOME") or os.path.join(os.path.expanduser("~"), ".cache"), "html-deck-tools")
    os.makedirs(base, exist_ok=True)
    return base


def _playwright_core():
    """The package.json of a project that has playwright-core, for createRequire; installs one into the tools folder when none."""
    pf = os.environ.get("PLAYWRIGHT_FROM")
    if pf and os.path.exists(os.path.join(os.path.dirname(pf), "node_modules", "playwright-core")):
        return pf
    tools = _tools_dir()
    pkg = os.path.join(tools, "package.json")
    if os.path.exists(os.path.join(tools, "node_modules", "playwright-core")):
        return pkg
    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm:
        return None
    if not os.path.exists(pkg):
        with open(pkg, "w", encoding="utf-8") as f:
            f.write('{"name": "html-deck-tools", "private": true}\n')
    print(f"browser: installing playwright-core into {tools} (no browser download)")
    try:
        subprocess.run([npm, "install", "playwright-core", "--no-fund", "--no-audit", "--loglevel=error"], cwd=tools, check=True, timeout=300)
    except (subprocess.SubprocessError, OSError) as exc:
        print(f"browser: playwright-core install failed ({exc})")
        return None
    return pkg if os.path.exists(os.path.join(tools, "node_modules", "playwright-core")) else None


def find_browser():
    env = os.environ.get("CHROME")
    if env and os.path.exists(env):
        return env
    for name in ("google-chrome", "google-chrome-stable", "chrome", "chromium", "chromium-browser", "msedge", "microsoft-edge"):
        p = shutil.which(name)
        if p:
            return p
    cands = []
    if sys.platform.startswith("win"):
        for root in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)"), os.environ.get("LocalAppData")):
            if root:
                cands += [os.path.join(root, "Google", "Chrome", "Application", "chrome.exe"),
                          os.path.join(root, "Microsoft", "Edge", "Application", "msedge.exe")]
    elif sys.platform == "darwin":
        cands += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
                  "/Applications/Chromium.app/Contents/MacOS/Chromium"]
    return next((c for c in cands if os.path.exists(c)), None)


def choose_route(prefer=None):
    """The first browser route the host has: ("python", None), ("node", package.json), ("bare", browser path), or (None, None)."""
    order = [prefer] if prefer else ["python", "node", "bare"]
    for r in order:
        if r == "python":
            try:
                import playwright.sync_api  # noqa: F401
                return "python", None
            except ImportError:
                continue
        if r == "node":
            if shutil.which("node"):
                pf = _playwright_core()
                if pf:
                    return "node", pf
            continue
        if r == "bare":
            b = find_browser()
            if b:
                return "bare", b
    return None, None


def describe_route(route, info):
    return {"python": "python-playwright", "node": f"node playwright-core from {os.path.dirname(info)}", "bare": f"{info} (bare: no layout report)"}.get(route, "none")


def _rmtree(path):
    def onerr(fn, p, exc):
        try:
            os.chmod(p, stat.S_IWRITE)
            fn(p)
        except OSError:
            pass
    shutil.rmtree(path, onerror=onerr)


def _url(path):
    return pathlib.Path(path).resolve().as_uri()


def browser_task(route, info, cmd, html_path, out_path, fill=0.55, width=1300, height=900):
    """cmd: pdf | report | shot. Returns True when the file was written."""
    if route == "python":
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = None
            for channel in ("chrome", "msedge", None):
                try:
                    b = p.chromium.launch(channel=channel) if channel else p.chromium.launch()
                    break
                except Exception:
                    continue
            if b is None:
                raise RuntimeError("no Chromium-family browser found: install Chrome or Edge, or run playwright install chromium")
            ctx = b.new_context(viewport={"width": width, "height": 900}, device_scale_factor=1)
            pg = ctx.new_page()
            pg.goto(_url(html_path), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(300)
            if cmd == "pdf":
                pg.pdf(path=out_path, width="13.333in", height="7.5in", print_background=True, prefer_css_page_size=True)
            elif cmd == "report":
                pg.evaluate(f"window.__fill = {fill}")
                data = pg.evaluate(MEASURE_JS)
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=1)
            else:
                pg.screenshot(path=out_path, full_page=True)
            b.close()
        return os.path.exists(out_path)
    if route == "node":
        tools = _tools_dir()
        script = os.path.join(tools, "deck-browser.mjs")
        measure = os.path.join(tools, "measure.js")
        with open(script, "w", encoding="utf-8") as f:
            f.write(NODE_SCRIPT)
        with open(measure, "w", encoding="utf-8") as f:
            f.write(MEASURE_JS)
        env = {**os.environ, "PLAYWRIGHT_FROM": info, "DECK_MEASURE": measure}
        subprocess.run(["node", script, cmd, os.path.abspath(html_path), os.path.abspath(out_path), str(fill), str(width)], check=True, env=env, timeout=300)
        return os.path.exists(out_path)
    if route == "bare":
        if cmd == "report":
            return False
        profile = tempfile.mkdtemp(prefix="deck-")
        args = [info, "--headless=new", "--disable-gpu", "--no-first-run", f"--user-data-dir={profile}", "--hide-scrollbars"]
        if cmd == "pdf":
            args += ["--no-pdf-header-footer", f"--print-to-pdf={os.path.abspath(out_path)}"]
        else:
            args += [f"--window-size={width},{height}", f"--screenshot={os.path.abspath(out_path)}"]
        try:
            subprocess.run(args + [_url(html_path)], check=False, timeout=180, capture_output=True)
        finally:
            _rmtree(profile)
        return os.path.exists(out_path)
    return False


def print_pdf(route, info, html_path, pdf_path):
    if not route:
        print("pdf: skipped (no browser route: install Chrome or Edge, or Playwright; or print the HTML from a browser at 13.333in x 7.5in with backgrounds on)")
        return False
    ok = browser_task(route, info, "pdf", html_path, pdf_path)
    print("pdf:", pdf_path if ok else "failed")
    return ok


def layout_report(route, info, html_path, json_path, fill):
    if route not in ("python", "node"):
        print("report: skipped (the layout report needs Playwright from Python or playwright-core from Node; the review relies on the sheet)")
        return None
    browser_task(route, info, "report", html_path, json_path, fill=fill)
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    print(f"report: {data['findings']} finding(s) -> {json_path}")
    for s in data["slides"]:
        for o in s["overflow"]:
            print(f"  - slide {s['n']} {o['path']}: {o['where']} by {o['by']}px")
        for c in s["cut"]:
            print(f"  - slide {s['n']} {c['path']}: text cut inside its box by {c['by']}px: {c['text']}")
        for o in s["overlaps"]:
            print(f"  - slide {s['n']} {o['path']}: overlap: {o['a']} / {o['b']}")
        for w in s["lone_words"]:
            print(f"  - slide {s['n']} {w['path']}: lone word on the last line: {w['word']} in: {w['text']}")
        for w in s["wrapped_values"]:
            print(f"  - slide {s['n']} {w['path']}: wraps to {w['lines']} lines: {w['text']}")
        if s.get("under_filled"):
            print(f"  - slide {s['n']}: filled {s['fill']:.2f} of the body, under {data['fill_threshold']}")
    return data


def contact_sheet(route, info, html_path, pdf_path, png_path, cols=3, zoom=0.315):
    """From the PDF with PyMuPDF where it is installed, else from the HTML through the browser route."""
    if pdf_path and os.path.exists(pdf_path):
        try:
            import fitz  # PyMuPDF
            src = fitz.open(pdf_path)
            n = src.page_count
            pw, ph = src[0].rect.width, src[0].rect.height
            gap = 12
            rows = -(-n // cols)
            sheet = fitz.open()
            page = sheet.new_page(width=cols * pw + (cols + 1) * gap, height=rows * ph + (rows + 1) * gap)
            for i in range(n):
                r, c = divmod(i, cols)
                x, y = gap + c * (pw + gap), gap + r * (ph + gap)
                page.show_pdf_page(fitz.Rect(x, y, x + pw, y + ph), src, i)
            page.get_pixmap(dpi=55).save(png_path)
            print("sheet:", png_path, f"({n} pages, {cols} per row, from the pdf)")
            return True
        except ImportError:
            pass
    if not route:
        print("sheet: skipped (no PyMuPDF and no browser route)")
        return False
    with open(html_path, encoding="utf-8") as f:
        deck = f.read()
    n = deck.count('<section class="slide')
    sheet_html = os.path.splitext(png_path)[0] + ".html"
    with open(sheet_html, "w", encoding="utf-8") as f:
        f.write(sheet_page(deck, cols, zoom))
    rows = -(-max(n, 1) // cols)
    width = int(cols * PAGE_W * zoom * 96 + (cols + 1) * 12) + 20
    height = int(rows * PAGE_H * zoom * 96 + (rows + 1) * 12) + 20
    ok = browser_task(route, info, "shot", sheet_html, png_path, width=width, height=height)
    print("sheet:", png_path if ok else "failed", f"({n} pages, {cols} per row, from the html)")
    return ok


def single_page(route, info, html_path, n, png_path):
    """One slide at full size (1280 by 720 pixels), for a closer look at a suspect page."""
    if not route:
        print("page: skipped (no browser route)")
        return False
    with open(html_path, encoding="utf-8") as f:
        deck = f.read()
    extra = (f'@page {{ size: auto; margin: 0; }} body {{ margin: 0; padding: 0; background: #fff; width: 13.333in; }} '
             f'.slide {{ margin: 0 !important; }} .slide:not([data-slide="{n}"]) {{ display: none; }}')
    page_html = os.path.splitext(png_path)[0] + ".html"
    with open(page_html, "w", encoding="utf-8") as f:
        f.write(deck.replace("</head>", f"<style>{extra}</style></head>", 1))
    ok = browser_task(route, info, "shot", page_html, png_path, width=1280, height=720)
    print("page:", png_path if ok else "failed", f"(slide {n})")
    return ok


def look_sheet(spec, theme, out_html, out_png, route, info, body_index=None):
    """The cover and one body slide in the recommended register and in the other, two per row."""
    meta = spec.get("meta", {})
    slides = spec["slides"]
    rec = "report" if meta.get("register") == "report" else "proposal"
    other = "proposal" if rec == "report" else "report"
    cover_i = next((i for i, s in enumerate(slides) if s.get("type") == "cover"), None)
    if body_index is None:
        rich = ("table", "gantt", "kpi", "facts", "timeline", "columns")
        body_index = next((i for i, s in enumerate(slides) if s.get("type", "content") == "content"
                           and any(b.get("kind") in rich for b in s.get("blocks", []))), None)
        if body_index is None:
            body_index = next((i for i, s in enumerate(slides) if s.get("type", "content") == "content"), None)
    pages = []
    for reg, label in ((rec, f"{rec} (recommended)"), (other, other)):
        rd = Renderer(theme, reg)
        rd.prepare(spec)
        m = {**meta, "register": reg}
        if cover_i is not None:
            pages.append(rd.slide(slides[cover_i], m, cover_i, label))
        if body_index is not None:
            pages.append(rd.slide(slides[body_index], m, body_index, label))
    doc = sheet_page(document("look", Renderer(theme, rec).css, "\n".join(pages)), 2, 0.47)
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(doc)
    print("look html:", out_html, f"(register {rec} recommended, body slide {body_index})")
    if not route:
        print("look: skipped (no browser route); open the look html in a browser instead")
        return False
    rows = -(-len(pages) // 2)
    width = int(2 * PAGE_W * 0.47 * 96 + 3 * 12) + 20
    height = int(rows * PAGE_H * 0.47 * 96 + (rows + 1) * 12) + 20
    ok = browser_task(route, info, "shot", out_html, out_png, width=width, height=height)
    print("look:", out_png if ok else "failed")
    return ok


def main(argv):
    global BASE_DIR
    sys.stdout.reconfigure(encoding="utf-8")  # a Windows console otherwise stops at the first character it cannot encode
    args = argv[1:]
    if len(args) < 2:
        print(__doc__)
        return 2

    def opt(name, default=None):
        return args[args.index(name) + 1] if name in args else default

    spec = json.load(open(args[0], encoding="utf-8"))
    BASE_DIR = os.path.dirname(os.path.abspath(args[0]))
    meta = spec.get("meta", {})
    if meta.get("external") and "--no-check" not in args and "--look" not in args:
        probs = check_style(spec)
        if probs:
            print("house-style check failed:")
            for p in probs:
                print("  -", p)
            return 1
        print("house-style check passed")
    theme = {**DEFAULT_THEME, **meta.get("theme", {})}
    out_html = args[1]
    needs_browser = any(k in args for k in ("--pdf", "--report", "--sheet", "--look"))
    route, info = (choose_route(opt("--route")) if needs_browser else (None, None))
    if needs_browser:
        print("browser:", describe_route(route, info))
    if "--look" in args:
        bi = opt("--look-slide")
        return 0 if look_sheet(spec, theme, out_html, opt("--look"), route, info, int(bi) if bi is not None else None) else 1
    register = meta.get("register", "proposal")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(Renderer(theme, register).html(spec))
    print("html:", out_html, f"({len(spec['slides'])} slides, register {register})")
    pdf = opt("--pdf")
    if "--report" in args:
        layout_report(route, info, out_html, opt("--report"), float(opt("--fill", 0.5)))
    if pdf:
        print_pdf(route, info, out_html, pdf)
    if "--sheet" in args:
        contact_sheet(route, info, out_html, pdf, opt("--sheet"))
    if "--page" in args:
        n = int(opt("--page"))
        png = args[args.index("--page") + 2]
        single_page(route, info, out_html, n, png)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
