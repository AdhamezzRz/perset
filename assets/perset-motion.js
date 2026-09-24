/* ==========================================================================
   PER SET — MOTION ENGINE
   No dependencies. One rAF loop. Everything degrades to a static, legible
   page if JavaScript never arrives or the visitor asks for reduced motion.
   ========================================================================== */

(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  var coarse = window.matchMedia('(pointer: coarse)');

  /* ---------------------------------------------------------------- utils */

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function clamp(n, a, b) { return n < a ? a : n > b ? b : n; }
  function lerp(a, b, t) { return a + (b - a) * t; }

  /* ------------------------------------------------------- scroll ticker
     A single requestAnimationFrame loop drives parallax, plate rotation,
     the progress thread and the cursor. Subscribers are plain functions. */

  var ticking = false;
  var subs = [];
  var scrollY = window.scrollY || 0;
  var vh = window.innerHeight;
  var vw = window.innerWidth;

  function onFrame(fn) { subs.push(fn); }

  function tick() {
    for (var i = 0; i < subs.length; i++) subs[i](scrollY, vh, vw);
    ticking = false;
  }

  function requestTick() {
    if (!ticking) { ticking = true; requestAnimationFrame(tick); }
  }

  window.addEventListener('scroll', function () {
    scrollY = window.scrollY || window.pageYOffset || 0;
    requestTick();
  }, { passive: true });

  var resizeTimer;
  window.addEventListener('resize', function () {
    vh = window.innerHeight;
    vw = window.innerWidth;
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      measureParallax();
      measureRotators();
      requestTick();
    }, 140);
    requestTick();
  }, { passive: true });

  /* --------------------------------------------------------------- reveal
     Elements carrying [data-ps-reveal] fade/rise in when they cross the
     viewport. Siblings inside [data-ps-stagger] inherit an incremental
     delay so nothing ever arrives all at once. */

  function initReveal() {
    var items = $$('[data-ps-reveal]');
    if (!items.length) return;

    // Assign stagger delays from the parent group.
    $$('[data-ps-stagger]').forEach(function (group) {
      var step = parseInt(group.getAttribute('data-ps-stagger'), 10) || 90;
      var kids = $$('[data-ps-reveal]', group);
      kids.forEach(function (kid, i) {
        if (!kid.style.getPropertyValue('--ps-delay')) {
          kid.style.setProperty('--ps-delay', (i * step) + 'ms');
        }
      });
    });

    if (reduced.matches || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-in'); });
      $$('.ps-lines, .ps-thread--draw').forEach(function (el) { el.classList.add('is-in'); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -9% 0px', threshold: 0.08 });

    items.forEach(function (el) { io.observe(el); });

    // Split headlines and stitched rules use the same observer contract.
    var io2 = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io2.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });

    $$('.ps-lines, .ps-thread--draw').forEach(function (el) { io2.observe(el); });
  }

  /* ----------------------------------------------------------- split text
     [data-ps-split="lines"] wraps each rendered line in a mask so it can
     rise from behind an edge. We measure real line boxes with Range so the
     split survives any font size or wrapping. */

  function splitLines(el) {
    if (el.dataset.psSplitDone === '1') return;
    var text = el.textContent.replace(/\s+/g, ' ').trim();
    if (!text) return;

    // Rebuild as words so we can measure where lines break.
    var words = text.split(' ');
    el.textContent = '';
    var spans = words.map(function (w, i) {
      var s = document.createElement('span');
      s.textContent = w + (i < words.length - 1 ? ' ' : '');
      s.style.display = 'inline-block';
      el.appendChild(s);
      return s;
    });

    // Group words by their vertical offset.
    var lines = [];
    var current = null;
    var lastTop = null;
    spans.forEach(function (s) {
      var top = Math.round(s.offsetTop);
      if (lastTop === null || Math.abs(top - lastTop) > 2) {
        current = [];
        lines.push(current);
        lastTop = top;
      }
      current.push(s.textContent);
    });

    el.textContent = '';
    el.classList.add('ps-lines');
    var step = parseInt(el.getAttribute('data-ps-split-step'), 10) || 110;
    lines.forEach(function (words, i) {
      var mask = document.createElement('span');
      mask.className = 'ps-line-mask';
      var inner = document.createElement('span');
      inner.className = 'ps-line-inner';
      inner.style.setProperty('--ps-delay', (i * step) + 'ms');
      inner.textContent = words.join('');
      mask.appendChild(inner);
      el.appendChild(mask);
    });
    el.dataset.psSplitDone = '1';
  }

  function splitChars(el) {
    if (el.dataset.psSplitDone === '1') return;
    var text = el.textContent;
    el.textContent = '';
    var step = parseInt(el.getAttribute('data-ps-split-step'), 10) || 32;
    var n = 0;
    text.split('').forEach(function (ch) {
      if (ch === ' ') { el.appendChild(document.createTextNode(' ')); return; }
      var s = document.createElement('span');
      s.className = 'ps-char';
      s.textContent = ch;
      s.style.setProperty('--ps-delay', (n * step) + 'ms');
      el.appendChild(s);
      n++;
    });
    el.dataset.psSplitDone = '1';
  }

  function initSplit() {
    $$('[data-ps-split]').forEach(function (el) {
      var mode = el.getAttribute('data-ps-split');
      if (mode === 'chars') splitChars(el);
      else splitLines(el);
    });
  }

  /* -------------------------------------------------------------- parallax
     Layers drift at a fraction of scroll speed. We cache each element's
     document offset once and only write a transform, never read layout,
     inside the loop. */

  var parallaxItems = [];

  function measureParallax() {
    parallaxItems = $$('[data-ps-parallax]').map(function (el) {
      var rect = el.getBoundingClientRect();
      return {
        el: el,
        speed: parseFloat(el.getAttribute('data-ps-parallax')) || 0.15,
        top: rect.top + (window.scrollY || 0),
        h: rect.height
      };
    });
  }

  function initParallax() {
    if (reduced.matches) return;
    measureParallax();
    if (!parallaxItems.length) return;

    onFrame(function (y, vhh) {
      for (var i = 0; i < parallaxItems.length; i++) {
        var p = parallaxItems[i];
        var centre = p.top + p.h / 2;
        var delta = (y + vhh / 2) - centre;
        if (Math.abs(delta) > vhh * 1.8) continue;
        p.el.style.setProperty('--ps-par', (delta * p.speed * -1).toFixed(2) + 'px');
      }
    });
  }

  /* -------------------------------------------------- scroll-linked plates
     The signature move. A plate carrying [data-ps-rotate] turns as it
     travels through the viewport, the way you would turn a piece over in
     your hands to read the back. */

  var rotators = [];

  function measureRotators() {
    rotators = $$('[data-ps-rotate]').map(function (el) {
      var rect = el.getBoundingClientRect();
      return {
        el: el,
        deg: parseFloat(el.getAttribute('data-ps-rotate')) || 40,
        scaleTo: parseFloat(el.getAttribute('data-ps-rotate-scale')) || 0,
        top: rect.top + (window.scrollY || 0),
        h: rect.height,
        shadow: $('.ps-plate-shadow', el.parentNode || el)
      };
    });
  }

  function initRotate() {
    if (reduced.matches) return;
    measureRotators();
    if (!rotators.length) return;

    onFrame(function (y, vhh) {
      for (var i = 0; i < rotators.length; i++) {
        var r = rotators[i];
        // progress: 0 when the element's top hits the bottom of the screen,
        // 1 when its bottom leaves the top.
        var p = (y + vhh - r.top) / (vhh + r.h);
        if (p < -0.2 || p > 1.2) continue;
        p = clamp(p, 0, 1);
        var deg = (p - 0.5) * 2 * r.deg;
        r.el.style.setProperty('--ps-rot', deg.toFixed(2) + 'deg');
        if (r.scaleTo) {
          var s = 1 + (r.scaleTo - 1) * Math.sin(p * Math.PI);
          r.el.style.transform = 'rotate(' + deg.toFixed(2) + 'deg) scale(' + s.toFixed(3) + ')';
        }
        if (r.shadow) {
          var ss = lerp(0.82, 1.08, Math.sin(p * Math.PI));
          r.shadow.style.setProperty('--ps-shadow-scale', ss.toFixed(3));
        }
      }
    });
  }

  /* ----------------------------------------------------------- glaze sheen
     The specular highlight on a plate tracks the pointer, so the glaze
     reads as a curved surface rather than a flat circle. */

  function initGlaze() {
    if (coarse.matches || reduced.matches) return;
    $$('.ps-plate, .ps-card__frame').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--ps-gx', (((e.clientX - r.left) / r.width) * 100).toFixed(1) + '%');
        el.style.setProperty('--ps-gy', (((e.clientY - r.top) / r.height) * 100).toFixed(1) + '%');
      }, { passive: true });
    });
  }

  /* --------------------------------------------------------------- header
     Hides on the way down, returns on the way up, and picks up a linen
     backdrop once you leave the hero. */

  function initHeader() {
    var header = $('[data-ps-header]');
    if (!header) return;
    var last = 0;
    var threshold = 64;

    onFrame(function (y) {
      header.classList.toggle('is-stuck', y > 24);
      if (Math.abs(y - last) > 6) {
        var down = y > last && y > threshold * 3;
        var menuOpen = document.documentElement.classList.contains('ps-menu-open');
        header.classList.toggle('is-hidden', down && !menuOpen);
        last = y;
      }
    });
  }

  /* ------------------------------------------------------ progress thread */

  function initProgress() {
    var bar = $('[data-ps-progress]');
    if (!bar) return;
    onFrame(function (y, vhh) {
      var max = document.documentElement.scrollHeight - vhh;
      bar.style.setProperty('--ps-progress', max > 0 ? clamp(y / max, 0, 1).toFixed(4) : 0);
    });
  }

  /* --------------------------------------------------------------- cursor
     A porcelain rim. It swells and labels itself over anything that
     declares [data-ps-cursor]. */

  function initCursor() {
    if (coarse.matches || reduced.matches) return;
    var el = document.createElement('div');
    el.className = 'ps-cursor';
    el.setAttribute('aria-hidden', 'true');
    var label = document.createElement('span');
    label.className = 'ps-cursor__label';
    el.appendChild(label);
    document.body.appendChild(el);

    var tx = vw / 2, ty = vh / 2, cx = tx, cy = ty, running = false;

    function loop() {
      cx = lerp(cx, tx, 0.19);
      cy = lerp(cy, ty, 0.19);
      el.style.transform = 'translate3d(' + cx.toFixed(1) + 'px,' + cy.toFixed(1) + 'px,0) translate(-50%,-50%)';
      if (Math.abs(cx - tx) > 0.1 || Math.abs(cy - ty) > 0.1) {
        requestAnimationFrame(loop);
      } else { running = false; }
    }

    window.addEventListener('pointermove', function (e) {
      tx = e.clientX; ty = e.clientY;
      el.classList.add('is-on');
      if (!running) { running = true; requestAnimationFrame(loop); }
    }, { passive: true });

    document.addEventListener('pointerleave', function () { el.classList.remove('is-on'); });

    document.addEventListener('pointerover', function (e) {
      var t = e.target.closest ? e.target.closest('[data-ps-cursor]') : null;
      if (t) {
        el.classList.add('is-lg');
        label.textContent = t.getAttribute('data-ps-cursor') || '';
      }
    });
    document.addEventListener('pointerout', function (e) {
      var t = e.target.closest ? e.target.closest('[data-ps-cursor]') : null;
      if (t && !(e.relatedTarget && e.relatedTarget.closest && e.relatedTarget.closest('[data-ps-cursor]') === t)) {
        el.classList.remove('is-lg');
        label.textContent = '';
      }
    });
  }

  /* ------------------------------------------------------------- magnetic
     Buttons lean very slightly toward the pointer. Subtle enough that it
     reads as attention rather than as a gimmick. */

  function initMagnetic() {
    if (coarse.matches || reduced.matches) return;
    $$('[data-ps-magnetic]').forEach(function (el) {
      var strength = parseFloat(el.getAttribute('data-ps-magnetic')) || 0.28;
      var raf = null, tX = 0, tY = 0, curX = 0, curY = 0;

      function run() {
        curX = lerp(curX, tX, 0.2);
        curY = lerp(curY, tY, 0.2);
        el.style.transform = 'translate3d(' + curX.toFixed(2) + 'px,' + curY.toFixed(2) + 'px,0)';
        if (Math.abs(curX - tX) > 0.05 || Math.abs(curY - tY) > 0.05) {
          raf = requestAnimationFrame(run);
        } else { raf = null; }
      }
      function kick() { if (!raf) raf = requestAnimationFrame(run); }

      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        tX = (e.clientX - (r.left + r.width / 2)) * strength;
        tY = (e.clientY - (r.top + r.height / 2)) * strength;
        kick();
      }, { passive: true });

      el.addEventListener('pointerleave', function () { tX = 0; tY = 0; kick(); });
    });
  }

  /* ------------------------------------------------------------- marquee
     Duplicate the group once so the translate(-50%) loop is seamless. */

  function initMarquee() {
    $$('.ps-marquee__track').forEach(function (track) {
      var group = $('.ps-marquee__group', track);
      if (!group || track.children.length > 1) return;
      var clone = group.cloneNode(true);
      clone.setAttribute('aria-hidden', 'true');
      track.appendChild(clone);
    });
  }

  /* ---------------------------------------------------------------- menu */

  function initMenu() {
    // There can be more than one toggle button in the DOM (a mobile-only one
    // and a desktop one, shown and hidden by CSS at different breakpoints).
    // Binding with $ (querySelector) instead of $$ only ever wired up the
    // first one — on desktop that button is display:none, so the visible
    // toggle silently did nothing. Bind every toggle that exists.
    var toggles = $$('[data-ps-menu-toggle]');
    var menu = $('[data-ps-menu]');
    if (!toggles.length || !menu) return;
    var closeBtn = $('[data-ps-menu-close]', menu);
    // Top-level rows get the staggered reveal, whether they are a plain link
    // or a group toggle for a dropdown. Only real navigation links (plain
    // top-level links, plus anything inside an open dropdown) close the
    // whole overlay on click — the toggle itself must not, or opening a
    // dropdown would immediately shut the menu behind it.
    var reveals = $$('.ps-menu__link, .ps-menu__group-toggle', menu);
    var links = $$('.ps-menu__link, .ps-menu__sublink', menu);
    var lastFocus = null;

    reveals.forEach(function (l, i) { l.style.setProperty('--ps-delay', (120 + i * 62) + 'ms'); });

    function setExpanded(on) {
      toggles.forEach(function (t) { t.setAttribute('aria-expanded', on ? 'true' : 'false'); });
    }

    function open() {
      lastFocus = document.activeElement;
      menu.classList.add('is-open');
      document.documentElement.classList.add('ps-menu-open');
      document.body.style.overflow = 'hidden';
      setExpanded(true);
      menu.removeAttribute('aria-hidden');
      setTimeout(function () { (closeBtn || reveals[0] || menu).focus(); }, 260);
    }
    function close() {
      menu.classList.remove('is-open');
      document.documentElement.classList.remove('ps-menu-open');
      document.body.style.overflow = '';
      setExpanded(false);
      menu.setAttribute('aria-hidden', 'true');
      if (lastFocus) lastFocus.focus();
    }

    toggles.forEach(function (toggle) {
      toggle.addEventListener('click', function () {
        menu.classList.contains('is-open') ? close() : open();
      });
    });
    if (closeBtn) closeBtn.addEventListener('click', close);
    links.forEach(function (l) { l.addEventListener('click', close); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('is-open')) close();
    });
  }

  /* ----------------------------------------------------------- cart bump */

  function bumpCart(count) {
    var el = $('[data-ps-cart-count]');
    if (!el) return;
    el.textContent = count;
    el.classList.toggle('is-on', count > 0);
    el.classList.remove('is-bump');
    void el.offsetWidth;
    el.classList.add('is-bump');
  }
  window.PerSetBumpCart = bumpCart;

  /* ------------------------------------------------------------ h-scroll
     Collection rails scroll horizontally with the wheel, and report
     progress so a thread indicator can track them. */

  function initRails() {
    $$('[data-ps-rail]').forEach(function (rail) {
      var bar = $('[data-ps-rail-bar]', rail.parentNode);
      function report() {
        var max = rail.scrollWidth - rail.clientWidth;
        if (bar && max > 0) {
          bar.style.setProperty('--ps-progress', clamp(rail.scrollLeft / max, 0, 1).toFixed(4));
        }
      }
      rail.addEventListener('scroll', report, { passive: true });
      report();

      $$('[data-ps-rail-prev], [data-ps-rail-next]', rail.parentNode).forEach(function (btn) {
        btn.addEventListener('click', function () {
          var dir = btn.hasAttribute('data-ps-rail-next') ? 1 : -1;
          var card = $('*', rail);
          var step = card ? card.getBoundingClientRect().width + 24 : rail.clientWidth * 0.8;
          rail.scrollBy({ left: dir * step, behavior: reduced.matches ? 'auto' : 'smooth' });
        });
      });
    });
  }

  /* ------------------------------------------------------------- accordion */

  function initAccordion() {
    $$('[data-ps-accordion] > details').forEach(function (d) {
      var summary = $('summary', d);
      if (!summary) return;
      summary.addEventListener('click', function () {
        if (d.hasAttribute('open')) return;
        $$('[data-ps-accordion] > details[open]').forEach(function (other) {
          if (other !== d && other.parentNode === d.parentNode) other.removeAttribute('open');
        });
      });
    });
  }

  /* ------------------------------------------------------------ transition
     The veil (see layout/theme.liquid) covers each page as it arrives and
     is lifted once the page is ready. Here it is drawn back down when the
     visitor leaves, so moving through the site feels like a cloth being laid
     rather than a browser reloading.

     Navigation is never the animation's responsibility. Every path through
     this code ends in a real navigation: if anything throws, if the veil
     never animates, if a timer is throttled in a background tab, the link
     still goes where it was going. */

  function initTransition() {
    if (reduced.matches) return;
    var veil = $('[data-ps-veil]');
    if (!veil) return;

    var leaving = false;

    function leaves(a) {
      if (!a || !a.href) return false;
      if (a.target && a.target !== '_self') return false;
      if (a.hasAttribute('download')) return false;
      if (a.getAttribute('rel') === 'external') return false;
      if (a.dataset.psNoTransition !== undefined) return false;

      var url;
      try { url = new URL(a.href, location.href); } catch (e) { return false; }
      if (url.origin !== location.origin) return false;
      if (url.protocol !== 'http:' && url.protocol !== 'https:') return false;
      // Same page, different hash: that is a scroll, not a journey.
      if (url.pathname === location.pathname && url.search === location.search && url.hash) return false;
      if (url.href === location.href) return false;
      return true;
    }

    document.addEventListener('click', function (e) {
      if (e.defaultPrevented || leaving) return;
      if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

      var a = e.target.closest ? e.target.closest('a') : null;
      if (!leaves(a)) return;

      e.preventDefault();
      leaving = true;
      var href = a.href;

      // Two independent paths to navigation: whichever fires first wins.
      var go = function () {
        if (!go.done) { go.done = true; window.location.href = href; }
      };
      veil.addEventListener('transitionend', go, { once: true });
      setTimeout(go, 700);

      try { veil.classList.remove('is-open'); } catch (err) { go(); }
    });
  }

  /* ---------------------------------------------------------------- boot */

  function boot() {
    initSplit();
    initReveal();
    initParallax();
    initRotate();
    initGlaze();
    initHeader();
    initProgress();
    initCursor();
    initMagnetic();
    initMarquee();
    initMenu();
    initRails();
    initAccordion();
    initTransition();
    requestTick();
    document.documentElement.classList.add('ps-ready');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  // Shopify's theme editor tears sections down and rebuilds them.
  document.addEventListener('shopify:section:load', function () {
    initSplit(); initReveal(); measureParallax(); measureRotators();
    initGlaze(); initMarquee(); initRails(); initMagnetic(); initAccordion();
    requestTick();
  });

  // Fonts change line wrapping, so re-measure once they land.
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () {
      measureParallax();
      measureRotators();
      requestTick();
    });
  }
})();
