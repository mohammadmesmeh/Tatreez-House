#!/usr/bin/env node
/**
 * WCAG 2.2 contrast check for the theme's colour schemes.
 *
 * Usage:  node scripts/contrast-check.mjs [path/to/settings_data.json]
 *
 * Reads the colour schemes the merchant configured in the theme editor
 * (config/settings_data.json → current.color_schemes) and prints, per scheme:
 *   - text on background                (Dawn headings, full-strength text)
 *   - body text on background           (Dawn renders body copy at rgba(text, 0.75))
 *   - button label on button            (primary button)
 *   - secondary button label on background (outline button, links)
 * Thresholds: AA normal text 4.5:1, AA large text / UI components 3:1.
 * Also checks the design-token pairs used outside schemes (accent, linen surface) read from
 * assets/tatreez-tokens.css, and flags scheme colours that are not in the brand palette.
 *
 * Read-only: never edits settings_data.json. Exit code 1 when a pair fails AA large/UI (3:1).
 */
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const file = process.argv[2] ?? path.join(root, 'config', 'settings_data.json');

const BRAND = {
  'Warm Ivory': '#F7F3EB',
  'Tatreez Black': '#292820',
  'Embroidery Red': '#8E3038',
  'Olive Green': '#667052',
  'Linen Beige': '#D9C8AD',
  Linen: '#F0E8D9',
  'Deep Green': '#17352B',
  White: '#FFFFFF',
};
const BODY_TEXT_ALPHA = 0.75; // layout/theme.liquid: body { color: rgba(var(--color-foreground), 0.75) }

const hexToRgb = (hex) => {
  let h = hex.trim().replace('#', '');
  if (h.length === 3) h = [...h].map((c) => c + c).join('');
  return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16));
};
const rgbToHex = (rgb) => '#' + rgb.map((v) => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();

const luminance = (rgb) => {
  const [r, g, b] = rgb.map((v) => {
    const c = v / 255;
    return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const ratio = (a, b) => {
  const [l1, l2] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (l1 + 0.05) / (l2 + 0.05);
};
const blend = (fg, bg, alpha) => fg.map((v, i) => v * alpha + bg[i] * (1 - alpha));

const grade = (r) => (r >= 7 ? 'AAA' : r >= 4.5 ? 'AA' : r >= 3 ? 'AA-large/UI only' : 'FAIL');

const brandName = (hex) => {
  const found = Object.entries(BRAND).find(([, v]) => v.toUpperCase() === hex.toUpperCase());
  if (found) return found[0];
  const rgb = hexToRgb(hex);
  const [name, , dist] = Object.entries(BRAND)
    .map(([n, v]) => {
      const d = Math.hypot(...hexToRgb(v).map((c, i) => c - rgb[i]));
      return [n, v, d];
    })
    .sort((a, b) => a[2] - b[2])[0];
  return `not brand (nearest: ${name} ${BRAND[name]}, Δ${dist.toFixed(0)})`;
};

// settings_data.json starts with a /* … */ banner, which JSON.parse rejects.
const raw = readFileSync(file, 'utf8').replace(/^\s*\/\*[\s\S]*?\*\//, '');
const data = JSON.parse(raw);
const schemes = data.current?.color_schemes;
if (!schemes) {
  console.error(`No current.color_schemes in ${file}`);
  process.exit(2);
}

const rows = [];
const offBrand = new Map();
for (const [id, { settings: s }] of Object.entries(schemes)) {
  const bg = hexToRgb(s.background);
  const text = hexToRgb(s.text);
  const body = blend(text, bg, BODY_TEXT_ALPHA);
  const pairs = [
    ['text / background', s.text, s.background, ratio(text, bg), 4.5],
    [`body text @${BODY_TEXT_ALPHA * 100}% / background`, rgbToHex(body), s.background, ratio(body, bg), 4.5],
    ['button label / button', s.button_label, s.button, ratio(hexToRgb(s.button_label), hexToRgb(s.button)), 4.5],
    [
      'secondary label / background',
      s.secondary_button_label,
      s.background,
      ratio(hexToRgb(s.secondary_button_label), bg),
      4.5,
    ],
  ];
  for (const [pair, fg, bgHex, r, need] of pairs) {
    rows.push({ scheme: id, pair, fg: fg.toUpperCase(), bg: bgHex.toUpperCase(), ratio: r, need, grade: grade(r) });
  }
  for (const key of ['background', 'text', 'button', 'button_label', 'secondary_button_label']) {
    const name = brandName(s[key]);
    if (name.startsWith('not brand')) offBrand.set(s[key].toUpperCase(), name);
  }
}

// Design-token pairs (assets/tatreez-tokens.css): colours used outside the colour schemes.
const tokenCss = readFileSync(path.join(root, 'assets', 'tatreez-tokens.css'), 'utf8');
const token = (name) => {
  const m = tokenCss.match(new RegExp(`--th-${name}:\\s*(\\d+),\\s*(\\d+),\\s*(\\d+)`));
  if (!m) throw new Error(`token --th-${name} not found`);
  return m.slice(1).map(Number);
};
const tokenPairs = [
  ['accent text (sale price) / ivory', 'red', 'ivory', 4.5],
  ['accent text / linen', 'red', 'linen', 4.5],
  ['accent text / white', 'red', 'white', 4.5],
  ['white text / accent (sale badge)', 'white', 'red', 4.5],
  ['ink text / linen', 'ink', 'linen', 4.5],
  ['muted ink 75% / linen', 'ink@0.75', 'linen', 4.5],
  ['deep green action / linen (UI)', 'green', 'linen', 3],
];
for (const [pair, fgName, bgName, need] of tokenPairs) {
  const bg = token(bgName);
  const [base, alpha] = fgName.split('@');
  const fg = alpha ? blend(token(base), bg, Number(alpha)) : token(base);
  const r = ratio(fg, bg);
  rows.push({ scheme: 'tokens', pair, fg: rgbToHex(fg), bg: rgbToHex(bg), ratio: r, need, grade: grade(r) });
}

const short = (id) => (id.length > 12 ? id.slice(0, 12) + '…' : id);
const header = ['Scheme', 'Pair', 'Foreground', 'Background', 'Ratio', 'Result'];
const table = rows.map((r) => [short(r.scheme), r.pair, r.fg, r.bg, r.ratio.toFixed(2) + ':1', r.grade]);
const widths = header.map((h, i) => Math.max(h.length, ...table.map((row) => row[i].length)));
const line = (cells) => '| ' + cells.map((c, i) => c.padEnd(widths[i])).join(' | ') + ' |';

console.log(`Contrast check — ${path.relative(root, file)}`);
console.log(line(header));
console.log('|' + widths.map((w) => '-'.repeat(w + 2)).join('|') + '|');
table.forEach((row) => console.log(line(row)));

const below = rows.filter((r) => r.ratio < r.need);
console.log(`\n${rows.length} pairs, ${rows.length - below.length} meet their requirement, ${below.length} below it.`);
below.forEach((r) =>
  console.log(`  - ${r.scheme}: ${r.pair} ${r.fg} on ${r.bg} = ${r.ratio.toFixed(2)}:1 (needs ${r.need}:1)`)
);

if (offBrand.size) {
  console.log('\nColours not in the brand palette:');
  for (const [hex, note] of offBrand) console.log(`  - ${hex}: ${note}`);
}

process.exit(below.length ? 1 : 0);
