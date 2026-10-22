# Theme wiring: settings that reference store data

Every theme setting whose value depends on data that lives in the **store** (menus, pages,
collections, blogs, products, images), so it can be re-checked after the theme is pushed to a
new store. Theme code contains no store-specific values (no shop domain, theme ID or image URL;
checked with `grep` on 2026-10-21). Store data itself is set up with [`SETUP.md`](SETUP.md) and
[`MENUS.md`](MENUS.md).

Status column: **set** = value present in the repo (wired in M2.1 Step 5 on `tatreez-house`,
2026-10-21); **editor** = the owner sets it in the theme editor (images).

> Note: a setting **missing** from a JSON template or section group renders as empty, not as the
> schema default. Every value below must exist explicitly in the file.

## Menus

| File | Setting | Value | Must exist in store | Status |
|---|---|---|---|---|
| `sections/header-group.json` | header › `menu` | `main-menu` | menu `main-menu` | set |
| `sections/header-group.json` | header › `menu_type_desktop` | `dropdown` (compact cards; `mega` brings back the full-width panels and the featured card below) | — | set |
| `sections/header-group.json` | header › `mega_feature_menu_handle` | `shop` (used only with the `mega` menu type) | top-level item **Shop** in `main-menu` | set, unused |
| `sections/header-group.json` | header › `mega_feature_heading` | empty → the linked collection's translated title | — | set |
| `sections/header-group.json` | header › `mega_feature_link` | `shopify://collections/clothing` | collection `clothing` | set |
| `sections/footer-group.json` | footer | no menu blocks (minimal footer: brand, newsletter, language, policies) | — | set |
| `config/settings_data.json` | `customer_account_menu` | `customer-account-main-menu` | menu `customer-account-main-menu` | set |

## Links (pages, collections)

| File | Setting | Value | Must exist in store | Status |
|---|---|---|---|---|
| `sections/header-group.json` | announcement 1 › `link` | `shopify://collections/digital-patterns` | collection `digital-patterns` | set |
| `templates/index.json` | hero slideshow › Welcome › `button_link_1` | `shopify://collections/all` | (always exists) | set |
| `templates/index.json` | hero slideshow › Welcome › `button_link_2` | `shopify://pages/tatreez-101` | page `tatreez-101` | set |
| `templates/index.json` | hero slideshow › Learn › `button_link_1` | `shopify://pages/tatreez-101` | page `tatreez-101` | set |
| `templates/index.json` | hero slideshow › Patterns › `button_link_1` | `shopify://collections/digital-patterns` | collection `digital-patterns` | set |
| `templates/index.json` | path cards › Shop › `link` | `shopify://collections/all` | — | set |
| `templates/index.json` | path cards › Learn › `link` | `shopify://pages/tatreez-101` | page `tatreez-101` | set |
| `templates/index.json` | brand story › `link` (label empty → translated "Read our story") | `shopify://pages/about` | page `about` | set |
| `templates/index.json` | workshops teaser › `link` (label empty → translated "See workshops") | `shopify://pages/workshops` | page `workshops` | set |

## Collections, blog

| File | Setting | Value | Must exist in store | Status |
|---|---|---|---|---|
| `templates/index.json` | featured collection › `collection` | `all` | (always exists) | set |
| `templates/index.json` | digital patterns › `collection` | `digital-patterns` | collection `digital-patterns` (Smart: type = Digital Pattern) | set |
| `templates/index.json` | learn teaser › `blog` | `journal` | blog `journal` with ≥ 1 article (hidden without articles) | set |
| `config/settings_data.json` | `cart_drawer_collection` | empty | — | set |

## Product data the theme reads (theme settings, Cards group)

| Setting | Value | Store data it matches | Status |
|---|---|---|---|
| `card_uncropped_product_type` | `Digital Pattern` (schema default) | product **type** of the 3 patterns | set (default) |
| `card_hidden_title_suffix` | `(PDF)` (schema default) | pattern titles end with " (PDF)" | set (default) |
| `card_new_tag` | `new-collection` (schema default) | tag on new products | set (default) |
| `card_swatch_option_names` | `Color, Colour` (schema default) | option name **Color** in `products.csv` | set (default) |
| `card_swatch_colors` | see below | colour option values in `products.csv` | set |

`card_swatch_colors` value for the demo catalogue (brand palette, one per line). Names are matched
in the storefront language: if the colour option values get Arabic translations, add the Arabic
names too, or link the option values to Shopify colour swatches (locale-independent):

```
Warm Ivory: #F7F3EB
Tatreez Black: #292820
Embroidery Red: #8E3038
Olive Green: #667052
Linen Beige: #D9C8AD
```

Reviews: the theme reads Shopify's standard metafields `reviews.rating` and `reviews.rating_count`
(written by Judge.me). No metafield definitions need to be created by hand.

## Images (owner sets these in the theme editor)

All image settings are intentionally **empty** in the repo; every section has a designed
image-less state. Recommended sizes:

| Section › setting | Recommended |
|---|---|
| Theme settings › Logo | `assets/tatreez-house-logo.png`, transparent PNG/SVG, ~ 400 px wide |
| Header › Logo over hero | `assets/tatreez-house-logo-light.png` (light version for the transparent header) |
| Hero slideshow › each slide › Image | landscape, ≥ 2400 × 1350 px; set the focal point in Files |
| Hero slideshow › each slide › Mobile image (optional) | portrait, ≥ 1100 × 1650 px |
| Choose your path › Shop / Learn › Image | landscape 5:4, ≥ 1400 × 1120 px |
| Brand story › Image | portrait 4:5, ≥ 1200 × 1500 px |
| Workshops teaser › Image | portrait 4:5, ≥ 1200 × 1500 px |
| Header › Mega menu feature › Image (optional) | landscape 4:3, ≥ 720 × 540 px |
| Footer › Footer logo (optional) | light/small logo, transparent PNG/SVG, ~ 480 px wide |
| Collection hero › Image (optional override) | landscape 4:3, ≥ 1600 × 1200 px; otherwise the collection image is used |

## Re-check after pushing to a new store

1. `shopify theme pull --only config/settings_data.json --only "templates/*.json" --only "sections/*.json"`
   and diff: nothing above may have been reset.
2. Open each link in the tables: no 404.
3. Header: Shop and Learn open compact dropdowns; footer: brand + newsletter, language selector, policy links;
   homepage: Journal teaser visible.
