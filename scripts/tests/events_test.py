"""Acceptance tests for M4 events: the events page and the workshop product template.

usage: python -X utf8 scripts/tests/events_test.py BASE_URL OUT_DIR [--page-view events] [--product-view workshop]
       [--empty-view NAME] [--preview-theme ID]
  BASE_URL        e.g. http://127.0.0.1:9393 (shopify theme dev) or the theme preview URL
  OUT_DIR         screenshots
  --page-view     alternate template for /pages/workshops until the page uses page.events ('' once assigned)
  --product-view  alternate template for event products until they use product.workshop ('' once assigned)
  --empty-view    optional page template whose collection is empty, to check the empty state
  --preview-theme run everything on the real store domain with this theme's preview (e.g. the
                  `shopify theme dev` development theme). Needed for the checkout flows, which
                  the local dev proxy cannot reach; BASE_URL is then ignored. Needs STORE_PW in
                  the environment for a password-protected store.

Seats are compared with docs/store-setup/workshops.csv (inventory is not exposed on the
storefront), so run it before real bookings change the counts. Checkout tests stop on the
checkout page and never pay. Requires Playwright + Microsoft Edge.
"""
import argparse, csv, os, re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument('base'); ap.add_argument('out')
ap.add_argument('--page-view', default='events'); ap.add_argument('--product-view', default='workshop')
ap.add_argument('--empty-view', default='')
ap.add_argument('--preview-theme', default='')
args = ap.parse_args()
STORE = 'https://tatreez-house.myshopify.com'
BASE, OUT = (STORE if args.preview_theme else args.base.rstrip('/')), args.out
view = lambda name, sep='?': f'{sep}view={name}' if name else ''
PAGE = '/pages/workshops' + view(args.page_view)
PRODUCT = lambda handle, extra='': f'/products/{handle}' + view(args.product_view) + (('&' if args.product_view else '?') + extra if extra else '')

R = []
def ok(name, cond, detail=''):
    R.append((name, None if cond is None else bool(cond), str(detail)))

csv_path = Path(__file__).resolve().parents[2] / 'docs/store-setup/workshops.csv'
SEATS = {}
for row in csv.DictReader(open(csv_path, encoding='utf-8')):
    SEATS[(row['URL handle'], row['Option1 value'])] = int(row['Inventory quantity'])

def shot(pg, name, **kw):
    try:
        pg.screenshot(path=f'{OUT}/{name}.jpg', type='jpeg', quality=70, timeout=60000, **kw)
    except Exception as e:
        print('NOTE screenshot skipped:', name, str(e)[:80])

ITEMS = """() => [...document.querySelectorAll('[data-event-item]')].map(li => ({
  hidden: li.hidden || getComputedStyle(li).display === 'none', type: li.dataset.eventType,
  start: li.querySelector('time.event-date-tile')?.getAttribute('datetime'),
  title: li.querySelector('.event-session__title')?.textContent.trim(),
  price: li.querySelector('.event-session__price')?.textContent.trim(),
  seats: li.querySelector('.event-session__seats')?.textContent.trim() || '',
  book: li.querySelector('.event-session__book')?.getAttribute('href') || '' }))"""
LAYOUT = """() => ({ overflow: document.documentElement.scrollWidth - innerWidth, dir: document.documentElement.dir || 'ltr',
  h1: [...document.querySelectorAll('h1')].filter(h => h.getClientRects().length).length })"""
DRAWER_OPEN = "() => document.querySelector('cart-drawer')?.classList.contains('active')"

def report():
    for name, cond, detail in R:
        print({True: 'PASS', False: 'FAIL', None: 'SKIP'}[cond], name, '-', detail[:220])
    print('summary', sum(c is True for _, c, _ in R), 'pass /', sum(c is False for _, c, _ in R), 'fail /', sum(c is None for _, c, _ in R), 'skip')
    return 0


