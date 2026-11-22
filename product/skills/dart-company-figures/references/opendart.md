# OpenDART: the API route

OpenDART (`https://opendart.fss.or.kr`) is DART's own API. It answers with JSON and spares the page reading, for the companies it covers. It needs a key, free on registration at that site, which the user holds. This route was written from the API's public guide pages, read in 2026-11, and no run has called it with a key: where an answer differs from this page, trust the guide ("오픈API 개발가이드" on the site), and tell the user what differed.

## When to take it

Take it when `DART_API_KEY` is set in the environment and the company files a business report. Its financial endpoints hold the statements of business, half-year and quarterly reports from fiscal 2015 on; a company whose only filing is an audit report its auditor filed has no rows there, and is read on the web as [dart-web.md](dart-web.md) says. Never ask for the key in chat: when the variable is absent, the web route is the route.

## The key

Read it from the environment into the request and nowhere else. Do not print a request's address, which carries the key as `crtfc_key`; print the path and the other parameters. A status of `010` or `011` means the key is not registered or not usable: say so and take the web route.

## The calls

Every call is `GET https://opendart.fss.or.kr/api/<name>.json` with `crtfc_key` and the parameters below, and answers `status` with `message`: `000` is success, `013` no data, `020` the day's request limit.

| Call | Parameters | Gives |
|---|---|---|
| `company` | `corp_code` | The overview: `corp_name`, `ceo_nm`, `corp_cls` (`Y` KOSPI, `K` KOSDAQ, `N` KONEX, `E` other), `jurir_no`, `bizr_no`, `adres`, `hm_url`, `est_dt`, `acc_mt`. |
| `list` | `corp_code`, `bgn_de`, `end_de` as `YYYYMMDD`, `pblntf_ty` (`A` periodic, `F` audit, `I` exchange), `last_reprt_at=Y` for the final version only | The filings, each with `rcept_no`, the same number the web viewer takes as `rcpNo`. |
| `fnlttSinglAcnt` | `corp_code`, `bsns_year`, `reprt_code` (`11011` business report, `11012` half-year, `11013` first quarter, `11014` third quarter) | The main accounts, revenue and operating profit among them, each row with `fs_div` (`CFS` consolidated, `OFS` separate), `account_nm`, `thstrm_amount` (this period) and `frmtrm_amount` (the one before), whole amounts in the currency the row names (`currency`). |
| `fnlttSinglAcntAll` | The same, and `fs_div` | Every account of the statements, with `sj_div` (`IS` income statement, `CIS` comprehensive income). |

The corp code is the web route's: `corp "<name>"` of the script needs no key. The guide also offers the whole list of corp codes as one archive (`corpCode.xml`), which is more than one company's lookup needs.

## What it does not replace

The amounts come as the report filed them, so the row's address is still the filing: `https://dart.fss.or.kr/dsaf001/main.do?rcpNo=<rcept_no>`. The auditor's opinion, the notes on related parties and segments, and a parent's table of its subsidiaries are read in the filing's sections on the web, as phases 4 to 6 need them.
