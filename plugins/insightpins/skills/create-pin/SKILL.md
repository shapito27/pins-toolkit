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
   - **Check that the page really loaded.** Many large sites block automated requests. Treat it as a
     failure when `extract_url` errors ("Access denied", 404) **or** returns a bot-check page: a title
     like "Client Challenge", "Just a moment...", "One moment, please", "Access denied", "Attention
     Required", "Verify you are human", usually with no images. Don't build a pin from that. Tell the
     user the site blocked the request and ask for the page title (or a short summary) and a direct
     image URL, then continue.
   - The page's description is often a chatty intro, not a summary. Write your own copy from what the
     page is about.
   - No URL: ask for the topic, the headline idea, an image URL and the site name. Don't invent a site name.
   - An image uploaded into the chat cannot be used as the pin photo (the tool needs a URL). Ask for a URL for it, or use a page image.

2. **Classify the content**: how-to/blog post, listicle (has a number), product, recipe, quote,
   travel/destination, or lifestyle/inspiration. Pull out facts the templates can show: the list
   number, price, cook time, servings, category.

3. **Write the copy** using the `pin-copy` skill: a short on-image headline (3-8 words, ideally),
   an optional subtitle, and separately the Pinterest title, description and alt text.
   Use only facts the page states: don't add selling points like "one-pan", "ready in 20 minutes"
   or "kid-friendly" unless the page says so.

4. **Pick the template.** Call `list_templates` (the list changes over time) and choose with
   [references/template-selection.md](references/template-selection.md). Fill `custom_fields` from
   real content only, for example `listNumber: "17"` for "17 Easy Dinners". Fields you don't pass are
   left off the pin, so omit any you don't have a real value for (never invent a price, cook time or
   count). Exception: `number-badge` and `side-panels` always show a number, so use them only when the
   content has one.

5. **Pick the style.** Call `list_styles` and choose a palette and font pairing with
   [references/style-selection.md](references/style-selection.md). If the user or their site has
   colors already used on earlier pins, keep them for brand consistency.

6. **Pick the photo** from the extracted images. You can't see them before rendering, so judge by the
   URL and file name too:
   - relevant to the headline, sharp, large, ideally vertical (2:3);
   - skip tracking pixels and tiny files (`.gif?`, `1x1`, `pixel`), logos, favicons, icons, footer or
     banner graphics, author headshots, ads, and thumbnails (sizes like `200x200` or `150x150` in the name);
   - skip **animated GIFs**: they're usually demo clips with captions baked in, and get cropped badly;
   - skip images that likely contain text: names with `infographic`, `pin`, `collage`, `chart`,
     `before-after`, `screenshot`, `quote`;
   - a size in the file name hints at orientation (`689x1024` is vertical, `1200x628` horizontal).
   **Match the photo to the template:** full-bleed templates (photo fills the whole pin, such as
   `bold-title`, `gradient-wave`, `corner-badge`, `travel-overlay`, `destination-card`) need a
   vertical photo, or heads and products get cut off. For a horizontal, square or unknown-shape photo,
   use a template that puts the photo in a panel (`split-horizontal`, `recipe-card`, `image-focus`,
   `minimal-clean`, `product-spotlight`, `story-card`).
   Use `additional_image_urls` only for collage templates, with photos that clearly belong together.

7. **Check quota before more than one render.** Call `get_quota` when making variations or when a
   render failed for limits. Tell the user how many renders a plan will use if they're running low.

8. **Render** with `render_pin`: template, palette, font, headline as `title`, subtitle as
   `description` (only on templates that support it), `site_name`, `image_url`, and a CTA that fits
   the content ("Get the Recipe", "Read the Guide", "Shop Now", "See the List"; 30 characters max).
   **Set `text_size` on the first render**; the template default (100) is usually too small at
   thumbnail size. Headlines up to ~7 words: 130-160. Longer headlines or quotes: 120-140. Very long
   text: 100-110 (or shorten it). On templates with a subtitle, keep `description_size` at 100-115.

9. **Check the preview** against the `pin-design` checklist. The preview image is about 200x300,
   which is roughly how the pin looks in a phone feed, so use it as the thumbnail test: if you
   struggle to read the headline in the preview, so will users. Re-render only for a real defect:
   unreadable or cut-off text, a badly cropped photo (cut-off heads, text baked into the photo cut in
   half), a wrong photo, or a field showing a value that isn't true.
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
