# M2.1 (m2-wiring) — UNTESTED items

Running list, kept while the development store is unavailable (HTTP 402 since 2026-10-21).
Checks available offline: `shopify theme check` and the Shopify AI Toolkit Liquid validator
(`sh scripts/validate-theme.sh`). Nothing below has run in a browser against a store.

| # | Item | Step | How to verify when a store exists |
|---|---|---|---|
| 1 | Hero slideshow: autoplay, loop, progress, pause (button/hover/focus/hidden tab/offscreen), arrow keys, inert slides, live region, reduced motion, JS disabled, header transparency, alignment 360–1920 px LTR + `/ar` | 2 | `python -X utf8 scripts/tests/hero_slideshow_test.py <base-url> <out-dir>` (34 checks) |
| 2 | Hero slideshow visuals without images (deep-green surface + stitch texture) and with images (overlay floor 30% + scrim) | 2 | Screenshots at 360/390/430/768/1440/1920, EN + `/ar` |
| 3 | "Logo over hero" setting and the ivory logo fallback | 2 | Set/unset the setting; check the transparent header |
| 4 | Card action row: one baseline per row with mixed cards (pattern + thobe + bag); equal heights; reserved swatch row | 3 | Screenshot grids at 360/430/768/1440; measure button `top` per row (Playwright) |
| 5 | "Add to cart" (single variant) adds and opens the drawer; live region "added" | 3 | `scratchpad quickadd_test.py` adapted to the new markup |
| 6 | "Choose options" opens Dawn's quick-add modal: image, title, price, chips, Add to cart; focus trapped; Escape closes; focus returns to the button | 3 | Keyboard run in Playwright from every grid in item 8 |
| 7 | Disabled "Sold out" button for unavailable products | 3 | Needs a sold-out product on the new store |
| 8 | Same card + quick add in: homepage featured, digital patterns strip, collection, search, related products, complementary products; buttons bind after Section Rendering API injection (filters, related, search) | 4 | Apply a filter, load a product page, search; click Choose options after each |
| 9 | Colour dots from the "Swatch colours" setting; "Available in N colours" text; "+N" in compact cards | 3 | Set `card_swatch_colors` (THEME-WIRING.md) and inspect bag / scarf / cushion cards |
| 10 | Compact cards (container query ≤ 220 px): no eyebrow, 2-line titles, short labels with full accessible name | 4 | 2-column mobile grid at 480–749 px; check accessible names |
| 11 | Mobile columns "auto": 1 column < 480 px, 2 columns 480–749 px, 3 on tablet | 4 | Collection + search at 360 / 430 / 600 / 768 px |
| 12 | Homepage product rows as scroll-snap carousels (~1.25 cards), focusable list, keyboard scrolling, RTL scroll direction | 4 | `/` and `/ar` at 360 / 390 px |
| 13 | Ratings: stars + value + count with "Rated … out of 5, N reviews"; nothing on cards without data; product page "No reviews yet" | 4 | Without reviews (empty state); with Judge.me test data only if real reviews exist (never fake) |
| 14 | Judge.me app block placement in the product page (`@app`) | 4 | After installing the app on the new store |
| 15 | Quick-add modal restyle (radius, 44 px close button) | 3 | Visual check |
