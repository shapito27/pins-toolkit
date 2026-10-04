---
name: pin-design
description: Pinterest pin visual design best practices. Use when choosing or judging how a pin looks - layout, text overlay, readability, contrast, colors, fonts, photo choice, branding - when checking a rendered pin preview for defects, or when the user asks how to make pins more eye-catching or noticeable.
---

# Pinterest pin design

A pin competes in a crowded grid, mostly on phones, where each pin is shown small (around
200-250 pixels wide). Design for that size first. Use the full checklist in
[references/design-checklist.md](references/design-checklist.md) when checking a preview or reviewing a pin.

## The essentials

1. **Vertical 2:3.** 1000x1500 is the standard. Much taller pins get cut off in the feed; square
   and horizontal pins take less space and get less attention.
2. **Readable at thumbnail size.** If you shrink the pin to a quarter of its size, the headline must
   still read at a glance. That means few words (3-8 is ideal), large, heavy type, and strong
   contrast with what's behind it.
3. **Contrast for every piece of text.** The subtitle and site name are small and regular weight,
   so they need even more contrast than the headline (a 4.5:1 contrast ratio or more); bold button
   labels need at least 3:1. Light text on a mid-tone panel or button (coral, orange, bright blue,
   lime, turquoise) works for a huge headline at best and fails for small text: use a dark panel,
   or dark text on a light background. The `create-pin` skill's `references/template-colors.md`
   lists the readable palettes for each template.
4. **One focal point.** One clear photo subject and one headline. Not three ideas, not five text blocks.
5. **Text on a calm area.** Put text on a solid band, panel or quiet part of the photo, never across
   faces, food or busy detail. If the photo is busy everywhere, choose a template with a text panel.
6. **Right photo.** Sharp, bright, relevant to the headline, showing the result or benefit (the
   finished dish, the styled room, the place itself). Real-life context usually beats a plain
   cut-out, except for clean product shots. Vertical photos for full-bleed layouts; horizontal ones
   belong in a panel, or the crop cuts off heads and products.
7. **Clear promise.** The pin says what the click gives: "15 Easy Weeknight Dinners", not
   "My Favorite Things". Concrete beats clever.
8. **Branding, quietly.** Site name on every pin, same few palettes and fonts across a site's pins.
   A small, consistent brand mark builds recognition; a large logo looks like an ad.
9. **Hierarchy.** Headline biggest, subtitle smaller, button and site name smallest. Two fonts at most.
10. **Safe edges.** Keep important text away from the outer edges and the bottom-right corner,
    where Pinterest places its own buttons on some screens.
11. **Color that fits.** The palette should fit the topic's mood and stand apart from the photo by
    lightness (dark panel next to a bright photo, light panel next to a dark one). Hot red or coral
    on a calm winter or wellness photo grabs attention, but it clashes with the promise and looks
    like an ad.

## Common defects to catch in a preview

- Headline cut off, wrapping into 4+ lines, or too small to read at thumbnail size (the most common
  defect: template default text sizes are often too small for short headlines).
- A big empty area with small text in it (raise the text size to fill it).
- Text baked into the photo (captions in GIFs or screenshots) showing through or cut off by the crop.
- Text over a busy or same-colored part of the photo.
- A field showing a value that isn't true for the content (a guessed price, count or cook time).
- Photo cropped badly: subject cut in half, heads cut off, product off-frame (fix with
  `image_focus`, or `image_fit: "contain"`), or a product sitting small in a big frame (`image_zoom`).
- Low-resolution, blurry, or stretched photo; a photo with its own text or watermark.
- Colors that blend into the photo; subtitle that's too long to read.
- Subtitle, site name or button text faded or low-contrast, even when the headline reads well
  (common on mid-tone color panels and on templates that draw small text in a light color).
- A palette that fights the topic's mood or the photo (hot coral on a snowy scene, neon on a calm
  wellness photo).

Fix the one thing that's wrong with the smallest change (text size, photo position, photo, template)
and keep the rest. The render result's `warnings` point at most of these defects.

## What not to do

- No misleading images or headlines (a photo that isn't what the page delivers). Pinterest limits
  misleading and spammy content, and it loses trust and clicks anyway.
- No fake play icons, fake app controls or "click here" gimmicks. A small button-style label that
  names what the click gives ("Get the Recipe", "Read the Guide") is fine.
- No walls of text. If it needs a paragraph, it belongs in the description.
