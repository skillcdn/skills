# Collectors

Working code for the two machine routes of [ad-library.md](ad-library.md), as run on 2026-10-02. Port it to whatever the agent has; the logic matters, not the language. Both return the same record per result, so the rest of the skill does not care which route produced it.

## The record

One record per creative group, read from the group's first ad.

| Record field | JSON in the page | On the card (English) | Notes |
|---|---|---|---|
| `id` | `ad_archive_id` | `Library ID: …` | The key for links. |
| `group` | `collation_id` | | The creative group. The same group shows under another member's ID in another view or under a date bound: remove duplicates by `group`, not by `id`. |
| `started`, `days` | `start_date` (Unix seconds) | `Started running on …` | The first day of delivery, and the days run as of today. |
| `active` | `is_active` | `Active`, `Inactive` | |
| `uses` | `collation_count` | `N ads use this creative and text` | The size of the creative group. Absent means one. Under a date bound it counts only the copies that had started by then. |
| `format`, `versions` | `snapshot.display_format`, the length of `snapshot.cards` | `This ad has multiple versions` | `VIDEO`, `IMAGE`, `CAROUSEL`, `DCO` (several versions), `DPA` (a product catalog). Others turn up (`MULTI_IMAGES`, `PAGE_LIKE`): read an unknown value as its name suggests. |
| `title`, `body`, `cta`, `landing` | `snapshot.title`, `.body.text`, `.cta_text`, `.link_url` | The headline, the text, the button, the link | For `DCO`, `DPA` and `CAROUSEL` the top-level text is a template such as `{{product.name}}`. The real copy, links and media are in `snapshot.cards[]`, and the record takes the first card's. |
| `video`, `video_hd`, `poster`, `image` | `snapshot.videos[0].video_sd_url`, `.video_hd_url`, `.video_preview_image_url`, `snapshot.images[0].resized_image_url` | The player, the image | Signed addresses that expire within days: read media in the same run and cite the Library ID. The small video is enough for an overview; words on screen need the large one. |
| `page`, `page_id`, `partner` | `page_name`, `page_id`, `snapshot.branded_content.page_name` | The advertiser, or `A with B` | The Page that runs the ad. A partnership ad names both. |
| `platforms` | `publisher_platform` | `Platforms` | |
| `low_impressions` | `impressions_with_index.impressions_text` equal to `<100` | `Low impression count` | |
| `rank` | Position in `edges` | Position on the page | Meaningful only under the sort order the URL asked for. |
| `cards` | `snapshot.cards[]` | The versions, or the slides of a carousel | In the saved record only: each version's title, text, link and media. What differs between them is what the advertiser is testing. |

## Page dump (a shell and a Chromium-family browser)

One headless run prints the page as the browser built it:

```sh
"<browser>" --headless=new --disable-gpu --no-first-run --user-data-dir="<a folder kept for the whole run>" --dump-dom "<url>"
```

- Keep the same `--user-data-dir` for every call. The first load of a new folder only passes the site's browser check and prints nothing or a page without results; the second load, and every load after it, prints the results.
- Never start the browser without `--headless=new` and that folder, not even to ask its version: on Windows the bare command opens a window in the user's own browser session.
- Do not add `--virtual-time-budget`: the results are in the first HTML, and that flag made runs hang at random.
- Give each run a timeout of about a minute and one retry. Quote the URL: it contains `&` and brackets.
- Chrome and Chromium print the page. On Windows, Edge printed nothing in the same test; when the output is empty for every URL, try another browser or the driven-browser route.

`adlib.py` below does this. It builds each address from a short spec, prints one short line per result while the full records go to a file (a page costs about a thousand tokens of context instead of ten thousand), and logs every browser run, so that the page-load budget is counted and not guessed. Save it in the run's `work/` folder and call it with `python` (`python3` on some systems): the output file, the country, then one spec per page.

