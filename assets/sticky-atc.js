/**
 * sticky-atc.js — mobile sticky add-to-cart bar (snippets/sticky-atc.liquid).
 *
 * Shows the bar when the main Add to cart button has scrolled above the viewport on small screens.
 * The bar's button submits the main product form (form attribute), so Dawn's product-form does the
 * work. Label, disabled state and price are mirrored from the main button / price block, re-read
 * after every variant change because Dawn's product-info replaces that markup.
 * While visible, scroll-padding keeps focused elements clear of the bar (WCAG 2.4.11).
 */
if (!customElements.get('sticky-atc')) {
  customElements.define(
    'sticky-atc',
    class StickyAtc extends HTMLElement {
      static mobileQuery = window.matchMedia('(max-width: 749px)');

      connectedCallback() {
        // Dawn's quick-add modal copies product-info (and this element) into a dialog: stay inert.
        if (this.closest('quick-add-modal')) return;

        this.button = this.querySelector('[data-sticky-button]');
        this.label = this.querySelector('[data-sticky-label]');
        this.errorElement = this.querySelector('[data-sticky-error]');
        this.priceTarget = this.querySelector('[data-sticky-price]');
        this.form = this.button ? document.getElementById(this.button.getAttribute('form')) : null;

        // Busy state on the bar itself: the main button (where Dawn shows its spinner) is off screen.
        this.onSubmit = (event) => {
          if (event.submitter !== this.button) return;
          this.setError('');
          this.setBusy(true);
        };
        this.form?.addEventListener('submit', this.onSubmit, true);
        this.mainButtonOutOfView = false;

        this.sync();
        this.observe();

        this.onMediaChange = () => this.update();
        StickyAtc.mobileQuery.addEventListener('change', this.onMediaChange);

        if (typeof subscribe === 'function' && typeof PUB_SUB_EVENTS !== 'undefined') {
          this.unsubscribers = [
            subscribe(PUB_SUB_EVENTS.variantChange, () => {
              // product-info swaps the button markup; re-observe the new node and mirror it.
              this.setError('');
              this.sync();
              this.observe();
            }),
            subscribe(PUB_SUB_EVENTS.cartUpdate, (event) => {
              if (event?.source === 'product-form') this.setBusy(false);
            }),
            subscribe(PUB_SUB_EVENTS.cartError, (event) => {
              if (event?.source !== 'product-form' || !this.isBusy) return;
              this.setBusy(false);
              // Dawn's server message is already localized; show it where the shopper is looking.
              // Dawn publishes the specific text (response.description) as `errors`; `message` is
              // Shopify's generic title ("Cart Error"), so it is only a fallback.
              const message = (typeof event.errors === 'string' ? event.errors : '') || event.message;
              this.setError(message || this.dataset.errorFallback || '');
            }),
          ];
        }
      }

      disconnectedCallback() {
        this.observer?.disconnect();
        this.unsubscribers?.forEach((unsubscribe) => unsubscribe());
        this.form?.removeEventListener('submit', this.onSubmit, true);
        StickyAtc.mobileQuery.removeEventListener('change', this.onMediaChange);
        document.documentElement.style.removeProperty('scroll-padding-block-end');
      }

      get mainButton() {
        return document.getElementById(this.dataset.targetButton);
      }

      observe() {
        this.observer?.disconnect();
        const target = this.mainButton;
        if (!target) return;
        this.observer = new IntersectionObserver(([entry]) => {
          // Only after scrolling past the button (it sits above the viewport), not before reaching it.
          this.mainButtonOutOfView = !entry.isIntersecting && entry.boundingClientRect.top < 0;
          this.update();
        });
        this.observer.observe(target);
      }

      sync() {
        const main = this.mainButton;
        if (main && this.button) {
          const label = main.querySelector('span')?.textContent.trim();
          if (label && this.label) this.label.textContent = label;
          this.button.disabled = main.disabled;
        }
        const price = document.getElementById(this.dataset.priceSource);
        if (price && this.priceTarget) this.priceTarget.innerHTML = price.innerHTML;
      }

      setBusy(busy) {
        this.isBusy = busy;
        this.button?.classList.toggle('loading', busy);
        this.button?.setAttribute('aria-busy', String(busy));
        this.querySelector('.loading__spinner')?.classList.toggle('hidden', !busy);
      }

      setError(message) {
        if (!this.errorElement) return;
        this.errorElement.textContent = typeof message === 'string' ? message : '';
        this.errorElement.hidden = !this.errorElement.textContent;
      }

      update() {
        const show = this.mainButtonOutOfView && StickyAtc.mobileQuery.matches;
        if (show && this.hidden) this.sync();
        this.hidden = !show;
        const root = document.documentElement;
        if (show) {
          root.style.setProperty('scroll-padding-block-end', `${this.offsetHeight + 16}px`);
        } else {
          root.style.removeProperty('scroll-padding-block-end');
        }
      }
    }
  );
}
