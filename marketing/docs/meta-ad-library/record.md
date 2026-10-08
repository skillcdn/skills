# The record

What every route yields per creative group, read from the group's first ad: the same record whether [the page dump](page-dump.md) or [the driven browser](driven-browser.md) produced it, so that the rest of a skill does not care which. The field names are the skills' own; the JSON keys and the English labels are the site's, as checked on the live site on 2026-10-02.

| Record field | JSON in the page | On the card (English) | Notes |
|---|---|---|---|
| `id` | `ad_archive_id` | `Library ID: …` | The key for links. |
| `group` | `collation_id` | | The creative group. The same group shows under another member's ID in another view or under a date bound: remove duplicates by `group`, not by `id`. |
| `started`, `days` | `start_date` (Unix seconds) | `Started running on …` | The first day of delivery, and the days run as of today. |
| `active` | `is_active` | `Active`, `Inactive` | |
| `uses` | `collation_count` | `N ads use this creative and text` | The size of the creative group. Absent means one. Under a date bound it counts only the copies that had started by then (22 copies today can be 19 a week back). |
| `format`, `versions` | `snapshot.display_format`, the length of `snapshot.cards` | `This ad has multiple versions` | `VIDEO`, `IMAGE`, `CAROUSEL`, `DCO` (several versions), `DPA` (a product catalog). Others turn up (`MULTI_IMAGES`, `PAGE_LIKE`): read an unknown value as its name suggests. |
| `title`, `body`, `cta`, `landing` | `snapshot.title`, `.body.text`, `.cta_text`, `.link_url` | The headline, the text, the button, the link | For `DCO`, `DPA` and `CAROUSEL` the top-level text is a template such as `{{product.name}}`. The real copy, links and media are in `snapshot.cards[]`, and the record takes the first card's. |
| `video`, `video_hd`, `poster`, `image` | `snapshot.videos[0].video_sd_url`, `.video_hd_url`, `.video_preview_image_url`, `snapshot.images[0].resized_image_url` | The player, the image | Signed addresses that expire within days (below). The small video is enough for an overview; words on screen need the large one. |
| `page`, `page_id`, `partner` | `page_name`, `page_id`, `snapshot.branded_content.page_name` | The advertiser, or `A with B` | The Page that runs the ad. A partnership ad names both. |
| `platforms` | `publisher_platform` | `Platforms` | |
| `low_impressions` | `impressions_with_index.impressions_text` equal to `<100` | `Low impression count` | |
| `rank` | Position in `edges` | Position on the page | Meaningful only under the sort order the URL asked for. |
| `cards` | `snapshot.cards[]` | The versions, or the slides of a carousel | In the saved record only: each version's title, text, link and media. What differs between them is what the advertiser is testing. |

## Media addresses

`video`, `video_hd`, `poster` and `image` are signed addresses set when the page loads: the `oe` value in each is a hexadecimal timestamp about four days ahead, and a page opened again by `id` carries addresses signed anew. Until then a plain request from any machine downloads the file, no cookie needed, which is how a sandbox on another network reads a video minutes after the page was read. Read media in the run that collected it, cite the Library ID, and keep no copy of the video.
