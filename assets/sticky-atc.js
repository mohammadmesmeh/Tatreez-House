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
        this.button = this.querySelector('[data-sticky-button]');
        this.priceTarget = this.querySelector('[data-sticky-price]');
        this.mainButtonOutOfView = false;

        this.sync();
        this.observe();

        this.onMediaChange = () => this.update();
        StickyAtc.mobileQuery.addEventListener('change', this.onMediaChange);

        if (typeof subscribe === 'function' && typeof PUB_SUB_EVENTS !== 'undefined') {
          this.unsubscribe = subscribe(PUB_SUB_EVENTS.variantChange, () => {
            // product-info swaps the button markup; re-observe the new node and mirror it.
            this.sync();
            this.observe();
          });
        }
      }

      disconnectedCallback() {
        this.observer?.disconnect();
        this.unsubscribe?.();
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
          if (label) this.button.textContent = label;
          this.button.disabled = main.disabled;
        }
        const price = document.getElementById(this.dataset.priceSource);
        if (price && this.priceTarget) this.priceTarget.innerHTML = price.innerHTML;
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
