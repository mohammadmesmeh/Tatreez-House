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
  thmanyah-sans-light.woff2     # served: Thmanyah Sans 300
  thmanyah-sans-regular.woff2   # served: Thmanyah Sans 400
  thmanyah-sans-medium.woff2    # served: Thmanyah Sans 500
  thmanyah-sans-bold.woff2      # served: Thmanyah Sans 700
  thmanyah-sans-black.woff2     # served: Thmanyah Sans 900
  thmanyah-serif-display-light.woff2     # served: Thmanyah Serif Display 300
  thmanyah-serif-display-regular.woff2   # served: Thmanyah Serif Display 400
  thmanyah-serif-display-medium.woff2    # served: Thmanyah Serif Display 500
  thmanyah-serif-display-bold.woff2      # served: Thmanyah Serif Display 700
  thmanyah-serif-display-black.woff2     # served: Thmanyah Serif Display 900
  fonts.css.liquid              # served: @font-face declarations (Latin + Arabic)
docs/fonts/
  README.md                     # this file
  licenses/
    OFL-Nunito.txt          # SIL Open Font License 1.1
    OFL-PlaywriteNZBasic.txt# SIL Open Font License 1.1
  Thmanyah-Font-Family/     # Arabic font source archive (originals; keep as-is)
    LICENSE.pdf
    ترخيص خط ثمانية.pdf          # Arabic text of the same license
    دليل جماليات خط ثمانية.pdf   # typeface aesthetics / specimen guide
    thmanyah typeface/      # 3 families x 5 weights x (otf + woff2)
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

### Thmanyah Sans
- Family **in CSS**: `Thmanyah Sans`
- Family name **inside the files**: typographic family `thmanyah sans` (the "Regular" and
  "Bold" files carry the plain family `thmanyah sans`; the other weights carry descriptive
  families such as `thmanyah sans Light` / `thmanyah sans Black`, i.e. the naming in the
  archive is inconsistent). The CSS name is ours, so the internal names do not matter.
- Weights: **static** (no `fvar`), `OS/2.usWeightClass` →
  Light `300`, Regular `400`, Medium `500`, Bold `700`, Black `900`.
- Subset served: arabic, scoped with
  `unicode-range: U+0600-06FF, U+0750-077F, U+08A0-08FF, U+FB50-FDFF, U+FE70-FEFF`
  (covers the Arabic block, Arabic Supplement, Arabic Extended-A, and the Arabic Presentation
  Forms the files actually contain). Latin glyphs in the files are intentionally **not**
  served — Latin routes to Nunito / Playwrite NZ Basic.
- Files (copied flat into `assets/`, clear names):
  | CSS weight | file | bytes |
  |---|---|---|
  | 300 | `thmanyah-sans-light.woff2` | 72,380 |
  | 400 | `thmanyah-sans-regular.woff2` | 77,776 |
  | 500 | `thmanyah-sans-medium.woff2` | 79,064 |
  | 700 | `thmanyah-sans-bold.woff2` | 79,160 |
  | 900 | `thmanyah-sans-black.woff2` | 77,112 |
- Source (originals, untouched):
  `docs/fonts/Thmanyah-Font-Family/thmanyah typeface/thmanyahsans/woff2/`.
  The `thmanyahseriftext` family is **not** wired up.
- License: © 2026 thmanyah Publishing and Distribution (https://thmanyah.com/,
  ask@thmanyah.com), reserved font name "thmanyah". `LICENSE.pdf` SHA-256
  `07bbb2321bd2b944333c25f4d55140ca22625666132394d7399a365bd8b79a10`. The Arabic text
  (`ترخيص خط ثمانية.pdf`) prevails over translations.

