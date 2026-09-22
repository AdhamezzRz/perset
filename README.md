# Per Set · Atelier

A custom Shopify theme for **Per Set** — hand-painted porcelain tableware,
made in small runs in Egypt.

Live store: [perset.shop](https://perset.shop)

---

## What this is

A theme built from scratch around the brand's own photography rather than a
marketplace template with the colours changed. The design language comes from
three things that are physically in every product shot:

- **Linen** — the cloth every piece is photographed on. It is the page
  background, and a woven texture sits under the whole site at about 5%
  opacity.
- **Glaze** — the specular highlight on a fired plate. It tracks the pointer
  across every plate on the site, so the discs read as curved rather than flat.
- **Thread** — the stitched borders painted onto the porcelain. Every rule,
  underline and divider is drawn as stitching, and several of them draw
  themselves as you scroll.

## The signature moments

| Where | What happens |
|---|---|
| Home hero | A plate sits *between* the lines of the headline and turns as you scroll, the way you would turn a piece over in your hands. |
| Collection stories | Three full-height panels that stick and stack, each re-pigmented to its own collection. |
| Set your table | An interactive place setting. The four pieces of a service are drawn at their **true relative sizes** — the 27 cm dinner plate really is 2.25× the 12 cm bowl. Switching collection re-lays the whole setting. |
| Everywhere | A porcelain-rim cursor that swells and labels itself over anything interactive. |
| Everywhere | Headlines split into real line boxes and rise from behind a mask. |

All of it is switched off under `prefers-reduced-motion: reduce`.

## Architecture

```
assets/
  perset-core.css     Design system: tokens, reset, type, layout, components
  perset-motion.js    Motion engine. One rAF loop, no dependencies.
  perset-cart.js      Progressive-enhancement cart. Falls back to form POST.
layout/
  theme.liquid        The shell
  password.liquid     Standalone coming-soon layout
sections/             Every section carries its own scoped {% stylesheet %}
snippets/             icon, product-card, meta-tags
templates/            JSON templates composing the sections
config/               settings_schema + settings_data
locales/              en.default + en.default.schema
```

**No build step. No framework. No dependencies.** Two fonts from Google
(Fraunces and Jost), everything else is in this repo.

### Colour

Tokens are sampled directly from the collection photography, so the interface
and the porcelain are speaking the same language. Any subtree can be
re-pigmented with a single attribute:

```html
<section data-ps-pigment="wild">   <!-- coral + forest green -->
<section data-ps-pigment="beads">  <!-- sage + coral        -->
<section data-ps-pigment="past">   <!-- saffron + peacock   -->
```

That swaps `--ps-accent`, `--ps-accent-2` and `--ps-wash` for everything
inside it.

### Motion

Sections declare intent in markup; `perset-motion.js` does the work.

```html
<div data-ps-stagger="90">
  <h2 data-ps-split="lines">Every set tells its own story</h2>
  <img data-ps-parallax="0.2">
  <div class="ps-plate" data-ps-rotate="55">
</div>
```

See `THEME-CONTRACT.md` for the full attribute reference.

## Working on it

There is no local build. Edit the files and push them to an **unpublished**
theme to preview:

1. Shopify admin → Online Store → Themes
2. Open **Per Set · Atelier** → Preview
3. Customise to edit section settings in the theme editor

Before changing anything, read `THEME-CONTRACT.md`. It exists so the site
keeps speaking one language.

### Validating

```bash
python3 tools/validate.py
```

Checks that every `{% schema %}` block is valid JSON, that every JSON template
and locale parses, and that Liquid tags are balanced across the theme.

## Status

Prices on the catalogue are **placeholders** and every product ships with zero
tracked inventory and a deny policy, so nothing is purchasable until real
prices and stock are set in admin. That guard is deliberate.
