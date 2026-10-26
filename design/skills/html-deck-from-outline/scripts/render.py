# -*- coding: utf-8 -*-
"""Render a deck file (see ../references/deck-spec.md) to one HTML file, and print it to PDF.

Usage:  python render.py <deck.json> <out.html> [--pdf <out.pdf>] [--no-check]

- One slide is one 13.333in x 7.5in page, on screen and in print.
- Cover: two title lines, one short tagline, the client's logo and then the presenter's at the lower left, four diagonal stripes at the upper right.
  Closing: a dark page with the thanks line, the white logo and the contact lines, all centered.
- Content: the title (a subtitle and a header logo only when the slide declares them), one to three blocks, a page number at the lower right.
- Structure comes from type, rules and real marks: columns / statement / facts / numbered / loop / brand are the editorial blocks;
  cards / banner / bullets / rows / stats / shots / stack / timeline / qa / split / profiles / steps / diagram / gantt / note are the rest.
- Line icons (ICONS) exist for the rare item whose meaning a word does not carry; a named product gets its real logo (an image path), never an icon.
- When meta.external is true, the strings are checked against meta.style before rendering; a failure lists each string.
- The PDF is printed with Playwright's Chromium. Without Playwright the HTML is written and the PDF step is skipped with a message.
"""
import base64
import html
import json
import math
import os
import re
import sys

DEFAULT_THEME = {
    "navy": "#22408E", "steel": "#7089BF", "ink": "#2A3242", "mute": "#5A6478",
    "tint": "#E7EDFA", "tint2": "#D9E2F6", "line": "#E2E8F5", "pale": "#BFD0EC",
    "font": "Pretendard",
    "font_css": "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css",
}
SKIP_KEYS = ("logo", "logo_white", "client_logo", "logos", "symbol", "center_logos", "id", "icon", "font_css")

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
    for path, s in _walk_strings(spec["slides"]):
        for ch, name in forbidden.items():
            if ch in s:
                problems.append(f"{path}: {name} ({ch}) in: {s[:60]}")
        if style.get("no_bracket_heads") and re.match(r"^\s*\[[^\]]+\]", s):
            problems.append(f"{path}: bracket head in: {s[:60]}")
    return problems


def _e(s):
    return html.escape("" if s is None else str(s), quote=False)


