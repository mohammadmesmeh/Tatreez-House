# Decisions log

Short, dated record of project decisions and why they were made. Newest milestone first.

## 2026-10-20 — Milestone M0 (foundation), branch `002-foundation`

| # | Decision | Reason |
|---|---|---|
| 1 | Withdraw the Thmanyah Arabic fonts (Thmanyah Sans, Thmanyah Serif Display): WOFF2 copies deleted, `@font-face` rules and stack references removed, source archive moved **out of the repository** (to `C:\Tatreez House-private-fonts\`, not deleted). | Its licence forbids web embedding and hosting the files for download, so it cannot be served from Shopify's CDN or kept in a public repo. The files were never committed (`git log --all -- "*thmanyah*"` is empty), so no history rewrite is needed. |
| 2 | Arabic body/UI = **Zain** 400/700; Arabic headings = **Amiri** 400/700; both from google/fonts, subset to Arabic, `unicode-range`-scoped. No Zain 300. | SIL OFL 1.1 permits self-hosting. Zain is a clean, modern sans that pairs with Nunito; Amiri is a classical Naskh that gives headings a heritage voice. No style uses a weight below 400. |
| 3 | **Nunito** for Latin body, UI *and* headings (700). **Playwrite NZ Basic** moves out of the heading stack into an opt-in `.font-accent` class. | A handwriting script as the default heading face hurts readability and accessibility. |
| 4 | One shared `snippets/theme-fonts.liquid` (preload, `fonts.css`, `--font-*` variables) rendered by the theme layout, the password layout and the gift card template. | Removes three copies of font logic; one place to change fonts. |
| 5 | Stop outputting the font pickers' `font_face`, preload and `fonts.shopifycdn.com` preconnect. Keep the `type_header_font` / `type_body_font` settings (IDs preserved) with an `info` note. | Assistant was declared and preloaded but never used. Keeping the settings avoids breaking saved editor data. |
| 6 | Arabic text gets `letter-spacing: 0`; Arabic headings get `line-height: 1.55` (1.45 for `h0`/`hxl`/`hxxl`). | Tracking breaks cursive joins; Amiri's tall metrics (1.758 em) made stacked marks collide at Dawn's ~1.3. Checked visually h0–h5. |
| 7 | Keep the admin colour schemes exactly as configured, including off-palette values (`#17352B`, `#F7F2E8`, `#252722`, `#8C2633`, `#F0E8D9`); report them instead. | The admin is the source of truth for settings; every pair passes WCAG AA (`scripts/contrast-check.mjs`), so there is no accessibility reason to override. |
| 8 | Hero colours come only from the colour scheme; the image overlay uses the scheme background instead of black. | No hex values in custom CSS; text and overlay always come from the same scheme, so contrast holds for any scheme the merchant picks. |
| 9 | Ship only `en.default.json`, `en.default.schema.json` and `ar.json`; delete 49 other locale files and `ar.schema.json`; re-enable `MatchingTranslations` (removing `.theme-check.yml`). | The store supports English and Arabic only. The merchant edits in English, so Arabic schema strings add upkeep without value. |
| 10 | Remove the 49 hero editor-label keys from the **storefront** locale; keep only the two copy defaults the section renders with `| t`. | Editor labels belong in the schema locale. This keeps `ar.json` identical in shape to `en.default.json` with no dead keys. |
| 11 | Full Modern Standard Arabic translation of `ar.json`, with all six Arabic plural forms; slider labels say "previous/next", not "left/right". | Required for a real bilingual store; "left/right" is wrong in RTL. |
| 12 | Hero alignment/position values renamed `left/right` → `start/end` (`top-left` → `top-start` …). | Values now describe reading direction and mirror in RTL. The placed hero uses `middle-center`/`center`, so no template migration was needed. |
| 13 | Hero heading/text in `templates/index.json` set to `""`. | The admin values equalled the English defaults; blank values let the locale defaults render, so Arabic shows the Arabic headline. CTA labels stay as set in the admin. |
| 14 | Featured collection moved to the custom linen scheme. | Separates it from the dark hero as its own band; contrast passes AA. |
| 15 | `assets/rtl.css`, loaded only when the locale direction is RTL, holds every Dawn RTL override; card alignment settings emit `start/end` from `theme.liquid`. | One place for direction fixes, zero cost for English visitors; logical values work in both directions. |
| 16 | No JS changes to Dawn's slider for RTL in M0. | No slider renders on the store yet (no products), so a JS change could not be verified. Re-test in M2 once products exist. |
| 17 | Constitution 2.0.0: plan → implement → verify loop per milestone; full spec-kit only for the pattern library and events; scoped commits allowed on feature branches. | Per-phase approval gates slowed small changes; the safety and honesty rules are unchanged. |
| 18 | Hero image always renders `alt` (falls back to `""`); hero CTA focus ring uses the scheme foreground. | Accessibility defects found in the M0 keyboard/DOM pass. |
