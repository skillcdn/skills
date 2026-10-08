# The driven browser

The route of [ad-library.md](ad-library.md) "Routes" for a browser the agent operates: navigate to a URL, then read the embedded results with a script in the page, else the cards, else the page text or a screenshot. It reaches what the page dump cannot (more results, the ad details, the advertiser's About tab, video frames) and yields the record of [record.md](record.md). The code below ran on the live site on 2026-10-02; the readers hold on to the JSON keys in the page and to the visible English labels, which is why every URL carries `locale=en_US`, and never on a class name, which the site generates. When a label changes, read one card's text and adjust the pattern.

## What a driven browser does on the site

- One navigation to a library page is one page load of the budget. Nothing carries a record from the page to a file except the agent itself: the short lines the embedded-results reader returns are the record of the pool (kept in a file where the agent has file tools), and full records with their media addresses are taken only for the ads that reach the shortlist, with `pick` on a page that still lists them (the advertiser view loaded for the shortlist, or the ad's own `id` page).
- The filter dialog exposes no names or roles to the accessibility tree, and synthetic clicks from script do not open its menus: URL parameters do everything, as [ad-library.md](ad-library.md) "URLs" says.
- Screenshots time out while the browser window is in the background; page text and script keep working.
- The site's header is an element with the role of a dialog that contains `Log in` on every page: it is not a login wall. A dialog closed by script takes about a second and a half to go.
- Reading reach costs no page load; six shortlisted ads' reach has been read from their advertiser views without one. Two screenshots per video read its frames (the frame script is the creative research skill's own).

## The embedded results

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

## Cards on the page

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

## Reach in the EU and the UK

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
