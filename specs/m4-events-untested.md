# M4 (m4-events) — test results and UNTESTED items

Store `tatreez-house.myshopify.com`, 2026-10-22. Data from `docs/store-setup/workshops.csv`
(3 products, 8 dates, all upcoming). Templates previewed with `?view=events` / `?view=workshop`
before the owner assigned them.

## Results

| Check | Result |
|---|---|
| `scripts/tests/events_test.py` on the `shopify theme dev` proxy | **40 pass, 0 fail, 2 skip** (the 2 checkout flows need the real domain) |
| Same suite on the real domain (`--preview-theme 189091577949`) | 39 pass, 1 fail: the $0 checkout hit Cloudflare's bot check after many automated runs |
| Checkout flows on the real domain (separate run) | "Buy it now" reaches checkout; the free circle reaches a $0 checkout ("Your order is free. No payment is required."), not completed. Screenshots in `docs/screenshots/m4/` |
| Lighthouse accessibility (events page EN + AR, paid workshop, free circle) | 100 / 100 / 100 / 100 |
| `shopify theme check` | 0 errors |
| Shopify AI Toolkit Liquid validator | VALID |

Covered by the suite: chronological sort; no past dates; filters with JS (aria-current, URL,
live region, shared link) and without JS (everything shows); "Free" and "Reserve a free spot" for
circles; seats text equals inventory; empty state with newsletter; only upcoming chips; date
change updates `?variant=`, seats, selected date, Google Calendar link and `.ics` (UTC start
checked); "Book a seat" opens the drawer with the formatted date; no shipping wording in the
drawer and cart; cards show the next date and "From"/"Free" without "Instant download";
"Choose options" opens the quick-add modal with date chips; EN + `/ar` (Arabic date names,
"بتوقيت فلسطين") at 360 / 768 / 1440 px without horizontal scroll and with one h1; keyboard
booking (arrow keys on the date chips, Tab to "Book a seat", Enter).

## Still untested

| # | Item | Why / how to verify |
|---|---|---|
| 1 | A completed booking: order created, seats (inventory) drop by 1 | Owner's real test booking after the templates are assigned (EVENTS-SETUP.md §4) |
| 2 | Past dates and sold-out dates in a browser ("Fully booked" chip/card, disabled; all dates sold out → "Fully booked" button; no upcoming dates → "No upcoming dates" + newsletter) | All demo dates are upcoming and in stock. Set one date's inventory to 0, and add a past date, then reload the events page and the product |
| 3 | Malformed date value (raw text, editor-only console warning) | Add a variant with a value like "Nov 7" in a test product |
| 4 | Summer-time edge weeks (late March, late October) | No such dates in the demo data; rule documented in DECISIONS.md (M4 #3) |
| 5 | Newsletter post from the events empty state / product "no dates" state | Shopify's bot protection blocks automated posts; both forms show the result when two are on a page (DECISIONS M4 #10) |
| 6 | Homepage teaser with sessions on the live theme | Rendered on the dev theme; check `/` after the push |
| 7 | Checkout shows the raw option value "2026-11-19 19:00" | Shopify checkout is not theme code; formatting it would need a checkout extension (Plus) |
| 8 | Product and page content in Arabic | Store content; translate in Translate & Adapt. Theme strings are translated |
