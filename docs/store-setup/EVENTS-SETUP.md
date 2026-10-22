# Events setup (M4): workshops and monthly circles

Workshops and circles are ordinary Shopify products:
- each **date** is a variant (option name `Date`, value `YYYY-MM-DD HH:MM`, Palestine time);
- **seats** are inventory;
- they **don't require shipping**.

This keeps booking native: no paid booking app, and the owner adds a date in under a minute.

## 1. Metafield definitions (do these BEFORE importing)

Go to **Settings → Metafields and metaobjects → Products → Add definition**. Create these five:

| Name | Namespace and key | Type |
|---|---|---|
| Event level | `custom.event_level` | Single line text |
| Event duration | `custom.event_duration` | Single line text |
| Event format | `custom.event_format` | Single line text |
| What's included | `custom.event_includes` | Multi-line text |
| What to bring | `custom.event_bring` | Multi-line text |

The namespace and key must match exactly.

## 2. Import

1. Go to **Products → Import** and upload `workshops.csv`.
2. Expect **3 products and 8 variants**:
   - Tatreez Foundations (3 dates · $45 · 10 seats)
   - Beyond the Basics (2 dates · $65 · 8 seats)
   - Monthly Stitch Circle (3 dates · free · 20 seats)
3. Open one product and check that the five metafields are filled (shown at the bottom of the product page).
4. If they're empty, the definitions didn't exist at import time. Fill them by hand, or re-import with **Overwrite existing products**.

## 3. Collection

Go to **Products → Collections → Create collection** and fill:
- **Title:** `Events`
- **Handle:** `events`
- **Type:** Smart
- **Conditions:** products must match **any** condition:
  - Product type is equal to `Workshop`
  - Product type is equal to `Community Circle`
- **Description:** "Hands-on tatreez workshops and free monthly stitch circles."

## 4. After the theme update

1. Open **Online Store → Pages → Workshops** and set **Theme template** to `events`.
2. For each workshop/circle product, set **Theme template** to `workshop`.
3. Test a booking:
   - Book a paid seat with test card `1`.
   - Join a circle: a $0 checkout needs no card.
   - Check that the inventory (seats) drops by 1.

## Owner guide (for the handoff doc)

- **Add a date:**
  1. Open the workshop.
  2. Go to **Variants → Add value** under "Date", using the format `2027-02-06 18:00`.
  3. Set the inventory to the number of seats.
- **Close a date:** set its inventory to 0, or delete the variant. Past dates hide automatically.
- **New workshop:** duplicate an existing one, then edit the title, description, metafields and dates.
