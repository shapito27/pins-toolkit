---
name: remake-pin
description: Make a new Pinterest pin in the style of an uploaded pin, but better. Use when the user uploads a pin and asks for one like it, a similar pin, a better version, the same style for their own content, or "make me a pin like this".
---

# Remake a pin: similar style, better pin

The user shows a pin they like. You make a new, original pin for their content that keeps what
works about that pin's style and fixes what doesn't.

## Steps

1. **Get the inputs.**
   - The reference pin (uploaded image).
   - Their content: the destination URL for the new pin. If the reference pin is their own, this
     may be the same page. Ask for it if missing.
   - Whose pin is it? If it isn't clearly theirs, treat it as inspiration only (see Originality).

2. **Analyze the reference pin.** Note:
   - layout type (full-bleed overlay, split, text panel, collage, quote, list with number badge...);
   - text hierarchy (headline size, subtitle, number, CTA, site name);
   - color mood (warm/cool, light/dark, bold/soft) and font mood (bold sans, elegant serif, playful);
   - the angle of the headline (list, how-to, outcome...);
   - what works and what's weak, using the `review-pin` rubric. Keep this short.

3. **Map it to InsightPins.** Call `list_templates` and `list_styles` and pick the closest template,
   palette and font pairing. Say in one line how close the match is ("closest layout is
   `split-horizontal`; the reference has a curved divider we don't have").

4. **Get the content and photo.** Call `extract_url` on the destination URL and check that the page
   really loaded, as in `create-pin` step 1 (bot-check pages come back without an error). Choose a photo that
   fits the reference's look (similar framing and brightness) and the `pin-design` rules.
   An image uploaded into the chat can't be used as the pin photo (the tool needs a URL), and the
   reference pin can't be used as a background because its text is baked in.

5. **Write better copy** with the `pin-copy` skill: keep the reference's angle if it fits the
   content, but make the headline more specific and readable. Use only facts the user's page
   states, never claims from the reference pin or added results.

6. **Improve, don't just copy.** Fix the weak points you found: larger or higher-contrast headline
   (choose the palette with the contrast table in `create-pin`'s `references/style-selection.md`),
   cleaner hierarchy, better photo, a real number, a clearer promise.

7. **Render** with `render_pin` and check the preview. Re-render only for real defects.

8. **Report**:
   - image link and `edit_url`; template, palette and font used;
   - "What's similar" (1-2 lines) and "What's better" (2-4 bullets) compared with the reference;
   - Pinterest title, description, alt text, board;
   - link expires in 7 days; photo source and the need for rights to publish it.

## Originality

- When the reference pin is someone else's, use it only for style: layout type, mood, angle.
- Never copy their photo, their exact headline or text, their logo or their brand name.
- If the user asks for an exact copy of another creator's pin, explain briefly that you'll make an
  original pin in a similar style instead, and do that.
