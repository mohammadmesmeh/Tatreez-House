"""Acceptance tests for the product card actions (M2.1 Step 3) and the grids (Step 4).

usage: python -X utf8 scripts/tests/cards_grids_test.py BASE_URL OUT_DIR
  BASE_URL  e.g. http://127.0.0.1:9393 (shopify theme dev) or the theme preview URL
  OUT_DIR   where screenshots are written

Step 3: one action baseline per row with mixed cards, "Add to cart" -> cart drawer, "Choose
options" -> quick-add modal (focus inside, trapped, Escape, focus returns), keyboard order.
Step 4: mobile "auto" columns, compact cards, homepage swipe carousels, quick add in search,
related products and after a Section Rendering API refresh (sort), rating empty states.
Assumes the demo catalogue (docs/store-setup/products.csv). Requires Playwright + Microsoft Edge.
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
    """cond None = SKIP (the store has no product in the state the check needs)."""
    R.append((name, None if cond is None else bool(cond), str(detail)))

ROWS = """() => { const rows = {};
  for (const c of document.querySelectorAll('#product-grid .product-card-wrapper')) {
    const card = c.getBoundingClientRect(), btn = c.querySelector('.card-action').getBoundingClientRect();
    (rows[Math.round(card.top)] ||= []).push([Math.round(btn.top), Math.round(card.height)]);
  }
  return Object.values(rows); }"""
COLUMNS = "() => new Set([...document.querySelectorAll('#product-grid > li')].map(li => Math.round(li.getBoundingClientRect().left))).size"
MODAL_OPEN = "() => !!document.querySelector('quick-add-modal[open]')"
FOCUS_IN_MODAL = "() => !!document.activeElement.closest('quick-add-modal[open]')"
DRAWER_OPEN = "() => document.querySelector('cart-drawer')?.classList.contains('active')"

def shot(pg, name, **kw):
    """Screenshots are evidence, not checks: a slow page must not abort the run."""
    try:
        pg.screenshot(path=f'{out}/{name}.jpg', type='jpeg', quality=72, timeout=60000, **kw)
    except Exception as e:
        print('NOTE screenshot skipped:', name, str(e)[:80])

def card(pg, handle):
    return pg.locator(f'.product-card-wrapper:has(a[href*="/products/{handle}"])').first

def open_options_by_keyboard(pg, scope, label):
    """Focus the card's Choose options button, press Enter, check the modal and close it again."""
    btn = scope.locator('.card-action').first
    btn.focus()
    pg.keyboard.press('Enter')
    pg.wait_for_function(MODAL_OPEN, timeout=30000)
    pg.wait_for_selector('quick-add-modal[open] [name="add"]', timeout=30000)
    pg.wait_for_timeout(400)
    ok(f'{label}: Choose options opens the modal, focus inside', pg.evaluate(FOCUS_IN_MODAL))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
    returned = pg.evaluate("() => document.activeElement.classList.contains('card-action')")
    ok(f'{label}: Escape closes, focus returns to the button', not pg.evaluate(MODAL_OPEN) and returned)

