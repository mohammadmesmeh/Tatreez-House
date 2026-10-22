# Owner guide

How to run Tatreez House day to day, without touching code. Everything here happens in the
Shopify admin. This is the start of the handoff guide; more sections will follow.

## Workshops and community circles

Each workshop or circle is a **product**. Each date is a **variant** of that product, and the
number of seats is its **inventory**. The Workshops page, the homepage and the product pages update
by themselves: past dates disappear, full dates show "Fully booked".

### Add a date

1. Go to **Products** and open the workshop or circle.
2. Under **Variants**, add a value to the **Date** option. Type it exactly like this:
   `2027-02-06 18:00` (year-month-day, a space, then the 24-hour time in Palestine time).
3. Set the **inventory** of the new date to the number of seats, for example `10`.
4. Click **Save**. The date appears on the Workshops page right away.

If a date is typed in another format, the page shows it as plain text and the booking still works,
but it can't be sorted or hidden when it's past, so it stays bookable until you close it (set
its inventory to 0). Fix the format, or fill **Event start** (below), to make it behave normally.

**Translating the store is safe.** Translate & Adapt may rename the "Date" option or change its
digits; the Workshops page keeps working because the theme finds the date by position (Theme
settings → Events). For full safety, also fill the variant field **Event start** for each date
(set up once as described in `docs/store-setup/EVENTS-SETUP.md`, "Translation-safe dates"); the
theme then reads the date from there.

Avoid the weeks when Palestine changes the clocks (late March and late October): the calendar file
can be one hour off then. The Google Calendar link is always right.

### Close a date

- **Stop bookings but keep the date visible:** set its inventory to `0`. It shows "Fully booked".
- **Remove it completely:** delete the variant.
- **Past dates** hide by themselves; you don't need to do anything.

### Create a new workshop

1. Open an existing workshop and choose **More actions → Duplicate**.
2. Change the title, description, price and images.
3. At the bottom of the product page, fill the event details: **Event level**, **Event duration**,
   **Event format**, **What's included** and **What to bring** (one item per line).
4. Replace the dates (see "Add a date") and set the seats.
5. Check that **Theme template** is `workshop` and that the product type is `Workshop` (or
   `Community Circle` for a free circle), so it appears on the Workshops page.
6. Make sure **Online Store** is ticked under **Sales channels**.

### See who booked

1. Go to **Orders**.
2. Search for the workshop name, or filter by product.
3. Each order shows the attendee's name and email and the date they chose. Free circle bookings
   are orders too, with a total of $0.

### Send the Zoom link

Shopify doesn't send Zoom links automatically. For each session:

1. Create the Zoom meeting.
2. In **Orders**, open each booking for that date and email the attendee from the **Customer**
   card (click their email address), or write to everyone at once from your own email, using
   the addresses on the orders (put them in Bcc).
3. Optional: add the link as an **order note** so you can see who has received it.

Send the link the day before and again an hour before the start.

### Cancellations and refunds

Open the order, choose **Refund**, and put the seat back in stock if you want to resell it
(tick **Restock**).
