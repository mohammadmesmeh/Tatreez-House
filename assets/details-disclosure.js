class DetailsDisclosure extends HTMLElement {
  constructor() {
    super();
    this.mainDetailsToggle = this.querySelector('details');
    this.content = this.mainDetailsToggle.querySelector('summary').nextElementSibling;

    this.mainDetailsToggle.addEventListener('focusout', this.onFocusOut.bind(this));
    this.mainDetailsToggle.addEventListener('toggle', this.onToggle.bind(this));
  }

  onFocusOut() {
    setTimeout(() => {
      if (!this.contains(document.activeElement)) this.close();
    });
  }

  onToggle() {
    if (!this.animations) this.animations = this.content.getAnimations();

    if (this.mainDetailsToggle.hasAttribute('open')) {
      this.animations.forEach((animation) => animation.play());
    } else {
      this.animations.forEach((animation) => animation.cancel());
    }
  }

  close() {
    this.mainDetailsToggle.removeAttribute('open');
    this.mainDetailsToggle.querySelector('summary').setAttribute('aria-expanded', false);
  }
}

customElements.define('details-disclosure', DetailsDisclosure);

/*
  Desktop header menus. Besides Dawn's behaviour (click/Enter/Space toggle the <details>, Escape
  closes it from global.js, focus leaving closes it from DetailsDisclosure), this adds:
  - hover opens on devices with a real pointer, with a short grace period when leaving; a click
    on a hover-opened trigger keeps it open instead of closing it;
  - an outside click closes it, and only one menu is open at a time;
  - aria-expanded always matches the open state, whatever opened or closed it;
  - the dropdown card sits 8px below the header edge (--th-dropdown-offset).
*/
class HeaderMenu extends DetailsDisclosure {
  constructor() {
    super();
    this.header = document.querySelector('.header-wrapper');
    this.summary = this.mainDetailsToggle.querySelector('summary');
    this.canHover = window.matchMedia('(hover: hover) and (pointer: fine)');

    this.addEventListener('pointerenter', (event) => {
      if (event.pointerType !== 'mouse' || !this.canHover.matches) return;
      clearTimeout(this.closeTimer);
      if (!this.mainDetailsToggle.open) {
        this.openedByHover = true;
        this.mainDetailsToggle.setAttribute('open', '');
      }
    });
    this.addEventListener('pointerleave', (event) => {
      if (event.pointerType !== 'mouse' || !this.openedByHover) return;
      this.closeTimer = setTimeout(() => this.close(), 150);
    });
    this.summary.addEventListener('click', (event) => {
      if (!this.openedByHover || !this.mainDetailsToggle.open) return;
      event.preventDefault();
      this.openedByHover = false;
      this.summary.setAttribute('aria-expanded', 'true');
    });
    document.addEventListener('click', (event) => {
      if (this.mainDetailsToggle.open && !this.contains(event.target)) this.close();
    });
  }

  onToggle() {
    const open = this.mainDetailsToggle.open;
    this.summary.setAttribute('aria-expanded', open);
    if (open) {
      document.querySelectorAll('header-menu').forEach((menu) => {
        if (menu !== this && menu.mainDetailsToggle.open) menu.close();
      });
      if (this.header && this.content) {
        const gap = this.header.getBoundingClientRect().bottom - this.mainDetailsToggle.getBoundingClientRect().bottom;
        this.content.style.setProperty('--th-dropdown-offset', `${Math.max(0, Math.round(gap)) + 8}px`);
      }
    } else {
      this.openedByHover = false;
    }

    if (!this.header) return;
    this.header.preventHide = open;

    if (document.documentElement.style.getPropertyValue('--header-bottom-position-desktop') !== '') return;
    document.documentElement.style.setProperty(
      '--header-bottom-position-desktop',
      `${Math.floor(this.header.getBoundingClientRect().bottom)}px`
    );
  }

  close() {
    clearTimeout(this.closeTimer);
    this.openedByHover = false;
    super.close();
  }
}

customElements.define('header-menu', HeaderMenu);