def _img_data(path):
    if not path or not os.path.exists(path):
        return None
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = {"svg": "image/svg+xml", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(ext, "image/png")
    with open(path, "rb") as f:
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
.slide { position: relative; width: 13.333in; height: 7.5in; overflow: hidden; margin: 0 auto 0.25in auto; background: linear-gradient(155deg, #FFFFFF 0%, #ECF0F9 100%); page-break-after: always; break-after: page; }
.slide:last-child { margin-bottom: 0; }
@media print { body { background: none; } .slide { margin: 0; } }
.content { position: absolute; left: 0.55in; right: 0.55in; top: 0.42in; bottom: 0.45in; display: flex; flex-direction: column; }
.header { position: relative; padding-left: 0.18in; margin-bottom: 0.3in; }
.header::before { content: ""; position: absolute; left: 0; top: 0.08in; width: 5.5pt; height: 0.5in; background: @STEEL; }
.header h1 { margin: 0; font-size: 26pt; font-weight: 700; color: @NAVY; line-height: 1.2; }
.header h2 { margin: 0.1in 0 0 0.02in; font-size: 14pt; font-weight: 400; color: @MUTE; }
.hlogo { position: absolute; right: 0; top: 0.06in; height: 0.46in; }
.tag { position: absolute; right: 0; top: 0.1in; background: @NAVY; color: #fff; font-size: 12pt; font-weight: 700; padding: 0.06in 0.3in; border-radius: 999px; }
.body { flex: 1; display: flex; flex-direction: column; gap: 0.26in; min-height: 0; }
.body.center { justify-content: center; padding-bottom: 0.3in; }
.note { position: absolute; left: 0.55in; right: 0.55in; bottom: 0.12in; font-size: 10.5pt; color: @MUTE; line-height: 1.35; }
.pageno { position: absolute; right: 0.5in; bottom: 0.26in; font-size: 9.5pt; color: #8A94A8; letter-spacing: 0.05em; }
.ic { display: block; flex: none; }
.idisc { flex: none; width: 0.52in; height: 0.52in; border-radius: 50%; background: @TINT; color: @NAVY; display: flex; align-items: center; justify-content: center; }

/* columns */
.cols { display: grid; align-items: start; }
.cols.stretch { align-items: stretch; }

/* statement */
.statement .st { margin: 0; font-weight: 700; color: @NAVY; line-height: 1.42; letter-spacing: -0.01em; }
.statement .st b { color: @STEEL; margin-right: 0.16in; }
.statement .sb { margin: 0.24in 0 0; font-size: 13.5pt; color: @INK; line-height: 1.6; }

/* facts (definition list) */
.facts { display: grid; }
.facts .f { display: grid; column-gap: 0.2in; padding: 0.13in 0; border-top: 1px solid #C9D1E3; }
.facts .f:last-child { border-bottom: 1px solid #C9D1E3; }
.facts dt { margin: 0; font-size: 11.5pt; color: @MUTE; padding-top: 0.03in; }
.facts dd { margin: 0; font-size: 14pt; font-weight: 600; color: @INK; line-height: 1.4; }
.facts.inline { grid-auto-flow: column; column-gap: 0.4in; border-top: 1px solid #C9D1E3; padding-top: 0.14in; }
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

/* loop */
.loop { position: relative; }
.loop svg { position: absolute; left: 0; top: 0; width: 100%; height: 100%; }
.loop .ln { position: absolute; transform: translate(-50%, -50%); background: #fff; border: 1px solid #C9D1E3; border-radius: 0.1in; padding: 0.1in 0.14in; text-align: center; }
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
.row .no { width: 0.34in; height: 0.34in; border-radius: 50%; background: @NAVY; color: #fff; font-weight: 700; font-size: 12pt; display: flex; align-items: center; justify-content: center; margin-left: 0.18in; }
.row .no.opt { background: @STEEL; }
.row .idisc { width: 0.44in; height: 0.44in; margin-left: 0.14in; }
.row .t { font-size: 13.5pt; font-weight: 700; padding-right: 0.2in; }
.row .d { font-size: 12pt; color: @MUTE; line-height: 1.4; }
.row .chip { margin-left: 0.2in; font-size: 11.5pt; font-weight: 700; padding: 0.05in 0.25in; border-radius: 999px; background: @TINT2; color: @NAVY; }
.row .chip.basic { background: @NAVY; color: #fff; }

.ticks { list-style: none; margin: 0; padding: 0; }
.ticks li { line-height: 1.45; }
.ticks li::before { content: "|  "; color: @STEEL; font-weight: 700; }
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
.tentry .when { font-size: 12pt; font-weight: 700; color: @STEEL; }
.tentry .ttl { font-size: 16pt; font-weight: 700; color: @NAVY; margin: 0.03in 0 0.12in 0; }
.tentry .ticks li { font-size: 12.5pt; margin-bottom: 0.06in; }

.qa .q { font-size: 16pt; font-weight: 700; color: @NAVY; margin: 0 0 0.08in 0; }
.qa .a { font-size: 12.5pt; line-height: 1.45; margin: 0 0 0.3in 0; }

.split { flex: 1; display: grid; column-gap: 0.25in; min-height: 0; }
.shots { display: flex; flex-direction: column; gap: 0.2in; height: 100%; }
.shot { flex: 1; background: #F4F6FB; border: 1.1pt solid @STEEL; border-radius: 0.06in; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 0.2in; }
.shot .lb { font-size: 12pt; font-weight: 700; color: @STEEL; }
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
.profile .pr .v div { border-left: 1.5pt solid #C9D1E3; padding-left: 0.16in; font-size: 12.5pt; line-height: 1.35; margin-bottom: 0.07in; }

/* steps */
.steps { display: flex; align-items: center; gap: 0.07in; }
.step { flex: 1; display: flex; align-items: center; gap: 0.09in; background: #fff; border: 1px solid @LINE; border-radius: 999px; padding: 0.1in 0.14in; font-size: 11pt; font-weight: 700; color: @INK; line-height: 1.2; }
.step .n { flex: none; width: 0.3in; height: 0.3in; border-radius: 50%; background: @NAVY; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 10.5pt; }
.step .ic { color: @STEEL; }
.sa { color: @STEEL; font-size: 15pt; line-height: 1; flex: none; }
.steps.tiles .step { flex-direction: column; border-radius: 0.14in; padding: 0.12in 0.1in; text-align: center; gap: 0.07in; align-self: stretch; justify-content: flex-start; }
.steps.tiles .sh { display: flex; align-items: center; gap: 0.08in; }
.steps.tiles .sl { font-size: 11pt; line-height: 1.25; }

/* diagram */
.diagram { height: 100%; background: #fff; border: 1px solid @LINE; border-radius: 0.1in; padding: 0.3in 0.25in; display: grid; grid-template-columns: 1.35in 0.45in 1fr 0.45in 1.35in; grid-template-rows: auto 0.4in auto 0.4in auto; column-gap: 0.08in; align-items: center; align-content: center; }
.dn { border: 1px solid @PALE; background: @TINT; border-radius: 0.1in; padding: 0.14in 0.16in; text-align: center; }
.dn.accent { background: @NAVY; color: #fff; border-color: @NAVY; }
.dn.strong { background: #fff; border: 2pt solid @NAVY; }
.dn h4 { margin: 0 0 0.05in 0; font-size: 12.5pt; display: flex; align-items: center; justify-content: center; gap: 0.08in; }
.dn h4 .ic { color: @STEEL; }
.dn.accent h4 .ic { color: #fff; }
.dn p { margin: 0; font-size: 10.5pt; line-height: 1.35; color: inherit; opacity: 0.9; }
.dn .chips { display: flex; justify-content: center; gap: 0.05in; margin-bottom: 0.08in; }
.dn .chips i { font-style: normal; width: 0.24in; height: 0.24in; border-radius: 50%; background: @NAVY; color: #fff; font-size: 9pt; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.dn.accent .chips i { background: #fff; color: @NAVY; }
.dn .nl { display: flex; justify-content: center; align-items: center; gap: 0.14in; margin-bottom: 0.08in; }
.dn .nl img { height: 0.34in; }
.arrow { text-align: center; font-size: 10pt; color: @MUTE; line-height: 1.1; }
.arrow span { display: block; font-size: 18pt; color: @STEEL; line-height: 1; }
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
.gantt .gmonths { display: grid; border-bottom: 1px solid #C9D1E3; }
.gantt .gmonths div { font-size: 11.5pt; font-weight: 700; color: @NAVY; padding: 0 0 0.08in 0.1in; border-left: 1px solid @LINE; }
.gantt .gl { font-size: 13pt; font-weight: 700; color: @INK; display: flex; align-items: center; height: 0.6in; padding-right: 0.2in; }
.gantt .gt { position: relative; height: 0.6in; background-image: linear-gradient(to right, @LINE 1px, transparent 1px); }
.gantt .gbar { position: absolute; top: 0.12in; height: 0.36in; border-radius: 0.18in; display: flex; align-items: center; padding: 0 0.16in; font-size: 11pt; white-space: nowrap; overflow: hidden; }
.gantt .gms { position: absolute; top: 0; height: 100%; }
.gantt .gms i { position: absolute; top: 0.19in; left: -0.11in; width: 0.22in; height: 0.22in; background: @NAVY; transform: rotate(45deg); }
.gantt .gms span { position: absolute; right: 0.2in; top: 0.16in; font-size: 12pt; font-weight: 700; color: @NAVY; white-space: nowrap; }

/* cover */
.cover .stripe { position: absolute; border-radius: 999px; transform: rotate(40deg); }
.cover .ttl { position: absolute; left: 0.75in; top: 2.05in; width: 10.5in; }
.cover .ttl h1 { margin: 0; font-size: 50pt; font-weight: 700; color: @NAVY; line-height: 1.22; }
.cover .tagline { margin: 0.35in 0 0 0.03in; font-size: 16pt; color: @MUTE; }
.cover .logos { position: absolute; left: 0.75in; top: 5.5in; display: flex; align-items: center; gap: 0.3in; }
.cover .logos img { height: 0.36in; display: block; }
.cover .logos img.client { height: 0.4in; }
.cover .logos .sep { width: 1px; height: 0.42in; background: #B9C3D6; }
.cover .foot { position: absolute; left: 0.75in; top: 6.2in; font-size: 12pt; font-weight: 700; color: @MUTE; }

/* closing */
.closing { background: @NAVY; }
.closing h1 { position: absolute; left: 0; right: 0; top: 2.75in; margin: 0; text-align: center; font-size: 44pt; font-weight: 700; color: #fff; }
.closing .logo { position: absolute; left: 50%; transform: translateX(-50%); top: 5.15in; height: 0.3in; }
.closing .contact { position: absolute; left: 0; right: 0; top: 5.65in; text-align: center; font-size: 12pt; color: #C9D4EE; line-height: 1.6; }
"""


def css(t):
    out = CSS_T.replace("@FONT_IMPORT", f"@import url('{t['font_css']}');" if t.get("font_css") else "")
    for key in ("navy", "steel", "ink", "mute", "tint2", "tint", "line", "pale", "font"):
        out = out.replace("@" + key.upper(), t[key])
    return out


class Renderer:
    def __init__(self, theme):
        self.t = theme
        self.css = css(theme)
        self.step = [theme["tint"], theme["pale"], theme["steel"], theme["navy"]]
        # cover stripes: (center x, center y, width, length, color) in inches
        self.stripes = [
            (5.3, 0.85, 0.9, 2.4, theme["tint2"]),
            (9.3, 2.1, 0.85, 6.1, theme["line"]),
            (8.7, 4.2, 1.05, 6.2, theme["tint"]),
            (9.9, 4.7, 0.75, 3.1, theme["steel"]),
        ]

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

    def columns(self, blk):
        inner = "".join(f'<div class="col">{self.block(b)}</div>' for b in blk["blocks"])
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

    def loop(self, blk):
        """Four nodes (top, right, bottom, left) joined clockwise by a ring; logos and a caption at the center.
        width, height and r (ring radius) are inches; node_w and center_w are the node and caption widths."""
        w, h, r = blk.get("width", 4.6), blk.get("height", 4.0), blk.get("r", 1.45)
        cx, cy, sc = w / 2, h / 2, 100
        heads = []
        for deg in (-45, 45, 135, 225):
            th = math.radians(deg)
            x, y = (cx + r * math.cos(th)) * sc, (cy + r * math.sin(th)) * sc
            heads.append(f'<path d="M-9,-6 L9,0 L-9,6 Z" fill="{self.t["steel"]}" transform="translate({x:.1f},{y:.1f}) rotate({deg + 90})"/>')
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
        for it in blk["items"]:
            inner = f'<p>{_e(it["body"])}</p>' if it.get("body") else ""
            if it.get("items"):
                inner += self.ticks(it["items"])
            if blk.get("icon_pos") == "inline":
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
        rows = []
        for i, it in enumerate(blk["items"]):
            tag = it.get("tag")
            basic = blk.get("basic_tag", "기본")
            opt = " opt" if tag and tag != basic else ""
            chip = f'<span class="chip{" basic" if tag == basic else ""}">{_e(tag)}</span>' if tag else "<span></span>"
            lead = _disc(it["icon"], 0.26) if it.get("icon") else f'<div class="no{opt}">{it.get("no", i + 1)}</div>'
            rows.append(f'<div class="row" style="min-height:{rh}in">{lead}'
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
            fg = "#fff" if c in (self.t["steel"], self.t["navy"]) else self.t["navy"]
            cells.append(f'<div class="lab" style="background:{c};color:{fg};min-height:{rh}in;grid-row:{i + 1}">{_e(it["label"])}</div>'
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
        return '<div class="qa">' + "".join(f'<p class="q">Q. {_e(it["q"])}</p><p class="a">{_e(it["a"])}</p>' for it in blk["items"]) + "</div>"

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
        """Strings render as pills in one line; items with icons, or style: tiles, render as tiles (number above the label)."""
        tiles = blk.get("style") == "tiles" or any(isinstance(s, dict) and s.get("icon") for s in blk["items"])
        parts = []
        for i, s in enumerate(blk["items"]):
            if i:
                parts.append('<div class="sa">&#8594;</div>')
            label, icon = (s, None) if isinstance(s, str) else (s["label"], s.get("icon"))
            if tiles:
                parts.append(f'<div class="step"><div class="sh"><span class="n">{i + 1}</span>{_icon(icon, 0.28)}</div><span class="sl">{_e(label)}</span></div>')
            else:
                parts.append(f'<div class="step"><span class="n">{i + 1}</span>{_icon(icon, 0.26)}<span>{_e(label)}</span></div>')
        return f'<div class="steps{" tiles" if tiles else ""}">{"".join(parts)}</div>'

    def gantt(self, blk):
        months = blk["months"]
        n = len(months)
        t = self.t
        tones = {"tint": (t["tint"], t["navy"]), "pale": (t["pale"], t["navy"]), "steel": (t["steel"], "#fff"), "navy": (t["navy"], "#fff")}
        head = "".join(f"<div>{_e(m)}</div>" for m in months)
        out = [f'<div class="gantt"><div></div><div class="gmonths" style="grid-template-columns:repeat({n},1fr)">{head}</div>']
        for r in blk["rows"]:
            out.append(f'<div class="gl">{_e(r["label"])}</div>')
            track = ""
            if "start" in r:
                bg, fg = tones.get(r.get("tone", "navy"), tones["navy"])
                left = r["start"] / n * 100
                width = (r["end"] - r["start"]) / n * 100
                track += f'<div class="gbar" style="left:{left:.3f}%;width:{width:.3f}%;background:{bg};color:{fg}">{_e(r.get("text", ""))}</div>'
            if "milestone" in r:
                pct = r["milestone"] / n * 100
                mtext = r.get("mtext", "" if "start" in r else r.get("text", ""))
                track += f'<div class="gms" style="left:{pct:.3f}%"><i></i><span>{_e(mtext)}</span></div>'
            out.append(f'<div class="gt" style="background-size:calc(100% / {n}) 100%;">{track}</div>')
        out.append("</div>")
        return "".join(out)

    def diagram(self, d, full=False):
        """Five nodes in a fixed arrangement: source (left), center, service (above), output (right), update (below).
        A node's `logos` (image paths) are drawn above its title. full=True draws it at page width: the top three rows
        inside a dashed frame, the update node below the frame."""
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

    def block(self, blk):
        k = blk["kind"]
        if k == "bullets":
            return self.ticks(blk["items"], blk.get("size", 13), blk.get("gap", 10))
        if k == "shots":
            return self.shots(blk["items"])
        if k == "diagram":
            return self.diagram(blk, full=True)
        if k == "note":
            return ""
        fn = getattr(self, k, None)
        if fn is None or k in ("block", "slide", "html", "ticks"):
            raise ValueError(f"unknown block kind: {k}")
        return fn(blk)

    def slide(self, s, meta, idx):
        t = s.get("type", "content")
        if t == "cover":
            logo = _img_data(meta.get("logo"))
            clogo = _img_data(meta.get("client_logo"))
            stripes = "".join(
                f'<div class="stripe" style="left:{cx - w / 2:.2f}in;top:{cy - l / 2:.2f}in;width:{w}in;height:{l}in;background:{c}"></div>'
                for cx, cy, w, l, c in self.stripes)
            tag = s.get("tagline") or s.get("subtitle") or ""
            logos = (f'<img class="client" src="{clogo}"><span class="sep"></span>' if clogo else "") + (f'<img src="{logo}">' if logo else "")
            foot = ""
            if s.get("footer"):
                foot = '<div class="foot">' + "&nbsp;&nbsp;|&nbsp;&nbsp;".join(_e(v) for v in [meta.get("client"), meta.get("date"), meta.get("brand")] if v) + "</div>"
            return (f'<section class="slide cover">{stripes}'
                    f'<div class="ttl"><h1>{"<br>".join(_e(x) for x in s["title_lines"])}</h1>'
                    + (f'<p class="tagline">{_e(tag)}</p>' if tag else "") + "</div>"
                    + (f'<div class="logos">{logos}</div>' if logos else "") + foot + "</section>")
        if t == "closing":
            logo = _img_data(meta.get("logo_white"))
            return (f'<section class="slide closing"><h1>{_e(s.get("title", "Thank you"))}</h1>'
                    + (f'<img class="logo" src="{logo}">' if logo else "")
                    + f'<div class="contact">{"<br>".join(_e(c) for c in s.get("contact", []))}</div></section>')
        blocks = s.get("blocks", [])
        notes = [b["text"] for b in blocks if b["kind"] == "note"]
        body = "".join(self.block(b) for b in blocks if b["kind"] != "note")
        tag = f'<div class="tag">{_e(s["tag"])}</div>' if s.get("tag") else ""
        hlogo = _img_data(s.get("logo"))
        hlogo = f'<img class="hlogo" src="{hlogo}">' if hlogo else ""
        sub = f'<h2>{_e(s["subtitle"])}</h2>' if s.get("subtitle") else ""
        note = f'<div class="note">{"<br>".join(_e(n) for n in notes)}</div>' if notes else ""
        cls = " center" if s.get("valign") == "center" else ""
        pageno = f'<div class="pageno">{idx + 1:02d}</div>' if meta.get("page_numbers", True) else ""
        return (f'<section class="slide"><div class="content"><div class="header">{tag}{hlogo}<h1>{_e(s["title"])}</h1>{sub}</div>'
                f'<div class="body{cls}">{body}</div></div>{note}{pageno}</section>')

    def html(self, spec):
        meta = spec.get("meta", {})
        slides = spec["slides"]
        title = " ".join(slides[0].get("title_lines", ["deck"])) if slides else "deck"
        pages = "\n".join(self.slide(s, meta, i) for i, s in enumerate(slides))
        return (f'<!doctype html><html><head><meta charset="utf-8"><title>{_e(title)}</title>'
                f"<style>{self.css}</style></head><body>\n{pages}\n</body></html>")


def to_pdf(html_path, pdf_path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("pdf: skipped (Playwright is not installed; print the HTML from a browser at 13.333in x 7.5in with backgrounds on)")
        return
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto("file:///" + os.path.abspath(html_path).replace("\\", "/"))
        pg.wait_for_load_state("networkidle")
        pg.evaluate("document.fonts.ready")
        pg.pdf(path=pdf_path, width="13.333in", height="7.5in", print_background=True, prefer_css_page_size=True)
        b.close()
    print("pdf:", pdf_path)


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    spec = json.load(open(argv[1], encoding="utf-8"))
    meta = spec.get("meta", {})
    if meta.get("external") and "--no-check" not in argv:
        probs = check_style(spec)
        if probs:
            print("house-style check failed:")
            for p in probs:
                print("  -", p)
            return 1
        print("house-style check passed")
    theme = {**DEFAULT_THEME, **meta.get("theme", {})}
    out_html = argv[2]
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(Renderer(theme).html(spec))
    print("html:", out_html, f"({len(spec['slides'])} slides)")
    if "--pdf" in argv:
        to_pdf(out_html, argv[argv.index("--pdf") + 1])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
