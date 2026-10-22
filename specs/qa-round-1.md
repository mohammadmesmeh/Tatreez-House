# QA round 1 — results (branch `fix/qa-round-1`)

Six issues from manual QA on the live store, fixed 2026-10-22/23. Screenshots:
[`docs/screenshots/qa-round-1/`](../docs/screenshots/qa-round-1) (`before-*` = live theme before
the fix, or the dev theme before the change; `after-*` = dev theme with the fixes).

## Issues

| # | Root cause | Fix | Regression check |
|---|---|---|---|
| 1 Card title underline | The stitch was a background on the title link, which Dawn makes a full-width block; Dawn's `.underline-links-hover:hover a` added a second, black underline. | Title text in an inline span with the stitch (`box-decoration-break: clone`, direction-aware); Dawn's underline off for the title. | `cards_grids_test.py` QA1 (EN + AR): link has no text-decoration, span background 100%, cloned, narrower than the link |
| 2 Toolbar alignment | Grid items top-aligned; Dawn's 15px summary margin / -15px label offset made the filter group 59px tall; count top-aligned; fixed-width sort select; physical label margin in RTL. | Centred items, offsets removed, one gap, count after Sort, `field-sizing: content` select with the chevron at the inline end, logical label margin. | QA2 at 768 / 1024 / 1440 EN + AR: equal centres, count after Sort, chevron ≤ 16px after the text |
| 3 Merchant text direction on /ar | English merchant content inherited `dir="rtl"`, so punctuation moved to the line start. | `dir="auto"` on merchant containers (page, article, product description/tabs, collection description, event metafield lines/lists) and inline `dir="auto"` spans on titles (product, article, card, session, menu links). | QA3: card titles (cards suite), /ar events page body and session titles (events suite) |
| 4 Light logo everywhere | The rule hiding the light logo lived in the hero CSS, loaded only on the homepage. | Hiding rule in the header CSS (every page); shown only while the header is transparent over the hero; lazy off the homepage. | `hero_slideshow_test.py` QA4: home top/scrolled one logo; collection, product, workshops, cart only the dark logo; 390 / 1440 EN + AR |
| 5 Workshops empty on /ar | Translate & Adapt renamed the option "Date" to "التاريخ"; the theme found the date option by that English name. Values stayed Latin (confirmed with a temporary debug template, since removed). | Date option by position (Theme settings → Events), Arabic-Indic / Persian digits normalised, variant metafield `custom.event_start` read first, unparseable dates listed as written. Also fixed a line break inside `<time datetime>`. | `events_test.py`: /ar lists the same sessions as EN; `event_date_selftest.py` 9 cases |

## Results (dev theme 189091577949 through `shopify theme dev`)

| Suite | Result |
|---|---|
| `event_date_selftest.py` | 9 / 9 |
| `hero_slideshow_test.py` | 53 / 53 |
| `cards_grids_test.py` | 51 pass, 0 fail, 1 skip (no sold-out product) |
| `events_test.py` | 40 pass, 1 fail, 3 skip — the "fail" is seats 19 vs 20 on two circle dates: real bookings changed the inventory since `workshops.csv`; skips: empty-state template and the two checkout flows (real domain only; passed in M4) |
| `header_dropdowns_test.py` | 46 / 46 |
| `keyboard_test.py` | 12 / 12 |
| `wired_screens_test.py` | 50 / 50 |
| `shopify theme check` | 0 errors (9 warnings, all in untouched Dawn files) |
| Toolkit validator | VALID |

Lighthouse 12.8.2, accessibility, mobile, 2026-10-22 21:05–21:12 UTC, dev theme:

| Page | Score |
|---|---|
| `/` | 100 |
| `/collections/all` | 100 |
| `/products/tatreez-foundations-workshop?view=workshop` | 100 |
| `/pages/workshops?view=events` | 100 |
| `/ar/pages/workshops?view=events` | 100 |

## UNTESTED

- Issue 3 before/after on the real text: the owner has since translated the workshops page content
  to Arabic, so the reversed English sentence can no longer be shown; checked through `dir="auto"`
  attributes and the resolved direction instead.
- Translation that rewrites a date into words (e.g. "٧ نوفمبر"): covered by the "not a date" case
  (listed as written, still bookable) but not seen in store data.
- `custom.event_start` with real store data: the definition does not exist yet; covered by the
  self-test with UTC instants (winter and summer).
- Firefox / Safari: `field-sizing: content` falls back to the widest option's width there.
- Checkout flows were not re-run (Cloudflare bot check after many automated runs); unchanged code.
