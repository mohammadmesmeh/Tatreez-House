<!--
Sync Impact Report
==================
Version change: (unratified scaffold) -> 1.0.0
Rationale: Initial adoption. The scaffold contained only template placeholders; no prior
governance values existed to preserve, so this is the project's first ratified constitution.

Modified principles:
  - [PRINCIPLE_1_NAME] -> I. Shopify-Native Architecture (NON-NEGOTIABLE)
  - [PRINCIPLE_2_NAME] -> II. Cultural Heritage & Brand Fidelity
  - [PRINCIPLE_3_NAME] -> III. Font Verification Before Use
  - [PRINCIPLE_4_NAME] -> IV. Bilingual Localization & Direction
  - [PRINCIPLE_5_NAME] -> V. Accessibility, Responsiveness & Quality
  - (added)             -> VI. Evidence-Based Verification
  - (added)             -> VII. Incremental Milestone Workflow
  - (added)             -> VIII. Git & Store Safety

Added sections:
  - Additional Constraints (was [SECTION_2_NAME])
  - Development Phases, Quality Gates & Testing (was [SECTION_3_NAME])

Removed sections: none

Deferred TODOs:
  - TODO(RATIFICATION_DATE): set to 2026-10-17 assuming adoption on the date of authoring;
    owner must confirm the actual adoption date.
  - TODO(FONT_SELECTION): Arabic display/body and English display/body fonts are provisional;
    see docs/PROJECT_BRIEF.md "Open Decisions". Not a blocker to this constitution.

Follow-up: remove this report before committing the amended constitution.
-->

# Tatreez House | دار التطريز Constitution

## Core Principles

### I. Shopify-Native Architecture (NON-NEGOTIABLE)

The storefront MUST be built on Shopify Online Store 2.0 using Liquid, semantic HTML,
maintainable CSS/JavaScript, JSON templates, sections, and snippets.

- Products, collections, cart, search, and localization MUST come from Shopify-native objects
  and APIs, not hardcoded store data.
- Anything a merchant would reasonably need to change MUST be exposed through section settings
  and schemas (merchant-editable), not baked into markup.
- Existing section setting IDs, schema handles, and merchant configuration MUST be preserved
  unless a documented, approved migration plan exists.
- Shared markup MUST be extracted into reusable snippets rather than duplicated across sections.
- Changes MUST remain compatible with the Shopify theme editor and the Dawn theme conventions
  recorded in AGENTS.md.

Rationale: The project is a portfolio-grade demonstration of professional OS 2.0 skills;
theme-native, merchant-editable, reusable code is the whole point.

### II. Cultural Heritage & Brand Fidelity

The storefront MUST respect Palestinian cultural heritage and follow the approved brand identity
in docs/PROJECT_BRIEF.md.

- The approved palette is fixed for brand surfaces: Warm Ivory `#F7F3EB`, Tatreez Black
  `#292820`, Embroidery Red `#8E3038`, Olive Green `#667052`, Linen Beige `#D9C8AD`,
  White `#FFFFFF`. Deviations require explicit owner approval.
- Cultural storytelling MUST be respectful, factual, and free of generic stereotypes, excessive
  ornamentation, or unsupported historical claims.
- Tatreez House is fictional: business credentials, sales figures, testimonials, and production
  results MUST NOT be invented. Sample product, collection, and article content MUST be clearly
  identifiable as fictional demonstration content.
- Decorative motifs MUST NOT replace meaningful product photography, nor compromise
  readability, accessibility, or performance.

Rationale: Brand integrity and cultural respect are non-negotiable constraints, not styling
preferences.

### III. Font Verification Before Use

No font family may be embedded or referenced until its identity and licensing are verified.

- Before configuring `@font-face`, inspect the actual font files and verify exact family names,
  available weights, formats, and license terms.
- Font files MUST NOT be downloaded, overwritten, embedded, or committed until their exact
  identities and permitted web usage are verified.
- Only the weights required by the design MAY be loaded; prefer WOFF2 where licensing permits.
- Every font stack MUST define sensible, language-appropriate system fallbacks.
- Display/accent fonts MUST be used selectively; product information, navigation, buttons, and
  long-form content MUST prioritize readability.
- Arabic shaping, punctuation, mixed Arabic/English text, and RTL rendering MUST be tested before
  a font is declared final.

Rationale: Font choices are provisional (see docs/PROJECT_BRIEF.md "Open Decisions"); using
unverified or unlicensed fonts is both a legal and a quality risk.

### IV. Bilingual Localization & Direction

Arabic (RTL) and English (LTR) MUST both be supported through Shopify's localization
architecture.

- User-facing strings MUST use Shopify translation mechanisms and locale files, not hardcoded
  language-dependent text.
- Layout MUST use CSS logical properties (`margin-inline`, `padding-inline`, `text-align: start`,
  etc.) so direction flips without duplicated RTL stylesheets.
- Navigation, product layouts, icons, forms, and cart interactions MUST be verified in both
  directions; brand marks and product photography MUST NOT be mirrored unnecessarily.
- A language selector MUST be provided only when the required Shopify localization configuration
  exists and is functional.
- Both locales MUST be tested on mobile and desktop.

