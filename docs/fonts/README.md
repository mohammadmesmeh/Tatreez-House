# Web fonts — sources, licenses, and status

This folder documents the fonts used by the Tatreez House theme, keeps the
third-party source files and license texts out of `assets/`, and records what is wired up.

Nothing here is served by the theme. Only the files copied into `assets/` are served, and only
`assets/fonts.css.liquid` declares fonts.

## Directory layout

```
assets/
  nunito-latin.woff2            # served: Nunito latin subset (variable)
  playwrite-nz-basic.woff2      # served: Playwrite NZ Basic (variable)
  fonts.css.liquid              # served: @font-face declarations (Latin + Arabic)
docs/fonts/
  README.md                     # this file
  licenses/
    OFL-Nunito.txt          # SIL Open Font License 1.1
    OFL-PlaywriteNZBasic.txt# SIL Open Font License 1.1
```

## Wired up — Latin

### Nunito
- Family in CSS: `Nunito`
- Axis: variable, `font-weight: 200 1000`, normal style
- Subset served: latin (`unicode-range` U+0000-00FF …)
- File: `assets/nunito-latin.woff2` (39,128 bytes)
- SHA-256: `ba344451eab25b217a165363b1982048a5e5830a0daf36577973955a04cac793`
- Source: Google Fonts CSS2 API, `family=Nunito:wght@200..1000`, `Nunito` v32,
  `https://fonts.gstatic.com/s/nunito/v32/XRXV3I6Li01BKofINeaB.woff2`
- License: SIL Open Font License 1.1. Copyright 2014 The Nunito Project Authors
  (https://github.com/googlefonts/nunito). Text: `licenses/OFL-Nunito.txt`
- Self-hosting permitted: yes (OFL 1.1).

### Playwrite NZ Basic
- Family in CSS: `Playwrite NZ Basic` (this is the official family name; "Playwrite New
  Zealand Basic" is the same font — Google uses the short form `NZ`)
- Axis: variable, `font-weight: 100 400`, normal style
- Subset served: latin (`unicode-range` U+0000-00FF …)
- File: `assets/playwrite-nz-basic.woff2` (37,308 bytes)
- SHA-256: `947c7f80daa998895febff219375966a9d0e6612d800da367da9d8ae9db7f61e`
- Source: Google Fonts CSS2 API, `family=Playwrite+NZ+Basic:wght@100..400`,
  `https://fonts.gstatic.com/s/playwritenzbasic/v1/YcmrsYdNS1SdgmGbGgtRtk4ljD2L-0ttuA.woff2`
- License: SIL Open Font License 1.1. Copyright 2023 The Playwrite Project Authors
  (https://github.com/TypeTogether/Playwrite). Text: `licenses/OFL-PlaywriteNZBasic.txt`
- Self-hosting permitted: yes (OFL 1.1).

## Wired up — Arabic

None yet. The previously used Arabic font was withdrawn on 2026-10-20 (licence forbids web
embedding); see `docs/DECISIONS.md`. The OFL replacement is documented in the next revision.

## How it is wired

- `assets/fonts.css.liquid` declares all `@font-face` rules with `font-display: swap` and
  `unicode-range` scoping. The `.css.liquid` extension is required: Shopify only runs Liquid
  (`asset_url`) inside `.liquid` assets. A plain `.css` asset would output the raw `{{ ... }}`
  and the fonts would silently fail.
- `layout/theme.liquid` links it once, above `{{ content_for_header }}`, as
  `{{ 'fonts.css' | asset_url | stylesheet_tag }}`.
- The font **stacks** are applied through Dawn's own variables in `layout/theme.liquid`
  (`:root`), so every component that already uses them follows:
    (Arabic display headings prefer the serif display face; Latin display prefers Playwrite
  theme-settings font stays as a further fallback, so the theme editor keeps working.
- No colours, spacing, or layout were changed.

## Verification performed
- Real family names and `OS/2` weight classes read from the files with `fontTools` (see above).
  Arabic ranges as listed). Playwrite NZ Basic's `cmap` (486 glyphs) has **no** Arabic glyphs,
  so its Latin range is safe.
- Dev theme (`shopify theme dev`, theme id `142644281431`, `http://127.0.0.1:9292`) loads
  `fonts.css` with **7** `@font-face` rules and no leaked `{{ }}`; all 7 font files return
  `200 font/woff2` at the expected byte sizes. Rendered `--font-body-family` /
  `--font-heading-family` confirmed in the served HTML.
- `shopify theme check`: 156 files, 9 warnings / 8 files — identical to the pre-font baseline
  (all pre-existing stock-Dawn offences; none font-related).
- **Not** visually inspected in a browser: rendering of actual Arabic glyphs has not been seen,
  only that the files load. Confirm visually in the theme preview before relying on it.
- **Update (feature 001, T004)**: `fonts.css.liquid` now declares **12** `@font-face` rules
  as part of the feature's end-to-end check (quickstart Scenarios 3–12); the `theme check`
  regression floor is re-checked in `specs/001-homepage-hero/tasks.md` T016.