```sh
python work/adlib.py work/pool.jsonl KR "q=<term>" "q=<term>&media=video" "q=<term>&sort=recent"
python work/adlib.py work/counts.jsonl KR "q=<domain>&exact=1" "q=<domain>&exact=1&before=7d" "q=<domain>&exact=1&before=30d"
```

| Spec key | Meaning |
|---|---|
| `q` | The search text, as typed: the script encodes it. A spec cannot contain `&` inside the text. |
| `exact=1` | The exact phrase; without it, every word in any order. |
| `page` | A Page ID, in place of `q`: the advertiser view. |
| `media` | `video`, `image`, `meme`, `image_and_meme`; all media without it. |
| `sort=recent` | Most recent first; impressions order without it. |
| `before`, `after` | The date bounds `start_date[max]` and `start_date[min]`: a date, or `30d` for thirty days ago. |
| `status` | `inactive` or `all`; active without it. |
| `id` | A Library ID alone: that one ad. |

A full address is accepted in place of a spec. The script needs only the standard library. `CHROME` sets the browser's path when it is not found. The browser profile and `loads.log` are created next to the output file; `ADLIB_PROFILE` moves the profile. The log has one line per browser run, the first check and the retries included: that is the count the budget is held against. Delete the profile folder when the run ends, and only the one this run made.

