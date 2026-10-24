"""Acceptance tests for the compact desktop dropdowns (snippets/header-dropdown-menu.liquid,
details-disclosure.js HeaderMenu, component-header-tatreez.css).

usage: python -X utf8 scripts/tests/header_dropdowns_test.py BASE_URL OUT_DIR

EN and /ar at 1024 and 1440 px: card geometry (under its own trigger, inline-start aligned,
~8px below the header, 220-400px wide, 44px rows, Nunito body size), hover / click / Enter /
Space open, Escape / outside click / focus leaving close, one menu open at a time,
aria-expanded, no layout shift, reduced motion, no mega menu card. Mobile drawer still opens.
Requires Playwright + Microsoft Edge.
"""
import sys
from playwright.sync_api import sync_playwright

base, out = sys.argv[1].rstrip('/'), sys.argv[2]
R = []

def goto(page, url):
    """Navigate and wait for the DOM, then up to 20s for full load. The theme dev proxy sometimes
    stalls on one asset, which would otherwise hang the whole suite."""
    response = page.goto(url, wait_until='domcontentloaded', timeout=120000)
    try:
        page.wait_for_load_state('load', timeout=20000)
    except Exception:
        pass
    return response


def ok(name, cond, detail=''):
    R.append((name, bool(cond), str(detail)))