Rationale: A bilingual heritage brand requires genuine localization, not a bolted-on Arabic page.

### V. Accessibility, Responsiveness & Quality

Every deliverable MUST be responsive, accessible, and maintainable.

- Semantic HTML, accessible labels, appropriate alternative text, and correct landmark/heading
  structure are REQUIRED.
- Interactive elements MUST be keyboard-accessible with visible focus indicators.
- Text and meaningful UI MUST meet sufficient color contrast against the approved palette.
- Mobile layouts MUST be designed deliberately, not merely compressed from desktop.
- Images and fonts MUST be optimized; unnecessary JavaScript MUST be avoided.
- Empty, error, loading, and success states MUST be defined and clear.
- Broken links and misleading placeholder functionality MUST NOT ship.

Rationale: Quality, accessibility, and performance are correctness requirements for a
portfolio-grade storefront.

### VI. Evidence-Based Verification

No feature may be claimed complete, working, or finished without recorded testing.

- Every feature MUST ship with explicit acceptance criteria and concrete verification steps.
- Verification evidence (what was run, on what device/locale, and the observed result) MUST be
  captured before a feature is called done.
- Non-functional behavior (e.g. an unconfigured download, booking, or newsletter action) MUST be
  labeled as a prototype or clearly unavailable, never presented as complete.
- Subscription, app, or payment costs of any proposed third-party solution MUST be disclosed
  before recommending it.

Rationale: The portfolio's credibility depends on accurate claims backed by tested behavior.

### VII. Incremental Milestone Workflow

Work MUST proceed in small, reviewable milestones across distinct phases.

- The phases are: constitution, specification, clarification, planning, tasks, implementation,
  and testing. Each phase MUST be completed and reviewed before the next begins.
- Feature implementation MUST NOT occur during the Constitution phase.
- The first implementation milestone is the custom homepage hero section as defined in
  docs/PROJECT_BRIEF.md; scope creep beyond the current milestone MUST be deferred.
- Owner review and approval are REQUIRED at each phase gate before proceeding.

Rationale: Small, gated milestones keep changes reviewable and protect uncommitted work.

### VIII. Git & Store Safety

Existing work and the live store MUST be protected at all times.

- Existing project instructions and AGENTS.md MUST NOT be overwritten without prior inspection.
- Existing files and uncommitted changes MUST be preserved; diffs MUST be reviewed before
  modifying or committing files.
- Credentials, secrets, and store tokens MUST NEVER be committed to Git.
- Development and testing MUST use the unpublished development theme; the live Horizon theme
  MUST NOT be modified or published.
- Publishing a theme, deleting store data, changing sensitive store settings, installing paid
  apps, or purchasing services REQUIRES explicit owner approval.
- No commit, publish, or deploy action occurs without explicit request.

Rationale: Irreversible store and Git actions are the highest-risk operations in this project.

## Additional Constraints

- Technology: Shopify OS 2.0, Liquid, JSON templates, the Shopify CLI for local development, and
  Git/GitHub for version control. Introducing non-native frameworks or paid dependencies requires
  approved justification.
- Theme baseline: Dawn, per AGENTS.md. Prefer extending existing sections/snippets over
  introducing parallel implementations.
- Content has two classes: (a) Shopify object data (products, collections, articles, pages) and
  (b) merchant-editable settings. Neither MAY be replaced by hardcoded literals.
- Localization targets: English (`en.default`) and Arabic. New locale files MUST follow Shopify's
  locale-file structure.
- Digital products and workshop booking MAY require compatible apps or explicitly documented
  prototypes; they MUST NOT be represented as functional until verified.

## Development Phases, Quality Gates & Testing

- Phase gates: constitution -> specification -> clarification -> planning -> tasks ->
  implementation -> testing. Each gate closes only on owner approval.
- Quality gate before "done": responsive check, keyboard/accessibility check, contrast check,
  RTL/LTR check, and confirmation that all strings are localized.
- Testing gate: acceptance criteria and verification steps MUST exist per feature, and evidence
  MUST be recorded. Untested behavior MUST be described as untested.
- Review gate: diffs reviewed before any commit; store-affecting actions require explicit
  approval.

## Governance

- This constitution supersedes conflicting practices, instructions, or habits. When guidance
  elsewhere conflicts, this document wins and the conflicting guidance MUST be updated.
- Amendment procedure: propose the change -> record rationale -> obtain owner approval -> update
  this file with a Sync Impact Report -> commit with a `docs:` message describing the amendment.
- Versioning policy: semantic versioning of governance. MAJOR for backward-incompatible removals
  or redefinitions of principles, MINOR for added or materially expanded principles/sections,
  PATCH for clarifications, wording, and typo fixes.
- Compliance review: every specification, plan, task list, and review MUST verify compliance with
  these principles; any deviation MUST be explicitly justified and approved, and unjustified
  complexity or deviation MUST be rejected.
- Unresolved business or design decisions MUST be recorded as open items (see
  docs/PROJECT_BRIEF.md "Open Decisions") rather than silently invented.
- Runtime development guidance: AGENTS.md (Dawn theme conventions) and docs/PROJECT_BRIEF.md.

**Version**: 1.0.0 | **Ratified**: 2026-10-17 | **Last Amended**: 2026-10-17
