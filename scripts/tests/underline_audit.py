"""Underline audit: exactly one underline style per state (the stitch replaces Dawn's underline).

usage: python -X utf8 scripts/tests/underline_audit.py BASE_URL [OUT_DIR]

For every audited link-like element, in each state (default, hover, keyboard focus), counts
- solid underlines: computed text-decoration-line containing "underline" on the element, its
  ancestors up to the section and its descendants (decorations propagate to the text);
- stitches: a dashed repeating-linear-gradient background drawn at a non-zero width.
It FAILs when both are drawn at once (double underline) and, where the stitch is drawn, also
requires text-decoration-line "none" on every element in that chain. EN and /ar.
"""
import json, sys
from playwright.sync_api import sync_playwright

base = sys.argv[1].rstrip('/')
out = sys.argv[2] if len(sys.argv) > 2 else None
R = []
def ok(name, cond, detail=''):
    R.append((name, bool(cond), str(detail)))

def goto(page, url):
    response = page.goto(url, wait_until='domcontentloaded', timeout=120000)
    try:
        page.wait_for_load_state('load', timeout=20000)
    except Exception:
        pass
    return response

MEASURE = """(el) => {
  const chain = [];
  for (let a = el; a && !a.matches('header, footer, main, body, .shopify-section'); a = a.parentElement) chain.push(a);
  chain.push(...el.querySelectorAll('*'));
  const solid = [], stitch = [];
  for (const n of chain) {
    const s = getComputedStyle(n);
    if (s.textDecorationLine.includes('underline')) solid.push(n.tagName + '.' + (n.getAttribute('class') || '').split(' ')[0]);
    if (s.backgroundImage.includes('repeating-linear-gradient') && !s.backgroundImage.includes('0deg') && parseFloat(s.backgroundSize) > 0)
      stitch.push(n.tagName + '.' + (n.getAttribute('class') || '').split(' ')[0]);
  }
  return { solid, stitch, text: el.innerText.trim().slice(0, 24) };
}"""

# (label, path, selector, viewport width, states)
TARGETS = [
    ('header item (current page)', '/pages/workshops', '.header__inline-menu a[aria-current="page"]', 1440, ('default', 'hover', 'focus')),
    ('header item', '/', '.header__inline-menu a.header__menu-item', 1440, ('default', 'hover', 'focus')),
    ('dropdown trigger (open)', '/', '#Details-HeaderMenu-1 > summary', 1440, ('open',)),
    ('dropdown trigger (child active)', '/collections/clothing', '#Details-HeaderMenu-1 > summary', 1440, ('default', 'hover')),
    ('dropdown link', '/', '#Details-HeaderMenu-1 .header__submenu a', 1440, ('open-hover', 'open-focus')),
    ('dropdown link (current page)', '/collections/clothing', '#Details-HeaderMenu-1 .header__submenu a[aria-current="page"]', 1440, ('open-default', 'open-hover')),
    ('drawer link', '/', '#menu-drawer .menu-drawer__menu-item', 390, ('drawer-hover', 'drawer-focus')),
    ('footer policy link', '/', '.footer__inline-link', 1440, ('default', 'hover', 'focus')),
    ('footer copyright link', '/', '.footer__copyright-line a', 1440, ('default', 'hover', 'focus')),
    ('language selector', '/', '#FooterLanguageForm .disclosure__button', 1440, ('default', 'hover', 'focus')),
    ('card title', '/collections/all', '.product-card-wrapper .card__heading a >> visible=true', 1440, ('default', 'hover', 'focus')),
    ('event card Details', '/pages/workshops?view=events', '.event-session__details', 1440, ('default', 'hover', 'focus')),
    ('view all', '/', '.collection__view-all a', 1440, ('default', 'hover', 'focus')),
    ('learn teaser link', '/', '.learn-teaser__all', 1440, ('default', 'hover', 'focus')),
    ('page content link (rte)', '/pages/tatreez-101', 'main .rte a', 1440, ('default', 'hover', 'focus')),
    ('pagination', '/collections/all?page=1', '.pagination__item', 1440, ('default', 'hover')),
    ('breadcrumb', '/products/navy-village-thobe', '.breadcrumbs a, nav[aria-label*="readcrumb"] a', 1440, ('default', 'hover')),
]

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel='msedge')
    for lang, prefix in (('en', ''), ('ar', '/ar')):
        for label, path, selector, width, states in TARGETS:
            ctx = b.new_context(viewport={'width': width, 'height': 900}); pg = ctx.new_page()
            goto(pg, base + prefix + path); pg.wait_for_timeout(800)
            if pg.locator(selector).count() == 0:
                R.append((f'{lang} {label}', None, 'not on this page'))
                ctx.close(); continue
            for state in states:
                pg.mouse.move(2, 2); pg.wait_for_timeout(100)
                if state.startswith('open'):
                    pg.locator('#Details-HeaderMenu-1 > summary').click(); pg.wait_for_timeout(400)
                if state.startswith('drawer'):
                    pg.click('header-drawer summary'); pg.wait_for_timeout(600)
                loc = pg.locator(f'{selector} >> visible=true').first
                if loc.count() == 0:
                    R.append((f'{lang} {label} [{state}]', None, 'not visible in this state'))
                    continue
                if state.endswith('hover'):
                    loc.scroll_into_view_if_needed(); loc.hover(); pg.wait_for_timeout(450)
                if state.endswith('focus'):
                    pg.keyboard.press('Shift'); loc.focus(); pg.wait_for_timeout(450)
                m = loc.evaluate(MEASURE)
                double = bool(m['solid']) and bool(m['stitch'])
                ok(f'{lang} {label} [{state}] "{m["text"]}": one underline style', not double, m)
                if out and lang == 'en' and state in ('default', 'hover', 'open', 'open-default') and label.startswith(('header item', 'dropdown')):
                    box = loc.bounding_box()
                    if box:
                        pg.screenshot(path=f'{out}/{label.replace(" ", "-").replace("(", "").replace(")", "")}-{state}-{lang}.png',
                                      clip={'x': max(box['x'] - 20, 0), 'y': max(box['y'] - 10, 0), 'width': box['width'] + 40, 'height': box['height'] + 20})
                if state.startswith(('open', 'drawer')):
                    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
            ctx.close()
    b.close()

for name, cond, detail in R:
    print({True: 'PASS', False: 'FAIL', None: 'SKIP'}[cond], name, '-', detail[:200])
print('summary', sum(c is True for _, c, _ in R), 'pass /', sum(c is False for _, c, _ in R), 'fail /', sum(c is None for _, c, _ in R), 'skip')
