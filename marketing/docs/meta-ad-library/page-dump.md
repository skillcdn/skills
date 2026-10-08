# The page dump

The shell route of [ad-library.md](ad-library.md) "Routes": one headless run of a Chromium-family browser per URL prints the page as the browser built it, and the results are JSON inside it. No window opens, and a dump takes two to nine seconds. The code below ran on the live site on 2026-10-02; port it to whatever the agent has, the logic matters and not the language. It yields the record of [record.md](record.md).

## One run per page

```sh
"<browser>" --headless=new --disable-gpu --no-first-run --user-data-dir="<a folder kept for the whole run>" --dump-dom "<url>"
```

- Keep the same `--user-data-dir` for every call: it holds the cookie of the site's browser check.
- The site answers some loads with that check, a fresh profile's first load most often: an empty dump, or a page of about 500 bytes whose script posts to `/__rd_verify…` and reloads. A plain dump leaves before the script finishes, so the check comes back on every load. Give that one load time with `--virtual-time-budget=15000`: the browser finishes the check by itself, the cookie (`rd_challenge`) lands in the profile, and plain loads print results again. The check returns from time to time during a run.
- Never start the browser without `--headless=new` and that folder, not even to ask its version: on Windows the bare command, `--version` included, opens a window in the user's own browser session.
- Do not add `--virtual-time-budget` to every load: the results are in the first HTML, and on ordinary pages that flag made three runs in twenty hang until killed, against none in a hundred without it.
- Give each run a timeout of about a minute. Quote the URL: it contains `&` and brackets.
- Chrome and Chromium print the page. On Windows, Edge printed nothing in the same test; when the output is empty for every URL, the patient load included, try another browser or the driven-browser route.

## The script

`adlib.py` below does this. It builds each address from a short spec, prints one short line per result while the full records go to a file (a page costs about a thousand tokens of context instead of ten thousand), and logs every browser run, so that the page-load budget is counted and not guessed. Save it in the run's `work/` folder and call it with `python` (`python3` on some systems): the output file, the country, then one spec per page.

```sh
python work/adlib.py work/pool.jsonl KR "q=<term>" "q=<term>&media=video" "q=<term>&sort=recent"
python work/adlib.py work/counts.jsonl KR "q=<domain>&exact=1&lines=10" "q=<domain>&exact=1&before=7d&lines=0" "q=<domain>&exact=1&before=30d&lines=0"
python work/adlib.py work/pool.jsonl clean
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
| `id` | A Library ID alone: that one ad, its media addresses signed anew. |
| `lines` | How many results to print for that page; `lines=0` prints the count alone. The file gets every record either way. |

A full address is accepted in place of a spec. The script needs only the standard library and runs from any directory: a restricted shell that refuses a change of directory or a variable inside the command takes the same line with the script and the output file by their full paths. `CHROME` sets the browser's path when it is not found. The output file's folder is made when it is missing. The browser profile and `loads.log` are created next to the output file, so that two runs never share a profile that the first to finish would delete; `ADLIB_PROFILE` moves the profile. On Windows the script reaches its own files past 260 characters of path and, when the profile would not fit next to the output file, keeps it in the system's temporary folder, where `clean` finds it (a profile path of 265 characters made no profile and ran every load to the timeout); what the agent writes with other tools (frames, the report) still needs a run folder short enough for them. The log has one line per browser run, the first check and the retries included: that is the count the budget is held against. When the run ends, `clean` in place of the country removes the profile this run made and nothing else, the browser's read-only files included; it needs no permission to delete files beyond the one to run the script, which is why it exists.

```python
import datetime, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time
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


def dump(url, patient=False):
    cmd = [browser(), "--headless=new", "--disable-gpu", "--no-first-run", "--user-data-dir=" + PROFILE]
    if patient:  # gives the site's browser check time to finish: its page posts, then reloads
        cmd.append("--virtual-time-budget=15000")
    cmd += ["--dump-dom", url]
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
    patient = False
    for _ in range(3):
        html = dump(url, patient)
        for block in re.findall(r'<script type="application/json"[^>]*>(.*?)</script>', html, re.S):
            if "search_results_connection" not in block and "deeplink_ad_archive" not in block:
                continue
            data = json.loads(block)
            one = find(data, "deeplink_ad_archive")  # a page opened by id
            if one:
                return {"count": 1, "edges": [{"node": {"collated_results": [one]}}]}
            conn = find(data, "search_results_connection")
            if conn is not None:
                return conn
        patient = True  # no results: most often the site's browser check, which a plain dump leaves before it finishes
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


def long(path):
    """An absolute path in the form Windows accepts past 260 characters; the plain absolute path elsewhere."""
    path = os.path.abspath(path)
    return os.sep * 2 + "?" + os.sep + path if os.name == "nt" else path


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    out, country, specs = sys.argv[1], sys.argv[2], [s.strip() for s in sys.argv[3:]]
    folder = os.path.dirname(os.path.abspath(out))
    PROFILE = os.environ.get("ADLIB_PROFILE") or os.path.join(folder, "browser-profile")
    if os.name == "nt" and len(PROFILE) > 200:  # the browser cannot make its profile under a path near 260 characters
        PROFILE = os.path.join(tempfile.gettempdir(), "adlib-" + hashlib.sha1(folder.encode()).hexdigest()[:12])
    out, LOADS = long(out), long(os.path.join(folder, "loads.log"))
    os.makedirs(long(folder), exist_ok=True)
    if country == "clean":  # the run is over: remove the browser profile it made
        target = long(PROFILE)
        for root, _, files in os.walk(target):
            for name in files:  # the browser leaves read-only files that Windows will not delete as they are
                os.chmod(os.path.join(root, name), 0o700)
        shutil.rmtree(target, ignore_errors=True)
        print("could not remove all of" if os.path.isdir(PROFILE) else "removed", PROFILE)
        sys.exit()
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
        shown = re.search(r"(?:^|&)lines=(\d+)", spec)  # the file keeps every record; this only shortens what is printed
        for a in result["ads"][:int(shown.group(1)) if shown else None]:
            text = " ".join((a["title"] or a["body"] or "").split())[:48]
            flag = " low" if a["low_impressions"] else ""
            print(f"{a['rank']:>3} {a['id']} {a['started']} {a['days']}d x{a['uses']} {a['format']}{flag} | {a['page']} | {urlparse(a['landing'] or '').netloc} | {text}")
    with open(LOADS, encoding="utf-8") as f:
        print("page loads so far:", sum(1 for _ in f))
```

The script loads a page up to three times, the second and third with time for the check. `NOT READ` after that is a stop sign, not a prompt to retry harder: see "Manners and limits" in [ad-library.md](ad-library.md). When only the count is wanted, as in counting by age, it is on the `count=` line, and `lines=0` in the spec keeps the rest out of the context. Take the script's whole output: a reader that closes the pipe early (`head`, `Select-Object -First`) stops it between pages, and the pages after that are not loaded. A script of the agent's own that prints ad text must write UTF-8 (`sys.stdout.reconfigure(encoding="utf-8")` in Python), or a Windows console stops it at the first emoji.