def new_ctx(b, **kw):
    """Browser context; with --preview-theme it logs in (STORE_PW) and turns the theme preview on."""
    kw.setdefault('viewport', {'width': 1440, 'height': 1000})
    ctx = b.new_context(**kw)
    # Shopify's preview bar overlays the page and intercepts clicks; it is not part of the theme.
    ctx.add_init_script("""document.addEventListener('DOMContentLoaded', () => {
      const s = document.createElement('style'); s.textContent = '#PBarNextFrameWrapper{display:none!important}';
      document.head.appendChild(s); });""")
    if args.preview_theme:
        pg = ctx.new_page()
        if os.environ.get('STORE_PW'):
            pg.goto(STORE + '/password', wait_until='load', timeout=120000)
            if pg.locator('input[type="password"]').count():
                pg.fill('input[type="password"]', os.environ['STORE_PW'])
                with pg.expect_navigation(timeout=120000):
                    pg.press('input[type="password"]', 'Enter')
        pg.goto(f'{STORE}/?preview_theme_id={args.preview_theme}', wait_until='load', timeout=120000)
        pg.close()
    return ctx


def hide_preview_bar(pg):
    # Shopify's preview bar overlays the page and intercepts clicks; it is not part of the theme.
    pg.evaluate("() => document.getElementById('PBarNextFrameWrapper')?.remove()")


