/**
 * announcement-autoplay.js — respects prefers-reduced-motion for the announcement bar.
 *
 * With a pause/play button present, Dawn's SlideshowComponent.setAutoPlay() starts rotating
 * without checking reduced motion. When the visitor prefers reduced motion, start paused by
 * calling Dawn's own toggle (the button then reads "Play slideshow").
 */
(() => {
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  customElements.whenDefined('slideshow-component').then(() => {
    document.querySelectorAll('.announcement-bar-slider .announcement-bar__autoplay').forEach((button) => {
      const slideshow = button.closest('slideshow-component');
      // setAutoPlay runs in the element constructor; wait a frame so its state exists.
      requestAnimationFrame(() => {
        if (slideshow?.autoplayButtonIsSetToPlay && typeof slideshow.autoPlayToggle === 'function') {
          slideshow.autoPlayToggle();
        }
      });
    });
  });
})();
