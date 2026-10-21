/**
 * hero-slideshow.js — full-bleed hero slideshow (sections/hero-slideshow.liquid).
 *
 * Timing lives in CSS: the hidden [data-timer] animates for --hero-duration and its
 * `animationend` advances the slide; the progress fill and the image zoom run in sync. Pausing
 * only toggles .is-playing (animation-play-state), so every pause resumes where it stopped.
 *
 * Plays only when not paused by the user AND no temporary hold applies (hover, focus inside,
 * tab hidden, section offscreen). prefers-reduced-motion starts paused, with instant swaps.
 * Without JavaScript, slide 1 is shown (server-rendered .is-active; others are inert).
 */
if (!customElements.get('hero-slideshow')) {
  customElements.define(
    'hero-slideshow',
    class HeroSlideshow extends HTMLElement {
      connectedCallback() {
        this.slides = Array.from(this.querySelectorAll('[data-slide]'));
        this.steps = Array.from(this.querySelectorAll('[data-step]'));
        this.toggle = this.querySelector('[data-toggle]');
        this.timer = this.querySelector('[data-timer]');
        this.slidesContainer = this.querySelector('[data-slides]');
        this.controls = this.querySelector('[data-controls]');
        this.index = 0;
        this.holds = new Set();

        this.setupHeaderOverlay();
        if (this.slides.length < 2) return;

        const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        this.userPaused = this.dataset.autoplay !== 'true' || reducedMotion;
        this.classList.add('is-enhanced', 'is-cycling');
        this.render();

        this.steps.forEach((step, i) => step.addEventListener('click', () => this.goTo(i, true)));
        this.toggle?.addEventListener('click', () => {
          this.userPaused = !this.userPaused;
          this.update();
        });
        this.controls?.addEventListener('keydown', (event) => this.onKeydown(event));
        this.timer?.addEventListener('animationend', () => this.goTo(this.index + 1, false));

        this.addEventListener('mouseenter', () => this.hold('hover', true));
        this.addEventListener('mouseleave', () => this.hold('hover', false));
        this.addEventListener('focusin', () => this.hold('focus', true));
        this.addEventListener('focusout', (event) => {
          if (!this.contains(event.relatedTarget)) this.hold('focus', false);
        });
        this.onVisibility = () => this.hold('hidden', document.hidden);
        document.addEventListener('visibilitychange', this.onVisibility);
        this.observer = new IntersectionObserver(([entry]) => this.hold('offscreen', !entry.isIntersecting), {
          threshold: 0.25,
        });
        this.observer.observe(this);

        this.update();
      }

      disconnectedCallback() {
        document.removeEventListener('visibilitychange', this.onVisibility);
        this.observer?.disconnect();
        document.documentElement.classList.remove('th-header-over-hero');
      }

      get playing() {
        return !this.userPaused && this.holds.size === 0;
      }

      hold(reason, active) {
        if (active) this.holds.add(reason);
        else this.holds.delete(reason);
        this.update();
      }

      goTo(target, manual) {
        const count = this.slides.length;
        this.index = (target + count) % count;
        // Restart the CSS timer, progress fill and zoom for the new slide.
        this.classList.remove('is-cycling');
        void this.offsetWidth;
        this.classList.add('is-cycling');
        // Polite announcements only for changes the visitor asked for.
        if (manual) this.slidesContainer.setAttribute('aria-live', 'polite');
        this.render();
        this.update();
      }

      onKeydown(event) {
        if (!event.target.matches('[data-step]')) return;
        const rtl = getComputedStyle(this).direction === 'rtl';
        const forward = rtl ? 'ArrowLeft' : 'ArrowRight';
        const back = rtl ? 'ArrowRight' : 'ArrowLeft';
        let next = null;
        if (event.key === forward) next = this.index + 1;
        if (event.key === back) next = this.index - 1;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = this.slides.length - 1;
        if (next === null) return;
        event.preventDefault();
        this.goTo(next, true);
        this.steps[this.index]?.focus();
      }

      render() {
        this.slides.forEach((slide, i) => {
          const active = i === this.index;
          slide.classList.toggle('is-active', active);
          slide.inert = !active;
        });
        this.steps.forEach((step, i) => {
          step.classList.toggle('is-active', i === this.index);
          step.classList.toggle('is-done', i < this.index);
          if (i === this.index) step.setAttribute('aria-current', 'true');
          else step.removeAttribute('aria-current');
        });
      }

      update() {
        const playing = this.playing;
        this.classList.toggle('is-playing', playing);
        // Off while it rotates by itself; polite when the visitor is in control.
        if (playing) this.slidesContainer.setAttribute('aria-live', 'off');
        else this.slidesContainer.setAttribute('aria-live', 'polite');
        this.toggle?.setAttribute('aria-pressed', String(this.userPaused));
      }

      // Transparent header over the hero: only when this hero is the first section on the page.
      setupHeaderOverlay() {
        if (this.dataset.headerOverlay !== 'true') return;
        const section = this.closest('.shopify-section');
        const main = document.querySelector('main');
        if (!section || !main || main.querySelector('.shopify-section') !== section) return;
        document.documentElement.classList.add('th-header-over-hero');
      }
    }
  );
}