def circle_flow(pg):
    """Free circle: Reserve my free spot -> drawer -> $0 checkout (stops on the checkout page)."""
    pg.goto(BASE + PRODUCT('monthly-stitch-circle'), wait_until='load', timeout=120000); pg.wait_for_timeout(2000)
    hide_preview_bar(pg)
    label = pg.locator('.product-form__submit span').first.inner_text().strip()
    ok('circle: "Reserve my free spot", price "Free", no Buy it now',
       label == 'Reserve my free spot' and pg.locator('[id^="price-"]').first.inner_text().strip() == 'Free'
       and pg.locator('.shopify-payment-button').count() == 0, label)
    pg.click('.product-form__submit'); pg.wait_for_function(DRAWER_OPEN, timeout=30000); pg.wait_for_timeout(800)
    hide_preview_bar(pg)
    pg.click('#CartDrawer-Checkout')
    pg.wait_for_url(re.compile(r'/checkouts?/'), timeout=60000); pg.wait_for_timeout(4000)
    body = pg.locator('body').inner_text()
    ok('circle: reaches a $0 checkout, no payment required (not completed)',
       '$0.00' in body and 'No payment is required' in body, pg.url.split('?')[0])
    shot(pg, 'circle-checkout-1440')


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel='msedge')

    # ---------- Events page ----------
    ctx = new_ctx(b, viewport={'width': 1440, 'height': 1000}); pg = ctx.new_page()
    pg.goto(BASE + PAGE, wait_until='load', timeout=120000); pg.wait_for_timeout(800)
    items = pg.evaluate(ITEMS)
    now = datetime.now(timezone.utc)
    starts = [datetime.fromisoformat(i['start']) for i in items if i['start']]
    ok('events: sessions listed', len(items) > 0, len(items))
    ok('events: sorted by date', starts == sorted(starts), [s.isoformat() for s in starts])
    ok('events: no past dates', all(s > now for s in starts))
    circles = [i for i in items if i['type'] == 'circle']
    ok('events: free circle shows "Free" and "Reserve a free spot"', circles and all(i['price'] == 'Free' for i in circles)
       and all(pg.locator(f'[data-event-item][data-event-type="circle"] .event-session__book').nth(k).inner_text().startswith('Reserve a free spot') for k in range(len(circles))),
       [i['price'] for i in circles])
    mismatches = []
    for i in items:
        handle = re.search(r'/products/([^?]+)', i['book']).group(1) if i['book'] else ''
        local = datetime.fromisoformat(i['start']).strftime('%Y-%m-%d %H:%M')
        expected = SEATS.get((handle, local))
        want = f'Only {expected} seats left' if expected is not None and expected <= 3 else f'{expected} seats left'
        if expected is None or i['seats'] != want:
            mismatches.append((handle, local, i['seats'], want))
    ok('events: seats text matches the inventory (workshops.csv)', not mismatches, mismatches[:3])
    ok('events: booking links preselect the date (?variant=)', all('variant=' in i['book'] for i in items if i['book']))
    shot(pg, 'events-1440-en', full_page=True)

    # Filters with JS
    pg.click('[data-filter="workshop"]'); pg.wait_for_timeout(300)
    vis = [i for i in pg.evaluate(ITEMS) if not i['hidden']]
    ok('filter (JS): Workshops shows only workshops, URL ?type=workshop, aria-current',
       vis and all(i['type'] == 'workshop' for i in vis) and 'type=workshop' in pg.url
       and pg.get_attribute('[data-filter="workshop"]', 'aria-current') == 'true', (len(vis), pg.url))
    status = pg.locator('[data-filter-status]').inner_text()
    ok('filter (JS): result announced in the live region', str(len(vis)) in status, status)
    pg.click('[data-filter="circle"]'); pg.wait_for_timeout(300)
    vis = [i for i in pg.evaluate(ITEMS) if not i['hidden']]
    ok('filter (JS): Community circles shows only circles', vis and all(i['type'] == 'circle' for i in vis), len(vis))
    pg.click('[data-filter="all"]'); pg.wait_for_timeout(300)
    ok('filter (JS): All shows everything again, type removed from URL',
       all(not i['hidden'] for i in pg.evaluate(ITEMS)) and 'type=' not in pg.url)
    sep = '&' if '?' in PAGE else '?'
    pg.goto(BASE + PAGE + sep + 'type=circle', wait_until='load', timeout=120000); pg.wait_for_timeout(500)
    vis = [i for i in pg.evaluate(ITEMS) if not i['hidden']]
    ok('filter (JS): shared link ?type=circle opens filtered', vis and all(i['type'] == 'circle' for i in vis))
    ctx.close()

    ctx = new_ctx(b, viewport={'width': 1440, 'height': 1000}, java_script_enabled=False); pg = ctx.new_page()
    pg.goto(BASE + PAGE + sep + 'type=workshop', wait_until='load', timeout=120000)
    vis = [i for i in pg.evaluate(ITEMS) if not i['hidden']]
    ok('filter (no JS): falls back to showing every session', {i['type'] for i in vis} == {'workshop', 'circle'}, len(vis))
    ctx.close()

    if args.empty_view:
        ctx = new_ctx(b, viewport={'width': 1440, 'height': 1000}); pg = ctx.new_page()
        pg.goto(BASE + '/pages/workshops?view=' + args.empty_view, wait_until='load', timeout=120000)
        empty = pg.locator('.events-empty')
        ok('empty state: "New dates are coming soon." + newsletter, no sessions',
           empty.count() == 1 and 'New dates are coming soon.' in empty.inner_text() and empty.locator('input[type=email]').count() == 1
           and pg.locator('[data-event-item]').count() == 0)
        shot(pg, 'events-empty-1440-en', full_page=True)
        ctx.close()
    else:
        ok('empty state', None, 'no --empty-view given')

    # ---------- Workshop template ----------
    ctx = new_ctx(b, viewport={'width': 1440, 'height': 1000}); pg = ctx.new_page()
    pg.goto(BASE + '/cart/clear', wait_until='load', timeout=120000)
    handle = 'tatreez-foundations-workshop'
    pg.goto(BASE + PRODUCT(handle), wait_until='load', timeout=120000); pg.wait_for_timeout(1500)
    chips = pg.locator('[data-event-dates] input[type=radio]')
    upcoming = [d for (h, d) in SEATS if h == handle and datetime.strptime(d, '%Y-%m-%d %H:%M') > datetime.now()]
    ok('workshop: only upcoming dates as chips', chips.count() == len(upcoming), (chips.count(), upcoming))
    ok('workshop: legend "Choose a date"', pg.locator('[data-event-dates] legend').inner_text().strip().lower() == 'choose a date')
    before = {'url': pg.url, 'gcal': pg.get_attribute('.event-calendar a', 'href'), 'ics': pg.get_attribute('[data-ics]', 'data-start'),
              'seats': pg.locator('.event-session-info__seats').inner_text()}
    pg.locator('[data-event-dates] label').nth(1).click()
    pg.wait_for_function("(old) => location.href !== old", arg=before['url'], timeout=30000); pg.wait_for_timeout(1200)
    after = {'url': pg.url, 'gcal': pg.get_attribute('.event-calendar a', 'href'), 'ics': pg.get_attribute('[data-ics]', 'data-start'),
             'seats': pg.locator('.event-session-info__seats').inner_text(), 'date': pg.locator('.event-session-info__date').inner_text()}
    ok('workshop: choosing a date updates ?variant=', 'variant=' in after['url'] and after['url'] != before['url'], after['url'])
    ok('workshop: calendar links follow the date', after['gcal'] != before['gcal'] and after['ics'] != before['ics']
       and '20261121T180000' in after['gcal'] and 'ctz=Asia%2FHebron' in after['gcal'], (after['ics'], after['gcal'][:140]))
    ok('workshop: seats and selected date follow the date', '21 Nov' in after['date'] and after['seats'].endswith('seats left'), after)
    ok('workshop: button label stays "Book a seat" after the change', pg.locator('.product-form__submit span').first.inner_text().strip() == 'Book a seat')
    with pg.expect_download(timeout=15000) as dl:
        pg.click('[data-ics]')
    ics = Path(dl.value.path()).read_text(encoding='utf-8')
    ok('workshop: .ics downloads with the right UTC start (18:00 +02:00 = 16:00Z)', 'DTSTART:20261121T160000Z' in ics and 'SUMMARY:Tatreez Foundations' in ics, ics[:200])
    shot(pg, 'workshop-1440-en', full_page=True)

    pg.click('.product-form__submit')
    pg.wait_for_function(DRAWER_OPEN, timeout=30000); pg.wait_for_timeout(800)
    drawer = pg.locator('cart-drawer').inner_text()
    ok('workshop: "Book a seat" opens the drawer with the formatted date', 'Sat, 21 Nov 2026 · 6:00 PM' in drawer and '2026-11-21 18:00' not in drawer, drawer[:300])
    ok('cart drawer: no shipping wording when nothing ships', 'shipping' not in pg.locator('cart-drawer .tax-note').inner_text().lower(),
       pg.locator('cart-drawer .tax-note').inner_text())
    shot(pg, 'workshop-drawer-1440-en')
    pg.goto(BASE + '/cart', wait_until='load', timeout=120000)
    ok('cart page: formatted date, no shipping wording', 'Sat, 21 Nov 2026' in pg.locator('main').inner_text()
       and 'shipping' not in pg.locator('.tax-note').first.inner_text().lower())

    ctx.close()

    # ---------- Arabic, widths, keyboard ----------
    for lang, prefix in (('en', ''), ('ar', '/ar')):
        for w in (360, 768, 1440):
            ctx = new_ctx(b, viewport={'width': w, 'height': 900}); pg = ctx.new_page()
            for name, path in (('events', PAGE), ('workshop', PRODUCT('compose-your-own-panel-workshop'))):
                pg.goto(BASE + prefix + path, wait_until='load', timeout=120000); pg.wait_for_timeout(800)
                m = pg.evaluate(LAYOUT)
                want = 'rtl' if lang == 'ar' else 'ltr'
                ok(f'{lang} {w}px {name}: no horizontal scroll, dir {want}, one h1', m['overflow'] <= 0 and m['dir'] == want and m['h1'] == 1, m)
                if lang == 'ar' and w == 1440:
                    text = pg.locator('main').inner_text()
                    ok(f'ar {name}: Arabic date names and "بتوقيت فلسطين"', 'بتوقيت فلسطين' in text and any(mn in text for mn in ('نوفمبر', 'ديسمبر', 'يناير')), text[:120])
                if w in (360, 1440):
                    shot(pg, f'{name}-{w}-{lang}', full_page=(w == 360))
            ctx.close()

    ctx = new_ctx(b, viewport={'width': 1440, 'height': 1000}); pg = ctx.new_page()
    pg.goto(BASE + '/cart/clear', wait_until='load', timeout=120000)
    pg.goto(BASE + PRODUCT('compose-your-own-panel-workshop'), wait_until='load', timeout=120000); pg.wait_for_timeout(1500)
    pg.locator('[data-event-dates] input:checked').focus()
    pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(1500)
    checked = pg.evaluate("() => document.querySelector('[data-event-dates] input:checked')?.value")
    focus_ok = pg.evaluate("() => !!document.activeElement.closest('[data-event-dates]')")
    for _ in range(25):
        pg.keyboard.press('Tab')
        if pg.evaluate("() => document.activeElement.classList.contains('product-form__submit')"):
            break
    on_button = pg.evaluate("() => document.activeElement.classList.contains('product-form__submit')")
    pg.keyboard.press('Enter')
    try:
        pg.wait_for_function(DRAWER_OPEN, timeout=30000); drawer_open = True
    except Exception:
        drawer_open = False
    ok('keyboard: arrow keys pick a date, Tab reaches "Book a seat", Enter books (drawer)',
       checked and checked.startswith('2026-12-12') and focus_ok and on_button and drawer_open, (checked, on_button, drawer_open))
    ctx.close()
    # Cards: next date + "From"/"Free", and Choose options opens the quick-add modal with date chips.
    ctx = new_ctx(b); pg = ctx.new_page()
    pg.goto(BASE + '/collections/events', wait_until='load', timeout=120000); pg.wait_for_timeout(1000)
    cards = pg.evaluate("""() => [...document.querySelectorAll('.product-card-wrapper')].map(c => ({
        title: c.querySelector('.card__heading a')?.textContent.trim(), next: c.querySelector('.card-event__next')?.textContent.trim(),
        price: c.querySelector('.card-event__price')?.textContent.trim(), badges: c.querySelector('.card-badges')?.textContent.trim() || '' }))""")
    ok('cards: next date and "From $45" / "Free", no "Instant download" badge',
       cards and all(c['next'] and c['next'].startswith('Next:') and (c['price'] == 'Free' or c['price'].startswith('From $')) for c in cards)
       and not any('Instant download' in c['badges'] for c in cards), cards)
    card = pg.locator('.product-card-wrapper:has(a[href*="compose-your-own-panel-workshop"])').first
    card.locator('.card-action').click()
    try:
        pg.wait_for_selector('quick-add-modal[open] [data-event-dates] label', timeout=30000); pg.wait_for_timeout(600)
        chip_texts = pg.locator('quick-add-modal[open] [data-event-dates] label').all_inner_texts()
        ok('cards: Choose options opens the quick-add modal with formatted date chips',
           len(chip_texts) == 2 and all('·' in c and 'seats left' in c for c in chip_texts), chip_texts)
        shot(pg, 'quick-add-modal-1440-en')
    except Exception as e:
        ok('cards: Choose options opens the quick-add modal with formatted date chips', False, str(e)[:160])
    ctx.close()

    # ---------- Checkout flows last (they leave the dev proxy for the real checkout) ----------
    if not args.preview_theme:
        ok('workshop: "Buy it now" reaches checkout', None, 'needs --preview-theme')
        ok('circle: $0 checkout', None, 'needs --preview-theme')
        b.close()
        raise SystemExit(report())
    ctx = new_ctx(b); pg = ctx.new_page()
    pg.goto(BASE + '/cart/clear', wait_until='load', timeout=120000)
    pg.goto(BASE + PRODUCT(handle), wait_until='load', timeout=120000); pg.wait_for_timeout(3000)
    hide_preview_bar(pg)
    buy = pg.locator('.shopify-payment-button__button--unbranded, .shopify-payment-button button').first
    if buy.count():
        buy.click()
        try:
            pg.wait_for_url(re.compile(r'/checkouts?/'), timeout=60000)
            ok('workshop: "Buy it now" reaches checkout', True, pg.url.split('?')[0])
        except Exception as e:
            ok('workshop: "Buy it now" reaches checkout', False, str(e)[:120])
    else:
        ok('workshop: "Buy it now" reaches checkout', False, 'dynamic checkout button not rendered')
    ctx.close()

    # Free circle: $0 checkout (stop on the checkout page).
    ctx = new_ctx(b); pg = ctx.new_page()
    pg.goto(BASE + '/cart/clear', wait_until='load', timeout=120000)
    try:
        circle_flow(pg)
    except Exception as e:
        ok('circle: $0 booking flow', False, f'{e}'[:160] + ' | ' + pg.url)
        shot(pg, 'circle-failure')
    ctx.close()
    b.close()

report()