```python
import datetime, json, os, re, shutil, subprocess, sys, time
from urllib.parse import urlencode, urlparse

CANDIDATES = [os.environ.get("CHROME"), "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium"]
BASE = "https://www.facebook.com/ads/library/?"
PROFILE = LOADS = None  # set from the output file's folder


def browser():
    for c in CANDIDATES:
        path = c and (c if os.path.isfile(c) else shutil.which(c))
        if path:
            return path
    sys.exit("no Chromium-family browser found: set CHROME to its path, or use the driven-browser route")


def address(country, spec):
    """'q=dog treats&sort=recent&before=30d' becomes an Ad Library address; a full address passes through."""
    if spec.startswith("http"):
        return spec
    p = dict(part.split("=", 1) for part in spec.split("&") if "=" in part)
    day = lambda v: (datetime.date.today() - datetime.timedelta(days=int(v[:-1]))).isoformat() if v.endswith("d") else v
    if "id" in p:
        return BASE + urlencode({"id": p["id"], "locale": "en_US"})
    u = {"active_status": p.get("status", "active"), "ad_type": "all", "country": country, "media_type": p.get("media", "all")}
    if "page" in p:
        u.update({"search_type": "page", "view_all_page_id": p["page"]})
    else:
        u.update({"search_type": "keyword_exact_phrase" if p.get("exact") else "keyword_unordered", "q": p["q"]})
    if p.get("sort") == "recent":
        u.update({"sort_data[mode]": "relevancy_monthly_grouped", "sort_data[direction]": "desc"})
    if "before" in p:
        u["start_date[max]"] = day(p["before"])
    if "after" in p:
        u["start_date[min]"] = day(p["after"])
    return BASE + urlencode({**u, "locale": "en_US"})


def dump(url):
    cmd = [browser(), "--headless=new", "--disable-gpu", "--no-first-run", "--user-data-dir=" + PROFILE, "--dump-dom", url]
    try:
        html = subprocess.run(cmd, capture_output=True, timeout=60).stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        html = ""
    with open(LOADS, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now().isoformat(timespec='seconds')}\t{len(html)}\t{url}\n")
    return html


def find(node, key):
    if isinstance(node, dict):
        if key in node:
            return node[key]
        node = list(node.values())
    if isinstance(node, list):
        for value in node:
            hit = find(value, key)
            if hit is not None:
                return hit
    return None


def connection(url):
    for _ in range(2):  # the first load of a fresh profile only passes the site's browser check
        for block in re.findall(r'<script type="application/json"[^>]*>(.*?)</script>', dump(url), re.S):
            if "search_results_connection" not in block and "deeplink_ad_archive" not in block:
                continue
            data = json.loads(block)
            one = find(data, "deeplink_ad_archive")  # a page opened by id
            if one:
                return {"count": 1, "edges": [{"node": {"collated_results": [one]}}]}
            conn = find(data, "search_results_connection")
            if conn is not None:
                return conn
        time.sleep(3)
    return None


def record(rank, group, today):
    ad = group[0]
    snap = ad.get("snapshot") or {}
    cards = snap.get("cards") or []
    card = cards[0] if cards else {}
    templated = lambda text: not text or "{{" in text  # catalog and dynamic ads keep their real copy in cards
    title = card.get("title") if templated(snap.get("title")) else snap["title"]
    body = (snap.get("body") or {}).get("text")
    body = card.get("body") if templated(body) else body
    video = (snap.get("videos") or [None])[0] or (card if card.get("video_sd_url") else None)
    image = (snap.get("images") or [None])[0] or (card if card.get("original_image_url") else None)
    started = None
    if ad.get("start_date"):  # midnight Pacific time; shift to mid-day so the date is right in any zone
        started = datetime.datetime.fromtimestamp(ad["start_date"] + 43200, datetime.timezone.utc).date()
    return {
        "rank": rank, "id": ad.get("ad_archive_id"), "group": ad.get("collation_id") or ad.get("ad_archive_id"),
        "page_id": ad.get("page_id"), "page": ad.get("page_name"),
        "partner": (snap.get("branded_content") or {}).get("page_name"),
        "started": started and started.isoformat(), "days": started and (today - started).days,
        "active": ad.get("is_active"), "uses": ad.get("collation_count") or 1, "format": snap.get("display_format"),
        "versions": len(cards) or 1, "platforms": ad.get("publisher_platform"),
        "low_impressions": (ad.get("impressions_with_index") or {}).get("impressions_text") == "<100",
        "cta": snap.get("cta_text") or card.get("cta_text"), "landing": snap.get("link_url") or card.get("link_url"),
        "title": title, "body": (body or "")[:1500],
        "video": video and (video.get("video_sd_url") or video.get("video_hd_url")),
        "video_hd": video and video.get("video_hd_url"),
        "poster": video and video.get("video_preview_image_url"),
        "image": image and (image.get("resized_image_url") or image.get("original_image_url")),
        "cards": [{"title": c.get("title"), "body": (c.get("body") or "")[:300], "landing": c.get("link_url"),
                   "video": c.get("video_sd_url"), "image": c.get("resized_image_url") or c.get("original_image_url")}
                  for c in cards[:10]],
    }


def page(url):
    conn = connection(url)
    if conn is None:
        return {"url": url, "ok": False}
    today = datetime.date.today()
    groups = [edge["node"]["collated_results"] for edge in conn.get("edges", []) if edge["node"].get("collated_results")]
    return {"url": url, "ok": True, "read": today.isoformat(), "count": conn.get("count"),
            "more": bool((conn.get("page_info") or {}).get("has_next_page")),
            "ads": [record(i + 1, g, today) for i, g in enumerate(groups)]}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    out, country, specs = sys.argv[1], sys.argv[2], [s.strip() for s in sys.argv[3:]]
    folder = os.path.dirname(os.path.abspath(out))
    PROFILE = os.environ.get("ADLIB_PROFILE") or os.path.join(folder, "browser-profile")
    LOADS = os.path.join(folder, "loads.log")
    for n, spec in enumerate(specs):
        if n:
            time.sleep(2)  # one page at a time, at a person's pace
        result = {"spec": spec, **page(address(country, spec))}
        with open(out, "a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
        if not result["ok"]:
            print("NOT READ (no result data in the page):", spec)
            continue
        print(f"count={result['count']} more={result['more']} ads={len(result['ads'])} | {spec}")
        for a in result["ads"]:
            text = " ".join((a["title"] or a["body"] or "").split())[:48]
            flag = " low" if a["low_impressions"] else ""
            print(f"{a['rank']:>3} {a['id']} {a['started']} {a['days']}d x{a['uses']} {a['format']}{flag} | {a['page']} | {urlparse(a['landing'] or '').netloc} | {text}")
    with open(LOADS, encoding="utf-8") as f:
        print("page loads so far:", sum(1 for _ in f), "| delete when the run ends:", PROFILE)
```

