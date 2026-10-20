# Implementation Plan: Merchant-Editable Homepage Hero Section

**Branch**: `001-homepage-hero` | **Date**: 2026-10-18 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-homepage-hero/spec.md`

## Summary

Deliver one new, reusable, merchant-editable Shopify OS 2.0 section — a full-width hero
(image with overlaid, centered text, falling back to a centered text block when no image is
configured) — plus the supporting assets, locale keys, and verified-font wiring it needs.

The section is delivered **unplaced**: `templates/index.json` is not modified, so the existing
homepage (image banner + featured collection) is untouched and the merchant adds the hero from
the theme editor. All hero copy is served from theme locale keys (English and Arabic) so the
same section renders per-locale copy, and the section reuses Dawn conventions (blocks, color
scheme, `.button` classes, responsive `image_tag`) rather than inventing new ones.

## Technical Context

**Language/Version**: Liquid (Shopify OS 2.0), CSS, minimal/zero JavaScript. Shopify CLI 4.9.4;
theme baseline Dawn per `AGENTS.md`.

**Primary Dependencies**: Shopify platform (Liquid, JSON templates, section schema, `image_url`/
`image_tag`, color schemes, locale files). No third-party apps or paid dependencies. Reuses the
already-shipped `assets/fonts.css.liquid`.

**Storage**: Shopify store objects (products/collections/pages) and theme settings only — no
local datastore. `templates/index.json` is deliberately **not** modified by this feature.

**Testing**: `shopify theme check` (static, via the Shopify CLI) plus manual verification on the
unpublished **development** theme (`shopify theme dev`, `http://127.0.0.1:9292`): responsive,
keyboard/contrast, LTR, and (once Arabic is enabled) RTL. Dawn ships no unit-test framework, so
there is no automated test runner; verification is scripted HTTP/HTML checks plus browser review
(see [quickstart.md](./quickstart.md)).

**Target Platform**: Shopify Online Store 2.0 storefront; evergreen desktop and mobile browsers;
both LTR (English) and RTL (Arabic) directions.

**Project Type**: Single project — a Shopify Liquid storefront theme (repository root is the
theme root).

**Performance Goals**: No cumulative layout shift attributable to the hero (SC-009); the hero
image is served responsively (`image_url`/`image_tag` with `widths`/`sizes`) and, when the hero
is the first section, loads with `fetchpriority="high"`; no new blocking resources.

**Constraints**: OS 2.0 + Dawn conventions; existing section setting IDs and merchant
configuration preserved; no publish and no live-theme changes (development theme only); the
[withdrawn Arabic font] font license restricts hosted web embedding (already on record, dev-theme test only);
Arabic store language is **not** enabled by this feature.

**Scale/Scope**: One new section (`sections/hero.liquid`), one CSS asset, ~10 settings, 3 blocks,
locale keys in 4 locale files, and wiring the already-verified `[withdrawn Arabic display font]` family
(5 weights). No new pages, apps, or JavaScript.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| # | Principle | Gate | Status |
|---|-----------|------|--------|
| I | Shopify-Native Architecture (NON-NEGOTIABLE) | Liquid/OS 2.0 only; merchant-editable via schema; existing setting IDs preserved; shared markup not duplicated | ✅ Pass |
| II | Cultural Heritage & Brand Fidelity | Brand palette via existing color-scheme mechanism; no invented business claims; fictional content clearly labelled | ✅ Pass |
| III | Font Verification Before Use | Only verified families/weights used (Nunito, Playwrite NZ Basic, [withdrawn Arabic text font], [withdrawn Arabic display font] — all inspected with `fontTools`); system fallbacks present | ✅ Pass |
| IV | Bilingual Localization & Direction | Copy from locale files; CSS logical properties; no duplicated RTL stylesheet; language selector out of scope | ✅ Pass (RTL verifiable only once Arabic is enabled — recorded) |
| V | Accessibility, Responsiveness & Quality | Semantic markup, `<h2>` heading, keyboard-operable controls with visible focus, WCAG AA contrast, deliberate mobile layout, defined empty states | ✅ Pass |
| VI | Evidence-Based Verification | Acceptance criteria + verification steps defined; loading verified by HTTP checks; unverified items labelled untested | ✅ Pass |
| VII | Incremental Milestone Workflow | Spec → clarify → plan completed; this is the first implementation milestone; no scope creep | ✅ Pass |
| VIII | Git & Store Safety | Dev theme only; no publish; no commit; live Horizon untouched; no credentials; font-license caveat recorded | ✅ Pass |

