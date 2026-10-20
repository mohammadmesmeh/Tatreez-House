# Phase 0 Research: Merchant-Editable Homepage Hero Section

**Feature**: `001-homepage-hero` | **Date**: 2026-10-18

All Technical Context unknowns were resolved by inspecting the actual theme in this repository
and the Shopify platform behaviour it already relies on. No `NEEDS CLARIFICATION` items remain.

---

## R1 — Section architecture: new section vs extending `image-banner`

**Decision**: Add a new, standalone section `sections/hero.liquid`, advertised to the theme
editor through a `presets` entry. Do **not** modify `sections/image-banner.liquid`.

**Rationale**:
- `sections/image-banner.liquid` already implements a full-width image with overlaid centred
  text (`<h2 class="banner__heading … {{ heading_size }}">`), a `color_scheme` setting, an
  overlay-opacity setting, and heading/text/buttons blocks. It is the correct *convention* to
  mirror, but it is a **stock Dawn file in active use** by `templates/index.json`.
- FR-019 requires that adding the hero not modify existing homepage sections; the constitution
  requires preserving existing section setting IDs and merchant configuration. Editing a stock
  section changes its behaviour for every existing placement and invites merge conflicts on
  Dawn updates.
- The hero also needs capabilities `image-banner` does not expose: copy served from locale keys
  (FR-011), a dedicated alternative-text setting (FR-006), and a deliberate **text-only**
  presentation when no image is set (FR-007), rather than Dawn's placeholder-SVG media area.

**Alternatives considered**:
1. *Extend `image-banner` in place* — rejected: violates FR-019 / constitution I without owner
   approval and risks Dawn-update conflicts.
2. *Reuse `image-banner` unchanged via a preset* — rejected: cannot satisfy FR-006 (editable
   alt text), FR-007 (text-only fallback), or FR-011 (locale-keyed copy).
3. *Build the hero from `custom-liquid`* — rejected: not merchant-editable through a schema,
   violates constitution I.

---

## R2 — Localization strategy for hero copy

**Decision**: Every piece of hero copy (headline, supporting text, both CTA labels) is addressed
through translation keys under the `sections.hero.*` namespace. Two coordinated mechanisms are
used so that the copy is correct in **both** the theme editor and the storefront:

1. **Editor defaults** — section-schema setting defaults reference the keys, e.g.
   `"default": "t:sections.hero.blocks.heading.settings.heading.default"`. Shopify resolves
   schema `t:` lookups from `*.schema.json`.
2. **Storefront fallback** — the Liquid renders the merchant's value when present and otherwise
   falls back to the same key via `| default: '<key>' | t`. Shopify resolves runtime `t` lookups
   from `*.json`.

**Rationale**: A Shopify section-setting default is resolved when the merchant adds the section
and the resolved string is then stored in the template JSON; on its own that would pin the
storefront to one language regardless of locale. The runtime fallback guarantees an *untouched*
hero renders per-locale copy (FR-011), while the schema default keeps the theme editor
merchant-friendly (FR-002…FR-005 defaults) instead of showing empty fields.

**Alternatives considered**:
1. *Schema defaults only* (the stock Dawn pattern) — rejected: storefront shows one language for
   all locales, failing FR-011's "each locale shows its own copy".
2. *Storefront keys only* — rejected: the editor shows blank defaults, harming the
   merchant-editable experience the feature exists to provide.
3. *Rely on the Translate & Adapt app for all copy* — rejected: the feature must not introduce an
   app dependency, and FR-011 requires theme locale files to carry the text.
4. *Hardcode English/Arabic strings in Liquid* — rejected: explicitly forbidden by FR-011 and
   constitution IV.

**Recorded trade-off**: the four copy strings consequently appear in two namespaces
(`*.schema.json` for the editor, `*.json` for the storefront). This intentional duplication is
logged in `plan.md` → Complexity Tracking.

---

## R3 — Locale file scope and Arabic enablement

**Decision**: Extend `locales/en.default.json` and `locales/en.default.schema.json`; create
`locales/ar.json` and `locales/ar.schema.json`. Do **not** add or publish Arabic in the store.

