"""Unit-style Liquid check for snippets/event-date.liquid (QA round 1, issue 5).

usage: python -X utf8 scripts/tests/event_date_selftest.py BASE_URL
  BASE_URL  a running `shopify theme dev` (e.g. http://127.0.0.1:9393) serving this repository

Writes a temporary template (templates/page.zz-selftest.json) that renders event-date for values a
translation tool could produce, waits for theme dev to sync it, checks the output and always
deletes the template again (it is never committed). Needs any page; /pages/workshops is used.
"""
import json, re, sys, time, urllib.request
from pathlib import Path

BASE = sys.argv[1].rstrip('/')
ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / 'templates' / 'page.zz-selftest.json'

CASES = [
    # (label, value, start, expected iso, expected short text in English)
    ('latin', '2026-11-07 18:00', '', '2026-11-07T18:00+02:00', 'Sat 7 Nov · 6:00 PM'),
    ('arabic-indic digits', '٢٠٢٦-١١-٠٧ ١٨:٠٠', '', '2026-11-07T18:00+02:00', 'Sat 7 Nov · 6:00 PM'),
    ('persian digits', '۲۰۲۶-۱۱-۰۷ ۱۸:۰۰', '', '2026-11-07T18:00+02:00', 'Sat 7 Nov · 6:00 PM'),
    ('slashes', '2026/11/07 18:00', '', '2026-11-07T18:00+02:00', 'Sat 7 Nov · 6:00 PM'),
    ('iso T', '2026-11-07T18:00', '', '2026-11-07T18:00+02:00', 'Sat 7 Nov · 6:00 PM'),
    ('summer time', '2026-06-13 18:00', '', '2026-06-13T18:00+03:00', 'Sat 13 Jun · 6:00 PM'),
    ('metafield wins (UTC instant)', 'anything', '2026-11-07T16:00:00Z', '2026-11-07T18:00+02:00', 'Sat 7 Nov · 6:00 PM'),
    ('metafield in summer', '', '2026-06-13T15:00:00Z', '2026-06-13T18:00+03:00', 'Sat 13 Jun · 6:00 PM'),
    ('not a date', 'TBD soon', '', '', None),
]

liquid = ''.join(
    "<li data-case=\"%s\">{%%- capture iso -%%}{%% render 'event-date', value: %s, start: %s, output: 'iso' %%}{%%- endcapture -%%}"
    "{%%- capture short -%%}{%% render 'event-date', value: %s, start: %s, output: 'short' %%}{%%- endcapture -%%}"
    "<b class=\"iso\">{{ iso | strip }}</b><i class=\"short\">{{ short | strip | strip_html }}</i></li>"
    % (label, json.dumps(value, ensure_ascii=False), json.dumps(start), json.dumps(value, ensure_ascii=False), json.dumps(start))
    for label, value, start, *_ in CASES)
TEMPLATE.write_text(json.dumps(ensure_ascii=False, obj={
    'sections': {'t': {'type': 'custom-liquid', 'settings': {'custom_liquid': '<ul id="selftest">' + liquid + '</ul>'}}},
    'order': ['t']}), encoding='utf-8')
DEBUG = '--debug' in sys.argv

results = []
try:
    url = BASE + '/pages/workshops?view=zz-selftest'
    html = ''
    for _ in range(30):
        time.sleep(3)
        try:
            html = urllib.request.urlopen(url, timeout=60).read().decode('utf-8')
        except Exception:
            continue
        if 'id="selftest"' in html:
            break
    if DEBUG:
        m = re.search(r'<ul id="selftest">(.*?)</ul>', html, re.S)
        print(m.group(1)[:1500] if m else html[:500])
    rows = dict(re.findall(r'<li data-case="([^"]+)"><b class="iso">(.*?)</b>', html, re.S))
    shorts = dict(re.findall(r'<li data-case="([^"]+)"><b class="iso">.*?</b><i class="short">(.*?)</i>', html, re.S))
    for label, value, start, want_iso, want_short in CASES:
        got_iso = rows.get(label)
        got_short = (shorts.get(label) or '').replace('&middot;', '·').strip()
        cond = got_iso == want_iso and (want_short is None or got_short == want_short)
        if want_short is None:
            cond = got_iso == '' and value in got_short
        results.append((label, cond, f'iso={got_iso!r} short={got_short!r}'))
finally:
    TEMPLATE.unlink(missing_ok=True)

for name, cond, detail in results:
    print('PASS' if cond else 'FAIL', 'event-date:', name, '-', detail)
print('summary', sum(c for _, c, _ in results), '/', len(CASES))
