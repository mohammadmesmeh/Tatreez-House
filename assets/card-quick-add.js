/**
 * card-quick-add.js — screen-reader announcements for product-card quick add.
 *
 * Pairs with snippets/card-quick-add.liquid. Adding to cart stays entirely in Dawn's
 * product-form (fetch to /cart/add.js, cart drawer/notification, cart count); this element only
 * listens: it announces "Adding…" when its own form really submits, then "Added" or the error
 * state when Dawn publishes cartUpdate / cartError for that submission (pubsub.js).
 */
if (!customElements.get('card-quick-add')) {
  customElements.define(
    'card-quick-add',
    class CardQuickAdd extends HTMLElement {
      connectedCallback() {
        this.status = this.querySelector('[data-card-quick-add-status]');
        this.form = this.querySelector('form[data-type="add-to-cart-form"]');
        if (!this.status || !this.form) return;

        // Capture on this ancestor runs before Dawn's product-form submit handler, so the button's
        // aria-disabled still reflects whether this submit will actually be processed.
        this.onSubmit = (event) => {
          if (event.target !== this.form) return;
          const button = this.form.querySelector('[type="submit"]');
          if (button?.getAttribute('aria-disabled') === 'true' || button?.disabled) return;
          this.pending = true;
          this.announce(this.dataset.adding);
        };
        this.addEventListener('submit', this.onSubmit, true);

        if (typeof subscribe !== 'function' || typeof PUB_SUB_EVENTS === 'undefined') return;
        this.unsubscribers = [
          subscribe(PUB_SUB_EVENTS.cartUpdate, (event) => {
            if (this.isOwnEvent(event)) this.settle(this.dataset.added);
          }),
          subscribe(PUB_SUB_EVENTS.cartError, (event) => {
            if (this.isOwnEvent(event)) this.settle(this.dataset.error);
          }),
        ];
      }

      disconnectedCallback() {
        this.removeEventListener('submit', this.onSubmit, true);
        this.unsubscribers?.forEach((unsubscribe) => unsubscribe());
      }

      // Only the card whose form was submitted answers (the same variant can appear on several
      // cards on one page, e.g. featured collection + recommendations).
      isOwnEvent(event) {
        if (!this.pending || !event || event.source !== 'product-form') return false;
        const variantInput = this.form.querySelector('[name="id"]');
        return Boolean(variantInput) && String(variantInput.value) === String(event.productVariantId);
      }

      settle(message) {
        this.pending = false;
        this.announce(message);
      }

      announce(message) {
        if (!message) return;
        // Clear first so repeating the same message is announced again.
        this.status.textContent = '';
        window.setTimeout(() => {
          this.status.textContent = message;
        }, 50);
      }
    }
  );
}
