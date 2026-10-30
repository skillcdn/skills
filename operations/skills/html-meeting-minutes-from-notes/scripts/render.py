#!/usr/bin/env python3
"""Renders a minutes file (JSON) to one self-contained HTML page and an A4 PDF.

Usage:  python render.py <minutes.json> [--out <folder>] [--png] [--sheet] [--check-only] [--no-check]
        python render.py --browser-check

- Reads the minutes file (references/minutes-spec.md gives its shape) and, unless `external` is false,
  checks every string against the house style: the usual set when `style` is absent, the usual set plus
  the file's own characters with `style.usual`, else the file's own set alone. A forbidden character or
  a bracketed head stops the render and is reported with the string's path in the file
  ($.sections[2].items[0].body) and the character's name. --check-only runs the check and stops;
  --no-check renders anyway, for a look at a draft; a delivery never uses it.
- Writes <out>/<file>.html, the stylesheet inline, the type Pretendard from its documented stylesheet
  unless `theme` names another font (the system's sans as the fallback), and the logos embedded as data
  URLs (paths relative to the minutes file; a missing file is reported and draws nothing), then prints <out>/<file>.pdf at
  A4 with the page number in the foot, with Playwright from Python and the Chrome or Edge already
  installed (the channel "chrome", then "msedge", then Playwright's own Chromium), and says how many
  pages it has. Without Playwright the PDF is skipped with a message. --out defaults to the folder of
  the minutes file.
- --png saves <out>/<file>-preview.png, a full-page screenshot of the HTML at A4 width, for a look at
  the content; --sheet tiles the PDF's pages into <out>/<file>-pages.png with PyMuPDF, for a look at
  the page breaks, and is skipped with a message when PyMuPDF is not installed.
- --browser-check launches and closes the browser and names the channel that answered: the check a
  run makes before its first message. Exit 0 when a browser launched, 1 otherwise.
Needs Python 3 and nothing else for the check and the HTML; Playwright for the PDF and the preview.
"""
import base64
import html
import json
import mimetypes
import os
import re
import sys

# The usual house style of a document that leaves the organization: middle dots in every form, dashes,
# circled numbers, and a head in brackets. A minutes file declares its own in `style`; this is the default.
USUAL_FORBIDDEN = {
    "·": "middle dot", "•": "bullet", "‧": "hyphenation point", "∙": "bullet operator",
    "ㆍ": "Hangul middle dot", "—": "em dash", "–": "en dash", "―": "horizontal bar",
}
for _i in range(20):
    USUAL_FORBIDDEN[chr(0x2460 + _i)] = "circled number"
SKIP_KEYS = ("file", "lang", "logos", "theme", "style", "external")  # paths, codes and the style itself
# The type: Pretendard, loaded from its documented stylesheet so that the print is the same on any machine with the
# network, with the system's sans that has the script's letters as the fallback; an organization's own font goes in
# theme.font and theme.font_css. The same default as the deck skill's helper.
DEFAULT_THEME = {
    "font": "Pretendard",
    "font_css": "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css",
}
FONT_FALLBACK = "'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Noto Sans CJK KR', sans-serif"
SECTION_TYPES = ("text", "list", "table", "kv")
CHANNELS = ("chrome", "msedge", None)  # the installed browsers first, Playwright's own Chromium last

