# Per Set — handover

What was built, what is real, and what still needs you.

---

## Before you publish

These are the things that are deliberately unfinished. Nothing here is a bug.

### 1. Prices are placeholders

Every product carries a made-up price:

| Product | Placeholder (EGP) |
|---|---|
| Dinner plates, set of 6 | 4,800 |
| Dessert plates, set of 6 | 3,900 |
| Salad plates, set of 6 | 3,900 |
| Soup bowls, set of 6 | 4,200 |
| Complete service, 24 pieces | 15,600 |

**Nothing can be bought at these prices.** Every product ships with inventory
tracked, quantity 0, and a deny policy, so the add-to-cart button is inert.
Set your real prices, then set stock. Do it in that order.

### 2. Contact details are blank

The contact page shows "Cairo, Egypt" and nothing else, because nothing else
is known. Fill in the address, email, phone and opening hours in the theme
editor under the contact page's form section. Empty fields simply do not
render, so the page stays tidy until you fill them.

### 3. Social links are blank

Same reason. Add them under Theme settings → Social. Each icon appears only
once its link is set. WhatsApp takes a number, not a URL.

### 4. Four products are using stand-in photography

There are 14 usable photographs for 15 products, so some pieces are shown by a
collection shot rather than their own. These four have no photograph of the
actual piece anywhere in the source material:

- Stitches of the Wild — Dessert Plates
- Stitches of the Wild — The Complete Service
- Pretty Past — Dessert Plates
- Pretty Past — Salad Plates

One more is uncertain: **A Tale in Beads — Dessert Plates** uses a shot where
the stacked top plate might be the salad plate. Worth checking.

Stitches of the Wild is the thinnest — two photographs covering five products.
If you shoot anything next, shoot that.

---

## What is real

- **3 collections**, with the copy you supplied, used verbatim.
- **15 products**, 5 per collection: four sets of six, plus the 24-piece
  complete service. Sizes, piece counts and descriptions are yours as written.
- **22 photographs** processed and uploaded, including square crops of the
  individual pieces cut from the high-resolution flat lays.
- **5 studio reels** uploaded. Four are shown in the "In motion" strip.
- **6 pages** written: Our Story, Care, Shipping, Returns, FAQ, and the
  existing Contact page.
- **Navigation** rebuilt: main menu, footer shop menu, footer information menu.

The four placeholder demo products that came with the store have been
archived, not deleted. They are recoverable if you want them.

---

### 5. The reels are very short

All five clips run between 0.8 and 2.0 seconds, so they read as looping
cinemagraphs rather than films. That is what was in the folder, not something
that happened in processing — they transcoded cleanly at full length.

They also arrived in three different shapes: reels 1 and 2 are portrait, reel
3 is landscape, reel 4 is square, and reel 5 is reel 4 letterboxed to 16:9.
The strip uses square frames, which is the only crop that treats all three
shapes fairly, and reel 5 is not used because it duplicates reel 4 with black
bars. If you shoot longer clips, the frame shape is a section setting and the
strip takes up to eight.

---

## The theme

Installed as **Per Set · Atelier (Claude build)**, unpublished. Your previous
themes are untouched: `Horizon` is still live and `Whisper` is still there as
a backup.

**Preview link:**
`https://perset.shop/?preview_theme_id=166988251321`

That link works for anyone you send it to, no login needed. Click through it,
and publish it yourself when you are happy. It will not go live on its own.

Every page was checked in a real browser at 1440 px and at 390 px: ten pages,
all passing, with no Liquid errors, no missing translation strings, no stuck
animations and no horizontal scrolling. Re-run that check any time with
`node tools/verify-pages.mjs` and `--mobile`.

### What is worth looking at

- **The homepage hero.** The plate sits between the lines of the headline and
  turns as you scroll.
- **The collection stories.** Three full-height panels that stack as you move
  down, each one re-coloured to its own collection.
- **Set your table.** The four pieces of a service drawn at their true
  relative sizes — the 27 cm dinner plate really is 2.25× the 12 cm bowl.
  Switch collection and the whole setting is re-laid.
- **In motion.** The reels, at the shape they were shot in. Each plays only
  while it is on screen.

Everything is editable in the theme editor. Every headline, every piece of
copy, every image is a setting, not hardcoded.

### How it behaves

- Motion switches off entirely for anyone whose system asks for reduced
  motion, and the reels never autoplay for them.
- Reels also do not autoplay when the browser reports Save Data.
- The site is readable with JavaScript switched off or failed. Nothing is
  hidden behind a script.
- Filtering and sorting on collection pages work without JavaScript.
- The cart works without JavaScript; the script only removes the page reload.

---

## The code

Lives at `github.com/AdhamezzRz/perset`, branch `claude/trusting-faraday-i1jsf8`.

No build step, no framework, no dependencies. Two fonts from Google, and
everything else is in the repo.

- `README.md` — what it is and how it is put together
- `THEME-CONTRACT.md` — the design system, so future work stays in one language
- `tools/validate.py` — checks schemas, JSON, Liquid balance, missing
  snippets and missing assets

---

## Known loose ends

- `assets/perset-writetest.css` is a 23-byte leftover from checking write
  access. Theme file deletion is blocked through the API, so remove it in the
  theme's code editor if it bothers you. It is unreferenced and inert.
- The base theme's other language files (German, French, and so on) are still
  in the theme. They carry the old theme's translation keys, not this one's,
  so any missing string falls back to the English written into the templates.
  Harmless, but you may want to delete them.
- The "Home page" and "Default example products" collections from the original
  setup are still there and unused.
