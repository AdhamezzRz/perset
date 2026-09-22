/* ==========================================================================
   PER SET — CART
   A thin layer over Shopify's cart routes. No dependencies, no framework.

   The contract with the markup:
     form[data-ps-add]          an add-to-cart form we intercept
     [data-ps-add-btn]          its submit button
     [data-ps-add-label]        the span inside it whose text we swap
     #ps-cart-region            the part of the cart page we re-render
     [data-ps-line]             one line item, carrying data-ps-key
     [data-ps-step]             a quantity stepper button ("-1" / "1")
     [data-ps-qty]              a quantity input
     [data-ps-remove]           a remove link (a real href, so it works dead)
     [data-ps-cart-note]        the order note textarea

   Every one of those still does the right thing with JavaScript switched
   off: the forms post, the remove links navigate, the note saves with the
   update button. This file only removes the page reload.
   ========================================================================== */

(function () {
  'use strict';

  var doc = document;

  // No fetch, no enhancement. The plain forms below us are already correct.
  if (!window.fetch || !window.DOMParser || !window.FormData) return;

  var routes = (function () {
    var tag = doc.getElementById('ps-routes');
    if (!tag) return null;
    try { return JSON.parse(tag.textContent); } catch (e) { return null; }
  })();
  if (!routes || !routes.cart_add) return;

  var busy = false;

  /* ---------------------------------------------------------------- utils */

  function attr(el, name, fallback) {
    var v = el && el.getAttribute(name);
    return v === null || v === undefined || v === '' ? fallback : v;
  }

  function say(message) {
    var live = doc.getElementById('ps-live');
    if (live && message) live.textContent = message;
  }

  function handle(response) {
    return response.json().then(function (data) {
      if (!response.ok) {
        var err = new Error(data.description || data.message || 'Cart error');
        err.fromApi = true;
        throw err;
      }
      return data;
    });
  }

  // Add uses the raw FormData so line-item properties survive untouched.
  function postForm(url, formData) {
    return fetch(url, {
      method: 'POST',
      headers: { Accept: 'application/json' },
      body: formData
    }).then(handle);
  }

  function postJSON(url, payload) {
    return fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(payload)
    }).then(handle);
  }

  function cartState() {
    return fetch(routes.cart + '.js', { headers: { Accept: 'application/json' } }).then(handle);
  }

  function bump(cart) {
    if (cart && typeof cart.item_count === 'number' && window.PerSetBumpCart) {
      window.PerSetBumpCart(cart.item_count);
    }
    return cart;
  }

  /* ------------------------------------------------------- region refresh
     Rather than re-templating line items in JS — which would mean building
     money formatting and discount rules a second time — we ask the server
     for the cart page and lift the rendered region out of it. One request,
     always in sync, currency handled by Liquid. */

  function refreshRegion() {
    var region = doc.getElementById('ps-cart-region');
    if (!region) return Promise.resolve();
    return fetch(routes.cart, { headers: { Accept: 'text/html' } })
      .then(function (r) { return r.text(); })
      .then(function (html) {
        var fresh = new DOMParser()
          .parseFromString(html, 'text/html')
          .getElementById('ps-cart-region');
        if (fresh) {
          region.innerHTML = fresh.innerHTML;
          doc.dispatchEvent(new CustomEvent('ps:cart:rendered'));
        }
      });
  }

  function release(el) {
    busy = false;
    if (el) { el.removeAttribute('aria-busy'); el.classList.remove('is-busy'); }
  }

  /* ------------------------------------------------------------ add to cart */

  doc.addEventListener('submit', function (e) {
    var form = e.target.closest ? e.target.closest('form[data-ps-add]') : null;
    if (!form || busy) return;
    e.preventDefault();

    var btn = form.querySelector('[data-ps-add-btn]');
    var label = form.querySelector('[data-ps-add-label]');
    var resting = label ? label.textContent : '';

    busy = true;
    if (btn) btn.setAttribute('aria-busy', 'true');
    if (label) label.textContent = attr(form, 'data-ps-busy-label', resting);

    postForm(routes.cart_add, new FormData(form))
      .then(cartState)
      .then(bump)
      .then(function () {
        say(attr(form, 'data-ps-added-message', 'Added to your cart.'));
        if (label) {
          label.textContent = attr(form, 'data-ps-done-label', resting);
          setTimeout(function () { label.textContent = resting; }, 2400);
        }
        return refreshRegion();
      })
      .catch(function (err) {
        // A refused add (sold out, limit reached) is a real answer: show it.
        // A dead connection is not, so let the browser post the form itself.
        if (err && err.fromApi) {
          say(err.message);
          if (label) label.textContent = resting;
        } else {
          form.submit();
        }
      })
      .then(function () { release(btn); });
  });

  /* ------------------------------------------------------------ line items */

  function lineOf(el) { return el.closest ? el.closest('[data-ps-line]') : null; }

  function changeLine(key, quantity, row) {
    busy = true;
    if (row) row.classList.add('is-busy');
    return postJSON(routes.cart_change, { id: key, quantity: quantity })
      .then(bump)
      .then(function (cart) {
        say(quantity === 0
          ? attr(row, 'data-ps-removed-message', 'Removed from your cart.')
          : attr(row, 'data-ps-updated-message', 'Cart updated.'));
        if (cart.item_count === 0) { window.location.href = routes.cart; return; }
        return refreshRegion();
      })
      .catch(function (err) {
        if (err && err.fromApi) { say(err.message); refreshRegion(); }
        else { window.location.href = routes.cart; }
      })
      .then(function () { release(row); });
  }

  // Steppers: on the cart they push to the server, on a product page they
  // only move the number the form is about to submit.
  doc.addEventListener('click', function (e) {
    var step = e.target.closest ? e.target.closest('[data-ps-step]') : null;
    if (step) {
      var input = doc.getElementById(step.getAttribute('aria-controls'));
      if (!input) return;
      var delta = parseInt(step.getAttribute('data-ps-step'), 10) || 0;
      var min = parseInt(input.getAttribute('min'), 10);
      if (isNaN(min)) min = 0;
      var next = Math.max(min, (parseInt(input.value, 10) || 0) + delta);
      if (next === (parseInt(input.value, 10) || 0)) return;
      input.value = next;
      var row = lineOf(input);
      if (row && !busy) changeLine(row.getAttribute('data-ps-key'), next, row);
      return;
    }

    var remove = e.target.closest ? e.target.closest('[data-ps-remove]') : null;
    if (remove && !busy) {
      var line = lineOf(remove);
      if (!line) return;
      e.preventDefault();
      changeLine(line.getAttribute('data-ps-key'), 0, line);
    }
  });

  // Typed quantities commit on change, so a half-typed number never fires.
  doc.addEventListener('change', function (e) {
    var input = e.target.closest ? e.target.closest('[data-ps-qty]') : null;
    if (!input || busy) return;
    var row = lineOf(input);
    if (!row) return;
    changeLine(row.getAttribute('data-ps-key'), Math.max(0, parseInt(input.value, 10) || 0), row);
  });

  /* ------------------------------------------------------------- the note */

  var noteTimer;
  doc.addEventListener('input', function (e) {
    var note = e.target.closest ? e.target.closest('[data-ps-cart-note]') : null;
    if (!note) return;
    clearTimeout(noteTimer);
    noteTimer = setTimeout(function () {
      postJSON(routes.cart_update, { note: note.value })
        .then(function () { say(attr(note, 'data-ps-saved-message', 'Note saved.')); })
        .catch(function () { /* the update button below still posts it */ });
    }, 700);
  });
})();