`NOT READ` twice for the same spec is a stop sign, not a prompt to retry harder: see "Manners and limits" in [ad-library.md](ad-library.md). When only the count is wanted, as in counting by age, it is on the `count=` line. A script of the agent's own that prints ad text must write UTF-8 (`sys.stdout.reconfigure(encoding="utf-8")` in Python), or a Windows console stops it at the first emoji.

## Driven browser: the embedded results

After navigating to a URL, run this in the page with the tool that evaluates script. It returns the count and one short line per result: the rank, the Library ID, the creative group (`g…`), the Page ID (`p…`), the start date, the days run, the uses, the format, then the advertiser, the landing host and the first words. Set `pick` to a few Library IDs to get their full records. The same script reads a page opened by `id`.

```js
(() => {
  const pick = null;  // or ["<Library ID>", ...] to get the full records of those ads
  const find = (o, k) => {
    if (!o || typeof o !== "object") return null;
    if (!Array.isArray(o) && k in o) return o[k];
    for (const v of Object.values(o)) { const hit = find(v, k); if (hit != null) return hit; }
    return null;
  };
  let conn = null;
  for (const s of document.querySelectorAll('script[type="application/json"]')) {
    const t = s.textContent;
    if (!t.includes("search_results_connection") && !t.includes("deeplink_ad_archive")) continue;
    const data = JSON.parse(t), one = find(data, "deeplink_ad_archive");  // a page opened by id
    conn = one ? { count: 1, edges: [{ node: { collated_results: [one] } }] } : find(data, "search_results_connection");
    if (conn) break;
  }
  if (!conn) return { ok: false, text: document.body.innerText.slice(0, 300) };
  const now = new Date(), today = Date.UTC(now.getFullYear(), now.getMonth(), now.getDate());
  const day = (t) => new Date((t + 43200) * 1000).toISOString().slice(0, 10);  // midnight Pacific time, shifted to mid-day
  const templated = (x) => !x || x.includes("{{");
  const host = (u) => { try { return new URL(u).host; } catch { return ""; } };
  const ads = conn.edges.filter((e) => e.node.collated_results?.length).map((e, i) => {
    const a = e.node.collated_results[0], s = a.snapshot || {}, c = (s.cards || [])[0] || {};
    const v = (s.videos || [])[0] || (c.video_sd_url ? c : null);
    const im = (s.images || [])[0] || (c.original_image_url ? c : null);
    const started = a.start_date ? day(a.start_date) : null;
    return {
      rank: i + 1, id: a.ad_archive_id, group: a.collation_id || a.ad_archive_id, page_id: a.page_id, page: a.page_name, partner: s.branded_content?.page_name || null,
      started, days: started ? Math.round((today - Date.parse(started)) / 86400000) : null,
      active: a.is_active, uses: a.collation_count || 1, format: s.display_format, versions: (s.cards || []).length || 1,
      platforms: a.publisher_platform, low_impressions: a.impressions_with_index?.impressions_text === "<100",
      cta: s.cta_text || c.cta_text || null, landing: s.link_url || c.link_url || null,
      title: templated(s.title) ? c.title || null : s.title,
      body: ((templated(s.body?.text) ? c.body : s.body.text) || "").slice(0, 1500),
      video: v ? v.video_sd_url || v.video_hd_url : null, video_hd: v ? v.video_hd_url || null : null, poster: v ? v.video_preview_image_url : null,
      image: im ? im.resized_image_url || im.original_image_url : null,
      cards: (s.cards || []).slice(0, 10).map((x) => ({ title: x.title, body: (x.body || "").slice(0, 300), landing: x.link_url, video: x.video_sd_url, image: x.resized_image_url || x.original_image_url })),
    };
  });
  if (pick) return ads.filter((a) => pick.includes(a.id));
  const line = (a) => `${a.rank} ${a.id} g${a.group} p${a.page_id} ${a.started} ${a.days}d x${a.uses} ${a.format}${a.low_impressions ? " low" : ""} | ${a.page} | ${host(a.landing)} | ${(a.title || a.body || "").replace(/\s+/g, " ").slice(0, 48)}`;
  return { ok: true, count: conn.count, more: !!conn.page_info?.has_next_page, lines: ads.map(line) };
})()
```

