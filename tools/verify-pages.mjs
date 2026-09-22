/**
 * End-to-end check of the live theme preview in a real browser.
 *
 *   node tools/verify-pages.mjs            # desktop, 1440px
 *   node tools/verify-pages.mjs --mobile   # phone, 390px
 *
 * Loads every important page against the preview theme, scrolls it to the
 * bottom so every reveal fires, and fails a page if:
 *   - our stylesheet is missing, or the motion engine never announced itself
 *   - the header or footer did not render
 *   - a Liquid error or a missing translation string reached the page
 *   - a reveal is still invisible while on screen
 *   - the page scrolls horizontally
 *
 * Needs playwright and a chromium binary. Override with the CHROME,
 * STORE_URL and PREVIEW_THEME_ID environment variables.
 */

import { chromium } from 'playwright';

const THEME = process.env.PREVIEW_THEME_ID || '166988251321';
const BASE = process.env.STORE_URL || 'https://perset.shop';
const MOBILE = process.argv.includes('--mobile');

const PAGES = [
  ['home',       '/'],
  ['collections','/collections'],
  ['collection', '/collections/stitches-of-the-wild'],
  ['product',    '/products/stitches-of-the-wild-dinner-plates-set-of-6'],
  ['cart',       '/cart'],
  ['search',     '/search?q=plate'],
  ['story',      '/pages/our-story'],
  ['faq',        '/pages/faq'],
  ['contact',    '/pages/contact'],
  ['notfound',   '/nothing-here'],
];

const browser = await chromium.launch({
  executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--no-sandbox', '--disable-dev-shm-usage'],
});
const ctx = await browser.newContext({
  viewport: MOBILE ? { width: 390, height: 844 } : { width: 1440, height: 900 },
  deviceScaleFactor: 2,
  isMobile: MOBILE,
  hasTouch: MOBILE,
});
const page = await ctx.newPage();

const noise = /favicon|googletagmanager|google-analytics|monorail|web-pixel|shopifycloud\/shop-js|bugsnag|consent/i;
let fails = 0;

await page.goto(`${BASE}/?preview_theme_id=${THEME}`, { waitUntil: 'domcontentloaded' });

for (const [name, path] of PAGES) {
  const problems = [];
  const onErr = m => { if (m.type() === 'error' && !noise.test(m.text())) problems.push('console: ' + m.text().slice(0, 160)); };
  const onPageErr = e => { if (!noise.test(String(e))) problems.push('pageerror: ' + String(e).slice(0, 160)); };
  const onReqFail = r => { if (!noise.test(r.url())) problems.push('reqfail: ' + r.url().slice(0, 120)); };
  page.on('console', onErr); page.on('pageerror', onPageErr); page.on('requestfailed', onReqFail);

  let status = '?';
  try {
    const resp = await page.goto(BASE + path, { waitUntil: 'networkidle', timeout: 45000 });
    status = resp ? resp.status() : '?';
  } catch (e) { status = 'ERR'; problems.push('goto: ' + e.message.slice(0, 120)); }

  await page.waitForTimeout(1200);
  await page.evaluate(async () => {
    const step = window.innerHeight * 0.75;
    for (let y = 0; y < document.body.scrollHeight; y += step) {
      window.scrollTo(0, y); await new Promise(r => setTimeout(r, 90));
    }
    window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 600));
  });

  const info = await page.evaluate(() => {
    const txt = document.body.innerText;
    return {
      title: document.title.trim().replace(/\s+/g, ' ').slice(0, 60),
      h1: (document.querySelector('h1')?.innerText || '(none)').trim().replace(/\s+/g, ' ').slice(0, 55),
      ready: document.documentElement.classList.contains('ps-ready'),
      ours: !!document.querySelector('link[href*="perset-core"]'),
      psHeader: !!document.querySelector('.ps-header'),
      psFooter: !!document.querySelector('.ps-footer'),
      hiddenInView: [...document.querySelectorAll('[data-ps-reveal]')]
        .filter(el => {
          const r = el.getBoundingClientRect();
          const cs = getComputedStyle(el);
          // Ignore anything that is not actually laid out: display:none
          // elements report opacity 0 at 0x0, which is not a stuck reveal.
          if (cs.display === 'none' || r.width === 0 || r.height === 0) return false;
          return cs.opacity === '0' && r.top < innerHeight && r.bottom > 0;
        }).length,
      liquid: (txt.match(/Liquid error[^\n]*/g) || []).slice(0, 2),
      missingT: (txt.match(/Translation missing: [^\s]*/g) || []).slice(0, 3),
      overflow: document.documentElement.scrollWidth > window.innerWidth + 2,
    };
  });

  const bad = !info.ours || !info.ready || !info.psHeader || !info.psFooter ||
              info.liquid.length || info.missingT.length || info.hiddenInView || info.overflow ||
              (typeof status === 'number' && status >= 500);
  if (bad) fails++;

  console.log(`${bad ? 'FAIL' : ' ok '} ${name.padEnd(12)} ${String(status).padEnd(4)} h1="${info.h1}"`);
  console.log(`      ours=${info.ours} ready=${info.ready} header=${info.psHeader} footer=${info.psFooter} hidden=${info.hiddenInView} xOverflow=${info.overflow}`);
  if (info.liquid.length)   console.log('      LIQUID: ' + info.liquid.join(' | '));
  if (info.missingT.length) console.log('      MISSING T: ' + info.missingT.join(' '));
  if (problems.length)      console.log('      ' + problems.slice(0, 4).join('\n      '));

  await page.screenshot({ path: `v-${MOBILE ? 'm' : 'd'}-${name}.png`, fullPage: false });
  if (!MOBILE) await page.screenshot({ path: `v-full-${name}.png`, fullPage: true });

  page.off('console', onErr); page.off('pageerror', onPageErr); page.off('requestfailed', onReqFail);
}

console.log(`\n${fails === 0 ? 'ALL PAGES PASS' : fails + ' page(s) with problems'} (${MOBILE ? 'mobile 390px' : 'desktop 1440px'})`);
await browser.close();
