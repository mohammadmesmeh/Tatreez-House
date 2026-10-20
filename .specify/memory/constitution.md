<!--
Sync Impact Report
==================
Version change: 1.0.0 -> 2.0.0 (MAJOR: phase-gate model redefined, principle VII replaced)
Date: 2026-10-20 (milestone M0, branch 002-foundation)

Modified principles:
  - III. Font Verification Before Use -> III. Licensed, Verified Fonts
        (records the decided system: Nunito / Zain / Amiri / Playwrite NZ Basic accent;
         adds "licence must permit web embedding"; removes the provisional-font TODO)
  - VII. Incremental Milestone Workflow -> VII. Milestone Loop (plan -> implement -> verify)
        (per-phase owner-approval gates replaced by one loop per milestone; full spec-kit
         flow only for complex features)
  - VIII. Git & Store Safety: scoped commits on feature branches are allowed; push, publish
        and store-affecting actions still need explicit approval.

Unchanged: I, II, IV, V, VI (all store-safety and honesty rules kept verbatim in substance).

Sections changed:
  - "Development Phases, Quality Gates & Testing" -> "Milestone Loop, Quality Gates & Testing"
  - Governance: amendment procedure no longer requires a separate approval phase for
    milestone-level work; constitution amendments still need owner approval.

Templates requiring updates:
  - .specify/templates/plan-template.md      ⚠ pending: "Constitution Check" gate names
  - .specify/templates/tasks-template.md     ⚠ pending: phase-gate wording
  - specs/001-homepage-hero/*                 ✅ historical; left as written (v1.0.0 era)

Deferred TODOs: none (TODO(FONT_SELECTION) resolved; ratification date 2026-10-17 kept).
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

### III. Licensed, Verified Fonts

No font family may be embedded or referenced until its identity and licence are verified, and the
licence MUST permit self-hosted web embedding.

- Before configuring `@font-face`, inspect the actual files and verify family names, weights,
  formats and licence terms (fontTools). Record sources, versions and hashes in
  `docs/fonts/README.md` and keep the licence texts in `docs/fonts/licenses/`.
- The decided system (2026-10-20): Nunito for Latin body, UI and headings; Zain for Arabic body
  and UI; Amiri for Arabic headings; Playwrite NZ Basic as an opt-in decorative accent only
  (`.font-accent`), never the default heading face. All SIL OFL 1.1.
- Only the weights required by the design MAY be loaded; WOFF2, subset by script, scoped with
  `unicode-range`; one preload per locale.
- Every font stack MUST define language-appropriate system fallbacks, Latin face first.
- Arabic shaping, punctuation, mixed Arabic/English text and RTL rendering MUST be checked
  visually before a font change ships.

Rationale: a font whose licence forbids web embedding was found in the theme and withdrawn in M0;
licensing is a legal risk, not a styling detail.

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

### VII. Milestone Loop (plan -> implement -> verify)

Work proceeds in small, reviewable milestones (M0, M1, …; see docs/PROJECT_BRIEF.md roadmap).

- Each milestone runs one loop: **plan** (scope, acceptance criteria, verification steps) ->
  **implement** -> **verify** (record evidence per principle VI) -> owner review of the result.
- The full spec-kit flow (specify, clarify, plan, tasks, implement, verify) is REQUIRED only for
  complex features with new data models or flows: the pattern library (metaobjects) and events.
  Other milestones use the light loop.
- Scope creep beyond the current milestone MUST be deferred to a later milestone and noted.
- Explicit STOP points named in a milestone request MUST be honoured; everything else proceeds
  without per-step approval.

Rationale: per-phase approval gates slowed small changes without adding safety; the safety rules
live in VI and VIII, which are unchanged.

### VIII. Git & Store Safety

Existing work and the live store MUST be protected at all times.

- Existing project instructions and AGENTS.md MUST NOT be overwritten without prior inspection.
- Existing files and uncommitted changes MUST be preserved; diffs MUST be reviewed before
  modifying or committing files.
- Small, scoped commits (Conventional Commits, one concern each) on feature branches are allowed
  during a milestone. Pushing, merging to `main` and rewriting history require owner approval.
- Credentials, secrets, and store tokens MUST NEVER be committed to Git.
- Development and testing MUST use the unpublished development theme; the live Horizon theme
  MUST NOT be modified or published.
- Publishing a theme, deleting store data, changing sensitive store settings, installing paid
  apps, or purchasing services REQUIRES explicit owner approval.
- No push, publish, or deploy action occurs without explicit request.

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

## Milestone Loop, Quality Gates & Testing

- Loop per milestone: plan -> implement -> verify -> owner review. Full spec-kit flow only for
  the pattern library and events (principle VII).
- Quality gate before "done": `shopify theme check` with 0 errors and no new warnings, responsive
  check (360/390/768/1024/1440), keyboard/focus check, contrast check
  (`node scripts/contrast-check.mjs`), RTL/LTR check, and all strings localized in EN and AR.
- Testing gate: acceptance criteria and verification steps MUST exist per milestone, and evidence
  MUST be recorded. Untested behavior MUST be labeled UNTESTED.
- Review gate: diffs reviewed before every commit; store-affecting actions require explicit
  approval.

## Governance

- This constitution supersedes conflicting practices, instructions, or habits. When guidance
  elsewhere conflicts, this document wins and the conflicting guidance MUST be updated.
- Amendment procedure: propose the change -> record rationale -> obtain owner approval -> update
  this file with a Sync Impact Report -> commit with a `docs:` message describing the amendment.
  (v2.0.0 was requested by the owner in the M0 brief, 2026-10-20.)
- Versioning policy: semantic versioning of governance. MAJOR for backward-incompatible removals
  or redefinitions of principles, MINOR for added or materially expanded principles/sections,
  PATCH for clarifications, wording, and typo fixes.
- Compliance review: every specification, plan, task list, and review MUST verify compliance with
  these principles; any deviation MUST be explicitly justified and approved, and unjustified
  complexity or deviation MUST be rejected.
- Unresolved business or design decisions MUST be recorded as open items (see
  docs/PROJECT_BRIEF.md "Open Decisions") rather than silently invented.
- Runtime development guidance: AGENTS.md (Dawn theme conventions) and docs/PROJECT_BRIEF.md.

**Version**: 2.0.0 | **Ratified**: 2026-10-17 | **Last Amended**: 2026-10-20
