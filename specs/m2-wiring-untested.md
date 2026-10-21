# M2.1 (m2-wiring) — UNTESTED items

What has and has not run in a browser. Store: `tatreez-house.myshopify.com` (development store),
tested through `shopify theme dev --store tatreez-house` (dev theme 189091577949) with Playwright
+ Microsoft Edge, 2026-10-21. Arabic is published, so RTL ran on the real `/ar` locale.

Suites (in the repo, `python -X utf8 scripts/tests/<suite> <base-url> <out-dir>`):

| Suite | Result |
|---|---|
| `hero_slideshow_test.py` | **33/33** (real `/ar`) |
| `cards_grids_test.py` | **40 pass, 0 fail, 1 skip** — the skip is "Sold out", which passed in the previous run while products were sold out |
| `keyboard_test.py` | **12/12** (EN + `/ar`) |
| `wired_screens_test.py` | **50/50** (4 pages × 360–1920 px × EN/AR: no horizontal scroll, correct `dir`, one h1; mega menu card) |

Offline checks: `shopify theme check` (0 errors; 9 warnings, all in untouched Dawn files) and the
Shopify AI Toolkit Liquid validator (`sh scripts/validate-theme.sh`).

Lighthouse 12.8.2 (Edge, through the local dev proxy):

| Page | Perf | A11y | Best practices | SEO |
|---|---|---|---|---|
| Home, mobile | 50 | 100 | 75 | 92 |
| Collection, mobile | 35 | 100 | 57 | 85 |
| Product, mobile | 35 | 100 (96 before the quantity-label fix) | 75 | 100 |
| Home `/ar`, mobile | 42 | 100 (after the "View all" name fix) | 57 | 85 |
| Home, desktop | 87 | 100 | 56 | 92 |

Performance and best practices are **not representative**: the dev proxy serves plain http from
127.0.0.1 with a 1.1–3.2 s server response, cross-origin script errors and 400/502 proxy
responses. Re-measure on the preview of the pushed theme (Step 6).

## Verified

| Item | Step | Evidence |
|---|---|---|
| Hidden content: visible without scroll-reveal JS | 1 | hero suite (JS off), Lighthouse screenshots |
| Hero: autoplay + loop, progress, inert slides, live region, one h2, pause (button / hover / focus), arrow keys, reduced motion, JS off, transparent header only over the hero, content edge = container edge 360–1920 LTR + `/ar` | 2 | hero suite |
| Card actions: one baseline per row, equal heights; Add to cart / Choose options / Sold out; visible without hover; accessible names; Tab order | 3 | cards suite |
| Add to cart -> drawer (no reload, live region, focus, Escape) | 3 | cards suite |
| Choose options -> modal: focus inside, 30 Tabs trapped, Escape + focus return, Add to cart from the modal | 3 | cards suite |
| Swatch dots with the brand colour map, colour names in the hidden text (EN + `/ar`), neutral fallback dot | 3 | `/collections/all` + `/ar`, computed colours |
| Mobile auto columns, compact cards, homepage carousels, quick add in search / related / after a Section Rendering refresh, rating empty states | 4 | cards suite |
| Footer: minimal layout 390 / 1440 EN + `/ar`, language selector (English / العربية) by keyboard, policy links, RTL copyright line | 5 | keyboard suite, screenshots |
| Header: Shop mega menu with the featured Clothing card (EN + `/ar`), homepage links (path cards, brand story, workshops) | 5 | wiring check, keyboard suite |

## Still untested

| # | Item | Step | Why / how to verify |
|---|---|---|---|
| 1 | Newsletter **server** responses (error and success states after a real post) | 5 | Shopify's bot protection holds the customer form submit in a headless browser; a real post would also create a customer. Styles were checked by injecting the exact markup. Verify by hand: submit `a@b` (error, red ring + message) and a real address (success panel). |
| 2 | Hero with images (overlay floor + scrim), "Logo over hero", footer logo, mega card image | 2, 5 | Image settings are left empty for the owner. |
| 3 | Judge.me app block placement and stars with real review data | 4 | After the app is installed and real reviews exist (never fake). |
| 4 | Hero pause on hidden tab / offscreen | 2 | In code (visibilitychange, IntersectionObserver); not asserted by the suite. |
| 5 | Performance on a real preview | 7 | Dev-proxy numbers only (see above). Needs the pushed theme (Step 6) and the store password. |
| 6 | Store content in Arabic: menu titles, collection titles ("Clothing" in the mega card), product titles, announcement text, "All patterns" label | 5 | Store data / merchant text; translate in Translate & Adapt. Theme strings are translated. |
| 7 | Store name shows "tatreez-house" in the header, footer wordmark and copyright | 5 | Set the store name to "Tatreez House" (Settings → General) or set the logos. |
