---
name: create-pin
description: Create a Pinterest pin image with the InsightPins connector. Use when the user wants a pin, pin image, pin graphic or Pinterest image for a URL, blog post, article, product, recipe, listicle or quote, says "make a pin", "pin this" or "turn this into a pin", or asks for several pin variations of one page.
---

# Create a Pinterest pin

You make finished 1000x1500 pins with the InsightPins connector (`extract_url`, `list_templates`,
`list_styles`, `render_pin`, `get_quota`). This skill adds the judgement: which template, which
photo, which words. Apply the `pin-design` and `pin-copy` skills while you work.

If the InsightPins tools are not available, tell the user to connect **InsightPins** on the
plugin's Connectors tab (or run `/mcp` in Claude Code), then continue once it's connected. You can
still draft the copy without it.

## Workflow

1. **Get the source.**
   - URL given: call `extract_url`. Note the title, description, site name and every image.
   - No URL: ask for the topic, the headline idea, an image URL and the site name. Don't invent a site name.
   - An image uploaded into the chat cannot be used as the pin photo (the tool needs a URL). Ask for a URL for it, or use a page image.

2. **Classify the content**: how-to/blog post, listicle (has a number), product, recipe, quote,
   travel/destination, or lifestyle/inspiration. Pull out facts the templates can show: the list
   number, price, cook time, servings, category.

3. **Write the copy** using the `pin-copy` skill: a short on-image headline (3-8 words, ideally),
   an optional subtitle, and separately the Pinterest title, description and alt text.

4. **Pick the template.** Call `list_templates` (the list changes over time) and choose with
   [references/template-selection.md](references/template-selection.md). Fill `custom_fields` from
   real content only, for example `listNumber: "17"` for "17 Easy Dinners". Never leave a template's
   default placeholder like "$29.99" or "TOP 10" on a pin; pick another template if you have no value.

5. **Pick the style.** Call `list_styles` and choose a palette and font pairing with
   [references/style-selection.md](references/style-selection.md). If the user or their site has
   colors already used on earlier pins, keep them for brand consistency.

6. **Pick the photo** from the extracted images:
   - relevant to the headline, sharp, large, ideally vertical or easy to crop to 2:3;
   - no text, logos or watermarks already in it;
   - not a site logo, icon, ad, author headshot or tiny thumbnail.
   Use `additional_image_urls` only for collage templates, with photos that clearly belong together.

7. **Check quota before more than one render.** Call `get_quota` when making variations or when a
   render failed for limits. Tell the user how many renders a plan will use if they're running low.

8. **Render** with `render_pin`: template, palette, font, headline as `title`, subtitle as
   `description` (only on templates that support it), `site_name`, `image_url`, and a CTA that fits
   the content ("Get the Recipe", "Read the Guide", "Shop Now", "See the List"; 30 characters max).
   For long headlines lower `text_size`; for short punchy ones raise it (120-160).

9. **Check the preview** against the `pin-design` checklist. Re-render only for a real defect:
   unreadable or cut-off text, wrong or poorly cropped photo, a default placeholder left on the pin.
   Fix the one thing that's wrong (usually `text_size`, `title_size` or the photo) and keep the rest.
   Don't re-render for taste alone unless the user asks.

10. **Report** (keep it short):
    - the image link from the latest render and its `edit_url` (opens the pin on insightpins.com
      for editing without using a render);
    - template, palette and font used;
    - the link expires in 7 days, so download the image;
    - where the photo came from, and that they need the right to publish it;
    - ready to paste: **Pinterest title**, **description**, **alt text**, **suggested board**,
      and the destination link (the source URL).

## Variations

When asked for several pins for one page (or via `/insightpins:pin-variations`), make each pin
different in a way that matters: a different photo, a different template category and a different
headline angle (see `pin-copy` angles). Changing only the color is not a variation. Present a short
table: pin, angle, template, link. Suggest posting them over several days or weeks, not all at once.

## When a limit is hit

If a render fails because the daily limit is reached, say so once: how many renders were used,
when the limit resets (00:00 UTC) and, if the tool's response gives an upgrade or plans link, share
it. Then offer what doesn't need a render: finished copy, the chosen settings so they can render
later, or the `edit_url` of an earlier pin.
