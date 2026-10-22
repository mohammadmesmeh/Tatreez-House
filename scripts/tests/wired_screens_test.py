"""M2.1 Step 7: screenshots of the wired store at every width in English and Arabic, with layout checks.

usage: python -X utf8 scripts/tests/wired_screens_test.py BASE_URL OUT_DIR
  BASE_URL  e.g. http://127.0.0.1:9393 (shopify theme dev) or the theme preview URL
  OUT_DIR   where screenshots are written (docs/screenshots/m2/wired for the committed set)

Per page, width and language: no horizontal scroll, correct document direction, exactly one h1.
Also captures the open Shop dropdown and the footer. Requires Playwright + Microsoft Edge.
"""
import sys
from playwright.sync_api import sync_playwright

base, out = sys.argv[1], sys.argv[2]
R = []
def ok(name, cond, detail=''):
    R.append((name, bool(cond), str(detail)))

PAGES = {'home': '/', 'collection': '/collections/all', 'product': '/products/navy-village-thobe', 'page': '/pages/tatreez-101'}
WIDTHS = (360, 390, 430, 768, 1440, 1920)
LANGS = (('en', ''), ('ar', '/ar'))
LAYOUT = """() => ({ overflow: document.documentElement.scrollWidth - innerWidth, dir: document.documentElement.dir || 'ltr',
                    h1: [...document.querySelectorAll('h1')].filter(h => h.getClientRects().length).length })"""

def shot(pg, name, **kw):
    try:
        pg.screenshot(path=f'{out}/{name}.jpg', type='jpeg', quality=68, timeout=60000, **kw)
    except Exception as e:
        print('NOTE screenshot skipped:', name, str(e)[:80])

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel='msedge')
    for lang, prefix in LANGS:
        for w in WIDTHS:
            ctx = b.new_context(viewport={'width': w, 'height': 1080 if w >= 1440 else 900}); pg = ctx.new_page()
            for name, path in PAGES.items():
                pg.goto(base + prefix + path, wait_until='load', timeout=120000); pg.wait_for_timeout(900)
                m = pg.evaluate(LAYOUT)
                want_dir = 'rtl' if lang == 'ar' else 'ltr'
                ok(f'{lang} {w}px {name}: no horizontal scroll, dir {want_dir}, one h1',
                   m['overflow'] <= 0 and m['dir'] == want_dir and m['h1'] == 1, m)
                shot(pg, f'{name}-{w}-{lang}')
            if w in (390, 1440):
                pg.goto(base + prefix + '/', wait_until='load', timeout=120000); pg.wait_for_timeout(600)
                pg.locator('footer.footer').scroll_into_view_if_needed(); pg.wait_for_timeout(400)
                try:
                    pg.locator('footer.footer').screenshot(path=f'{out}/footer-{w}-{lang}.jpg', type='jpeg', quality=72)
                except Exception as e:
                    print('NOTE footer screenshot skipped:', str(e)[:80])
            if w == 1440:
                pg.goto(base + prefix + '/collections/all', wait_until='load', timeout=120000); pg.wait_for_timeout(600)
                pg.locator('#Details-HeaderMenu-1 > summary').click(); pg.wait_for_timeout(500)
                ok(f'{lang} 1440px: Shop opens as a compact dropdown', pg.locator('#Details-HeaderMenu-1 .th-dropdown').is_visible())
                shot(pg, f'dropdown-1440-{lang}', clip={'x': 0, 'y': 0, 'width': 1440, 'height': 440})
            ctx.close()
    b.close()

for name, cond, detail in R:
    print('PASS' if cond else 'FAIL', name, '-', detail[:160])
print('summary', sum(c for _, c, _ in R), '/', len(R))
