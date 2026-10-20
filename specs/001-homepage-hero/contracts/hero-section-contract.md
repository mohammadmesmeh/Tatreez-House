# Interface Contract: Hero Section

**Feature**: `001-homepage-hero` | **Date**: 2026-10-18

This theme's externally-observable interfaces are (a) the **section schema** the theme editor
renders for merchants, (b) the **rendered DOM/semantics** the storefront and assistive technology
consume, and (c) the **locale key set** translators and the localization platform rely on. Each is
specified below as a contract the implementation must satisfy.

---

## 1. Editor contract — section registration

```jsonc
{
  "name": "t:sections.hero.name",
  "tag": "section",
  "class": "section hero-section",
  "disabled_on": { "groups": ["header", "footer"] },
  "blocks": [ /* { "type": "heading" }, { "type": "text" }, { "type": "buttons" } */ ],
  "settings": [ /* see §2 */ ],
  "presets": [
    { "name": "t:sections.hero.presets.name",
      "blocks": [ { "type": "heading" }, { "type": "text" }, { "type": "buttons" } ] }
  ]
}
```

**Guarantees**
- The section is offered in the editor's "Add section" list **only** through `presets`; it is not
  referenced by any template on delivery (FR-001).
- `class` includes Dawn's shared `section` class so section spacing stays consistent.
- `disabled_on` keeps the hero out of header/footer groups.

## 2. Editor contract — setting IDs and types

| ID | Type | Options / range | Default | Required |
|----|------|-----------------|---------|----------|
| `image` | `image_picker` | — | — | no |
| `image_alt` | `text` | — | `""` | no |
| `image_height` | `select` | `adapt` \| `small` \| `medium` \| `large` | `large` | yes |
| `image_overlay_opacity` | `range` | min 0, max 100, step 5 | `40` | yes |
| `color_scheme` | `color_scheme` | schemes from `settings_schema.json` | `scheme-1` | yes |
| `desktop_content_position` | `select` | `top-left`…`bottom-right` | `middle-center` | yes |
| `desktop_content_alignment` | `select` | `left` \| `center` \| `right` | `center` | yes |
| `mobile_content_alignment` | `select` | `left` \| `center` \| `right` | `center` | yes |
| `heading_size` | `select` | size classes (`h0`, `h1`, `h2`, `hxl`, `hxxl`) | `h1` | yes |

**Guarantees**
- Setting IDs are **new**; none collide with or rename any existing Dawn setting (constitution I).
- The three `*_alignment`/`*_position` options store physical-looking tokens but the markup applies
  them through logical properties, so `left`/`right` resolve to start/end under `dir="rtl"`
  (FR-012).
- `heading_size` selects a **class**, never an element name (FR-014).

## 3. Storefront DOM contract

```html
<section id="Hero-{{ section.id }}" class="hero-section color-{{ color_scheme }}">
  <div class="hero-section__media">            <!-- omitted entirely when image is blank -->
    <img … width height sizes srcset alt="…" /> <!-- alt = image_alt | image.alt | '' -->
  </div>
  <div class="hero-section__content">
    <h2 class="hero-section__heading inline-richtext {{ heading_size }}">…</h2>
    <div class="hero-section__text rte">…</div>
    <div class="hero-section__buttons">
      <a class="button" href="…">…</a>          <!-- primary -->
      <a class="button button--secondary" href="…">…</a>
    </div>
  </div>
</section>
```

**Guarantees**
- **Exactly one** heading element and it is `<h2>`. The page keeps its single `<h1>` from
  `sections/header.liquid` (FR-014).
- No media wrapper is emitted when no image is configured, and the content is centred on the
  colour-scheme background (FR-007).
- Colours resolve from the `color-*` class only (FR-009).
- `alt` follows `image_alt → image.alt → ''`; an empty `alt` is emitted only for a genuinely
  decorative image (FR-006).
- Each CTA renders **iff** both label and link are non-blank (FR-005).
- No inline `onclick`, no third-party script tag (FR-016).
- Every copy string is produced by a `t` lookup or a setting whose default is a `t` key — no
  literal UI prose in Liquid (FR-011).

## 4. Localization contract — locale keys

See `data-model.md` → *Locale String Set* for the full key tree. The contract is:

| Rule | Detail |
|------|--------|
| Namespace | `sections.hero.*` only; no keys placed in `general.*` or other sections' namespaces. |
| Mirroring | `en.default.json` / `en.default.schema.json` / `ar.json` / `ar.schema.json` expose an **identical key shape**. |
| Defaults | Every merchant-editable copy setting's `default` is a `t:` key, and the same key also exists in the storefront files for runtime fallback. |
| Placeholders | Any interpolated variable in a string uses `{{ }}` / `%{}` correctly per Shopify locale rules. |
| Publication | Files are added; the Arabic store language is **not** enabled by the feature. |

## 5. Compatibility contract

| Constraint | Guarantee |
|------------|-----------|
| OS 2.0 | Section is JSON-template compatible and editor-safe. |
| Existing setting IDs | None renamed, removed, or repurposed. |
| Homepage | `templates/index.json` byte-identical after the feature. |
| Live theme | Never read from, written to, or published. |
| Regression floor | `shopify theme check` count ≤ 156 files / 9 warnings, no new offence. |
| Fonts | Only families verified with `fontTools` are referenced (constitution III). |
