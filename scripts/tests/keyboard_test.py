"""M2.1 Step 7: keyboard pass over the wired header, dropdown menus, mobile drawer and footer.

usage: python -X utf8 scripts/tests/keyboard_test.py BASE_URL OUT_DIR

Checks, in English and Arabic: the skip link is the first stop and moves focus to main; the Shop
dropdown opens with Enter, its first link is reachable, Escape closes it and focus returns
to Shop; every Tab stop over the first 60 has a visible focus indicator; the mobile drawer opens
from the keyboard and Escape closes it; the footer language selector opens with Enter and its
options are reachable. Requires Playwright + Microsoft Edge.
"""
import sys
from playwright.sync_api import sync_playwright

base, out = sys.argv[1], sys.argv[2]
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

# Follows focus into shadow DOM (shopify-account) and accepts a ring drawn on a close ancestor
# through :has(:focus-visible) (path cards, mega menu card: the whole card shows the ring).
RING = """() => { let e = document.activeElement; if (!e || e === document.body) return null;
  while (e.shadowRoot && e.shadowRoot.activeElement) e = e.shadowRoot.activeElement;
  const drawn = el => { const s = getComputedStyle(el), a = getComputedStyle(el, '::after');
    return (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0) || (s.boxShadow && s.boxShadow !== 'none')
      || (a.content !== 'none' && ((a.boxShadow && a.boxShadow !== 'none') || (a.outlineStyle !== 'none' && parseFloat(a.outlineWidth) > 0))); };
  const vis = e.getClientRects().length > 0;
  let ring = drawn(e);
  for (let up = e.parentElement, n = 0; !ring && up && n < 5; up = up.parentElement, n++) ring = drawn(up) && up.matches(':has(:focus-visible)');
  return { vis, ring, label: (e.getAttribute('aria-label') || e.innerText || e.value || '').trim().replace(/\\s+/g, ' ').slice(0, 30), tag: e.tagName } }"""
ACTIVE = "() => [document.activeElement.tagName, (document.activeElement.innerText || document.activeElement.getAttribute('aria-label') || '').trim().slice(0, 30), document.activeElement.id]"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel='msedge')
    for lang, prefix in (('en', ''), ('ar', '/ar')):
        pg = b.new_page(viewport={'width': 1440, 'height': 900})
        goto(pg, base + prefix + '/collections/all'); pg.wait_for_timeout(1000)

        pg.keyboard.press('Tab')
        first = pg.evaluate("() => document.activeElement.classList.contains('skip-to-content-link')")
        pg.keyboard.press('Enter'); pg.wait_for_timeout(300)
        in_main = pg.evaluate("() => !!document.activeElement.closest('main') || document.activeElement.id === 'MainContent'")
        ok(f'{lang}: skip link is the first stop and moves focus to main', first and in_main)

        summary = pg.locator('#Details-HeaderMenu-1 > summary')
        summary.focus(); pg.keyboard.press('Enter'); pg.wait_for_timeout(500)
        opened = pg.evaluate("() => document.getElementById('Details-HeaderMenu-1').open")
        reached = False
        for _ in range(12):
            pg.keyboard.press('Tab')
            if pg.evaluate("() => !!document.activeElement.closest('#Details-HeaderMenu-1 .header__submenu')"):
                reached = True; break
        shot_name = f'{out}/kbd-dropdown-1440-{lang}.png'
        pg.screenshot(path=shot_name, clip={'x': 0, 'y': 0, 'width': 1440, 'height': 440})
        pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
        closed = not pg.evaluate("() => document.getElementById('Details-HeaderMenu-1').open")
        back = pg.evaluate("() => document.activeElement === document.querySelector('#Details-HeaderMenu-1 > summary')")
        ok(f'{lang}: Shop dropdown opens with Enter, its first link reachable by Tab', opened and reached)
        ok(f'{lang}: Escape closes the dropdown and focus returns to Shop', closed and back, pg.evaluate(ACTIVE))

        goto(pg, base + prefix + '/'); pg.wait_for_timeout(1000)
        missing = []
        for i in range(60):
            pg.keyboard.press('Tab'); pg.wait_for_timeout(60)
            r = pg.evaluate(RING)
            if r and r['vis'] and not r['ring']:
                missing.append(f"{r['tag']} {r['label']}")
        ok(f'{lang}: first 60 Tab stops on the homepage all show a focus indicator', not missing, missing[:6])

        lang_btn = pg.locator('#FooterLanguageForm button.disclosure__button, #FooterLanguageForm .localization-form__select').first
        if lang_btn.count():
            lang_btn.focus(); pg.keyboard.press('Enter'); pg.wait_for_timeout(400)
            expanded = lang_btn.get_attribute('aria-expanded') == 'true'
            pg.keyboard.press('Tab'); pg.wait_for_timeout(150)
            option = pg.evaluate("() => !!document.activeElement.closest('#FooterLanguageForm') && document.activeElement !== document.querySelector('#FooterLanguageForm .disclosure__button')")
            names = pg.locator('#FooterLanguageForm .disclosure__list a, #FooterLanguageForm .disclosure__list button').all_inner_texts()
            pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
            ok(f'{lang}: footer language selector opens with Enter; options reachable (English / العربية)',
               expanded and option and any('English' in n for n in names) and any('العربية' in n for n in names), names)
        else:
            ok(f'{lang}: footer language selector present', False, 'not found')
        pg.close()

        pg = b.new_page(viewport={'width': 390, 'height': 844})
        goto(pg, base + prefix + '/'); pg.wait_for_timeout(1000)
        menu = pg.locator('header-drawer summary').first
        menu.focus(); pg.keyboard.press('Enter'); pg.wait_for_timeout(600)
        open_ = pg.evaluate("() => document.querySelector('header-drawer details').hasAttribute('open')")
        pg.keyboard.press('Tab'); pg.wait_for_timeout(150)
        inside = pg.evaluate("() => !!document.activeElement.closest('#menu-drawer, .menu-drawer')")
        pg.screenshot(path=f'{out}/kbd-drawer-390-{lang}.png')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(600)
        closed = not pg.evaluate("() => document.querySelector('header-drawer details').hasAttribute('open')")
        ok(f'{lang} 390px: mobile drawer opens with Enter, focus moves inside, Escape closes', open_ and inside and closed)
        pg.close()
    b.close()

for name, cond, detail in R:
    print('PASS' if cond else 'FAIL', name, '-', detail[:200])
print('summary', sum(c for _, c, _ in R), '/', len(R))
