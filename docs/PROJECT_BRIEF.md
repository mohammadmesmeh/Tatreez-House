# Tatreez House — Project Brief

## 1. Project Overview

**Project name:** Tatreez House | دار التطريز

**Project type:** Shopify Online Store 2.0 portfolio and learning project.

**Brand concept:** Palestinian heritage woven into contemporary everyday life.

Tatreez House is a fictional Palestinian fashion and cultural brand that celebrates Palestinian embroidery through contemporary clothing, accessories, home textiles, downloadable embroidery patterns, educational content, and workshops.

This is a learning and portfolio project, not a real client engagement. Do not invent business credentials, sales figures, customer testimonials, or production results.

## 2. Project Goals

- Build a professional, responsive Shopify storefront.
- Demonstrate practical Shopify Liquid and Online Store 2.0 skills.
- Use reusable sections, snippets, JSON templates, and merchant-editable settings.
- Support Arabic and English with appropriate RTL and LTR layouts.
- Use Shopify's native products, collections, localization, cart, and theme architecture.
- Provide a clear shopping experience for physical and digital products.
- Present tatreez educational content and workshop information.
- Maintain a clean Git history and publish a professional portfolio case study.

## 3. Target Audiences

### Shoppers
People interested in embroidered clothing, accessories, home textiles, gifts, and Palestinian-inspired design.

### Embroidery learners
People interested in learning about tatreez, its cultural context, motifs, techniques, and downloadable patterns.

### Workshop visitors
People interested in discovering embroidery workshops, event details, and booking options when a suitable booking solution is configured.

## 4. Brand Positioning and Voice

**Core idea:** Every stitch carries a story.

**English headline:** Wear the Story. Keep the Heritage.

**Arabic headline:** ارتدِ الحكاية، واحفظ التراث.

**English supporting copy:** Discover contemporary pieces inspired by Palestinian tatreez.

**Arabic supporting copy:** اكتشف قطعًا معاصرة تستلهم فن التطريز الفلسطيني.

**Primary CTA:** Explore the Collection / اكتشف المجموعة

**Secondary CTA:** Discover Tatreez / اكتشف فن التطريز

Brand attributes:
- Authentic and respectful
- Contemporary and timeless
- Warm and human
- Editorial and refined
- Educational and welcoming

Avoid generic cultural stereotypes, excessive ornamentation, and unsupported historical claims. Cultural storytelling must be respectful and fact-checked.

## 5. Visual Identity

### Color palette

- Warm Ivory: #F7F3EB
- Tatreez Black: #292820
- Embroidery Red: #8E3038
- Olive Green: #667052
- Linen Beige: #D9C8AD
- White: #FFFFFF

Suggested distribution: 60% ivory/white, 25% dark, 10% embroidery red, 5% olive/beige.

Use the palette consistently and verify text contrast for accessibility.

### Typography

The proposed typography system uses separate display and body fonts for Arabic and English.

**English**
- Display / accent: Playwrite New Zealand Basic
- Body / UI: Nunito

**Arabic**
- Display: Thuluth / Thamanya (ثمانية); use the exact local font family and filename after inspecting the project assets.
- Body / UI: Zain, pending confirmation of the exact font family and available files.

**Implementation requirements**
- Inspect local font files before configuring `@font-face`.
- Verify exact family names, available weights, formats, and licenses.
- Prefer WOFF2 when available and permitted.
- Load only the font weights required by the design.
- Define sensible system fallbacks.
- Use the display fonts selectively; prioritize readability in product information, navigation, buttons, and long-form content.
- Test Arabic shaping, punctuation, mixed Arabic/English text, and RTL layouts.
- Do not download or overwrite font files without reviewing the existing assets and licensing.

**Provisional CSS font stacks**
- English body: `Nunito, sans-serif`
- English display: `Playwrite New Zealand Basic, cursive`
- Arabic body: `Zain, sans-serif`
- Arabic display: the verified local Thuluth / Thamanya family, with a suitable Arabic fallback.

These stacks are provisional until the font files and browser rendering are verified.

Font choices are pending owner approval.

- Arabic display font: proposed Thuluth/Thamanya-style reference, exact font name and file to be confirmed by the owner.
- Arabic body font: proposed Zain, exact family and weights to be confirmed.
- English display font: pending owner selection.
- English body/UI font: pending owner selection.

Do not download, embed, or commit font files until their exact identities, licenses, and permitted web usage are verified.

Prefer optimized WOFF2 files where licensing permits. Define robust language-specific fallbacks. Avoid loading unnecessary font weights.

### Photography and motifs

