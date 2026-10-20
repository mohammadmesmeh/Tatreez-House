"""Capture full-page screenshots of the key storefront pages for design reviews.

usage: python scripts/capture-screens.py OUT_DIR [BASE_URL] [--widths 390,1440] [--rtl]

Pages: home, a collection, a garment product, a pattern product, search, the cart drawer after a
card quick add (first digital pattern), and the mobile menu (drawer open, widths below 990px). Uses the system Microsoft Edge through
Playwright (no browser download), emulates prefers-reduced-motion so scroll-reveal animations
do not hide content in full-page captures, and writes JPEGs to keep the repository small.
--rtl forces dir="rtl" lang="ar" and injects rtl.css (for stores without Arabic enabled).
"""
import argparse
import pathlib
from playwright.sync_api import sync_playwright

PAGES = {
    'home': '/',
    'collection': '/collections/clothing',
    'product-garment': '/products/ivory-heritage-dress',
    'product-pattern': '/products/cypress-motif-pattern',
    'search': '/search?q=tatreez',
}

parser = argparse.ArgumentParser()
parser.add_argument('out')
parser.add_argument('base', nargs='?', default='http://127.0.0.1:9393')
parser.add_argument('--widths', default='390,1440')
parser.add_argument('--rtl', action='store_true')
parser.add_argument('--pages', default=','.join(list(PAGES) + ['cart-drawer', 'mobile-menu']))
parser.add_argument('--quality', type=int, default=68)
args = parser.parse_args()
out = pathlib.Path(args.out)
out.mkdir(parents=True, exist_ok=True)
suffix = '-rtl' if args.rtl else ''


def force_rtl(page):
    page.evaluate("""() => {
      const h = document.documentElement; h.dir = 'rtl'; h.lang = 'ar';
      const base = document.querySelector('link[href*="/assets/base.css"]');
      if (base && !document.querySelector('link[href*="/assets/rtl.css"]')) {
        const l = document.createElement('link'); l.rel = 'stylesheet';
        l.href = base.href.split('/assets/')[0] + '/assets/rtl.css'; document.head.appendChild(l);
      }
    }""")
    page.wait_for_timeout(400)


def open_page(page, path):
    page.goto(args.base + path, wait_until='load', timeout=120000)
    page.wait_for_timeout(1500)
    if args.rtl:
        force_rtl(page)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge')
    for width in [int(w) for w in args.widths.split(',')]:
        ctx = browser.new_context(viewport={'width': width, 'height': 900 if width >= 750 else 844},
                                  reduced_motion='reduce')
        page = ctx.new_page()
        for name in args.pages.split(','):
            target = out / f'{name}-{width}{suffix}.jpg'
            if name == 'cart-drawer':
                page.goto(args.base + '/cart/clear', wait_until='load')
                open_page(page, '/collections/digital-patterns')
                card = page.locator('.product-card-wrapper').first
                card.hover()
                card.locator('.quick-add__submit').click()
                page.wait_for_selector('cart-drawer.active', timeout=20000)
                page.wait_for_timeout(1200)
                page.screenshot(path=str(target), type='jpeg', quality=args.quality)
            elif name == 'mobile-menu':
                if width >= 990:
                    continue
                open_page(page, PAGES['home'])
                page.locator('header-drawer summary').click()
                page.wait_for_timeout(900)
                page.screenshot(path=str(target), type='jpeg', quality=args.quality)
            else:
                open_page(page, PAGES[name])
                page.screenshot(path=str(target), full_page=True, type='jpeg', quality=args.quality)
            print('saved', target)
        ctx.close()
    browser.close()
