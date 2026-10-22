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

Performance and best practices above are **not representative**: the dev proxy serves plain http
from 127.0.0.1 with a 1.1–3.2 s server response, cross-origin script errors and 400/502 proxy
responses.

**Live store** (`https://tatreez-house.myshopify.com`, theme "Tatreez House" #189100294237 with the
owner's images, 2026-10-22, Lighthouse 12.8.2, mobile unless noted):

| Page | Perf (run 1 → run 2) | A11y | Best practices | Main-thread work (run 1 → run 2) |
|---|---|---|---|---|
| Home | 59 → 38 | 100 | 75 | 76.2 s → 23.6 s |
| Collection | 56 → 46 | 100 | 75 | 23.2 s → 17.2 s |
| Product | 45 → 38 | 100 | 75 | 21.3 s → 16.0 s |
| Home `/ar` | 35 → 30 | 100 | 75 | 68.7 s → 30.6 s |
| Home, desktop | 70 → 61 | 100 | 74 | — |

Run 1 found the hero progress fill animating `inline-size` (a layout on every frame); run 2 is
after the `transform` fix (`perf(hero)` commit). The fix cut the homepage's style & layout from
22.6 s to 4.8 s and rendering from 17.5 s to 2.5 s. The lower run-2 scores come from a slower
network during that run (server response 220–620 ms vs 220–280 ms; FCP 3–4 s vs 2.3–2.5 s), not
from the change. Remaining issues for M6: total blocking time 1.1–2.3 s on phones (theme JS plus
Shopify's analytics / perf-kit scripts), render-blocking CSS, image delivery; on `/ar` the LCP is
the second hero slide (autoplay shows it at ~6 s on a slow load). Best practices 74–75: Shopify's
`shop.app` third-party cookie, the `shopify-account` menu console message and one platform 400.

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
| 2 | Hero with images (overlay floor + scrim), "Logo over hero" | 2 | The owner set the images on the live theme (2026-10-22); not re-run through the suites with images. Footer logo and mega card image still empty. |
| 3 | Judge.me app block placement and stars with real review data | 4 | After the app is installed and real reviews exist (never fake). |
| 4 | Hero pause on hidden tab / offscreen | 2 | In code (visibilitychange, IntersectionObserver); not asserted by the suite. |
| 5 | Performance tuning (TBT, render-blocking CSS, image delivery) | M6 | Measured on the live store (above); not optimised in M2.1 beyond the hero animation fix. |
| 6 | Store content in Arabic: menu titles, collection titles ("Clothing" in the mega card), product titles, announcement text, "All patterns" label | 5 | Store data / merchant text; translate in Translate & Adapt. Theme strings are translated. |
| 7 | Store name shows "tatreez-house" in the header, footer wordmark and copyright | 5 | Set the store name to "Tatreez House" (Settings → General) or set the logos. |
