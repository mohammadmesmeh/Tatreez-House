const SCROLL_ANIMATION_TRIGGER_CLASSNAME = 'scroll-trigger';
const SCROLL_ZOOM_IN_TRIGGER_CLASSNAME = 'animate--zoom-in';
// Tatreez House: content is visible by default (tatreez-tokens.css, "Scroll reveal"). The script
// only ADDS an entrance animation, so content never depends on it to become visible.
const SCROLL_ANIMATION_RUN_CLASSNAME = 'th-reveal-run';
const SCROLL_ANIMATION_READY_CLASSNAME = 'js-reveal-ready';

// Scroll in animation logic
function onIntersection(entries, observer) {
  entries.forEach((entry, index) => {
    if (!entry.isIntersecting) return;
    const elementTarget = entry.target;
    if (elementTarget.hasAttribute('data-cascade')) {
      elementTarget.style.setProperty('--animation-order', index);
    }
    elementTarget.classList.add(SCROLL_ANIMATION_RUN_CLASSNAME);
    observer.unobserve(elementTarget);
  });
}

function initializeScrollAnimationTrigger(rootEl = document, isDesignModeEvent = false) {
  const animationTriggerElements = Array.from(rootEl.getElementsByClassName(SCROLL_ANIMATION_TRIGGER_CLASSNAME));
  if (animationTriggerElements.length === 0) return;

  if (isDesignModeEvent) {
    animationTriggerElements.forEach((element) => {
      element.classList.add('scroll-trigger--design-mode');
    });
    return;
  }

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  document.documentElement.classList.add(SCROLL_ANIMATION_READY_CLASSNAME);

  // Start the animation just before an element enters (32px early), so the shopper never sees
  // it jump from visible to hidden. Elements already on screen at load are never animated.
  const observer = new IntersectionObserver(onIntersection, {
    rootMargin: '0px 0px 32px 0px',
  });
  const viewportHeight = window.innerHeight;
  animationTriggerElements.forEach((element) => {
    if (element.getBoundingClientRect().top < viewportHeight) return;
    observer.observe(element);
  });
}

// Zoom in animation logic
function initializeScrollZoomAnimationTrigger() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const animationTriggerElements = Array.from(document.getElementsByClassName(SCROLL_ZOOM_IN_TRIGGER_CLASSNAME));

  if (animationTriggerElements.length === 0) return;

  const scaleAmount = 0.2 / 100;

  animationTriggerElements.forEach((element) => {
    let elementIsVisible = false;
    const observer = new IntersectionObserver((elements) => {
      elements.forEach((entry) => {
        elementIsVisible = entry.isIntersecting;
      });
    });
    observer.observe(element);

    element.style.setProperty('--zoom-in-ratio', 1 + scaleAmount * percentageSeen(element));

    window.addEventListener(
      'scroll',
      throttle(() => {
        if (!elementIsVisible) return;

        element.style.setProperty('--zoom-in-ratio', 1 + scaleAmount * percentageSeen(element));
      }),
      { passive: true }
    );
  });
}

function percentageSeen(element) {
  const viewportHeight = window.innerHeight;
  const scrollY = window.scrollY;
  const elementPositionY = element.getBoundingClientRect().top + scrollY;
  const elementHeight = element.offsetHeight;

  if (elementPositionY > scrollY + viewportHeight) {
    // If we haven't reached the image yet
    return 0;
  } else if (elementPositionY + elementHeight < scrollY) {
    // If we've completely scrolled past the image
    return 100;
  }

  // When the image is in the viewport
  const distance = scrollY + viewportHeight - elementPositionY;
  let percentage = distance / ((viewportHeight + elementHeight) / 100);
  return Math.round(percentage);
}

window.addEventListener('DOMContentLoaded', () => {
  initializeScrollAnimationTrigger();
  initializeScrollZoomAnimationTrigger();
});

if (Shopify.designMode) {
  document.addEventListener('shopify:section:load', (event) => initializeScrollAnimationTrigger(event.target, true));
  document.addEventListener('shopify:section:reorder', () => initializeScrollAnimationTrigger(document, true));
}
