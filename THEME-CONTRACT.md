# Per Set · Atelier — theme contract

Everything in this theme is built against the tokens and class names in
`assets/perset-core.css` and the behaviours in `assets/perset-motion.js`.
Read those two files before writing a section. Do not introduce a second
design language.

## The brand

Per Set makes hand-painted porcelain tableware in Egypt. Three collections,
each sold as a 24-piece service (6 dinner, 6 dessert, 6 salad, 6 soup).

| Collection | Handle | Pigment key | Story |
|---|---|---|---|
| Stitches of the Wild | `stitches-of-the-wild` | `wild` | Embroidery on porcelain. Leopards, bamboo, pink parasols, stitched borders. Coral and forest green. |
| A Tale in Beads | `a-tale-in-beads` | `beads` | A story drawn one bead at a time. Beaded palms on sage, coral beaded rim. |
| Pretty Past | `pretty-past` | `past` | Vintage plates too beautiful to let go. Peacocks, roses, saffron ground. |

Voice: warm, unhurried, specific. Short declaratives. Never shouty, never
"luxury" as an adjective. Describe what the hand did, not how it makes you
feel. Egyptian pounds (EGP) are the store currency — always render prices
through the `money` filter, never hardcode a symbol.

## Design tokens

Set on `:root`. Use them; never hardcode a hex.

- Surfaces: `--ps-linen` `--ps-linen-warm` `--ps-linen-deep` `--ps-porcelain`
- Ink: `--ps-ink` `--ps-ink-soft` `--ps-ink-faint` `--ps-hairline`
- Pigments: `--ps-coral` `--ps-coral-deep` `--ps-sage` `--ps-forest`
  `--ps-saffron` `--ps-peacock` `--ps-gold`
- Semantic: `--ps-accent` (re-pigmented per collection), `--ps-wash`
- Type scale: `--ps-step--2` through `--ps-step-8` (fluid clamps)
- Space: `--ps-s-3xs` through `--ps-s-4xl`
- Motion: `--ps-ease-set` `--ps-ease-lift` `--ps-ease-swap` `--ps-ease-thread`,
  durations `--ps-t-fast` `--ps-t-base` `--ps-t-slow` `--ps-t-drape`

Re-pigment any subtree with `data-ps-pigment="wild|beads|past"`. That one
attribute swaps `--ps-accent`, `--ps-accent-2` and `--ps-wash`.

## Typography

- `Fraunces` (variable serif, SOFT + WONK axes) for everything expressive.
- `Jost` for body, labels, buttons and UI.
- Classes: `.ps-h-hero` `.ps-h1` `.ps-h2` `.ps-h3` `.ps-h4` `.ps-eyebrow`
  `.ps-lede` `.ps-prose` `.ps-em` `.ps-num`
- Never set `font-family` directly. Use `var(--ps-display)` / `var(--ps-body)`.

## Layout primitives

`.ps-shell` (+ `--narrow` `--text` `--wide` `--flush`), `.ps-section`
(+ `--tight` `--flush-top` `--flush-bottom`), `.ps-grid` (+ `--2` `--3` `--4`
`--auto`), `.ps-stack`, `.ps-row` (+ `--between` `--center`), `.ps-bleed`,
`.ps-ratio` (+ `--1` `--43` `--34` `--169` `--23`).

## Motion contract

Declare intent in markup; `perset-motion.js` does the rest.

| Attribute | Effect |
|---|---|
| `data-ps-reveal="up\|fade\|scale\|glaze\|set\|left\|right"` | Reveals on scroll. `set` is the house default: rises, un-rotates and scales in like a plate being set down. |
| `data-ps-stagger="90"` | On a parent. Children with `data-ps-reveal` inherit incremental delays in ms. |
| `data-ps-split="lines"` | Splits a heading into real line boxes that rise from behind a mask. Use on display headings. |
| `data-ps-split="chars"` | Per-character reveal. Short words only. |
| `data-ps-parallax="0.2"` | Drifts at a fraction of scroll speed. |
| `data-ps-rotate="40"` | Scroll-linked rotation in degrees, centred on viewport crossing. The signature plate move. |
| `data-ps-magnetic="0.3"` | Element leans toward the pointer. |
| `data-ps-cursor="Label"` | Swells the custom cursor and labels it. |
| `data-ps-rail` | Horizontal scroll container; pairs with `data-ps-rail-prev/next/bar`. |
| `data-ps-accordion` | On a wrapper of `<details>`; closes siblings. |

All of it is disabled under `prefers-reduced-motion: reduce`. Never animate
something that is the only way to read content.

## Components

- `.ps-btn` (+ `--ghost` `--accent` `--light` `--block` `--sm`)
- `.ps-link` — uppercase micro link with a retracting underline
- `.ps-card` — product card, rendered via `{% render 'product-card' %}`
- `.ps-plate` + `.ps-plate-shadow` — a plate with glaze and a cast shadow
- `.ps-marquee` — running text band
- `.ps-field` / `.ps-input` / `.ps-label` — floating-label form fields
- `.ps-thread` — hand-drawn rule, `{% render 'icon', name: 'thread', draw: true %}`
- `{% render 'icon', name: '…', size: 20 %}` — the icon set

## Rules

1. Semantic HTML first. One `h1` per page. Buttons are `<button>`, links are `<a>`.
2. Every image goes through `image_url` + `image_tag` with `widths`, `sizes`
   and `loading: 'lazy'` (hero images use `loading: 'eager'` and `fetchpriority`).
3. Every section needs a `{% schema %}` with real settings so the merchant can
   edit copy in the theme editor. Never hardcode marketing copy that should be
   editable.
4. All user-facing strings go through `| t` with a sensible `default:`.
5. Respect `section.settings.padding_top` / `padding_bottom` where offered.
6. No external JS libraries. No jQuery. No build step.
7. Test mentally against 360px width before you call a section done.
