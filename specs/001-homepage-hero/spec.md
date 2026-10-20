# Feature Specification: Merchant-Editable Homepage Hero Section

**Feature Branch**: `001-homepage-hero`

**Created**: 2026-10-17

**Status**: Draft

**Input**: User description: Define the first feature for Tatreez House — a custom, merchant-editable Shopify homepage hero section that introduces the brand, presents a bilingual headline and supporting text, and guides visitors to the collection and to educational content.

## Clarifications

### Session 2026-10-17

- Q: Which hero layout should this section ship with, given it must stay within layouts the theme already supports? → A: Full-width image with overlaid, centered text (the theme's existing image-banner convention); falls back to a centered text block when no image is set.
- Q: Should the new hero be added alongside the homepage's existing sections, or replace the current image banner? → A: Ship the section unplaced — do not add it to the homepage; the merchant adds it from the theme editor when ready.
- Q: Which verified font should the hero use for each language (Latin body, Latin display, Arabic)? → A: Latin body = Nunito; Latin headline/display = Playwrite NZ Basic; Arabic body = Thmanyah Sans; Arabic headline/display = Thmanyah Serif Display. Drop "Zain" (not present).
- Q: Should this feature set up the Arabic locale and hero translations, or only make the hero translation-ready? → A: Make the hero translation-ready by adding its English and Arabic strings as theme locale keys; do not add or publish the Arabic language in the store in this feature.
- Q: What should the two call-to-action links default to, given their intended destinations may not exist yet? → A: Primary defaults to the all-products collection (`/collections/all`); secondary defaults to a "Tatreez" educational page created in this feature as clearly-fictional demo content.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Visitor understands the brand and reaches the collection (Priority: P1)

A first-time visitor lands on the Tatreez House homepage and sees a hero that states the brand's promise and offers a clear path into the product collection. They immediately understand that this is a Palestinian heritage-inspired brand and know where to go next.

**Why this priority**: The hero is the first impression and the primary entry point to shopping. Without this story there is no meaningful hero feature; everything else enhances it.

**Independent Test**: With the section placed on the homepage via the theme editor and loaded in an empty store context (no image, default text), confirm the brand statement is present and the primary call to action leads to the intended collection. Delivers value on its own as a navigable brand introduction.

**Acceptance Scenarios**:

1. **Given** a visitor on the homepage, **When** the hero loads, **Then** the headline, supporting text, and both call-to-action labels are visible and readable.
2. **Given** the hero is displayed, **When** the visitor activates the primary call to action, **Then** they are taken to the intended collection/page and not to a broken or empty destination.
3. **Given** only the required content is configured (no image), **When** the hero loads, **Then** it still presents all text content clearly with no blank or broken area.

---

### User Story 2 - Merchant customizes the hero without code (Priority: P2)

A store owner or content editor opens the theme editor and changes the hero heading, supporting text, both call-to-action labels and links, and the optional image and its alt text — entirely through editable settings, with no code changes.

**Why this priority**: The project's core goal is a merchant-editable, reusable theme section. If content cannot be edited safely by a non-technical merchant, the feature fails its purpose even if it looks correct.

**Independent Test**: In the theme editor, edit every documented setting, save, and confirm each change is reflected on the storefront; then revert. Delivers value independently as a content-management capability.

**Acceptance Scenarios**:

1. **Given** the section is added to the homepage, **When** the merchant edits the heading, supporting text, and both call-to-action labels and links, **Then** each change is saved and visibly reflected on the storefront.
2. **Given** the merchant adds an image and its alt text, **When** the storefront loads, **Then** the image is displayed with the provided alternative text.
3. **Given** the merchant clears an optional setting (for example, removes the image or leaves one call to action empty), **When** the storefront loads, **Then** the hero degrades gracefully with no empty placeholder, broken link, or visual gap.

---

### User Story 3 - Arabic-speaking visitor gets a native right-to-left experience (Priority: P3)

An Arabic-speaking visitor views the homepage in Arabic and sees the hero copy in Arabic, laid out right-to-left, matching the brand's bilingual heritage positioning.

**Why this priority**: Bilingual support is a defining brand requirement, but it depends on the base hero existing first, so it follows the P1/P2 stories.

**Independent Test**: With the store's Arabic language enabled (a separate step), switch the storefront locale to Arabic and confirm the hero shows the Arabic headline, supporting text, and call-to-action labels, correctly directed right-to-left, with no leftover English defaults or mirrored imagery.

**Acceptance Scenarios**:

1. **Given** the storefront locale is Arabic, **When** the hero loads, **Then** all hero text is displayed in Arabic and the layout reads right-to-left.
2. **Given** the storefront locale is English, **When** the hero loads, **Then** all hero text is displayed in English and the layout reads left-to-right.
3. **Given** a translated string is missing for a locale, **When** the hero loads, **Then** a readable fallback is shown rather than an empty or broken element.

---

### Edge Cases

- **No image configured**: the hero must still render a complete, legible text presentation rather than an empty or collapsed area.
- **Empty heading or empty supporting text**: the remaining content must render without leaving dangling labels, gaps, or unstyled elements.
- **One call to action configured, the other left blank**: only the configured action is shown; no empty button and no link to an undefined destination.
- **Call-to-action link unset or invalid**: the action must not render as a clickable dead link.
- **Very long headline or supporting text (both languages)**: text wraps within the hero without overflow, clipping, or overlap on small screens.
- **Narrow viewport (~320px) and large desktop (≥1920px)**: hero remains readable and correctly balanced at both extremes.
- **Text over a busy or light image**: readability and contrast are preserved (for example, via overlay or contrast-aware treatment).
- **Image fails to load**: alternative text or a sensible background fallback keeps the hero usable.
- **Mixed Arabic and English text in one field**: directional rendering stays correct.
- **Missing translation for a locale**: falls back to a readable default rather than showing an empty string.
- **Brand fonts unavailable or still failing to load**: the hero falls back to a readable system font without layout breakage.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The homepage MUST support a hero section that a merchant can add, remove, and configure from the theme editor. This feature ships the section unplaced: it MUST NOT be added to the homepage template, so existing homepage sections remain unchanged until the merchant places it.
- **FR-002**: The hero MUST display an editable headline, with the English default "Wear the Story. Keep the Heritage." and the Arabic default "ارتدِ الحكاية، واحفظ التراث."
- **FR-003**: The hero MUST display editable supporting text, with the English default "Discover contemporary pieces inspired by Palestinian tatreez." and the Arabic default "اكتشف قطعًا معاصرة تستلهم فن التطريز الفلسطيني."
- **FR-004**: The hero MUST provide a primary call to action with an editable label and link, defaulting to "Explore the Collection" / "اكتشف المجموعة" and the all-products collection (`/collections/all`).
- **FR-005**: The hero MUST provide a secondary call to action with an editable label and link, defaulting to "Discover Tatreez" / "اكتشف فن التطريز" and a "Tatreez" educational page created in this feature as clearly-fictional demonstration content.
- **FR-006**: The hero MUST support an optional image with merchant-editable alternative text.
- **FR-007**: The hero layout MUST be a full-width image with overlaid, centered text, reusing the theme's existing image-banner convention; when no image is configured it MUST fall back to a centered text block. No new layout paradigm is introduced in this feature.
- **FR-008**: The hero MUST degrade gracefully when optional content is missing: no empty buttons, no broken links, and no blank visual gaps.
- **FR-009**: The hero MUST use the store's approved brand colors through the theme's existing color-scheme mechanism rather than hardcoded per-element colors.
- **FR-010**: The hero MUST use the verified brand fonts below, applied only after each family's files, real family names, weights, and licenses are verified: Latin body = Nunito, Latin headline/display = Playwrite NZ Basic, Arabic body = Thmanyah Sans, Arabic headline/display = Thmanyah Serif Display. Display fonts apply to the headline only; supporting text and call-to-action labels use the body font. The brief's "Zain" is dropped (not present in the project); until a family is verified and wired, the hero MUST fall back to the theme's configured typography and system fallbacks.
- **FR-011**: All hero user-facing text MUST be translatable through the store's localization mechanism (theme locale files) so that each locale shows its own copy; no language-dependent text may be hardcoded in the layout. This feature MUST provide the hero's English and Arabic strings as locale keys, but MUST NOT add or publish the Arabic language in the store (store-level Arabic enablement is a separate, owner-approved step).
- **FR-012**: The hero MUST render correctly in both right-to-left (Arabic) and left-to-right (English) directions using direction-aware layout, without mirroring brand marks or product imagery unnecessarily.
- **FR-013**: The hero MUST be responsive, with deliberately designed mobile and desktop presentations rather than a single compressed layout.
- **FR-014**: The hero MUST use semantic markup with a correct heading hierarchy. Its main visible heading MUST be an `<h2>` — the theme's header already renders the homepage's single `<h1>` — kept visually prominent (styled as the display heading) without introducing a second top-level heading; any sub-headings within the hero MUST nest below the `<h2>`.
- **FR-015**: All hero interactive elements MUST be keyboard-operable with a visible focus indicator.
- **FR-016**: Hero text and controls MUST meet WCAG AA contrast for their size against their background, including text placed over imagery.
- **FR-017**: Hero imagery MUST be served responsively and optimized, and the hero MUST avoid unnecessary dependencies or blocking resources.
- **FR-018**: The hero MUST contain no hardcoded store objects (URLs, product/collection handles, prices) beyond editable merchant defaults.
- **FR-019**: Adding the hero MUST NOT modify, replace, or remove existing homepage sections or unrelated theme files without explicit owner approval.

### Key Entities *(include if feature involves data)*

- **Hero Section**: A reusable, merchant-configurable content block consisting of headline, supporting text, two optional call-to-action actions (each with label and link), an optional image with alt text, and presentation settings (layout/alignment/placement within existing conventions, and color scheme).
- **Call-to-Action Action**: A label plus a destination link; used for both the primary and secondary actions and independently optional.
- **Hero Image**: An optional visual asset plus its alternative text, used as the hero's background behind the overlaid text (per the full-width banner layout in FR-007).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A first-time visitor can identify the brand's purpose from the hero and reach the product collection within two interactions from the homepage.
- **SC-002**: The hero renders without horizontal overflow or content clipping at every tested viewport width from 320px to 1920px.
- **SC-003**: Every interactive element in the hero is reachable and operable using the keyboard alone, each showing a visible focus state.
- **SC-004**: Hero text and controls achieve a contrast ratio meeting WCAG AA (at least 4.5:1 for normal text and 3:1 for large text), including when text is layered over an image.
- **SC-005**: The hero displays correct, complete copy and correct reading direction in both English (left-to-right) and Arabic (right-to-left), with no empty or mismatched strings.
- **SC-006**: A non-technical merchant can change the headline, supporting text, both call-to-action labels and links, and the image and its alt text, achieving visible results with zero code edits.
- **SC-007**: When no image is configured, the hero still presents all configured text legibly, with no empty region of the page.
- **SC-008**: Leaving optional settings blank produces no errors, no broken links, and no empty placeholder elements visible to visitors.
- **SC-009**: The hero introduces no cumulative layout shift attributable to its own content (its text/media occupy stable space before images finish loading).

## Open Questions / Unresolved Decisions

None remaining. All previously open questions were resolved in the Clarifications session above (2026-10-17).

## Assumptions

- The project uses an existing Shopify Online Store 2.0 theme (Dawn) and a Shopify CLI development workflow, consistent with the project constitution and `AGENTS.md`.
- Development and verification happen on the unpublished development theme; the live theme is not touched.
- The merchant has theme-editor access to configure section settings.
- The feature is delivered as a new, reusable section that is **not** placed on the homepage by this feature; the merchant adds it from the theme editor. Existing homepage sections are preserved unless the owner explicitly approves replacement.
- Hero default copy is the bilingual text supplied in this feature description; product copy, photography, and final brand assets may not exist yet and are optional for this feature.
- Font application is gated by the constitution's font-verification principle; until fonts are verified and licensed, the hero relies on the theme's configured typography and system fallbacks.
- The store's Arabic language is not enabled by this feature; the hero is delivered with Arabic locale keys (translation-ready), and end-to-end Arabic/RTL verification is deferred to the separate owner-approved enablement step.
- Contrast, keyboard operation, and responsive behavior are verified against the theme's existing browser support and Shopify's theme-editor preview, using standard accessibility tooling.
