#!/usr/bin/env node
// Reads DART, the disclosure site of Korea's Financial Supervisory Service, one page per call, at a
// person's pace: a company by name, its overview, its filings in a period, a filing's table of
// contents and one section of it as text. Needs Node.js 22 or newer and nothing else.
//
//   node dart.example.mjs corp "<company name>"
//   node dart.example.mjs info <corp code>
//   node dart.example.mjs search <corp code> <from YYYYMMDD> <to YYYYMMDD> [types]
//   node dart.example.mjs toc <rcpNo> [word,word] [--doc <dcmNo>]
//   node dart.example.mjs sect <rcpNo> <dcmNo> <eleId> <offset> <length> <dtd> [word,word]
//
// types: A001 business report, A002 half-year, A003 quarterly, F001 audit report, F002 consolidated
// audit report, I002 fair disclosure (provisional results). Default: A001,F001,F002.
// A word list keeps only the sections, or the rows of a section, that hold one of the words.
// The routes are the site's own, read from its pages on 2026-11 (references/dart-web.md says how to
// find each again). Every call opens the search page first for a session, then the one route, two
// seconds apart. It writes no file and keeps nothing.

const BASE = "https://dart.fss.or.kr";
const SEARCH_PAGE = "/dsab007/main.do";
const PAUSE_MS = 2000;
const AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36";

let cookie = "";
const pause = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function stop(message) {
  console.error(message);
  process.exit(2);
}

async function open(path, { form, referer = BASE + SEARCH_PAGE } = {}) {
  await pause(PAUSE_MS);
  let res;
  try {
    res = await fetch(BASE + path, {
      method: form ? "POST" : "GET",
      headers: {
        "User-Agent": AGENT,
        Referer: referer,
        ...(cookie ? { Cookie: cookie } : {}),
        ...(form ? { "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest" } : {}),
      },
      body: form ? form.toString() : undefined,
    });
  } catch (e) {
    stop(`NOT READ: ${path} (${e.cause?.code ?? e.message})`);
  }
  for (const c of res.headers.getSetCookie?.() ?? []) {
    const pair = c.split(";")[0];
    const name = pair.split("=")[0];
    cookie = [...cookie.split("; ").filter((p) => p && !p.startsWith(name + "=")), pair].join("; ");
  }
  const text = await res.text();
  if (!res.ok) stop(`NOT READ: ${path} answered ${res.status}. Stop and tell the user; do not retry harder.`);
  return text;
}

