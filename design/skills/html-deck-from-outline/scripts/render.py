# -*- coding: utf-8 -*-
"""Render a deck file (see ../references/deck-spec.md) to one HTML file, and print it to PDF.

Usage:  python render.py <deck.json> <out.html> [--pdf <out.pdf>] [--no-check]

- One slide is one 13.333in x 7.5in page, on screen and in print.
- Block kinds: cards / banner / bullets / rows / shots / stack / timeline / qa / note / split (with an optional diagram).
- When meta.external is true, the strings are checked against meta.style before rendering; a failure lists each string.
- The PDF is printed with Playwright's Chromium. Without Playwright the HTML is written and the PDF step is skipped with a message.
"""
import base64
import html
import json
import os
import re
import sys

DEFAULT_THEME = {
    "navy": "#22408E", "steel": "#7089BF", "ink": "#2A3242", "mute": "#5A6478",
    "tint": "#E7EDFA", "tint2": "#D9E2F6", "line": "#E2E8F5", "pale": "#BFD0EC",
    "font": "Pretendard",
    "font_css": "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css",
}
SKIP_KEYS = ("logo", "logo_white", "id", "font_css")


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
    return html.escape(str(s), quote=False)


def _img_data(path):
    if not path or not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def css(t):
    step = [t["tint"], t["pale"], t["steel"], t["navy"]]
    font_import = f"@import url('{t['font_css']}');" if t.get("font_css") else ""
    return f"""
{font_import}
@page {{ size: 13.333in 7.5in; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: #9aa3b5; }}
body {{ font-family: {t['font']}, "Malgun Gothic", "Apple SD Gothic Neo", sans-serif; color: {t['ink']}; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.slide {{ position: relative; width: 13.333in; height: 7.5in; overflow: hidden; margin: 0 auto 0.25in auto; background: linear-gradient(155deg, #FFFFFF 0%, #ECF0F9 100%); page-break-after: always; break-after: page; }}
.slide:last-child {{ margin-bottom: 0; }}
@media print {{ body {{ background: none; }} .slide {{ margin: 0; }} }}
.content {{ position: absolute; left: 0.55in; right: 0.55in; top: 0.42in; bottom: 0.45in; display: flex; flex-direction: column; }}
.header {{ position: relative; padding-left: 0.18in; margin-bottom: 0.22in; }}
.header::before {{ content: ""; position: absolute; left: 0; top: 0.08in; width: 5.5pt; height: 0.5in; background: {t['steel']}; }}
.header h1 {{ margin: 0; font-size: 26pt; font-weight: 700; color: {t['navy']}; line-height: 1.2; }}
.header h2 {{ margin: 0.08in 0 0 0.02in; font-size: 15.5pt; font-weight: 700; color: #3A4356; }}
.tag {{ position: absolute; right: 0; top: 0.1in; background: {t['navy']}; color: #fff; font-size: 12pt; font-weight: 700; padding: 0.06in 0.3in; border-radius: 999px; }}
.body {{ flex: 1; display: flex; flex-direction: column; gap: 0.26in; min-height: 0; }}
.note {{ position: absolute; left: 0.55in; right: 0.55in; bottom: 0.12in; font-size: 10.5pt; color: {t['mute']}; line-height: 1.35; }}
.cards {{ display: grid; gap: 0.25in; }}
.card {{ background: #fff; border: 1px solid {t['line']}; border-radius: 0.09in; padding: 0.22in 0.25in; }}
.card h3 {{ margin: 0 0 0.12in 0; font-size: 15pt; color: {t['navy']}; }}
.card p {{ margin: 0; font-size: 12.5pt; line-height: 1.45; }}
.banner {{ background: {t['tint']}; border-radius: 0.16in; padding: 0.2in 0.35in; display: flex; align-items: center; font-size: 13.5pt; line-height: 1.45; }}
.banner b {{ color: {t['navy']}; margin-right: 0.15in; white-space: nowrap; }}
.rows {{ display: flex; flex-direction: column; gap: 0.12in; }}
.row {{ display: grid; grid-template-columns: 0.72in 3.1in 1fr auto; align-items: center; background: #fff; border: 1px solid {t['line']}; border-radius: 0.14in; padding: 0.1in 0.18in 0.1in 0; }}
.row .no {{ width: 0.34in; height: 0.34in; border-radius: 50%; background: {t['navy']}; color: #fff; font-weight: 700; font-size: 12pt; display: flex; align-items: center; justify-content: center; margin-left: 0.18in; }}
.row .no.opt {{ background: {t['steel']}; }}
.row .t {{ font-size: 13.5pt; font-weight: 700; padding-right: 0.2in; }}
.row .d {{ font-size: 12pt; color: {t['mute']}; line-height: 1.4; }}
.row .chip {{ margin-left: 0.2in; font-size: 11.5pt; font-weight: 700; padding: 0.05in 0.25in; border-radius: 999px; background: {t['tint2']}; color: {t['navy']}; }}
.row .chip.basic {{ background: {t['navy']}; color: #fff; }}
.ticks {{ list-style: none; margin: 0; padding: 0; }}
.ticks li {{ line-height: 1.45; }}
.ticks li::before {{ content: "|  "; color: {t['steel']}; font-weight: 700; }}
.ticks b {{ color: {t['navy']}; }}
.stack {{ display: grid; column-gap: 0.25in; row-gap: 0.14in; align-items: stretch; }}
.stack .lab {{ display: flex; align-items: center; justify-content: center; text-align: center; border-radius: 0.14in; font-size: 14.5pt; font-weight: 700; padding: 0.1in 0.2in; }}
.stack .desc {{ background: #fff; border: 1px solid {t['line']}; border-radius: 0.1in; padding: 0.12in 0.25in; display: flex; align-items: center; font-size: 12pt; line-height: 1.4; }}
.stack .aside {{ grid-column: 3; background: #fff; border: 1px solid {t['line']}; border-radius: 0.08in; padding: 0.2in 0.25in; }}
.stack .aside h3 {{ margin: 0 0 0.15in 0; font-size: 14pt; color: {t['navy']}; }}
.stack .aside .ticks li {{ font-size: 11.5pt; margin-bottom: 0.1in; }}
.stack .aside .ticks b {{ color: {t['ink']}; }}
.timeline {{ flex: 1; display: grid; column-gap: 0.3in; }}
.tcol {{ position: relative; padding-left: 0.3in; }}
.tcol::before {{ content: ""; position: absolute; left: 0.12in; top: 0; bottom: 0; width: 3.5pt; background: {t['pale']}; }}
.tentry {{ position: relative; margin-bottom: 0.25in; }}
.tentry::before {{ content: ""; position: absolute; left: -0.3in; top: 0.1in; width: 0.2in; height: 0.2in; border-radius: 50%; background: {t['navy']}; margin-left: 0.03in; }}
.tentry.opt::before {{ background: {t['steel']}; }}
.tentry .when {{ font-size: 12pt; font-weight: 700; color: {t['steel']}; }}
.tentry .ttl {{ font-size: 16pt; font-weight: 700; color: {t['navy']}; margin: 0.03in 0 0.12in 0; }}
.tentry .ticks li {{ font-size: 12.5pt; margin-bottom: 0.06in; }}
.qa .q {{ font-size: 16pt; font-weight: 700; color: {t['navy']}; margin: 0 0 0.08in 0; }}
.qa .a {{ font-size: 12.5pt; line-height: 1.45; margin: 0 0 0.3in 0; }}
.split {{ flex: 1; display: grid; column-gap: 0.25in; min-height: 0; }}
.shots {{ display: flex; flex-direction: column; gap: 0.2in; height: 100%; }}
.shot {{ flex: 1; background: #F4F6FB; border: 1.1pt solid {t['steel']}; border-radius: 0.06in; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 0.2in; }}
.shot .lb {{ font-size: 12pt; font-weight: 700; color: {t['steel']}; }}
.shot .cap {{ font-size: 11pt; color: {t['mute']}; margin-top: 0.05in; }}
.diagram {{ height: 100%; background: #fff; border: 1px solid {t['line']}; border-radius: 0.1in; padding: 0.3in 0.25in; display: grid; grid-template-columns: 1.35in 0.45in 1fr 0.45in 1.35in; grid-template-rows: auto 0.4in auto 0.4in auto; column-gap: 0.08in; align-items: center; align-content: center; }}
.dn {{ border: 1px solid {t['pale']}; background: {t['tint']}; border-radius: 0.1in; padding: 0.14in 0.16in; text-align: center; }}
.dn.accent {{ background: {t['navy']}; color: #fff; border-color: {t['navy']}; }}
.dn h4 {{ margin: 0 0 0.05in 0; font-size: 12.5pt; }}
.dn p {{ margin: 0; font-size: 10.5pt; line-height: 1.35; color: inherit; opacity: 0.9; }}
.arrow {{ text-align: center; font-size: 10pt; color: {t['mute']}; line-height: 1.1; }}
.arrow span {{ display: block; font-size: 18pt; color: {t['steel']}; line-height: 1; }}
.arrow.v {{ display: flex; align-items: center; justify-content: center; gap: 0.08in; }}
.arrow.v span {{ display: inline; }}
.cover .stripes {{ position: absolute; right: -1.2in; top: -1.6in; width: 6in; height: 11in; transform: rotate(45deg); display: flex; gap: 0.6in; }}
.cover .stripes i {{ display: block; width: 1.05in; border-radius: 0.5in; }}
.cover .ttl {{ position: absolute; left: 0.95in; top: 2.5in; width: 9.5in; }}
.cover .ttl::before {{ content: ""; display: block; width: 1.5in; height: 5pt; background: {t['steel']}; margin-bottom: 0.25in; }}
.cover .ttl h1 {{ margin: 0; font-size: 40pt; font-weight: 700; color: {t['navy']}; line-height: 1.2; }}
.cover .sub {{ position: absolute; left: 0.95in; top: 4.75in; width: 9.5in; font-size: 15pt; color: {t['mute']}; }}
.cover .logo {{ position: absolute; left: 0.95in; top: 6.05in; height: 0.32in; }}
.cover .foot {{ position: absolute; left: 0.95in; top: 6.6in; font-size: 13pt; font-weight: 700; }}
.closing {{ background: {t['navy']}; }}
.closing h1 {{ position: absolute; left: 0.95in; top: 2.7in; margin: 0; font-size: 40pt; color: #fff; }}
.closing .contact {{ position: absolute; left: 0.98in; top: 4.1in; font-size: 14pt; color: #C9D4EE; line-height: 1.6; }}
.closing .logo {{ position: absolute; left: 0.98in; top: 6.5in; height: 0.34in; }}
""", step


