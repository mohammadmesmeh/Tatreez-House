# Tasks: Merchant-Editable Homepage Hero Section

**Input**: Design documents from `/specs/001-homepage-hero/`
- plan.md (required)
- spec.md (required for user stories)
- research.md, data-model.md, contracts/hero-section-contract.md, quickstart.md
- `.specify/memory/constitution.md` (project principles; non-negotiable)

**Tests**: OPTIONAL — no automated tests are requested by the spec or present in Dawn; test tasks are not included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing. Only **User Story 1** exists for this feature; it is the MVP.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Path Conventions (Shopify theme, repository root = theme root)

- `sections/`
- `assets/`
- `layout/`
- `locales/`
- `docs/fonts/`
- `templates/` (must remain untouched)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Baseline capture and store-content prerequisites.

- [x] T001 Confirm theme-check baseline and working tree state. Record current `shopify theme check` output (156 files, 9 warnings / 8 files) to compare against later; ensure no uncommitted changes block work. Files: repo root (verification only).
- [ ] T002 [P] Create the fictional "Tatreez" demo page in the development store (`s8vaej-jj.myshopify.com`, theme `142644281431`) with handle `tatreez` so the secondary CTA default `/pages/tatreez` does not 404. (Store content — manual/admin task; do not create theme files.) Verify access to the page after creation. Page title should be 'Tatreez' (clearly fictional demo). Body: short blurb stating it is fictional demonstration content.

**Checkpoint**: Baseline captured; secondary link target exists (or creation tracked).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Changes that affect theme-wide behavior and must be complete before US1 implementation work that depends on them. These are additive and align with constitution III/IV.

- [x] T003 [P] Copy the five verified `Thmanyah Serif Display` static weights (300/400/500/700/900) WOFF2 files into `assets/` (from `docs/fonts/Thmanyah-Font-Family/thmanyah typeface/`), preserving filenames and using only weights that were fontTools-verified. Files: `assets/thmanyah-serif-display-*.woff2` (new).
- [x] T004 [P] Update `assets/fonts.css.liquid` to add `@font-face` declarations for `Thmanyah Serif Display` (arabic range scoped), using the same `font-display`/format conventions as existing declarations; do not duplicate existing `@font-face` rules and do not reference unverified weights. File: `assets/fonts.css.liquid`.
- [x] T005 [P] Update `docs/fonts/README.md` to record the Thmanyah Serif Display wiring (families/weights, purpose: Arabic display headings), provenance/licensing note consistent with existing entries, and the dev-theme-only caveat. File: `docs/fonts/README.md`.
- [x] T006 [P] Update `layout/theme.liquid` to insert `'Thmanyah Serif Display'` into `--font-heading-family` before `'Thmanyah Sans'` (so Arabic headings prefer the display serif; Latin still prefers `'Playwrite NZ Basic'`), and add direction handling: set `<html dir="rtl">` when `request.locale.iso_code` is RTL (e.g. `ar`, `he`, `fa`, `ur`), otherwise `dir="ltr"`. File: `layout/theme.liquid`. (RTL full verification deferred until Arabic enabled; this is additive/readiness only.)

**Checkpoint**: Font wiring and document direction are in place; no existing sections modified. Theme still passes static checks.

---

## Phase 3: User Story 1 - Merchant can add, configure, and preview the homepage hero section (Priority: P1) — MVP

**Goal**: Deliver a new, reusable, merchant-editable hero section (`sections/hero.liquid`) with blocks (heading/text/buttons), locale-keyed bilingual copy (EN+AR), color scheme, image with dedicated alt fallback, text-only fallback when no image, `<h2>` semantic heading, and responsive styles with CSS logical properties. Section ships **unplaced** (no change to `templates/index.json`).

**Independent Test**: Verify via quickstart.md Scenarios 3–12 on the unpublished development theme: added from editor with preset blocks; single `<h2>` and header keeps `<h1>` (Scenario 4); image present (Scenario 5); no-image text-only fallback (Scenario 6); keyboard/focus (Scenario 8); responsive (Scenario 9); LTR/RTL via `dir` override (Scenario 10); CTA destinations resolve (Scenario 11); no new runtime deps (Scenario 12). Also Scenarios 1–2 (theme check, templates/index.json unchanged).

### Implementation for User Story 1

