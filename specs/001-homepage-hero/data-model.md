# Phase 1 Data Model: Merchant-Editable Homepage Hero Section

**Feature**: `001-homepage-hero` | **Date**: 2026-10-18

This is a Shopify Liquid theme, so there is no database. The "data model" is the set of
**merchant-editable theme artefacts** the feature introduces: a section, its blocks and settings,
the store objects it references, and the locale keys that supply its copy. Field names below are
the exact setting/block IDs that appear in the section schema and in `templates/*.json` once a
merchant adds the section.

---

## Entity: Hero Section  (`sections/hero.liquid`)

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `id` | string | yes | platform-generated | Shopify section instance id (`section.id`). |
| `color_scheme` | `color_scheme` ref | yes | `scheme-1` | FR-009; reference to a scheme in `config/settings_schema.json`. |
| `image` | `image_picker` | no | blank | FR-006; blank ⇒ text-only presentation (FR-007). |
| `image_alt` | `text` | no | blank | FR-006; blank ⇒ fall back to `image.alt`. |
| `image_height` | `select` | yes | `large` | Layout control; constrained to Dawn-like steps. |
| `image_overlay_opacity` | `range` (0–100) | yes | `40` | Keeps overlaid text legible (FR-008). |
| `desktop_content_position` | `select` | yes | `middle-center` | Where the content block sits on desktop. |
| `desktop_content_alignment` | `select` | yes | `center` | Text alignment; must resolve **logically** for RTL. |
| `mobile_content_alignment` | `select` | yes | `center` | Text alignment on small screens. |
| `heading_size` | `select` | yes | `h1` | **Visual** size only (class on the `<h2>`); never changes the heading level (FR-014). |
| `blocks` | block list | yes (via preset) | heading, text, buttons | At most one of each; enforced by block `limit` (FR-002). |

**Relationships**
- `color_scheme` → a scheme defined in `config/settings_schema.json`.
- `image` → a Shopify image/file object; the section also reads `image.alt` (R8).
- `blocks[]` → zero-or-one Heading, zero-or-one Text, zero-or-one Buttons.
- `blocks.buttons.button_link_*` → a Shopify `url` (collection, page, or any store URL).

**Lifecycle / state transitions**
1. **Unplaced** — the section exists in the theme, is listed in the editor via `presets`, and is
   referenced by no template. This is the state delivered by the feature; `templates/index.json`
   is unchanged (FR-001, FR-019).
2. **Added** — a merchant inserts the hero from the theme editor; Shopify writes the section and
   its preset blocks into a template's JSON with defaults resolved.
3. **Configured** — the merchant edits settings/blocks.
4. **Published** — merchant publishes the theme containing the placement. **Out of scope**: the
   feature never publishes and never edits the live Horizon theme (constitution VIII).

---

## Entity: Heading block  (`type: "heading"`)

| Field | Type | Required | Default (English) | Notes |
|-------|------|----------|-------------------|-------|
| `heading` | `inline_richtext` | yes | `t:sections.hero.blocks.heading.settings.heading.default` | FR-002; drives the single hero `<h2>` (FR-014). |

- Validation: rendered as `<h2>`; the block contributes the section's main visible heading.
- Collapsed/empty value ⇒ the section must not render an empty heading element.

## Entity: Text block  (`type: "text"`)

| Field | Type | Required | Default (English) | Notes |
|-------|------|----------|-------------------|-------|
| `text` | `inline_richtext` | no | `t:sections.hero.blocks.text.settings.text.default` | FR-003; supporting sentence. |

## Entity: Buttons block  (`type: "buttons"`)

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `button_label_1` | `inline_richtext` | yes | `t:sections.hero.blocks.buttons.settings.button_label_1.default` | FR-004; primary CTA label. |
| `button_link_1` | `url` | yes | `/collections/all` | FR-004/FR-018; defaults to the all-products collection. |
| `button_style_secondary_1` | `checkbox` | no | `false` | Renders `.button--secondary`. |
| `button_label_2` | `inline_richtext` | no | `t:sections.hero.blocks.buttons.settings.button_label_2.default` | FR-005; secondary CTA label. |
| `button_link_2` | `url` | no | `/pages/tatreez` | FR-005; demo "Tatreez" page (R10). |
| `button_style_secondary_2` | `checkbox` | no | `true` | Secondary visual style by default. |

- Validation: each button renders only when **both** its label and link are non-blank; a link
  without a label (or vice-versa) must not produce an empty or dangling control (FR-005).

---

## Entity: Hero Image (derived, not stored by the theme)

| Field | Source | Notes |
|-------|--------|-------|
| `image` | merchant `image_picker` | Aspect ratio drives the section's intrinsic sizing (no CLS, SC-009). |
| `alt` | `image_alt` setting → `image.alt` → `''` | FR-006 resolution order (R8). |
| responsive sources | `image_url`/`image_tag` `widths` + `sizes` | R5; AVIF/WebP/JPEG by browser support. |

## Entity: CTA Link (derived)

| Field | Notes |
|-------|-------|
| `label` | Translatable, from the Buttons block. |
| `url` | Store-relative or Shopify route via a `url` setting (FR-018). |
| `style` | `primary` or `secondary` class only. |
| `accessible_name` | Equals the visible label (no icon-only CTAs). |

---

## Entity: Locale String Set  (`sections.hero.*`)

Two mirrored namespaces (see `research.md` R2/R3):

| Namespace | Files | Consumer |
|-----------|-------|----------|
| Schema | `locales/en.default.schema.json`, `locales/ar.schema.json` | Theme editor labels + setting defaults |
| Storefront | `locales/en.default.json`, `locales/ar.json` | Runtime `t` lookups / copy fallback |

Key shape (identical keys in all four files):

```text
sections.hero.name
sections.hero.presets.name
sections.hero.settings.<setting>.label            # image_height, image_alt, color_scheme, …
sections.hero.settings.<select_option>.label      # per-option labels for the selects
sections.hero.blocks.heading.name
sections.hero.blocks.heading.settings.heading.label
sections.hero.blocks.heading.settings.heading.default
sections.hero.blocks.text.name
sections.hero.blocks.text.settings.text.label
sections.hero.blocks.text.settings.text.default
sections.hero.blocks.buttons.name
sections.hero.blocks.buttons.settings.button_label_1.label
sections.hero.blocks.buttons.settings.button_label_1.default
sections.hero.blocks.buttons.settings.button_label_2.label
sections.hero.blocks.buttons.settings.button_label_2.default
```

- Validation (FR-011): no hero string may exist in Liquid; every visible string resolves from one
  of these keys. English and Arabic key sets must be **identical in shape**.
- Arabic is added to the theme only; the store language is not enabled (clarification decision 4).

---

## Cross-cutting validation rules

| Rule | Source |
|------|--------|
| Exactly one hero heading element, and it is `<h2>`; the document keeps a single `<h1>` from the header. | FR-014 |
| Colours come only from the selected colour scheme; no literal brand colours in the hero. | FR-009 |
| Every interactive control is reachable by keyboard and shows a visible focus state. | FR-015 |
| Layout uses logical properties so `dir="rtl"` flips it without a second stylesheet. | FR-012 |
| No new blocking JS; no third-party runtime dependency. | FR-016 / constitution I |
| Section works with image blank (text-only) **and** with image present. | FR-007 |
| Section must not appear on the storefront until a merchant places it. | FR-001 |