> ⚠️ **License caveat on record.** The Thmanyah license permits commercial use in
> websites/branding/logos and embedding "as part of a compiled, packaged, or obfuscated
> product", but prohibits hosting the Font Software for download and making it available for
> independent reuse "including through web embedding". Serving these WOFF2 from the theme's
> public `assets/` (Shopify CDN) therefore sits against that restriction. This was applied at
> the project owner's explicit instruction for a **development-theme-only** test; obtain written
> permission / an appropriate license before publishing.

### Thmanyah Serif Display
- Family **in CSS**: `Thmanyah Serif Display` (serves as the Arabic **display/heading** face;
  declared decision — spec clarification, 2026-10-17).
- Weights: **static** (not variable), `OS/2.usWeightClass` →
  Light `300`, Regular `400`, Medium `500`, Bold `700`, Black `900`; verified with `fontTools`
  (family `thmanyah serif display`, 416 glyphs, Arabic present).
- Subset served: same Arabic `unicode-range` as Thmanyah Sans
  (`U+0600-06FF, U+0750-077F, U+08A0-08FF, U+FB50-FDFF, U+FE70-FEFF`); Latin glyphs in the
  files are intentionally not served — Latin display routes to Playwrite NZ Basic.
- Files (copied flat into `assets/`, clear names):
  | CSS weight | file | bytes | SHA-256 (prefix) |
  |---|---|---|---|
  | 300 | `thmanyah-serif-display-light.woff2` | 75,732 | `3DB143F2…886A` |
  | 400 | `thmanyah-serif-display-regular.woff2` | 81,136 | `214A70D9…1CA6` |
  | 500 | `thmanyah-serif-display-medium.woff2` | 82,552 | `E21A2EA5…6259` |
  | 700 | `thmanyah-serif-display-bold.woff2` | 81,988 | `D36DA84E…46CE` |
  | 900 | `thmanyah-serif-display-black.woff2` | 79,212 | `A057BE61…A0B` |
- Source (originals, untouched):
  `docs/fonts/Thmanyah-Font-Family/thmanyah typeface/thmanyahserifdisplay/woff2/`.
- License: same Thmanyah terms as above — the ⚠️ license caveat applies to these files too.

## How it is wired

- `assets/fonts.css.liquid` declares all `@font-face` rules with `font-display: swap` and
  `unicode-range` scoping. The `.css.liquid` extension is required: Shopify only runs Liquid
  (`asset_url`) inside `.liquid` assets. A plain `.css` asset would output the raw `{{ ... }}`
  and the fonts would silently fail.
- `layout/theme.liquid` links it once, above `{{ content_for_header }}`, as
  `{{ 'fonts.css' | asset_url | stylesheet_tag }}`.
- The font **stacks** are applied through Dawn's own variables in `layout/theme.liquid`
  (`:root`), so every component that already uses them follows:
  - `--font-body-family: 'Nunito', 'Thmanyah Sans', <theme body font>, <fallbacks>`
  - `--font-heading-family: 'Playwrite NZ Basic', 'Thmanyah Serif Display', 'Thmanyah Sans', <theme heading font>, <fallbacks>`
    (Arabic display headings prefer the serif display face; Latin display prefers Playwrite
    NZ Basic; Thmanyah Sans remains as the Arabic text fallback.)
  Because Nunito/Playwrite are scoped to Latin and the Thmanyah families to Arabic, Latin text renders
  in Nunito / Playwrite NZ Basic and Arabic text falls through to Thmanyah Serif Display
  (headings) / Thmanyah Sans (body). The merchant's
  theme-settings font stays as a further fallback, so the theme editor keeps working.
- No colours, spacing, or layout were changed.

## Verification performed
- Real family names and `OS/2` weight classes read from the files with `fontTools` (see above).
- `unicode-range` derived from the actual `cmap` of `thmanyahsans-Regular.woff2` (411 glyphs;
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
  (added the five `Thmanyah Serif Display` weights). Browser loading of the new rules is verified
  as part of the feature's end-to-end check (quickstart Scenarios 3–12); the `theme check`
  regression floor is re-checked in `specs/001-homepage-hero/tasks.md` T016.
