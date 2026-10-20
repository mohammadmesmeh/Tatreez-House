/**
 * footer-accordion.js — collapses footer menu columns into accordions below 750px.
 *
 * Used by sections/footer.liquid. Lists render collapsed on small screens from first paint (CSS
 * :not(:defined)), so nothing shifts when this script runs; the heading button then toggles its
 * list (aria-expanded + hidden). On wider screens CSS shows the plain label and keeps the list
 * visible, and this element resets to "expanded".
 */
if (!customElements.get('footer-accordion')) {
  customElements.define(
    'footer-accordion',
    class FooterAccordion extends HTMLElement {
      static mobileQuery = window.matchMedia('(max-width: 749px)');

      connectedCallback() {
        this.button = this.querySelector('.footer-accordion__toggle');
        this.panel = this.querySelector('[data-accordion-panel]');
        if (!this.button || !this.panel) return;

        this.onClick = () => this.setExpanded(this.button.getAttribute('aria-expanded') !== 'true');
        this.onMediaChange = () => this.setExpanded(!FooterAccordion.mobileQuery.matches);

        this.button.addEventListener('click', this.onClick);
        FooterAccordion.mobileQuery.addEventListener('change', this.onMediaChange);
        this.onMediaChange();
      }

      disconnectedCallback() {
        this.button?.removeEventListener('click', this.onClick);
        FooterAccordion.mobileQuery.removeEventListener('change', this.onMediaChange);
      }

      setExpanded(expanded) {
        this.button.setAttribute('aria-expanded', String(expanded));
        this.panel.hidden = !expanded;
      }
    }
  );
}
