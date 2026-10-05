---
name: optimize-pin
description: Optimize a Pinterest pin for more clicks, saves and impressions. Use when the user wants to improve a pin's performance or conversion, make a pin more noticeable, eye-catching or clickable, fix an underperforming pin, or get improved versions of a pin to A/B test.
---

# Optimize a Pinterest pin

Turn an existing pin into better-performing versions: review it, then render improved variants with
the InsightPins connector. Each variant tests one change, so the user learns what works.

## Steps

1. **Get the inputs.**
   - The current pin: an image shared in the chat (best), or the settings of a pin you made earlier in this conversation.
   - The destination URL (the page the pin links to). You need it to get usable photos and to keep
     the copy honest. Ask for it if missing.
   - Optional: performance numbers (impressions, saves, outbound clicks) and the current title and description.

2. **Diagnose.** Review the pin with the `review-pin` rubric. If the user gave numbers, find where
   people drop off:
   - **Low impressions:** people don't see it. Mostly discoverability: keywords in the title,
     description and on-image headline, the board, freshness and topic demand. Improve the copy and
     board, and suggest posting fresh pins.
   - **Impressions fine, few saves:** the pin doesn't look worth keeping. Work on the photo, the
     promise and how readable the pin is at thumbnail size.
   - **Saves fine, few outbound clicks:** the pin gives no reason to click. Make the promise
     specific about what's on the page ("7 make-ahead breakfasts", "the full packing list"), match
     the button text to that payoff, and make sure the headline doesn't already give everything away.
   - **Clicks fine, but the user says visitors leave:** the pin and the page don't match. Make the
     pin promise exactly what the page delivers; the page itself is outside what the pin can fix.
   Share the score and the top 3 fixes briefly before rendering.

3. **Plan 2-3 variants** (check `get_quota` first and tell the user how many renders this uses).
   Give each one a short hypothesis: what it changes and why it should do better. Each changes one
   main lever:
   - **A - Headline:** the closest layout, palette and photo to the original, with a stronger
     headline using a different `pin-copy` angle (a number, an outcome, a problem solved). "Same
     photo" means the original photo from the page (or the user's original, uploaded), never the old
     pin image.
   - **B - Layout and readability:** a template that puts the headline on a solid panel or makes it
     bigger, with a palette from the template's "Readable with" list in `create-pin`'s `references/template-colors.md` and `text_size: "auto"`.
   - **C - Photo and color:** a different, stronger photo from the page (use `image_details`: a large
     portrait photo whose `alt` matches the promise) and a palette that stands apart from it by
     lightness and fits the topic's mood. It reuses B's template, so its palette must be in that
     template's "Readable with" list too. Use `image_focus` or `image_zoom` when the subject was
     cut off or too small.
   **Keep the comparison fair:** B and C reuse A's headline (or the original one, if the headline
   wasn't a problem), and C reuses B's template, so A vs the original tests the headline, B vs A
   the layout and readability (template, palette, text size), and C vs B the photo and color. If
   the original has no photo (a text-only or quote pin), B is the same headline on a photo template
   with the page's best photo, and C swaps that photo and palette. Keep the brand's palette and
   fonts in A, and in B and C when they are in the template's "Readable with" list. Apart from A,
   which keeps the original's palette on purpose, never pick a palette outside that list (or
   outside "Also without a button" when you hide the button).
   **Low on renders:** with 2 left, make A and B. With 1 left, make the single version that fixes
   the top problems together, and say it can't show which change helped. With none left, don't
   render: deliver the review, the copy and the settings (see the last section) and say when the
   limit resets.

4. **Render** each variant with `render_pin` (call `extract_url` on the destination URL for photos,
   `list_templates` and `list_styles` for current options). Check each preview and its `warnings`
   (see `create-pin`); re-render only for a real defect.

5. **Check that each variant is really better.** Score each preview with the `review-pin` rubric.
   A variant must beat the original on the criterion it targets and must not lose on any other. In
   particular, check every piece of text, not only the headline: a bold color that makes the
   subtitle, site name or button text fade is a new defect, not an improvement. Fix it with one
   re-render (a palette from the template's "Readable with" list, or hide the subtitle) if renders
   allow; otherwise report the
   variant with the problem named and the fix to apply on insightpins.com through its `edit_url`.
   If the tool returned no preview, say you couldn't check the variants and what to look at.

6. **Report**:
   - a short table: variant, what changed, hypothesis, rubric score, image link, `edit_url`;
   - optimized Pinterest **title**, **description**, **alt text** and **board** (shared across
     variants unless the headline angle needs its own title), written with the `pin-copy` skill;
     headlines and copy use only facts the page states, with no added numbers, audiences, results
     or effects ("the 12 lessons I learned", not "the lessons that made it stick" or "perfect for
     busy families");
   - links expire in 7 days; note the photo sources and that the user needs the right to publish them;
   - **how to test**:
     - publish each variant as a new pin to the same URL and board, a few days apart, and keep the
       original live;
     - compare rates, not totals: save rate (saves / impressions) and outbound click rate
       (outbound clicks / impressions), from Pinterest Analytics;
     - wait 2-4 weeks and for at least about 1,000 impressions per pin before picking a winner;
       below that, small differences are noise;
     - then make more pins in the winner's style and test the next lever.

## Without a destination URL

You can still re-render with a photo URL the user provides, or with their original photo (the one
without text), uploaded as described in `create-pin`'s `references/user-photos.md` (and tell them it is
kept on InsightPins for 7 days). Never upload the
old pin itself: its text is baked in and would show under the new text. If no usable photo is
available, deliver the review, the improved copy and the exact template/palette/font settings so
the user can apply them on insightpins.com.