def exercise(pg, scope, label):
    """Run the card's action by keyboard: Choose options -> modal, Add to cart -> drawer."""
    if scope.locator('modal-opener').count():
        open_options_by_keyboard(pg, scope, label)
    elif scope.locator('product-form').count():
        scope.locator('.card-action').focus(); pg.keyboard.press('Enter')
        pg.wait_for_function(DRAWER_OPEN, timeout=30000); pg.wait_for_timeout(600)
        ok(f'{label}: Add to cart (keyboard) opens the drawer', True)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
    else:
        ok(f'{label}: card action works', None, 'only sold-out products here')

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel='msedge')

    # --- Step 3: mixed rows on one baseline (patterns + garments + bags + home in /collections/all) ---
    for w in (1440, 768, 430):
        ctx = b.new_context(viewport={'width': w, 'height': 1000}); pg = ctx.new_page()
        goto(pg, base + '/collections/all'); pg.wait_for_timeout(800)
        rows = pg.evaluate(ROWS)
        multi = [r for r in rows if len(r) > 1]
        aligned = all(max(x[0] for x in r) - min(x[0] for x in r) <= 1 for r in multi)
        equal = all(max(x[1] for x in r) - min(x[1] for x in r) <= 1 for r in multi)
        ok(f'{w}px: action buttons share one baseline per row, cards equal height', aligned and equal, rows)
        shot(pg, f'cards-all-{w}', full_page=True)
        ctx.close()

    # Products are picked by their live state (the catalogue's inventory can change in the admin).
    ctx = b.new_context(viewport={'width': 1440, 'height': 1000}); pg = ctx.new_page()
    products = pg.request.get(base + '/products.json').json()['products']
    avail = lambda pr: any(v['available'] for v in pr['variants'])
    pick = lambda f: next((pr for pr in products if f(pr)), None)
    single = pick(lambda pr: avail(pr) and len(pr['variants']) == 1)
    multi = pick(lambda pr: avail(pr) and len(pr['variants']) > 1)
    sold = pick(lambda pr: not avail(pr))
    print('NOTE products used: single', single and single['handle'], '| multi', multi and multi['handle'], '| sold out', sold and sold['handle'])

    goto(pg, base + '/collections/all'); pg.wait_for_timeout(800)
    expected = {pr['handle']: ('Add to cart' if len(pr['variants']) == 1 else 'Choose options') if avail(pr) else 'Sold out' for pr in products}
    actual = {h: card(pg, h).locator('.card-action .card-action__label').inner_text().strip() for h in expected}
    ok('every card: "Add to cart" (1 variant) / "Choose options" (several) / "Sold out"', actual == expected,
       {h: a for h, a in actual.items() if a != expected[h]} or 'all match')
    if sold:
        btn = card(pg, sold['handle']).locator('.card-action')
        ok('sold out: the button is disabled, row keeps its place', btn.is_disabled() and btn.is_visible(), sold['handle'])
    else:
        ok('sold out: the button is disabled', None, 'no sold-out product in the store')
    anyc = card(pg, (multi or single or products[0])['handle'])
    name = anyc.locator('.card-action').evaluate(
        "b => b.getAttribute('aria-labelledby').split(' ').map(id => document.getElementById(id).textContent.trim()).join(' ')")
    ok('accessible name = label + product title', name.endswith(anyc.locator('.card__heading a').first.inner_text().strip()) and len(name.split()) > 2, name)
    # Disabled "Sold out" buttons keep Dawn's 50% opacity (WCAG 1.4.3 exempts inactive controls).
    vis = pg.evaluate("() => [...document.querySelectorAll('.card-action')].every(b => { const s = getComputedStyle(b); return s.opacity === (b.disabled ? '0.5' : '1') && s.visibility === 'visible'; })")
    ok('actions visible without hover', vis)
    ok('no rating markup on cards without review data', pg.locator('.product-card-wrapper .rating-stars').count() == 0)
    ok('no chips / inline forms left on cards', pg.locator('.product-card-wrapper .variant-chips, .product-card-wrapper card-variant-picker').count() == 0)

    # Keyboard order inside a card: title link -> action button (skipped by a disabled button).
    c = card(pg, (multi or single)['handle'])
    c.locator('.card__heading a >> visible=true').first.focus(); pg.keyboard.press('Tab')
    ok('Tab from the card title lands on its action button',
       pg.evaluate("() => document.activeElement.classList.contains('card-action')"))

    # Add to cart (single variant) -> drawer.
    if single:
        goto(pg, base + '/cart/clear')
        goto(pg, base + '/collections/all'); pg.wait_for_timeout(800)
        url = pg.url
        c = card(pg, single['handle']); c.locator('.card-action').click()
        pg.wait_for_function(DRAWER_OPEN, timeout=30000); pg.wait_for_timeout(800)
        status = c.locator('[data-card-quick-add-status]').text_content() or ''
        ok('Add to cart opens the cart drawer without a reload', pg.url == url and single['title'][:12] in pg.locator('cart-drawer').inner_text())
        ok('live region announces "added"', 'added' in status.lower(), status)
        ok('focus moves into the drawer', pg.evaluate("() => !!document.activeElement.closest('cart-drawer')"))
        shot(pg, f'cards-add-drawer-1440')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(600)
        ok('Escape closes the drawer', not pg.evaluate(DRAWER_OPEN))
    else:
        ok('Add to cart opens the cart drawer', None, 'no available single-variant product')

    # Choose options -> modal, focus trap, add from the modal.
    if multi:
        c = card(pg, multi['handle'])
        open_options_by_keyboard(pg, c, 'collection')
        c.locator('.card-action').click()
        pg.wait_for_selector('quick-add-modal[open] [name="add"]', timeout=30000); pg.wait_for_timeout(500)
        trapped = True
        for _ in range(30):
            pg.keyboard.press('Tab')
            if not pg.evaluate(FOCUS_IN_MODAL):
                trapped = False; break
        ok('Tab stays inside the modal (30 presses)', trapped)
        shot(pg, f'cards-modal-1440')
        pg.locator('quick-add-modal[open] [name="add"]').first.click()
        pg.wait_for_function(DRAWER_OPEN, timeout=30000); pg.wait_for_timeout(800)
        ok('Add to cart in the modal opens the drawer with the product', multi['title'][:12] in pg.locator('cart-drawer').inner_text())
    else:
        ok('Choose options opens the quick-add modal', None, 'no available multi-variant product')
    ctx.close()

    # --- Step 4: mobile auto columns + compact cards ---
    expect = {360: 1, 430: 1, 600: 2, 768: 3}
    for w, n in expect.items():
        ctx = b.new_context(viewport={'width': w, 'height': 900}); pg = ctx.new_page()
        goto(pg, base + '/collections/all'); pg.wait_for_timeout(600)
        cols = pg.evaluate(COLUMNS)
        info = card(pg, single['handle']).evaluate("""c => { const full = c.querySelector('.card-action__label'), short = c.querySelector('.card-action__label--short');
            return { width: Math.round(c.getBoundingClientRect().width), fullVisible: full.getBoundingClientRect().width > 2,
                     shortVisible: getComputedStyle(short).display !== 'none', overflow: document.documentElement.scrollWidth > innerWidth } }""")
        compact = w == 600
        blank = pg.evaluate("() => [...document.querySelectorAll('.card-action')].filter(b => b.innerText.trim() === '').length")
        ok(f'{w}px: every card action shows visible text (incl. Sold out)', blank == 0, f'{blank} blank')
        ok(f'{w}px: {n} column(s), {"compact" if compact else "full"} labels, no horizontal scroll',
           cols == n and info['fullVisible'] != compact and info['shortVisible'] == compact and not info['overflow'], {'cols': cols, **info})
        if w in (360, 600):
            shot(pg, f'cards-all-{w}', full_page=True)
        ctx.close()

    # --- Step 4: homepage swipe carousels ---
    for w in (360, 390):
        ctx = b.new_context(viewport={'width': w, 'height': 844}); pg = ctx.new_page()
        goto(pg, base + '/'); pg.wait_for_timeout(800)
        lists = pg.evaluate("""() => [...document.querySelectorAll('.th-swipe-mobile .product-grid')].map(ul => { const li = ul.querySelector('li');
            return { snap: getComputedStyle(ul).scrollSnapType, scrollable: ul.scrollWidth > ul.clientWidth + 10, tab: ul.tabIndex,
                     visible: +[...ul.children].reduce((n, el) => { const r = el.getBoundingClientRect();
                       return n + Math.max(0, Math.min(r.right, innerWidth) - Math.max(r.left, 0)) / r.width; }, 0).toFixed(2) } })""")
        good = len(lists) >= 2 and all(l['snap'].split()[0] in ('x', 'inline') and l['scrollable'] and l['tab'] == 0 and 1.15 <= l['visible'] <= 1.4 for l in lists)
        ok(f'{w}px: homepage product rows are snap carousels (~1.25 cards, focusable)', good, lists)
        ul = pg.locator('.th-swipe-mobile .product-grid').first
        ul.scroll_into_view_if_needed(); ul.focus(); before = ul.evaluate('e => e.scrollLeft')
        pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(700)
        blank = pg.evaluate("() => [...document.querySelectorAll('.th-swipe-mobile .card-action')].filter(b => b.innerText.trim() === '').length")
        ok(f'{w}px: carousel card actions show visible text', blank == 0, f'{blank} blank')
        ok(f'{w}px: arrow key scrolls the focused carousel', ul.evaluate('e => e.scrollLeft') != before)
        ul.evaluate('e => window.scrollBy(0, e.getBoundingClientRect().top - 120)'); pg.wait_for_timeout(300)
        shot(pg, f'home-carousel-{w}')
        ctx.close()

    # --- Step 4: quick add in search, related products, after Section Rendering ---
    ctx = b.new_context(viewport={'width': 1440, 'height': 1000}); pg = ctx.new_page()
    target = multi or single
    goto(pg, base + '/search?type=product&q=' + target['title'].split()[0]); pg.wait_for_timeout(800)
    ok('search: results have card actions', pg.locator('#product-grid .card-action').count() >= 1)
    exercise(pg, card(pg, target['handle']), 'search')

    goto(pg, base + '/collections/all'); pg.wait_for_timeout(800)
    pg.evaluate("() => FacetFiltersForm.renderPage('sort_by=price-descending')")
    pg.wait_for_function("() => location.search.includes('price-descending') && !document.querySelector('.collection.loading')", timeout=30000)
    pg.wait_for_timeout(1200)
    exercise(pg, card(pg, target['handle']), 'after sort (Section Rendering API)')

    goto(pg, base + '/products/' + target['handle'])
    ok('product page: one h1', pg.locator('h1').count() == 1)
    empty = pg.locator('.product__info-container .rating-stars').inner_text() if pg.locator('.product__info-container .rating-stars').count() else ''
    ok('product page: rating empty state "No reviews yet"', 'No reviews yet' in empty, empty)
    pg.mouse.wheel(0, 4000); pg.wait_for_timeout(500)
    pg.locator('product-recommendations').scroll_into_view_if_needed()
    try:
        pg.wait_for_selector('product-recommendations .card-action', timeout=20000)
        rel = pg.locator('product-recommendations .product-card-wrapper')
        ok('related products: cards with actions', rel.count() >= 1, rel.count())
        for i in range(rel.count()):
            if rel.nth(i).locator('modal-opener, product-form').count():
                exercise(pg, rel.nth(i), 'related products'); break
        else:
            ok('related products: card action works', None, 'only sold-out recommendations')
        shot(pg, f'related-1440', full_page=True)
    except Exception as e:
        ok('related products: cards with actions', False, f'no recommendations rendered: {e}'[:160])
    ctx.close()

    # --- QA round 1, issues 1-3: card title underline, toolbar alignment, merchant text direction ---
    TITLE = """(handle) => { const c = [...document.querySelectorAll('.product-card-wrapper')].find(c => c.querySelector('a[href*="/products/' + handle + '"]'));
      const a = [...c.querySelectorAll('.card__heading a')].find(x => x.getClientRects().length), s = a.querySelector('.card__title-text');
      const as = getComputedStyle(a), ss = getComputedStyle(s);
      return { linkDeco: as.textDecorationLine, spanSize: ss.backgroundSize, clone: ss.boxDecorationBreak || ss.webkitBoxDecorationBreak,
               spanW: Math.round(s.getBoundingClientRect().width), linkW: Math.round(a.getBoundingClientRect().width), dir: s.getAttribute('dir'),
               display: ss.display } }"""
    TOOLBAR = """() => { const q = s => document.querySelector(s); const cy = e => { const r = e.getBoundingClientRect(); return Math.round(r.top + r.height / 2); };
      const sel = q('.facet-filters__sort'), caret = q('.facet-filters__field .icon-caret'), count = q('.product-count');
      const ctx = document.createElement('canvas').getContext('2d'); const st = getComputedStyle(sel); ctx.font = `${st.fontWeight} ${st.fontSize} ${st.fontFamily}`;
      const textW = ctx.measureText(sel.options[sel.selectedIndex].text).width; const sr = sel.getBoundingClientRect(), cr = caret.getBoundingClientRect();
      const rtl = document.documentElement.dir === 'rtl';
      const gap = rtl ? Math.round((sr.right - textW) - cr.right) : Math.round(cr.left - (sr.left + textW));
      return { centres: [q('.facets__heading'), q('.facets__summary'), q('.facet-filters__label'), sel, count].map(cy), gap,
               countAfterSort: rtl ? count.getBoundingClientRect().right <= sr.left : count.getBoundingClientRect().left >= sr.right } }"""
    for lang, prefix in (('en', ''), ('ar', '/ar')):
        for w in (768, 1024, 1440):
            ctx = b.new_context(viewport={'width': w, 'height': 900}); pg = ctx.new_page()
            goto(pg, base + prefix + '/collections/all'); pg.wait_for_timeout(1500)
            tb = pg.evaluate(TOOLBAR)
            ok(f'QA2 {lang} {w}px: toolbar items centred on one line, count grouped after Sort, chevron right after the text',
               max(tb['centres']) - min(tb['centres']) <= 1 and tb['countAfterSort'] and 0 <= tb['gap'] <= 16, tb)
            if w == 1440:
                c = pg.locator('.product-card-wrapper:has(a[href*="tatreez-starter-pattern-bundle"])').first
                c.scroll_into_view_if_needed(); c.locator('.card__heading a >> visible=true').first.hover(); pg.wait_for_timeout(500)
                ti = pg.evaluate(TITLE, 'tatreez-starter-pattern-bundle')
                ok(f'QA1 {lang}: hovered title has one underline (stitched, under the words, per line)',
                   ti['linkDeco'] == 'none' and ti['spanSize'].startswith('100%') and ti['clone'] == 'clone'
                   and ti['display'] == 'inline' and ti['spanW'] < ti['linkW'], ti)
                ok(f'QA3 {lang}: card titles carry dir="auto"', ti['dir'] == 'auto', ti['dir'])
            ctx.close()

    b.close()

for name, cond, detail in R:
    print({True: 'PASS', False: 'FAIL', None: 'SKIP'}[cond], name, '-', detail[:200])
print('summary', sum(c is True for _, c, _ in R), 'pass /', sum(c is False for _, c, _ in R), 'fail /', sum(c is None for _, c, _ in R), 'skip')