GEOMETRY = """(i) => {
  const d = document.getElementById('Details-HeaderMenu-' + i), s = d.querySelector('summary'), card = d.querySelector('.th-dropdown');
  const c = card.getBoundingClientRect(), t = s.getBoundingClientRect(), h = document.querySelector('.header-wrapper').getBoundingClientRect();
  const rows = [...card.querySelectorAll('.header__menu-item')].map(a => { const r = a.getBoundingClientRect(), st = getComputedStyle(a);
    return [Math.round(r.height), st.fontFamily.split(',')[0].replace(/"/g, ''), st.fontSize]; });
  return { rtl: document.documentElement.dir === 'rtl', cardLeft: Math.round(c.left), cardRight: Math.round(c.right), width: Math.round(c.width),
    trigLeft: Math.round(t.left), trigRight: Math.round(t.right), gap: Math.round(c.top - h.bottom), rows,
    position: getComputedStyle(card).position, expanded: s.getAttribute('aria-expanded') };
}"""
STATE = "() => [1, 2].map(i => [document.getElementById('Details-HeaderMenu-' + i).open, document.querySelector('#Details-HeaderMenu-' + i + ' > summary').getAttribute('aria-expanded')])"
MAIN_TOP = "() => { const m = document.getElementById('MainContent'); return m ? Math.round(m.getBoundingClientRect().top) : location.href; }"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel='msedge')
    for lang, prefix in (('en', ''), ('ar', '/ar')):
        for w in (1024, 1440):
            tag = f'{lang} {w}px'
            ctx = b.new_context(viewport={'width': w, 'height': 900}); pg = ctx.new_page()
            goto(pg, base + prefix + '/collections/all'); pg.wait_for_timeout(800)
            pg.mouse.move(5, 880)
            ok(f'{tag}: no mega menu card in the desktop header', pg.locator('.header__inline-menu .mega-feature').count() == 0)
            main_before = pg.evaluate(MAIN_TOP)

            # Click opens, geometry.
            pg.click('#Details-HeaderMenu-1 > summary'); pg.wait_for_timeout(400)
            g = pg.evaluate(GEOMETRY, 1)
            aligned = abs(g['cardRight'] - g['trigRight']) <= 2 if g['rtl'] else abs(g['cardLeft'] - g['trigLeft']) <= 2
            ok(f'{tag}: click opens Shop as a compact card under its trigger (inline-start aligned)',
               g['expanded'] == 'true' and g['position'] == 'absolute' and aligned and 220 <= g['width'] <= 400, g)
            ok(f'{tag}: ~8px below the header edge', 6 <= g['gap'] <= 10, g['gap'])
            ok(f'{tag}: 44px rows in Nunito at body size', all(r[0] >= 44 and r[1] == 'Nunito' and r[2] == '15px' for r in g['rows']), g['rows'])
            ok(f'{tag}: no layout shift when open', pg.evaluate(MAIN_TOP) == main_before)
            if w == 1440:
                pg.screenshot(path=f'{out}/dropdown-shop-{w}-{lang}.jpg', type='jpeg', quality=72, clip={'x': 0, 'y': 0, 'width': w, 'height': 420})

            # Outside click closes.
            pg.mouse.click(5, 880); pg.wait_for_timeout(300)  # empty page gutter, not a link
            ok(f'{tag}: outside click closes, aria-expanded false', pg.evaluate(STATE)[0] == [False, 'false'], pg.evaluate(STATE))

            # Hover opens; one at a time; leaving closes; click keeps a hover-opened menu open.
            box = pg.locator('#Details-HeaderMenu-1 > summary').bounding_box()
            pg.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2); pg.wait_for_timeout(300)
            hover_open = pg.evaluate(STATE)[0]
            box2 = pg.locator('#Details-HeaderMenu-2 > summary').bounding_box()
            pg.mouse.move(box2['x'] + box2['width'] / 2, box2['y'] + box2['height'] / 2, steps=8); pg.wait_for_timeout(400)
            st = pg.evaluate(STATE)
            ok(f'{tag}: hover opens; moving to Learn leaves only Learn open', hover_open == [True, 'true'] and st == [[False, 'false'], [True, 'true']], st)
            pg.mouse.click(box2['x'] + box2['width'] / 2, box2['y'] + box2['height'] / 2); pg.wait_for_timeout(300)
            ok(f'{tag}: clicking a hover-opened trigger keeps it open', pg.evaluate(STATE)[1] == [True, 'true'])
            pg.mouse.move(5, 880); pg.wait_for_timeout(400)
            still_open = pg.evaluate(STATE)[1][0]
            pg.mouse.click(5, 880); pg.wait_for_timeout(300)
            pg.locator('#Details-HeaderMenu-2 > summary').hover(); pg.wait_for_timeout(300)
            pg.mouse.move(5, 880); pg.wait_for_timeout(500)
            ok(f'{tag}: a hover-opened menu closes when the pointer leaves (a clicked one stays)',
               still_open and pg.evaluate(STATE)[1] == [False, 'false'], pg.evaluate(STATE))

            # Keyboard: Enter opens, Tab into links, Escape closes and returns focus; Space opens; focus leaving closes.
            pg.focus('#Details-HeaderMenu-1 > summary'); pg.keyboard.press('Enter'); pg.wait_for_timeout(300)
            pg.keyboard.press('Tab'); pg.wait_for_timeout(150)
            in_card = pg.evaluate("() => !!document.activeElement.closest('#Details-HeaderMenu-1 .th-dropdown')")
            ring = pg.evaluate("() => getComputedStyle(document.activeElement).outlineStyle !== 'none'")
            pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
            back = pg.evaluate("() => document.activeElement.id === 'HeaderMenu-shop'")
            ok(f'{tag}: Enter opens, Tab reaches the first link (visible focus), Escape closes and returns focus',
               in_card and ring and back and pg.evaluate(STATE)[0] == [False, 'false'], (in_card, ring, back))
            pg.keyboard.press('Space'); pg.wait_for_timeout(300)
            space_open = pg.evaluate(STATE)[0] == [True, 'true']
            links = pg.locator('#Details-HeaderMenu-1 .th-dropdown a').count()
            for _ in range(links + 1):
                pg.keyboard.press('Tab'); pg.wait_for_timeout(80)
            pg.wait_for_timeout(200)
            ok(f'{tag}: Space opens; tabbing past the last link closes it', space_open and pg.evaluate(STATE)[0] == [False, 'false'], pg.evaluate(STATE))
            ctx.close()

    # Reduced motion: no open animation.
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce'); pg = ctx.new_page()
    goto(pg, base + '/collections/all'); pg.wait_for_timeout(500)
    pg.click('#Details-HeaderMenu-1 > summary'); pg.wait_for_timeout(50)
    anim = pg.evaluate("() => { const c = document.querySelector('#Details-HeaderMenu-1 .th-dropdown'); const s = getComputedStyle(c); return [s.animationName, s.opacity]; }")
    ok('reduced motion: the card appears without animation', anim[0] == 'none' and anim[1] == '1', anim)
    ctx.close()

    # Mobile drawer unchanged: still opens with its groups.
    ctx = b.new_context(viewport={'width': 390, 'height': 844}); pg = ctx.new_page()
    goto(pg, base + '/'); pg.wait_for_timeout(800)
    pg.click('header-drawer summary'); pg.wait_for_timeout(600)
    items = pg.locator('#menu-drawer .menu-drawer__menu > li').count()
    ok('mobile drawer still opens with the menu groups', pg.evaluate("() => document.querySelector('header-drawer details').hasAttribute('open')") and items >= 4, items)
    pg.screenshot(path=f'{out}/drawer-390-en.jpg', type='jpeg', quality=72)
    ctx.close()

    # --- One underline style per state (stitch replaces Dawn's underline): EN + /ar ---
    CHAIN = """(el) => { const s = el.matches('.th-stitch') ? el : el.querySelector('.th-stitch');
      if (!s) return { stitch: false };
      const drawn = parseFloat(getComputedStyle(s).backgroundSize) > 0;
      const chain = [s, ...s.querySelectorAll('*')];
      for (let a = s.parentElement; a && !a.matches('header, .header__inline-menu, body'); a = a.parentElement) chain.push(a);
      const deco = chain.filter(n => getComputedStyle(n).textDecorationLine !== 'none').map(n => n.tagName + '.' + (n.getAttribute('class') || '').split(' ')[0]);
      return { stitch: true, drawn, deco }; }"""
    for lang, prefix in (('en', ''), ('ar', '/ar')):
        for path, sel, states in (
            ('/pages/workshops', '.header__inline-menu a[aria-current="page"]', ('current', 'hover', 'focus')),
            ('/', '.header__inline-menu a.header__menu-item', ('rest', 'hover', 'focus')),
            ('/', '#Details-HeaderMenu-1 > summary', ('open',)),
            ('/collections/clothing', '#Details-HeaderMenu-1 > summary', ('current', 'hover')),
            ('/', '#Details-HeaderMenu-1 .header__submenu a', ('open-hover', 'open-focus')),
            ('/collections/clothing', '#Details-HeaderMenu-1 .header__submenu a[aria-current="page"]', ('open-current',)),
        ):
            ctx = b.new_context(viewport={'width': 1440, 'height': 900}); pg = ctx.new_page()
            goto(pg, base + prefix + path); pg.wait_for_timeout(600)
            for state in states:
                pg.mouse.move(2, 880); pg.wait_for_timeout(200)
                if state.startswith('open'):
                    pg.locator('#Details-HeaderMenu-1 > summary').click(); pg.wait_for_timeout(400)
                el = pg.locator(f'{sel} >> visible=true').first
                if state.endswith('hover'):
                    el.hover(); pg.wait_for_timeout(450)
                if state.endswith('focus'):
                    pg.keyboard.press('Shift'); el.focus(); pg.wait_for_timeout(450)
                r = el.evaluate(CHAIN)
                if state == 'rest':
                    # Guards the state selectors: a plain item at rest has neither underline.
                    ok(f'{lang} {path} {sel.split()[-1][:30]} [rest]: no stitch, no text-decoration',
                       r['stitch'] and not r['drawn'] and not r['deco'], r)
                    continue
                ok(f'{lang} {path} {sel.split()[-1][:30]} [{state}]: stitch drawn, no text-decoration anywhere along it',
                   r['stitch'] and r['drawn'] and not r['deco'], r)
                if state.startswith('open'):
                    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
            ctx.close()

    b.close()

for name, cond, detail in R:
    print('PASS' if cond else 'FAIL', name, '-', detail[:220])
print('summary', sum(c for _, c, _ in R), '/', len(R))
