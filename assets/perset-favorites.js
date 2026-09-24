/* ==========================================================================
   PER SET — FAVOURITES
   A quiet wishlist. Shopify has no native one, so this keeps a list of
   product handles in localStorage and nothing more — no account, no sync
   across devices. That is a real limitation and the empty state says so.

   The contract with the markup:
     [data-ps-fav-toggle]          a heart button
       data-ps-fav-handle="..."    the product handle it saves
     [data-ps-fav-count]           any element whose text becomes the count
     [data-ps-fav-list]            the favourites page's grid, filled by JS

   Everything here degrades to "does nothing" if localStorage is unavailable
   (private windows, blocked storage) rather than throwing.
   ========================================================================== */

(function () {
  'use strict';

  var KEY = 'perset:favorites';

  function read() {
    try {
      var raw = window.localStorage.getItem(KEY);
      var list = raw ? JSON.parse(raw) : [];
      return Array.isArray(list) ? list : [];
    } catch (e) {
      return [];
    }
  }

  function write(list) {
    try { window.localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) { /* storage unavailable */ }
    paintCounts(list.length);
    document.dispatchEvent(new CustomEvent('ps:favorites-changed', { detail: { handles: list, count: list.length } }));
  }

  function has(handle) { return read().indexOf(handle) !== -1; }

  function toggle(handle) {
    var list = read();
    var i = list.indexOf(handle);
    if (i === -1) { list.push(handle); } else { list.splice(i, 1); }
    write(list);
    return i === -1; // true if it is now saved
  }

  function paintCounts(count) {
    var nodes = document.querySelectorAll('[data-ps-fav-count]');
    for (var i = 0; i < nodes.length; i++) {
      nodes[i].textContent = count;
      nodes[i].classList.toggle('is-on', count > 0);
    }
  }

  function paintToggle(btn) {
    var handle = btn.getAttribute('data-ps-fav-handle');
    var on = has(handle);
    btn.classList.toggle('is-fav', on);
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    var label = on ? btn.getAttribute('data-ps-fav-label-on') : btn.getAttribute('data-ps-fav-label-off');
    if (label) {
      var text = btn.querySelector('[data-ps-fav-text]');
      if (text) text.textContent = label;
      else btn.setAttribute('aria-label', label);
    }
  }

  function initToggles(root) {
    var btns = (root || document).querySelectorAll('[data-ps-fav-toggle]');
    for (var i = 0; i < btns.length; i++) {
      var btn = btns[i];
      if (btn.dataset.psFavBound) continue;
      btn.dataset.psFavBound = '1';
      paintToggle(btn);
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var handle = this.getAttribute('data-ps-fav-handle');
        if (!handle) return;
        var nowOn = toggle(handle);
        paintToggle(this);
        var live = document.getElementById('ps-live');
        if (live) {
          live.textContent = nowOn
            ? (this.getAttribute('data-ps-fav-added') || 'Saved to your favourites.')
            : (this.getAttribute('data-ps-fav-removed') || 'Removed from your favourites.');
        }
      });
    }
  }

  document.addEventListener('ps:favorites-changed', function () {
    initToggles(document); // re-paint any toggle for a handle that changed elsewhere
    var btns = document.querySelectorAll('[data-ps-fav-toggle]');
    for (var i = 0; i < btns.length; i++) paintToggle(btns[i]);
  });

  document.addEventListener('DOMContentLoaded', function () {
    paintCounts(read().length);
    initToggles(document);
  });
  document.addEventListener('shopify:section:load', function (e) { initToggles(e.target); });

  window.PerSetFavorites = { has: has, toggle: toggle, all: read };
})();
