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

## The logo and the credit

- The hand-lettered **per set** mark now carries the brand: header, menu
  overlay, footer, the coming-soon page, and the veil that covers each page
  as it loads. It is one file rendered through a CSS mask, so it is oxblood
  on linen and blush on oxblood without a second asset.
- The logo's own two colours, sampled from the file, are in the palette as
  `--ps-oxblood` (#500C02) and `--ps-blush` (#F2A4B6). Buttons, the footer,
  the veil and text selection use them.
- **The veil doubles as the preloader.** It holds about a second on the first
  page of a visit, lifts almost at once on every page after, and a hard
  timeout lifts it regardless. It is never shown without JavaScript and is
  removed for anyone who asks for reduced motion.
- The favicon and the social share image are the mark on its oxblood ground.
- The footer reads **Powered by Najmarketing.co**, linked. Both the text and
  the link are settings on the footer section, and Shopify's own credit can
  be switched on beside it if you ever want it.

## The code

Lives at `github.com/AdhamezzRz/perset`, branch `claude/trusting-faraday-i1jsf8`.

No build step, no framework, no dependencies. Two fonts from Google, and
everything else is in the repo.

- `README.md` — what it is and how it is put together
- `THEME-CONTRACT.md` — the design system, so future work stays in one language
- `tools/validate.py` — checks schemas, JSON, Liquid balance, missing
  snippets and missing assets

---

## Round 2 — the design review

You sent through Judy and Dana's scroll-through of the preview, plus the
thank-you-card PDF as inspiration for the hero. This is what changed:

- **Header** — the inline nav is gone; the logo is centred; one burger on
  the left opens the full-screen menu (this also fixed a real bug: the
  desktop burger had no click handler at all, only the mobile one did).
  A favourites icon sits in the tools on the right.
- **Hero** — the plate and "A Table Worth Staying At" are gone. In their
  place: an oxblood section with the blush ticket-edge stripe from the
  thank-you card, the logomark, and "Beautiful per piece / perfect per
  set." The hand-painted eyebrow line was removed from here, nowhere else
  — see the flag below.
- **Collections intro** — the old lede, buttons and stray "LL" are gone.
  Copy is now "The Collections" / "The making of a set" / the new body
  line. The marquee's "Service for six" slot is now the logomark instead.
- **Collection panels** (Stitches / Beads / Past) — the description no
  longer truncates, there is one pill ("24-Piece Set") instead of two, and
  the button reads "View Collection." All three now use a single,
  consistently cropped plate image rather than a flat-lay.
- **Set your table** — rebuilt. It was a stacked, hover-to-reveal
  composition; it is now a picker: choose Dinner, Salad, Soup or Dessert
  and see that one piece alone, in the same square crop every time. Copy
  is now "Inside the Set" / "Everything you need to set a table of six,
  choose a plate and explore."
- **Favourites** — Shopify has no wishlist of its own, so this is a
  localStorage one: a heart on every product card and on the product page,
  a `/pages/favourites` page that shows whatever is saved, and the count
  in the header. It only remembers on the device it was saved on — there
  is no account sync. If you outgrow that later, it is a real app
  (Shopify has a few) rather than something to patch in.
- Caught while sweeping the preview afterwards: the reel strip's play
  button had a missing translation string. Fixed, unrelated to the review.

~~**One thing to confirm with the client:**~~ Resolved in the next round —
see below. It was a statement about the product, not just about where
that line sat.

---

## Round 3 — sold as a set, not by the piece

Judy's next note settled the question round 2 left open, and went
further: **plates are sold only as the complete 24-piece set, never as
separate dinner/salad/soup/dessert listings**, and every trace of "hand
painted", "hand drawn", "fired in small runs" and "no two alike" comes
off the site.

- **Catalog** — each collection already had a bundled "Complete
  Service, 24 Pieces" product sitting alongside its four separate piece
  products (from the very first build). The fix was to stop showing the
  four separate ones: they're off every collection, off the new "Shop
  all", off both nav menus — a collection page now shows exactly the one
  product that's actually for sale. Shopify's automatic "all products"
  collection can't be filtered, so a real collection (handle
  `frontpage`, titled "Shop all", reusing the store's unused leftover
  "Home page" collection) now stands in for it everywhere in the theme.
  **The four piece products per collection are still live** — status
  Active — because "Set your table" needs their photos and Liquid can't
  read a product that isn't published to the Online Store. They're
  unreachable through any link, nav, or collection the theme controls,
  but Shopify's own site search still indexes them, so a very specific
  search could still surface one at its old per-piece price. Closing
  that fully means either giving the picker its own dedicated images
  instead of borrowing product photos, or accepting that loss of the
  picture-per-piece (several pieces, especially in Pretty Past, don't
  have a distinct clean crop the way the dinner plates do — that's a
  photography gap, not a code one). Flagging it rather than guessing.
- **Set your table** — moved off the homepage onto its own page at
  `/pages/set-your-table`, and into the main nav.
- **Shop all** — the header's full-screen menu now nests Stitches of
  the Wild, A Tale in Beads and Pretty Past under "Shop all" as a
  dropdown, using the browser's native disclosure element so it needs no
  extra JavaScript.
- **Footer** — the scrolling "Hand painted · Fired in small runs · No
  two alike · Made in Egypt" banner is gone; "First look at the next
  firing" is now a plain "Keep in touch"; the tagline under the logo now
  reads "Beautiful per piece, perfect per set."
- **Homepage** — the reel strip ("In motion"), the "Start here" featured
  row and the craft-process section are removed, per the client's list of
  pages to drop. Their section files are still in the repo, just unused,
  in case any of them comes back later.
- **Copy purge** — "hand painted", "hand drawn", "fired in small runs"
  and "no two alike" (and close paraphrases like "painted by hand," "not
  identical") are out of every section default, template, collection
  description and the three sellable products' own descriptions. Two FAQ
  questions that existed only to explain hand-variation were removed
  outright rather than reworded, since there was no honest way to answer
  them under the new positioning.

---

## Known loose ends

- `assets/perset-writetest.css` is a 23-byte leftover from checking write
  access. Theme file deletion is blocked through the API, so remove it in the
  theme's code editor if it bothers you. It is unreferenced and inert.
- The base theme's other language files (German, French, and so on) are still
  in the theme. They carry the old theme's translation keys, not this one's,
  so any missing string falls back to the English written into the templates.
  Harmless, but you may want to delete them.
- The "Default example products" collection from the original setup is
  still there and unused. Its sibling, "Home page", is no longer unused —
  it's now the curated "Shop all" collection, see Round 3 above.
