# Decisions log

Short, dated record of project decisions and why they were made. Newest milestone first.

## 2026-10-21 — Milestone M2.1 (wiring and verification), branch `m2-wiring`

| # | Decision | Reason |
|---|---|---|
| 1 | Scroll-reveal content is **visible by default**; the slide-in animation only runs when JS has marked the element (`th-reveal-run`) and `html.js-reveal-ready` is set. | Root cause of the hidden content: Dawn sets `.scroll-trigger` to opacity 0.01 and depends on JS to reveal it; late or failing JS, previews and Lighthouse left content invisible. |
| 2 | Hero slideshow timing is a CSS animation (`animationend` advances the slide; `animation-play-state` pauses it). Header turns transparent only when the slideshow is the first section in `<main>`. | One timer drives autoplay and the progress bar; pause/hover/focus/hidden/offscreen and reduced motion are all CSS states. Other pages keep the solid header. |
| 3 | Hero overlay floor 30% plus a 60% content scrim. | Ivory text needs ≥ 67% ink over a white photo for 4.5:1; floor + scrim give ≥ 72% whatever the merchant sets. |
| 4 | Card actions are always visible: "Add to cart" (one variant), "Choose options" (Dawn's quick-add modal), disabled "Sold out". Variant chips and inline forms removed from cards. | One button, one baseline per row on every grid; variant choice belongs in the modal or product page. |
| 5 | Ratings come only from Shopify's standard `reviews.rating` / `reviews.rating_count` metafields; nothing renders on cards without data, the product page shows "No reviews yet". | Never fake reviews; any reviews app that writes the standard metafields works (Judge.me does). |
| 6 | Compact cards via a container query, limited to phone-width screens (card ≤ 320 px, screen < 750 px). | Narrow desktop/tablet cards (e.g. 3 columns at 768 px) must keep full labels. |
| 7 | Homepage product rows on phones are a CSS scroll-snap list (82% items, ~1.28 cards visible), focusable for arrow keys, no JS. | Swipeable with the next card peeking; native RTL scrolling. |
| 8 | Swatch dots: Shopify swatch data first, then the "Swatch colours" theme setting (brand palette); unmapped colours show a neutral ringed dot; the hidden text names every colour. | Merchant-editable mapping; an unmapped colour is still understandable and announced. |
| 9 | **Minimal footer, no menu columns** (owner decision, 2026-10-21): brand + newsletter, language selector, policy links, copyright, demo-brand note. Replaces M2 #20 (footer accordions removed with `footer-accordion.js`). Payment icons, Follow on Shop and the country selector are off (settings kept). | Calmer footer; policies come from Settings → Policies, so no footer menus are needed. |
| 10 | Blank text settings fall back to translated defaults in the new footer fields and the mega menu card (empty heading → the linked collection's translated title). Extends M2 #16. | `/ar` shows Arabic without hard-coded English setting values. |
| 11 | New development store `tatreez-house.myshopify.com` (the previous store froze with HTTP 402). Theme code has no store-specific values; store data is recreated from `docs/store-setup/`. | Portability; the store can be rebuilt. |
| 12 | Acceptance suites live in `scripts/tests/` and pick products by live availability (SKIP when no product is in the needed state). | Inventory changed during testing (all physical products briefly sold out). |
| 13 | The `[shopify-account] Menu … not found in Storefront API` console message is left as is. | The menu exists for Liquid; the account component's API lookup does not find it and falls back to the same default items. Not fixable in theme code. |

## 2026-10-20 — Milestone M2 (design system and UX), branch `m2-design-system`

| # | Decision | Reason |
|---|---|---|
| 1 | `main` created from `master` and `002-foundation` merged into it (no-ff); M2 branches from `main`. | The brief named `main` as the base branch but it did not exist yet; `master` was the original baseline. |
| 2 | **Fraunces** (SIL OFL) for Latin headings, instanced SOFT 0 / WONK 0, `wght` 300–700 + `opsz` kept (66 KB). Heading stack `'Fraunces', 'Amiri', Georgia, serif`. | Editorial voice the brief asked for; WONK/SOFT off for a calm, upright face; optical sizing pays for itself across 18–76 px. |
| 3 | Preload the heading face too (Nunito + Fraunces; Zain + Amiri for Arabic). | The hero heading is usually the LCP element, and a late heading font showed the fallback serif — the most likely cause of the reported "Times New Roman" headings (see report: preview could not be loaded, failure mode reproduced). |
| 4 | **Deep green `#17352B` adopted as a brand colour** (primary action); brand palette formalised as RGB tokens in `assets/tatreez-tokens.css`, the only file with brand colour values. | The admin already uses it for every primary button; 13.29:1 with white. |
| 5 | Type scale 1.15 at 360 px → 1.25 at 1440 px, fluid with `clamp()`, mapped one step down onto Dawn's classes. | A 1.25 scale at phone width made h1 48 px; Dawn uses `h2` for every section title. |
| 6 | Content width via the editor's Page width setting (1200 → 1400 = 1300 px content), not a CSS override. | The setting moves in 100 px steps; overriding `--page-width` would silently disable the editor control (code review finding). |
| 7 | 2 px radius and wider grid gaps (24/40 px) set through Dawn's theme settings. | Merchant-editable values instead of CSS overrides. |
| 8 | Stitch language: one ornament (cross-stitch "x" on an 8 px grid) used for dividers, eyebrows, bullets and the link underline; nothing else decorates. | "Restrained graphic language, never clutter"; one memorable signature. |
| 9 | Mega menu featured card is set in header settings (image, heading, link, which menu item). Menu structure is **not** hardcoded. | Merchant-editable; nav content belongs in Online Store → Navigation (STOP list in the M2 report). |
| 10 | Announcement pause/play uses Dawn's existing `.slideshow__autoplay` wiring; the button is moved into the flex row. | WCAG 2.2.2 without new JS; Dawn's absolute positioning made it overlap "next" (Lighthouse target-size). |
| 11 | Card data rules are theme settings: uncropped product type (`Digital Pattern`), hidden title suffix (`(PDF)`), "New" tag (`new-collection`). | No store data hardcoded in Liquid. |
| 12 | Sale / Sold out badges use the merchant's badge colour-scheme settings; New / Instant download use tokens. | Respect existing settings; tokens only where no setting exists. |
| 13 | Quick add stays on Dawn's `product-form` + cart drawer; `card-quick-add.js` only listens to `cartUpdate` / `cartError` pubsub to announce states. | No parallel cart logic; one source of truth for add-to-cart behaviour. |
| 14 | Unavailable chip values rendered disabled at 75% ink with strike-through and a dashed border. | Dawn's 60% is ~4:1 (fails AA text); state not carried by colour alone. |
| 15 | Path cards: one link per card (the heading, stretched); the CTA is a visual label. Card-level focus ring only where `:has()` is supported. | Avoid a giant link plus duplicate buttons; never lose focus visibility in older browsers. |
| 16 | Section copy defaults live in storefront locales (EN + AR); blank settings fall back to them. Merchant text is never passed through `| t`. | Arabic storefront shows Arabic without admin translation; `text | default: key | t` rendered "Translation missing" for merchant text (found on the featured collection button). |
| 17 | Brand story and workshops teaser are two thin sections over one `editorial-split` snippet. | Each needs its own translated defaults; markup is shared. |
| 18 | Learn teaser renders nothing in the store when the blog has no articles; a hint shows only in the editor. | Spec; avoids an empty section. |
| 19 | No homepage newsletter section. | The footer already has one, and Liquid cannot detect whether customer email signup is enabled. |
| 20 | Footer accordions via a tiny `footer-accordion` element; lists stay open without JS and always on desktop. | Progressive enhancement; no layout dependency on JS. |
| 21 | Mobile sticky add to cart submits the main product form (`form` attribute) and reserves `scroll-padding-block-end`. | Reuses Dawn's product-form; WCAG 2.4.11 focus not obscured. |
| 22 | RTL sliders: `.slider` tracks forced LTR with RTL content inside each slide. | Dawn's slider JS assumes LTR `scrollLeft`; the announcement bar showed half-scrolled slides in RTL. CSS-only, verified. |
| 23 | Before/after screenshots committed as JPEG (quality ~68–72). | Portfolio evidence with a small repository footprint. |

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
