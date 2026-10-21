"""Acceptance tests for sections/hero-slideshow.liquid (M2.1).

usage: python -X utf8 scripts/tests/hero_slideshow_test.py BASE_URL OUT_DIR
  BASE_URL  e.g. http://127.0.0.1:9393 (shopify theme dev) or the theme preview URL
  OUT_DIR   where screenshots are written

Covers autoplay + loop, progress state, inert slides, live region, heading rule, pause by button /
hover / focus, arrow keys, transparent header (top / scrolled / other pages), reduced motion,
JavaScript disabled, and content alignment with the page container at 360-1920 px in LTR and
real RTL (/ar). Requires Playwright and Microsoft Edge (channel msedge).
STATUS: written in M2.1, NOT YET RUN — the store became unavailable before the first run.
"""
import sys
from playwright.sync_api import sync_playwright

base, out = sys.argv[1], sys.argv[2]
R = []
def ok(name, cond, detail=''):
    R.append((name, bool(cond), str(detail)))

ACTIVE = "() => [...document.querySelectorAll('[data-slide]')].findIndex(s => s.classList.contains('is-active'))"
STATE = """() => { const s=[...document.querySelectorAll('[data-slide]')], st=[...document.querySelectorAll('[data-step]')];
  return { active: s.findIndex(x=>x.classList.contains('is-active')), inert: s.map(x=>x.inert), current: st.map(x=>x.getAttribute('aria-current')),
           done: st.map(x=>x.classList.contains('is-done')), pressed: document.querySelector('[data-toggle]')?.getAttribute('aria-pressed'),
           live: document.querySelector('[data-slides]').getAttribute('aria-live') } }"""

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel='msedge')

    # --- Autoplay, loop, progress, inert, live region (normal motion) ---
    # Timing is measured from the timer's own animationstart, not from the load event (a slow dev
    # proxy can fire load seconds after the slideshow started). The viewport is taller than the
    # hero so the pointer can rest outside it (hovering pauses autoplay by design).
    ctx = b.new_context(viewport={'width': 1440, 'height': 1400}); pg = ctx.new_page()
    pg.add_init_script("""
      window.__hs = { starts: [], changes: [] };
      document.addEventListener('animationstart', e => { if (e.animationName === 'heroTimer') window.__hs.starts.push(performance.now()); }, true);
      new MutationObserver(() => {
        const s = [...document.querySelectorAll('[data-slide]')]; if (!s.length) return;
        const i = s.findIndex(x => x.classList.contains('is-active'));
        const log = window.__hs.changes; if (!log.length || log[log.length - 1][1] !== i) log.push([performance.now(), i]);
      }).observe(document, { subtree: true, attributes: true, attributeFilter: ['class'] });
    """)
    pg.goto(base + '/', wait_until='domcontentloaded', timeout=120000)
    pg.mouse.move(5, 1390)
    pg.wait_for_function('window.__hs.starts.length > 0', timeout=60000)
    s0 = pg.evaluate(STATE)
    ok('starts on slide 1, others inert', s0['active'] == 0 and s0['inert'] == [False, True, True], s0)
    ok('live region off while autoplaying', s0['live'] == 'off', s0['live'])
    pg.wait_for_function('window.__hs.changes.filter(c => c[1] === 0).length >= 2', timeout=40000)
    log = pg.evaluate('window.__hs')
    first_start = log['starts'][0]
    seq = [c[1] for c in log['changes']]
    times = [round((c[0] - first_start) / 1000, 2) for c in log['changes']]
    gaps = [round(times[i + 1] - times[i], 2) for i in range(1, len(times) - 1)]
    ok('autoplay order 1 -> 2 -> 3 -> 1 (infinite loop)', seq[:4] == [0, 1, 2, 0], seq)
    ok('each slide shows ~6s (5.7-6.6s)', times[1] and 5.7 <= times[1] <= 6.6 and all(5.7 <= g <= 6.6 for g in gaps[:2]), {'first': times[1], 'gaps': gaps})
    s1 = pg.evaluate(STATE)
    ok('progress: current step marked, earlier steps full', s1['current'][s1['active']] == 'true' and all(s1['done'][:s1['active']]), s1)
    # headings
    hs = pg.evaluate("() => ({ h1: document.querySelectorAll('h1').length, heroH2: document.querySelectorAll('[data-slide] h2').length, heroP: document.querySelectorAll('[data-slide] p.hero-slide__heading').length })")
    ok('one h1, one hero h2, other slides use <p>', hs['h1'] == 1 and hs['heroH2'] == 1 and hs['heroP'] == 2, hs)
    # pause button
    pg.click('[data-toggle]'); pg.mouse.move(5, 1390)
    before = pg.evaluate(ACTIVE); pg.wait_for_timeout(7500)
    ok('pause button: aria-pressed true, no change for 7.5s', pg.evaluate(STATE)['pressed'] == 'true' and pg.evaluate(ACTIVE) == before)
    ok('live region polite when paused', pg.evaluate(STATE)['live'] == 'polite')
    pg.click('[data-toggle]'); pg.mouse.move(5, 1390)
    ok('play again: aria-pressed false', pg.evaluate(STATE)['pressed'] == 'false')
    # hover pause
    pg.mouse.move(720, 400); a = pg.evaluate(ACTIVE); pg.wait_for_timeout(7500)
    ok('hover pauses autoplay', pg.evaluate(ACTIVE) == a)
    pg.mouse.move(5, 1390)
    # keyboard: focus a step, arrow keys
    cur = pg.evaluate(ACTIVE)
    pg.focus(f'[data-step] >> nth={cur}'); pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(300)
    ok('ArrowRight moves to the next slide and focus follows', pg.evaluate(ACTIVE) == (cur + 1) % 3 and pg.evaluate("document.activeElement.getAttribute('aria-current')") == 'true', (cur, pg.evaluate(ACTIVE)))
    pg.keyboard.press('End'); pg.wait_for_timeout(200)
    ok('End goes to last slide', pg.evaluate(ACTIVE) == 2)
    f = pg.evaluate(ACTIVE); pg.wait_for_timeout(7500)
    ok('focus inside pauses autoplay', pg.evaluate(ACTIVE) == f)
    ok('manual change sets live region polite', pg.evaluate(STATE)['live'] == 'polite')
    # header transparency
    pg.evaluate('window.scrollTo(0,0)'); pg.keyboard.press('Escape'); pg.mouse.move(5, 1390); pg.wait_for_timeout(500)
    hdr = "() => getComputedStyle(document.querySelector('.header-wrapper')).backgroundColor"
    ok('header transparent over hero at top', pg.evaluate(hdr) in ('rgba(0, 0, 0, 0)', 'transparent'), pg.evaluate(hdr))
    pg.mouse.wheel(0, 1400); pg.wait_for_timeout(900)
    ok('header solid after scrolling', pg.evaluate(hdr) not in ('rgba(0, 0, 0, 0)', 'transparent'), pg.evaluate(hdr))
    pg.goto(base + '/collections/clothing', wait_until='load', timeout=120000); pg.wait_for_timeout(1000)
    ok('header solid on other pages', pg.evaluate(hdr) not in ('rgba(0, 0, 0, 0)', 'transparent') and not pg.evaluate("document.documentElement.classList.contains('th-header-over-hero')"), pg.evaluate(hdr))
    ctx.close()

    # --- Reduced motion ---
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce'); pg = ctx.new_page()
    pg.goto(base + '/', wait_until='load', timeout=120000); pg.wait_for_timeout(1200); pg.mouse.move(5, 1390)
    a = pg.evaluate(ACTIVE); pg.wait_for_timeout(7500)
    st = pg.evaluate(STATE)
    ok('reduced motion: no autoplay, button offers play', pg.evaluate(ACTIVE) == a and st['pressed'] == 'true', st['pressed'])
    zoom = pg.evaluate("getComputedStyle(document.querySelector('.hero-slide.is-active .hero-slide__media')).animationName")
    trans = pg.evaluate("getComputedStyle(document.querySelector('.hero-slide')).transitionDuration")
    ok('reduced motion: instant swap (no transition)', trans in ('0s', '0s, 0s'), trans)
    ctx.close()

    # --- JS disabled ---
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, java_script_enabled=False); pg = ctx.new_page()
    pg.goto(base + '/', wait_until='load', timeout=120000); pg.wait_for_timeout(800)
    vis = pg.evaluate("""() => [...document.querySelectorAll('[data-slide]')].map(s => { const c=getComputedStyle(s); return c.visibility + '/' + c.opacity })""")
    txt = pg.evaluate("() => { const h=document.querySelector('[data-slide] .hero-slide__heading'); const b=h.getBoundingClientRect(); return [h.textContent.trim(), b.width>0, getComputedStyle(h).color] }")
    ok('JS off: slide 1 visible, others hidden', vis[0] == 'visible/1' and all(v.startswith('hidden') for v in vis[1:]), vis)
    ok('JS off: slide 1 heading rendered', txt[1] and txt[0], txt)
    pg.screenshot(path=f'{out}/hero-nojs-1440.jpg', type='jpeg', quality=72, clip={'x': 0, 'y': 0, 'width': 1440, 'height': 900})
    ctx.close()

    # --- Alignment with the page container at many widths (LTR and real RTL) ---
    # Real RTL when the Arabic locale is published; otherwise force dir=rtl on the default route.
    probe = b.new_context(); ar_ok = probe.new_page().goto(base + '/ar', timeout=120000).status == 200; probe.close()
    rtl_path = '/ar' if ar_ok else '/'
    if not ar_ok:
        print('NOTE /ar is not available (Arabic not published): RTL alignment uses forced dir="rtl"')
    for path, rtl in (('/', False), (rtl_path, True)):
        for w in (360, 390, 430, 768, 1440, 1920):
            ctx = b.new_context(viewport={'width': w, 'height': 900}); pg = ctx.new_page()
            pg.goto(base + path, wait_until='load', timeout=120000); pg.wait_for_timeout(1000)
            if rtl and not ar_ok:
                pg.evaluate("() => { document.documentElement.dir = 'rtl'; const base = document.querySelector('link[href*=\"/assets/base.css\"]'); const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = base.href.split('/assets/')[0] + '/assets/rtl.css'; document.head.appendChild(l); }")
                pg.wait_for_timeout(500)
            m = pg.evaluate("""(rtl) => { const el=document.querySelector('[data-slide].is-active .hero-slide__content'); if(!el) return ['no active slide content', document.querySelectorAll('[data-slide]').length, location.pathname]; const c=el.getBoundingClientRect();
                 const ref=document.querySelector('.path-cards .page-width'); const cs=getComputedStyle(ref); const r=ref.getBoundingClientRect();
                 const start = rtl ? r.right - parseFloat(cs.paddingRight) : r.left + parseFloat(cs.paddingLeft);
                 const mine = rtl ? c.right : c.left; return [Math.round(mine), Math.round(start), document.documentElement.scrollWidth <= innerWidth] }""", rtl)
            ok(f'{"RTL" if rtl else "LTR"} {w}px: hero content edge = container edge, no overflow', isinstance(m[0], (int, float)) and abs(m[0] - m[1]) <= 1 and m[2], m)
            if w in (390, 1440):
                pg.screenshot(path=f'{out}/hero-{w}{"-rtl" if rtl else ""}.jpg', type='jpeg', quality=72, clip={'x': 0, 'y': 0, 'width': w, 'height': 900})
            ctx.close()
    b.close()

for name, cond, detail in R:
    print('PASS' if cond else 'FAIL', name, '-', detail[:160])
print('summary', sum(c for _, c, _ in R), '/', len(R))
