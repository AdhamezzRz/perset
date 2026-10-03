# Per Set — Story: *Opening day*

A five-frame Instagram Story that tells people the store is open. 1080 × 1920,
30 fps, silent. Post the frames in order.

Same system as the feed campaign: **Damion** for headlines and hand-written
notes (the closest Google font to the logo's script), **Jost** for labels, the
oxblood `#500C02` / blush `#F2A4B6` / linen `#F4EEE4` palette, the blush ticket
edge, stitched dashed rules.

## The frames

| # | File | Length | What happens |
|---|---|---|---|
| 1 | `story-1-were-open.mp4` | 6.3 s | An oxblood shop shutter with the logo and a taped note, "back in a minute, setting the table". It rattles, jolts and rolls up on a Cairo doorway with a laid table inside, a pink parasol leaning on the frame. "We're open." |
| 2 | `story-2-the-receipt.mp4` | 8.2 s | A receipt prints line by line for a table of six: 1 × complete set, 24 pcs, the four piece sizes, double-boxed, across Egypt, total "one good table", then an OPEN NOW stamp lands. |
| 3 | `story-3-pick-your-plate.mp4` | 7.0 s | The three dinner plates drop in one by one and spin lazily, each with its line: leopards under a pink parasol, a palm built bead by bead, a peacock among roses. "Pick your plate." |
| 4 | `story-4-saved-you-a-seat.mp4` | 5.9 s | Overhead, a table laid for six. A hand sets the last plate down and slips away. "Saved you a seat." |
| 5 | `story-5-set-your-table.mp4` | 5.0 s | Closing card with a hand-drawn arrow into a clear space for the link sticker. |

## Stickers to add in Instagram

- **Frame 3:** a Questions sticker reading *"Which plate is yours? a, b or c"*,
  placed under the hint line, around the lower third. Reply to every answer
  with the matching set.
- **Frame 5:** a Link sticker reading *"Set your table"* pointing to
  `https://perset.shop/pages/set-your-table` (the site's interactive place
  setting). Put it in the empty space between the arrow and the logo.
- **Any frame:** a music or sound sticker. The frames are silent on purpose.
  Frame 1 wants a shutter clack as it rolls up, frame 2 a printer or a
  typewriter, frame 3 a few porcelain taps. Higgsfield has no sound-effect
  model, so use Instagram's audio library.

The receipt prints no prices because the catalogue prices are still
placeholders. Its shipping lines reuse the store's own cart note.

## How it was made

- **Higgsfield:** two scenes generated from the store's product photography as
  references (GPT Image 2.5, so the plates in them are the real designs), then
  animated with Kling 3.0: the shop doorway (std) and the hand setting the
  plate (pro). Kling job ids: `c287daaf-3903-4a6f-b2bb-9a2bd9a20cdf` and
  `f618567e-dfff-45d0-babe-604de597bf24`.
- **Local:** the shutter, receipt, spinning plates, titles and link card are
  HTML timelines rendered frame by frame with Playwright and composed with
  ffmpeg. They cost no credits.
- **Credits:** 2 images at 2.75 + Kling std 7.5 + Kling pro 8.75 = **21.75**.

## Re-rendering

```
src/common.py          shared fonts, logo mask, easing helpers
src/build_s1..s5.py    write each frame's HTML timeline
src/render.js          node render.js page.html outDir fps seconds png|jpeg transparent(0|1)
src/assemble_story.py  ffmpeg: overlays on the Kling clips, encodes frames, builds a preview
assets/                the two generated scenes and the three plate cut-outs
```

The Kling clips are not stored here; `assemble_story.py` expects them as
`k1.mp4` (doorway) and `k2.mp4` (hand and plate) next to the rendered frame
folders. Fonts are the latin subsets of Damion and Jost from Google Fonts,
embedded in `src/fonts_embedded.css`.
