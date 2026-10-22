# Tatreez House design system — "Editorial heritage"

Calm, spacious, warm ivory surfaces and confident type. Tatreez appears as a precise, restrained
graphic language built on a stitch grid, never as decoration for its own sake.

Implemented in **`assets/tatreez-tokens.css`** (loaded after `base.css` on every page), plus the
snippets listed under *Components*. Colour schemes stay the merchant's source of truth; tokens only
add what schemes cannot express (accent, linen surface, spacing, type, shape, motion).

## Principles

1. **One signature: the stitch.** The cross-stitch "x" on an 8 px grid is the only ornament. It
   appears as dividers, eyebrow marks, list bullets and the link underline. Nothing else decorates.
2. **Type does the work.** Fraunces at display sizes carries the brand; everything else stays quiet
   in Nunito.
3. **Structure is information.** Eyebrows only where they carry data (product type, section
   category). No numbering unless the content is a sequence.
4. **Both directions, always.** Logical properties only. Arabic is never tracked or uppercased.
5. **Accessible by default.** AA contrast, visible focus, 44 px targets and reduced motion are part
   of every component, not a later pass.

## Colour

Brand palette (decided 2026-10-20 in M2, see `docs/DECISIONS.md`):

| Token | Name | Hex | Use |
|---|---|---|---|
| `--th-ivory` | Warm Ivory | `#F7F3EB` | Page surface (admin scheme-1 uses `#F7F2E8`) |
| `--th-linen` | Linen | `#F0E8D9` | Alternate surface (admin linen scheme) |
| `--th-linen-deep` | Linen Beige | `#D9C8AD` | Borders, ornaments on ivory |
| `--th-ink` | Tatreez Black | `#292820` | Text (admin uses `#252722`) |
| `--th-green` | Deep Green | `#17352B` | **Primary action** (adopted M2) |
| `--th-red` | Embroidery Red | `#8E3038` | Accent: ornaments, sale, highlights |
| `--th-olive` | Olive Green | `#667052` | Secondary accent (sparingly) |
| `--th-white` | White | `#FFFFFF` | Cards, inputs |

Values are stored once as RGB triplets so they work with Dawn's `rgb(var(--x))` convention.

**Semantic roles** (what components use):

| Role | Token | Resolves to |
|---|---|---|
| surface | `--th-surface` | the section's scheme background |
| surface-alt | `--th-surface-alt` | linen, with the woven texture class `.th-linen` |
| ink | `--th-ink-role` | scheme foreground |
| muted ink | `--th-ink-muted` | scheme foreground at 75% (Dawn body text; ≥ 5.5:1 on every scheme) |
| accent | `--th-accent` | embroidery red |
| primary action | `--th-action` | scheme button colour (deep green in all light schemes) |
| border | `--th-border` | linen beige |

Contrast for every scheme and for the accent tokens is checked by
`node scripts/contrast-check.mjs`.

## Typography

| Role | Stack | Notes |
|---|---|---|
| Headings, display | `'Fraunces', 'Amiri', Georgia, serif` | Fraunces variable `opsz` 9–144 + `wght` 300–700, SOFT 0, WONK 0 |
| Body, UI | `'Nunito', 'Zain', system-ui, 'Segoe UI', Tahoma, sans-serif` | unchanged from M0 |
| Accent script | `.font-accent` (Playwrite NZ Basic) | rare, Latin only |

**Scale**: modular, fluid between 360 and 1440 px with `clamp()`. Ratio 1.15 at 360 px rising to
**1.25** at 1440 px (base 16 px):

| Token | 360 px | 1440 px | Dawn classes mapped |
|---|---|---|---|
| `--th-step-display` | 43 | 76 | `.hxxl` |
| `--th-step-h1` | 37 | 61 | `.hxl` |
| `--th-step-h2` | 32 | 49 | `.h0` |
| `--th-step-h3` | 28 | 39 | `h1`, `.h1` (page and product titles) |
| `--th-step-h4` | 24 | 31 | `h2`, `.h2` (section titles) |
| `--th-step-h5` | 21 | 25 | `h3`, `.h3` |
| `--th-step-h6` | 18 | 20 | `h4`, `.h4` |

Dawn's semantic sizes are smaller than a classic scale, so each Dawn class maps one step down;
`--font-heading-scale` (editor setting) still multiplies everything.

