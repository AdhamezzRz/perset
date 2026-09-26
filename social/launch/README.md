# Per Set — launch campaign: *On the plate. On the table.*

Nine posts to open the Per Set Instagram: six 4:5 feed posts (1080 × 1350)
and three Reels (1080 × 1920). One idea runs through all of them.

## The idea

Every Per Set collection carries a small world on the plate: leopards under a
pink parasol, a beaded palm, a peacock among roses. The campaign takes that
world off the plate and puts it on the table around it. The parasol on the
plate becomes the parasol over lunch. The palm on the plate becomes the palm
over breakfast. The painted roses sit next to picked ones.

That gives the brand a repeatable, ownable visual device (the motif appears
twice, once painted and once real), a hand-written "spot it" annotation style
that makes people look twice, and a line that carries the brand's own idiom:

> **Beautiful per piece. Perfect per set. On the plate, on the table.**

## Type and system

- **Damion** (Google Fonts) is the campaign script. It is the closest match
  to the hand-lettered logo: monoline, same weight, same slant and bounce.
  It is used only for headlines and the hand-written notes, never body copy.
- **Jost** for labels, as on the site. Fraunces is kept for the store.
- Oxblood `#500C02`, blush `#F2A4B6`, linen `#F4EEE4`. The blush ticket edge
  from the site hero frames the cards.
- The lifestyle scenes were generated from the real product photography as
  references (GPT Image 2.5 via Higgsfield), so the plates in them are the
  actual Per Set designs. They are shot to read as 35 mm editorial film:
  Cairo balconies and gardens, real light, a hand in frame, crumbs.

Voice rules from the brief still hold: warm and specific, never "luxury",
and none of "hand painted / hand drawn / fired in small runs / no two alike".

## Credits used

| What | Model | Credits |
|---|---|---|
| 6 lifestyle worlds + 3 packshots | GPT Image 2.5, high, 2k | 24.75 |
| 3 motif-alive clips (pro) | Kling 3.0 | 26.25 |
| 3 living-scene clips (std) | Kling 3.0 | 22.5 |
| Stop-motion reel, cards, overlays, 6 posts | composed locally | 0 |
| **Total** | | **73.5** |

---

## Posting order

```
Row 1:  01 Same parasol        02 Own palm            03 Painted and picked
Row 2:  R1 Into the plate      04 Guests: six         R2 The table sets itself
Row 3:  05 Which table?        R3 They know you're    06 per piece. per set.
                                  looking
```

Post 01 first. R1 is the campaign film and should go up with a pinned
comment linking the shop. R3 is the loop built for shares and saves.

Hashtags (8 to 12, rotate): `#perset #porcelain #tableware #tablescape
#tablesetting #dinnerware #madeinegypt #cairo #homeware #setthetable
#hostingseason #tabledecor`

---

## Feed posts

### 01 — Same parasol  `01-wild-same-parasol.png`
Lunch in a bamboo garden under a real pink parasol; hand-written notes point
from "her parasol" (the real one) to "his parasol" (on the plate).

> Her parasol. His parasol.
> Lunch under bamboo, on the plate and over the table.
>
> Stitches of the Wild — a complete set for six.
> perset.shop

### 02 — Own palm  `02-beads-own-palm.png`
Breakfast on a Cairo balcony, palm shadows across the plate. Notes: "this
palm" (the balcony) and "that palm" (on the plate).

> Breakfast under its own palm.
> Cairo, 8 a.m. Tea, figs, and A Tale in Beads.
>
> A complete 24-piece set for six.
> perset.shop

### 03 — Painted and picked  `03-past-painted-picked.png`
Golden hour, garden roses lying beside the plate, one petal on the rim.

> Roses, painted and picked.
> Pretty Past at golden hour, with a peacock feather for company.
>
> A complete set for six.
> perset.shop

### 04 — Guests: six  `04-guests-six.png`
The dusk dinner with a three-line ledger.

> Guests: six.
> Pieces: twenty-four.
> Reasons to host: unlimited.
>
> Perfect per set. perset.shop

### 05 — Which table are you?  `05-which-table.png`
Three worlds, three answers. Built to be answered.

> Which table are you?
> a. The long lunch
> b. The slow Saturday
> c. The dinner that runs late
>
> Answer below. We'll tell you which set is yours.

### 06 — per piece. per set.  `06-per-everything.png`
Type only, in the campaign script.

> per piece. per set. per table. per Sunday.
> Porcelain tableware, made in Cairo.
>
> Now open — perset.shop

---

## Reels

### R1 — Into the plate  `reel-01-into-the-plate.mp4` · 22 s
"What's on the plate..." then the camera dives into the parasol on the plate
and comes out at a real lunch under a real parasol. Same again for the palm
and the roses. Ends on the logo.

> What's on the plate is on the table.
> Three collections, three tables. Now open — perset.shop

Sound: a warm, slightly cheeky instrumental; cut the beat on each dive.

### R2 — The table sets itself  `reel-02-table-sets-itself.mp4` · 19 s
Stop-motion. Six place settings drop onto the linen piece by piece while the
count runs to 24. Cut from the real plates, so every piece is the real
design.

> A table for six, in 24 pieces. Watch it set itself.
> 6 dinner · 6 dessert · 6 salad · 6 soup. perset.shop

Sound: one porcelain "tink" per piece works best (24 taps), or a clean
stop-motion sound from the library.

### R3 — They know you're looking  `reel-03-they-know-youre-looking.mp4` · 12 s
The leopards turn their heads and blink. The peacock fans its tail and the
painted roses bloom into real ones. Built to loop.

> They know you're looking.
> Beautiful per piece. perset.shop

Sound: something quiet with a small "boing" or wink on the blink.

---

## Files

```
social/launch/
  01-… 06-….png                 feed posts, 1080 × 1350
  reel-01/02/03-….mp4           reels, 1080 × 1920, 30 fps, silent
  worlds/w11…w32.jpg            the six generated lifestyle scenes, 1792 × 2240
  src/                          build_posts.py (HTML → PNG), assemble_reels.py,
                                stopmotion_frames.js, shoot.js
```

Reels are exported silent on purpose so music is chosen in-app. Every piece
points to perset.shop; the end cards can be re-rendered with the Instagram
handle from the sources if the domain is down on launch day.