**Rationale**:
- Dawn ships `locales/<lang>.json` + `locales/<lang>.schema.json` for ~30 languages; **Arabic is
  absent**, so `ar` files are genuinely new, not overwrites.
- Adding theme locale files for a language the store has not enabled is inert: it makes the theme
  *translation-ready* (FR-011) without publishing a language, matching clarification decision 4.
- The two file families serve different consumers (`*.schema.json` → theme editor; `*.json` →
  storefront), which is why both are required by R2.

**Alternatives considered**: only `en` files (rejected — no Arabic copy, fails FR-011);
store language publication (rejected — out of scope and forbidden by the clarification).

---

## R4 — Bilingual direction (RTL) handling

**Decision**: Style the hero exclusively with **CSS logical properties**
(`text-align: center` where symmetric, `inset-inline-*`, `padding-inline`, `margin-inline`,
`border-inline`). Add direction handling to `layout/theme.liquid`, setting
`dir="rtl"` on `<html>` when the active locale is right-to-left (derived from
`request.locale.iso_code`), otherwise `dir="ltr"`.

**Rationale**:
- Dawn's stock stylesheets (including `section-image-banner.css`) use physical offsets
  (`left`/`right`), which do not flip. Reusing them would break FR-012 in RTL.
- `layout/theme.liquid` currently sets `lang` but never `dir`; without a `dir` attribute, logical
  properties cannot flip and bidi text order is wrong at the document level.
- constitution IV forbids shipping a duplicated RTL stylesheet, so a single logical-property
  stylesheet plus a document-level `dir` is the only compliant route.

**Alternatives considered**: a separate `*-rtl.css` (rejected — duplication, forbidden);
per-section `[dir]` overrides (rejected — cannot fix document-level bidi, still duplicates).

**Verification caveat (honest)**: with Arabic not enabled, `dir="rtl"` cannot be exercised on the
dev storefront. RTL will be verified with the dev tools' `dir="rtl"` override and re-verified
when Arabic is enabled; the plan records it as deferred rather than proven.

---

## R5 — Responsive, optimized imagery

**Decision**: Render the hero image with `image_url` / `image_tag`, supplying a `widths`
ladder and a `sizes` expression matching the layout, plus `fetchpriority="high"` when the hero is
the first section on the page. Fall back to the Shopify `placeholder-svg` **only** when the
merchant has explicitly configured an image setting that is empty in a way that should still show
media — see R11: by default, no image means no media area.

**Rationale**: This is Dawn's own approach; it yields correctly sized AVIF/WebP/JPEG sources and
avoids hand-rolled `srcset`. Serving the hero image responsively with an intrinsic aspect ratio is
what keeps hero CLS at zero (SC-009).

**Alternatives considered**: fixed-size `img` (rejected — poor mobile cost, CLS risk);
CSS `background-image` (rejected — not responsive, not accessible).

---

## R6 — Colour scheme integration

**Decision**: Expose a `"type": "color_scheme"` setting (default `scheme-1`) and wrap the section
in `color-{{ section.settings.color_scheme }}`, exactly as stock Dawn sections do.

**Rationale**: FR-009 requires the hero to use the theme's existing colour-scheme mechanism, not
new colours. Dawn's `settings_schema.json` defines colour-scheme settings (three `color_scheme`
entries confirmed), so reusing the type introduces no new tokens.

**Alternatives considered**: bespoke colour settings (rejected — FR-009, constitution II).

---

## R7 — Heading hierarchy and visual prominence

**Decision**: The hero's main visible heading is an `<h2>` element carrying a display-sized visual
class (e.g. `hero__heading h1 …`), so semantics and visual weight are decoupled.

**Rationale**: `sections/header.liquid` renders the homepage's single `<h1>` for
`request.page_type == 'index'`, so a hero `<h1>` would create a second top-level heading and break
FR-014. Dawn's `image-banner` already decouples level from size by putting a size class on an
`<h2>`, so this is the established theme convention.

**Alternatives considered**: hero `<h1>` (rejected — duplicates the document `<h1>`); a plain
unstyled `<h2>` (rejected — would lose the intended visual prominence).

---

## R8 — Alternative text source

**Decision**: Provide a dedicated `image_alt` text setting; when it is blank, fall back to the
picked image's own `alt` value (`section.settings.image.alt`).

