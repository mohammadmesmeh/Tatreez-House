# Web fonts — sources, licences and status

Every font served by the Tatreez House theme is licensed under the **SIL Open Font License 1.1**
and self-hosted from `assets/`. This folder documents where each file came from, how it was
produced, and keeps the licence texts. Nothing in `docs/` is served by the theme.

## The system

| Role | Family | Weights served | Scope (`unicode-range`) | File(s) |
|---|---|---|---|---|
| Latin body, UI and headings | **Nunito** | variable 200–1000 (body 400/700, headings 700) | Latin | `nunito-latin.woff2` |
| Arabic body and UI | **Zain** | 400, 700 | Arabic | `zain-arabic-400.woff2`, `zain-arabic-700.woff2` |
| Arabic headings | **Amiri** | 400, 700 | Arabic | `amiri-arabic-400.woff2`, `amiri-arabic-700.woff2` |
| Decorative accent only | **Playwrite NZ Basic** | variable 100–400 | Latin | `playwrite-nz-basic.woff2` |

Stacks (set once in `snippets/theme-fonts.liquid`, rendered by both layouts and the gift card template):

```css
--font-body-family:    'Nunito', 'Zain', system-ui, 'Segoe UI', Tahoma, sans-serif;
--font-heading-family: 'Nunito', 'Amiri', 'Times New Roman', serif;
--font-accent-family:  'Playwrite NZ Basic', 'Nunito', cursive;   /* only via .font-accent */
```

The Latin face is always first and is scoped to Latin; the Arabic faces are scoped to Arabic.
The browser therefore picks the face per character: in a mixed string such as
«ارتدِ الحكاية — Wear the Story», the Arabic runs render in Zain/Amiri and the Latin runs in
Nunito, with no extra markup. A face is downloaded only when a character in its range is
rendered, so an English-only page never fetches the Arabic files.

Zain 300 was not added: no style in the theme uses a weight below 400.

### Why Playwrite is accent-only

Playwrite NZ Basic is a handwriting script. It was previously the default heading face; it is
now opt-in through the `.font-accent` utility class (short Latin phrases only), because a script
face hurts readability and accessibility when it carries every heading.

### Arabic typography rules (`assets/fonts.css.liquid`)

- Arabic text is never letter-spaced (`html:lang(ar) * { letter-spacing: 0 }`): tracking breaks
  the joins of a cursive script. Dawn letter-spaces body text, headings and buttons.
- Amiri's vertical metrics are tall (hhea ascent + descent = 1124 + 634 = **1.758 em**, Nunito
  is 1.364 em). Dawn's heading line-height (≈1.3) lets stacked marks on consecutive lines touch,
  so Arabic headings use `line-height: 1.55` (1.45 for the display sizes `.h0`, `.hxl`, `.hxxl`).

### Loading

- `fonts.css` (from `assets/fonts.css.liquid`) holds all `@font-face` rules, each with
  `font-display: swap`. Keep the `.css.liquid` extension: `asset_url` only runs in `.liquid` assets.
- Exactly one preload: `zain-arabic-400.woff2` when `request.locale.iso_code == 'ar'`,
  `nunito-latin.woff2` otherwise.
- **Dawn's font pickers** (`type_header_font`, `type_body_font`) are kept in
  `config/settings_schema.json` (setting IDs preserved, theme editor unchanged) but the layouts no
  longer output their `font_face` rules or the `fonts.shopifycdn.com` preconnect. The pickers
  carry an `info` note saying they have no effect. Result: no Shopify-hosted font (Assistant)
  is declared or requested. `heading_scale` and `body_scale` still work.

## Sources and verification

