/**
 * card-variant-picker.js — inline variant selection for product cards.
 *
 * Pairs with snippets/card-variant-picker.liquid (rendered by card-product for
 * quick add "standard" on multi-variant products). Matches the selected option
 * values against the real embedded variant data, keeps the form's hidden
 * variant id synchronised with a valid variant, and updates the card's price,
 * submit button and availability messaging. Adding to cart stays entirely in
 * Dawn's product-form element (product-form.js), which already provides the
 * fetch to /cart/add.js, cart notification / drawer updates, cart-count pubsub,
 * loading and error states, and duplicate-submission prevention.
 */
if (!customElements.get('card-variant-picker')) {
  customElements.define(
    'card-variant-picker',
    class CardVariantPicker extends HTMLElement {
      constructor() {
        super();

        try {
          this.variants = JSON.parse(this.querySelector('[data-variant-data]')?.textContent || '[]');
        } catch (error) {
          this.variants = [];
        }

        this.form = document.getElementById(this.dataset.productForm);
        this.variantIdInput = this.form ? this.form.querySelector('[name="id"]') : null;
        this.submitButton = this.form ? this.form.querySelector('[type="submit"]') : null;
        this.submitButtonText = this.submitButton ? this.submitButton.querySelector('span') : null;
        this.productFormElement = this.form ? this.form.closest('product-form') : null;

        this.unavailablePanel = this.querySelector('[data-picker-unavailable]');
        this.statusElement = this.querySelector('[data-picker-status]');

        const cardScope = this.closest('.product-card-wrapper');
        this.priceBox = cardScope ? cardScope.querySelector('[data-card-price] .price') : null;
        this.priceRegular = this.priceBox ? this.priceBox.querySelector('.price__regular .price-item--regular') : null;
        this.priceSaleAmount = this.priceBox ? this.priceBox.querySelector('.price__sale .price-item--sale') : null;
        this.priceSaleCompare = this.priceBox ? this.priceBox.querySelector('.price__sale s.price-item--regular') : null;
      }

      connectedCallback() {
        if (!this.form || !this.variantIdInput || !this.variants.length) return;

        this.addEventListener('change', () => this.update());
        this.update(false);
      }

      get selectedOptions() {
        const controls = Array.from(
          this.querySelectorAll('input[type="radio"][data-option-position], select[data-option-position]')
        );
        controls.sort((a, b) => Number(a.dataset.optionPosition) - Number(b.dataset.optionPosition));

        const selected = [];
        controls.forEach((control) => {
          if (control instanceof HTMLSelectElement) {
            selected.push(control.value);
          } else if (control.checked) {
            selected.push(control.value);
          }
        });
        return selected;
      }

      findVariant(selectedOptions) {
        return this.variants.find(
          (variant) =>
            variant.options.length === selectedOptions.length &&
            variant.options.every((option, index) => option === selectedOptions[index])
        );
      }

      update(announce = true) {
        const variant = this.findVariant(this.selectedOptions) || null;
        const strings = window.variantStrings || {};
        const canAddToCart = Boolean(variant && variant.available && !variant.requires_selling_plan);

        if (variant) this.variantIdInput.value = variant.id;

        this.updatePrice(variant);
        this.updateSubmitButton(variant, canAddToCart, strings);

        // Chosen combination has no purchasable variant (or needs a selling
        // plan): surface the product-page link so there is always a way forward.
        if (this.unavailablePanel) {
          this.unavailablePanel.hidden = Boolean(variant && !variant.requires_selling_plan);
        }

        // A new selection clears any stale error state from a previous submit.
        if (this.productFormElement) {
          this.productFormElement.handleErrorMessage(false);
          this.productFormElement.error = false;
        }

        if (announce && this.statusElement) {
          this.statusElement.textContent = this.statusText(variant, strings);
        }
      }

      updatePrice(variant) {
        if (!variant || !this.priceBox) return;

        if (this.priceRegular) this.priceRegular.textContent = variant.price;

        const onSale = Boolean(variant.compare_at_price && variant.compare_at_price !== variant.price);
        if (onSale) {
          if (this.priceSaleCompare) this.priceSaleCompare.textContent = variant.compare_at_price;
          if (this.priceSaleAmount) this.priceSaleAmount.textContent = variant.price;
        }

        this.priceBox.classList.toggle('price--on-sale', onSale);
        this.priceBox.classList.toggle('price--sold-out', !variant.available);
      }

      updateSubmitButton(variant, canAddToCart, strings) {
        if (!this.submitButton) return;

        const label = !variant ? strings.unavailable : variant.available ? strings.addToCart : strings.soldOut;
        if (label && this.submitButtonText) this.submitButtonText.textContent = label;

        const soldOutMessage = this.submitButton.querySelector('.sold-out-message');
        if (soldOutMessage) soldOutMessage.classList.add('hidden');

        this.submitButton.toggleAttribute('disabled', !canAddToCart);
        if (canAddToCart) this.submitButton.removeAttribute('aria-disabled');
      }

      statusText(variant, strings) {
        if (!variant) return strings.unavailable || '';

        const parts = [variant.price];
        if (variant.requires_selling_plan) {
          parts.unshift(strings.unavailable || '');
        } else {
          parts.push(variant.available ? strings.addToCart || '' : strings.soldOut || '');
        }
        return parts.filter(Boolean).join(', ');
      }
    }
  );
}