- **Weights**: display 400 (Fraunces' optical sizing does the work), section headings 500,
  card titles 500.
- **Tracking**: −0.02 em for display and h1, −0.01 em for h2/h3, 0 below. Arabic: always 0.
- **Line height**: 1.08 display, 1.15 headings, 1.6 body. Arabic headings keep M0's 1.45–1.55.
- **Eyebrow** (`.th-eyebrow`): 12 px Nunito 700, uppercase, +0.14 em tracking, preceded by the
  stitch "x". Arabic: no uppercase, no tracking, 14 px.
- Measure: running text ≤ 68ch.

## Spacing, layout and shape

- **8 px scale**: `--th-space-1` (8) … `--th-space-14` (112).
- **Section rhythm**: `--th-section-y` = 64 px on mobile → 112 px on desktop (fluid).
- **Content width**: target 1320 px. Driven by the editor setting *Page width* = 1400 (1300 px of content inside Dawn's gutters — the setting moves in 100 px steps, so 1300 is the closest). `--th-content-max` derives from it.
- **Radius**: `--th-radius` = 2 px everywhere (buttons, inputs, chips, cards, badges).
- **Borders**: 1 px linen (`--th-border`).
- **Touch targets**: interactive elements ≥ 44 × 44 px (`--th-target`).

## Tatreez graphic language

All original, drawn on an 8 px stitch grid (one cross-stitch = 2 crossing diagonals in one cell).

| Element | Implementation |
|---|---|
| Stitch divider | `snippets/stitch-divider.liquid`: a band of cross-stitches forming a running chevron, SVG `<pattern>`, `aria-hidden`, colour from a `tone` (accent / ink / action / border) |
| Stitch "x" ornament | `assets/icon-stitch-x.svg`, used by `.th-eyebrow` and `.th-list` bullets |
| Stitched underline | `.th-link`: dashed "running stitch" underline drawn with `background` gradients, shown on hover **and** focus; Dawn's focus outline stays, so focus visibility never depends on it |
| Linen texture | `.th-linen`: two crossing hairline gradients (warp and weft), CSS only, 0 bytes of images |

## Motion

- `--th-duration` 240 ms, `--th-ease` `cubic-bezier(0.2, 0.7, 0.2, 1)` (ease-out).
- Uses: fades/reveals ≤ 300 ms, card image zoom (1.04) and second-image crossfade on hover.
- `@media (prefers-reduced-motion: reduce)`: all transitions and the zoom are switched off.

## Components (M2)

| Component | Files | Notes |
|---|---|---|
| Header, mega menu, drawer | `sections/header.liquid`, `snippets/mega-menu-feature.liquid`, `assets/component-header-tatreez.css` | Featured card from header settings; sticky shrink; drawer groups menus with children first |
| Announcement bar | `sections/announcement-bar.liquid` | Pause/play (WCAG 2.2.2) via Dawn's slideshow-component |
| Product card | `snippets/card-product.liquid`, `card-badges.liquid`, `card-quick-add.liquid`, `card-variant-picker.liquid`, `card-inline-add-form.liquid`, `assets/component-card-tatreez.css`, `assets/card-quick-add.js`, `assets/card-variant-picker.js` | 4:5 media, data badges, quick add via Dawn product-form |
| Option chips | `assets/component-variant-chips.css` | Shared by cards and the product page |
| Collection hero | `sections/collection-hero.liquid`, `assets/section-collection-hero.css` | Split text + image, toolbar styling |
| Hero | `sections/hero.liquid`, `assets/component-hero.css` | Full-bleed or split, eyebrow |
| Path cards | `sections/path-cards.liquid`, `assets/section-path-cards.css` | "Choose your path", one stretched link per card |
| Editorial split | `snippets/editorial-split.liquid`, `sections/brand-story.liquid`, `sections/workshops-teaser.liquid`, `assets/section-editorial-split.css` | Shared markup, per-section translated defaults |
| Learn teaser | `sections/learn-teaser.liquid`, `assets/section-learn-teaser.css` | Hidden in store without articles |
| Footer | `sections/footer.liquid`, `assets/section-footer-tatreez.css`, `assets/footer-accordion.js` | Stitch divider, mobile accordions, demo note |
| Sticky add to cart | `snippets/sticky-atc.liquid`, `assets/sticky-atc.js`, `assets/component-sticky-atc.css` | Mobile only, submits the main form |
| Stitch divider | `snippets/stitch-divider.liquid` | `aria-hidden`, tone: accent / ink / action / border |

## Do / don't

- Do pull colours from the scheme; use `--th-accent` only for ornament, sale and small highlights.
- Do keep one stitch ornament per view region; never stack dividers.
- Don't track or uppercase Arabic, mirror photography, or use the script face for headings.
- Don't add new hex values outside `tatreez-tokens.css`.
