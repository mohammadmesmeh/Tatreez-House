/*
  event-session.js — booking behaviour for event products (rendered by snippets/buy-buttons.liquid
  as <event-booking>, so it works whichever optional blocks the template uses).
  - On a date change Dawn re-renders the section and publishes variantChange with the new HTML:
    restore the booking label that product-form.js resets to "Add to cart", and swap the session
    info (date, seats, calendar links) when the template has that block. <event-booking> sits
    before the sticky bar in the DOM, so this runs before sticky-atc copies the label.
  - Build the .ics file client-side from the start time, duration and title.
  - When the selected variant is a past date (no chip checked), select the first bookable date.
*/
if (!customElements.get('event-booking')) {
  customElements.define(
    'event-booking',
    class EventBooking extends HTMLElement {
      connectedCallback() {
        this.sectionId = this.dataset.section;
        this.onClick = (event) => {
          const button = event.target.closest('[data-ics]');
          if (button) this.downloadIcs(button);
        };
        document.addEventListener('click', this.onClick);

        if (typeof subscribe === 'function' && typeof PUB_SUB_EVENTS !== 'undefined') {
          this.unsubscribe = subscribe(PUB_SUB_EVENTS.variantChange, ({ data }) => {
            if (!data || data.sectionId !== this.sectionId || !data.html) return;
            const infoId = `EventSession-${this.sectionId}`;
            const source = data.html.getElementById(infoId);
            const target = document.getElementById(infoId);
            if (source && target) target.innerHTML = source.innerHTML;

            const buttonId = `ProductSubmitButton-${this.sectionId}`;
            const sourceLabel = data.html.querySelector(`#${buttonId} > span`);
            const label = document.querySelector(`#${buttonId} > span`);
            if (sourceLabel && label) label.textContent = sourceLabel.textContent.trim();
          });
        }

        this.selectFirstUpcoming();
      }

      disconnectedCallback() {
        this.unsubscribe?.();
        document.removeEventListener('click', this.onClick);
      }

      selectFirstUpcoming() {
        const fieldset = document.querySelector(`#variant-selects-${this.sectionId} [data-event-dates]`);
        if (!fieldset || fieldset.querySelector('input:checked')) return;
        const first = fieldset.querySelector('input:not([disabled])');
        if (!first) return;
        first.checked = true;
        first.dispatchEvent(new Event('change', { bubbles: true }));
      }

      downloadIcs(button) {
        const start = new Date(button.dataset.start);
        if (Number.isNaN(start.getTime())) return;
        const end = new Date(start.getTime() + (Number(button.dataset.duration) || 120) * 60000);
        const stamp = (date) => date.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
        const text = (value) => (value || '').replace(/[\\;,]/g, (c) => `\\${c}`).replace(/\n/g, '\\n');
        const ics = [
          'BEGIN:VCALENDAR',
          'VERSION:2.0',
          'PRODID:-//Tatreez House//Events//EN',
          'CALSCALE:GREGORIAN',
          'BEGIN:VEVENT',
          `UID:${stamp(start)}-${button.dataset.filename}@tatreez-house`,
          `DTSTAMP:${stamp(new Date())}`,
          `DTSTART:${stamp(start)}`,
          `DTEND:${stamp(end)}`,
          `SUMMARY:${text(button.dataset.title)}`,
          `DESCRIPTION:${text(button.dataset.url)}`,
          `URL:${button.dataset.url}`,
          'END:VEVENT',
          'END:VCALENDAR',
        ].join('\r\n');

        const url = URL.createObjectURL(new Blob([ics], { type: 'text/calendar;charset=utf-8' }));
        const link = document.createElement('a');
        link.href = url;
        link.download = button.dataset.filename || 'event.ics';
        document.body.appendChild(link);
        link.click();
        link.remove();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
      }
    }
  );
}
