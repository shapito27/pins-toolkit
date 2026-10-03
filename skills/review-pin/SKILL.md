---
name: review-pin
description: Review and score a Pinterest pin. Use when the user uploads or shares a pin image and asks for feedback, a review, a score, a critique, "what's wrong with this pin", "is this pin good" or "why isn't my pin getting clicks". Also reviews pin titles and descriptions when the user pastes them.
---

# Review a Pinterest pin

You look at the pin image yourself and give an honest, specific review. No render and no
InsightPins call is needed, so a review uses none of the user's render limit.

## Steps

1. **Get the pin.** An uploaded image is best. If the user gives only a link to a Pinterest pin
   page, ask them to upload the image (you may not be able to see it through the link). Ask for the
   pin title, description and destination URL too if they want those reviewed; they're optional.

2. **Understand it.** Identify the content type (how-to, listicle, product, recipe, quote, travel,
   lifestyle), the headline, the photo, the layout, the colors and the promise to the viewer.

3. **Score it** with the rubric in [references/scoring-rubric.md](references/scoring-rubric.md):
   each criterion 1-10, then the weighted overall score. Be calibrated: most pins are 5-7; reserve
   9-10 for pins with nothing meaningful to fix. Base every score on something visible in the pin.

4. **Find the fixes that matter most.** Rank by expected impact on clicks and saves. Readability
   and the clarity of the promise usually matter more than color nuances.

5. **Write the review** in this shape:

   ```
   Overall: 6.5/10 - one-line verdict

   What works
   - ...

   Top fixes (biggest impact first)
   1. Problem -> concrete fix
   2. ...
   3. ...

   Scores
   | Criterion | Score | Note |

   Better headline options
   - ... (2-3 options, different angles)
   ```

   If title/description were given, add a short "Copy" section with an improved title and
   description, following the `pin-copy` skill.

6. **Offer the next step**: render improved versions with `/insightpins:optimize-pin`, or a new pin
   in a similar style for their own page with the `remake-pin` skill.

## Tone

Direct and useful, like a good designer friend. Say what's wrong plainly, but always with a fix.
Don't pad with generic advice that doesn't apply to this pin. If it's a strong pin, say so and keep
the fix list short.

## Limits

- You can't see the pin's real performance data. If the user shares impressions, saves, outbound
  clicks or click-through rate, use them: low impressions point to keywords/topic and freshness; good
  impressions but few clicks point to the image, headline and promise.
- Don't guess at Pinterest's ranking internals. Stick to what is visible and widely established.
