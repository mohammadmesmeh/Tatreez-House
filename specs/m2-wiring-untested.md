# M2.1 (m2-wiring) — UNTESTED items

Running list, kept while the development store is unavailable (HTTP 402 since 2026-10-21).
Checks available offline: `shopify theme check` and the Shopify AI Toolkit Liquid validator
(`sh scripts/validate-theme.sh`). Nothing below has run in a browser against a store.

| # | Item | Step | How to verify when a store exists |
|---|---|---|---|
| 1 | Hero slideshow: autoplay, loop, progress, pause (button/hover/focus/hidden tab/offscreen), arrow keys, inert slides, live region, reduced motion, JS disabled, header transparency, alignment 360–1920 px LTR + `/ar` | 2 | `python -X utf8 scripts/tests/hero_slideshow_test.py <base-url> <out-dir>` (34 checks) |
| 2 | Hero slideshow visuals without images (deep-green surface + stitch texture) and with images (overlay floor 30% + scrim) | 2 | Screenshots at 360/390/430/768/1440/1920, EN + `/ar` |
| 3 | "Logo over hero" setting and the ivory logo fallback | 2 | Set/unset the setting; check the transparent header |