CSS = """
@page { size: A4; margin: 18mm 16mm 16mm; }
* { box-sizing: border-box; }
body { font-family: @FONT; color: #1b1b1b; margin: 0; font-size: 10.5pt; line-height: 1.55;
       word-break: keep-all; overflow-wrap: break-word; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.top { display: flex; justify-content: space-between; align-items: center;
       border-bottom: 1.2px solid #222; padding-bottom: 3mm; margin-bottom: 5mm; }
.top .logos { display: flex; align-items: center; gap: 4mm; }
.top .logos img { height: 4.5mm; width: auto; display: block; }
.top .logos .sep { width: 0.6px; height: 4.5mm; background: #bbb; }
.top .org { font-size: 9.5pt; color: #555; letter-spacing: 0.5px; }
.top .kind { font-size: 9.5pt; color: #555; }
h1 { font-size: 18pt; margin: 0 0 1.5mm; letter-spacing: -0.2px; color: #111; }
table { width: 100%; border-collapse: collapse; }
table.meta { margin-bottom: 7mm; font-size: 10pt; }
table.meta th { width: 22mm; text-align: left; background: #f2f2f2; color: #333; font-weight: 600;
                padding: 2mm 3mm; border: 0.6px solid #c8c8c8; }
table.meta td { padding: 2mm 3mm; border: 0.6px solid #c8c8c8; }
h2 { font-size: 12pt; color: #111; margin: 6mm 0 2.5mm; padding-bottom: 1mm; border-bottom: 0.6px solid #999;
     page-break-after: avoid; break-after: avoid; }
p { margin: 0 0 2mm; }
ol.items { margin: 0; padding-left: 0; list-style: none; counter-reset: it; }
ol.items > li { position: relative; padding-left: 8mm; margin-bottom: 2.4mm; counter-increment: it;
                page-break-inside: avoid; break-inside: avoid; }
ol.items > li::before { content: counter(it) ")"; position: absolute; left: 1.5mm; top: 0; color: #333; font-weight: 600; }
ol.items .t { font-weight: 600; }
ol.items .b { color: #222; }
table.grid { font-size: 9.8pt; margin-top: 1mm; }
table.grid thead { display: table-header-group; }
table.grid th { background: #f2f2f2; font-weight: 600; text-align: left; padding: 1.8mm 2.5mm; border: 0.6px solid #c8c8c8; }
table.grid td { padding: 1.8mm 2.5mm; border: 0.6px solid #c8c8c8; vertical-align: top; }
table.grid tr { page-break-inside: avoid; break-inside: avoid; }
table.kv th { width: 22mm; text-align: left; background: #f2f2f2; font-weight: 600; padding: 1.8mm 2.5mm; border: 0.6px solid #c8c8c8; }
table.kv td { padding: 1.8mm 2.5mm; border: 0.6px solid #c8c8c8; }
table.kv tr { page-break-inside: avoid; break-inside: avoid; }
.note { font-size: 9pt; color: #555; margin-top: 1.5mm; }
.footer { margin-top: 9mm; padding-top: 2.5mm; border-top: 0.6px solid #999; font-size: 8.8pt; color: #666; }
"""

FOOTER_TEMPLATE = ("<div style='width:100%;text-align:center;font-size:8px;color:#777;font-family:sans-serif'>"
                   "<span class='pageNumber'></span> / <span class='totalPages'></span></div>")


def _e(s):
    """Escapes a string for HTML; a newline in it becomes a line break."""
    return "<br>".join(html.escape(line) for line in str(s).split("\n"))


def _img(path, base_dir):
    """A logo file as a data URL, so that the HTML is one file; nothing for a path that does not exist."""
    if not path:
        return ""
    p = path if os.path.isabs(path) else os.path.join(base_dir, path)
    if not os.path.isfile(p):
        print(f"logo: not found, renders no mark: {path}")
        return ""
    mime = mimetypes.guess_type(p)[0] or "image/png"
    with open(p, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode('ascii')}"


def _walk(value, path="$"):
    """Every string in the file with its path, as $.sections[2].items[0].body."""
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from _walk(v, f"{path}.{k}")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from _walk(v, f"{path}[{i}]")


def validate(spec):
    """What the renderer needs: a title, a header table of pairs, and sections of a known type."""
    problems = []
    if not isinstance(spec.get("title"), str) or not spec["title"].strip():
        problems.append("$.title: a title is required")
    meta = spec.get("meta", [])
    if not isinstance(meta, list) or any(not (isinstance(r, list) and len(r) == 2) for r in meta):
        problems.append("$.meta: a list of [label, value] pairs")
    sections = spec.get("sections")
    if not isinstance(sections, list) or not sections:
        problems.append("$.sections: a list of sections is required")
        return problems
    for i, sec in enumerate(sections):
        at = f"$.sections[{i}]"
        if not isinstance(sec, dict) or not sec.get("heading"):
            problems.append(f"{at}: a section is an object with a heading")
            continue
        t = sec.get("type", "text")
        if t not in SECTION_TYPES:
            problems.append(f"{at}.type: unknown section type {t!r}; one of {', '.join(SECTION_TYPES)}")
        elif t == "text" and not isinstance(sec.get("paragraphs"), list):
            problems.append(f"{at}.paragraphs: a list of strings")
        elif t == "list" and not isinstance(sec.get("items"), list):
            problems.append(f"{at}.items: a list of strings or of objects with title and body")
        elif t == "table" and not (isinstance(sec.get("columns"), list) and isinstance(sec.get("rows"), list)):
            problems.append(f"{at}: a table has columns and rows")
        elif t == "kv" and not isinstance(sec.get("rows"), list):
            problems.append(f"{at}.rows: a list of [label, value] pairs")
    return problems


def resolve_style(spec):
    """The set the check applies: the usual set, the usual set plus the file's own, or the file's own alone."""
    style = spec.get("style")
    if style is None:
        return dict(USUAL_FORBIDDEN), True, "the usual set"
    usual = bool(style.get("usual"))
    forbidden = dict(USUAL_FORBIDDEN) if usual else {}
    own = style.get("forbidden", {})
    if isinstance(own, list):
        own = {ch: ch for ch in own}
    forbidden.update(own)
    no_bracket = bool(style.get("no_bracket_heads", usual))
    return forbidden, no_bracket, ("the usual set and the file's own" if usual else "the file's own set")


