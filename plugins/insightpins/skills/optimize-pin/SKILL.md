---
name: optimize-pin
description: Optimize a Pinterest pin for more clicks, saves and impressions. Use when the user wants to improve a pin's performance or conversion, make a pin more noticeable, eye-catching or clickable, fix an underperforming pin, or get improved versions of a pin to A/B test.
---

# Optimize a Pinterest pin

Turn an existing pin into better-performing versions: review it, then render improved variants with
the InsightPins connector, each designed to test one change.

## Steps

1. **Get the inputs.**
   - The current pin: an uploaded image (best), or the settings of a pin you made earlier in this conversation.
   - The destination URL (the page the pin links to). You need it to get usable photos and to keep
     the copy honest. Ask for it if missing.
   - Optional: performance numbers (impressions, saves, outbound clicks) and the current title and description.

2. **Diagnose.** Review the pin with the `review-pin` rubric. If the user gave numbers, use them:
   - Low impressions: the problem is mostly discoverability (keywords, board, freshness, topic
     demand). Improve the title, description, board and on-image keyword, and suggest posting fresh pins.
   - Impressions fine, few saves or clicks: the problem is the creative (headline, photo,
     readability, promise). Focus the variants there.
   Share the score and the top 3 fixes briefly before rendering.

3. **Plan 2-3 variants** (check `get_quota` first and tell the user how many renders this uses).
   Each variant changes one main lever, so the user learns what works:
   - **A - Headline angle**: same layout and photo, stronger headline using a different `pin-copy` angle.
   - **B - Layout and readability**: a template that puts text on a solid panel or uses a bigger
     title, with higher contrast and larger `text_size`.
   - **C - Photo and color**: a different, stronger photo from the page and a palette that
     contrasts more with it.
   Keep every variant compliant with the `pin-design` essentials. If the user has only 1 render left,
   make the single version that fixes the top problems together.

4. **Render** each variant with `render_pin` (call `extract_url` on the destination URL for photos,
   `list_templates` and `list_styles` for current options). Check each preview; re-render only for a
   real defect.

5. **Report**:
   - a short table: variant, what changed, why it should do better, image link, `edit_url`;
   - optimized Pinterest **title**, **description**, **alt text** and **board** (shared across
     variants unless the headline angle needs its own title);
   - links expire in 7 days; note the photo sources and that the user needs the right to publish them;
   - **how to test**: publish the variants as separate pins to the same URL a few days apart, wait
     2-4 weeks (pins take time to gain traction), compare saves and outbound click rate, then make
     more pins in the style of the winner.

## Without a destination URL

You can still re-render using a photo URL the user provides. An image uploaded into the chat
can't be used as the pin photo because the tool needs a URL, and the old pin can't be used as the
background because its text is baked in. If no usable photo is available, deliver the review, the
improved copy and the exact template/palette/font settings so the user can apply them on
insightpins.com.