- [x] T007 [P] [US1] Create `sections/hero.liquid` implementing the section schema and rendering per contract. Must satisfy: blocks heading(text)/text(inline_richtext)/buttons with limits; settings image(image_picker), image_alt(text), image_height(select), image_overlay_opacity(range 0–100 default 40), color_scheme, desktop_content_position, desktop_content_alignment, mobile_content_alignment, heading_size; presets with those three blocks; render `<h2>` with visual size class (semantic level decoupled from size); alt resolution order `image_alt → image.alt → ''`; no media wrapper when image blank (text-only fallback); CTAs render only if both label and link non-blank; use Dawn button classes; no hardcoded prose (all strings from `t:` keys). File: `sections/hero.liquid`. (Constraints: FR-014 requires `<h2>`, FR-007 text-only fallback, FR-006 alt editable, FR-018 no hardcoded store URLs except schema defaults `/collections/all` and `/pages/tatreez`.)
- [x] T008 [P] [US1] Create `assets/component-hero.css` with styles for `.hero-section` using CSS logical properties (`inset-inline-*`, `padding-inline`, `margin-inline`, `text-align` logical where applicable). Include color-scheme token usage, overlay handling, responsive breakpoints mirroring Dawn spacing, and focus-visible styles for CTAs. Do not duplicate `section-image-banner.css`; keep file small and self-contained. File: `assets/component-hero.css`.
- [x] T009 [P] [US1] Extend `locales/en.default.json` to add `sections.hero.*` storefront keys (name, presets.name, settings labels, blocks names/labels/defaults) exactly matching the contract’s key tree; use the bilingual English defaults from spec. File: `locales/en.default.json`.
- [x] T010 [P] [US1] Extend `locales/en.default.schema.json` to add `sections.hero.*` schema keys (labels and setting defaults) so theme editor shows locale-appropriate defaults; mirror the same key names/shape. File: `locales/en.default.schema.json`.
- [x] T011 [P] [US1] Create `locales/ar.json` with `sections.hero.*` storefront keys containing Arabic defaults (headline/supporting text/CTAs) as specified. File: `locales/ar.json`.
- [x] T012 [P] [US1] Create `locales/ar.schema.json` with `sections.hero.*` schema keys containing Arabic labels/defaults. File: `locales/ar.schema.json`.
- [x] T013 [US1] Wire styles into the hero section: in `sections/hero.liquid` load `{{ 'component-hero.css' | asset_url | stylesheet_tag }}` and apply the `color-{{ section.settings.color_scheme }}` class and responsive `image_tag` with `widths`/`sizes` and `fetchpriority="high"` when appropriate. File: `sections/hero.liquid`. (Depends on T007, T008.)
- [x] T014 [US1] Verify the section is unplaced: confirm `templates/index.json` remains byte-identical to pre-feature state (git diff shows no changes). File: `templates/index.json` (verification only).
- [ ] T015 [US1] Manual end-to-end verification per quickstart.md Scenarios 3–12 against the dev theme (`shopify theme dev` at `http://127.0.0.1:9292`, dev theme `142644281431`). Record any deviations (especially RTL: use `dir="rtl"` override until Arabic enabled) in `specs/001-homepage-hero/verification.md` (create if needed). (no commit required).

**Checkpoint**: Hero section is implemented, bilingual locale keys present, styles loaded, section unplaced, and manual verification completed. All US1 acceptance scenarios satisfied per quickstart.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Regression checks, documentation consistency, and handoff verification.

- [x] T016 [P] Run `shopify theme check` and confirm the baseline floor is preserved: ≤ 156 files, ≤ 9 warnings / 8 files, with **no new offences/warnings** attributable to hero/assets/locales/ar*. Compare against T001 baseline. (Verification only.)
- [x] T017 [P] Re-verify `templates/index.json` is unchanged (git status/diff) and ensure no unintended edits to existing sections (`image-banner.liquid`, header, etc.). (Verification only.)
- [x] T018 Document verification evidence (theme-check output, quickstart pass/fail, RTL caveat) in `specs/001-homepage-hero/verification.md`; confirm license caveat is present in `docs/fonts/README.md` (T005). (Verification only.)
- [x] T019 Final sanity check against constitution gates (I–VIII): no publish/live-theme changes, fonts only verified families, logical properties used, locale files added but Arabic not published, section unplaced. (Verification only.)

**Checkpoint**: No regressions; all gates satisfied; feature ready for review/approval before any implementation execution beyond planning/artifacts (this is the task list). No publish occurred.

---

## Dependencies & Execution Order

### Phase Dependencies
- **Phase 1 (Setup)**: No dependencies — can start immediately.
- **Phase 2 (Foundational)**: Depends on Phase 1 completion — blocks Phase 3. The four foundational tasks are independent of each other ([P] marked) and can run in parallel once Setup is done.
- **Phase 3 (US1)**: Depends on Phase 2 completion. T007–T012 are independent file creations ([P]); T013 depends on T007,T008; T014–T015 depend on prior US1 tasks as appropriate.
- **Phase 4 (Polish)**: Depends on Phase 3 completion. Tasks are verification-only and can run in parallel.

### Within User Story 1
- Create section + CSS + locale files first ([P]). Wire styles into section (T013). Verify unplaced state (T014). Manual verification (T015).

### Parallel Opportunities
- T003,T004,T005,T006 (Foundational) can run in parallel after T001–T002.
- T007,T008,T009,T010,T011,T012 (US1 file creation) can run in parallel after Foundational.
- T016,T017,T018,T019 (Polish verification) can run in parallel after US1 complete.

---

## Implementation Notes

- **No automated tests**: Dawn has no test framework; rely on `shopify theme check` + quickstart scenarios.
- **RTL caveat**: `dir` attribute added to `layout/theme.liquid` (T006); full storefront RTL verification is deferred until the Arabic store language is enabled. Use dev tools `dir="rtl"` override for Scenario 10.
- **Locale duplication**: hero copy keys appear in both `*.schema.json` (editor) and `*.json` (storefront) namespaces — intentional (R2 in research.md). Keep key shapes identical across all four locale files.
- **Alt text**: dedicated `image_alt` setting; fallback order `image_alt → image.alt → ''` (T007). Do not hardcode alt from heading.
- **Heading**: exactly one `<h2>` per hero; header keeps `<h1>` on homepage (T007, contract §3).
- **No-image fallback**: omit media wrapper entirely when no image configured (T007, FR-007).
- **No publish**: never run `theme push --live` or `theme publish`. All work against unpublished development theme.
- **License**: Thmanyah fonts are not to be published/web-embedded beyond dev theme testing per existing caveat; T005 records it.