def check_style(spec):
    """The house-style check: every string outside the skipped keys, against the resolved set."""
    forbidden, no_bracket, _ = resolve_style(spec)
    problems = []
    for path, s in _walk({k: v for k, v in spec.items() if k not in SKIP_KEYS}):
        found = []
        for ch in s:
            if ch in forbidden and ch not in found:
                found.append(ch)
        if found:
            names = ", ".join(f"{forbidden[ch]} ({ch})" for ch in found)
            problems.append(f"{path}: {names}: {s[:60]}")
        if no_bracket and s.lstrip().startswith("["):
            problems.append(f"{path}: bracketed head: {s[:60]}")
    return problems


def render_section(sec):
    t = sec.get("type", "text")
    out = [f"<h2>{_e(sec['heading'])}</h2>"]
    if t == "text":
        out += [f"<p>{_e(p)}</p>" for p in sec.get("paragraphs", [])]
    elif t == "list":
        out.append('<ol class="items">')
        for item in sec.get("items", []):
            if isinstance(item, str):
                out.append(f"<li><span class='b'>{_e(item)}</span></li>")
            else:
                title = f"<span class='t'>{_e(item['title'])}</span> " if item.get("title") else ""
                body = f"<span class='b'>{_e(item['body'])}</span>" if item.get("body") else ""
                out.append(f"<li>{title}{body}</li>")
        out.append("</ol>")
    elif t == "table":
        widths = sec.get("widths") or []
        out.append('<table class="grid"><thead><tr>')
        for i, col in enumerate(sec["columns"]):
            w = f' style="width:{html.escape(str(widths[i]))}"' if i < len(widths) and widths[i] else ""
            out.append(f"<th{w}>{_e(col)}</th>")
        out.append("</tr></thead><tbody>")
        for row in sec.get("rows", []):
            out.append("<tr>" + "".join(f"<td>{_e(c)}</td>" for c in row) + "</tr>")
        out.append("</tbody></table>")
    elif t == "kv":
        out.append('<table class="kv">')
        for k, v in sec.get("rows", []):
            out.append(f"<tr><th>{_e(k)}</th><td>{_e(v)}</td></tr>")
        out.append("</table>")
    if sec.get("note"):
        out.append(f"<div class='note'>{_e(sec['note'])}</div>")
    return "\n".join(out)


def render_html(spec, base_dir):
    theme = {**DEFAULT_THEME, **(spec.get("theme") or {})}
    font = theme.get("font")
    stack = (f"'{font}', " if font else "") + FONT_FALLBACK
    font_import = f"<style>@import url('{html.escape(theme['font_css'])}');</style>" if theme.get("font_css") else ""
    imgs = []
    for logo in spec.get("logos") or []:
        data = _img(logo.get("src", ""), base_dir)
        if data:
            imgs.append(f"<img src='{data}' alt='{html.escape(logo.get('alt', ''))}'>")
    if imgs:
        left = "<span class='logos'>" + "<span class='sep'></span>".join(imgs) + "</span>"
    else:
        left = f"<span class='org'>{_e(spec.get('org', ''))}</span>"
    parts = [
        f"<!doctype html><html lang='{html.escape(spec.get('lang', 'en'))}'><head><meta charset='utf-8'>",
        f"<title>{html.escape(spec['title'])}</title>{font_import}<style>{CSS.replace('@FONT', stack)}</style></head><body>",
        f"<div class='top'>{left}<span class='kind'>{_e(spec.get('kind', 'Minutes'))}</span></div>",
        f"<h1>{_e(spec['title'])}</h1>",
    ]
    if spec.get("meta"):
        parts.append('<table class="meta">')
        parts += [f"<tr><th>{_e(k)}</th><td>{_e(v)}</td></tr>" for k, v in spec["meta"]]
        parts.append("</table>")
    parts += [render_section(s) for s in spec["sections"]]
    if spec.get("footer"):
        parts.append(f"<div class='footer'>{_e(spec['footer'])}</div>")
    parts.append("</body></html>")
    return "\n".join(parts)


def page_count(pdf_path):
    """The number of pages, read from the PDF's own page objects; 0 when it cannot be read that way."""
    with open(pdf_path, "rb") as f:
        return len(re.findall(rb"/Type\s*/Page\b", f.read()))


def launch(playwright):
    """The first Chromium-family browser that launches, with the name of its channel; the launch is the test."""
    for channel in CHANNELS:
        try:
            browser = playwright.chromium.launch(channel=channel) if channel else playwright.chromium.launch()
            return browser, channel or "chromium"
        except Exception:  # an installed browser that is not there raises here; try the next
            continue
    return None, None