const entities = { "&nbsp;": " ", "&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&#10;": "\n", "&#39;": "'" };
const plain = (html) =>
  html
    .replace(/<[^>]+>/g, " ")
    .replace(/&[a-z#0-9]+;/gi, (e) => entities[e] ?? " ")
    .replace(/\s+/g, " ")
    .trim();
const attr = (html, name) => new RegExp(`${name}\\s*=\\s*['"]([^'"]*)['"]`).exec(html)?.[1];

// A section's HTML as lines: a table row becomes one line, its cells joined by tabs.
function sectionText(html) {
  const body = html.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>|<head[\s\S]*?<\/head>/gi, "");
  const lines = [];
  let rest = body;
  for (;;) {
    const at = rest.search(/<tr[\s>]/i);
    const before = at < 0 ? rest : rest.slice(0, at);
    for (const piece of before.split(/<\/p>|<br\s*\/?>|<\/div>|<\/h\d>|<\/table>/i)) {
      const text = plain(piece);
      if (text) lines.push(text);
    }
    if (at < 0) break;
    const close = /<\/tr>/i.exec(rest.slice(at));
    const end = close ? at + close.index : -1;
    const row = rest.slice(at, end < 0 ? undefined : end);
    const cells = [...row.matchAll(/<t[dh][^>]*>([\s\S]*?)<\/t[dh]>/gi)].map((m) => plain(m[1]));
    if (cells.some(Boolean)) lines.push(cells.join("\t"));
    if (end < 0) break;
    rest = rest.slice(end + 5);
  }
  return lines;
}

// A filing may write a title or an account with spaces between its letters ("손 익 계 산 서"): compare without them.
const squeeze = (text) => text.replace(/\s+/g, "");
const holds = (text, words) => words.length === 0 || words.some((w) => squeeze(text).includes(squeeze(w)));
const wordList = (arg) => (arg ? arg.split(",").map((w) => w.trim()).filter(Boolean) : []);

const commands = {
  // The companies a name matches: corp code, name, market, stock code, representative, business registration number, industry.
  async corp([name]) {
    if (!name) stop('usage: corp "<company name>"');
    const html = await open("/corp/searchCorpL.ax", { form: new URLSearchParams({ textCrpNm: name, currentPage: "1", maxResults: "50" }) });
    const rows = [...html.matchAll(/<tr[^>]*>([\s\S]*?)<\/tr>/gi)].map((m) => m[1]).filter((r) => r.includes("hiddenCikCD"));
    if (rows.length === 0) console.log(`no company named like "${name}". Try the legal name, a shorter part of it, or the stock code.`);
    for (const row of rows) {
      const code = /name='hiddenCikCD\d+'\s+value='(\d+)'/.exec(row)?.[1];
      const tip = (attr(row, "title") ?? "").replace(/&nbsp;/g, "").replace(/&#10;/g, "\n");
      const field = (label) => new RegExp(`${label}\\s*:(.*)`).exec(tip)?.[1]?.trim() ?? "";
      const cells = [...row.matchAll(/<td[^>]*>([\s\S]*?)<\/td>/g)].map((m) => plain(m[1]));
      const market = /class="tagCom_[a-z_]+"\s+title="([^"]*)"/.exec(row)?.[1] ?? "not listed";
      console.log([code, field("회사명") || cells[1], market, cells[3] || "-", field("대표자명"), field("사업자번호"), field("업종")].join("\t"));
    }
    console.log(`${rows.length} shown: corp code, name, market, stock code, representative, business registration number, industry`);
  },

  // The overview of one company: what its own filing says of its site, its address, its founding.
  async info([code]) {
    if (!/^\d{8}$/.test(code ?? "")) stop("usage: info <corp code, 8 digits>");
    const html = await open("/dsae001/selectPopup.ax", { form: new URLSearchParams({ selectKey: code }) });
    const rows = [...html.matchAll(/<tr[^>]*>([\s\S]*?)<\/tr>/gi)].map((m) => m[1]);
    for (const row of rows) {
      const head = plain(/<th[^>]*>([\s\S]*?)<\/th>/.exec(row)?.[1] ?? "");
      const value = plain(/<td[^>]*>([\s\S]*?)<\/td>/.exec(row)?.[1] ?? "").replace(/\s*(정보 더보기|rss)\s*/g, " ").trim();
      if (head) console.log(`${head}\t${value}`);
    }
    if (rows.length === 0) console.log(plain(html).slice(0, 600));
  },

  // The filings of one company in a period, newest first: filed day, rcpNo, report, filer, remark.
  async search([code, from, to, types = "A001,F001,F002"]) {
    if (!/^\d{8}$/.test(code ?? "") || !/^\d{8}$/.test(from ?? "") || !/^\d{8}$/.test(to ?? "")) stop("usage: search <corp code> <from YYYYMMDD> <to YYYYMMDD> [types]");
    const form = new URLSearchParams({ currentPage: "1", maxResults: "100", maxLinks: "10", sort: "date", series: "desc", textCrpCik: code, startDate: from, endDate: to, finalReport: "recent" });
    for (const type of wordList(types)) form.append("publicType", type);
    const html = await open("/dsab007/detailSearch.ax", { form });
    const rows = [...html.matchAll(/<tr[^>]*>([\s\S]*?)<\/tr>/gi)].map((m) => m[1]).filter((r) => r.includes("rcpNo="));
    for (const row of rows) {
      const cells = [...row.matchAll(/<td[^>]*>([\s\S]*?)<\/td>/g)].map((m) => m[1]);
      const rcpNo = /rcpNo=(\d+)/.exec(row)?.[1];
      const remark = [...(cells[5] ?? "").matchAll(/title="([^"]*)"/g)].map((m) => m[1]).join("; ");
      console.log([plain(cells[4] ?? ""), rcpNo, plain(cells[2] ?? ""), plain(cells[3] ?? ""), remark || "-"].join("\t"));
    }
    const total = /\[총\s*([\d,]+)건\]/.exec(html)?.[1] ?? String(rows.length);
    console.log(`${rows.length} of ${total} shown: filed, rcpNo, report, filer, remark`);
  },

  // The table of contents of one filing: title, then what `sect` takes (dcmNo eleId offset length dtd).
  async toc(args) {
    const at = args.indexOf("--doc");
    const doc = at < 0 ? "" : args.splice(at, 2)[1];
    const [rcpNo, words] = args;
    if (!/^\d{14}$/.test(rcpNo ?? "") || (at >= 0 && !/^\d+$/.test(doc ?? ""))) stop("usage: toc <rcpNo, 14 digits> [word,word] [--doc <dcmNo of an attached document>]");
    const html = await open(`/dsaf001/main.do?rcpNo=${rcpNo}${doc ? `&dcmNo=${doc}` : ""}`);
    const pick = wordList(words);
    const re = /node\d+\['text'\]\s*=\s*"([^"]*)";[\s\S]*?\['dcmNo'\]\s*=\s*"(\d+)";[\s\S]*?\['eleId'\]\s*=\s*"(\d+)";[\s\S]*?\['offset'\]\s*=\s*"(\d+)";[\s\S]*?\['length'\]\s*=\s*"(\d+)";[\s\S]*?\['dtd'\]\s*=\s*"([^"]*)"/g;
    const nodes = [...html.matchAll(re)].map((m) => m.slice(1));
    for (const [title, ...rest] of nodes) if (holds(title, pick)) console.log(`${title}\t${rest.join(" ")}`);
    console.log(`${nodes.length} sections in the filing: title, then dcmNo eleId offset length dtd`);
    const attached = [...html.matchAll(/<option[^>]*value="rcpNo=(\d+)&(?:amp;)?dcmNo=(\d+)"[^>]*>([^<]*)</g)].map((m) => `${plain(m[3])}\t${m[2]}`);
    if (attached.length) console.log(`attached documents (title, dcmNo; "toc ${rcpNo} --doc <dcmNo>" lists one's sections):\n${[...new Set(attached)].join("\n")}`);
  },

  // One section as text: a table row is one line, cells joined by tabs. The unit line is kept whatever the words.
  async sect([rcpNo, dcmNo, eleId, offset, length, dtd, words]) {
    if (!rcpNo || !dcmNo || !eleId || !offset || !length || !dtd) stop("usage: sect <rcpNo> <dcmNo> <eleId> <offset> <length> <dtd> [word,word]");
    const query = new URLSearchParams({ rcpNo, dcmNo, eleId, offset, length, dtd });
    const html = await open(`/report/viewer.do?${query}`, { referer: `${BASE}/dsaf001/main.do?rcpNo=${rcpNo}` });
    const pick = wordList(words);
    const lines = sectionText(html);
    for (const line of lines) if (holds(line, pick) || /단위\s*[:：]/.test(line) || /^제\s*\d+\s*\(?(당|전)?\)?\s*기/.test(line)) console.log(line);
    console.log(`${lines.length} lines in the section`);
  },
};

const [command, ...args] = process.argv.slice(2);
if (!commands[command]) stop("usage: dart.example.mjs corp|info|search|toc|sect ...  (the head of this file says what each takes)");
await open(SEARCH_PAGE, { referer: BASE + "/" });
await commands[command](args);
