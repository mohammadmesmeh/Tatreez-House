# Menus (Content → Menus)

The theme reads these menus **by handle**. The handles must match exactly on any store. This file
records what was **verified** on the previous development store (`s8vaej-jj`, 2026-10-21) by
rendering every `linklists` entry from a temporary snippet, and what to create on the new store.
The full store setup is in [`SETUP.md`](SETUP.md), section 6.

## Verified on the previous store

| Handle | Title | Links (top level) |
|---|---|---|
| `main-menu` | Main menu | 4 |
| `footer-shop` | Footer Shop | 4 |
| `footer-learn` | Footer Learn | 4 |
| `footer-about` | Footer About | 5 |
| `customer-account-main-menu` | Customer account main menu | 2 |
| `footer` | Footer menu (Shopify default, not used by the theme) | 1 |

`main-menu` structure as rendered in the header (verified URLs):

```
Shop                     (top level, with children → mega menu)
├── Clothing             /collections/clothing
├── Accessories          /collections/accessories
├── Home & Textiles      /collections/home-textiles
└── Digital Patterns     /collections/digital-patterns
Learn                    (top level, with children → dropdown)
├── Tatreez 101          /pages/tatreez-101
└── Digital Patterns     /collections/digital-patterns
Workshops                /pages/workshops
About                    /pages/about
```

The footer menus' individual link URLs were not captured (only their handles and link counts).
Shopify also creates child "legacy" linklists for nested menu items (for example
`…-legacy-shop`); the theme does not reference them.

## To create on the new store

Use exactly these handles. The structure below matches the verified one, plus **Journal** under
Learn as planned in `SETUP.md` (the previous store did not have it yet).

**`main-menu`**

```
Shop → Collections › All products
  Clothing → Collections › Clothing
  Accessories → Collections › Accessories
  Home & Textiles → Collections › Home & Textiles
  Digital Patterns → Collections › Digital Patterns
Learn → Pages › Tatreez 101
  Tatreez 101 → Pages › Tatreez 101          (handle tatreez-101)
  Journal → Blogs › Journal                   (handle journal)
  Digital Patterns → Collections › Digital Patterns
Workshops → Pages › Workshops                (handle workshops)
About → Pages › About                        (handle about)
```

The top-level item **Shop** must keep the handle `shop`: the mega menu featured card is attached
to it (header setting "Show in menu item" = `shop`).

Footer menus (`footer-shop`, `footer-learn`, `footer-about`) are **not used**: the footer is minimal
(decision 2026-10-21) and shows the policy links from Settings → Policies instead. Do not create them.

**`customer-account-main-menu`**: created automatically by Shopify; keep it (the theme setting
"Customer account menu" points to it).

## Check after creating them

Render the handles once (for example with `shopify theme dev` and a temporary snippet that loops
`linklists` and prints `handle` and `links.size`), or open the storefront and confirm:
the Shop mega menu (with the featured Clothing card), the Learn dropdown and the mobile drawer groups.

Verified on `tatreez-house` (2026-10-21): `main-menu` exactly as above, including Journal.