NO_BROWSER = ("no Chromium-family browser could be launched: install Chrome or Edge, "
              "or run `playwright install chromium` on the user's word")


def browser_check():
    """Launches and closes the browser, and names the channel that answered."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("browser check: Playwright is not installed in this Python (pip install playwright)")
        return 1
    with sync_playwright() as p:
        browser, channel = launch(p)
        if browser is None:
            print(f"browser check: {NO_BROWSER}")
            return 1
        version = browser.version
        browser.close()
    print(f"browser check: ok ({channel} {version})")
    return 0


def to_pdf(html_path, pdf_path, png_path=None):
    """Prints the HTML at A4 with page numbers; a full-page preview PNG too when asked. True when printed."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("pdf: skipped (Playwright is not installed: pip install playwright, then run again; "
              "or print the HTML from a browser at A4 with background graphics on)")
        return False
    with sync_playwright() as p:
        browser, _ = launch(p)
        if browser is None:
            print(f"pdf: skipped ({NO_BROWSER})")
            return False
        page = browser.new_page()
        page.goto("file:///" + os.path.abspath(html_path).replace("\\", "/"))
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(300)
        page.pdf(path=pdf_path, format="A4", print_background=True, prefer_css_page_size=True,
                 display_header_footer=True, header_template="<div></div>", footer_template=FOOTER_TEMPLATE,
                 margin={"top": "18mm", "right": "16mm", "bottom": "16mm", "left": "16mm"})
        if png_path:
            page.set_viewport_size({"width": 794, "height": 1123})
            page.screenshot(path=png_path, full_page=True)
            print("png:", png_path)
        browser.close()
    n = page_count(pdf_path)
    print("pdf:", pdf_path, f"({n} pages)" if n else "")
    return True


def contact_sheet(pdf_path, png_path, cols=3, dpi=55):
    """Tiles every page of the PDF into one PNG, cols per row, at a small size, for the page breaks."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("sheet: skipped (PyMuPDF is not installed: pip install pymupdf; or read the PDF page by page)")
        return
    src = fitz.open(pdf_path)
    n = src.page_count
    if not n:
        return
    pw, ph = src[0].rect.width, src[0].rect.height
    gap = 12
    rows = -(-n // cols)
    sheet = fitz.open()
    page = sheet.new_page(width=cols * pw + (cols + 1) * gap, height=rows * ph + (rows + 1) * gap)
    for i in range(n):
        r, c = divmod(i, cols)
        x, y = gap + c * (pw + gap), gap + r * (ph + gap)
        page.show_pdf_page(fitz.Rect(x, y, x + pw, y + ph), src, i)
    page.get_pixmap(dpi=dpi).save(png_path)
    print("sheet:", png_path, f"({n} pages, {cols} per row)")


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")  # a Windows console otherwise stops at the first character it cannot encode
    args, flags, out_dir = [], set(), None
    it = iter(argv[1:])
    for a in it:
        if a == "--out":
            out_dir = next(it, None)
            if out_dir is None:
                print(__doc__)
                return 2
        elif a.startswith("--"):
            flags.add(a)
        else:
            args.append(a)
    if "--browser-check" in flags:
        return browser_check()
    if len(args) != 1:
        print(__doc__)
        return 2
    spec_path = os.path.abspath(args[0])
    base_dir = os.path.dirname(spec_path)
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    problems = validate(spec)
    if problems:
        print("minutes file:")
        for p in problems:
            print("  -", p)
        return 1
    if spec.get("external", True) and "--no-check" not in flags:
        problems = check_style(spec)
        if problems:
            print("house-style check failed:")
            for p in problems:
                print("  -", p)
            return 1
        print(f"house-style check passed ({resolve_style(spec)[2]})")
    elif "--no-check" in flags:
        print("house-style check skipped (--no-check): a draft for a look, not for a delivery")
    if "--check-only" in flags:
        return 0
    out_dir = os.path.normpath(out_dir or base_dir)
    os.makedirs(out_dir, exist_ok=True)
    name = spec.get("file") or os.path.splitext(os.path.basename(spec_path))[0]
    html_path = os.path.join(out_dir, name + ".html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(render_html(spec, base_dir))
    print("html:", html_path, f"({len(spec['sections'])} sections)")
    pdf_path = os.path.join(out_dir, name + ".pdf")
    png_path = os.path.join(out_dir, name + "-preview.png") if "--png" in flags else None
    if to_pdf(html_path, pdf_path, png_path):
        if "--sheet" in flags:
            contact_sheet(pdf_path, os.path.join(out_dir, name + "-pages.png"))
    elif "--sheet" in flags:
        print("sheet: skipped (no PDF to tile)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