**Post-Phase-1 re-check:** ✅ Still passes. One preference deviation (new section rather than
extending `image-banner`) is justified under Complexity Tracking.

## Project Structure

### Documentation (this feature)

```text
specs/001-homepage-hero/
├── spec.md              # Feature specification (already complete)
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── hero-section-contract.md   # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
```

### Source Code (repository root)

```text
sections/
└── hero.liquid                     # NEW: the merchant-editable hero section (unplaced)

assets/
├── component-hero.css              # NEW: hero styles (CSS logical properties for RTL)
├── fonts.css.liquid                # EXTEND: add [withdrawn Arabic display font] @font-face (arabic range)
└── [withdrawn-arabic-display-font].woff2  # NEW: 5 verified weights (light/regular/medium/bold/black)

layout/
└── theme.liquid                    # EXTEND: add [withdrawn Arabic display font] to --font-heading-family;
                                    #         add direction (`dir`) handling for RTL locales

locales/
├── en.default.json                 # EXTEND: sections.hero.* storefront copy keys
├── ar.json                         # NEW:    sections.hero.* Arabic storefront copy keys
├── en.default.schema.json          # EXTEND: sections.hero.* editor labels + setting defaults
└── ar.schema.json                  # NEW:    sections.hero.* Arabic editor labels + defaults

docs/fonts/
└── README.md                       # EXTEND: record [withdrawn Arabic display font] wiring

# Explicitly NOT modified:
templates/index.json                # homepage left untouched (section ships unplaced)
sections/image-banner.liquid        # existing hero/section preserved
```

**Structure Decision**: The repository root **is** the Shopify theme; no new top-level
directories are introduced. The feature adds one section under `sections/`, one stylesheet under
`assets/`, locale keys under the existing `locales/`, and four small additive edits to existing
theme files (`assets/fonts.css.liquid`, `layout/theme.liquid`, and the two existing `en.*` locale
files). Everything else is new files only.

## Complexity Tracking

> Justified deviations from preferences (not constitution violations).

| Deviation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| New `sections/hero.liquid` instead of extending `sections/image-banner.liquid` | Spec FR-019 forbids modifying existing homepage sections, and the constitution preserves existing section setting IDs / merchant config. The hero also needs locale-keyed copy, a dedicated alt-text setting, and a text-only (no-image) presentation that `image-banner` does not provide. | Extending `image-banner` would change a stock Dawn section's behaviour and settings for every existing use, risking Dawn-update conflicts and violating FR-019 without owner approval. |
| Dual locale namespace for hero copy (schema keys **and** storefront `t` keys) | Shopify resolves section-schema `t:` defaults from `*.schema.json` (editor UX), while runtime `t` lookups resolve from `*.json` (storefront). To have both a locale-correct editor default **and** per-locale storefront copy (FR-011) when a value is untouched, the keys exist in both namespaces. | Storing copy only in schema files leaves the storefront showing one language's default for all locales; storing it only in storefront files leaves the editor defaults blank, which fails the merchant-editable-experience goal (FR-002…FR-005 defaults). |
| `dir` handling added to `layout/theme.liquid` | Dawn sets `lang` but never `dir`; without a `dir="rtl"` on `<html>`, CSS logical properties cannot flip and FR-012 cannot be satisfied. | Per-hero RTL overrides would duplicate stylesheets, which constitution IV forbids, and could not correct bidi text at the document level. |
