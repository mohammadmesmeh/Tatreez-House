# M2.1 (m2-wiring) — UNTESTED items

Running list of what has and has not run in a browser. Store: `tatreez-house.myshopify.com`
(development store, live since 2026-10-21), tested through `shopify theme dev --store
tatreez-house` with Playwright + Microsoft Edge.

Suites (in the repo):

- `python -X utf8 scripts/tests/hero_slideshow_test.py <base-url> <out-dir>`: **33/33 pass**
  (2026-10-21).
- `python -X utf8 scripts/tests/cards_grids_test.py <base-url> <out-dir>`: **35 pass, 0 fail,
  1 skip** (2026-10-21). It picks products by live availability; a check with no product in the
  needed state reports SKIP.

Offline checks: `shopify theme check` (0 errors) and the Shopify AI Toolkit Liquid validator
(`sh scripts/validate-theme.sh`).

## Verified

| Item | Step | Evidence |
|---|---|---|
| Hero: autoplay + loop (~6 s per slide), progress state, inert slides, live region off/polite, one h2, pause by button / hover / focus, arrow keys, reduced motion, JS disabled, transparent header (top / scrolled / other pages) | 2 | hero suite |
| Hero: content edge = page container edge at 360/390/430/768/1440/1920, LTR and forced RTL | 2 | hero suite |
| Hero visuals without images (deep-green surface, ivory text, progress bars) | 2 | screenshots 390 / 1440 |
| Card action row: one baseline per row and equal card heights with mixed cards at 1440 / 768 / 430 | 3 | cards suite |
| Labels: "Add to cart" (1 variant), "Choose options" (several), disabled "Sold out"; visible without hover; accessible name = label + title; Tab from title reaches the action | 3 | cards suite (7 products were sold out on the store during the run) |
| Add to cart -> cart drawer, no reload, live region "… added to your cart.", focus in drawer, Escape closes | 3 | cards suite |
| No chips / inline forms on cards; no rating markup without review data | 3 | cards suite |
| Mobile columns "auto": 1 column at 360 / 430, 2 at 600, 3 at 768, no horizontal scroll | 4 | cards suite |
| Compact cards only on phone widths (≤ 320 px card, < 750 px screen): short labels, full accessible name; every action shows text (fixed: Sold out was blank in compact cards) | 4 | cards suite |
| Homepage product rows: scroll-snap carousels, 1.28 cards visible at 360 / 390, focusable, arrow keys scroll | 4 | cards suite |
| Quick add in search results, related products and after a Section Rendering API refresh (sort) | 4 | cards suite (single-variant products; see open item 2) |
| Product page: one h1; rating empty state "No reviews yet. Be the first to review." | 4 | cards suite |

## Still untested

| # | Item | Step | Why / how to verify |
|---|---|---|---|
| 1 | "Choose options" -> quick-add modal: focus trap (30 Tabs), Escape, focus return, Add to cart from the modal | 3 | All multi-variant products were sold out during the final run. An earlier run opened the modal for Navy Village Thobe (screenshot: chips, quantity, Add to cart), but the trap/Escape results were not recorded. Re-run the cards suite once a multi-variant product is in stock. |
| 2 | Choose options in search / related / after a filter (Section Rendering re-binding of modal-opener) | 4 | Same reason; the suite exercises it automatically when an in-stock multi-variant product exists. |
| 3 | Real RTL at `/ar` (hero, cards, carousels scroll direction) | 2–4 | `/ar` returns 404: Arabic is not published on the new store yet. RTL was checked with forced `dir="rtl"` only. |
| 4 | Colour dots from the "Swatch colours" setting; "Available in N colours"; "+N" in compact cards | 3 | Dots render as outlines until `card_swatch_colors` is set in Step 5 (value in `docs/store-setup/THEME-WIRING.md`). |
| 5 | Hero with images (overlay floor 30% + scrim), "Logo over hero" setting | 2 | Image settings are left empty for the owner; check after images are set. |
| 6 | Judge.me app block placement (`@app`) and stars with real review data | 4 | After the app is installed and real reviews exist (never fake). |
| 7 | Hero pause on hidden tab / offscreen | 2 | Covered by code (visibilitychange, IntersectionObserver) but not asserted by the suite. |
| 8 | Lighthouse, full keyboard pass, 360–1920 screenshots set in `docs/screenshots/m2/` | 7 | Step 7. |
| 9 | Store name shows "tatreez-house" in the header text logo | 5 | Set the store name to "Tatreez House" in the admin (Settings → General) or set the logo. |
