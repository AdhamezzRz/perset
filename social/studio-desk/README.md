# Per Set — Studio Desk pack

Eight pieces for Instagram (and Pinterest): two carousels, three single
posts, three Reels. All 4:5 (1080 × 1350) or 9:16 (1080 × 1920).

The idea is a studio desk, not a feed. Real plate photography is treated like
paper, tape, film and ink: swatches, torn edges, pencil loops, handwritten
notes, a menu card, a ruler. Where a photograph was needed it was made to look
like one: flash, hard sun, grain, crumbs, imperfect framing.

Type: **Damion** (the closest Google font to the logo's script) for every
headline and note, **Jost** for labels, **Fraunces** italic only on the menu
card. Oxblood `#500C02`, blush `#F2A4B6`, linen.

## What is real and what is generated

| Piece | Source |
|---|---|
| Palette carousel, place setting, menu card, mood board, anatomy reel | Real product photography, cut out and cropped. Colours were **sampled from the photos**, so the hex codes are close, not exact; screens vary. |
| Evidence carousel (4 photos) | Generated in Higgsfield (GPT Image 2.5) from the real plate photos as references, then given film grain and a vignette. Plates are the real designs; the food, glassware, cloth and room are generated. |
| Three pours reel | Three keyframes generated the same way, animated with Kling 3.0 pro, graded with temporal grain. |

Meta asks for realistic AI-generated photos and video to be disclosed and may
label them automatically. Use the "AI info" toggle on the evidence carousel
and the pours reel if Instagram offers it.

Credits: 7 images × 2.75 + 3 Kling pro clips × 8.75 = **45.5**. Everything
else is composed locally and cost nothing.

## Posting order

| Day | Piece | Why |
|---|---|---|
| 1 | Reel 3 · three pours | The most thumb-stopping thing in the set. |
| 2 | Carousel 1 · colour, borrowed from porcelain | Built to be saved. |
| 3 | Post 2 · a menu for six | Saves and shares. |
| 4 | Reel 2 · anatomy of a plate | Shows the detail. |
| 5 | Carousel 2 · evidence of a good dinner | The funny one. Ask for tagged stories. |
| 6 | Post 1 · a place setting, to scale | Practical, saveable. |
| 7 | Reel 1 · the moodboard + Post 3 as a story or pin | Closes the week. |

Hashtags (8 to 12, rotate): `#perset #porcelain #tableware #tablescape
#tablesetting #setthetable #dinnerware #madeinegypt #cairo #homeware
#hostingseason #colourpalette`

---

## Captions

### Reel 3 · Three pours — `reels/reel-3-three-pours.mp4` · 16.8 s
> honey. olive oil. sumac.
> Three pours, three plates.
>
> Figs and honey on A Tale in Beads. Lentil soup and olive oil in a Pretty Past bowl. Fattoush and sumac on Stitches of the Wild.
>
> perset.shop

### Carousel 1 · Colour, borrowed from porcelain — `carousel-1-palette/` · 5 slides
> Colour, borrowed from porcelain.
> Fifteen colours from three plates, and what we'd put next to each. Hex codes are sampled from our photos, so treat them as close, not exact.
>
> Save this for your next table. Every collection is a complete 24-piece set.
> perset.shop

### Post 2 · A menu for six — `posts/post-2-menu-for-six.jpg`
> A menu for six, one piece at a time.
> Lentil soup in the bowl. Fattoush on the salad plate. Mahshi on the dinner plate. Om Ali on the dessert plate. Hibiscus over ice.
>
> Every set is 24 pieces: 6 dinner, 6 dessert, 6 salad, 6 soup. Set the table first.
> perset.shop

### Reel 2 · Anatomy of a plate — `reels/reel-2-anatomy-of-a-plate.mp4` · 12.6 s
> Anatomy of a plate.
> Stitches of the Wild, 27 cm: the parasols, the leopards, the bamboo, the stripe, the border.
>
> Five details, one plate, part of a complete set for six.
> perset.shop

### Carousel 2 · Evidence of a good dinner — `carousel-2-evidence/` · 5 slides
> Evidence of a good dinner.
> Exhibits A to D. Swipe for the full case file, and tell us what's in yours.
>
> Tomorrow: hand wash. Hand washing keeps the colours bright. Worth it.
> perset.shop

### Post 1 · A place setting, to scale — `posts/post-1-place-setting-to-scale.jpg`
> A place setting, to scale.
> Dinner plate 27 cm. Salad plate 21 cm, stacked on top. Soup bowl 12 cm in the middle. Dessert plate 21 cm, for later. Repeat × 6: 24 pieces.
>
> Save it for when you're laying the table.
> perset.shop

### Reel 1 · The moodboard builds itself — `reels/reel-1-moodboard-builds-itself.mp4` · 11.5 s · and Post 3 — `posts/post-3-moodboard.jpg`
> The moodboard.
> Stitches. Beads. Brushstrokes. A table for six, set of 24.
>
> Save it for later. perset.shop

---

## Files

```
carousel-1-palette/    5 slides, 1080 × 1350
carousel-2-evidence/   5 slides, 1080 × 1350
posts/                 3 posts, 1080 × 1350
reels/                 3 Reels, 1080 × 1920, 30 fps, silent
assets/                evidence photos (graded), pour keyframes, macro crops
src/                   the HTML builders and render scripts
```

Reels are silent so music is chosen in the app. Reel 1 suits a soft
"click" for each piece landing; reel 3 wants quiet kitchen sounds.
The 4:5 images also work as Pinterest pins.

The builders in `src/` expect the plate cut-outs, fonts and logo from the
theme assets; they are included for reference and for restyling copy.