All four Arabic files come from the official [google/fonts](https://github.com/google/fonts)
repository, pinned to the last commit that touched each family:

| Family | Path | Commit | Upstream version | Copyright |
|---|---|---|---|---|
| Zain | `ofl/zain/Zain-Regular.ttf`, `Zain-Bold.ttf` | `361c997df97cbbbce27b401ffb712b6bce2f4b3b` | 2.000 | © 2024 The Zain Project Authors (github.com/googlefonts/zain) |
| Amiri | `ofl/amiri/Amiri-Regular.ttf`, `Amiri-Bold.ttf` | `fffdadf0f0c9cc1ec8b407063424a8bfbee05611` | 1.002 | © 2010-2022 The Amiri Project Authors (github.com/aliftype/amiri) |

Verified with fontTools 4.67 before and after subsetting:

| File | name ID 1/16 | `usWeightClass` | UPM | hhea asc / desc | Arabic code points (U+0600–06FF) |
|---|---|---|---|---|---|
| `Zain-Regular.ttf` → `zain-arabic-400.woff2` | Zain | 400 | 800 | 869 / −459 | 109 → 109 |
| `Zain-Bold.ttf` → `zain-arabic-700.woff2` | Zain | 700 | 800 | 869 / −459 | 109 → 109 |
| `Amiri-Regular.ttf` → `amiri-arabic-400.woff2` | Amiri | 400 | 1000 | 1124 / −634 | 255 → 255 |
| `Amiri-Bold.ttf` → `amiri-arabic-700.woff2` | Amiri | 700 | 1000 | 1124 / −634 | 255 → 255 |

Neither licence declares a Reserved Font Name, so the subsets may keep the family names.

### Subsetting command

```sh
U="U+0020,U+00A0,U+0600-06FF,U+0750-077F,U+08A0-08FF,U+FB50-FDFF,U+FE70-FEFF,U+200C-200F,U+2010-2027,U+2039-203A,U+25CC"
pyftsubset Zain-Regular.ttf --unicodes="$U" --layout-features='*' --flavor=woff2 \
  --name-IDs='*' --output-file=zain-arabic-400.woff2
# same for Zain-Bold → zain-arabic-700, Amiri-Regular → amiri-arabic-400, Amiri-Bold → amiri-arabic-700
```

Ranges: Arabic, Arabic Supplement, Arabic Extended-A, Presentation Forms A and B (Arabic
punctuation and Arabic-Indic digits are inside U+0600–06FF), ZWNJ/ZWJ and direction marks,
general punctuation, space/NBSP, and U+25CC (dotted circle, used by the shaper for isolated marks).
`--layout-features='*'` keeps every GSUB/GPOS feature so joining, ligatures and mark positioning
work. `--name-IDs='*'` keeps the copyright and licence name records.

### Files

| File | Bytes | SHA-256 |
|---|---|---|
| `assets/nunito-latin.woff2` | 39,128 | `ba344451eab25b217a165363b1982048a5e5830a0daf36577973955a04cac793` |
| `assets/playwrite-nz-basic.woff2` | 37,308 | `947c7f80daa998895febff219375966a9d0e6612d800da367da9d8ae9db7f61e` |
| `assets/zain-arabic-400.woff2` | 32,476 | `bf1720817247f8d21781a80f1375eea312fd585125803a9ce311656f2151009e` |
| `assets/zain-arabic-700.woff2` | 32,292 | `646703bc9066553997cde42a55b503af06a86321014720b962e235e3410a6150` |
| `assets/amiri-arabic-400.woff2` | 109,176 | `6213f582b0e8788c6f870e524231a9660bd4922382fe5193cb1acfb7780e8df4` |
| `assets/amiri-arabic-700.woff2` | 109,304 | `a2a6e11492cb2a2f4420ba4bd370e7e1e8d2d4c0ba6a5f2935b199a06da35677` |
| **Total** | **359,684** (≈351 KB) | |

Amiri stays relatively large after subsetting because its GSUB closure keeps ~5,900 glyphs
(Naskh ligatures and mark variants). It is only fetched when Arabic heading text renders.

### Latin files (unchanged)

- **Nunito** — Google Fonts CSS2 API, `family=Nunito:wght@200..1000`, v32 Latin subset,
  `https://fonts.gstatic.com/s/nunito/v32/XRXV3I6Li01BKofINeaB.woff2`. Variable `wght` 200–1000.
  © 2014 The Nunito Project Authors (github.com/googlefonts/nunito).
- **Playwrite NZ Basic** — Google Fonts CSS2 API, `family=Playwrite+NZ+Basic:wght@100..400`, v1,
  `https://fonts.gstatic.com/s/playwritenzbasic/v1/YcmrsYdNS1SdgmGbGgtRtk4ljD2L-0ttuA.woff2`.
  Variable `wght` 100–400. © 2023 The Playwrite Project Authors (github.com/TypeTogether/Playwrite).
  "Playwrite NZ Basic" is the official family name.

## Licences

| Family | Licence | Text | Self-hosting / web embedding |
|---|---|---|---|
| Nunito | SIL OFL 1.1 | `licenses/OFL-Nunito.txt` | permitted |
| Playwrite NZ Basic | SIL OFL 1.1 | `licenses/OFL-PlaywriteNZBasic.txt` | permitted |
| Zain | SIL OFL 1.1 | `licenses/OFL-Zain.txt` | permitted |
| Amiri | SIL OFL 1.1 | `licenses/OFL-Amiri.txt` | permitted |

An earlier Arabic font was withdrawn on 2026-10-20 because its licence forbids web embedding;
see `docs/DECISIONS.md`.
