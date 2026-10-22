/*
  events-filter.js — filters the events list by type (All / Workshops / Community circles).
  The filters are links with ?type=, so a filtered view can be shared; without JS every session
  shows (first N by CSS). Loaded only by sections/events-listing.liquid.
*/
if (!customElements.get('events-filter')) {
  customElements.define(
    'events-filter',
    class EventsFilter extends HTMLElement {
      connectedCallback() {
        this.links = [...this.querySelectorAll('[data-filter]')];
        this.items = [...this.querySelectorAll('[data-event-item]')];
        this.max = Number(this.dataset.max) || 12;
        this.status = this.querySelector('[data-filter-status]');
        this.empty = this.querySelector('[data-filter-empty]');

        this.links.forEach((link) =>
          link.addEventListener('click', (event) => {
            event.preventDefault();
            this.apply(link.dataset.filter, true);
          })
        );

        const requested = new URL(window.location.href).searchParams.get('type');
        const known = this.links.some((link) => link.dataset.filter === requested);
        this.apply(known ? requested : 'all', false);
      }

      apply(type, fromClick) {
        let shown = 0;
        this.items.forEach((item) => {
          const visible = (type === 'all' || item.dataset.eventType === type) && shown < this.max;
          if (visible) shown += 1;
          item.hidden = !visible;
          item.classList.remove('is-beyond-limit');
        });

        this.links.forEach((link) => {
          if (link.dataset.filter === type) {
            link.setAttribute('aria-current', 'true');
          } else {
            link.removeAttribute('aria-current');
          }
        });
        if (this.empty) this.empty.hidden = shown > 0;

        if (fromClick) {
          const url = new URL(window.location.href);
          if (type === 'all') {
            url.searchParams.delete('type');
          } else {
            url.searchParams.set('type', type);
          }
          window.history.replaceState({}, '', url);
          const active = this.links.find((link) => link.dataset.filter === type);
          if (this.status && active) this.status.textContent = active.dataset.status;
        }
      }
    }
  );
}