Use natural textile textures, close-up embroidery details, thoughtful product photography, and warm neutral backgrounds.

Tatreez-inspired geometric motifs may appear as restrained decorative accents. They must not compromise readability, accessibility, or page performance.

Do not use decorative imagery as a substitute for meaningful product photography.

## 6. Localization and Direction

The storefront must support Arabic and English through Shopify's localization and locale architecture.

- Arabic pages use RTL where appropriate.
- English pages use LTR.
- Use Shopify's translation mechanisms rather than hardcoding language-dependent UI strings.
- Use CSS logical properties such as `margin-inline`, `padding-inline`, and `text-align: start`.
- Provide a functional language selector when the required Shopify localization configuration is available.
- Ensure navigation, product layouts, icons, forms, and cart interactions work in both directions.
- Do not mirror brand marks or product photography unnecessarily.
- Test both languages on mobile and desktop.

## 7. Required Pages and Content

1. Home
2. Shop and collection listings
3. Product detail pages
4. Digital embroidery patterns
5. Events and workshops
6. Learn and blog
7. About
8. Contact
9. Cart

### Suggested collections

- Embroidered Clothing
- Accessories
- Home & Textiles
- Digital Patterns
- Gifts & Heritage

### Suggested educational articles

- Introduction to Palestinian Tatreez
- Understanding Geometric Motifs
- Cross-Stitch Basics
- Caring for Embroidered Textiles

All sample product, collection, and article content must be clearly understood as fictional demonstration content where applicable.

## 8. Homepage Experience

Recommended section order:

1. Announcement bar, only when useful
2. Accessible header and primary navigation
3. Hero with brand headline and two clear calls to action
4. Featured collections
5. Featured products using Shopify product data
6. Brand story and cultural context
7. Digital embroidery patterns
8. Educational articles
9. Workshops and events
10. Newsletter signup, only when configured and functional
11. Footer with navigation, localization, and relevant store information

The homepage should feel editorial and spacious rather than crowded. The mobile layout must be designed deliberately, not merely compressed from desktop.

## 9. Shopify Technical Architecture

- Shopify Online Store 2.0
- Shopify Liquid
- Semantic HTML
- Maintainable CSS and JavaScript
- JSON templates
- Reusable sections and snippets
- Merchant-editable section schemas and settings
- Shopify native products, collections, cart, and localization
- Shopify CLI for local development
- Git and GitHub for version control

Do not hardcode store data that should come from Shopify objects or merchant settings.

Follow existing theme conventions where practical. Inspect the existing theme structure before introducing or replacing files.

## 10. Digital Products and Workshops

Digital embroidery patterns may require a compatible digital-download app or an explicitly documented prototype.

Workshop listings and booking flows may require a compatible booking app or a documented prototype.

Do not present a nonfunctional download or booking button as complete. Explain any subscription, app, or payment costs before recommending paid services.

## 11. Accessibility, Performance, and Quality

- Semantic HTML and accessible labels
- Keyboard-accessible navigation and interactions
- Visible focus indicators
- Sufficient color contrast
- Appropriate alternative text
- Responsive layouts
- Optimized images and font loading
- Minimal unnecessary JavaScript
- Clear empty, error, and success states
- No broken links or misleading placeholder functionality

## 12. Development and Safety Rules

- Keep the published Horizon theme unchanged.
- Develop and test using the unpublished development theme.
- Never publish a theme without explicit owner approval.
- Do not delete store data, change sensitive store settings, purchase services, or install paid apps without explicit approval.
- Protect existing files and uncommitted changes.
- Inspect diffs before committing.
- Never claim a feature works until it has been tested.

## 13. Portfolio Deliverables

- Working development-store preview where available
- GitHub repository
- Project README
- Desktop and mobile screenshots
- Technical documentation
- Portfolio case study
- Accurate CV description of implemented and tested features

## 14. First Implementation Milestone

Build the custom homepage hero section.

The hero should have:
- Merchant-editable heading and supporting text
- Primary and secondary CTA labels and links
- Configurable background or image where appropriate
- Responsive layout
- Accessible contrast and focus behavior
- Arabic and English support
- RTL/LTR compatibility
- Sensible fallback behavior when optional content is empty

Use the project's approved fonts after they are selected. Do not rebuild the entire homepage in the first milestone.

## 15. Open Decisions

- Final Arabic display and body fonts
- Final English display and body fonts
- Final logo and brand mark
- Approved photography assets
- Final bilingual product and article copy
- Digital download solution
- Workshop booking solution
- Newsletter provider, if needed

Record decisions when approved. Do not silently invent answers to unresolved business or design questions.