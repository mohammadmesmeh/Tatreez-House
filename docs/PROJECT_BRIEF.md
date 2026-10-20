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

Decided 2026-10-20 (milestone M0; see `docs/DECISIONS.md`). All four families are SIL OFL 1.1,
self-hosted from `assets/`. Details, sources and subsetting: `docs/fonts/README.md`.

| Role | Family | Weights | Scope |
|---|---|---|---|
| Latin body, UI and headings | Nunito | variable (400 body, 700 bold and headings) | Latin |
| Arabic body and UI | Zain | 400, 700 | Arabic only (`unicode-range`) |
| Arabic headings | Amiri (Naskh) | 400, 700 | Arabic only (`unicode-range`) |
| Decorative accent | Playwrite NZ Basic | variable 100–400 | Latin, opt-in `.font-accent` only |

**Font stacks**
- Body: `'Nunito', 'Zain', system-ui, 'Segoe UI', Tahoma, sans-serif`
- Headings: `'Nunito', 'Amiri', 'Times New Roman', serif`
- Accent: `'Playwrite NZ Basic', 'Nunito', cursive`

The Latin face is first in every stack and scoped to Latin, so mixed Arabic/English text picks
the right face per character. The handwriting script is never the default heading face.

**Rules**
- Load only the weights the design uses; one preload (Zain on the Arabic storefront, Nunito otherwise).
- Arabic text is never letter-spaced; Arabic headings get extra line-height for Amiri's tall marks.
- Any new font needs verified identity, weights and a licence that permits web embedding before use.

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

Use the approved fonts (section 5). Do not rebuild the entire homepage in the first milestone.

## 15. Job-Aligned Requirements

The portfolio targets a Shopify Website Designer role. The finished store must show:

- **Two clear user paths** from the homepage: *Shop* (garments, accessories, home textiles) and
  *Learn* (tatreez history, motifs, techniques).
- **Digital patterns** sold as downloadable products with their own product template.
- **Events**: paid workshops and free monthly community circles, with clear dates, seats and
  registration states.
- **Pattern library**: a browsable, filterable catalogue of motifs (name, region, meaning,
  difficulty, chart, related products).
- **Blog / education**: articles linked to motifs and products.
- **Non-technical-owner handoff**: everything editable in the theme editor, plus a plain-language
  owner guide.

## 16. Milestone Roadmap

| Milestone | Scope | Status |
|---|---|---|
| M0 | Foundation: licensed font system, brand colour check, full EN/AR locales, hero on the homepage, RTL fixes for Dawn, docs | Done (2026-10-20), owner actions pending |
| M1 | Homepage "two paths" section (Shop / Learn) | Done (delivered with M2, 2026-10-20) |
| M2 | Design system and UX overhaul ("Editorial heritage"): tokens, Fraunces, header and mega menu, product cards with quick add, collection hero, homepage story sections, footer, mobile sticky add to cart | Done (2026-10-20), admin menus and images pending |
| M3 | Store: garment product template using metafields (motif story, care, size guide); `product.pattern` template for digital patterns with Shopify Digital Downloads (verify cost first) | Planned |
| M4 | Pattern library: `motif` metaobject, metaobject pages, filtering (full spec-kit flow) | Planned |
| M5 | Events: workshops as products (date = variant, seats = inventory), `product.workshop` template; monthly community circles with free registration (full spec-kit flow); Learn hub page + blog/article templates linked to motifs | Planned |
| M6 | Accessibility/performance audit, owner handoff guide, screenshots, case study | Planned |

## 17. Open Decisions

- ~~Final Arabic display and body fonts~~ — resolved 2026-10-20: Amiri (headings), Zain (body).
- ~~Final English display and body fonts~~ — resolved 2026-10-20: Nunito (body and headings),
  Playwrite NZ Basic as accent only.
- Final logo and brand mark
- Approved photography assets
- Final bilingual product and article copy
- Digital download solution (M2; Shopify Digital Downloads — cost to verify)
- Workshop booking solution (M4)
- Newsletter provider, if needed
- Colour schemes: the admin schemes use near-brand values (`#F7F2E8`, `#252722`, `#8C2633`,
  `#F0E8D9`) and a deep green `#17352B` that is not in the palette above — confirm or align.
