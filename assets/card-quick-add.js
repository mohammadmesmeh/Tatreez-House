/**
 * card-quick-add.js — screen-reader announcements for product-card quick add.
 *
 * Pairs with snippets/card-quick-add.liquid. Adding to cart stays entirely in Dawn's
 * product-form (fetch to /cart/add.js, cart drawer/notification, cart count); this element only
 * listens: it announces "Adding…" when its form submits, then "Added" or the error state when
 * Dawn publishes cartUpdate / cartError for this card's variant (pubsub.js).
 */
if (!customElements.get('card-quick-add')) {
  customElements.define(
    'card-quick-add',
    class CardQuickAdd extends HTMLElement {
      connectedCallback() {
        this.status = this.querySelector('[data-card-quick-add-status]');
        this.form = this.querySelector('form[data-type="add-to-cart-form"]');
        if (!this.status || !this.form) return;

        this.onSubmit = () => this.announce(this.dataset.adding);
        this.form.addEventListener('submit', this.onSubmit);

        if (typeof subscribe !== 'function' || typeof PUB_SUB_EVENTS === 'undefined') return;
        this.unsubscribers = [
          subscribe(PUB_SUB_EVENTS.cartUpdate, (event) => {
            if (this.isOwnEvent(event)) this.announce(this.dataset.added);
          }),
          subscribe(PUB_SUB_EVENTS.cartError, (event) => {
            if (this.isOwnEvent(event)) this.announce(this.dataset.error);
          }),
        ];
      }

      disconnectedCallback() {
        this.form?.removeEventListener('submit', this.onSubmit);
        this.unsubscribers?.forEach((unsubscribe) => unsubscribe());
      }

      isOwnEvent(event) {
        if (!event || event.source !== 'product-form') return false;
        const variantInput = this.form.querySelector('[name="id"]');
        return Boolean(variantInput) && String(variantInput.value) === String(event.productVariantId);
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
