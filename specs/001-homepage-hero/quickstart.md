# Quickstart & Validation: Homepage Hero Section

**Feature**: `001-homepage-hero` | **Date**: 2026-10-18

Runnable scenarios that prove the hero works end-to-end. They validate the contract in
[`contracts/hero-section-contract.md`](./contracts/hero-section-contract.md) and the entities in
[`data-model.md`](./data-model.md). Implementation detail lives in `tasks.md`, not here.

---

## Prerequisites

| Item | Value |
|------|-------|
| Shopify CLI | 4.9.4 (already installed) |
| Development theme | `142644281431` on `s8vaej-jj.myshopify.com` |
| Live theme (**do not touch**) | Horizon `142642937943` |
| Storefront password | `iaplay` |
| Dev server (optional) | `shopify theme dev` → `http://127.0.0.1:9292` |
| Regression floor | `shopify theme check` → 156 files, 9 warnings / 8 files |

> All validation happens on the **unpublished development theme**. Never run `theme push --live`
> or `theme publish` during this milestone (constitution VIII).

---

## Scenario 1 — Static integrity (no regressions)

```powershell
shopify theme check
```

**Expected**: file count ≤ 156 and warnings ≤ 9, with **no** new offence mentioning
`sections/hero.liquid`, `assets/component-hero.css`, `assets/fonts.css.liquid`, or `locales/ar*`.
Covers: compatibility contract §5.

## Scenario 2 — The section is unplaced on delivery

```powershell
git diff --stat -- templates/ ; git diff -- templates/index.json
```

**Expected**: empty output — `templates/index.json` is byte-identical, so the homepage still shows
only `image_banner` + `featured_collection`. Covers: FR-001, FR-019.

## Scenario 3 — Merchant adds the hero from the editor

1. `shopify theme dev` (or open the dev theme's editor).
2. Customize homepage → **Add section** → *Hero*.
3. Observe the preset places Heading + Text + Buttons blocks, each pre-filled with localized copy.

**Expected**: the hero appears in the list, is added with its three preset blocks, and exposes all
settings from contract §2. Covers: FR-001, FR-002, FR-003, FR-004, FR-005.

## Scenario 4 — Heading hierarchy

With the hero on the homepage, inspect the rendered HTML.

**Expected**: exactly one `<h1>` (from `sections/header.liquid`) and the hero contributes a
`<h2 class="hero-section__heading …">`. No second `<h1>`. Covers: FR-014.

## Scenario 5 — Image present, overlay legible

Set an image; leave overlay at default.

**Expected**: full-width image with overlaid centred content; the content block's alignment
follows the configured position; overlaid text meets WCAG AA against the image. Covers: FR-006,
FR-008.

## Scenario 6 — No image (text-only fallback)

Clear the image setting.

**Expected**: **no** media area or placeholder graphic; the content renders as a centred text
block on the colour-scheme background with comfortable spacing — not a collapsed strip or an empty
box. Covers: FR-007.

## Scenario 7 — Colour scheme only

Switch `color_scheme` between schemes.

**Expected**: only the theme's scheme colours change; no hero-specific colours appear. Covers:
FR-009.

## Scenario 8 — Keyboard and focus

Tab from the top of the page through the hero.

**Expected**: both CTAs are reachable in order with a visible focus indicator; no keyboard trap;
CTAs are real links (navigate with Enter). Covers: FR-015.

## Scenario 9 — Responsive behaviour

Check 375 px, 768 px and 1440 px widths (dev tools).

**Expected**: intentional layout at each width; no horizontal scroll; no layout shift as the hero
image loads. Covers: SC-009, constitution V.

## Scenario 10 — LTR/RTL direction

With English active (LTR), confirm text and content order. Then simulate RTL with
`dir="rtl"` on `<html>` in dev tools (Arabic is not enabled yet).

**Expected**: LTR is correct; under the RTL override the content block and any physical-looking
alignment tokens mirror correctly with **no duplicated stylesheet**. Covers: FR-012.

> Recorded caveat: full RTL verification is deferred until the Arabic store language is enabled
> (`research.md` R4). Do not claim RTL as proven before then.

## Scenario 11 — CTA destinations

Click both CTAs.

**Expected**: primary goes to the all-products collection; secondary goes to the demo *Tatreez*
page and does **not** 404. Covers: FR-004, FR-005, FR-010.

## Scenario 12 — No new runtime dependencies

Inspect the rendered `<head>`/`<body>` additions.

**Expected**: only `component-hero.css` is added; no new `<script>`, no third-party origin. Covers:
FR-016.

---

## Exit criteria

The milestone is complete when Scenarios 1–12 pass on the development theme, the theme-check
regression floor holds, `templates/index.json` is unchanged, and no publish has occurred. Any
scenario that cannot be run (e.g. Scenario 10's full RTL pass) is reported explicitly as untested
rather than assumed (constitution VI).