On this route nothing carries a record from the page to a file except the agent itself, so the short lines are the record of the pool: keep them (in a file when the agent has file tools) and count one load per navigation. Take full records, with their media addresses, only for the ads that reach the shortlist, with `pick` on a page that still lists them: the advertiser view loaded for the shortlist, or the ad's own `id` page.

## Driven browser: cards on the page

Results that arrived by scrolling are not in the embedded JSON. Read them from the cards; this needs the English labels, so the URL must carry `locale=en_US`.

```js
(() => {
  const ids = [...document.querySelectorAll("span, div")].filter((e) => e.childElementCount === 0 && /^Library ID: \d+$/.test(e.textContent.trim()));
  const seen = new Set(), ads = [];
  for (const leaf of ids) {
    let el = leaf;  // climb until the next ancestor would hold a second ad
    while (el.parentElement && (el.parentElement.innerText.match(/Library ID: \d+/g) || []).length === 1) el = el.parentElement;
    if (seen.has(el)) continue;
    seen.add(el);
    const text = el.innerText, lines = text.split("\n").map((s) => s.trim()).filter((s) => s && s !== "\u200b");
    const at = lines.indexOf("Sponsored"), v = el.querySelector("video");
    const out = [...el.querySelectorAll('a[href*="l.php?u="]')].map((a) => new URL(a.href).searchParams.get("u"));
    ads.push({
      id: (text.match(/Library ID: (\d+)/) || [])[1],
      started: (text.match(/Started running on ([A-Za-z]{3} \d{1,2}, \d{4})/) || [])[1] || null,
      active: lines[0] === "Active",
      uses: Number(((text.match(/([\d,]+) ads use this creative and text/) || [])[1] || "1").replace(/,/g, "")),
      versions_note: text.includes("This ad has multiple versions"),
      low_impressions: text.includes("Low impression count"),
      page: at > 0 ? lines[at - 1] : null,
      body: at >= 0 ? lines.slice(at + 1, at + 4).join(" / ").slice(0, 300) : null,
      cta: lines[lines.length - 1], landing: out[0] || null,
      video: v ? v.currentSrc || v.src : null, poster: v ? v.poster : null, seconds: v ? Math.round(v.duration) : null,
    });
  }
  return { cards: ads.length, more: [...document.querySelectorAll('a[role="button"]')].some((a) => a.innerText.trim() === "See more"), ads };
})()
```

Class names on the site are generated and change; these two readers hold on to the JSON keys and to the visible labels only. When a label changes, read one card's text and adjust the pattern.

## Driven browser: reach in the EU and the UK

Reach belongs to one ad, not to its group, and it sits three clicks deep: the card's `See ad details` (on a grouped card `See summary details`, then `See ad details` of an ad inside the summary), then the collapsed section `Transparency by location`. This script does the clicks on a page that lists the ad, reads `Reach` and the breakdown under it, and closes the dialogs again. It costs no page load.