class Renderer:
    def __init__(self, theme):
        self.t = theme
        self.css, self.step = css(theme)

    def ticks(self, items, size=None, gap=None):
        style = f"font-size:{size}pt;" if size else ""
        out = [f'<ul class="ticks" style="{style}">']
        for it in items:
            head, body = it[0], (it[1] if len(it) > 1 else "")
            gs = f' style="margin-bottom:{gap}pt"' if gap else ""
            out.append(f"<li{gs}><b>{_e(head)}</b>{('&nbsp;&nbsp;&nbsp;' + _e(body)) if body else ''}</li>")
        out.append("</ul>")
        return "".join(out)

    def cards(self, blk):
        n = blk.get("cols", len(blk["items"]))
        hs = f"min-height:{blk['h']}in;" if blk.get("h") else ""
        cards = "".join(f'<div class="card" style="{hs}"><h3>{_e(it["title"])}</h3><p>{_e(it["body"])}</p></div>' for it in blk["items"])
        return f'<div class="cards" style="grid-template-columns:repeat({n},1fr)">{cards}</div>'

    def banner(self, blk):
        lead = f"<b>{_e(blk['lead'])}</b>" if blk.get("lead") else ""
        return f'<div class="banner" style="min-height:{blk.get("h", 0.95)}in"><div>{lead}{_e(blk.get("body", ""))}</div></div>'

    def rows(self, blk):
        rh = blk.get("row_h", 0.78)
        rows = []
        for i, it in enumerate(blk["items"]):
            tag = it.get("tag")
            opt = " opt" if tag and tag != blk.get("basic_tag", "기본") else ""
            chip = f'<span class="chip{" basic" if tag == blk.get("basic_tag", "기본") else ""}">{_e(tag)}</span>' if tag else "<span></span>"
            rows.append(f'<div class="row" style="min-height:{rh}in"><div class="no{opt}">{it.get("no", i + 1)}</div>'
                        f'<div class="t">{_e(it["title"])}</div><div class="d">{_e(it["desc"])}</div>{chip}</div>')
        return f'<div class="rows">{"".join(rows)}</div>'

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
        cols = "3in 5.6in 1fr" if aside else "3in 1fr"
        return f'<div class="stack" style="grid-template-columns:{cols}">{"".join(cells)}</div>'

    def timeline(self, blk):
        cols = blk["cols"]
        out = [f'<div class="timeline" style="grid-template-columns:repeat({len(cols)},1fr)">']
        for entries in cols:
            out.append('<div class="tcol">')
            for e in entries:
                out.append(f'<div class="tentry{" opt" if e.get("option") else ""}"><div class="when">{_e(e["when"])}</div>'
                           f'<div class="ttl">{_e(e["title"])}</div>{self.ticks([[x] for x in e.get("items", [])])}</div>')
            out.append("</div>")
        out.append("</div>")
        return "".join(out)

    def qa(self, blk):
        return '<div class="qa">' + "".join(f'<p class="q">Q. {_e(it["q"])}</p><p class="a">{_e(it["a"])}</p>' for it in blk["items"]) + "</div>"

    def diagram(self, d):
        nodes = {n["id"]: n for n in d["nodes"]}
        order = [n["id"] for n in d["nodes"]]
        labels = {(a, b): l for a, b, l in d["edges"]}

        def node(nid, extra=""):
            n = nodes[nid]
            return f'<div class="dn{" accent" if n.get("accent") else ""}" style="{extra}"><h4>{_e(n["title"])}</h4><p>{_e(n.get("body", ""))}</p></div>'

        def arrow(txt, extra=""):
            return f'<div class="arrow" style="{extra}"><span>&#8594;</span>{_e(txt)}</div>'

        src, core, aux, out, upd = order[:5]
        return ('<div class="diagram">'
                + node(aux, "grid-column:3;grid-row:1")
                + f'<div class="arrow v" style="grid-column:3;grid-row:2"><span>&#8597;</span>{_e(labels.get((core, aux), ""))}</div>'
                + node(src, "grid-column:1;grid-row:3")
                + arrow(labels.get((src, core), ""), "grid-column:2;grid-row:3")
                + node(core, "grid-column:3;grid-row:3")
                + arrow(labels.get((core, out), ""), "grid-column:4;grid-row:3")
                + node(out, "grid-column:5;grid-row:3")
                + f'<div class="arrow v" style="grid-column:3;grid-row:4"><span>&#8593;</span>{_e(labels.get((upd, core), ""))}</div>'
                + node(upd, "grid-column:3;grid-row:5")
                + "</div>")

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
        if k == "note":
            return ""
        fn = getattr(self, k, None)
        if fn is None:
            raise ValueError(f"unknown block kind: {k}")
        return fn(blk)

    def slide(self, s, meta):
        t = s.get("type", "content")
        if t == "cover":
            logo = _img_data(meta.get("logo"))
            foot = "&nbsp;&nbsp;|&nbsp;&nbsp;".join(_e(v) for v in [meta.get("client"), meta.get("date"), meta.get("brand")] if v)
            stripes = "".join(f'<i style="background:{c}"></i>' for c in [self.t["tint2"], self.t["pale"], self.t["steel"], self.t["tint"]])
            return (f'<section class="slide cover"><div class="stripes">{stripes}</div>'
                    f'<div class="ttl"><h1>{"<br>".join(_e(x) for x in s["title_lines"])}</h1></div>'
                    f'<div class="sub">{_e(s.get("subtitle", ""))}</div>'
                    + (f'<img class="logo" src="{logo}">' if logo else "")
                    + f'<div class="foot">{foot}</div></section>')
        if t == "closing":
            logo = _img_data(meta.get("logo_white"))
            return (f'<section class="slide closing"><h1>{_e(s.get("title", "Thank you"))}</h1>'
                    f'<div class="contact">{"<br>".join(_e(c) for c in s.get("contact", []))}</div>'
                    + (f'<img class="logo" src="{logo}">' if logo else "") + "</section>")
        blocks = s.get("blocks", [])
        notes = [b["text"] for b in blocks if b["kind"] == "note"]
        body = "".join(self.block(b) for b in blocks if b["kind"] != "note")
        tag = f'<div class="tag">{_e(s["tag"])}</div>' if s.get("tag") else ""
        sub = f'<h2>{_e(s["subtitle"])}</h2>' if s.get("subtitle") else ""
        note = f'<div class="note">{"<br>".join(_e(n) for n in notes)}</div>' if notes else ""
        return (f'<section class="slide"><div class="content"><div class="header">{tag}<h1>{_e(s["title"])}</h1>{sub}</div>'
                f'<div class="body">{body}</div></div>{note}</section>')

    def html(self, spec):
        meta = spec.get("meta", {})
        slides = spec["slides"]
        title = " ".join(slides[0].get("title_lines", ["deck"])) if slides else "deck"
        pages = "\n".join(self.slide(s, meta) for s in slides)
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
