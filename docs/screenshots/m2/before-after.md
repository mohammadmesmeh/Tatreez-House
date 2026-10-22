# M2 before / after

Captured with `scripts/capture-screens.py` (headless Microsoft Edge via Playwright, reduced motion
emulated so scroll-reveal does not hide content) against the development theme through
`shopify theme dev`. **Before** = start of M2 (2026-10-20, after M0). **After** = end of M2.
Same store data in both sets.

## Pairs (English, same width)

| Page | Width | Before | After |
|---|---|---|---|
| Home | 390 | [before/home-390.jpg](before/home-390.jpg) | [after/home-390.jpg](after/home-390.jpg) |
| Home | 1440 | [before/home-1440.jpg](before/home-1440.jpg) | [after/home-1440.jpg](after/home-1440.jpg) |
| Collection (Clothing) | 390 | [before/collection-390.jpg](before/collection-390.jpg) | [after/collection-390.jpg](after/collection-390.jpg) |
| Collection (Clothing) | 1440 | [before/collection-1440.jpg](before/collection-1440.jpg) | [after/collection-1440.jpg](after/collection-1440.jpg) |
| Garment product | 390 | [before/product-garment-390.jpg](before/product-garment-390.jpg) | [after/product-garment-390.jpg](after/product-garment-390.jpg) |
| Garment product | 1440 | [before/product-garment-1440.jpg](before/product-garment-1440.jpg) | [after/product-garment-1440.jpg](after/product-garment-1440.jpg) |
| Pattern product | 390 | [before/product-pattern-390.jpg](before/product-pattern-390.jpg) | [after/product-pattern-390.jpg](after/product-pattern-390.jpg) |
| Pattern product | 1440 | [before/product-pattern-1440.jpg](before/product-pattern-1440.jpg) | [after/product-pattern-1440.jpg](after/product-pattern-1440.jpg) |
| Search "tatreez" | 390 | [before/search-390.jpg](before/search-390.jpg) | [after/search-390.jpg](after/search-390.jpg) |
| Search "tatreez" | 1440 | [before/search-1440.jpg](before/search-1440.jpg) | [after/search-1440.jpg](after/search-1440.jpg) |
| Cart drawer | 390 | [before/cart-drawer-390.jpg](before/cart-drawer-390.jpg) (added from the product page) | [after/cart-drawer-390.jpg](after/cart-drawer-390.jpg) (added by card quick add) |
| Cart drawer | 1440 | [before/cart-drawer-1440.jpg](before/cart-drawer-1440.jpg) | [after/cart-drawer-1440.jpg](after/cart-drawer-1440.jpg) |

## What changed, page by page

- **Home**: stock Dawn banner + one product row → split editorial hero with eyebrow, "Choose your
  path" (Shop / Learn), 4:5 product cards with quick add, brand story, digital-patterns strip,
  workshops teaser; rotating announcements with pause.
- **Collection**: plain title + ragged `adapt` images → split collection hero with stitch divider,
  hairline toolbar, 3-column 4:5 grid, product-type eyebrows, data badges, hover/focus quick add.
- **Product**: Fraunces title, 2 px option chips (unavailable values struck through and readable),
  mobile sticky add to cart.
- **Cart drawer**: opened by one-tap quick add from a card (no page reload); RTL close button fixed.
- **Search**: same new cards; 44 px filter and sort controls.

## Also captured (after only)

All pages at **360 / 768 / 1024 / 1440 px**, in English and in forced RTL (`-rtl` suffix), plus
the open mobile menu at 360 and 768 px: see the `after/` folder.
RTL captures force `dir="rtl" lang="ar"` and inject `rtl.css` because the Arabic language is not
published on the store yet; the copy therefore stays English in those images.
