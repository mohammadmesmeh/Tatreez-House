# Store setup: rebuild Tatreez House on a new store

Everything the theme needs from the Shopify admin, in order. Store data (products, pages, menus,
settings) lives in the store, not in the theme, so a new store must be set up again from this
kit.

- **Store:** `tatreez-house.myshopify.com` (development store, Basic plan, created 2026-10-21).
- **Time needed:** about 1 hour, plus product images.

**Files in this folder**

| File | Use |
|---|---|
| `products.csv` | All 10 products (final names, prices, types, SEO) |
| `content/page-*.html` | Page bodies: paste through the editor's `<>` (Show HTML) button |
| `content/article-*.html` | The first Journal article |
| `content/policy-shipping.txt` | Shipping policy text |
| `assets/` | Logos, pattern cover images and pattern PDFs |

---

## 1. Store basics

**Settings → General**
- Store name: `Tatreez House`
- Store currency: **USD**
- Store contact email: a project email, not a personal one

**Brand** (Settings → Brand, or General → Brand assets)

| Field | Value |
|---|---|
| Default logo | `assets/tatreez-house-logo.png` |
| Square logo | `assets/tatreez-house-square.png` |
| Primary colour | `#17352B` |
| Secondary colour | `#8C2633` |
| Slogan | Wear the Story. Keep the Heritage. |
| Short description | Contemporary clothing, home textiles and downloadable patterns inspired by Palestinian tatreez — plus workshops for those who want to learn the stitch. |

## 2. Products

1. **Products → Import:** upload `products.csv`. Expect 10 products and 20 variants.
2. Add 2 images per product, each with alt text. Use the pattern images in `assets/`.
3. For multi-colour products, assign an image to each colour variant.
4. Set a **Category** on each product:

   | Products | Category to search |
   |---|---|
   | Thobes / dress | dress |
   | Bag | handbag |
   | Scarf | scarf |
   | Cushion | cushion cover |
   | Wall art | wall art |
   | Patterns | pattern |

## 3. Collections (Smart, by product type)

**Products → Collections → Create collection**, with Type = **Smart**.

| Title | Condition: Product type is equal to | Description |
|---|---|---|
| Clothing | `Clothing` | Contemporary pieces carrying traditional tatreez motifs, made to be worn every day. |
| Accessories | `Accessories` | Embroidered bags and scarves: small ways to carry the stitch with you. |
| Home & Textiles | `Home & Textiles` | Cushions and wall pieces that bring tatreez into the spaces you live in. |
| Digital Patterns | `Digital Pattern` | Downloadable cross-stitch charts for learners: stitch the motifs yourself, at your own pace. |

Expected counts: Clothing 3 · Accessories 2 · Home & Textiles 2 · Digital Patterns 3.

## 4. Pages

**Online Store → Pages → Add page.** Paste each body through the `<>` button, and set the URL
handle exactly as shown.

| Title | Handle | Body |
|---|---|---|
| Tatreez 101 | `tatreez-101` | `content/page-tatreez-101.html` |
| About | `about` | `content/page-about.html` |
| Workshops | `workshops` | `content/page-workshops.html` |
| Contact | `contact` | Use the contact template, if one isn't created automatically |

## 5. Blog

1. **Content → Blog posts → Manage blogs:** rename `News` to **Journal**, change the handle to
   `journal`, and disable comments.
2. **Add blog post:** "How to Read a Cross-Stitch Chart", with the body from
   `content/article-how-to-read-a-cross-stitch-chart.html`.
   - Excerpt: "Each square is one stitch. Learn to read colours, symbols and the centre marks,
     and any tatreez motif is within reach."
   - Tags: `learn, beginner, charts`
   - Image: `assets/cypress-motif-pattern.png`

## 6. Menus (Content → Menus)

Handles must match exactly.

**`main-menu`**
- Shop → Collections › All products
  - Clothing
  - Accessories
  - Home & Textiles
  - Digital Patterns
- Learn → Pages › Tatreez 101
  - Tatreez 101
  - Journal (Blogs › Journal)
  - Digital Patterns
- Workshops → Pages › Workshops
- About → Pages › About

**`footer-shop`:** Clothing, Accessories, Home & Textiles, Digital Patterns

**`footer-learn`:** Tatreez 101, Journal, Digital Patterns, Workshops

**`footer-about`:** About, Contact, Shipping policy, Refund policy, Privacy policy

**`customer-account-main-menu`:** usually created automatically; leave it.

## 7. Policies (Settings → Policies)

- Refund, Privacy and Terms: **Create from template**.
- Shipping: paste `content/policy-shipping.txt`.

## 8. Markets and shipping

**Markets**
- Palestinian Territories: active, with English and Arabic.
- Add an **International** market: Rest of world, USD, active.

**Settings → Shipping and delivery → General profile**

| Zone | Rate | Price | Condition |
|---|---|---|---|
| Palestine | Standard | $5 | — |
| International | Standard | $15 | order price ≤ $149.99 |
| International | Free international shipping | $0 | order price ≥ $150 |

## 9. Payments

**Settings → Payments:** activate **(for testing) Bogus Gateway**. It is available on
development stores.

Test card numbers:
- `1`: success
- `2`: decline
- `3`: error

## 10. Apps

1. **Shopify Digital Products** (free, by Shopify): attach each PDF from `assets/` to its pattern
   only.
   - `cypress-motif-pattern.pdf`
   - `moon-of-bethlehem-pattern.pdf`
   - `tatreez-starter-pattern-bundle.pdf`
2. **Judge.me** (free plan): no imported or sample reviews.
3. **Translate & Adapt** (free, by Shopify): after step 11.

## 11. Languages

**Settings → Languages:** add **Arabic**, publish it, and enable it in both markets. Then
translate the products, collections, pages and menus in Translate & Adapt.

## 12. Checkout and notifications

- **Settings → Checkout → Customize:** logo, colours and fonts.
- **Settings → Notifications → Customize email templates:** logo, and accent colour `#17352B`.

## 13. Theme

1. In the repo, Claude Code runs `shopify theme push --unpublished --store tatreez-house`, with
   the theme named **"Tatreez House"**.
2. In that theme's editor, set the images: logo, hero slides, path cards, brand story, workshops
   and the mega menu card.
3. Before any later push, always `theme pull` first.

## 14. Test order

1. In the cart: Moon of Bethlehem Thobe + Cypress Motif Pattern.
2. Ship to an international address. Expect free shipping, because the order is over $150.
3. Pay with the Bogus Gateway, card `1`.
4. Check:
   - the download link appears on the order status page
   - the email arrives
   - the pattern is fulfilled and the thobe is unfulfilled
5. Save screenshots to `docs/screenshots/checkout/`.

## 15. Share the preview

The store password is in **Online Store → Preferences**. Share the theme preview link together
with the password.
