# Tatreez House | دار التطريز

A bilingual (English / Arabic) Shopify Online Store 2.0 theme for a Palestinian tatreez
(embroidery) brand: contemporary clothing, digital embroidery patterns, workshops and community
events, and learning content about motifs and technique.

> **Fictional demo brand.** Tatreez House is a portfolio project, not a real business. Products,
> prices and copy on the development store are demonstration content. No sales figures,
> testimonials or credentials are claimed.

## Tech stack

- Shopify Online Store 2.0, based on **Dawn**
- Liquid, JSON templates, sections and snippets; vanilla CSS and JS (no build step)
- Shopify CLI for local development and theme checks
- Spec Kit (`.specify/`, `specs/`) for planning complex features
- Small Node and Python scripts for checks (`scripts/`)

## Architecture

```
layout/      theme.liquid (sets lang/dir, loads rtl.css for Arabic), password.liquid
sections/    Dawn sections + custom hero.liquid
snippets/    Dawn snippets + theme-fonts.liquid (shared font loading), card-variant-picker.liquid
templates/   JSON templates; index.json places the custom hero
assets/      Dawn CSS/JS + component-hero.css, rtl.css, fonts.css.liquid, self-hosted WOFF2 fonts
locales/     en.default.json, en.default.schema.json, ar.json (full Arabic storefront)
config/      settings_schema.json, settings_data.json (pulled from the theme editor)
docs/        PROJECT_BRIEF.md, DECISIONS.md, fonts/
specs/       per-feature specifications (001-homepage-hero)
scripts/     contrast-check.mjs
```

Conventions:
- Every merchant-facing value is a section or theme setting. Every string is a locale key.
- Colours come from the theme's colour schemes (`rgb(var(--color-foreground))`, …), never hex in custom CSS.
- New CSS uses logical properties (`margin-inline`, `text-align: start`, …). Dawn's own physical
  rules are mirrored for Arabic in one file, `assets/rtl.css`.

## Bilingual and RTL

- `layout/theme.liquid` sets `dir="rtl"` for the Arabic locale and loads `rtl.css` only there.
- `locales/ar.json` translates every storefront key, with all six Arabic plural forms.
- Hero position and alignment settings use `start / center / end`, so they mirror automatically.

## Fonts and licences

All fonts are SIL Open Font License 1.1, self-hosted and scoped with `unicode-range`:

| Role | Family |
|---|---|
| Latin body, UI, headings | Nunito |
| Arabic body, UI | Zain (Arabic subset) |
| Arabic headings | Amiri (Arabic subset) |
| Decorative accent (opt-in `.font-accent`) | Playwrite NZ Basic |

Sources, versions, subsetting commands, hashes and licence texts: [`docs/fonts/README.md`](docs/fonts/README.md).

## Local development

Requires [Shopify CLI](https://shopify.dev/docs/api/shopify-cli) and Node 18+.

```sh
# Serve the theme against the development theme (never the live theme)
shopify theme dev --store <your-store>.myshopify.com --theme <development-theme-id> \
  --theme-editor-sync --reconciliation-strategy keep-local

# Pull settings changed in the theme editor before editing locally
shopify theme pull --theme <development-theme-id> \
  --only config/settings_data.json --only "templates/*.json" --only "sections/*.json"

# Static checks
shopify theme check                 # expect 0 errors
node scripts/contrast-check.mjs     # WCAG contrast of every colour scheme
```

Never run `shopify theme publish` or `theme push --live` against the live theme.

## Roadmap

| Milestone | Scope | Status |
|---|---|---|
| 001 | Custom homepage hero section | Done |
| M0 | Foundation: licensed fonts, colour check, full Arabic locale, hero on homepage, RTL fixes, docs | Done (owner admin actions pending) |
| M1 | Homepage "two paths" (Shop / Learn) and remaining homepage sections | Planned |
| M2 | Garment product template (metafields); digital pattern template | Planned |
| M3 | Pattern library (`motif` metaobjects, filtering) | Planned |
| M4 | Workshops (products as events) and free community circles | Planned |
| M5 | Learn hub, blog and article templates linked to motifs | Planned |
| M6 | Accessibility/performance audit, owner handoff guide, case study | Planned |

Decisions and their reasons: [`docs/DECISIONS.md`](docs/DECISIONS.md). Full brief:
[`docs/PROJECT_BRIEF.md`](docs/PROJECT_BRIEF.md).

## Credits

Built on [Dawn](https://github.com/Shopify/dawn) by Shopify (see the Dawn repository for its licence). Fonts by the Nunito, Zain,
Amiri and Playwrite project authors (SIL OFL 1.1).