**Rationale**: FR-006 requires *merchant-editable* alternative text. Shopify's image picker does
not expose an alt field, so a dedicated setting is the only way the merchant can supply it in the
theme editor, while the image's own `alt` remains a sensible automatic fallback.

**Alternatives considered**: `image.alt` only (rejected — not editable in the editor, fails
FR-006); `alt` from the heading (rejected — decorative duplication).

---

## R9 — Font wiring for Arabic display headings

**Decision**: Ship `[withdrawn Arabic display font]` (five verified static weights: 300/400/500/700/900) as
WOFF2 under `assets/`, add matching `@font-face` rules scoped to the Arabic unicode range in
`assets/fonts.css.liquid`, and insert `[withdrawn Arabic display font]` into `--font-heading-family`
ahead of `[withdrawn Arabic text font]` so Arabic headings prefer the display serif while Latin headings
continue to prefer `'Playwrite NZ Basic'`.

**Rationale**: Clarification decision 3 names [withdrawn Arabic display font] as the Arabic display face,
and the family was already verified with `fontTools` (family `[withdrawn Arabic display font]`, static
weights 300/400/500/700/900, 416 glyphs, Arabic present, not variable). constitution III permits
use only after such verification — done.

**Alternatives considered**: reuse [withdrawn Arabic text font] for display (rejected — clarification chose the
serif display face); a Latin-only heading stack (rejected — Arabic headings would fall through to
the body face).

---

## R10 — CTA defaults and destinations

**Decision**: Both CTAs are `"type": "url"` settings. Primary default `/collections/all`;
secondary default `/pages/tatreez`, pointing at a new, clearly-fictional demo page created in the
development store (handle `tatreez`).

**Rationale**: FR-004/FR-005 and clarification decision 5 fix these defaults. Using `url`
settings (rather than hardcoded hrefs) satisfies FR-018 (no hardcoded store URLs). The demo page
is created as store content, not theme code, and is labelled fictional so it is never mistaken for
real business content (constitution II).

**Alternatives considered**: `collection`/`page` picker types (rejected — less flexible, and the
clarification specified sensible URL defaults); no default link (rejected — FR-004 requires one).

**Dependency**: the secondary default only resolves once the page exists; the implementation
milestone therefore includes creating it, and the link is verified to not 404.

---

## R11 — Presentation when no image is configured

**Decision**: When `section.settings.image` is blank, do not render a media area at all. Render the
content block centred on the section's colour-scheme background with comfortable vertical rhythm,
so the hero is a complete, legible text block rather than a collapsed strip or empty box.

**Rationale**: FR-007 (clarification decision 1) explicitly chooses a centred text block over an
empty area; SC requires no collapsed/blank region. Skipping the media wrapper entirely also avoids
the WCAG issue of decorative placeholder graphics being announced.

**Alternatives considered**: `placeholder-svg` media (rejected — clarification chose the text
block; a placeholder would also be announced to assistive tech); collapsing the section (rejected
— FR-007 forbids an empty/collapsed area).

---

## R12 — Verification strategy and tooling

**Decision**: Verify with `shopify theme check` (static) plus the runnable scenarios in
[quickstart.md](./quickstart.md) against the unpublished **development** theme served by
`shopify theme dev` (`http://127.0.0.1:9292`).

**Rationale**: Dawn ships no unit-test framework, so there is nothing to extend; the platform's own
linter plus rendered-HTML/browser checks are the meaningful evidence available. constitution VI
requires verification evidence that is actually obtainable, and requires anything untested to be
labelled as such.

**Alternatives considered**: adding Jest/Playwright to a Liquid theme (rejected — large new
dependency with no first-class Liquid rendering, outside feature scope); manual review only
(rejected — not repeatable).

---

## R13 — Baseline integrity

**Decision**: Treat the recorded `theme check` baseline as a hard floor: **156 files,
9 warnings across 8 files**, all pre-existing stock Dawn concerns and none font- or hero-related.
The hero work must not add a new offence or a new warning.

**Rationale**: constitution VI and the project's standing "no unverified visual claims" rule; it
gives an objective, cheap regression signal for every task in the milestone.

**Alternatives considered**: no baseline (rejected — loses the only automated signal).