```js
(async () => {
  const id = "<Library ID>";  // an ad whose card is on this page
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const leaves = (root, test) => [...root.querySelectorAll("*")].filter((e) => e.childElementCount === 0 && test(e.textContent.trim()));
  const press = (el) => (el.closest('[role="button"]') || el).click();
  const dialogs = () => [...document.querySelectorAll('[role="dialog"]')];  // the site's header is one of them, always
  let card = leaves(document, (t) => t === "Library ID: " + id)[0];
  if (!card) return { ok: false, why: "no card with this Library ID on the page" };
  while (card.parentElement && (card.parentElement.innerText.match(/Library ID: \d+/g) || []).length === 1) card = card.parentElement;
  const button = leaves(card, (t) => t === "See ad details" || t === "See summary details")[0];
  if (!button) return { ok: false, why: "no details button on the card" };
  const grouped = button.textContent.trim() === "See summary details";
  press(button); await wait(2500);
  if (grouped) {  // a group opens a summary that lists its ads, each with its own details
    const inner = leaves(dialogs().pop(), (t) => t === "See ad details")[0];
    if (inner) { press(inner); await wait(2500); }
  }
  const section = leaves(dialogs().pop(), (t) => t === "Transparency by location")[0];
  let out = { ok: false, why: "no transparency section: not an ad delivered in the EU or the UK" };
  if (section) {
    press(section); await wait(2000);
    const text = dialogs().pop().innerText, at = text.indexOf("\nReach\n");
    out = { ok: at >= 0, grouped, reach: at < 0 ? null : text.slice(at + 7).split("\n")[0], breakdown: at < 0 ? null : text.slice(at).split("\nReach\n").pop().split("\nAbout the advertiser")[0].trim().split("\n").slice(0, 60).join(" ") };
  }
  for (let i = 0; i < 4 && dialogs().length > 1; i++) { leaves(dialogs().pop(), (t) => t === "Close").forEach(press); await wait(1500); }
  return { ...out, open_dialogs: dialogs().length - 1 };
})()
```

Names of countries and genders inside the details arrive in the browser's own language whatever `locale` says: read that table by position, not by label.

## Notes from real runs

- 2026-10-02, Windows, Chrome: page dumps took 2 to 9 seconds each. With `--virtual-time-budget` three runs in about twenty hung until killed; without it, none in about a hundred.
- 2026-10-02: a fresh profile folder returned nothing, or a page without results, on its first load and the full page on the second. `curl` with a browser's user-agent got HTTP 403 and a script that asks the browser to verify itself; that check is not to be scripted.
- 2026-10-02: the count for one query moved between 1,675 and 1,681 across loads minutes apart.
- 2026-10-02: `media_type=image` returned zero for one keyword in one country and thousands in another; an odd zero is checked once with a neighboring value before it is believed.
- 2026-10-02: a landing domain as the query (`keyword_exact_phrase`, the bare domain without `www.`) returned the ads of every Page linking to that store, nine Pages in one case. A store's path on a marketplace worked the same way as an exact phrase; a product address with a query string did not.
- 2026-10-02: about 150 page loads from one desktop in two hours, a second or two apart, met no login wall and no block. That is an observation, not a limit to aim for.
- 2026-10-02, driven browser: the page's filter dialog exposed no names or roles to the accessibility tree, and synthetic clicks from script did not open its menus; URL parameters did everything. Screenshots timed out while the browser window was in the background; page text and script kept working.
- 2026-10-02, first run by a fresh agent: 24 page loads and 28 minutes for a full creative research with frames for six videos. `chrome.exe --version` on Windows opened the user's browser instead of printing a version. Hook frames 240 pixels wide from the small video could not be read for small print; 480 pixels from the large video could.
- 2026-10-02, second run by a fresh agent: 73 page loads and 25 minutes for a sector sweep with twelve candidates counted. The same creative group came back under different Library IDs in the most-recent and the impressions views, and its `uses` fell from 22 to 19 under a date bound a week back. A hand-built address picked up a carriage return and cost two extra loads, which is why the script builds addresses. A default profile folder shared between two runs would have been deleted by the first to finish, which is why the profile sits next to the output file.
- 2026-10-02, third run by a fresh agent, driven browser only, a German market: 22 page loads; reach read for six of six shortlisted ads without a load, from the advertiser views; two screenshots per video. The site's header is an element with the role of a dialog that contains `Log in` on every page: it is not a login wall. A dialog closed by script takes about a second and a half to go.
